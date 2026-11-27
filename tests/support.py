from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from app.content import ROOT, load_catalog
from app.learning import Learning
from app.storage import BACKUP_DB, Store

LISTS = "s1.m03.u01"
FOR = "s1.m02.u02"
WHILE = "s1.m02.u03"
RECURSION = "s2.m05.u01"
UNIT = ROOT / "content/stage-1-python/m03-collections/u01-lists"
SOLUTIONS = (UNIT / "solutions/lists_practice.py").read_text(encoding="utf-8")
FIX = "def add_server(servers, name):\n    servers.append(name)\n    return servers\n"
PLACEMENT_SOURCE = (
    "def active_servers(servers, disabled):\n"
    "    return [name for name in servers if name not in disabled]\n"
)
TODAY = date(2026, 11, 27)


def result(status, *, stdout="", stderr=""):
    return {"status": status, "stdout": stdout, "stderr": stderr, "truncated": False}


def fake_runner(problem_id, source, stdin=None):
    if stdin is not None:
        return result("passed", stdout=f"{stdin.strip()}\n4\n")
    if source == "unavailable":
        return result("unavailable", stderr="Docker did not start")
    if source in {SOLUTIONS, FIX, PLACEMENT_SOURCE}:
        return result("passed", stderr="OK")
    return result("failed", stderr="Test failure")


class AcademyCase(TestCase):
    lists_only = True

    def setUp(self):
        root = Path(self.enterContext(TemporaryDirectory(prefix="cs-academy-test-")))
        catalog = load_catalog()
        if self.lists_only:
            catalog.play = {LISTS: catalog.play[LISTS]}
            catalog.cards = {key: card for key, card in catalog.cards.items() if card["unit"] == LISTS}
            catalog.placements = {LISTS: catalog.placements[LISTS]}
        self.store = Store(root / "data" / BACKUP_DB, root / "backups", catalog)
        self.store.initialize()
        self.date = TODAY
        self.learning = Learning(self.store, clock=lambda: self.date, runner=fake_runner)
