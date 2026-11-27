import http.client
import json
import os
import socket
import threading
from contextlib import contextmanager
from datetime import timedelta
from urllib.parse import urlencode

from app.server import HOST, TEST_PORT, Server, handler_for

from .support import FIX, LISTS, SOLUTIONS

HOST_HEADER = f"{HOST}:{TEST_PORT}"
ORIGIN = f"http://{HOST_HEADER}"


class LocalConnection(http.client.HTTPConnection):
    def __init__(self, sock):
        super().__init__(HOST, TEST_PORT, timeout=25)
        self.socket_override = sock

    def connect(self):
        self.sock = self.socket_override


class API:
    def __init__(self, connection):
        self.connection = connection

    def request(self, path, *, method="GET", body=None, raw=None, host=HOST_HEADER,
                origin=ORIGIN, token="1", extra=None):
        headers = {"Host": host}
        if method == "POST":
            if origin is not None:
                headers["Origin"] = origin
            if token is not None:
                headers["X-CS-Academy"] = token
            headers["Content-Type"] = "application/json"
        headers.update(extra or {})
        data = raw if raw is not None else None if body is None else json.dumps(body).encode()
        with self.connection() as connection:
            connection.request(method, path, body=data, headers=headers)
            response = connection.getresponse()
            wire = response.read()
            payload = json.loads(wire) if response.headers["Content-Type"].startswith(
                "application/json"
            ) else wire
            return response.status, payload, response.headers

    def get(self, path):
        status, data, _ = self.request(path)
        if status != 200:
            raise AssertionError((status, data))
        return data

    def post(self, path, data):
        status, result, _ = self.request(path, method="POST", body=data)
        if status != 200:
            raise AssertionError((status, result))
        return result


def socketpair_api(learning):
    handler = handler_for(learning, TEST_PORT)

    @contextmanager
    def connection():
        def serve():
            with server:
                handler(server, (HOST, TEST_PORT), None)

        client, server = socket.socketpair()
        server.settimeout(25)
        thread = threading.Thread(target=serve)
        thread.start()
        conn = LocalConnection(client)
        try:
            yield conn
        finally:
            conn.close()
            client.close()
            thread.join(timeout=25)
            if thread.is_alive():
                raise AssertionError("HTTP handler did not finish")

    return API(connection)


@contextmanager
def tcp_api(case):
    try:
        server = Server(case.learning, test=True)
    except PermissionError as error:
        if os.environ.get("CS_ACADEMY_REQUIRE_TCP") or os.environ.get("CS_ACADEMY_REQUIRE_DOCKER"):
            raise
        case.skipTest(f"Loopback bind unavailable: {error}")
    with server:
        thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05})
        thread.start()

        @contextmanager
        def connection():
            conn = http.client.HTTPConnection(HOST, TEST_PORT, timeout=25)
            try:
                yield conn
            finally:
                conn.close()

        try:
            yield API(connection)
        finally:
            server.shutdown()
            thread.join()


