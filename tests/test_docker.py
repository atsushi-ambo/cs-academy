import os
import subprocess
from unittest import SkipTest

from app.content import LISTS
from app.execution import run_problem
from runner.host import IMAGE, OUTPUT_LIMIT

from .http_support import play_lists, tcp_api
from .support import PLACEMENT_SOURCE, SOLUTIONS, AcademyCase


class DockerIntegrationTest(AcademyCase):
    @classmethod
    def setUpClass(cls):
        try:
            subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"],
                           capture_output=True, timeout=8, check=True)
        except (OSError, subprocess.SubprocessError) as error:
            if os.environ.get("CS_ACADEMY_REQUIRE_DOCKER"):
                raise AssertionError("Docker is required for this test run") from error
            raise SkipTest("Docker is unavailable") from error
        try:
            subprocess.run(["docker", "image", "inspect", IMAGE],
                           capture_output=True, timeout=8, check=True)
        except (OSError, subprocess.SubprocessError) as error:
            raise AssertionError("Runner image is missing. Run make runner-image.") from error

    def test_solution_starter_and_user_stdin(self):
        key = f"{LISTS}/st14"
        accepted = run_problem(key, SOLUTIONS)
        self.assertEqual(accepted["status"], "passed", accepted)
        self.assertIn("test_empty", accepted["stderr"])
        rejected = run_problem(key, self.store.catalog.problems[key].starter)
        self.assertEqual(rejected["status"], "failed", rejected)
        self.assertIn("NotImplementedError", rejected["stderr"])
        premature_exit = run_problem(key, "raise SystemExit(0)")
        self.assertEqual(premature_exit["status"], "failed", premature_exit)
        echo = run_problem(key, "print(input())", "hello from stdin\n")
        self.assertEqual(echo["stdout"], "hello from stdin\n")
        self.assertEqual(echo["status"], "passed")

    def test_limits(self):
        key = f"{LISTS}/st02"
        hanging = run_problem(key, "while True:\n    pass", "")
        self.assertEqual(hanging["status"], "timeout", hanging)
        net = run_problem(key, """
import socket
try:
    socket.create_connection(("192.0.2.1", 80), timeout=1)
except OSError:
    print("network unavailable")
else:
    raise SystemExit(1)
""", "")
        self.assertEqual(net["status"], "passed", net)
        self.assertEqual(net["stdout"], "network unavailable\n")
        large = run_problem(key, 'print("x" * 200000)', "")
        self.assertEqual(large["status"], "passed", large)
        self.assertTrue(large["truncated"])
        self.assertEqual(len(large["stdout"]), OUTPUT_LIMIT)

    def test_lists_journey_over_tcp_and_docker(self):
        self.learning.runner = run_problem
        with tcp_api(self) as api:
            play_lists(self, api)
            result = api.post("/api/placement", {"answers": [2, 0, 3, 2],
                                                 "source": PLACEMENT_SOURCE})
            self.assertTrue(result["passed"], result)
