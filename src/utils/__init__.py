"""
Configuration and data loading utilities
"""
import os
import json
from typing import Dict, Any, Optional


class ConfigLoader:
    """Handles loading of configuration files"""
    
    @staticmethod
    def load_env(env_file: str = ".env") -> Dict[str, str]:
        """Load environment variables from .env file"""
        if not os.path.exists(env_file):
            print(f"Warning: {env_file} not found.")
            return {}
        
        config = {}
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        return config
    
    @staticmethod
    def load_json(file_path: str) -> Optional[Dict[str, Any]]:
        """Load JSON configuration file"""
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} not found.")
            return None
        
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def load_text(file_path: str) -> str:
        """Load text/markdown file"""
        if not os.path.exists(file_path):
            return ""
        
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    @staticmethod
    def save_text(file_path: str, content: str, mode: str = "w"):
        """Save text to file"""
        try:
            with open(file_path, mode, encoding="utf-8") as f:
                f.write(content)
        except Exception as e:
            print(f"Error saving to {file_path}: {e}")
