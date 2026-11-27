import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tempfile import TemporaryDirectory
from unittest import SkipTest

from app.execution import run_problem
from runner.host import IMAGE, OUTPUT_LIMIT, docker_endpoint, run_container

from .http_support import play_path, tcp_api, try_source
from .support import FOR, LISTS, PLACEMENT_SOURCE, RECURSION, SOLUTIONS, AcademyCase

PLACEMENT_SOLUTIONS = {
    FOR: "def even_slots(stop):\n    return list(range(0, stop, 2))\n",
    LISTS: PLACEMENT_SOURCE,
    RECURSION: (
        "def scan_pages(n):\n"
        "    if n == 0:\n"
        "        return 0\n"
        "    return 2 * n + scan_pages(n - 1)\n"
    ),
}


WORKERS = min(4, os.cpu_count() or 2)


def parallel(function, jobs):
    with ThreadPoolExecutor(WORKERS) as pool:
        return list(pool.map(lambda job: function(*job), jobs))


def journey_runs(catalog):
    for uid, sequence in catalog.play.items():
        attempt = 0
        for key in sequence:
            kind = catalog.steps[key]["type"]
            problem = catalog.problems.get(key)
            if kind == "try" and uid != LISTS:
                yield (key, *try_source(uid, {"starter": problem.starter}, attempt))
                attempt += 1
            elif kind in ("fix", "code"):
                yield key, problem.starter, None
                yield key, problem.solution, None


def prefetched_runner(catalog):
    jobs = list(dict.fromkeys(journey_runs(catalog)))
    results = dict(zip(jobs, parallel(run_problem, jobs), strict=True))

    def runner(key, source, stdin=None):
        found = results.get((key, source, stdin))
        return found if found is not None else run_problem(key, source, stdin)

    return runner


class DockerIntegrationTest(AcademyCase):
    lists_only = False

    @classmethod
    def setUpClass(cls):
        try:
            subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"],
                           capture_output=True, timeout=30, check=True)
        except (OSError, subprocess.SubprocessError) as error:
            if os.environ.get("CS_ACADEMY_REQUIRE_DOCKER"):
                raise AssertionError("Docker is required for this test run") from error
            raise SkipTest("Docker is unavailable") from error
        try:
            subprocess.run(["docker", "image", "inspect", IMAGE],
                           capture_output=True, timeout=30, check=True)
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

    def test_predictions_and_parsons_match_python(self):
        catalog = self.store.catalog
        endpoint = docker_endpoint()
        with TemporaryDirectory(prefix="academy-test-docker-") as config:
            env = {"PATH": os.environ.get("PATH", os.defpath), "DOCKER_HOST": endpoint,
                   "DOCKER_CONFIG": config}
            jobs = []
            for sequence in catalog.play.values():
                for key in sequence:
                    step = catalog.steps[key]
                    if step["type"] == "predict":
                        jobs.append((key, step["code"], step["choices"][step["answer"]]["text"].rstrip()))
                    elif step["type"] == "parsons":
                        jobs.append((key, "\n".join(step["lines"]), step["expected_stdout"].rstrip()))
            results = parallel(lambda key, source, _: run_container({"source": source, "stdin": ""}, env),
                               jobs)
            for (key, _, expected), result in zip(jobs, results, strict=True):
                with self.subTest(step=key):
                    if key == f"{LISTS}/st05":
                        self.assertEqual(result["status"], "failed", result)
                        self.assertEqual(result["stderr"].splitlines()[-1], expected)
                        continue
                    if key == f"{LISTS}/st12":
                        self.assertEqual(expected, "0 1 2 (on three lines)")
                        expected = "0\n1\n2"
                    self.assertEqual(result["status"], "passed", result)
                    self.assertEqual(result["stdout"].rstrip(), expected)

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

    def test_path_journey_over_tcp_and_docker(self):
        self.learning.runner = prefetched_runner(self.store.catalog)
        with tcp_api(self) as api:
            for uid, spec in self.store.catalog.placements.items():
                with self.subTest(placement=uid):
                    problem = self.store.catalog.problems[spec["problem"]]
                    questions = spec["questions"]
                    answers = [self.store.catalog.steps[key]["answer"] for key in questions]
                    body = {"unit": uid, "answers": answers}
                    trial = api.post("/api/placement", {**body, "source": problem.starter})
                    self.assertFalse(trial["passed"], trial)
                    self.assertEqual(trial["execution"]["status"], "failed", trial)
                    trial = api.post("/api/placement", {**body, "source": PLACEMENT_SOLUTIONS[uid]})
                    self.assertTrue(trial["passed"], trial)
            play_path(self, api)
