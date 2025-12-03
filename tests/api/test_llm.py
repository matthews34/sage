"""Tests for LLM endpoints."""

import pytest


@pytest.mark.unit
def test_chat_endpoint(client):
    """Test chat endpoint."""
    payload = {
        "prompt": "Hello, how are you?",
        "model": "tinyllama",
    }
    response = client.post("/api/v1/llm/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "model" in data


@pytest.mark.unit
def test_chat_endpoint_validation(client):
    """Test chat endpoint validation."""
    # Missing required field
    response = client.post("/api/v1/llm/chat", json={})
    assert response.status_code == 422  # Validation error
