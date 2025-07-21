"""Advanced AI Agent with modular architecture."""

import json
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI

from .config import Config
from ..memory.base_memory import BaseMemory
from ..memory.simple_memory import SimpleMemory
from ..memory.file_memory import FileMemory
from ..tools.base_tool import BaseTool


class AdvancedAgent:
    """
    Advanced AI Agent with pluggable memory and tools.
    
    This agent supports:
    - Multiple memory backends
    - Tool/function calling
    - Configurable behavior
    - Logging and debugging
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.logger = self._setup_logging()
        
        # Initialize memory backend
        self.memory = self._create_memory_backend()
        
        # Initialize tools
        self.tools: Dict[str, BaseTool] = {}
        
        # Initialize conversation with system prompt
        if not self.memory.get_messages():
            self.memory.add_message("system", config.system_prompt)
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the agent."""
        logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _create_memory_backend(self) -> BaseMemory:
        """Create the appropriate memory backend based on configuration."""
        if self.config.memory_backend == "file":
            return FileMemory(self.config.memory_file, self.config.max_memory_messages)
        elif self.config.memory_backend == "simple":
            return SimpleMemory(self.config.max_memory_messages)
        else:
            raise ValueError(f"Unknown memory backend: {self.config.memory_backend}")
    
    def add_tool(self, tool: BaseTool) -> None:
        """Add a tool to the agent."""
        self.tools[tool.name] = tool
        self.logger.info(f"Added tool: {tool.name}")
    
    def remove_tool(self, tool_name: str) -> None:
        """Remove a tool from the agent."""
        if tool_name in self.tools:
            del self.tools[tool_name]
            self.logger.info(f"Removed tool: {tool_name}")
    
    def chat(self, user_input: str) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            user_input: The user's message
            
        Returns:
            The agent's response
        """
        self.logger.info(f"User input: {user_input}")
        
        # Add user message to memory
        self.memory.add_message("user", user_input)
        
        try:
            # Get response from OpenAI
            messages = self.memory.get_messages()
            
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            assistant_message = response.choices[0].message.content
            
            # Process tool calls if enabled
            if self.config.enable_tools and self._requires_tool_call(assistant_message):
                assistant_message = self._process_tool_calls(assistant_message)
            
            # Add assistant response to memory
            self.memory.add_message("assistant", assistant_message)
            
            self.logger.info(f"Agent response: {assistant_message}")
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def _requires_tool_call(self, message: str) -> bool:
        """Check if the message indicates a tool should be called."""
        # Simple heuristic - could be made more sophisticated
        tool_indicators = ["TOOL:", "CALL:", "EXECUTE:", "USE_TOOL:"]
        return any(indicator in message.upper() for indicator in tool_indicators)
    
    def _process_tool_calls(self, message: str) -> str:
        """Process any tool calls in the message."""
        # This is a simplified implementation
        # In a real system, you'd parse the tool calls more carefully
        for tool_name, tool in self.tools.items():
            if tool_name.upper() in message.upper():
                try:
                    # Extract parameters (simplified)
                    result = tool.execute({})
                    return f"{message}\n\nTool Result: {result}"
                except Exception as e:
                    self.logger.error(f"Tool {tool_name} failed: {e}")
                    return f"{message}\n\nTool Error: {str(e)}"
        
        return message
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history."""
        return self.memory.get_messages()
    
    def clear_memory(self) -> None:
        """Clear the conversation memory."""
        self.memory.clear()
        # Re-add system prompt
        self.memory.add_message("system", self.config.system_prompt)
        self.logger.info("Memory cleared")
    
    def save_state(self) -> None:
        """Save the agent's current state."""
        self.memory.save()
        self.logger.info("Agent state saved")
    
    def load_state(self) -> None:
        """Load the agent's previous state."""
        self.memory.load()
        self.logger.info("Agent state loaded")