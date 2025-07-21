# OpenWebUI Tool Template

This template provides a complete boilerplate for creating new OpenWebUI tools. It includes best practices, error handling, and common patterns used in tool development.

## Quick Start

1. **Copy the template:**
   ```bash
   cp -r template/ my_new_tool/
   cd my_new_tool/
   ```

2. **Rename the main file:**
   ```bash
   mv tool_template.py my_tool_name.py
   ```

3. **Customize the metadata:**
   Edit the header of your tool file to update:
   - `title`: Display name of your tool
   - `author`: Your name or organization
   - `author_url`: Link to your profile/website
   - `funding_url`: Link for sponsorship/donations
   - `version`: Semantic version (start with 0.1.0)
   - `license`: Choose appropriate license

4. **Update the class configuration:**
   In the `__init__` method, modify:
   - `self.name`: Internal tool name (snake_case)
   - `self.description`: Brief description of what your tool does
   - API endpoints and configuration

5. **Implement your actions:**
   Replace the example actions (`my_action`, `secondary_action`) with your specific functionality.

6. **Test your tool:**
   - Install it in OpenWebUI
   - Test all actions with various inputs
   - Verify error handling works correctly

## Template Features

### Included Patterns

- **Metadata Header**: Proper tool metadata in the required format
- **Class Structure**: Standard `Tools` class with proper initialization
- **Action Methods**: Example actions with proper signatures and documentation
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Event Emission**: Real-time status updates using `__event_emitter__`
- **Input Validation**: Safe input handling and validation
- **API Integration**: Example external API integration with session pooling
- **Logging**: Proper logging setup for debugging
- **Caching**: Simple caching mechanism example

### Best Practices Demonstrated

1. **Type Hints**: All parameters and return values have type annotations
2. **Documentation**: Comprehensive docstrings for all public methods
3. **Error Messages**: Clear, actionable error messages for users
4. **Resource Management**: Proper HTTP session management
5. **Security**: Environment variable usage for API keys
6. **Performance**: Connection pooling and caching examples

## Customization Guide

### Adding New Actions

```python
def your_new_action(
    self,
    param1: str,
    param2: int = 10,
    __user__: dict = None,
    __event_emitter__: Callable[[dict], Any] = None,
) -> str:
    """
    Description of your new action.
    
    :param param1: Description of parameter 1
    :param param2: Description of parameter 2 with default
    :return: Description of return value
    """
    # Your implementation here
    pass
```

### API Integration

```python
def _make_api_call(self, endpoint: str, data: Dict) -> Optional[Dict]:
    """Make an API call with proper error handling"""
    try:
        response = self.session.post(
            f"{self.base_url}/{endpoint}",
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {str(e)}")
        return None
```

### Status Updates

```python
if __event_emitter__:
    __event_emitter__({
        "type": "status",
        "data": {
            "description": "Processing your request...",
            "done": False  # Set to True when complete
        },
    })
```

### Input Validation

```python
def _validate_email(self, email: str) -> str:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email.lower().strip()
```

## Configuration Options

### Environment Variables

Add environment variable configuration:

```python
def __init__(self):
    # API Configuration
    self.api_key = os.getenv("YOUR_API_KEY")
    self.api_base_url = os.getenv("YOUR_API_URL", "https://api.default.com")
    self.timeout = int(os.getenv("API_TIMEOUT", "30"))
    
    # Feature flags
    self.enable_caching = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    self.debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
```

### Configuration Validation

```python
def _validate_configuration(self):
    """Validate tool configuration on startup"""
    if not self.api_key:
        logger.warning("API key not configured - some features may be unavailable")
    
    if self.timeout < 5:
        logger.warning("Timeout is very low - may cause connection issues")
```

## Testing Your Tool

### Manual Testing

1. **Install the tool** in your OpenWebUI instance
2. **Test each action** with various inputs:
   - Valid inputs
   - Invalid inputs
   - Edge cases (empty strings, very long inputs, special characters)
3. **Check error handling** by:
   - Providing invalid API keys
   - Testing network timeouts
   - Testing with malformed data

### Example Test Cases

```python
# Test valid input
result = tool.my_action("valid input", "optional", 5, True)

# Test invalid input
result = tool.my_action("", "optional", 5, True)  # Should return error

# Test boundary conditions
result = tool.my_action("x" * 1000, "optional", 100, True)  # Max values
```

## Common Patterns

### Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_second=1.0):
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
```

### Async Operations

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def long_running_operation(
    self,
    data: str,
    __event_emitter__: Callable[[dict], Any] = None,
) -> str:
    """Handle long-running operations"""
    
    def heavy_work(data):
        import time
        time.sleep(5)  # Simulate heavy work
        return f"Processed: {data}"
    
    if __event_emitter__:
        __event_emitter__({
            "type": "status",
            "data": {"description": "Starting heavy processing...", "done": False},
        })
    
    with ThreadPoolExecutor() as executor:
        future = executor.submit(heavy_work, data)
        result = future.result()
    
    if __event_emitter__:
        __event_emitter__({
            "type": "status",
            "data": {"description": "Processing complete", "done": True},
        })
    
    return result
```

### Data Persistence

```python
import json

def _save_data(self, key: str, data: Dict):
    """Save data to a simple file-based cache"""
    cache_file = f"/tmp/tool_cache_{self.name}.json"
    try:
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        cache = {}
    
    cache[key] = data
    
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

def _load_data(self, key: str) -> Optional[Dict]:
    """Load data from cache"""
    cache_file = f"/tmp/tool_cache_{self.name}.json"
    try:
        with open(cache_file, 'r') as f:
            cache = json.load(f)
        return cache.get(key)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
```

## Deployment Checklist

Before deploying your tool:

- [ ] Update all metadata (title, author, version, etc.)
- [ ] Test all actions with various inputs
- [ ] Verify error handling works correctly
- [ ] Check that API keys are properly configured
- [ ] Test event emission and status updates
- [ ] Validate input sanitization
- [ ] Ensure proper logging is in place
- [ ] Test with different user contexts
- [ ] Verify resource cleanup (close connections, etc.)
- [ ] Document any environment variables needed
- [ ] Create user documentation (README)

## Troubleshooting

### Common Issues

1. **Tool doesn't appear in list**: Check Python syntax and class name
2. **Actions not working**: Verify method signatures and imports
3. **API errors**: Check environment variables and network connectivity
4. **Performance issues**: Add rate limiting and optimize heavy operations

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Add debug statements:

```python
logger.debug(f"Processing request: {data}")
logger.debug(f"API response: {response}")
```

This template provides a solid foundation for building robust, production-ready OpenWebUI tools. Customize it according to your specific needs and requirements.