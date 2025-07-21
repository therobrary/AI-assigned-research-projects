"""Base memory interface for AI agents."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseMemory(ABC):
    """
    Abstract base class for agent memory systems.
    
    Memory systems handle storing and retrieving conversation history,
    managing context windows, and persisting state between sessions.
    """
    
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
    
    @abstractmethod
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to memory.
        
        Args:
            role: The role of the message sender (system, user, assistant)
            content: The message content
        """
        pass
    
    @abstractmethod
    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages in memory.
        
        Returns:
            List of message dictionaries with 'role' and 'content' keys
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all messages from memory."""
        pass
    
    @abstractmethod
    def save(self) -> None:
        """Save memory state (if persistent backend supports it)."""
        pass
    
    @abstractmethod
    def load(self) -> None:
        """Load memory state (if persistent backend supports it)."""
        pass
    
    def _truncate_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Truncate messages to stay within max_messages limit.
        Always keeps the system message (first message) if present.
        """
        if len(messages) <= self.max_messages:
            return messages
        
        # Keep system message + most recent messages
        if messages and messages[0].get("role") == "system":
            return [messages[0]] + messages[-(self.max_messages - 1):]
        else:
            return messages[-self.max_messages:]