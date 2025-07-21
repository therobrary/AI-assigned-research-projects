#!/usr/bin/env python3
"""
Demo script to showcase AI agent components without requiring API keys.

This script demonstrates:
- Memory management
- Tool execution
- Configuration management
- Error handling

Run: python demo.py
"""

import sys
import os
import json
import tempfile

# Add paths for imports
sys.path.append('advanced_agent')
sys.path.append('template')

def demo_calculator_tool():
    """Demonstrate the calculator tool."""
    print("=== Calculator Tool Demo ===")
    
    from advanced_agent.tools.calculator import CalculatorTool
    
    calc = CalculatorTool()
    
    test_expressions = [
        "2 + 3 * 4",
        "(10 + 5) / 3",
        "2 ** 10", 
        "sqrt(16)",  # This will fail - not supported
        "15 * 23 + 7"
    ]
    
    for expr in test_expressions:
        result = calc.execute({"expression": expr})
        print(f"  {expr:15} = {result}")
    
    print()


def demo_memory_backends():
    """Demonstrate different memory backends."""
    print("=== Memory Backends Demo ===")
    
    from advanced_agent.memory.simple_memory import SimpleMemory
    from advanced_agent.memory.file_memory import FileMemory
    
    # Simple memory demo
    print("Simple Memory:")
    simple_mem = SimpleMemory(max_messages=3)
    simple_mem.add_message("system", "You are helpful")
    simple_mem.add_message("user", "Hello")
    simple_mem.add_message("assistant", "Hi there!")
    simple_mem.add_message("user", "How are you?")  # Should trigger truncation
    
    messages = simple_mem.get_messages()
    print(f"  Messages count: {len(messages)}")
    for msg in messages:
        print(f"    {msg['role']}: {msg['content'][:30]}...")
    
    # File memory demo
    print("\nFile Memory:")
    temp_file = tempfile.mktemp(suffix=".json")
    file_mem = FileMemory(temp_file, max_messages=5)
    file_mem.add_message("system", "You are helpful")
    file_mem.add_message("user", "Test message")
    
    # Create a new instance to test persistence
    file_mem2 = FileMemory(temp_file, max_messages=5)
    messages = file_mem2.get_messages()
    print(f"  Loaded {len(messages)} messages from file")
    
    # Clean up
    if os.path.exists(temp_file):
        os.unlink(temp_file)
    
    print()


def demo_configuration():
    """Demonstrate configuration management."""
    print("=== Configuration Demo ===")
    
    # Mock environment for demo
    import os
    original_env = os.environ.copy()
    
    try:
        # Set mock environment variables
        os.environ.update({
            'OPENAI_API_KEY': 'demo_key_12345',
            'OPENAI_MODEL': 'gpt-4',
            'MAX_TOKENS': '800',
            'TEMPERATURE': '0.5'
        })
        
        from advanced_agent.core.config import Config
        
        config = Config.from_env()
        print(f"  Model: {config.model}")
        print(f"  Max Tokens: {config.max_tokens}")
        print(f"  Temperature: {config.temperature}")
        print(f"  API Key: {config.openai_api_key[:10]}...")
        
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)
    
    print()


def demo_web_search_tool():
    """Demonstrate the mock web search tool."""
    print("=== Web Search Tool Demo ===")
    
    from advanced_agent.tools.web_search import WebSearchTool
    
    search = WebSearchTool()
    
    test_queries = [
        "python programming",
        "weather forecast",
        "artificial intelligence",
        ""  # Empty query
    ]
    
    for query in test_queries:
        if query:
            result = search.execute({"query": query})
            print(f"  Query: '{query}'")
            # Show first few lines of result
            lines = result.split('\n')[:4]
            for line in lines:
                print(f"    {line}")
            print("    ...")
        else:
            result = search.execute({})
            print(f"  Empty query: {result}")
        print()


def demo_template_config():
    """Demonstrate template configuration options."""
    print("=== Template Configuration Demo ===")
    
    # Mock environment for demo
    import os
    original_env = os.environ.copy()
    
    try:
        os.environ.update({
            'OPENAI_API_KEY': 'demo_key_12345',
            'SYSTEM_PROMPT': 'You are a coding assistant.',
            'MAX_MEMORY_MESSAGES': '15'
        })
        
        from template.config import AgentConfig, CODING_ASSISTANT_CONFIG
        
        config = AgentConfig.from_env()
        print(f"  System prompt: {config.system_prompt}")
        print(f"  Memory limit: {config.max_memory_messages}")
        
        print("\n  Predefined configs available:")
        print(f"    Coding Assistant: {CODING_ASSISTANT_CONFIG['temperature']}")
        
    finally:
        os.environ.clear()
        os.environ.update(original_env)
    
    print()


def main():
    """Run all demos."""
    print("AI Agents Framework Demo")
    print("=" * 50)
    print("This demo showcases the components without requiring API keys.\n")
    
    try:
        demo_calculator_tool()
        demo_memory_backends()
        demo_configuration()
        demo_web_search_tool()
        demo_template_config()
        
        print("=== Demo Complete ===")
        print("All components working correctly!")
        print("\nTo use with real API calls:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key")
        print("3. Run python basic_agent.py or python advanced_agent/main.py")
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running from the guides/custom-ai-agents directory")
    except Exception as e:
        print(f"Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()