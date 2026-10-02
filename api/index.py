import os
import sys
import traceback
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI-Powered Resume Scorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Add current_dir (api/) and root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
ROOT_DIR = os.path.dirname(current_dir)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import_error = None
try:
    from app.api.endpoints import router as api_router
    app.include_router(api_router, prefix="/api")
    app.include_router(api_router)
except Exception as e:
    import_error = traceback.format_exc()


@app.get("/api/health")
@app.get("/health")
@app.get("/api/index.py")
@app.get("/api/index")
@app.get("/api")
@app.get("/")
def health_check(request: Request):
    return {
        "status": "healthy" if not import_error else "import_error",
        "python": sys.version,
        "cwd": os.getcwd(),
        "sys_path": sys.path[:5],
        "headers": dict(request.headers),
        "import_error": import_error,
    }
