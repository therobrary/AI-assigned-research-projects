"""Simple in-memory storage for agent conversations."""

from typing import List, Dict, Any
from .base_memory import BaseMemory


class SimpleMemory(BaseMemory):
    """
    Simple in-memory conversation storage.
    
    This memory backend stores conversation history in memory only.
    Data is lost when the agent is restarted.
    """
    
    def __init__(self, max_messages: int = 20):
        super().__init__(max_messages)
        self.messages: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to memory."""
        message = {"role": role, "content": content}
        self.messages.append(message)
        
        # Truncate if necessary
        self.messages = self._truncate_messages(self.messages)
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """Get all messages in memory."""
        return self.messages.copy()
    
    def clear(self) -> None:
        """Clear all messages from memory."""
        self.messages.clear()
    
    def save(self) -> None:
        """Save memory state (no-op for in-memory storage)."""
        pass  # In-memory storage doesn't persist
    
    def load(self) -> None:
        """Load memory state (no-op for in-memory storage)."""
        pass  # In-memory storage doesn't persist