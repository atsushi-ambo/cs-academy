import sqlite3
import stat
from contextlib import closing
from datetime import timedelta
from unittest.mock import patch

from app.content import LISTS
from app.learning import RequestError
from app.storage import BACKUP_DB, MIGRATIONS, Store

from .support import PLACEMENT_SOURCE, AcademyCase


class LearningTest(AcademyCase):
    def play(self, step, action, **fields):
        with self.store.transaction() as db:
            return self.learning.play(
                db, {"step": f"{LISTS}/{step}", "action": action, **fields}, self.date,
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

    def test_placement_only_queues_unseen_cards_and_keeps_results(self):
        self.play("st01", "continue")
        self.play("st02", "run", source="print(4)", stdin="")
        self.play("st03", "continue")
        self.play("st04", "answer", choice=2)
        with self.store.transaction() as db:
            good_day = db.execute("SELECT due_day FROM review_cards WHERE id=?",
                                  (f"{LISTS}/st04",)).fetchone()[0]
            with self.assertRaises(RequestError):
                self.learning.skip(db, self.date)
            fail = self.learning.place(db, {"answers": [2, 0, 3, 2], "source": "starter"}, self.date)
            self.assertFalse(fail["passed"])
            low = self.learning.place(db, {"answers": [0, 1, 0, 0], "source": PLACEMENT_SOURCE},
                                      self.date)
            self.assertFalse(low["passed"])
            good = self.learning.place(db, {"answers": [2, 0, 3, 0], "source": PLACEMENT_SOURCE},
                                       self.date)
            self.assertTrue(good["passed"])
            self.assertTrue(self.learning.placement(db)["can_skip"])
            self.assertFalse(self.learning.today(db, self.date)["skipped"])
            self.assertEqual(self.learning.today(db, self.date)["completed"], 4)
            self.learning.skip(db, self.date)
            self.learning.skip(db, self.date)
            self.assertTrue(self.learning.today(db, self.date)["skipped"])
            self.assertEqual(self.learning.today(db, self.date)["completed"], 4)
            self.assertEqual(good_day, (self.date + timedelta(days=3)).isoformat())
            rows = db.execute(
                "SELECT due_day, COUNT(*) FROM review_cards WHERE due_day IS NOT NULL GROUP BY due_day"
            ).fetchall()
            self.assertEqual([count for _, count in rows], [2, 2, 1, 1])
            key = self.learning.reviews(db, self.date)["due"][0]["id"]
            wrong = (self.learning.card(key)["answer"] + 1) % 4
            self.learning.review(db, {"card": key, "retry": False, "choice": wrong}, self.date)
            self.learning.place(db, {"answers": [2, 0, 3, 2], "source": PLACEMENT_SOURCE}, self.date)
            self.assertTrue(self.learning.today(db, self.date)["recommend"])
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
        with patch("app.storage.MIGRATIONS", [first, MIGRATIONS[1]]):
            with self.assertRaises(sqlite3.Error):
                fresh.initialize()
        fresh.initialize()
        with fresh.transaction() as db:
            self.assertEqual(list(map(tuple, db.execute("SELECT * FROM schema_version"))), [(1,), (2,)])
