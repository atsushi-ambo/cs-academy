import json
import logging
import re
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import BoundedSemaphore
from urllib.parse import parse_qs

from .content import ROOT
from .learning import RequestError, expect, fields

MAX_BODY = 128 * 1024
HOST = "127.0.0.1"
PORT = 4350
TEST_PORT = 4356
WEB = ROOT / "web"
STATIC = {
    "/": ("index.html", "text/html"),
    "/app.css": ("app.css", "text/css"),
    "/app.js": ("app.js", "text/javascript"),
    "/markdown.js": ("markdown.js", "text/javascript"),
}
CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; "
       "form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
GET_ROUTES = {
    "/api/today": "today",
    "/api/path": "path",
    "/api/play": "step_view",
    "/api/reviews": "reviews",
    "/api/placement": "placement",
    "/api/reference": "reference",
}
POST_ROUTES = {
    "/api/play": "play",
    "/api/review": "review",
    "/api/placement": "place",
    "/api/placement/skip": "skip",
}


def unique_object(pairs):
    body = dict(pairs)
    if len(body) != len(pairs):
        raise ValueError("Duplicate JSON field")
    return body


def invalid_constant(_):
    raise ValueError("Non-JSON number")


def handler_for(learning, port):
    allowed_hosts = [f"{HOST}:{port}", f"localhost:{port}"]

    class Handler(BaseHTTPRequestHandler):
        server_version = "CS-Academy"
        sys_version = ""

        def log_message(self, *_):
            pass

        def check_host(self):
            expect(self.headers.get_all("Host") in [[host] for host in allowed_hosts],
                   "Host rejected", 403)

        def read_body(self):
            host = self.headers["Host"]
            expect(self.headers.get_all("Origin") == [f"http://{host}"], "Origin rejected", 403)
            expect(self.headers.get_all("X-CS-Academy") == ["1"], "Required header missing", 403)
            expect(not self.headers.get_all("Transfer-Encoding"), "Unsupported transfer encoding")
            lengths = self.headers.get_all("Content-Length") or []
            expect(len(lengths) == 1 and re.fullmatch(r"[0-9]{1,10}", lengths[0]),
                   "Invalid content length")
            size = int(lengths[0])
            expect(size <= MAX_BODY, "Request body exceeds the size limit", 413)
            expect(self.headers.get_all("Content-Type") == ["application/json"],
                   "Expected application/json", 415)
            raw = self.rfile.read(size)
            expect(len(raw) == size, "Incomplete request body")
            try:
                body = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                                  parse_constant=invalid_constant)
            except (ValueError, RecursionError) as error:
                raise RequestError("Invalid JSON") from error
            expect(type(body) is dict, "Expected a JSON object")
            return body

        def send_payload(self, status, content, content_type):
            self.send_response(status)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", CSP)
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(content)

        def json_response(self, status, body):
            self.send_payload(status, json.dumps(body, ensure_ascii=True).encode(), "application/json")

        def get(self):
            path, separator, query = self.path.partition("?")
            if self.path == "/api/backups":
                with learning.store.locked():
                    return {"backups": learning.store.backups_list()}
            route = GET_ROUTES.get(path)
            if route is None:
                status = 405 if self.path in POST_ROUTES or self.path in {
                    "/api/backup", "/api/restore",
                } else 404
                raise RequestError("Route unavailable for GET", status)
            with learning.store.transaction() as db:
                method = getattr(learning, route)
                if route in {"step_view", "placement", "reference"}:
                    params = parse_qs(query, keep_blank_values=True, strict_parsing=True,
                                      max_num_fields=2)
                    if route == "step_view" and "step" in params:
                        fields(params, "unit", "step")
                    else:
                        fields(params, "unit")
                    expect(all(len(values) == 1 for values in params.values()),
                           "Duplicate query field")
                    if route == "step_view":
                        return method(db, params["unit"][0], params.get("step", [None])[0])
                    return method(db, params["unit"][0])
                expect(not separator, "Unexpected query")
                if route in {"today", "reviews"}:
                    return method(db, learning.clock())
                return method(db)

        def post(self, body):
            if self.path == "/api/backup":
                fields(body)
                return {"backup": learning.store.backup()}
            if self.path == "/api/restore":
                fields(body, "backup", "confirm")
                expect(isinstance(body["backup"], str) and body["confirm"] is True,
                       "Select a backup and confirm the restore")
                return {"saved_previous": learning.store.restore(body["backup"])}
            route = POST_ROUTES.get(self.path)
            expect(route is not None, "Unknown POST route", 404)
            with learning.store.transaction() as db:
                return getattr(learning, route)(db, body, learning.clock())

        def dispatch(self, is_post):
            try:
                self.check_host()
                if not is_post and self.path in STATIC:
                    filename, kind = STATIC[self.path]
                    self.send_payload(200, (WEB / filename).read_bytes(), kind)
                    return
                result = self.post(self.read_body()) if is_post else self.get()
                status = 503 if (result.get("status") == "unavailable"
                                 or result.get("execution", {}).get("status") == "unavailable") else 200
                self.json_response(status, result)
            except RequestError as error:
                self.json_response(error.status, {"error": str(error)})
            except ValueError as error:
                self.json_response(400, {"error": str(error)})
            except (BrokenPipeError, ConnectionResetError, TimeoutError):
                return
            except (OSError, sqlite3.Error):
                logging.exception("Local storage operation failed")
                self.json_response(500, {"error": "Storage operation failed. Check the server terminal."})

        def do_GET(self):
            self.dispatch(False)

        def do_POST(self):
            self.dispatch(True)

    return Handler


class Server(ThreadingHTTPServer):
    daemon_threads = False

    def __init__(self, learning, *, test=False):
        port = TEST_PORT if test else PORT
        self.slots = BoundedSemaphore(12)
        super().__init__((HOST, port), handler_for(learning, port))

    def get_request(self):
        client, address = super().get_request()
        client.settimeout(25)
        return client, address

    def process_request(self, request, client_address):
        if not self.slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()
