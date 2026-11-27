import sys
import traceback
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app.content import load_catalog
from runner import sandbox
from runner.host import IMAGE, WALL_TIMEOUT, command, execute

from .support import LISTS, RECURSION


class RunnerCommandTest(unittest.TestCase):
    def test_isolation_command(self):
        argv = command("one-unique-name")
        self.assertEqual(argv[:3], ["docker", "run", "--rm"])
        self.assertEqual(argv[-1], IMAGE)
        self.assertEqual(WALL_TIMEOUT, 10)
        for key, value in {
            "--name": "one-unique-name", "--pull": "never", "--network": "none",
            "--user": "65532:65532", "--cap-drop": "ALL", "--security-opt": "no-new-privileges",
            "--pids-limit": "32", "--tmpfs": "/tmp:rw,noexec,nosuid,nodev,size=16m,mode=1777",
            "--memory": "128m", "--memory-swap": "128m", "--cpus": "0.5",
            "--log-driver": "none",
        }.items():
            with self.subTest(key=key):
                self.assertEqual(argv[argv.index(key) + 1], value)
        self.assertIn("--read-only", argv)
        self.assertIn("-i", argv)
        self.assertTrue({"-v", "--volume", "--mount", "--privileged", "--env"}.isdisjoint(argv))

    def test_remote_docker_is_rejected_before_sending_source(self):
        with patch.dict("os.environ", {"DOCKER_HOST": "ssh://remote"}, clear=True):
            with patch("runner.host.run_container") as run:
                outcome = execute(f"{LISTS}/st02", "print(4)", "")
        run.assert_not_called()
        self.assertEqual(outcome["status"], "unavailable")
        self.assertIn("local Unix Docker socket", outcome["stderr"])

    def test_fixed_local_environment_excludes_client_configuration(self):
        environment = {
            "DOCKER_CONTEXT": "orbstack", "DOCKER_HOST": "ssh://ignored",
            "DOCKER_CONFIG": "/original-config", "PATH": "/docker-bin",
        }
        with patch.dict("os.environ", environment, clear=True):
            with patch("runner.host.subprocess.run") as inspect:
                inspect.return_value.stdout = "unix:///local-engine.sock\n"
                with patch("runner.host.run_container") as run:
                    execute(f"{LISTS}/st02", "print(4)", "stdin")
        self.assertEqual(inspect.call_args.args[0][-2:], ["--", "orbstack"])
        payload, isolated_environment = run.call_args.args
        self.assertEqual(payload, {"source": "print(4)", "stdin": "stdin"})
        self.assertEqual(isolated_environment["DOCKER_HOST"], "unix:///local-engine.sock")
        self.assertNotIn("DOCKER_CONTEXT", isolated_environment)
        self.assertNotEqual(isolated_environment["DOCKER_CONFIG"], "/original-config")


