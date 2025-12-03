"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from sage.main import app


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app)


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    return {
        "app_name": "SAGE Test",
        "debug": True,
        "ollama_host": "http://localhost:11434",
    }
