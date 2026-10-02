import os
import sys
import traceback

# Ensure both api/ and project root are in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
ROOT_DIR = os.path.dirname(current_dir)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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


@app.middleware("http")
async def vercel_path_rewrite_recovery(request: Request, call_next):
    if request.url.path in ("/api/index.py", "/api/index", "/api", "/api/"):
        real_path = (
            request.headers.get("x-matched-path")
            or request.headers.get("x-invoke-path")
            or request.headers.get("x-forwarded-uri")
        )
        if real_path:
            clean_path = real_path.split("?")[0]
            if clean_path not in ("/api/index.py", "/api/index", "/api", "/api/"):
                request.scope["path"] = clean_path
                request.scope["raw_path"] = clean_path.encode()

    response = await call_next(request)
    return response


# Import and mount router
init_error = None
try:
    from app.api.endpoints import router as api_router
    app.include_router(api_router, prefix="/api")
    app.include_router(api_router)
except Exception:
    init_error = traceback.format_exc()


@app.api_route("/api/health", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/health", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/api/index.py", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/api/index", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/api", methods=["GET", "POST", "OPTIONS"])
@app.api_route("/", methods=["GET", "POST", "OPTIONS"])
def health_check():
    if init_error:
        return {
            "status": "initialization_error",
            "error": init_error,
            "sys_path": sys.path[:5],
            "current_dir": current_dir,
            "contents": os.listdir(current_dir),
        }
    return {
        "status": "healthy",
        "service": "AI-Powered Resume Scorer API",
        "version": "1.0.0",
        "platform": "Vercel Serverless",
    }


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def catch_all(request: Request, full_path: str):
    return {
        "status": "catch_all_matched",
        "full_path": full_path,
        "url_path": str(request.url.path),
        "scope_path": request.scope.get("path"),
        "init_error": init_error,
        "matched_path_header": request.headers.get("x-matched-path"),
        "invoke_path_header": request.headers.get("x-invoke-path"),
        "routes": [getattr(r, "path", str(type(r))) for r in app.routes],
    }

