import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.content import LISTS, ROOT, ContentError, load_catalog

from .support import UNIT


class ContentTest(unittest.TestCase):
    def test_loads_sample(self):
        catalog = load_catalog()
        self.assertEqual(len(catalog.stages), 8)
        self.assertEqual(len(catalog.play[LISTS]), 21)
        self.assertEqual(len(catalog.steps), 24)
        self.assertEqual(sum(card["kind"] == "predict" for card in catalog.cards.values()), 6)
        self.assertIn("test_empty", catalog.problems[f"{LISTS}/st14"].test_body)
        self.assertIn("Text version", catalog.steps[f"{LISTS}/st03"]["body"])
        self.assertIn("reference", catalog.resources[LISTS]["lesson"].lower())
        self.assertIn("Hands-on", catalog.resources[LISTS]["handson"])

    def changed(self, first, replacement, *, curriculum=False):
        with TemporaryDirectory() as root:
            directory = Path(root) / "content"
            shutil.copytree(ROOT / "content", directory)
            file = directory / ("curriculum.yaml" if curriculum else
                                UNIT.relative_to(ROOT / "content") / "steps.yaml")
            contents = file.read_text(encoding="utf-8")
            self.assertIn(first, contents)
            file.write_text(contents.replace(first, replacement, 1), encoding="utf-8")
            return load_catalog(directory)

    def test_rejects_duplicate_ids_and_keys(self):
        variants = [
            ("id: st05", "id: st04", False, "duplicate ID"),
            ("answer: 2", "answer: 2\n    answer: 1", False, "Duplicate YAML key"),
            ("id: s0.m01.u02", "id: s0.m01.u01", True, "duplicate ID"),
        ]
        for first, replacement, curriculum, error in variants:
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ContentError, error):
                self.changed(first, replacement, curriculum=curriculum)

    def test_rejects_bad_steps(self):
        variants = [
            ("type: try", "type: run", "Unknown step type"),
            ('why: "Correct. -1 is always the last item."', "why: ''", "non-empty text"),
            ("answer: 2", "answer: 4", "Invalid answer"),
            (
                "    type: try\n    title:",
                "    type: read\n    body: More reading\n    title:",
                "two consecutive read",
            ),
            ("exercise: exercises/lists_practice.py", "exercise: ../lists_practice.py",
             "Invalid unit asset"),
            ("from_steps: [st04", "from_steps: [st01", "Invalid review step"),
        ]
        for first, replacement, error in variants:
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ContentError, error):
                self.changed(first, replacement)
