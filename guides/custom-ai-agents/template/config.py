"""Configuration module for the AI agent template."""

import os
import logging
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class AgentConfig:
    """Configuration settings for the AI agent."""
    
    # OpenAI settings
    openai_api_key: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.7
    
    # Agent behavior
    system_prompt: str = "You are a helpful AI assistant."
    max_memory_messages: int = 20
    
    # File settings
    memory_file: str = "agent_memory.json"
    
    # Logging
    log_level: int = logging.INFO
    
    @classmethod
    def from_env(cls, env_file: str = ".env") -> 'AgentConfig':
        """
        Create configuration from environment variables.
        
        Args:
            env_file: Path to .env file (default: ".env")
            
        Returns:
            AgentConfig instance
            
        Raises:
            ValueError: If required environment variables are missing
        """
        load_dotenv(env_file)
        
        # Required settings
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file."
            )
        
        # Optional settings with defaults
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        max_tokens = int(os.getenv("MAX_TOKENS", "500"))
        temperature = float(os.getenv("TEMPERATURE", "0.7"))
        
        system_prompt = os.getenv(
            "SYSTEM_PROMPT", 
            "You are a helpful AI assistant."
        )
        max_memory_messages = int(os.getenv("MAX_MEMORY_MESSAGES", "20"))
        memory_file = os.getenv("MEMORY_FILE", "agent_memory.json")
        
        # Logging level
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        
        return cls(
            openai_api_key=openai_api_key,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system_prompt=system_prompt,
            max_memory_messages=max_memory_messages,
            memory_file=memory_file,
            log_level=log_level
        )
    
    def validate(self) -> None:
        """
        Validate configuration settings.
        
        Raises:
            ValueError: If any settings are invalid
        """
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        
        if not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0 and 2")
        
        if self.max_memory_messages <= 0:
            raise ValueError("max_memory_messages must be positive")


# Example configuration presets
CODING_ASSISTANT_CONFIG = {
    "system_prompt": (
        "You are a helpful coding assistant. Provide clear, concise code examples "
        "and explanations. Always include comments in your code."
    ),
    "temperature": 0.3,  # Lower temperature for more focused responses
    "max_tokens": 1000   # More tokens for code examples
}

CREATIVE_WRITER_CONFIG = {
    "system_prompt": (
        "You are a creative writing assistant. Help users with storytelling, "
        "character development, and creative expression."
    ),
    "temperature": 0.9,  # Higher temperature for creativity
    "max_tokens": 800
}

RESEARCH_ASSISTANT_CONFIG = {
    "system_prompt": (
        "You are a research assistant. Provide well-researched, factual information "
        "with citations when possible. Be thorough and analytical."
    ),
    "temperature": 0.5,
    "max_tokens": 1200
}