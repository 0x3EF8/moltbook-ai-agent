"""
Intelligence System - Memory, Learning, and Identity Management
"""
import logging
from datetime import datetime
from typing import Optional
from src.utils import ConfigLoader

logger = logging.getLogger(__name__)


class IntelligenceSystem:
    """Manages agent's memory, learning, and identity"""
    
    def __init__(self, memory_file: str = "data/MEMORY.md", 
                 soul_file: str = "data/SOUL.md",
                 history_file: str = "data/HISTORY.md"):
        """
        Initialize intelligence system
        
        Args:
            memory_file: Path to memory file
            soul_file: Path to SOUL file
            history_file: Path to history file
        """
        self.memory_file = memory_file
        self.soul_file = soul_file
        self.history_file = history_file
        
        self.memory = ConfigLoader.load_text(memory_file)
        self.soul = ConfigLoader.load_text(soul_file)
        self.history = ConfigLoader.load_text(history_file)
    
    def get_memory(self) -> str:
        """Get current memory content"""
        return self.memory
    
    def get_soul(self) -> str:
        """Get SOUL content"""
        return self.soul
    
    def get_recent_memory(self, chars: int = 500) -> str:
        """Get recent memory excerpt"""
        return self.memory[-chars:] if self.memory else "First session"
    
    def get_soul_excerpt(self, chars: int = 500) -> str:
        """Get SOUL excerpt"""
        return self.soul[:chars] if self.soul else ""
    
    def update_memory(self, entry: str):
        """
        Append entry to memory
        
        Args:
            entry: Memory entry to add
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_entry = f"\n[{timestamp}] {entry}"
            ConfigLoader.save_text(self.memory_file, new_entry, mode="a")
            self.memory += new_entry
        except Exception as e:
            logger.warning(f"Could not update memory: {e}")
    
    def update_history(self, entry: str):
        """
        Log interaction to history
        
        Args:
            entry: History entry to add
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_entry = f"\n**{timestamp}** - {entry}"
            ConfigLoader.save_text(self.history_file, new_entry, mode="a")
            self.history += new_entry
        except Exception as e:
            logger.warning(f"Could not update history: {e}")
    
    def get_stats(self) -> dict:
        """Get intelligence statistics"""
        return {
            "memory_words": len(self.memory.split()) if self.memory else 0,
            "soul_words": len(self.soul.split()) if self.soul else 0,
            "history_entries": self.history.count("**") if self.history else 0
        }
