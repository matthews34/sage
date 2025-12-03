"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sage.api.routes import health, llm, stt, tts
from sage.config import get_settings

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Smart Autonomous General-purpose Engine - AI-powered application framework for edge devices",
    version=settings.app_version,
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(llm.router, prefix="/api/v1/llm", tags=["llm"])
app.include_router(stt.router, prefix="/api/v1/stt", tags=["stt"])
app.include_router(tts.router, prefix="/api/v1/tts", tags=["tts"])


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    pass
