"""Tests for configuration."""

import pytest

from sage.config import Settings, get_settings


@pytest.mark.unit
def test_settings_creation():
    """Test settings can be created."""
    settings = Settings()
    assert settings is not None
    assert settings.app_name == "SAGE"
    assert settings.app_version == "0.1.0"


@pytest.mark.unit
def test_get_settings():
    """Test get_settings returns cached instance."""
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2  # Should be same cached instance
