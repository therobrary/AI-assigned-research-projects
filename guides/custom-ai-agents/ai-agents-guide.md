# Building Simple, Customizable AI Agents: A Practical Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Why "Tiny" AI Agents Matter](#why-tiny-ai-agents-matter)
3. [Prerequisites and Setup](#prerequisites-and-setup)
4. [Basic Agent Example](#basic-agent-example)
5. [Best Practices](#best-practices)
   - [Prompt Design](#prompt-design)
   - [Memory Handling](#memory-handling)
   - [Evaluation Loops](#evaluation-loops)
6. [Advanced Agent Architecture](#advanced-agent-architecture)
7. [Reusable Framework and Template](#reusable-framework-and-template)
8. [Troubleshooting](#troubleshooting)
9. [Further Reading](#further-reading)

## Introduction

AI agents are autonomous systems that can perceive their environment, make decisions, and take actions to achieve specific goals. This guide teaches you how to build simple, customizable AI agents that are lightweight, maintainable, and extensible.

Drawing inspiration from the ["Tiny React" philosophy](https://markchur.ch/posts/tiny-react/), we focus on creating minimal viable agents that do one thing well, rather than complex frameworks that try to solve every problem. As highlighted in the comprehensive survey ["A Survey on Large Language Models as Agents"](https://arxiv.org/abs/2210.03629), effective agent design often comes down to clear interfaces, focused responsibilities, and iterative improvement.

## Why "Tiny" AI Agents Matter

The "tiny" philosophy for AI agents emphasizes:

- **Simplicity**: Easier to understand, debug, and maintain
- **Modularity**: Components can be swapped, tested, and improved independently  
- **Transparency**: Clear data flow and decision paths
- **Rapid iteration**: Quick to modify and experiment with
- **Cost efficiency**: Lower token usage and computational overhead
- **Debugging**: Easier to trace issues and understand behavior

Small, focused agents often outperform complex systems because they:
- Have fewer failure points
- Are easier to optimize for specific tasks
- Can be composed together for complex workflows
- Allow for precise testing and validation

## Prerequisites and Setup

### Requirements

- Python 3.8+
- OpenAI API key (or compatible LLM API)
- Basic understanding of Python and API calls

### Installation

```bash
pip install openai python-dotenv
```

### Environment Setup

Create a `.env` file in your project directory:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo  # or gpt-4, etc.
```

## Basic Agent Example

Here's a complete, functional AI agent in under 50 lines of code (see [`basic_agent.py`](basic_agent.py)):

```python
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

class SimpleAgent:
    def __init__(self, system_prompt="You are a helpful AI assistant."):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.messages = [{"role": "system", "content": system_prompt}]
    
    def chat(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": assistant_message})
            return assistant_message
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def save_memory(self, filename="memory.json"):
        with open(filename, 'w') as f:
            json.dump(self.messages, f, indent=2)
    
    def load_memory(self, filename="memory.json"):
        try:
            with open(filename, 'r') as f:
                self.messages = json.load(f)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    agent = SimpleAgent("You are a helpful coding assistant.")
    agent.load_memory()
    
    print("Simple AI Agent (type 'quit' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            agent.save_memory()
            break
        
        response = agent.chat(user_input)
        print(f"Agent: {response}")
```

This basic agent demonstrates:
- Simple conversation loop
- Memory persistence across interactions
- Clean separation of concerns
- Error handling
- Configurable behavior

Key features:
- **Single file**: Easy to understand and modify
- **Minimal dependencies**: Only OpenAI SDK and python-dotenv
- **Memory**: Maintains conversation context
- **Configurable**: Easy to adjust prompts and behavior

## Best Practices

### Prompt Design

**1. Be Specific and Clear**
```python
# Good
prompt = "You are a helpful coding assistant. Respond with concise, accurate code examples."

# Avoid
prompt = "You are helpful."
```

**2. Use System Messages Effectively**
```python
system_message = {
    "role": "system", 
    "content": "You are a task-focused agent. Always respond in this format: THOUGHT: [reasoning] ACTION: [what you'll do]"
}
```

**3. Provide Examples (Few-shot Learning)**
```python
examples = [
    {"role": "user", "content": "Calculate 2+2"},
    {"role": "assistant", "content": "THOUGHT: Simple arithmetic calculation. ACTION: 2 + 2 = 4"}
]
```

### Memory Handling

**1. Bounded Memory**
```python
def maintain_memory(messages, max_messages=10):
    """Keep only recent messages to avoid token limits"""
    if len(messages) > max_messages:
        # Keep system message + recent history
        return [messages[0]] + messages[-(max_messages-1):]
    return messages
```

**2. Semantic Memory**
```python
def summarize_old_context(messages):
    """Compress old messages into summary"""
    # Implementation would summarize and compress older messages
    pass
```

**3. External Memory**
```python
def save_memory_to_file(messages, filename="agent_memory.json"):
    """Persist memory between sessions"""
    import json
    with open(filename, 'w') as f:
        json.dump(messages, f)
```

### Evaluation Loops

**1. Simple Success Metrics**
```python
def evaluate_response(response, expected_format=None):
    """Basic response validation"""
    if expected_format == "json":
        try:
            json.loads(response)
            return True
        except:
            return False
    return len(response.strip()) > 0
```

**2. Iterative Improvement**
```python
def self_correct(agent, initial_response, max_attempts=3):
    """Allow agent to refine its response"""
    for attempt in range(max_attempts):
        if evaluate_response(initial_response):
            return initial_response
        
        correction_prompt = f"Your previous response '{initial_response}' was not in the expected format. Please correct it."
        initial_response = agent.generate_response(correction_prompt)
    
    return initial_response
```

## Advanced Agent Architecture

For more complex use cases, we provide a modular architecture in the [`advanced_agent/`](advanced_agent/) folder:

```
advanced_agent/
├── core/
│   ├── __init__.py
│   ├── agent.py          # Main agent class
│   └── config.py         # Configuration management
├── tools/
│   ├── __init__.py
│   ├── base_tool.py      # Tool interface
│   ├── web_search.py     # Example web search tool
│   └── calculator.py     # Example calculator tool
├── memory/
│   ├── __init__.py
│   ├── base_memory.py    # Memory interface
│   ├── simple_memory.py  # In-memory storage
│   └── file_memory.py    # File-based persistence
└── main.py               # Example usage
```

Key architectural principles:
- **Plugin architecture**: Tools and memory backends are pluggable
- **Clear interfaces**: Base classes define contracts
- **Separation of concerns**: Each module has a single responsibility
- **Testability**: Components can be unit tested independently

See the [advanced agent example](advanced_agent/main.py) for a complete implementation.

## Reusable Framework and Template

The [`template/`](template/) folder provides a starting point for new agent projects:

```
template/
├── agent.py              # Basic agent implementation
├── config.py             # Configuration template
├── requirements.txt      # Dependencies
├── .env.example          # Environment variables template
├── README.md             # Setup and usage instructions
└── tests/
    └── test_agent.py     # Basic test structure
```

To use the template:

1. Copy the template folder to your new project
2. Rename `.env.example` to `.env` and add your API keys
3. Install dependencies: `pip install -r requirements.txt`
4. Customize `agent.py` for your specific use case
5. Run tests: `python -m pytest tests/`

## Troubleshooting

### Common Issues

**1. API Rate Limits**
```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(60/calls_per_minute)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

**2. Token Limits**
- Use shorter prompts and responses
- Implement memory truncation
- Summarize old conversation history

**3. Inconsistent Responses**
- Add response format validation
- Use structured outputs (JSON mode if available)
- Implement retry logic with corrections

**4. Context Loss**
- Persist conversation history
- Use external memory systems
- Implement context summarization

### Debugging Tips

1. **Log everything**: Add comprehensive logging to trace agent decisions
2. **Start simple**: Begin with the basic agent and add complexity gradually
3. **Test incrementally**: Validate each component before integration
4. **Use mock responses**: Test your logic without API calls during development

## Further Reading

### Essential Resources

1. **["Tiny React" Blog Post](https://markchur.ch/posts/tiny-react/)** - Philosophy behind minimal, focused design
2. **[Research Paper: "A Survey on Large Language Models as Agents"](https://arxiv.org/abs/2210.03629)** - Comprehensive overview of agent architectures
3. **[Tiny React GitHub Repository](https://github.com/mark-church/tiny-react)** - Reference implementation

### Additional Learning

- **LangChain Documentation** - For more complex agent frameworks
- **OpenAI Cookbook** - Practical examples and best practices
- **Anthropic's Constitutional AI** - Techniques for safer, more reliable agents
- **ReAct Paper** - Reasoning and Acting with Language Models
- **AutoGPT and Similar Projects** - Examples of autonomous agent implementations

### Community Resources

- **Reddit r/MachineLearning** - Discussion on latest agent techniques
- **AI Agent Discord Communities** - Real-time help and collaboration
- **GitHub Awesome Lists** - Curated collections of agent resources

---

*This guide is part of the AI-assigned-research-projects collection. Contributions and improvements are welcome!*