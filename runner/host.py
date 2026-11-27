import json
import os
import selectors
import subprocess
import sys
import time
from tempfile import TemporaryDirectory
from uuid import uuid4

from app.content import SOURCE_LIMIT, STDIN_LIMIT, load_catalog

from .sandbox import START, TESTS_PASSED, TIMED_OUT

IMAGE = "cs-academy-runner:p0"
WALL_TIMEOUT = 10
OUTPUT_LIMIT = 16 * 1024


def command(name):
    return [
        "docker", "run", "--rm", "--name", name, "--pull", "never", "-i",
        "--network", "none", "--user", "65532:65532", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges", "--pids-limit", "32",
        "--read-only", "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=16m,mode=1777",
        "--memory", "128m", "--memory-swap", "128m", "--cpus", "0.5",
        "--log-driver", "none", IMAGE,
    ]


def unavailable(message):
    return {"status": "unavailable", "stdout": "", "stderr": message, "truncated": False}


def collect(process, data, deadline):
    output = {"stdout": bytearray(), "stderr": bytearray()}
    truncated = False
    pending = memoryview(data)
    with selectors.DefaultSelector() as selector:
        for name in ("stdin", "stdout", "stderr"):
            stream = getattr(process, name)
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_WRITE if name == "stdin"
                              else selectors.EVENT_READ, name)
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return output, truncated, True
            for key, _ in selector.select(remaining):
                fd, name = key.fd, key.data
                if name == "stdin":
                    try:
                        pending = pending[os.write(fd, pending):]
                    except BlockingIOError:
                        continue
                    except BrokenPipeError:
                        pending = pending[len(pending):]
                    if not pending:
                        selector.unregister(fd)
                        key.fileobj.close()
                    continue

                try:
                    chunk = os.read(fd, 8192)
                except BlockingIOError:
                    continue
                if chunk:
                    room = OUTPUT_LIMIT - len(output[name])
                    truncated |= len(chunk) > room
                    output[name].extend(chunk[:room])
                else:
                    selector.unregister(fd)
        try:
            process.wait(timeout=max(0, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            return output, truncated, True
    return output, truncated, False


def docker_endpoint():
    context = os.environ.get("DOCKER_CONTEXT")
    endpoint = os.environ.get("DOCKER_HOST") if not context else None
    if not endpoint:
        arguments = ["docker", "context", "inspect", "--format", "{{.Endpoints.docker.Host}}"]
        if context:
            arguments.extend(["--", context])
        result = subprocess.run(arguments, capture_output=True, text=True, timeout=2, check=True)
        endpoint = result.stdout.strip()
    if not endpoint.startswith("unix:///") or "\n" in endpoint:
        raise ValueError("The runner requires a local Unix Docker socket.")
    return endpoint


def cleanup(name, environment):
    try:
        subprocess.run(["docker", "rm", "-f", name], env=environment,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=3, check=False)
    except (OSError, subprocess.TimeoutExpired):
        pass


def run_container(payload, environment):
    name = f"cs-academy-{uuid4().hex}"
    deadline = time.monotonic() + WALL_TIMEOUT
    try:
        process = subprocess.Popen(command(name), env=environment, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return unavailable("Docker CLI could not start. Install Docker and start its engine.")

    with process:
        timed_out = True
        try:
            output, truncated, timed_out = collect(
                process, json.dumps(payload, ensure_ascii=False).encode("utf-8"), deadline,
            )
        except OSError:
            return unavailable("Docker I/O failed. Check that the Docker engine is ready.")
        finally:
            if timed_out:
                if process.poll() is None:
                    process.kill()
                cleanup(name, environment)

    stdout = output["stdout"].decode("utf-8", "replace")
    stderr = output["stderr"].decode("utf-8", "replace")
    startup, marker, stderr_after = stderr.partition(START + "\n")
    if not marker:
        if "no such image" in stderr.lower() or "unable to find image" in stderr.lower():
            return unavailable("Runner image is missing. Run make runner-image.")
        return unavailable("Docker did not start the runner. Check the engine and make runner-image.")

    if timed_out or process.returncode == TIMED_OUT:
        status = "timeout"
    else:
        success = TESTS_PASSED if payload.get("test_body") else 0
        status = "passed" if process.returncode == success else "failed"
    return {"status": status, "stdout": stdout, "stderr": startup + stderr_after,
            "truncated": truncated}


def execute(problem_id, source, stdin=None):
    problems = load_catalog().problems
    if not isinstance(problem_id, str) or problem_id not in problems:
        raise ValueError("Unknown problem")
    if not isinstance(source, str) or len(source.encode("utf-8")) > SOURCE_LIMIT:
        raise ValueError("Invalid source")
    problem = problems[problem_id]
    tests = stdin is None
    if tests and not problem.test_body:
        raise ValueError("This problem has no test suite")
    if not tests and (not isinstance(stdin, str) or len(stdin.encode("utf-8")) > STDIN_LIMIT):
        raise ValueError("Invalid stdin")

    payload = {"source": source, "stdin": stdin if not tests else ""}
    if tests:
        payload.update(test_body=problem.test_body, test_class=problem.test_class,
                       module=problem.module)
    try:
        endpoint = docker_endpoint()
    except ValueError as error:
        return unavailable(str(error))
    except (OSError, subprocess.SubprocessError):
        return unavailable("Docker CLI or context is unavailable. Check the local Docker engine.")
    with TemporaryDirectory(prefix="academy-docker-") as config:
        # Docker client proxy settings are injected into containers as environment variables.
        environment = {"PATH": os.environ.get("PATH", os.defpath), "DOCKER_HOST": endpoint,
                       "DOCKER_CONFIG": config}
        return run_container(payload, environment)


def main():
    request = json.loads(sys.stdin.buffer.read(6 * (SOURCE_LIMIT + STDIN_LIMIT) + 1024))
    if not isinstance(request, dict) or set(request) not in (
        {"problem_id", "source"}, {"problem_id", "source", "stdin"}
    ):
        raise ValueError("Invalid runner request")
    if "stdin" in request and not isinstance(request["stdin"], str):
        raise ValueError("Invalid stdin")
    print(json.dumps(execute(**request), ensure_ascii=True))


if __name__ == "__main__":
    main()
