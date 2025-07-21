"""File-based memory storage for agent conversations."""

import json
import logging
from typing import List, Dict, Any
from .base_memory import BaseMemory


class FileMemory(BaseMemory):
    """
    File-based conversation storage.
    
    This memory backend persists conversation history to a JSON file,
    allowing conversations to continue across agent restarts.
    """
    
    def __init__(self, filename: str = "agent_memory.json", max_messages: int = 20):
        super().__init__(max_messages)
        self.filename = filename
        self.messages: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        # Try to load existing memory
        self.load()
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to memory."""
        message = {"role": role, "content": content}
        self.messages.append(message)
        
        # Truncate if necessary
        self.messages = self._truncate_messages(self.messages)
        
        # Auto-save after each message
        self.save()
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Get all messages in memory."""
        return self.messages.copy()
    
    def clear(self) -> None:
        """Clear all messages from memory."""
        self.messages.clear()
        self.save()
    
    def save(self) -> None:
        """Save memory state to file."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.messages, f, indent=2)
            self.logger.debug(f"Memory saved to {self.filename}")
        except Exception as e:
            self.logger.error(f"Failed to save memory to {self.filename}: {e}")
    
    def load(self) -> None:
        """Load memory state from file."""
        try:
            with open(self.filename, 'r') as f:
                self.messages = json.load(f)
            self.logger.debug(f"Memory loaded from {self.filename}")
        except FileNotFoundError:
            self.logger.debug(f"No existing memory file found at {self.filename}")
            self.messages = []
        except Exception as e:
            self.logger.error(f"Failed to load memory from {self.filename}: {e}")
            self.messages = []