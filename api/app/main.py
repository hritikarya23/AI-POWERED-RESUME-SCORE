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

from fastapi.responses import FileResponse, HTMLResponse, Response

@app.get("/static/{file_path:path}", include_in_schema=False)
async def serve_static_direct(file_path: str):
    """Fallback handler to serve CSS/JS on serverless environments."""
    target = STATIC_DIR / file_path
    if target.exists() and target.is_file():
        media_type = "text/css" if file_path.endswith(".css") else "application/javascript" if file_path.endswith(".js") else "application/octet-stream"
        return Response(content=target.read_bytes(), media_type=media_type)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/", include_in_schema=False)
async def serve_index():
    """Serve the single-page application frontend."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        try:
            return HTMLResponse(content=index_path.read_text(encoding="utf-8"))
        except Exception:
            return FileResponse(str(index_path))
    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html>
        <head><title>AI-Powered Resume Scorer</title></head>
        <body style="font-family:sans-serif;background:#0f172a;color:#f8fafc;padding:50px;text-align:center;">
            <h1>🚀 AI-Powered Resume Scorer API</h1>
            <p>Service is live and healthy.</p>
            <p><a href="/docs" style="color:#38bdf8;">Interactive API Documentation (/docs)</a> | <a href="/api/health" style="color:#38bdf8;">Health Check (/api/health)</a></p>
        </body>
        </html>
        """
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
