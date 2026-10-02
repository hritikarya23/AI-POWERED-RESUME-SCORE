import os
import sys
import json
import traceback
from http.server import BaseHTTPRequestHandler

# 1. Ensure ROOT_DIR is on sys.path so 'app' packages can be imported
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 2. Patch asyncio.Queue for older vc_init.py ASGI wrapper if Vercel attempts ASGI
import asyncio
try:
    _orig_queue_init = asyncio.Queue.__init__
    def _patched_queue_init(self, *args, **kwargs):
        kwargs.pop("loop", None)
        return _orig_queue_init(self, *args, **kwargs)
    asyncio.Queue.__init__ = _patched_queue_init
except Exception:
    pass

# 3. Create FastAPI app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

app = FastAPI(
    title="AI-Powered Resume Scorer API",
    version="1.0.0",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_error = None
try:
    from app.api.endpoints import router as api_router
    # Include with prefix '/api' and without prefix so all rewrite styles work
    app.include_router(api_router, prefix="/api")
    app.include_router(api_router)
except Exception as e:
    init_error = traceback.format_exc()

@app.get("/api/health")
@app.get("/health")
def health_endpoint():
    if init_error:
        return {
            "status": "initialization_error",
            "error": init_error,
            "root_dir": ROOT_DIR,
            "sys_path": sys.path[:5],
        }
    return {
        "status": "healthy",
        "service": "AI-Powered Resume Scorer",
        "version": "1.0.0",
        "platform": "Vercel Serverless"
    }

# TestClient to allow BaseHTTPRequestHandler to dispatch directly to FastAPI in-process
_test_client = TestClient(app)

class handler(BaseHTTPRequestHandler):
    """
    Vercel Serverless Function Handler.
    Compatible with both BaseHTTPRequestHandler and direct ASGI.
    """
    def _handle_request(self, method: str):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            headers = {k: v for k, v in self.headers.items() if k.lower() != "host"}
            
            # Determine path: ensure it reflects original requested path
            req_path = self.path
            if req_path in ("/api/index", "/api/index.py", "/api", "/api/"):
                orig = (
                    self.headers.get("x-matched-path")
                    or self.headers.get("x-invoke-path")
                    or self.headers.get("x-forwarded-uri")
                )
                if orig:
                    req_path = orig
            
            response = _test_client.request(
                method=method,
                url=req_path,
                headers=headers,
                content=body,
            )
            
            self.send_response(response.status_code)
            for k, v in response.headers.items():
                if k.lower() not in ("content-length", "content-encoding", "transfer-encoding"):
                    self.send_header(k, v)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Content-Length", str(len(response.content)))
            self.end_headers()
            self.wfile.write(response.content)
        except Exception as e:
            err_msg = json.dumps({
                "status": "error",
                "message": str(e),
                "traceback": traceback.format_exc(),
            }).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(err_msg)))
            self.end_headers()
            self.wfile.write(err_msg)

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

application = app
