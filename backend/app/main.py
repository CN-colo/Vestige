from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from pathlib import Path

from .config import settings
from .database import init_db
from .routers import auth, articles, projects, public, ai, media, keys, favorites, comments, follows, tag_subscriptions, likes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database
    init_db()
    # Ensure uploads directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Mount static files for documentation (AGENT_GUIDE.md, AI_API.md in project root)
project_root = Path(__file__).parent.parent.parent
docs_dir = project_root
if docs_dir.exists():
    # Only mount if the directory exists (for development)
    app.mount("/docs-static", StaticFiles(directory=str(docs_dir), html=True), name="docs-static")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(articles.router, prefix="/api/articles", tags=["Articles"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(public.router, prefix="/api/public", tags=["Public"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(media.router, prefix="/api/media", tags=["Media"])
app.include_router(keys.router, prefix="/api/keys", tags=["API Keys"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["Favorites"])
app.include_router(comments.router, prefix="/api/comments", tags=["Comments"])
app.include_router(follows.router, prefix="/api/follows", tags=["Follows"])
app.include_router(tag_subscriptions.router, prefix="/api/subscriptions", tags=["Tag Subscriptions"])
app.include_router(likes.router, prefix="/api/likes", tags=["Likes"])


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "message": "Welcome to Vestige API"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}