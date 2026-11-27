from datetime import date, timedelta

from .content import SOURCE_LIMIT, STDIN_LIMIT, is_parsons_order
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
        self.clock = clock
        self.runner = runner

    def playable(self, uid):
        expect(isinstance(uid, str) and uid in self.catalog.play, "Unit not found", 404)
        return self.catalog.units[uid]

    def version(self, uid):
        return self.catalog.units[uid]["version"]

    def completed(self, db):
        return {row["step_id"] for row in db.execute(
            """SELECT p.step_id FROM step_progress AS p
               JOIN steps AS s ON s.id=p.step_id
               JOIN units AS u ON u.id=s.unit_id AND u.version=p.unit_version
               WHERE p.complete=1"""
        )}

    def current(self, uid, done):
        return next((key for key in self.catalog.play[uid] if key not in done), None)

    def skips(self, db):
        return dict(db.execute(
            """SELECT s.unit_id, s.recommend FROM unit_skips AS s
               JOIN units AS u ON u.id=s.unit_id AND u.version=s.unit_version"""
        ))

    def activity(self, db):
        return dict(db.execute(
            """SELECT unit_id, MAX(resumed) FROM (
                   SELECT a.unit_id, a.id AS attempt_id, a.action='resume' AS resumed
                   FROM attempts AS a
                   JOIN units AS u ON u.id=a.unit_id AND u.version=a.unit_version
                   UNION ALL
                   SELECT s.unit_id, NULL, 0 FROM step_progress AS p
                   JOIN steps AS s ON s.id=p.step_id
                   JOIN units AS u ON u.id=s.unit_id AND u.version=p.unit_version
               ) GROUP BY unit_id ORDER BY MAX(attempt_id) DESC, unit_id"""
        ))

    def blockers(self, uid, done, skips, activity):
        if uid in skips or uid in activity:
            return []
        return [key for key in self.catalog.units[uid]["prerequisites"]
                if key in self.catalog.play and key not in skips and self.current(key, done)]

    def require_open(self, db, uid, done):
        blocked = self.blockers(uid, done, self.skips(db), self.activity(db))
        if blocked:
            names = ", ".join(self.catalog.units[key]["title"] for key in blocked)
            raise RequestError(f"Complete or skip first: {names}", 409)

    def unit_summary(self, uid, done, skips, activity):
        sequence = self.catalog.play.get(uid, [])
        count = sum(key in done for key in sequence)
        unit = self.catalog.units[uid]
        return {
            "id": uid, "title": unit["title"],
            "total": len(sequence), "completed": count,
            "status": "completed" if sequence and count == len(sequence) else unit["status"],
            "skipped": uid in skips, "recommend": bool(skips.get(uid)),
            "blockers": [{"id": key, "title": self.catalog.units[key]["title"]}
                         for key in self.blockers(uid, done, skips, activity)] if sequence else [],
            "placement": uid in self.catalog.placements,
        }

    def path(self, db):
        done, skips, activity = self.completed(db), self.skips(db), self.activity(db)
        stages = {number: {"number": number, "title": title, "modules": []}
                  for number, title in self.catalog.stages.items()}
        modules = {}
        for mid, module in self.catalog.modules.items():
            modules[mid] = {"id": mid, "title": module["title"], "units": []}
            stages[module["stage"]]["modules"].append(modules[mid])
        for uid, unit in self.catalog.units.items():
            modules[unit["module_id"]]["units"].append(self.unit_summary(uid, done, skips, activity))
        return {"stages": list(stages.values())}

    def reference(self, db, uid):
        unit = self.playable(uid)
        self.require_open(db, uid, self.completed(db))
        return {"title": unit["title"], **self.catalog.resources[uid]}

    def today(self, db, today):
        day = today.isoformat()
        done, skips, activity = self.completed(db), self.skips(db), self.activity(db)
        units = {uid: self.unit_summary(uid, done, skips, activity)
                 for uid in self.catalog.units if uid in self.catalog.play}
        open_units = {uid: unit for uid, unit in units.items() if not unit["blockers"]}
        unfinished = {uid: unit for uid, unit in open_units.items()
                      if unit["status"] != "completed" and (uid not in skips or activity.get(uid))}
        candidates = [*activity, *unfinished]
        selected = next((unfinished[uid] for uid in candidates if uid in unfinished), None)
        if selected is None:
            selected = next((open_units[uid] for uid in [*activity, *open_units]
                             if uid in open_units and uid not in skips), None)
        remaining = [key for uid in unfinished for key in self.catalog.play[uid] if key not in done]
        code_remaining = sum(self.catalog.steps[key]["type"] in {"fix", "code"} for key in remaining)
        quest = dict(db.execute("SELECT kind, progress FROM daily_quest WHERE day=?", (day,)))
        due = len(self.due(db, day))
        reviewed = min(DAILY_REVIEW_LIMIT, quest.get("review", 0))
        steps = quest.get("step", 0)
        code = quest.get("code", 0)
        return {
            "unit": selected, "recommended": [unit for unit in open_units.values() if unit["recommend"]],
            "xp": db.execute("SELECT COALESCE(SUM(points), 0) FROM xp_events").fetchone()[0],
            "streak": streak(db, today), "due": due, "date": day,
            "quests": {
                "step": {"progress": steps, "target": min(3, steps + len(remaining))},
                "code": {"progress": code, "target": min(1, code + code_remaining)},
                "review": {"progress": reviewed, "target": min(DAILY_REVIEW_LIMIT, due + reviewed)},
            },
        }

    def step_view(self, db, uid, selected=None):
        unit = self.playable(uid)
        done = self.completed(db)
        self.require_open(db, uid, done)
        sequence = self.catalog.play[uid]
        current = self.current(uid, done)
        completed = [
            {"id": key, "title": f"{index}. {self.step_title(key)}"}
            for index, key in enumerate(sequence, 1) if key in done
        ]
        expect(selected is None or (selected in sequence and selected in done),
               "This step is not completed", 404)
        key = current if selected is None else selected
        result = {"step": None, "unit": unit["title"], "completed_steps": completed,
                  "total": len(sequence)}
        if key is None:
            return result
        raw = self.catalog.steps[key]
        view = {key: raw[key] for key in ("type", "body", "code", "task", "prompt", "rubric") if key in raw}
        view.update(id=key, title=self.step_title(key), complete=key in done)
        state = self.state(db, uid, key)
        if "choices" in raw:
            view["choices"] = [item["text"] for item in raw["choices"]]
            if view["complete"]:
                view["feedback"] = self.feedback(raw, True)
        if raw["type"] == "parsons":
            view["lines"] = raw["lines"] if view["complete"] else list(reversed(raw["lines"]))
        if key in self.catalog.problems:
            problem = self.catalog.problems[key]
            view.update(starter=problem.starter, tests=bool(problem.test_body),
                        can_open_solution=bool(
                            problem.solution and (view["complete"] or state["failures"] >= 3)
                        ),
                        failures=state["failures"])
        hints = self.hints(key)
        view.update(hints=list(hints[:state["hints"]]), max_hints=len(hints))
        return {**result, "step": view, "index": sequence.index(key) + 1}

    def step_title(self, key):
        return self.catalog.steps[key].get("title", "What will Python print?")

    def state(self, db, uid, key):
        return db.execute(
            "SELECT * FROM step_progress WHERE step_id=? AND unit_version=?", (key, self.version(uid))
        ).fetchone() or {"complete": 0, "failures": 0, "hints": 0}

    def hints(self, key):
        if key in self.catalog.problems:
            return self.catalog.problems[key].hints
        return self.catalog.steps[key].get("hint_levels", ())

    def attempt(self, db, uid, key, day, action, result, answer=None):
        db.execute(
            """INSERT INTO attempts (unit_id, step_id, unit_version, day, action, result, answer)
               VALUES (?, ?, ?, ?, ?, ?, ?)""", (uid, key, self.version(uid), day, action, result, answer),
        )

    def record_resumed_progress(self, db, uid, key, day):
        db.execute(
            """INSERT INTO attempts (unit_id, step_id, unit_version, day, action, result)
               SELECT s.unit_id, ?, s.unit_version, ?, 'resume', 'progress'
               FROM unit_skips AS s WHERE s.unit_id=? AND s.unit_version=? AND NOT EXISTS (
                   SELECT 1 FROM attempts AS a WHERE a.unit_id=s.unit_id
                   AND a.unit_version=s.unit_version AND a.action='resume'
               )""", (key, day, uid, self.version(uid)),
        )

    def complete(self, db, uid, key, day, points):
        db.execute(
            """INSERT INTO step_progress (step_id, unit_version, complete) VALUES (?, ?, 1)
               ON CONFLICT(step_id, unit_version) DO UPDATE SET complete=1""", (key, self.version(uid)),
        )
        self.record_resumed_progress(db, uid, key, day)
        if points:
            award(db, f"step:{key}:{self.version(uid)}", day, points)
        progress(db, day, "step")
        if self.current(uid, self.completed(db)) is None:
            db.execute("UPDATE unit_skips SET recommend=0 WHERE unit_id=? AND unit_version=?",
                       (uid, self.version(uid)))
            vocab = [card_id for card_id, card in self.catalog.cards.items()
                     if card["unit"] == uid and card["kind"] == "vocab"]
            self.queue_cards(db, vocab, date.fromisoformat(day) + timedelta(days=1))

    def play(self, db, body, today):
        uid, action = body.get("unit"), body.get("action")
        self.playable(uid)
        done = self.completed(db)
        self.require_open(db, uid, done)
        current = self.current(uid, done)
        if action == "start":
            fields(body, "unit", "action")
            if current:
                self.attempt(db, uid, current, today.isoformat(), action, "opened")
            return {"started": current is not None}

        key = body.get("step")
        expect(isinstance(key, str) and key in self.catalog.play[uid], "Step not found", 404)
        expect(isinstance(action, str), "Invalid action")
        step = self.catalog.steps[key]
        kind, day = step["type"], today.isoformat()
        state = self.state(db, uid, key)
        problem = self.catalog.problems.get(key)

        if action == "solution":
            fields(body, "unit", "step", "action")
            expect(problem and problem.solution and (state["complete"] or state["failures"] >= 3),
                   "The solution is still locked", 409)
            return {"solution": problem.solution, "explanation": problem.explanation}

        expect(key == current, "Refresh Play to resume from the current step", 409)
        if action == "hint":
            fields(body, "unit", "step", "action", "level")
            hints, level = self.hints(key), body["level"]
            expect(type(level) is int and 1 <= level <= min(len(hints), state["hints"] + 1),
                   "Invalid hint level")
            db.execute(
                """INSERT INTO step_progress (step_id, unit_version, hints) VALUES (?, ?, ?)
                   ON CONFLICT(step_id, unit_version) DO UPDATE SET hints=MAX(hints, excluded.hints)
                """, (key, self.version(uid), level),
            )
            if level > state["hints"]:
                self.record_resumed_progress(db, uid, key, day)
            return {"hint": hints[level - 1]}

        if kind == "read" and action == "continue":
            fields(body, "unit", "step", "action")
            self.attempt(db, uid, key, day, action, "read")
            self.complete(db, uid, key, day, 2)
            return {"complete": True}
        if kind == "explain" and action == "explain":
            fields(body, "unit", "step", "action", "response", "self_checked")
            expect(bool(text(body["response"], STDIN_LIMIT).strip()), "Write your explanation first")
            expect(body["self_checked"] is True, "Check your explanation against the rubric")
            self.attempt(db, uid, key, day, action, "self-checked")
            self.complete(db, uid, key, day, 2)
            return {"complete": True}
        if kind == "predict" and action == "answer":
            fields(body, "unit", "step", "action", "choice")
            answer = choice_index(body["choice"], step["choices"])
            correct = answer == step["answer"]
            self.attempt(db, uid, key, day, action, "correct" if correct else "wrong", answer)
            if key in self.catalog.cards:
                self.schedule(db, key, today, "practice", answer_grade(correct, state["hints"]))
            self.complete(db, uid, key, day, max(1, 5 - state["hints"]) if correct else 2)
            return {"complete": True, **self.feedback(step, correct)}
        if kind == "parsons" and action == "order":
            fields(body, "unit", "step", "action", "order")
            order = body["order"]
            line_count = len(step["lines"])
            expect(is_parsons_order(order, line_count), "Use each line exactly once")
            authored_order = [line_count - 1 - index for index in order]
            correct = (authored_order == list(range(line_count))
                       or authored_order in step.get("accepted_orders", []))
            self.attempt(db, uid, key, day, action, "correct" if correct else "wrong")
            if correct:
                self.complete(db, uid, key, day, 5)
            return {"complete": correct, "stdout": step["expected_stdout"] if correct else ""}

        expect(problem is not None and (action == "run" or (action == "tests" and problem.test_body)),
               "Invalid action for this step")
        return self.run(db, body, uid, key, step, action, state, day)

    def run(self, db, body, uid, key, step, action, state, day):
        if action == "run":
            fields(body, "unit", "step", "action", "source", "stdin")
            source = text(body["source"], SOURCE_LIMIT)
            result = self.runner(key, source, text(body["stdin"], STDIN_LIMIT))
            complete = False
            if step["type"] == "try" and result["status"] == "passed":
                check = step["check"]
                stdout = result["stdout"]
                if "stdout_line" in check:
                    complete = check["stdout_line"] in stdout.splitlines()
                else:
                    complete = check["stdout_contains"] in stdout
            if result["status"] != "unavailable":
                self.attempt(db, uid, key, day, action, result["status"])
            if complete:
                self.complete(db, uid, key, day, 0)
            return {**result, "complete": complete}

        fields(body, "unit", "step", "action", "source")
        result = self.runner(key, text(body["source"], SOURCE_LIMIT))
        status = result["status"]
        failures = state["failures"]
        if status != "unavailable":
            self.attempt(db, uid, key, day, action, status)
            if status == "passed":
                self.complete(db, uid, key, day, 15 - 3 * state["hints"])
                progress(db, day, "code")
            else:
                failures += 1
                db.execute(
                    """INSERT INTO step_progress (step_id, unit_version, failures) VALUES (?, ?, 1)
                       ON CONFLICT(step_id, unit_version) DO UPDATE SET failures=failures+1""",
                    (key, self.version(uid)),
                )
                self.record_resumed_progress(db, uid, key, day)
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
            """INSERT INTO review_logs (card_id, day, event, grade, stability, difficulty, revision)
               VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(card_id, day, event, revision) DO NOTHING""",
            (key, day, event, grade, memory.stability, memory.difficulty, stored["revision"]),
        )
        if log.rowcount:
            db.execute(
                """UPDATE review_cards SET due_day=?, last_day=?, stability=?, difficulty=?
                   WHERE id=?""",
                (due_date(memory).isoformat(), day, memory.stability, memory.difficulty, key),
            )

    def due(self, db, day):
        reviewed = db.execute(
            "SELECT COUNT(*) FROM review_logs WHERE day=? AND event='due'", (day,),
        ).fetchone()[0]
        room = max(0, DAILY_REVIEW_LIMIT - reviewed)
        rows = db.execute("SELECT id, due_day FROM review_cards WHERE due_day<=? ORDER BY due_day,id",
                          (day,))
        return [(row["id"], row["due_day"]) for row in rows if row["id"] in self.catalog.cards][:room]

    def retries(self, db, day):
        return [row[0] for row in db.execute(
            """SELECT missed.card_id FROM review_logs AS missed
               JOIN review_cards AS card ON card.id=missed.card_id AND card.revision=missed.revision
               WHERE missed.day=? AND missed.event='due' AND missed.grade=? AND NOT EXISTS (
                   SELECT 1 FROM review_logs AS retry
                   WHERE retry.card_id=missed.card_id AND retry.day=missed.day AND retry.event='retry'
                     AND retry.revision=missed.revision
               ) ORDER BY missed.id""", (day, Grade.AGAIN),
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
        def review_question(key):
            uid = self.catalog.cards[key]["unit"]
            return {**self.question(key), "unit": self.catalog.units[uid]["title"]}

        day = today.isoformat()
        return {
            "due": [{**review_question(key), "due_day": due_day} for key, due_day in self.due(db, day)],
            "retries": [review_question(key) for key in self.retries(db, day)],
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
        uid = self.catalog.cards[key]["unit"]
        if not correct and self.current(uid, self.completed(db)) is not None:
            db.execute(
                "UPDATE unit_skips SET recommend=1 WHERE unit_id=? AND unit_version=?",
                (uid, self.version(uid)),
            )
        return self.feedback(question, correct)

    def placement_spec(self, uid):
        self.playable(uid)
        expect(uid in self.catalog.placements, "Placement not found", 404)
        return self.catalog.placements[uid]

    def placement(self, db, uid):
        spec = self.placement_spec(uid)
        result = self.placement_result(db, uid)
        skipped = uid in self.skips(db)
        return {
            "unit": self.catalog.units[uid]["title"], "title": spec["title"],
            "questions": [self.question(key) for key in spec["questions"]],
            "starter": self.catalog.problems[spec["problem"]].starter,
            "minimum_correct": spec["minimum_correct"],
            "result": dict(result) if result else None,
            "skipped": skipped,
            "can_skip": bool(result and result["passed"] and not skipped
                             and self.current(uid, self.completed(db))),
        }

    def placement_result(self, db, uid):
        return db.execute(
            """SELECT correct, questions, code_passed, passed FROM placement_results
               WHERE unit_id=? AND unit_version=? ORDER BY id DESC LIMIT 1""", (uid, self.version(uid))
        ).fetchone()

    def place(self, db, body, today):
        fields(body, "unit", "answers", "source")
        uid = body["unit"]
        spec = self.placement_spec(uid)
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
            (uid, self.version(uid), today.isoformat(), correct, len(questions), code_passed, passed),
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

    def skip(self, db, body, today):
        fields(body, "unit")
        uid = body["unit"]
        self.placement_spec(uid)
        result = self.placement_result(db, uid)
        expect(result and result["passed"] and self.current(uid, self.completed(db)) is not None,
               "A passing placement result is required", 409)
        inserted = db.execute(
            """INSERT INTO unit_skips (unit_id, unit_version, day) VALUES (?, ?, ?)
               ON CONFLICT(unit_id, unit_version) DO NOTHING""",
            (uid, self.version(uid), today.isoformat()),
        )
        if inserted.rowcount:
            predictions = [key for key, card in self.catalog.cards.items()
                           if card["unit"] == uid and card["kind"] == "predict"]
            self.queue_cards(db, predictions, today)
        return {"skipped": True}
