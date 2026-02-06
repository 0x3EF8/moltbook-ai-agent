"""
Unit tests for IntelligenceSystem
"""
import pytest
import tempfile
import os
from src.intelligence import IntelligenceSystem


class TestIntelligenceSystem:
    """Test suite for Intelligence System"""
    
    def test_init_with_nonexistent_files(self):
        """Test initialization with non-existent files"""
        intel = IntelligenceSystem(
            memory_file="nonexistent_memory.md",
            soul_file="nonexistent_soul.md",
            history_file="nonexistent_history.md"
        )
        assert intel.memory == ""
        assert intel.soul == ""
        assert intel.history == ""
    
    def test_get_stats_empty(self):
        """Test stats with empty files"""
        intel = IntelligenceSystem(
            memory_file="nonexistent.md",
            soul_file="nonexistent.md",
            history_file="nonexistent.md"
        )
        stats = intel.get_stats()
        assert stats['memory_words'] == 0
        assert stats['soul_words'] == 0
        assert stats['history_entries'] == 0
    
    def test_get_recent_memory_empty(self):
        """Test getting recent memory when empty"""
        intel = IntelligenceSystem(memory_file="nonexistent.md")
        recent = intel.get_recent_memory()
        assert recent == "First session"
    
    def test_get_recent_memory_excerpt(self):
        """Test memory excerpt with content"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write("A" * 1000)
            temp_file = f.name
        
        try:
            intel = IntelligenceSystem(memory_file=temp_file)
            recent = intel.get_recent_memory(chars=100)
            assert len(recent) == 100
            assert recent == "A" * 100
        finally:
            os.unlink(temp_file)
    
    def test_update_memory_adds_timestamp(self):
        """Test that memory updates include timestamps"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write("Initial content")
            temp_file = f.name
        
        try:
            intel = IntelligenceSystem(memory_file=temp_file)
            intel.update_memory("Test entry")
            
            # Read back the file
            with open(temp_file, 'r') as f:
                content = f.read()
            
            assert "Test entry" in content
            assert "[" in content  # Timestamp format
            assert "]" in content
        finally:
            os.unlink(temp_file)
    
    def test_get_soul_excerpt(self):
        """Test getting SOUL excerpt"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write("SOUL content here with personality traits and directives")
            temp_file = f.name
        
        try:
            intel = IntelligenceSystem(soul_file=temp_file)
            excerpt = intel.get_soul_excerpt(chars=20)
            assert len(excerpt) == 20
            assert excerpt == "SOUL content here wi"
        finally:
            os.unlink(temp_file)
