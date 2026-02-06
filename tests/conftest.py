"""
Pytest configuration and fixtures
"""
import pytest


@pytest.fixture
def mock_env():
    """Mock environment variables"""
    return {
        "MOLTBOOK_API_KEY": "test_moltbook_key",
        "GEMINI_API_KEY": "test_gemini_key"
    }


@pytest.fixture
def mock_persona():
    """Mock persona configuration"""
    return {
        "name": "test-agent",
        "description": "Test agent for unit tests",
        "expertise": ["testing", "validation"],
        "tone": "test-friendly",
        "engagement_style": "test_mode"
    }
