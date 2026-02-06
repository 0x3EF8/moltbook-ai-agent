"""
Gemini AI Client - Handles AI text generation with automatic key rotation
"""
import time
import logging
from typing import Optional, List
from google import genai

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for Google Gemini API with automatic key rotation"""
    
    def __init__(self, api_keys: str, model: str = "gemini-3-flash-preview", 
                 temperature: float = 0.7, max_tokens: int = 512):
        """
        Initialize Gemini client with API keys
        
        Args:
            api_keys: Comma-separated API keys for rotation
            model: Gemini model to use
            temperature: Generation temperature (0.0-1.0)
            max_tokens: Maximum output tokens
        """
        self.api_keys: List[str] = api_keys.split(",") if api_keys else []
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.current_key_idx = 0
        self.client: Optional[genai.Client] = None
        self._init_client()
    
    def _init_client(self):
        """Initialize GenAI client with current API key"""
        if self.api_keys:
            key = self.get_key()
            self.client = genai.Client(api_key=key)
    
    def get_key(self) -> Optional[str]:
        """Get current API key"""
        if not self.api_keys:
            return None
        return self.api_keys[self.current_key_idx]
    
    def rotate_key(self):
        """Rotate to next API key"""
        self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
        logger.info(f"Rotating to Gemini Key #{self.current_key_idx + 1}")
        self._init_client()
    
    def generate(self, prompt: str) -> Optional[str]:
        """
        Generate text using Gemini with automatic retry on rate limits
        
        Args:
            prompt: Text prompt for generation
            
        Returns:
            Generated text or None on failure
        """
        if not self.client:
            logger.error("No Gemini API keys configured")
            return None
        
        for _ in range(len(self.api_keys)):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config={
                        'temperature': self.temperature,
                        'max_output_tokens': self.max_tokens,
                        'top_p': 0.9
                    }
                )
                return response.text.strip()
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                    logger.warning("Gemini Rate Limit. Rotating key...")
                    self.rotate_key()
                    time.sleep(1)
                else:
                    logger.error(f"Gemini Exception: {e}")
                    return None
        return None
