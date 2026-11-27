import json
import subprocess
import sys

from .content import ROOT


def run_problem(problem_id, source, stdin=None):
    request = {"problem_id": problem_id, "source": source}
    if stdin is not None:
        request["stdin"] = stdin
    try:
        child = subprocess.run(
            [sys.executable, "-m", "runner.host"], cwd=ROOT,
            input=json.dumps(request, ensure_ascii=False).encode("utf-8"),
            capture_output=True, timeout=17, check=True,
        )
        return json.loads(child.stdout)
    except (OSError, ValueError, subprocess.SubprocessError):
        return {"status": "unavailable", "stdout": "", "stderr": "Runner process failed.",
                "truncated": False}
