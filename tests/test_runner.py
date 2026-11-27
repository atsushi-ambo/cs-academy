import sys
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
                    status = sandbox.grade()
        return status, output.getvalue()

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
