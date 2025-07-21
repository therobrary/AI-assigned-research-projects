# AI Agent Template

## Quick Start

1. **Copy this template to your project:**
   ```bash
   cp -r template/ my_agent/
   cd my_agent/
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run your agent:**
   ```bash
   python agent.py
   ```

## Customization

### Basic Customization

Edit the configuration in `.env`:

```bash
# Required
OPENAI_API_KEY=your_api_key_here

# Optional customizations
OPENAI_MODEL=gpt-3.5-turbo
SYSTEM_PROMPT=You are a helpful AI assistant specialized in [YOUR DOMAIN].
MAX_TOKENS=500
TEMPERATURE=0.7
MAX_MEMORY_MESSAGES=20
```

### Advanced Customization

#### 1. Custom System Prompts

Create specialized agents by modifying the system prompt:

```python
# In config.py, use predefined configs or create your own
from config import CODING_ASSISTANT_CONFIG, CREATIVE_WRITER_CONFIG

# Or define custom configuration
CUSTOM_CONFIG = {
    "system_prompt": "You are a [SPECIALIZED] assistant that...",
    "temperature": 0.5,
    "max_tokens": 800
}
```

#### 2. Add Custom Tools

Extend your agent with custom capabilities:

```python
# In agent.py, add methods for custom functionality
class TemplateAgent:
    def custom_function(self, input_data):
        """Add your custom logic here."""
        # Process input
        result = self.process_data(input_data)
        return result
    
    def chat(self, user_input: str) -> str:
        # Add custom preprocessing
        if self.should_use_custom_function(user_input):
            return self.custom_function(user_input)
        
        # Default chat behavior
        return super().chat(user_input)
```

#### 3. Integrate External APIs

Add external service integration:

```python
import requests

class TemplateAgent:
    def search_web(self, query: str) -> str:
        """Integrate with web search API."""
        # Replace with actual API
        response = requests.get(f"https://api.example.com/search?q={query}")
        return response.json()
```

## File Structure

```
template/
├── agent.py              # Main agent implementation
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── tests/
    └── test_agent.py     # Basic tests
```

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *Required* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | Model to use |
| `SYSTEM_PROMPT` | Default assistant | System prompt for agent behavior |
| `MAX_TOKENS` | `500` | Maximum tokens per response |
| `TEMPERATURE` | `0.7` | Response creativity (0-1) |
| `MAX_MEMORY_MESSAGES` | `20` | Messages to keep in memory |
| `MEMORY_FILE` | `agent_memory.json` | File for conversation persistence |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Example Use Cases

### 1. Coding Assistant
```bash
SYSTEM_PROMPT="You are a helpful coding assistant. Provide clear, concise code examples with comments."
TEMPERATURE=0.3
MAX_TOKENS=1000
```

### 2. Creative Writer
```bash
SYSTEM_PROMPT="You are a creative writing assistant. Help with storytelling and character development."
TEMPERATURE=0.9
MAX_TOKENS=800
```

### 3. Research Assistant
```bash
SYSTEM_PROMPT="You are a research assistant. Provide well-researched, factual information."
TEMPERATURE=0.5
MAX_TOKENS=1200
```

## Testing

Run the included tests:

```bash
python -m pytest tests/ -v
```

## Troubleshooting

**Common Issues:**

1. **API Key Error**: Make sure your `.env` file has a valid `OPENAI_API_KEY`
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Permission Issues**: Check file permissions for `agent_memory.json`

**Getting Help:**

- Check the logs for detailed error messages
- Adjust `LOG_LEVEL=DEBUG` in your `.env` for more verbose output
- Refer to the main guide: `../ai-agents-guide.md`

## Next Steps

1. **Experiment**: Try different system prompts and configurations
2. **Extend**: Add custom tools and integrations
3. **Deploy**: Package your agent for production use
4. **Share**: Contribute improvements back to the template

---

*This template is part of the AI-assigned-research-projects collection.*