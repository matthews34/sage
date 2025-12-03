"""Tests for LLM service."""

import pytest

from sage.core.llm import LLMService


@pytest.mark.unit
def test_llm_service_initialization():
    """Test LLM service initialization."""
    service = LLMService()
    assert service is not None
    assert service.host is not None
    assert service.default_model is not None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_llm_generate():
    """Test LLM generation (placeholder)."""
    service = LLMService()
    result = await service.generate("Test prompt")
    assert result is not None
    assert isinstance(result, str)
