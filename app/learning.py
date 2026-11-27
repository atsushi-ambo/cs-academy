from datetime import date, timedelta

from .content import LISTS, SOURCE_LIMIT, STDIN_LIMIT
from .execution import run_problem
from .fsrs import Grade, Memory, answer_grade, due_date, update

DAILY_REVIEW_LIMIT = 10
CARDS_PER_DAY = 2


class RequestError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def expect(condition, message, status=400):
    if not condition:
        raise RequestError(message, status)


def fields(body, *keys):
    expect(set(body) == set(keys), "Invalid request fields")


def text(value, limit):
    expect(isinstance(value, str), "Expected text")
    try:
        size = len(value.encode("utf-8"))
    except UnicodeError as error:
        raise RequestError("Invalid UTF-8 text") from error
    expect(size <= limit, "Text is too long")
    return value


def choice_index(value, choices):
    expect(type(value) is int and 0 <= value < len(choices), "Invalid choice")
    return value


def progress(db, day, kind, count=1):
    db.execute(
        """INSERT INTO daily_quest VALUES (?, ?, ?) ON CONFLICT(day, kind) DO UPDATE
           SET progress=progress+excluded.progress""", (day, kind, count),
    )


def award(db, key, day, points):
    db.execute("INSERT INTO xp_events VALUES (?, ?, ?) ON CONFLICT(event_key) DO NOTHING",
               (key, day, points))


def streak(db, today):
    active = [date.fromisoformat(row[0]) for row in db.execute(
        "SELECT DISTINCT day FROM xp_events WHERE day <= ? ORDER BY day DESC", (today.isoformat(),)
    )]
    cursor = today - timedelta(days=1) if today not in active else today
    missed = {}
    count = 0
    for learned in active:
        while cursor > learned:
            week = cursor.isocalendar()[:2]
            missed[week] = missed.get(week, 0) + 1
            if missed[week] > 2:
                return count
            cursor -= timedelta(days=1)
        count += 1
        cursor = learned - timedelta(days=1)
    return count


