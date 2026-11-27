import http.client
import json
import os
import socket
import threading
from contextlib import contextmanager
from datetime import timedelta

from app.server import HOST, TEST_PORT, Server, handler_for

from .support import FIX, SOLUTIONS

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
        progress = api.get("/api/play")
        step = progress["step"]
        case.assertEqual(progress["index"], i)
        case.assertEqual(progress["total"], 21)
        case.assertNotIn("answer", step)
        case.assertNotIn("solution", step)
        case.assertTrue(not step.get("tests") or isinstance(step["tests"], bool))

        def send(action, **fields):
            return api.post("/api/play", {"step": step["id"], "action": action, **fields})

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
    case.assertIsNone(api.get("/api/play")["step"])
    summary = api.get("/api/today")
    case.assertEqual(summary["completed"], 21)
    case.assertEqual(summary["xp"], 122)
    case.assertEqual(summary["quests"]["code"]["progress"], 5)
    case.assertEqual(summary["quests"]["step"]["progress"], 21)
    case.assertEqual(summary["due"], 0)
    case.date = case.date + timedelta(days=1)
    cards = api.get("/api/reviews")["due"]
    case.assertEqual([card["id"].split("/")[-1] for card in cards if "/st" in card["id"]],
                     ["st04", "st05"])
    case.assertEqual(cards[0]["due_day"], case.date.isoformat())
