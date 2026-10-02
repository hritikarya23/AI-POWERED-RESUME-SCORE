import os
import sys

# 1. Ensure ROOT_DIR, current_dir, and /var/task are on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if "/var/task" not in sys.path:
    sys.path.insert(0, "/var/task")

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

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

# Standard FastAPI app object expected by Vercel's FastAPI framework runner
app = FastAPI(
    title="AI-Powered Resume Scorer API",
    version="1.0.0",
    docs_url="/api/docs",
)

# Enable CORS for all frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Vercel Internal Rewrite Path Recovery Middleware
# In Vercel, rewrites like /api/(.*) -> /api/index.py pass /api/index.py to FastAPI.
# This middleware restores the actual intended endpoint from Vercel's internal headers.
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


# Include API routes with /api prefix and direct
app.include_router(api_router, prefix="/api")
app.include_router(api_router)


@app.get("/api/index.py")
def index_fallback():
    return {
        "status": "healthy",
        "service": "AI-Powered Resume Scorer API",
        "version": "1.0.0",
        "platform": "Vercel Serverless",
    }


# Aliases for all possible Vercel entrypoint discovery patterns
application = app
handler = app
