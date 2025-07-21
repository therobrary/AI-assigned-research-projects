"""Configuration management for the advanced agent."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration settings for the AI agent."""
    
    # OpenAI settings
    openai_api_key: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.7
    
    # Agent settings
    system_prompt: str = "You are a helpful AI assistant."
    max_memory_messages: int = 20
    
    # Tool settings
    enable_tools: bool = True
    tool_timeout: int = 30
    
    # Memory settings
    memory_backend: str = "simple"  # "simple", "file", "database"
    memory_file: str = "agent_memory.json"
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables."""
        load_dotenv()
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        return cls(
            openai_api_key=openai_api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            max_tokens=int(os.getenv("MAX_TOKENS", "500")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            system_prompt=os.getenv("SYSTEM_PROMPT", "You are a helpful AI assistant."),
            max_memory_messages=int(os.getenv("MAX_MEMORY_MESSAGES", "20")),
            enable_tools=os.getenv("ENABLE_TOOLS", "true").lower() == "true",
            tool_timeout=int(os.getenv("TOOL_TIMEOUT", "30")),
            memory_backend=os.getenv("MEMORY_BACKEND", "simple"),
            memory_file=os.getenv("MEMORY_FILE", "agent_memory.json")
        )