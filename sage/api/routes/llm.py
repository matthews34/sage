"""LLM endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request model."""

    prompt: str
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int | None = None


class ChatResponse(BaseModel):
    """Chat response model."""

    response: str
    model: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Generate chat completion using LLM."""
    # TODO: Implement actual LLM integration
    return ChatResponse(
        response="This is a placeholder response. LLM integration pending.",
        model=request.model or "tinyllama",
    )
