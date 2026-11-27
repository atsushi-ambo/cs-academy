from datetime import timedelta

from app.content import LISTS, SOURCE_LIMIT, STDIN_LIMIT
from app.server import MAX_BODY, TEST_PORT

from .http_support import play_lists, socketpair_api, tcp_api
from .support import FIX, PLACEMENT_SOURCE, AcademyCase


class HTTPTest(AcademyCase):
    def setUp(self):
        super().setUp()
        self.api = socketpair_api(self.learning)

    def test_security_headers_and_api_guards(self):
        for host in ["evil.example", "127.0.0.1", "127.0.0.1:4350"]:
            with self.subTest(host=host):
                status, _, _ = self.api.request("/api/today", host=host)
                self.assertEqual(status, 403)
        status, html, headers = self.api.request("/", host=f"localhost:{TEST_PORT}")
        self.assertEqual(status, 200)
        self.assertIn(b'src="/app.js"', html)
        self.assertIn("script-src 'self'", headers["Content-Security-Policy"])
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(headers["Referrer-Policy"], "no-referrer")

        action = {"step": f"{LISTS}/st01", "action": "continue"}
        for kwargs, expected in [
            ({"origin": "http://evil.example"}, 403),
            ({"origin": f"http://localhost:{TEST_PORT}"}, 403),
            ({"origin": None}, 403),
            ({"token": None}, 403),
            ({"raw": b"["}, 400),
            ({"raw": b'{"step": 1, "step": 2}'}, 400),
            ({"raw": b"[]"}, 400),
            ({"raw": b"", "extra": {"Content-Length": str(MAX_BODY + 1)}}, 413),
            ({"extra": {"Content-Type": "text/plain"}}, 415),
        ]:
            with self.subTest(expected=expected, keys=list(kwargs)):
                status, _, _ = self.api.request("/api/play", method="POST", body=action, **kwargs)
                self.assertEqual(status, expected)
        self.assertEqual(self.api.request("/api/backup")[0], 405)
        self.assertEqual(self.api.request("/api/placement/skip")[0], 405)
        self.assertEqual(self.api.request(f"/api/play?step={LISTS}/st01")[0], 404)
        self.assertEqual(self.api.request("/api/play?step=x&step=y")[0], 400)
        self.assertEqual(self.api.get("/api/today")["completed"], 0)
        self.assertFalse(self.store.backups.exists())
        self.assertTrue(self.api.post("/api/play", action)["complete"])

    def test_solution_lock_and_execution_counts(self):
        def post(step, action, **fields):
            return self.api.post("/api/play", {"step": f"{LISTS}/{step}", "action": action, **fields})

        post("st01", "continue")
        step2 = {"step": f"{LISTS}/st02", "action": "run"}
        for source, stdin in [("日" * (SOURCE_LIMIT // 3 + 1), ""), ("", "a" * (STDIN_LIMIT + 1))]:
            status, _, _ = self.api.request(
                "/api/play", method="POST", body={**step2, "source": source, "stdin": stdin},
            )
            self.assertEqual(status, 400)
        post("st02", "run", source="print(4)", stdin="input")
        post("st03", "continue")
        post("st04", "answer", choice=2)
        post("st05", "answer", choice=0)
        post("st06", "continue")
        post("st07", "order", order=[2, 1, 0])
        post("st08", "continue")
        post("st09", "answer", choice=3)
        key = f"{LISTS}/st10"
        tests = {"step": key, "action": "tests", "source": "unavailable"}
        status, _, _ = self.api.request("/api/play", method="POST", body={**tests, "tests": "foo"})
        self.assertEqual(status, 400)
        status, data, _ = self.api.request("/api/play", method="POST", body=tests)
        self.assertEqual(status, 503)
        self.assertEqual(data["failures"], 0)
        solution = {"step": key, "action": "solution"}
        self.assertEqual(self.api.request("/api/play", method="POST", body=solution)[0], 409)
        baseline = self.api.get("/api/today")["xp"]
        for i in range(1, 4):
            run = post("st10", "run", source=FIX, stdin="")
            self.assertFalse(run["complete"])
            failed = post("st10", "tests", source="starter")
            self.assertEqual(failed["failures"], i)
            self.assertEqual(failed["can_open_solution"], i == 3)
        self.assertEqual(self.api.get("/api/today")["xp"], baseline)
        self.assertEqual(post("st10", "solution")["solution"], FIX)
        for level in range(1, 4):
            self.assertTrue(post("st10", "hint", level=level)["hint"])
        self.assertTrue(post("st10", "tests", source=FIX)["complete"])
        self.assertEqual(self.api.get("/api/today")["xp"], baseline + 6)
        with self.store.transaction() as db:
            self.assertEqual(db.execute(
                "SELECT COUNT(*) FROM attempts WHERE step_id=? AND action='tests'", (key,),
            ).fetchone()[0], 4)

    def test_lists_journey_over_http_handler(self):
        play_lists(self, self.api)
        self.assertEqual(self.api.get("/api/today")["streak"], 1)

    def test_placement_and_restore_over_http(self):
        pre = self.api.post("/api/backup", {})["backup"]
        self.assertIn(pre, self.api.get("/api/backups")["backups"])
        self.assertFalse(self.api.get("/api/placement")["can_skip"])
        unavailable, _, _ = self.api.request(
            "/api/placement", method="POST", body={"answers": [2, 0, 3, 2], "source": "unavailable"},
        )
        self.assertEqual(unavailable, 503)
        passed = self.api.post("/api/placement", {"answers": [2, 0, 3, 2], "source": PLACEMENT_SOURCE})
        self.assertTrue(passed["passed"])
        self.assertTrue(self.api.get("/api/placement")["can_skip"])
        self.assertEqual(self.api.get("/api/today")["completed"], 0)
        self.assertEqual(len(self.api.get("/api/reviews")["due"]), 0)
        self.api.post("/api/placement/skip", {})
        due = self.api.get("/api/reviews")["due"]
        self.assertEqual(len(due), 2)
        self.assertEqual(due[0]["id"], f"{LISTS}/st04")
        self.assertTrue(self.api.get("/api/today")["skipped"])
        self.date += timedelta(days=1)
        self.assertEqual(len(self.api.get("/api/reviews")["due"]), 4)
        status, _, _ = self.api.request("/api/restore", method="POST",
                                        body={"backup": pre, "confirm": False})
        self.assertEqual(status, 400)
        self.assertIsNotNone(self.api.post("/api/restore", {"backup": pre, "confirm": True})[
            "saved_previous"
        ])
        self.assertFalse(self.api.get("/api/today")["skipped"])
        self.assertIsNone(self.api.get("/api/placement")["result"])

    def test_loopback_lists_journey_on_port_4356(self):
        with tcp_api(self) as api:
            play_lists(self, api)
