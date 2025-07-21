# Building Custom Tools for OpenWebUI: Complete Guide

## Table of Contents

1. [Introduction](#introduction)
2. [OpenWebUI Plugin Architecture Overview](#openwebui-plugin-architecture-overview)
3. [Tool Anatomy](#tool-anatomy)
4. [Hello World Tool Walk-through](#hello-world-tool-walk-through)
5. [Best Practices](#best-practices)
6. [Advanced Topics](#advanced-topics)
7. [FAQ & Troubleshooting](#faq--troubleshooting)
8. [Resources](#resources)

## Introduction

OpenWebUI tools (also known as action plugins) are Python-based extensions that enable you to add custom functionality to your OpenWebUI instance. These tools can perform various tasks such as web searches, API calls, data processing, and integrations with external services.

This guide provides comprehensive documentation on how to build, test, and distribute custom tools for OpenWebUI, complete with working examples and best practices.

### What You'll Learn

- Understanding the OpenWebUI plugin architecture
- Building your first custom tool
- Implementing advanced features like external API integrations
- Following best practices for tool development
- Troubleshooting common issues

## OpenWebUI Plugin Architecture Overview

OpenWebUI uses a modular plugin system where tools are Python scripts that follow a specific structure and API. The architecture consists of several key components:

### Core Components

1. **Tool Definition**: Python files that define the tool's functionality
2. **Metadata**: Information about the tool (name, description, version, etc.)
3. **Actions**: The actual functions that execute when the tool is called
4. **Frontend Integration**: How the tool appears and behaves in the UI
5. **Permissions**: Security and access control for the tool

### Tool Lifecycle

```
User Input → OpenWebUI → Tool Validation → Tool Execution → Response Processing → User Output
```

### Directory Structure

Tools in OpenWebUI follow this typical structure:

```
your_tool/
├── __init__.py
├── main.py           # Main tool implementation
├── requirements.txt  # Python dependencies (optional)
└── README.md        # Documentation (optional)
```

## Tool Anatomy

Every OpenWebUI tool must implement specific components to function properly:

### 1. Metadata

Tools must define metadata using a specific format:

```python
"""
title: Your Tool Name
author: Your Name
author_url: https://github.com/yourusername
funding_url: https://github.com/sponsors/yourusername
version: 1.0.0
"""
```

### 2. Tool Class

The main tool functionality is implemented in a class that inherits from the base `Tools` class:

```python
from typing import Callable, Any
import asyncio

class Tools:
    def __init__(self):
        self.citation = True  # Enable citation if needed
        
    async def your_function_name(
        self,
        prompt: str,
        __user__: dict,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Your tool's main function
        
        :param prompt: The user's input prompt
        :param __user__: User information (id, name, role, etc.)
        :param __event_emitter__: Function to emit real-time updates
        :return: The tool's response
        """
        # Your implementation here
        pass
```

### 3. Function Signatures

OpenWebUI tools support several function signature patterns:

#### Basic Function
```python
async def basic_function(self, prompt: str, __user__: dict) -> str:
    return f"Processed: {prompt}"
```

#### Function with Event Emitter
```python
async def function_with_events(
    self, 
    prompt: str, 
    __user__: dict, 
    __event_emitter__: Callable[[dict], Any] = None
) -> str:
    if __event_emitter__:
        await __event_emitter__({"type": "status", "data": {"description": "Processing..."}})
    
    # Do work
    result = process_data(prompt)
    
    if __event_emitter__:
        await __event_emitter__({"type": "status", "data": {"description": "Complete!"}})
    
    return result
```

#### Function with Multiple Parameters
```python
async def function_with_params(
    self,
    query: str,
    max_results: int = 10,
    __user__: dict = None,
    __event_emitter__: Callable[[dict], Any] = None,
) -> str:
    # Implementation
    pass
```

### 4. Frontend Integration

Tools automatically appear in the OpenWebUI interface. You can control how they're presented:

- **Function Name**: Becomes the tool name in the UI
- **Docstring**: Provides description and parameter information
- **Type Hints**: Help the UI understand parameter types

### 5. Permissions and Security

OpenWebUI provides user information through the `__user__` parameter:

```python
def check_permissions(self, __user__: dict) -> bool:
    """Check if user has required permissions"""
    user_role = __user__.get("role", "user")
    return user_role in ["admin", "user"]
```

## Hello World Tool Walk-through

Let's build a simple "Hello World" tool step by step:

### Step 1: Create the Tool File

Create a file named `hello_world.py`:

```python
"""
title: Hello World Tool
author: OpenWebUI Guide
author_url: https://github.com/therobrary/AI-assigned-research-projects
version: 1.0.0
"""

from typing import Callable, Any
import asyncio

class Tools:
    def __init__(self):
        self.citation = False
        
    async def hello_world(
        self,
        name: str,
        __user__: dict,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        A simple hello world function that greets the user
        
        :param name: The name to greet
        :param __user__: User information
        :param __event_emitter__: Event emitter for real-time updates
        :return: A greeting message
        """
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status", 
                "data": {"description": "Generating greeting..."}
            })
        
        # Simulate some processing time
        await asyncio.sleep(1)
        
        greeting = f"Hello, {name}! Welcome to OpenWebUI tools!"
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status", 
                "data": {"description": "Greeting complete!"}
            })
        
        return greeting
```

### Step 2: Install the Tool

1. Copy the tool file to your OpenWebUI tools directory
2. Restart OpenWebUI (if required)
3. The tool will automatically appear in the tools list

### Step 3: Test the Tool

1. Open OpenWebUI
2. Look for "Hello World Tool" in the tools section
3. Call the function: "Use hello_world tool with name 'Alice'"
4. Verify the output: "Hello, Alice! Welcome to OpenWebUI tools!"

## Best Practices

### 1. Naming Conventions

- **Tool Names**: Use descriptive, lowercase names with underscores
- **Function Names**: Use clear, action-oriented names
- **Variables**: Follow Python PEP 8 conventions

```python
# Good
async def search_web(self, query: str) -> str:

# Avoid
async def func1(self, q: str) -> str:
```

### 2. Error Handling

Always implement proper error handling:

```python
async def safe_function(self, input_data: str, __user__: dict) -> str:
    try:
        # Your logic here
        result = process_data(input_data)
        return result
    except ValueError as e:
        return f"Invalid input: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
```

### 3. Logging

Use proper logging for debugging and monitoring:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Tools:
    async def logged_function(self, prompt: str, __user__: dict) -> str:
        logger.info(f"Processing request from user {__user__.get('id')}")
        
        try:
            result = process_prompt(prompt)
            logger.info("Request processed successfully")
            return result
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise
```

### 4. User Experience

Provide clear feedback and status updates:

```python
async def user_friendly_function(
    self,
    prompt: str,
    __user__: dict,
    __event_emitter__: Callable[[dict], Any] = None,
) -> str:
    steps = [
        "Analyzing input...",
        "Processing data...",
        "Generating response...",
        "Finalizing result..."
    ]
    
    for i, step in enumerate(steps):
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "description": step,
                    "progress": (i + 1) / len(steps)
                }
            })
        
        # Simulate work
        await asyncio.sleep(1)
    
    return "Task completed successfully!"
```

### 5. Input Validation

Validate inputs before processing:

```python
async def validated_function(self, url: str, __user__: dict) -> str:
    # Validate URL format
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return "Error: Invalid URL format"
    
    # Process valid URL
    return f"Processing URL: {url}"
```

### 6. Internationalization (i18n)

Support multiple languages:

```python
MESSAGES = {
    "en": {
        "processing": "Processing your request...",
        "complete": "Task completed successfully!",
        "error": "An error occurred"
    },
    "es": {
        "processing": "Procesando su solicitud...",
        "complete": "¡Tarea completada con éxito!",
        "error": "Ocurrió un error"
    }
}

def get_message(key: str, lang: str = "en") -> str:
    return MESSAGES.get(lang, MESSAGES["en"]).get(key, key)
```

### 7. Configuration Management

Use environment variables for configuration:

```python
import os

class Tools:
    def __init__(self):
        self.api_key = os.getenv("YOUR_API_KEY")
        self.base_url = os.getenv("YOUR_BASE_URL", "https://api.example.com")
        
        if not self.api_key:
            raise ValueError("YOUR_API_KEY environment variable is required")
```

### Checklist

- [ ] Clear, descriptive function names
- [ ] Comprehensive error handling
- [ ] Input validation
- [ ] Proper logging
- [ ] User-friendly status updates
- [ ] Documentation (docstrings)
- [ ] Type hints
- [ ] Environment-based configuration
- [ ] Testing with various inputs
- [ ] Performance considerations

## Advanced Topics

### 1. Stateful Tools

For tools that need to maintain state between calls:

```python
class Tools:
    def __init__(self):
        self.session_data = {}
        
    async def stateful_function(
        self,
        action: str,
        data: str = "",
        __user__: dict = None,
    ) -> str:
        user_id = __user__.get("id")
        
        if user_id not in self.session_data:
            self.session_data[user_id] = {"history": []}
        
        if action == "store":
            self.session_data[user_id]["history"].append(data)
            return f"Stored: {data}"
        elif action == "recall":
            history = self.session_data[user_id]["history"]
            return f"History: {', '.join(history)}"
        elif action == "clear":
            self.session_data[user_id] = {"history": []}
            return "History cleared"
        
        return "Unknown action"
```

### 2. External API Integration

Integrating with external services:

```python
import aiohttp
import json

class Tools:
    def __init__(self):
        self.api_key = os.getenv("EXTERNAL_API_KEY")
        
    async def call_external_api(
        self,
        query: str,
        __user__: dict,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": "Calling external API..."}
            })
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {"query": query}
            
            try:
                async with session.post(
                    "https://api.example.com/search",
                    headers=headers,
                    json=payload
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return f"API Response: {data.get('result', 'No result')}"
                    else:
                        return f"API Error: {response.status}"
                        
            except aiohttp.ClientError as e:
                return f"Network error: {str(e)}"
```

### 3. Async Operations

Handling multiple async operations:

```python
import asyncio

class Tools:
    async def parallel_processing(
        self,
        urls: str,  # Comma-separated URLs
        __user__: dict,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        url_list = [url.strip() for url in urls.split(",")]
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Processing {len(url_list)} URLs..."}
            })
        
        async def process_url(url: str) -> str:
            # Simulate processing
            await asyncio.sleep(1)
            return f"Processed: {url}"
        
        # Process URLs in parallel
        tasks = [process_url(url) for url in url_list]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Format results
        formatted_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                formatted_results.append(f"Error processing {url_list[i]}: {str(result)}")
            else:
                formatted_results.append(result)
        
        return "\n".join(formatted_results)
```

### 4. File Operations

Working with files and uploads:

```python
import tempfile
import os

class Tools:
    async def process_file(
        self,
        file_content: str,
        filename: str = "input.txt",
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": "Processing file..."}
            })
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_path = temp_file.name
        
        try:
            # Process the file
            with open(temp_path, 'r') as f:
                content = f.read()
                word_count = len(content.split())
                line_count = len(content.splitlines())
            
            result = f"File Analysis:\n"
            result += f"Filename: {filename}\n"
            result += f"Lines: {line_count}\n"
            result += f"Words: {word_count}\n"
            result += f"Characters: {len(content)}"
            
            return result
            
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
```

### 5. Database Integration

Connecting to databases:

```python
import sqlite3
import aiosqlite

class Tools:
    def __init__(self):
        self.db_path = "tool_data.db"
        
    async def database_operation(
        self,
        operation: str,
        table: str = "data",
        key: str = "",
        value: str = "",
        __user__: dict = None,
    ) -> str:
        
        async with aiosqlite.connect(self.db_path) as db:
            if operation == "create_table":
                await db.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table} (
                        id INTEGER PRIMARY KEY,
                        key TEXT UNIQUE,
                        value TEXT,
                        user_id TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                await db.commit()
                return f"Table {table} created successfully"
                
            elif operation == "insert":
                user_id = __user__.get("id") if __user__ else "anonymous"
                await db.execute(
                    f"INSERT OR REPLACE INTO {table} (key, value, user_id) VALUES (?, ?, ?)",
                    (key, value, user_id)
                )
                await db.commit()
                return f"Inserted {key}: {value}"
                
            elif operation == "select":
                cursor = await db.execute(f"SELECT value FROM {table} WHERE key = ?", (key,))
                result = await cursor.fetchone()
                return result[0] if result else f"Key {key} not found"
```

## FAQ & Troubleshooting

### Common Issues

#### Q: My tool doesn't appear in OpenWebUI
**A**: Check the following:
- Ensure the tool file is in the correct directory
- Verify the metadata format is correct
- Check that the class is named `Tools`
- Restart OpenWebUI if necessary

#### Q: Tool execution fails with "function not found"
**A**: Verify:
- Function is defined as `async`
- Function has correct parameter signature
- Function name doesn't conflict with reserved names

#### Q: Event emitter not working
**A**: Ensure:
- Function signature includes `__event_emitter__` parameter
- Check for `None` before using: `if __event_emitter__:`
- Use correct event format: `{"type": "status", "data": {...}}`

#### Q: External API calls timing out
**A**: Consider:
- Increasing timeout values
- Implementing retry logic
- Using connection pooling
- Adding proper error handling

#### Q: Tool state not persisting
**A**: Options:
- Use class instance variables for session state
- Implement database storage for persistent state
- Use external caching solutions (Redis, etc.)

### Performance Tips

1. **Use async/await properly**: Don't block the event loop
2. **Implement caching**: Cache frequently accessed data
3. **Limit resource usage**: Set reasonable timeouts and limits
4. **Use connection pooling**: For database and API connections
5. **Profile your code**: Identify bottlenecks

### Security Considerations

1. **Validate all inputs**: Never trust user input
2. **Use environment variables**: For sensitive configuration
3. **Implement proper authentication**: Check user permissions
4. **Sanitize outputs**: Prevent injection attacks
5. **Limit resource access**: Follow principle of least privilege

### Debugging Tips

1. **Use logging**: Add comprehensive logging throughout your tool
2. **Test incrementally**: Build and test small pieces at a time
3. **Check OpenWebUI logs**: Look for error messages in the server logs
4. **Use try-catch blocks**: Handle exceptions gracefully
5. **Test with different inputs**: Verify edge cases

## Resources

### Official Documentation
- [OpenWebUI Tools Documentation](https://docs.openwebui.com/features/plugin/tools/)
- [OpenWebUI Plugin Documentation](https://docs.openwebui.com/features/plugin/)

### Tutorials and Guides
- [OpenWebUI Action Tools Tutorial](https://pahautelman.github.io/pahautelman-blog/tutorials/open-webui-action-tools/open-webui-action-tools/)

### Example Repositories
- [OpenWebUI Main Repository](https://github.com/open-webui/open-webui)
- [Tool Skeleton Template](https://github.com/pahautelman/open-webui-tool-skeleton)
- [TogetherAI Image Generation Tool](https://github.com/therobrary/IaC-for-Robnet/blob/main/openwebui-tools/togetherai-img-gen.py)

### API References
- [OpenWeatherMap One Call API 3.0](https://openweathermap.org/api/one-call-3)

### Community Resources
- OpenWebUI Discord Server
- GitHub Discussions
- Reddit r/OpenWebUI

---

*This guide is part of the AI-assigned research projects collection. For updates and additional resources, visit the [repository](https://github.com/therobrary/AI-assigned-research-projects).*