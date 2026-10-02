"""Main FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.endpoints import router as api_router
from app.services.semantic import SemanticMatcher

# Directories
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-warm SentenceTransformers model during application startup."""
    print("Initializing AI-Powered Resume Scorer engine...")
    matcher = SemanticMatcher.get_instance()
    engine_name = "SentenceTransformer (all-MiniLM-L6-v2)" if matcher.is_neural else "TF-IDF Vectorizer Fallback"
    print(f"AI Engine Status: Active ({engine_name})")
    yield


app = FastAPI(
    title="AI-Powered Resume Scorer API",
    description="Intelligent ATS & Semantic Resume Scorer comparing resumes against job descriptions with AI matching and improvement tips.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(api_router, prefix="/api", tags=["Scoring & Analysis"])

# Mount static assets directory
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_index():
    """Serve the single-page application frontend."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {
        "message": "AI-Powered Resume Scorer API is running. Visit /docs for the interactive Swagger documentation.",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
