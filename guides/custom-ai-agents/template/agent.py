#!/usr/bin/env python3
"""
AI Agent Template

A simple template for creating new AI agents. Customize this file
to build your own AI agent with specific capabilities.
"""

import os
import json
import logging
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from config import AgentConfig


class TemplateAgent:
    """
    Template AI Agent with basic functionality.
    
    Customize this class to add your own features:
    - Modify the system prompt
    - Add custom tools/functions
    - Implement specialized behavior
    - Add validation and error handling
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key)
        self.messages: List[Dict[str, Any]] = []
        
        # Set up logging
        self.logger = self._setup_logging()
        
        # Initialize with system prompt
        self.add_message("system", config.system_prompt)
        
        # Load previous conversation if available
        self.load_memory()
    
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
            logger.setLevel(self.config.log_level)
        return logger
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.messages.append({"role": role, "content": content})
        self._truncate_memory()
    
    def _truncate_memory(self) -> None:
        """Keep memory within configured limits."""
        if len(self.messages) > self.config.max_memory_messages:
            # Keep system message + recent history
            system_msg = self.messages[0] if self.messages[0]["role"] == "system" else None
            recent_messages = self.messages[-(self.config.max_memory_messages - 1):]
            
            if system_msg:
                self.messages = [system_msg] + recent_messages
            else:
                self.messages = recent_messages
    
    def chat(self, user_input: str) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            user_input: The user's message
            
        Returns:
            The agent's response
        """
        self.logger.info(f"User input: {user_input}")
        
        # Add user message
        self.add_message("user", user_input)
        
        try:
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=self.messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response
            self.add_message("assistant", assistant_message)
            
            # Auto-save memory
            self.save_memory()
            
            self.logger.info(f"Agent response: {assistant_message}")
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            self.logger.error(error_msg)
            return error_msg
    
    def save_memory(self) -> None:
        """Save conversation history to file."""
        try:
            with open(self.config.memory_file, 'w') as f:
                json.dump(self.messages, f, indent=2)
            self.logger.debug(f"Memory saved to {self.config.memory_file}")
        except Exception as e:
            self.logger.error(f"Failed to save memory: {e}")
    
    def load_memory(self) -> None:
        """Load conversation history from file."""
        try:
            with open(self.config.memory_file, 'r') as f:
                self.messages = json.load(f)
            self.logger.debug(f"Memory loaded from {self.config.memory_file}")
        except FileNotFoundError:
            self.logger.debug("No existing memory file found")
        except Exception as e:
            self.logger.error(f"Failed to load memory: {e}")
    
    def clear_memory(self) -> None:
        """Clear conversation history and restart with system prompt."""
        self.messages = [{"role": "system", "content": self.config.system_prompt}]
        self.save_memory()
        self.logger.info("Memory cleared")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history."""
        return self.messages.copy()


def main():
    """Main function to run the template agent."""
    
    # Load configuration
    config = AgentConfig.from_env()
    
    # Create agent
    agent = TemplateAgent(config)
    
    print("Template AI Agent")
    print("=" * 30)
    print("Type 'quit' to exit, 'clear' to clear memory, 'help' for commands")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif user_input.lower() == 'clear':
                agent.clear_memory()
                print("Memory cleared.")
                continue
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif user_input.lower() == 'history':
                history = agent.get_conversation_history()
                print("\nConversation History:")
                for i, msg in enumerate(history):
                    print(f"{i+1}. {msg['role']}: {msg['content'][:100]}...")
                continue
            
            if not user_input:
                continue
            
            response = agent.chat(user_input)
            print(f"Agent: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    """Print available commands."""
    help_text = """
Available commands:
- quit/exit/q: Exit the agent
- clear: Clear conversation memory
- history: Show conversation history
- help: Show this help message

Customize this agent by:
1. Modifying the system prompt in config.py
2. Adding custom tools and functions
3. Implementing specialized behavior
4. Adding validation and error handling
    """
    print(help_text)


if __name__ == "__main__":
    main()