class Learning:
    def __init__(self, store, *, clock=date.today, runner=run_problem):
        self.store = store
        self.catalog = store.catalog
        self.unit = self.catalog.units[LISTS]
        self.version = self.unit["version"]
        self.sequence = self.catalog.play[LISTS]
        self.clock = clock
        self.runner = runner

    def completed(self, db):
        return {row[0] for row in db.execute(
            "SELECT step_id FROM step_progress WHERE unit_version=? AND complete=1", (self.version,)
        )}

    def current(self, db):
        done = self.completed(db)
        return next((key for key in self.sequence if key not in done), None)

    def skipped(self, db):
        return db.execute(
            "SELECT recommend FROM unit_skips WHERE unit_id=? AND unit_version=?",
            (LISTS, self.version),
        ).fetchone()

    def today(self, db, today):
        day = today.isoformat()
        done = self.completed(db)
        skip = self.skipped(db)
        quest = dict(db.execute("SELECT kind, progress FROM daily_quest WHERE day=?", (day,)))
        due = len(self.due(db, day))
        reviewed = quest.get("review", 0)
        return {
            "unit": self.unit["title"], "total": len(self.sequence),
            "completed": sum(key in done for key in self.sequence),
            "skipped": skip is not None, "recommend": skip is not None and bool(skip["recommend"]),
            "xp": db.execute("SELECT COALESCE(SUM(points), 0) FROM xp_events").fetchone()[0],
            "streak": streak(db, today), "due": due, "date": day,
            "quests": {
                "step": {"progress": quest.get("step", 0), "target": 3},
                "code": {"progress": quest.get("code", 0), "target": 1},
                "review": {"progress": reviewed, "target": min(DAILY_REVIEW_LIMIT, due + reviewed)},
            },
        }

    def step_view(self, db):
        key = self.current(db)
        if key is None:
            return {"step": None, "unit": self.unit["title"]}
        raw = self.catalog.steps[key]
        view = {key: raw[key] for key in ("type", "body", "code", "task") if key in raw}
        view.update(id=key, title=raw.get("title", "What will Python print?"))
        state = self.state(db, key)
        if "choices" in raw:
            view["choices"] = [item["text"] for item in raw["choices"]]
        if raw["type"] == "parsons":
            view["lines"] = list(reversed(raw["lines"]))
        if key in self.catalog.problems:
            problem = self.catalog.problems[key]
            view.update(starter=problem.starter, tests=bool(problem.test_body),
                        can_open_solution=bool(problem.solution and state["failures"] >= 3),
                        failures=state["failures"])
        hints = self.hints(key)
        view.update(hints=list(hints[:state["hints"]]), max_hints=len(hints))
        return {"step": view, "index": self.sequence.index(key) + 1, "total": len(self.sequence),
                "unit": self.unit["title"]}

    def state(self, db, key):
        return db.execute(
            "SELECT * FROM step_progress WHERE step_id=? AND unit_version=?", (key, self.version)
        ).fetchone() or {"complete": 0, "failures": 0, "hints": 0}

    def hints(self, key):
        if key in self.catalog.problems:
            return self.catalog.problems[key].hints
        return self.catalog.steps[key].get("hint_levels", ())

    def attempt(self, db, key, day, action, result, answer=None):
        db.execute(
            """INSERT INTO attempts (unit_id, step_id, unit_version, day, action, result, answer)
               VALUES (?, ?, ?, ?, ?, ?, ?)""", (LISTS, key, self.version, day, action, result, answer),
        )

    def complete(self, db, key, day, points):
        db.execute(
            """INSERT INTO step_progress (step_id, unit_version, complete) VALUES (?, ?, 1)
               ON CONFLICT(step_id, unit_version) DO UPDATE SET complete=1""", (key, self.version),
        )
        if points:
            award(db, f"step:{key}:{self.version}", day, points)
        progress(db, day, "step")
        if self.current(db) is None:
            db.execute("UPDATE unit_skips SET recommend=0 WHERE unit_id=? AND unit_version=?",
                       (LISTS, self.version))
            vocab = [card_id for card_id, card in self.catalog.cards.items()
                     if card["unit"] == LISTS and card["kind"] == "vocab"]
            self.queue_cards(db, vocab, date.fromisoformat(day) + timedelta(days=1))

    def play(self, db, body, today):
        key, action = body.get("step"), body.get("action")
        expect(isinstance(key, str) and key in self.sequence and isinstance(action, str),
               "Unknown step or action")
        step = self.catalog.steps[key]
        kind, day = step["type"], today.isoformat()
        state = self.state(db, key)
        problem = self.catalog.problems.get(key)

        if action == "solution":
            fields(body, "step", "action")
            expect(problem and problem.solution and (state["complete"] or state["failures"] >= 3),
                   "The solution is still locked", 409)
            return {"solution": problem.solution, "explanation": problem.explanation}

        expect(key == self.current(db), "Refresh Play to resume from the current step", 409)
        if action == "hint":
            fields(body, "step", "action", "level")
            hints, level = self.hints(key), body["level"]
            expect(type(level) is int and 1 <= level <= min(len(hints), state["hints"] + 1),
                   "Invalid hint level")
            db.execute(
                """INSERT INTO step_progress (step_id, unit_version, hints) VALUES (?, ?, ?)
                   ON CONFLICT(step_id, unit_version) DO UPDATE SET hints=MAX(hints, excluded.hints)
                """, (key, self.version, level),
            )
            return {"hint": hints[level - 1]}

        if kind == "read" and action == "continue":
            fields(body, "step", "action")
            self.complete(db, key, day, 2)
            return {"complete": True}
        if kind == "predict" and action == "answer":
            fields(body, "step", "action", "choice")
            answer = choice_index(body["choice"], step["choices"])
            correct = answer == step["answer"]
            self.attempt(db, key, day, action, "correct" if correct else "wrong", answer)
            if key in self.catalog.cards:
                self.schedule(db, key, today, "practice", answer_grade(correct, state["hints"]))
            self.complete(db, key, day, max(1, 5 - state["hints"]) if correct else 2)
            return {"complete": True, **self.feedback(step, correct)}
        if kind == "parsons" and action == "order":
            fields(body, "step", "action", "order")
            order = body["order"]
            correct_order = list(reversed(range(len(step["lines"]))))
            expect(isinstance(order, list) and len(order) == len(correct_order)
                   and all(type(i) is int for i in order) and sorted(order) == sorted(correct_order),
                   "Use each line exactly once")
            correct = order == correct_order
            self.attempt(db, key, day, action, "correct" if correct else "wrong")
            if correct:
                self.complete(db, key, day, 5)
            return {"complete": correct, "stdout": step["expected_stdout"] if correct else ""}

        expect(problem is not None and (action == "run" or (action == "tests" and problem.test_body)),
               "Invalid action for this step")
        return self.run(db, body, key, step, action, state, day)

    def run(self, db, body, key, step, action, state, day):
        if action == "run":
            fields(body, "step", "action", "source", "stdin")
            source = text(body["source"], SOURCE_LIMIT)
            result = self.runner(key, source, text(body["stdin"], STDIN_LIMIT))
            check = step.get("check")
            complete = bool(step["type"] == "try" and result["status"] == "passed"
                            and check["stdout_contains"] in result["stdout"])
            if complete:
                self.complete(db, key, day, 0)
            return {**result, "complete": complete}

        fields(body, "step", "action", "source")
        result = self.runner(key, text(body["source"], SOURCE_LIMIT))
        status = result["status"]
        failures = state["failures"]
        if status != "unavailable":
            self.attempt(db, key, day, action, status)
            if status == "passed":
                self.complete(db, key, day, 15 - 3 * state["hints"])
                progress(db, day, "code")
            else:
                failures += 1
                db.execute(
                    """INSERT INTO step_progress (step_id, unit_version, failures) VALUES (?, ?, 1)
                       ON CONFLICT(step_id, unit_version) DO UPDATE SET failures=failures+1""",
                    (key, self.version),
                )
        return {**result, "complete": status == "passed", "failures": failures,
                "can_open_solution": status == "passed" or failures >= 3}

    @staticmethod
    def feedback(question, correct):
        return {"correct": correct, "answer": question["answer"],
                "why": [item["why"] for item in question["choices"]]}

    def schedule(self, db, key, today, event, grade):
        stored = db.execute("SELECT * FROM review_cards WHERE id=?", (key,)).fetchone()
        memory = None
        if stored["last_day"]:
            memory = Memory(stored["stability"], stored["difficulty"],
                            date.fromisoformat(stored["last_day"]))
        memory = update(memory, grade, today)
        day = today.isoformat()
        log = db.execute(
            """INSERT INTO review_logs (card_id, day, event, grade, stability, difficulty)
               VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(card_id, day, event) DO NOTHING""",
            (key, day, event, grade, memory.stability, memory.difficulty),
        )
        if log.rowcount:
            db.execute(
                """UPDATE review_cards SET due_day=?, last_day=?, stability=?, difficulty=?
                   WHERE id=?""",
                (due_date(memory).isoformat(), day, memory.stability, memory.difficulty, key),
            )

    def due(self, db, day):
        reviewed = db.execute(
            "SELECT COUNT(*) FROM review_logs WHERE day=? AND event='due'", (day,)
        ).fetchone()[0]
        room = max(0, DAILY_REVIEW_LIMIT - reviewed)
        rows = db.execute("SELECT id, due_day FROM review_cards WHERE due_day<=? ORDER BY due_day,id",
                          (day,))
        return [(row["id"], row["due_day"]) for row in rows if row["id"] in self.catalog.cards][:room]

    def retries(self, db, day):
        return [row[0] for row in db.execute(
            """SELECT card_id FROM review_logs AS missed
               WHERE day=? AND event='due' AND grade=? AND NOT EXISTS (
                   SELECT 1 FROM review_logs AS retry
                   WHERE retry.card_id=missed.card_id AND retry.day=missed.day AND retry.event='retry'
               ) ORDER BY id""", (day, Grade.AGAIN),
        ) if row[0] in self.catalog.cards]

    def card(self, key):
        card = self.catalog.cards[key]
        return self.catalog.steps[card["step"]] if card["kind"] == "predict" else card

    def question(self, key):
        card = self.card(key)
        return {"id": key, "code": card.get("code"),
                "title": card.get("title", "What will Python print?"),
                "choices": [item["text"] for item in card["choices"]]}

    def reviews(self, db, today):
        day = today.isoformat()
        return {
            "due": [{**self.question(key), "due_day": due_day} for key, due_day in self.due(db, day)],
            "retries": [self.question(key) for key in self.retries(db, day)],
        }

    def review(self, db, body, today):
        fields(body, "card", "choice", "retry")
        key, retry = body["card"], body["retry"]
        expect(isinstance(key, str) and key in self.catalog.cards and type(retry) is bool,
               "Invalid review request")
        day = today.isoformat()
        due = self.due(db, day)
        if retry:
            available = not due and key in self.retries(db, day)
        else:
            available = any(key == card_id for card_id, _ in due)
        expect(available, "This review is no longer available", 409)
        question = self.card(key)
        answer = choice_index(body["choice"], question["choices"])
        correct = answer == question["answer"]
        self.schedule(db, key, today, "retry" if retry else "due", answer_grade(correct))
        if not retry:
            progress(db, day, "review")
            award(db, f"review:{key}:{day}", day, 5 if correct else 2)
        if not correct and self.current(db) is not None:
            db.execute(
                "UPDATE unit_skips SET recommend=1 WHERE unit_id=? AND unit_version=?",
                (self.catalog.cards[key]["unit"], self.version),
            )
        return self.feedback(question, correct)

    def placement(self, db):
        spec = self.catalog.placements[LISTS]
        result = self.placement_result(db)
        return {
            "title": spec["title"], "questions": [self.question(key) for key in spec["questions"]],
            "starter": self.catalog.problems[spec["problem"]].starter,
            "minimum_correct": spec["minimum_correct"],
            "result": dict(result) if result else None,
            "skipped": self.skipped(db) is not None,
            "can_skip": bool(result and result["passed"] and self.current(db) is not None
                             and self.skipped(db) is None),
        }

    def placement_result(self, db):
        return db.execute(
            """SELECT correct, questions, code_passed, passed FROM placement_results
               WHERE unit_id=? AND unit_version=? ORDER BY id DESC LIMIT 1""", (LISTS, self.version)
        ).fetchone()

    def place(self, db, body, today):
        fields(body, "answers", "source")
        spec = self.catalog.placements[LISTS]
        questions = spec["questions"]
        answers = body["answers"]
        expect(isinstance(answers, list) and len(answers) == len(questions),
               "Answer every question")
        correct = 0
        for key, answer in zip(questions, answers, strict=True):
            card = self.card(key)
            correct += choice_index(answer, card["choices"]) == card["answer"]
        result = self.runner(spec["problem"], text(body["source"], SOURCE_LIMIT))
        if result["status"] == "unavailable":
            return {"execution": result}
        code_passed = result["status"] == "passed"
        passed = code_passed and correct >= spec["minimum_correct"]
        summary = {"correct": correct, "questions": len(questions), "passed": passed,
                   "code_passed": code_passed}
        db.execute(
            """INSERT INTO placement_results
               (unit_id, unit_version, day, correct, questions, code_passed, passed)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (LISTS, self.version, today.isoformat(), correct, len(questions), code_passed, passed),
        )
        return {**summary, "execution": result}

    @staticmethod
    def queue_cards(db, card_ids, start):
        unscheduled = [key for key in card_ids if db.execute(
            "SELECT due_day FROM review_cards WHERE id=?", (key,)
        ).fetchone()[0] is None]
        db.executemany(
            "UPDATE review_cards SET due_day=? WHERE id=?",
            (((start + timedelta(days=index // CARDS_PER_DAY)).isoformat(), key)
             for index, key in enumerate(unscheduled)),
        )

    def skip(self, db, today):
        result = self.placement_result(db)
        expect(result and result["passed"] and self.current(db) is not None,
               "A passing placement result is required", 409)
        inserted = db.execute(
            """INSERT INTO unit_skips (unit_id, unit_version, day) VALUES (?, ?, ?)
               ON CONFLICT(unit_id, unit_version) DO NOTHING""",
            (LISTS, self.version, today.isoformat()),
        )
        if inserted.rowcount:
            predictions = [key for key, card in self.catalog.cards.items()
                           if card["unit"] == LISTS and card["kind"] == "predict"]
            self.queue_cards(db, predictions, today)
        return {"skipped": True}
