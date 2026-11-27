from datetime import timedelta
from urllib.parse import urlencode

from app.content import SOURCE_LIMIT, STDIN_LIMIT
from app.server import MAX_BODY, TEST_PORT

from .http_support import play_lists, play_path, socketpair_api, tcp_api
from .support import FIX, FOR, LISTS, PLACEMENT_SOURCE, RECURSION, WHILE, AcademyCase, result


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

        action = {"unit": LISTS, "step": f"{LISTS}/st01", "action": "continue"}
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
        self.assertEqual(self.api.request(f"/api/play?unit={LISTS}&step={LISTS}/st01")[0], 404)
        self.assertEqual(self.api.request(f"/api/play?unit={LISTS}&step=x&step=y")[0], 400)
        self.assertEqual(self.api.get("/api/today")["unit"]["completed"], 0)
        self.assertFalse(self.store.backups.exists())
        self.assertTrue(self.api.post("/api/play", action)["complete"])

    def test_solution_lock_and_execution_counts(self):
        def post(step, action, **fields):
            return self.api.post("/api/play", {"unit": LISTS, "step": f"{LISTS}/{step}", "action": action, **fields})

        post("st01", "continue")
        step2 = {"unit": LISTS, "step": f"{LISTS}/st02", "action": "run"}
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
        tests = {"unit": LISTS, "step": key, "action": "tests", "source": "unavailable"}
        status, _, _ = self.api.request("/api/play", method="POST", body={**tests, "tests": "foo"})
        self.assertEqual(status, 400)
        status, data, _ = self.api.request("/api/play", method="POST", body=tests)
        self.assertEqual(status, 503)
        self.assertEqual(data["failures"], 0)
        solution = {"unit": LISTS, "step": key, "action": "solution"}
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
        self.assertFalse(self.api.get(f"/api/placement?unit={LISTS}")["can_skip"])
        unavailable, _, _ = self.api.request(
            "/api/placement", method="POST", body={"unit": LISTS, "answers": [2, 0, 3, 2], "source": "unavailable"},
        )
        self.assertEqual(unavailable, 503)
        passed = self.api.post("/api/placement", {"unit": LISTS, "answers": [2, 0, 3, 2], "source": PLACEMENT_SOURCE})
        self.assertTrue(passed["passed"])
        self.assertTrue(self.api.get(f"/api/placement?unit={LISTS}")["can_skip"])
        self.assertEqual(self.api.get("/api/today")["unit"]["completed"], 0)
        self.assertEqual(len(self.api.get("/api/reviews")["due"]), 0)
        self.api.post("/api/placement/skip", {"unit": LISTS})
        due = self.api.get("/api/reviews")["due"]
        self.assertEqual(len(due), 2)
        self.assertEqual(due[0]["id"], f"{LISTS}/st04")
        self.assertTrue(self.api.get("/api/today")["unit"]["skipped"])
        self.date += timedelta(days=1)
        self.assertEqual(len(self.api.get("/api/reviews")["due"]), 4)
        status, _, _ = self.api.request("/api/restore", method="POST",
                                        body={"backup": pre, "confirm": False})
        self.assertEqual(status, 400)
        self.assertIsNotNone(self.api.post("/api/restore", {"backup": pre, "confirm": True})[
            "saved_previous"
        ])
        self.assertFalse(self.api.get("/api/today")["unit"]["skipped"])
        self.assertIsNone(self.api.get(f"/api/placement?unit={LISTS}")["result"])

    def test_loopback_lists_journey_on_port_4356(self):
        with tcp_api(self) as api:
            play_lists(self, api)


