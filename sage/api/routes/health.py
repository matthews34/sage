"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "sage",
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    # TODO: Add actual service checks (database, ollama, etc.)
    return {
        "status": "ready",
        "services": {
            "database": "unknown",
            "ollama": "unknown",
            "chromadb": "unknown",
        },
    }
