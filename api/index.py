import os
import sys
import json
import traceback
from http.server import BaseHTTPRequestHandler

# 1. Ensure ROOT_DIR, current_dir, and /var/task are on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if "/var/task" not in sys.path:
    sys.path.insert(0, "/var/task")

# NOTE: Do NOT expose 'app' or 'application' at the module top level.
# This prevents Vercel from using its buggy asgi_cycle wrapper.
_fastapi_app = None
_test_client = None
_load_error = None


def _get_app_and_client():
    global _fastapi_app, _test_client, _load_error
    if _fastapi_app is not None:
        return _fastapi_app, _test_client, None
    if _load_error is not None:
        return None, None, _load_error

    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from starlette.testclient import TestClient
        from app.api.endpoints import router as api_router

        a = FastAPI(
            title="AI-Powered Resume Scorer API",
            version="1.0.0",
            docs_url="/api/docs",
        )
        a.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        a.include_router(api_router, prefix="/api")
        a.include_router(api_router)

        _fastapi_app = a
        _test_client = TestClient(a)
        return _fastapi_app, _test_client, None
    except Exception as e:
        _load_error = traceback.format_exc()
        return None, None, _load_error


class handler(BaseHTTPRequestHandler):
    def _respond_json(self, status_code: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_request(self, method: str):
        try:
            # 1. Recover original request path
            req_path = self.path
            if req_path in ("/api/index", "/api/index.py", "/api", "/api/"):
                orig = (
                    self.headers.get("x-matched-path")
                    or self.headers.get("x-invoke-path")
                    or self.headers.get("x-forwarded-uri")
                )
                if orig:
                    req_path = orig

            # Special diagnostic endpoint
            if req_path in ("/api/diagnostic", "/diagnostic"):
                try:
                    root_files = os.listdir(ROOT_DIR) if os.path.exists(ROOT_DIR) else []
                except Exception:
                    root_files = []
                try:
                    cur_files = os.listdir(current_dir) if os.path.exists(current_dir) else []
                except Exception:
                    cur_files = []
                try:
                    task_files = os.listdir("/var/task") if os.path.exists("/var/task") else []
                except Exception:
                    task_files = []

                _, _, err = _get_app_and_client()
                return self._respond_json(200, {
                    "status": "diagnostic",
                    "python_version": sys.version,
                    "cwd": os.getcwd(),
                    "sys_path": sys.path[:5],
                    "root_files": root_files,
                    "cur_files": cur_files,
                    "task_files": task_files,
                    "load_error": err,
                })

            # 2. Get App & TestClient
            f_app, client, err = _get_app_and_client()
            if err or client is None:
                return self._respond_json(500, {
                    "status": "app_initialization_error",
                    "error": err,
                    "path": req_path,
                })

            # 3. Read body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            # 4. Filter headers
            headers = {k: v for k, v in self.headers.items() if k.lower() != "host"}

            # 5. Dispatch in-memory
            response = client.request(
                method=method,
                url=req_path,
                headers=headers,
                content=body,
            )

            # 6. Send response
            self.send_response(response.status_code)
            for k, v in response.headers.items():
                if k.lower() not in ("content-length", "content-encoding", "transfer-encoding"):
                    self.send_header(k, v)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Content-Length", str(len(response.content)))
            self.end_headers()
            self.wfile.write(response.content)

        except Exception as e:
            self._respond_json(500, {
                "status": "server_error",
                "error": str(e),
                "traceback": traceback.format_exc(),
            })

    def do_GET(self):
        self._handle_request("GET")

    def do_POST(self):
        self._handle_request("POST")

    def do_PUT(self):
        self._handle_request("PUT")

    def do_DELETE(self):
        self._handle_request("DELETE")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Content-Length", "0")
        self.end_headers()
