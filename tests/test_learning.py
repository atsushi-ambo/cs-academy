import sqlite3
import stat
from contextlib import closing
from datetime import date, timedelta
from unittest.mock import patch

from app.fsrs import Grade, update
from app.learning import RequestError
from app.storage import BACKUP_DB, MIGRATIONS, Store, connect, migrate

from .support import LISTS, PLACEMENT_SOURCE, AcademyCase, result


class LearningTest(AcademyCase):
    def play(self, step, action, **fields):
        with self.store.transaction() as db:
            return self.learning.play(
                db, {"unit": LISTS, "step": f"{LISTS}/{step}", "action": action, **fields}, self.date,
            )

    def today(self):
        with self.store.transaction() as db:
            return self.learning.today(db, self.date)

    def test_read_xp_quest_streak_and_no_duplicate_credit(self):
        self.play("st01", "continue")
        with self.assertRaises(RequestError):
            self.play("st01", "continue")
        summary = self.today()
        self.assertEqual(summary["xp"], 2)
        self.assertEqual(summary["quests"]["step"]["progress"], 1)
        self.assertEqual(summary["streak"], 1)
        self.play("st02", "run", source="print(4)", stdin="")
        self.assertEqual(self.today()["xp"], 2)
        self.date += timedelta(days=3)
        self.play("st03", "continue")
        self.assertEqual(self.today()["streak"], 2)
        self.assertEqual(self.today()["quests"]["step"]["progress"], 1)
        self.date += timedelta(days=4)
        self.play("st04", "answer", choice=2)
        self.assertEqual(self.today()["streak"], 1)

    def test_review_cap_and_retry_do_not_add_quest_credit(self):
        with self.store.transaction() as db:
            db.execute("UPDATE review_cards SET due_day=?", (self.date.isoformat(),))
            queue = self.learning.reviews(db, self.date)["due"]
            self.assertEqual(len(queue), 10)
            for item in queue:
                key = item["id"]
                answer = self.learning.card(key)["answer"]
                choice = (answer + 1) % 4 if key == queue[0]["id"] else answer
                self.learning.review(db, {"card": key, "retry": False, "choice": choice}, self.date)
            self.assertEqual(self.learning.reviews(db, self.date)["due"], [])
            key = queue[0]["id"]
            self.assertEqual([item["id"] for item in self.learning.reviews(db, self.date)["retries"]],
                             [key])
            self.learning.review(
                db, {"card": key, "retry": True, "choice": self.learning.card(key)["answer"]},
                self.date,
            )
            self.assertEqual(self.learning.reviews(db, self.date)["retries"], [])
        self.assertEqual(self.today()["quests"]["review"], {"progress": 10, "target": 10})
        self.assertEqual(self.today()["xp"], 47)

    def test_predict_revision_resets_memory_and_retires_old_logs(self):
        self.date = date.today()
        day = self.date.isoformat()
        key = f"{LISTS}/st04"
        with self.store.transaction() as db:
            db.execute("UPDATE review_cards SET due_day=? WHERE id=?", (day, key))
            self.learning.review(db, {"card": key, "choice": 0, "retry": False}, self.date)
            self.assertEqual(self.learning.retries(db, day), [key])
            old_log = dict(db.execute("SELECT * FROM review_logs").fetchone())

        self.store.catalog.steps[key]["answer"] = 0
        self.store.initialize()
        with self.store.transaction() as db:
            card = db.execute("SELECT * FROM review_cards WHERE id=?", (key,)).fetchone()
            self.assertEqual((card["last_day"], card["stability"], card["difficulty"]),
                             (None, None, None))
            self.assertEqual(card["due_day"], day)
            self.assertEqual(self.learning.retries(db, day), [])
            self.assertEqual(self.learning.due(db, day), [(key, day)])
            self.learning.review(db, {"card": key, "choice": 0, "retry": False}, self.date)
            history, current = [dict(row) for row in db.execute("SELECT * FROM review_logs ORDER BY id")]
            self.assertEqual(history, old_log)
            self.assertGreater(current["revision"], history["revision"])
            memory = update(None, Grade.GOOD, self.date)
            self.assertEqual(current["stability"], memory.stability)
            self.assertEqual(current["difficulty"], memory.difficulty)
        self.store.initialize()
        with self.store.transaction() as db:
            card = db.execute("SELECT * FROM review_cards WHERE id=?", (key,)).fetchone()
            self.assertEqual(card["revision"], current["revision"])
            self.assertEqual(card["last_day"], day)

    def test_review_cap_counts_old_revisions(self):
        self.date = date.today()
        key = f"{LISTS}/st04"
        step = self.store.catalog.steps[key]
        revised_answer = (step["answer"] + 1) % len(step["choices"])
        with self.store.transaction() as db:
            db.execute("UPDATE review_cards SET due_day=?", (self.date.isoformat(),))
            queue = self.learning.reviews(db, self.date)["due"]
            self.assertEqual(len(queue), 10)
            self.assertIn(key, [item["id"] for item in queue])
            for item in queue:
                card = item["id"]
                answer = self.learning.card(card)["answer"]
                choice = revised_answer if card == key else answer
                self.learning.review(db, {"card": card, "retry": False, "choice": choice}, self.date)

        step["answer"] = revised_answer
        self.store.initialize()
        with self.store.transaction() as db:
            with self.assertRaises(RequestError) as error:
                self.learning.review(
                    db, {"card": key, "retry": False, "choice": revised_answer}, self.date,
                )
            self.assertEqual(error.exception.status, 409)
            self.assertEqual(self.learning.reviews(db, self.date), {"due": [], "retries": []})
        self.assertEqual(self.today()["quests"]["review"], {"progress": 10, "target": 10})

    def test_review_quest_caps_preexisting_excess_progress(self):
        with self.store.transaction() as db:
            db.execute("INSERT INTO daily_quest VALUES (?, 'review', 11)", (self.date.isoformat(),))
        self.assertEqual(self.today()["quests"]["review"], {"progress": 10, "target": 10})

    def test_predict_revision_preserves_unanswered_placement_due_day(self):
        self.date = date.today()
        key = f"{LISTS}/st09"
        with self.store.transaction() as db:
            self.learning.place(db, {"unit": LISTS, "answers": [2, 0, 3, 2], "source": PLACEMENT_SOURCE}, self.date)
            self.learning.skip(db, {"unit": LISTS}, self.date)
        step = self.store.catalog.steps[key]
        step["answer"] = (step["answer"] + 1) % len(step["choices"])
        self.store.initialize()
        with self.store.transaction() as db:
            card = db.execute("SELECT revision, due_day FROM review_cards WHERE id=?", (key,)).fetchone()
            self.assertEqual(tuple(card), (1, (self.date + timedelta(days=1)).isoformat()))

    def test_restore_legacy_backup_detects_changed_choice_text(self):
        key = f"{LISTS}/st04"
        self.play("st01", "continue")
        self.play("st02", "run", source="print(4)", stdin="")
        self.play("st03", "continue")
        self.play("st04", "answer", choice=2)
        identifier = self.store.backup()
        backup = self.store.backups / identifier / BACKUP_DB
        legacy_path = backup.with_name("legacy.sqlite3")
        with closing(connect(legacy_path)) as legacy:
            with patch("app.storage.MIGRATIONS", MIGRATIONS[:2]):
                migrate(legacy)
            legacy.execute("ATTACH DATABASE ? AS snapshot", (str(backup),))
            with legacy:
                for table in ("stages", "modules", "units", "steps", "review_cards", "review_logs"):
                    columns = ", ".join(row[1] for row in legacy.execute(f"PRAGMA table_info({table})"))
                    legacy.execute(f"INSERT INTO {table} SELECT {columns} FROM snapshot.{table}")
        legacy_path.replace(backup)
        self.store.catalog.steps[key]["choices"][2]["text"] = "Different correct choice"
        self.store.restore(identifier)
        with self.store.transaction() as db:
            card = db.execute("SELECT * FROM review_cards WHERE id=?", (key,)).fetchone()
            self.assertEqual(card["revision"], 1)
            self.assertIsNone(card["last_day"])
            log = db.execute("SELECT card_id, revision, event FROM review_logs").fetchone()
            self.assertEqual(tuple(log), (key, 0, "practice"))

    def test_predict_explanation_edit_preserves_schedule(self):
        key = f"{LISTS}/st04"
        self.play("st01", "continue")
        self.play("st02", "run", source="print(4)", stdin="")
        self.play("st03", "continue")
        self.play("st04", "answer", choice=2)
        with self.store.transaction() as db:
            original = dict(db.execute("SELECT * FROM review_cards WHERE id=?", (key,)).fetchone())
        self.store.catalog.steps[key]["choices"][2]["why"] = "A revised explanation."
        self.store.initialize()
        with self.store.transaction() as db:
            self.assertEqual(
                dict(db.execute("SELECT * FROM review_cards WHERE id=?", (key,)).fetchone()), original,
            )

    def test_try_requires_four_on_its_own_output_line(self):
        self.play("st01", "continue")
        with patch.object(self.learning, "runner", return_value=result(
            "passed", stdout="['web01', 'web02', 'web04']\n3\n",
        )):
            self.assertFalse(self.play("st02", "run", source="unused", stdin="")["complete"])
        self.assertEqual(self.today()["unit"]["completed"], 1)
        with patch.object(self.learning, "runner", return_value=result(
            "passed", stdout="['web01', 'web02', 'web03', 'db01']\n4\n",
        )):
            self.assertTrue(self.play("st02", "run", source="unused", stdin="")["complete"])
        self.assertEqual(self.today()["unit"]["completed"], 2)

    def test_quest_targets_fit_remaining_work(self):
        self.assertEqual(self.today()["quests"]["code"]["target"], 1)
        with self.store.transaction() as db:
            db.executemany(
                "INSERT INTO step_progress (step_id, unit_version, complete) VALUES (?, ?, 1)",
                ((key, self.learning.version(LISTS)) for key in self.store.catalog.play[LISTS]
                 if key != f"{LISTS}/st18"),
            )
        self.assertEqual(
            self.today()["quests"],
            {"step": {"progress": 0, "target": 1}, "code": {"progress": 0, "target": 0},
             "review": {"progress": 0, "target": 0}},
        )
        self.play("st18", "continue")
        self.date += timedelta(days=1)
        with self.store.transaction() as db:
            db.execute("UPDATE review_cards SET due_day=NULL")
        self.assertTrue(all(quest["target"] == 0 for quest in self.today()["quests"].values()))

    def test_placement_only_queues_unseen_cards_and_keeps_results(self):
        self.play("st01", "continue")
        self.play("st02", "run", source="print(4)", stdin="")
        self.play("st03", "continue")
        self.play("st04", "answer", choice=2)
        with self.store.transaction() as db:
            good_day = db.execute("SELECT due_day FROM review_cards WHERE id=?",
                                  (f"{LISTS}/st04",)).fetchone()[0]
            with self.assertRaises(RequestError):
                self.learning.skip(db, {"unit": LISTS}, self.date)
            fail = self.learning.place(db, {"unit": LISTS, "answers": [2, 0, 3, 2], "source": "starter"}, self.date)
            self.assertFalse(fail["passed"])
            low = self.learning.place(db, {"unit": LISTS, "answers": [0, 1, 0, 0], "source": PLACEMENT_SOURCE},
                                      self.date)
            self.assertFalse(low["passed"])
            good = self.learning.place(db, {"unit": LISTS, "answers": [2, 0, 3, 0], "source": PLACEMENT_SOURCE},
                                       self.date)
            self.assertTrue(good["passed"])
            self.assertTrue(self.learning.placement(db, LISTS)["can_skip"])
            self.assertFalse(self.learning.today(db, self.date)["unit"]["skipped"])
            self.assertEqual(self.learning.today(db, self.date)["unit"]["completed"], 4)
            self.learning.skip(db, {"unit": LISTS}, self.date)
            self.learning.skip(db, {"unit": LISTS}, self.date)
            self.assertTrue(self.learning.today(db, self.date)["unit"]["skipped"])
            self.assertEqual(self.learning.today(db, self.date)["unit"]["completed"], 4)
            self.assertEqual(good_day, (self.date + timedelta(days=3)).isoformat())
            rows = db.execute(
                "SELECT due_day, COUNT(*) FROM review_cards WHERE due_day IS NOT NULL GROUP BY due_day"
            ).fetchall()
            self.assertEqual([count for _, count in rows], [2, 2, 1, 1])
            key = self.learning.reviews(db, self.date)["due"][0]["id"]
            wrong = (self.learning.card(key)["answer"] + 1) % 4
            self.learning.review(db, {"card": key, "retry": False, "choice": wrong}, self.date)
            self.learning.place(db, {"unit": LISTS, "answers": [2, 0, 3, 2], "source": PLACEMENT_SOURCE}, self.date)
            self.assertTrue(self.learning.today(db, self.date)["unit"]["recommend"])
            self.assertEqual(db.execute("SELECT COUNT(*) FROM review_logs").fetchone()[0], 2)

    def test_backup_online_round_trip_and_rejects_invalid_backup(self):
        def counts():
            tables = (
                "stages", "modules", "units", "steps", "attempts", "step_progress", "review_cards",
                "review_logs", "xp_events", "daily_quest", "placement_results",
                "unit_skips", "schema_version",
            )
            with self.store.transaction() as db:
                return [db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in tables]

        self.play("st01", "continue")
        self.play("st02", "run", source="print(4)", stdin="")
        self.play("st03", "continue")
        before = counts()
        identifier = self.store.backup()
        self.play("st04", "answer", choice=2)
        after = counts()
        self.assertNotEqual(before, after)
        safety_copy = self.store.restore(identifier)
        self.assertEqual(before, counts())
        self.store.restore(safety_copy)
        self.assertEqual(after, counts())
        self.assertEqual(stat.S_IMODE(self.store.path.parent.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE((self.store.backups / identifier).stat().st_mode), 0o700)
        with self.assertRaises(ValueError):
            self.store.restore("../data")
        false_backup = self.store.backups / "20261127T000000-000000000000"
        false_backup.mkdir(mode=0o700)
        with closing(sqlite3.connect(false_backup / BACKUP_DB)) as wrong_db, wrong_db:
            wrong_db.execute("CREATE TABLE unrelated (x)")
        with self.assertRaisesRegex(ValueError, "does not belong"):
            self.store.restore(false_backup.name)
        self.assertEqual(after, counts())

    def test_failed_first_migration_remains_retryable(self):
        path = self.store.path.with_name("other.sqlite3")
        fresh = Store(path, self.store.backups, self.store.catalog)
        first = self.store.path.parent / MIGRATIONS[0].name
        first.write_text(MIGRATIONS[0].read_text(encoding="utf-8") + "\nINVALID SQL;", encoding="utf-8")
        with patch("app.storage.MIGRATIONS", [first, *MIGRATIONS[1:]]):
            with self.assertRaises(sqlite3.Error):
                fresh.initialize()
        fresh.initialize()
        with fresh.transaction() as db:
            self.assertEqual(list(map(tuple, db.execute("SELECT * FROM schema_version"))),
                             [(1,), (2,), (3,)])

    def test_incomplete_backup_schema_leaves_live_db_unchanged(self):
        self.play("st01", "continue")
        before = self.store.path.read_bytes()
        for statement, message in [
            ("DROP TABLE xp_events", "missing table xp_events"),
            ("ALTER TABLE attempts DROP COLUMN answer", "missing columns in attempts: answer"),
            ("DROP INDEX attempts_by_action", "missing index in attempts"),
        ]:
            with self.subTest(statement=statement):
                identifier = self.store.backup()
                backup = self.store.backups / identifier / BACKUP_DB
                with closing(sqlite3.connect(backup)) as damaged, damaged:
                    damaged.execute(statement)
                with self.assertRaisesRegex(ValueError, message):
                    self.store.restore(identifier)
                self.assertEqual(self.store.path.read_bytes(), before)

    def test_backup_missing_review_log_unique_index_leaves_live_db_unchanged(self):
        identifier = self.store.backup()
        backup = self.store.backups / identifier / BACKUP_DB
        with closing(sqlite3.connect(backup)) as damaged, damaged:
            definition = damaged.execute(
                "SELECT sql FROM sqlite_schema WHERE name='review_logs'",
            ).fetchone()[0]
            damaged.execute("DROP TABLE review_logs")
            damaged.execute(definition.replace(",\n    UNIQUE (card_id, day, event, revision)", ""))
            damaged.execute("CREATE INDEX review_logs_day ON review_logs(day, event)")
            damaged.execute(
                "CREATE INDEX review_logs_revision ON review_logs(card_id, day, event, revision)",
            )
        self.play("st01", "continue")
        before = self.store.path.read_bytes()
        with self.assertRaisesRegex(ValueError, "missing unique index in review_logs"):
            self.store.restore(identifier)
        self.assertEqual(self.store.path.read_bytes(), before)
