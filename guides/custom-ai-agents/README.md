# Custom AI Agents Guide

This directory contains a comprehensive guide and framework for building simple, customizable AI agents.

## 📚 What's Included

### 1. [Main Guide](ai-agents-guide.md)
Comprehensive guide covering:
- Why "tiny" AI agents matter
- Setup and prerequisites
- Best practices for prompt design, memory, and evaluation
- Troubleshooting tips
- Further reading and resources

### 2. [Basic Agent](basic_agent.py)
A complete, functional AI agent in under 50 lines:
- Simple conversation loop
- Memory persistence
- Minimal dependencies (only OpenAI SDK + python-dotenv)
- Error handling

### 3. [Advanced Agent](advanced_agent/)
Modular architecture demonstrating:
- Pluggable memory backends (in-memory, file-based)
- Tool system (calculator, web search)
- Configuration management
- Logging and error handling
- Clean separation of concerns

### 4. [Template](template/)
Project scaffold for new agents:
- Template implementation
- Configuration management
- Test structure
- Setup documentation

### 5. [Demo Script](demo.py)
Showcase components without API keys:
- Calculator tool functionality
- Memory backend examples
- Configuration demonstration

## 🚀 Quick Start

### Option 1: Basic Agent (Simplest)
```bash
# 1. Install dependencies
pip install openai python-dotenv

# 2. Set up environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# 3. Run
python basic_agent.py
```

### Option 2: Advanced Agent (Full Features)
```bash
# 1. Navigate to advanced agent
cd advanced_agent/

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# 4. Run
python main.py
```

### Option 3: Use Template (For New Projects)
```bash
# 1. Copy template
cp -r template/ my_new_agent/
cd my_new_agent/

# 2. Install and configure
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings

# 3. Customize and run
python agent.py
```

## 🔧 Demo Without API Keys

To see the framework in action without requiring API keys:

```bash
python demo.py
```

This demonstrates:
- Calculator tool execution
- Memory management
- Configuration handling
- Mock web search results

## 📖 Key Concepts

### "Tiny" Philosophy
- **Simplicity**: Easy to understand and debug
- **Modularity**: Swappable components
- **Transparency**: Clear data flow
- **Rapid iteration**: Quick to modify and experiment

### Architecture Principles
- **Plugin architecture**: Tools and memory are pluggable
- **Clear interfaces**: Base classes define contracts
- **Separation of concerns**: Each module has single responsibility
- **Testability**: Components can be unit tested independently

### Best Practices Covered
- Prompt design techniques
- Memory management strategies
- Evaluation and improvement loops
- Error handling patterns
- Configuration management

## 🛠 Extending the Framework

### Adding New Tools
1. Inherit from `BaseTool`
2. Implement `execute()` method
3. Add to agent with `agent.add_tool()`

### Adding Memory Backends
1. Inherit from `BaseMemory`
2. Implement abstract methods
3. Update configuration to use new backend

### Customizing Behavior
- Modify system prompts
- Adjust temperature and token limits
- Add custom validation logic
- Implement specialized conversation flows

## 📚 References

This guide incorporates insights from:
- [Tiny React Philosophy](https://markchur.ch/posts/tiny-react/)
- [Survey on Large Language Models as Agents](https://arxiv.org/abs/2210.03629)
- [Tiny React GitHub Repository](https://github.com/mark-church/tiny-react)

## 🤝 Contributing

This is part of the AI-assigned-research-projects collection. Contributions and improvements are welcome!

## 📝 License

See the main repository license.