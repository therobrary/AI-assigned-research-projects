# Advanced AI Agent

This folder contains a modular AI agent architecture that demonstrates best practices for building extensible AI systems.

## Architecture

```
advanced_agent/
├── core/
│   ├── agent.py          # Main agent class
│   └── config.py         # Configuration management
├── tools/
│   ├── base_tool.py      # Tool interface
│   ├── calculator.py     # Calculator tool
│   └── web_search.py     # Web search tool (mock)
├── memory/
│   ├── base_memory.py    # Memory interface
│   ├── simple_memory.py  # In-memory storage
│   └── file_memory.py    # File-based persistence
├── main.py               # Example usage
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## Features

- **Modular Design**: Pluggable memory backends and tools
- **Configuration Management**: Environment-based configuration
- **Memory Management**: Automatic context window management
- **Tool Integration**: Extensible tool system for external capabilities
- **Error Handling**: Comprehensive error handling and logging
- **Persistence**: Optional state persistence between sessions

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your configuration:
   ```bash
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   MEMORY_BACKEND=file
   ENABLE_TOOLS=true
   ```

3. Run the agent:
   ```bash
   python main.py
   ```

## Usage Examples

### Basic Conversation
```
You: Hello, how are you?
Agent: Hello! I'm doing well, thank you for asking. How can I assist you today?
```

### Calculator Tool
```
You: Calculate 15 * 23 + 7
Agent: TOOL: calculator
Tool Result: 352
The result of 15 * 23 + 7 is 352.
```

### Web Search Tool
```
You: Search for Python tutorials
Agent: TOOL: web_search
Tool Result: [Mock search results for Python tutorials]
```

## Extending the Agent

### Adding New Tools

1. Create a new tool class inheriting from `BaseTool`:
   ```python
   from tools.base_tool import BaseTool
   
   class MyTool(BaseTool):
       def __init__(self):
           super().__init__("my_tool", "Description of my tool")
       
       def execute(self, parameters):
           # Implementation here
           return "Tool result"
   ```

2. Add the tool to your agent:
   ```python
   agent.add_tool(MyTool())
   ```

### Adding New Memory Backends

1. Create a new memory class inheriting from `BaseMemory`:
   ```python
   from memory.base_memory import BaseMemory
   
   class MyMemory(BaseMemory):
       def add_message(self, role, content):
           # Implementation here
           pass
       
       # Implement other abstract methods...
   ```

2. Update the configuration to use your memory backend.

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Model to use |
| `MAX_TOKENS` | `500` | Maximum tokens per response |
| `TEMPERATURE` | `0.7` | Response creativity (0-1) |
| `SYSTEM_PROMPT` | Default | System prompt for the agent |
| `MAX_MEMORY_MESSAGES` | `20` | Maximum messages to keep in memory |
| `ENABLE_TOOLS` | `true` | Whether to enable tool usage |
| `MEMORY_BACKEND` | `simple` | Memory backend (`simple` or `file`) |
| `MEMORY_FILE` | `agent_memory.json` | File for persistent memory |

## Best Practices

1. **Keep tools focused**: Each tool should do one thing well
2. **Handle errors gracefully**: Always include error handling in tools
3. **Validate inputs**: Check tool parameters before execution
4. **Log important events**: Use logging for debugging and monitoring
5. **Manage memory**: Implement proper context window management
6. **Test components**: Unit test tools and memory backends independently

## Troubleshooting

- **ImportError**: Make sure all dependencies are installed
- **API Errors**: Check your OpenAI API key and internet connection
- **Memory Issues**: Monitor token usage and adjust max_memory_messages
- **Tool Failures**: Check tool parameters and error messages