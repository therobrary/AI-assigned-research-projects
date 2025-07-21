#!/usr/bin/env python3
"""
Advanced AI Agent Example

This example demonstrates a modular AI agent architecture with:
- Pluggable memory backends
- Tool/function calling capabilities
- Configurable behavior
- Logging and error handling
"""

import logging
from core.config import Config
from core.agent import AdvancedAgent
from tools.calculator import CalculatorTool
from tools.web_search import WebSearchTool


def main():
    """Main function to demonstrate the advanced agent."""
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("Advanced AI Agent Example")
    print("=" * 40)
    
    try:
        # Load configuration from environment
        config = Config.from_env()
        print(f"Using model: {config.model}")
        print(f"Memory backend: {config.memory_backend}")
        print(f"Tools enabled: {config.enable_tools}")
        
        # Create agent
        agent = AdvancedAgent(config)
        
        # Add tools if enabled
        if config.enable_tools:
            agent.add_tool(CalculatorTool())
            agent.add_tool(WebSearchTool())
            print("Tools added: calculator, web_search")
        
        print("\nAgent ready! Type 'quit' to exit, 'clear' to clear memory.")
        print("Try asking: 'Calculate 2 + 3 * 4' or 'Search for Python tutorials'")
        print("-" * 40)
        
        # Main conversation loop
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                agent.save_state()
                print("Goodbye! Agent state saved.")
                break
            elif user_input.lower() == 'clear':
                agent.clear_memory()
                print("Memory cleared.")
                continue
            elif user_input.lower() == 'history':
                history = agent.get_conversation_history()
                print("\nConversation History:")
                for i, msg in enumerate(history):
                    print(f"{i+1}. {msg['role']}: {msg['content'][:100]}...")
                continue
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            if not user_input:
                continue
            
            # Get response from agent
            response = agent.chat(user_input)
            print(f"Agent: {response}")
    
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure OPENAI_API_KEY is set.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def print_help():
    """Print help information."""
    help_text = """
Available commands:
- quit/exit/q: Exit the agent
- clear: Clear conversation memory
- history: Show conversation history
- help: Show this help message

For tool usage:
- Calculator: "Calculate 2 + 3 * 4" or "What is 15 * 23?"
- Web Search: "Search for Python tutorials" or "Find information about AI"

The agent will attempt to use tools when appropriate based on your requests.
    """
    print(help_text)


if __name__ == "__main__":
    main()