import json
import runpy
import subprocess
import sys
import unittest
from pathlib import Path

START = "CS_ACADEMY_RUN_STARTED"
TESTS_PASSED = 42
TESTS_FAILED = 43
TIMED_OUT = 124


def grade():
    unit = Path("/tmp/unit")
    if sys.argv[2:] == ["inline"]:
        variables = runpy.run_path(str(unit / "submission.py"), run_name="__academy_submission__")
        test_file = unit / "test_submission.py"
        exec(compile(test_file.read_bytes(), str(test_file), "exec"), variables)
        return TESTS_PASSED
    test_name, test_class = sys.argv[2:]
    tests = runpy.run_path(str(unit / "tests" / f"test_{test_name}.py"))
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(tests[test_class])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return TESTS_PASSED if result.testsRun and result.wasSuccessful() else TESTS_FAILED


def prepare(payload):
    unit = Path("/tmp/unit")
    unit.mkdir()
    test_body = payload.get("test_body")
    if not test_body:
        program = unit / "submission.py"
        program.write_text(payload["source"], encoding="utf-8")
        return [str(program)], payload["stdin"].encode("utf-8")

    module = payload.get("module")
    if module:
        (unit / "exercises").mkdir()
        (unit / "tests").mkdir()
        (unit / "exercises" / f"{module}.py").write_text(payload["source"], encoding="utf-8")
        (unit / "tests" / f"test_{module}.py").write_text(test_body, encoding="utf-8")
        return [__file__, "grade", module, payload["test_class"]], b""
    (unit / "submission.py").write_text(payload["source"], encoding="utf-8")
    (unit / "test_submission.py").write_text(test_body, encoding="utf-8")
    return [__file__, "grade", "inline"], b""


def main():
    if sys.argv[1:] and sys.argv[1] == "grade":
        return grade()
    payload = json.loads(sys.stdin.buffer.read())
    argv, stdin = prepare(payload)
    print(START, file=sys.stderr, flush=True)
    try:
        result = subprocess.run([sys.executable, "-I", "-B", "-u", *argv], input=stdin, timeout=10)
    except subprocess.TimeoutExpired:
        return TIMED_OUT
    # Keep user exit statuses outside Docker's reserved 125–127 range.
    if payload.get("test_body"):
        return TESTS_PASSED if result.returncode == TESTS_PASSED else TESTS_FAILED
    return 0 if result.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