def play_lists(case, api):
    predictable = [2, 1, 3, 1, 2, 1]
    starter_run = 'servers = ["web01", "web02", "web03", "db01"]\nprint(input())\nprint(len(servers))'

    for i in range(1, 22):
        progress = api.get(f"/api/play?unit={LISTS}")
        step = progress["step"]
        case.assertEqual(progress["index"], i)
        case.assertEqual(progress["total"], 21)
        case.assertNotIn("answer", step)
        case.assertNotIn("solution", step)
        case.assertTrue(not step.get("tests") or isinstance(step["tests"], bool))

        def send(action, **fields):
            return api.post("/api/play", {"unit": LISTS, "step": step["id"], "action": action, **fields})

        match step["type"]:
            case "read":
                finished = send("continue")
            case "try":
                finished = send("run", source=starter_run, stdin="入力を確認\n")
                case.assertIn("入力を確認", finished["stdout"])
                case.assertIn("4", finished["stdout"])
            case "predict":
                if i == 4:
                    case.assertIn("Which end", send("hint", level=1)["hint"])
                finished = send("answer", choice=predictable.pop(0))
                case.assertEqual(len(finished["why"]), 4)
            case "parsons":
                case.assertFalse(send("order", order=[0, 1, 2])["complete"])
                finished = send("order", order=[2, 1, 0])
                case.assertEqual(finished["stdout"], "['web01', 'web02']")
            case "fix" | "code":
                finished = send("tests", source=FIX if step["type"] == "fix" else SOLUTIONS)
                case.assertEqual(finished["status"], "passed", finished)
                case.assertTrue(finished["can_open_solution"])
                case.assertIn("def ", send("solution")["solution"])
            case other:
                case.fail(f"Unexpected step kind: {other}")
        case.assertTrue(finished["complete"], finished)
    case.assertIsNone(api.get(f"/api/play?unit={LISTS}")["step"])
    before = api.get("/api/today")
    play = api.get(f"/api/play?unit={LISTS}")
    case.assertEqual(len(play["completed_steps"]), 21)
    key = next(key for key in case.store.catalog.play[LISTS] if case.store.catalog.steps[key]["type"] == "code")
    past = api.get("/api/play?" + urlencode({"unit": LISTS, "step": key}))["step"]
    case.assertTrue(past["complete"])
    case.assertTrue(past["can_open_solution"])
    case.assertEqual(api.post("/api/play", {"unit": LISTS, "step": key, "action": "solution"})["solution"],
                     case.store.catalog.problems[key].solution)
    code = {"unit": LISTS, "step": key, "action": "tests", "source": SOLUTIONS}
    case.assertEqual(api.request("/api/play", method="POST", body=code)[0], 409)
    case.assertEqual(api.get("/api/today"), before)
    summary = api.get("/api/today")
    case.assertEqual(summary["unit"]["completed"], 21)
    case.assertEqual(summary["xp"], 122)
    case.assertEqual(summary["quests"]["code"]["progress"], 5)
    case.assertEqual(summary["quests"]["step"]["progress"], 21)
    case.assertEqual(summary["due"], 0)
    case.date = case.date + timedelta(days=1)
    cards = api.get("/api/reviews")["due"]
    case.assertEqual([card["id"].split("/")[-1] for card in cards if "/st" in card["id"]],
                     ["st04", "st05"])
    case.assertEqual(cards[0]["due_day"], case.date.isoformat())


TRY_EDITS = {
    "s1.m02.u02": [
        ('["web", "db"]', '["web", "db", "cache"]'),
        ("range(3, 0, -1)", "range(3, -1, -1)"),
        ("[4, 7]", "[4, 7, 3]"),
    ],
    "s1.m02.u03": [
        ("left = 2", "left = 4"),
        ("    checks += 1", "    checks += 1\n    left -= 1"),
    ],
    "s1.m02.u04": [
        ("count += 1", "count += ms"),
        ("[4, 7], [], [9]", "[4, 7], [5], [9]"),
    ],
    "s2.m05.u01": [
        ("range(1, 4)", "range(1, 5)"),
        ("scan(2)", "scan(3)"),
        ("print(ways(3))", "print(ways(4))"),
    ],
    "s2.m05.u03": [
        ("audit(1)", "audit(2)"),
        ("down(sys.getrecursionlimit() + 10)", "down(4)"),
        ("calls(7)", "calls(8)"),
    ],
    "s2.m05.u04": [
        ("[4, 8, 5], 1", "[4, 8, 5], 0"),
        ("walk([1, [2]])", "walk([1, []])"),
    ],
    "s2.m05.u05": [
        ("n = 2", "n = 3"),
        ('["first", "middle", "previous-last"]', 'reversed(["first", "middle", "previous-last"])'),
        ("range(2, 4)", "range(2, 5)"),
        (
            '        if level > 0:\n            pending.append(("open", level - 1))\n'
            '        pending.append(("close", level))',
            '        pending.append(("close", level))\n'
            '        if level > 0:\n            pending.append(("open", level - 1))',
        ),
    ],
}


