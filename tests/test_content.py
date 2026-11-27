import shutil
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory

from app.content import ROOT, ContentError, load_catalog

from .support import LISTS, UNIT


class ContentTest(unittest.TestCase):
    def test_algorithm_units_have_the_required_play_and_review_steps(self):
        catalog = load_catalog()
        units = ("s1.m02.u02", "s1.m02.u03", "s1.m02.u04", "s2.m05.u01",
                 "s2.m05.u03", "s2.m05.u04", "s2.m05.u05", "s2.m02.u01", "s2.m02.u02",
                 "s2.m02.u03", "s2.m02.u04", "s2.m02.u05", "s2.m03.u04", "s2.m03.u05")
        for uid in units:
            with self.subTest(unit=uid):
                steps = catalog.play[uid]
                counts = Counter(catalog.steps[key]["type"] for key in steps)
                self.assertTrue(18 <= len(steps) <= 28)
                self.assertEqual(catalog.steps[steps[0]]["type"], "read")
                for kind, minimum in {"predict": 5, "code": 3, "fix": 2, "parsons": 1,
                                      "try": 1, "explain": 1}.items():
                    self.assertGreaterEqual(counts[kind], minimum, kind)
                for key in steps:
                    if catalog.steps[key]["type"] == "predict":
                        self.assertIn(key, catalog.cards)

    def test_loads_sample(self):
        catalog = load_catalog()
        self.assertEqual(len(catalog.stages), 8)
        self.assertEqual(len(catalog.play[LISTS]), 21)
        self.assertEqual(sum(key.startswith(LISTS + "/") for key in catalog.steps), 24)
        self.assertEqual(sum(card["kind"] == "predict" for card in catalog.cards.values() if card["unit"] == LISTS), 6)
        self.assertIn("test_empty", catalog.problems[f"{LISTS}/st14"].test_body)
        self.assertIn("Text version", catalog.steps[f"{LISTS}/st03"]["body"])
        self.assertIn("reference", catalog.resources[LISTS]["lesson"].lower())
        self.assertIn("Hands-on", catalog.resources[LISTS]["handson"])

    def changed(self, first, replacement, *, curriculum=False, unit_file="steps.yaml"):
        with TemporaryDirectory() as root:
            directory = Path(root) / "content"
            shutil.copytree(ROOT / "content", directory)
            file = directory / ("curriculum.yaml" if curriculum else
                                UNIT.relative_to(ROOT / "content") / unit_file)
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
            ('stdout_line: "4"', "stdout_line: 4", "non-empty text"),
            ('stdout_line: "4"', r'stdout_line: "4\n5"', "stdout_line must be one line"),
            ('stdout_line: "4"', 'stdout_line: "4", stdout_contains: "4"', "expected one stdout check"),
        ]
        for first, replacement, error in variants:
            with self.subTest(replacement=replacement), self.assertRaisesRegex(ContentError, error):
                self.changed(first, replacement)

    def test_rejects_invalid_parsons_alternatives(self):
        for alternatives in ("true", "[[0, 1]]", "[[0, 0, 1]]", "[[0, 1, 3]]",
                             "[[false, 1, 2]]", "[[0, 1, 2]]", "[[1, 0, 2], [1, 0, 2]]"):
            with self.subTest(alternatives=alternatives), self.assertRaises(ContentError):
                self.changed('    expected_stdout: "[\'web01\', \'web02\']"',
                             f'    accepted_orders: {alternatives}\n    expected_stdout: example')

    def test_authored_parsons_orders_produce_expected_output(self):
        for key, step in load_catalog().steps.items():
            if step["type"] != "parsons":
                continue
            lines = step["lines"]
            for order in [list(range(len(lines))), *step.get("accepted_orders", [])]:
                with self.subTest(step=key, order=order):
                    source = "\n".join(lines[index] for index in order)
                    result = subprocess.run([sys.executable, "-I", "-B", "-c", source],
                                            capture_output=True, text=True, timeout=3)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout.splitlines(), step["expected_stdout"].splitlines())

    def test_two_input_complexity_includes_outer_pass(self):
        body = load_catalog().steps["s2.m02.u01/st08"]["body"]
        self.assertIn("a × b comparisons", body)
        self.assertIn("O(a + a × b)", body)

    def test_slice_lesson_shows_when_slice_length_rule_applies(self):
        body = load_catalog().steps[f"{LISTS}/st06"]["body"]
        self.assertIn("`0 <= start <= stop <= len(x)`", body)
        self.assertIn("x[3:10]  # [40, 50]", body)

    def test_rejects_invalid_prerequisite(self):
        with self.assertRaisesRegex(ContentError, "Invalid prerequisites"):
            self.changed("s1.m02.u02", "unknown", unit_file="unit.yaml")

    def test_rejects_missing_explain_rubric(self):
        with self.assertRaisesRegex(ContentError, "Missing rubric"):
            self.changed("[correct idea, a concrete example, clear English]", "[]")