class MultiUnitHTTPTest(AcademyCase):
    lists_only = False

    def setUp(self):
        super().setUp()
        self.learning.runner = self.runner
        self.api = socketpair_api(self.learning)

    def runner(self, key, source, stdin=None):
        problem = self.store.catalog.problems[key]
        if stdin is not None:
            check = self.store.catalog.steps[key]["check"]
            return result("passed", stdout=f"{stdin.strip()}\n{check['stdout_line']}\n")
        return result("failed" if source == problem.starter else "passed")

    def units(self):
        return [unit for stage in self.api.get("/api/path")["stages"]
                for module in stage["modules"] for unit in module["units"]]

    def test_all_playable_units_over_http_handler(self):
        play_path(self, self.api)
        units = self.units()
        self.assertEqual([unit["id"] for unit in units if unit["status"] == "completed"],
                         [uid for uid in self.store.catalog.units if uid in self.store.catalog.play])

    def test_loopback_path_over_tcp(self):
        with tcp_api(self) as api:
            play_path(self, api)

    def test_unit_validation_and_prerequisites(self):
        units = {unit["id"]: unit for unit in self.units()}
        self.assertEqual(units["s1.m02.u01"]["status"], "outline")
        self.assertFalse(units[FOR]["blockers"])
        self.assertEqual(units[WHILE]["blockers"][0]["id"], FOR)
        for route in ("play", "reference", "placement"):
            for uid in ("../data", "unknown", "s1.m02.u01"):
                self.assertEqual(self.api.request(f"/api/{route}?" + urlencode({"unit": uid}))[0], 404)
        for uid in ([], {}, "unknown"):
            status, _, _ = self.api.request("/api/play", method="POST", body={"unit": uid, "action": "start"})
            self.assertEqual(status, 404)
        self.assertEqual(self.api.request(f"/api/play?unit={WHILE}")[0], 409)
        status, _, _ = self.api.request("/api/play", method="POST",
                                        body={"unit": WHILE, "action": "start"})
        self.assertEqual(status, 409)
        status, _, _ = self.api.request("/api/play", method="POST",
                                        body={"unit": FOR, "step": f"{WHILE}/st01", "action": "continue"})
        self.assertEqual(status, 404)
        self.assertEqual(self.api.request(f"/api/play?unit={FOR}&unit={WHILE}")[0], 400)
        self.assertIn("loop", self.api.get(f"/api/reference?unit={FOR}")["lesson"])
        self.assertEqual(self.api.request(f"/api/placement?unit={WHILE}")[0], 404)

    def pass_placement(self, uid):
        catalog = self.store.catalog
        questions = catalog.placements[uid]["questions"]
        answers = [catalog.steps[key]["answer"] for key in questions]
        placement = self.api.post("/api/placement", {"unit": uid, "answers": answers, "source": "solution"})
        self.assertTrue(placement["passed"])
        self.assertTrue(self.api.get(f"/api/placement?unit={uid}")["can_skip"])

    def test_placement_recency_and_cross_unit_review(self):
        self.pass_placement(FOR)
        self.assertEqual(self.api.request(f"/api/play?unit={WHILE}")[0], 409)
        self.api.post("/api/placement/skip", {"unit": FOR})
        self.assertEqual(self.api.request(f"/api/play?unit={WHILE}")[0], 200)
        self.assertIsNone(self.api.get(f"/api/placement?unit={RECURSION}")["result"])
        self.pass_placement(RECURSION)
        self.api.post("/api/placement/skip", {"unit": RECURSION})
        for uid in (WHILE, LISTS):
            self.api.post("/api/play", {"unit": uid, "action": "start"})
            self.assertEqual(self.api.get("/api/today")["unit"]["id"], uid)
        self.api.post("/api/play", {"unit": WHILE, "step": f"{WHILE}/st01", "action": "continue"})
        summary = self.api.get("/api/today")
        self.assertEqual((summary["unit"]["id"], summary["unit"]["completed"]), (WHILE, 1))
        self.assertEqual(summary["quests"]["step"]["progress"], 1)
        due = self.api.get("/api/reviews")["due"]
        self.assertEqual({card["id"].split("/")[0] for card in due}, {RECURSION, FOR})
        card = next(card for card in due if card["id"].startswith(RECURSION + "/"))
        wrong = (self.store.catalog.steps[card["id"]]["answer"] + 1) % 4
        self.api.post("/api/review", {"card": card["id"], "choice": wrong, "retry": False})
        self.assertEqual([unit["id"] for unit in self.api.get("/api/today")["recommended"]], [RECURSION])
        self.assertEqual(self.api.get("/api/today")["quests"]["review"]["progress"], 1)
