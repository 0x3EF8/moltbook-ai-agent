"""
Unit tests for GeminiClient
"""
import pytest
from unittest.mock import Mock, patch
from src.clients.gemini_client import GeminiClient


class TestGeminiClient:
    """Test suite for Gemini AI client"""
    
    def test_init_with_single_key(self):
        """Test initialization with single API key"""
        client = GeminiClient("test_key_123")
        assert len(client.api_keys) == 1
        assert client.api_keys[0] == "test_key_123"
        assert client.model == "gemini-3-flash-preview"
        assert client.temperature == 0.7
        assert client.max_tokens == 512
    
    def test_init_with_multiple_keys(self):
        """Test initialization with multiple API keys"""
        client = GeminiClient("key1,key2,key3")
        assert len(client.api_keys) == 3
        assert client.api_keys == ["key1", "key2", "key3"]
    
    def test_get_key(self):
        """Test getting current API key"""
        client = GeminiClient("key1,key2")
        assert client.get_key() == "key1"
        client.current_key_idx = 1
        assert client.get_key() == "key2"
    
    def test_rotate_key(self):
        """Test key rotation"""
        client = GeminiClient("key1,key2,key3")
        assert client.current_key_idx == 0
        
        client.rotate_key()
        assert client.current_key_idx == 1
        
        client.rotate_key()
        assert client.current_key_idx == 2
        
        client.rotate_key()  # Should wrap around
        assert client.current_key_idx == 0
    
    def test_authentication_header_format(self):
        """Test that authentication is properly configured"""
        client = GeminiClient("test_key")
        assert client.get_key() == "test_key"
    
    @patch('src.clients.gemini_client.genai.Client')
    def test_generate_with_config(self, mock_client_class):
        """Test that generate passes correct configuration"""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = "Generated text"
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        client = GeminiClient("test_key", temperature=0.8, max_tokens=256)
        result = client.generate("Test prompt")
        
        # Verify generate_content was called with config
        mock_client.models.generate_content.assert_called_once()
        call_kwargs = mock_client.models.generate_content.call_args[1]
        assert 'config' in call_kwargs
        assert call_kwargs['config']['temperature'] == 0.8
        assert call_kwargs['config']['max_output_tokens'] == 256
        assert result == "Generated text"
