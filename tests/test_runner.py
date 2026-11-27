import unittest
from unittest.mock import patch

from app.content import LISTS
from runner.host import IMAGE, WALL_TIMEOUT, command, execute


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
