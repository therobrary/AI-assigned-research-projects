# Building Custom Tools for OpenWebUI

## Table of Contents
1. [Introduction](#introduction)
2. [Understanding OpenWebUI Plugin Architecture](#understanding-openwebui-plugin-architecture)
3. [Tool Anatomy](#tool-anatomy)
4. [Hello World Tool Walkthrough](#hello-world-tool-walkthrough)
5. [Best Practices](#best-practices)
6. [Advanced Topics](#advanced-topics)
7. [Examples](#examples)
8. [Template Usage](#template-usage)
9. [FAQ & Troubleshooting](#faq--troubleshooting)
10. [Resources](#resources)

## Introduction

OpenWebUI supports custom tools (also known as action plugins) that extend the platform's capabilities. These tools allow you to integrate external APIs, perform complex operations, and create interactive experiences for users. This guide provides a comprehensive walkthrough of building, testing, and distributing custom tools for OpenWebUI.

## Understanding OpenWebUI Plugin Architecture

OpenWebUI's plugin system is built on a simple yet powerful architecture:

- **Tools** are Python scripts that define specific actions
- **Actions** are functions within tools that can be called by the AI or users
- **Metadata** describes the tool's capabilities, requirements, and interface
- **Frontend Integration** allows tools to interact with the OpenWebUI interface

### Core Components

1. **Tool Definition**: A Python class that inherits from the base tool class
2. **Action Methods**: Functions decorated with `@action` that define what the tool can do
3. **Metadata**: JSON/YAML configuration describing the tool's properties
4. **Dependencies**: Required packages and API keys

## Tool Anatomy

### Basic Structure

```python
"""
title: Tool Name
author: Your Name
author_url: https://your-website.com
funding_url: https://github.com/sponsors/yourusername
version: 0.1.0
license: MIT
"""

from typing import Callable, Any
import requests

class Tools:
    def __init__(self):
        self.name = "tool_name"
        self.description = "Brief description of what this tool does"
        
    def action_name(
        self,
        param1: str,
        param2: int = 10,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Description of what this action does.
        
        :param param1: Description of parameter 1
        :param param2: Description of parameter 2 (optional)
        :return: Description of return value
        """
        # Your implementation here
        return "Result"
```

### Metadata Fields

- **title**: Display name of the tool
- **author**: Tool creator's name
- **author_url**: Link to author's profile or website
- **funding_url**: Link for supporting the author
- **version**: Semantic version number
- **license**: License type (MIT, Apache 2.0, etc.)

### Special Parameters

- **__user__**: Contains user information and session data
- **__event_emitter__**: Allows real-time communication with the frontend

## Hello World Tool Walkthrough

Let's create a simple "Hello World" tool step by step:

### Step 1: Create the Tool File

Create a file named `hello_world.py`:

```python
"""
title: Hello World Tool
author: OpenWebUI Community
author_url: https://github.com/open-webui/open-webui
version: 1.0.0
license: MIT
"""

from typing import Callable, Any

class Tools:
    def __init__(self):
        self.name = "hello_world"
        self.description = "A simple greeting tool that demonstrates basic OpenWebUI tool functionality"

    def greet(
        self,
        name: str = "World",
        language: str = "en",
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Generate a greeting message in different languages.
        
        :param name: Name to greet (default: "World")
        :param language: Language code (en, es, fr, de) (default: "en")
        :return: Greeting message
        """
        greetings = {
            "en": f"Hello, {name}!",
            "es": f"¡Hola, {name}!",
            "fr": f"Bonjour, {name}!",
            "de": f"Hallo, {name}!",
        }
        
        greeting = greetings.get(language, greetings["en"])
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": f"Generated greeting for {name}", "done": True},
            })
        
        return greeting
```

### Step 2: Install the Tool

1. Copy the tool file to your OpenWebUI tools directory
2. Restart OpenWebUI or refresh the tools list
3. The tool should appear in the available tools list

### Step 3: Test the Tool

You can now use the tool in conversations:
- Type: "Greet me in Spanish"
- The AI will use the `greet` action with appropriate parameters

## Best Practices

### Naming Conventions

- **Tool files**: Use snake_case (e.g., `weather_tool.py`)
- **Class name**: Always use `Tools`
- **Action methods**: Use descriptive snake_case names
- **Parameters**: Use clear, descriptive names

### Error Handling

```python
def api_call(self, endpoint: str) -> dict:
    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API call failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def process_data(self, data: str) -> str:
    logger.info(f"Processing data: {data[:50]}...")
    # Processing logic
    logger.info("Data processing completed")
    return result
```

### Event Emission

Use event emitters to provide real-time feedback:

```python
def long_running_task(
    self,
    data: str,
    __event_emitter__: Callable[[dict], Any] = None,
) -> str:
    if __event_emitter__:
        __event_emitter__({
            "type": "status",
            "data": {"description": "Starting processing...", "done": False},
        })
    
    # Do work...
    
    if __event_emitter__:
        __event_emitter__({
            "type": "status",
            "data": {"description": "Processing complete", "done": True},
        })
    
    return result
```

### Security Considerations

1. **API Key Management**: Use environment variables
2. **Input Validation**: Always validate and sanitize inputs
3. **Rate Limiting**: Implement rate limiting for external APIs
4. **User Permissions**: Check user permissions when necessary

```python
import os
from typing import Optional

def validate_api_key(self) -> Optional[str]:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise ValueError("WEATHER_API_KEY environment variable not set")
    return api_key

def validate_input(self, city: str) -> str:
    if not city or len(city.strip()) == 0:
        raise ValueError("City name cannot be empty")
    if len(city) > 100:
        raise ValueError("City name too long")
    return city.strip()
```

### Internationalization (i18n)

Support multiple languages in your tools:

```python
def get_message(self, key: str, language: str = "en") -> str:
    messages = {
        "en": {
            "error_invalid_input": "Invalid input provided",
            "success_completed": "Operation completed successfully"
        },
        "es": {
            "error_invalid_input": "Entrada inválida proporcionada",
            "success_completed": "Operación completada exitosamente"
        }
    }
    return messages.get(language, messages["en"]).get(key, key)
```

### UX Guidelines

1. **Clear Descriptions**: Provide helpful docstrings and parameter descriptions
2. **Sensible Defaults**: Use reasonable default values for optional parameters
3. **Progress Feedback**: Use event emitters for long-running operations
4. **Error Messages**: Provide clear, actionable error messages

## Advanced Topics

### Stateful Tools

Some tools need to maintain state between calls:

```python
class Tools:
    def __init__(self):
        self.name = "stateful_tool"
        self.description = "Tool that maintains state between calls"
        self.session_data = {}
    
    def store_value(
        self,
        key: str,
        value: str,
        __user__: dict = None,
    ) -> str:
        user_id = __user__.get("id", "anonymous") if __user__ else "anonymous"
        if user_id not in self.session_data:
            self.session_data[user_id] = {}
        
        self.session_data[user_id][key] = value
        return f"Stored {key} = {value}"
    
    def get_value(
        self,
        key: str,
        __user__: dict = None,
    ) -> str:
        user_id = __user__.get("id", "anonymous") if __user__ else "anonymous"
        user_data = self.session_data.get(user_id, {})
        return user_data.get(key, "Key not found")
```

### External API Integration

Best practices for API integration:

```python
import requests
from typing import Dict, Any
import time
from functools import wraps

def rate_limit(calls_per_second: float = 1.0):
    """Decorator to rate limit API calls"""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

class Tools:
    def __init__(self):
        self.name = "api_tool"
        self.base_url = "https://api.example.com"
        self.session = requests.Session()
        # Set common headers
        self.session.headers.update({
            "User-Agent": "OpenWebUI-Tool/1.0",
            "Accept": "application/json"
        })
    
    @rate_limit(calls_per_second=0.5)  # Maximum 1 call every 2 seconds
    def call_api(
        self,
        endpoint: str,
        params: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Make a rate-limited API call"""
        try:
            response = self.session.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
```

### Async Operations

For CPU-intensive or I/O-bound operations:

```python
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

class Tools:
    def __init__(self):
        self.name = "async_tool"
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def cpu_intensive_task(
        self,
        data: str,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """Handle CPU-intensive work in a separate thread"""
        def heavy_computation(data):
            # Simulate heavy work
            import time
            time.sleep(2)
            return f"Processed: {data}"
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": "Starting heavy computation...", "done": False},
            })
        
        # Run in thread pool to avoid blocking
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(heavy_computation, data)
            result = future.result()
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": "Computation complete", "done": True},
            })
        
        return result
```

## Examples

This guide includes three practical examples in the `examples/` directory:

### 1. Hello World Tool (`examples/hello_world_tool/`)
A minimal example demonstrating basic tool structure and functionality.

### 2. Web Search Tool (`examples/web_search/`)
An advanced example that showcases:
- Integration with SearxNG search API
- Document processing with Docling
- Complex data transformation
- Error handling and fallbacks

### 3. Weather Tool (`examples/weather_tool/`)
A practical example featuring:
- OpenWeatherMap API integration
- Environment variable configuration
- Data formatting and presentation
- Error handling for network issues

## Template Usage

The `template/` directory contains a boilerplate tool structure that you can use to quickly scaffold new tools:

1. Copy the template directory
2. Rename files and update metadata
3. Implement your specific functionality
4. Test and deploy

## FAQ & Troubleshooting

### Common Issues

**Q: My tool doesn't appear in the tools list**
A: Check the following:
- Ensure the file is in the correct tools directory
- Verify the Python syntax is correct
- Check that the class is named `Tools`
- Restart OpenWebUI after adding the tool

**Q: Tool actions aren't being called**
A: Verify:
- Action methods are properly defined in the `Tools` class
- Method signatures include required parameters
- No syntax errors in the tool file

**Q: API calls are failing**
A: Common causes:
- Missing or incorrect API keys
- Network connectivity issues
- Rate limiting by the external service
- Incorrect endpoint URLs

**Q: Tool is slow or unresponsive**
A: Consider:
- Adding timeout parameters to network requests
- Using async operations for heavy tasks
- Implementing proper error handling
- Adding progress indicators with event emitters

### Debugging Tips

1. **Use logging**: Add logging statements to track execution flow
2. **Test independently**: Test your tool functions outside of OpenWebUI first
3. **Check logs**: Review OpenWebUI logs for error messages
4. **Start simple**: Begin with a minimal working version and add features incrementally

### Performance Optimization

1. **Cache responses**: Cache API responses when appropriate
2. **Connection pooling**: Reuse HTTP connections for multiple requests
3. **Lazy loading**: Load heavy resources only when needed
4. **Background processing**: Use threads or async for long-running tasks

## Resources

### Official Documentation
- [OpenWebUI Tools Documentation](https://docs.openwebui.com/features/plugin/tools/)
- [OpenWebUI Plugin Guide](https://docs.openwebui.com/features/plugin/)

### Community Resources
- [OpenWebUI Tool Skeleton](https://github.com/pahautelman/open-webui-tool-skeleton)
- [Building Action Tools Tutorial](https://pahautelman.github.io/pahautelman-blog/tutorials/open-webui-action-tools/open-webui-action-tools/)
- [OpenWebUI GitHub Repository](https://github.com/open-webui/open-webui)

### API References
- [OpenWeatherMap API](https://openweathermap.org/api/one-call-3)
- [SearxNG API Documentation](https://docs.searxng.org/)

### Development Tools
- [Requests Library](https://docs.python-requests.org/)
- [aiohttp for Async HTTP](https://docs.aiohttp.org/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

---

*This guide is part of the AI-assigned-research-projects repository. Contributions and improvements are welcome!*