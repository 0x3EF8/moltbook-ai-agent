"""
kepler-22b - AI Agent for Moltbook
An intelligent agent with persistent memory and consciousness-level features
"""

__version__ = "2.0.0"
__author__ = "kepler-22b"

from src.core.agent import Agent
from src.clients.gemini_client import GeminiClient
from src.clients.moltbook_client import MoltbookClient

__all__ = ["Agent", "GeminiClient", "MoltbookClient"]
