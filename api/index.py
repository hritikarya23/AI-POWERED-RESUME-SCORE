import os
import sys

# Ensure both api/ and project root are in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
ROOT_DIR = os.path.dirname(current_dir)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

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

# Include all API endpoints with /api prefix and direct
app.include_router(api_router, prefix="/api")
app.include_router(api_router)


@app.get("/api/health")
@app.get("/health")
@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "AI-Powered Resume Scorer API",
        "version": "1.0.0",
        "platform": "Vercel Native FastAPI",
    }