def try_source(uid, step, index):
    if uid == LISTS:
        return 'print(input())\nprint(len(["web01", "web02", "web03", "db01"]))', "入力を確認\n"
    old, new = TRY_EDITS[uid][index]
    if old not in step["starter"]:
        raise AssertionError(f"Missing edit target in {step['id']}: {old}")
    return step["starter"].replace(old, new, 1), ""


def play_path(case, api):
    catalog = case.store.catalog
    graded = 0
    total = 0
    played = []
    for stage in api.get("/api/path")["stages"]:
        for module in stage["modules"]:
            for unit in module["units"]:
                uid = unit["id"]
                if uid not in catalog.play:
                    continue
                with case.subTest(unit=uid):
                    count, code = play_unit(case, api, uid)
                    total += count
                    graded += code
                    played.append(uid)
    case.assertEqual(played, [uid for uid in catalog.units if uid in catalog.play])
    summary = api.get("/api/today")
    case.assertEqual(summary["quests"]["step"]["progress"], total)
    case.assertEqual(summary["quests"]["code"]["progress"], graded)
    case.date += timedelta(days=1)
    due = api.get("/api/reviews")["due"]
    case.assertGreater(len({card["id"].split("/")[0] for card in due}), 1)


def play_unit(case, api, uid):
    catalog = case.store.catalog
    path = f"/api/play?unit={uid}"
    attempt = 0
    graded = 0
    api.post("/api/play", {"unit": uid, "action": "start"})

    def send(action, **fields):
        return api.post("/api/play", {"unit": uid, "step": key, "action": action, **fields})

    for index, key in enumerate(catalog.play[uid], 1):
        progress = api.get(path)
        step = progress["step"]
        raw = catalog.steps[key]
        with case.subTest(step=key):
            case.assertEqual(progress["index"], index)
            case.assertEqual(step["id"], key)
            case.assertNotIn("answer", step)
            case.assertNotIn("solution", step)
            case.assertTrue(not step.get("tests") or isinstance(step["tests"], bool))
            match step["type"]:
                case "read":
                    finished = send("continue")
                case "try":
                    source, stdin = try_source(uid, step, attempt)
                    finished = send("run", source=source, stdin=stdin)
                    if stdin:
                        case.assertIn(stdin.strip(), finished["stdout"])
                    attempt += 1
                case "predict":
                    finished = send("answer", choice=raw["answer"])
                    case.assertTrue(finished["correct"])
                    case.assertEqual(len(finished["why"]), 4)
                case "parsons":
                    case.assertEqual(step["lines"], raw["lines"][::-1])
                    finished = send("order", order=list(reversed(range(len(step["lines"])))))
                case "fix" | "code":
                    problem = catalog.problems[key]
                    rejected = send("tests", source=problem.starter)
                    case.assertEqual(rejected["status"], "failed", rejected)
                    case.assertFalse(rejected["complete"])
                    finished = send("tests", source=problem.solution)
                    case.assertEqual(finished["status"], "passed", finished)
                    case.assertEqual(send("solution")["solution"], problem.solution)
                    graded += 1
                case "explain":
                    payload = {"unit": uid, "step": key, "action": "explain",
                               "response": "This is my trace. The stopping case ends the work."}
                    status, _, _ = api.request("/api/play", method="POST",
                                               body={**payload, "self_checked": False})
                    case.assertEqual(status, 400)
                    finished = api.post("/api/play", {**payload, "self_checked": True})
                case other:
                    case.fail(f"Unexpected step kind: {other}")
            case.assertTrue(finished["complete"], finished)
    finished = api.get(path)
    case.assertIsNone(finished["step"])
    case.assertEqual(len(finished["completed_steps"]), finished["total"])
    return finished["total"], graded