class TechniqueTest(unittest.TestCase):
    def grade_fixture(self, problem, source):
        output = StringIO()
        payload = {
            "source": source, "test_body": problem.test_body,
            "module": problem.module, "test_class": problem.test_class,
        }
        with TemporaryDirectory(prefix="academy-technique-") as root:
            unit = Path(root) / "unit"
            with patch.object(sandbox, "Path", return_value=unit):
                argv, _ = sandbox.prepare(payload)
                with (patch.object(sys, "argv", argv), patch.object(sys, "path", sys.path.copy()),
                      patch.dict(sys.modules), redirect_stderr(output)):
                    sys.modules.pop(problem.module, None)
                    try:
                        status = sandbox.grade()
                    except AssertionError:
                        traceback.print_exc()
                        status = sandbox.TESTS_FAILED
        return status, output.getvalue()

    def test_complexity_and_array_graders_accept_equivalent_solutions(self):
        catalog = load_catalog()
        cases = (
            ("s2.m02.u01/st10", "        for place in range(places):\n            count += 1",
             "        place = 0\n        while place < places:\n            count += 1\n            place += 1"),
            ("s2.m02.u01/st15", "        for right in range(left + 1, n):\n            pairs += 1",
             "        if left + 1 < n:\n            for right in range(left + 1, n):\n                pairs += 1"),
            ("s2.m02.u01/st16", "range(4)", "(0, 1, 2, 3)"),
            ("s2.m02.u01/st16", "range(4)", "(\n            0, 1, 2, 3\n        )"),
            ("s2.m02.u02/st10", "        for event in range(n):\n            visits += 1",
             "        if n:\n            for event in range(n):\n                visits += 1"),
            ("s2.m02.u02/st16", "        for right in range(n):\n            pairs += 1",
             "        if n:\n            for right in range(n):\n                pairs += 1"),
            ("s2.m02.u02/st18", "size * size <= budget:\n        size *= 2",
             "size ** 2 <= budget:\n        size += size"),
            ("s2.m02.u03/st07", "return 1 + half_path(size // 2)",
             "recurse = half_path\n    return 1 + recurse(size=size // 2)"),
            ("s2.m02.u03/st10", "return 1 + tour_calls(n - 1) + tour_calls(n - 1)",
             "return 1 + sum(tour_calls(n=n - 1) for _ in range(2))"),
            ("s2.m02.u03/st15", "range(1, n + 1)", "reversed(range(1, n + 1))"),
            ("s2.m02.u03/st16", "return n * job_plans(n - 1)",
             "recurse = job_plans\n    return n * recurse(n=n - 1)"),
            ("s2.m02.u03/st18", "return n * n * n", "return pow(n, 3)"),
            ("s2.m02.u04/st07", "for value in values:", "for index in range(len(values)):\n        value = values[index]"),
            ("s2.m02.u04/st07", "for value in values:", "for value in reversed(values):"),
            ("s2.m02.u04/st10", "count_ones(values, index + 1)", "count_ones(values, index=index + 1)"),
            ("s2.m02.u04/st10", "count_ones(values, index + 1)", "count_ones(index=index + 1, values=values)"),
            ("s2.m02.u04/st16", "for index in range(len(values)):\n        if values[index] < 0:",
             "for index, value in enumerate(values):\n        if value < 0:"),
            ("s2.m02.u04/st18", "for change in changes:", "for _, change in enumerate(changes):"),
            ("s2.m02.u05/st10", "for code in codes:", "for index in range(len(codes)):\n        code = codes[index]"),
            ("s2.m02.u05/st15", "return (n + 1) / 2", "return float(n + 1) / 2"),
            ("s2.m02.u05/st16", catalog.problems["s2.m02.u05/st16"].solution,
             "def first_index(codes, target):\n"
             "    return next((i for i, code in enumerate(codes) if code == target), -1)\n"),
            ("s2.m03.u04/st07", "return a is b", "return not (a is not b)"),
            ("s2.m03.u05/st07", "return cells[row * cols + col]", "return cells[abs(row * cols + col)]"),
            ("s2.m03.u05/st10", "cells[row * cols + col] = value", "cells[abs(row * cols + col)] = value"),
            ("s2.m03.u05/st15", "while capacity < count:", "for _ in range(max(0, count - 1).bit_length()):"),
        )
        for key, original, equivalent in cases:
            with self.subTest(step=key, equivalent=equivalent):
                problem = catalog.problems[key]
                self.assertIn(original, problem.solution)
                source = problem.solution.replace(original, equivalent, 1)
                status, output = self.grade_fixture(problem, source)
                self.assertEqual(status, sandbox.TESTS_PASSED, output)

    def test_complexity_graders_still_enforce_work_and_object_identity(self):
        catalog = load_catalog()
        cases = (
            ("s2.m02.u01/st16", "range(4):\n            checks += 1",
             "range(n):\n            checks += 4 if label == 0 else 0"),
            ("s2.m02.u04/st10", "count_ones(values, index + 1)", "count_ones(values.copy(), index + 1)"),
        )
        for key, original, wrong in cases:
            with self.subTest(step=key):
                problem = catalog.problems[key]
                self.assertIn(original, problem.solution)
                source = problem.solution.replace(original, wrong, 1)
                status, output = self.grade_fixture(problem, source)
                self.assertEqual(status, sandbox.TESTS_FAILED, output)

    def test_batch_pages_enforces_recursion_and_prohibits_loops_and_sum(self):
        problem = load_catalog().problems[f"{RECURSION}/st07"]
        cases = {
            "iterative": (
                "    total = 0\n"
                "    for page in range(1, n + 1):\n"
                "        total += page\n"
                "    return total\n",
                "This exercise must use recursion: batch_pages never calls itself.",
            ),
            "closed formula": (
                "    return n * (n + 1) // 2\n",
                "This exercise must use recursion: batch_pages never calls itself.",
            ),
            "comprehension": (
                "    return 0 if n == 0 else [n for _ in range(1)][0] + batch_pages(n - 1)\n",
                "batch_pages must not use loops.",
            ),
            "sum": (
                "    return 0 if n == 0 else sum((n, batch_pages(n - 1)))\n",
                "batch_pages must not use sum().",
            ),
        }
        for technique, (body, message) in cases.items():
            with self.subTest(technique=technique):
                status, output = self.grade_fixture(problem, "def batch_pages(n):\n" + body)
                self.assertEqual(status, sandbox.TESTS_FAILED, output)
                self.assertIn(message, output)
                self.assertIn("failures=1", output)
        status, output = self.grade_fixture(problem, problem.solution)
        self.assertEqual(status, sandbox.TESTS_PASSED, output)
