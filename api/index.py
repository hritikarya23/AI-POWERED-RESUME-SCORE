import os
import sys
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure ROOT_DIR is on sys.path so 'app' packages can be imported
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

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

try:
    from app.api.endpoints import router as api_router
    # Include with prefix '/api' and without prefix so all rewrite styles work
    app.include_router(api_router, prefix="/api")
    app.include_router(api_router)
except Exception as e:
    err_tb = traceback.format_exc()
    @app.get("/api/health")
    @app.get("/health")
    def health_diag():
        return {
            "status": "initialization_error",
            "error": err_tb,
            "root_dir": ROOT_DIR,
            "sys_path": sys.path[:5],
        }

application = app
