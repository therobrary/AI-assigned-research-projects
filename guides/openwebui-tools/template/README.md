# OpenWebUI Tool Template

A template for creating custom OpenWebUI tools. This template provides a solid foundation with best practices, error handling, and common patterns.

## Quick Start

1. **Copy this template**:
   ```bash
   cp -r template/ my_new_tool/
   cd my_new_tool/
   ```

2. **Customize the tool**:
   - Edit `main.py` and update the metadata (title, author, etc.)
   - Replace `your_main_function` with your actual function name
   - Implement your tool's logic in the processing methods
   - Update `requirements.txt` with your dependencies

3. **Configure environment variables** (if needed):
   ```bash
   export YOUR_API_KEY="your_api_key_here"
   export YOUR_API_URL="https://your-api.com"
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install in OpenWebUI**:
   - Copy `main.py` to your OpenWebUI tools directory
   - Restart OpenWebUI
   - Your tool will appear in the tools list

## Template Structure

```
template/
├── main.py              # Main tool implementation
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

## What's Included

### ✅ Basic Structure
- Proper metadata format
- Tool class with `__init__` method
- Main function with correct signature
- Event emitter support

### ✅ Error Handling
- Input validation
- Exception catching
- User-friendly error messages
- Logging support

### ✅ Best Practices
- Async/await patterns
- Type hints
- Comprehensive docstrings
- Configuration via environment variables
- Status updates for users

### ✅ Helper Methods
- External API calling pattern
- Input validation utilities
- Output formatting helpers
- Private method organization

### ✅ User Experience
- Real-time status updates
- Progress indicators
- Clear error messages
- Proper logging

## Customization Guide

### 1. Update Metadata

Edit the metadata at the top of `main.py`:

```python
"""
title: My Awesome Tool
author: Your Name
author_url: https://github.com/yourusername
funding_url: https://github.com/sponsors/yourusername
version: 1.0.0
"""
```

### 2. Rename Main Function

Change `your_main_function` to something descriptive:

```python
async def search_database(self, query: str, ...):
async def process_image(self, image_url: str, ...):
async def generate_report(self, data: str, ...):
```

### 3. Implement Your Logic

Replace the processing logic in `_process_input`:

```python
async def _process_input(self, input_data: str, option: str, __event_emitter__=None):
    # Your custom logic here
    result = await your_custom_processing(input_data)
    return result
```

### 4. Add Configuration

Add environment variables for your tool:

```python
def __init__(self):
    self.my_api_key = os.getenv("MY_API_KEY")
    self.my_setting = os.getenv("MY_SETTING", "default_value")
```

### 5. Update Dependencies

Modify `requirements.txt` with your specific dependencies:

```
aiohttp>=3.8.0
your-specific-library>=1.0.0
```

## Function Signature Patterns

### Basic Function
```python
async def simple_function(self, input: str, __user__: dict) -> str:
```

### Function with Options
```python
async def advanced_function(
    self,
    required_param: str,
    optional_param: str = "default",
    __user__: dict = None,
    __event_emitter__: Callable[[dict], Any] = None,
) -> str:
```

### Function with Multiple Types
```python
async def flexible_function(
    self,
    text_input: str,
    number_input: int = 10,
    boolean_flag: bool = True,
    __user__: dict = None,
) -> str:
```

## Event Emitter Usage

Send status updates to users:

```python
# Status update
await __event_emitter__({
    "type": "status",
    "data": {"description": "Processing..."}
})

# Error message
await __event_emitter__({
    "type": "error", 
    "data": {"description": "Something went wrong"}
})

# Progress update
await __event_emitter__({
    "type": "status",
    "data": {
        "description": "Step 2 of 5...",
        "progress": 0.4
    }
})
```

## Common Patterns

### API Integration
```python
async def call_api(self, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(self.api_url, json=data) as response:
            return await response.json()
```

### File Processing
```python
async def process_file(self, file_content: str):
    # Process file content
    lines = file_content.split('\n')
    # Your processing logic
    return processed_result
```

### Database Operations
```python
async def query_database(self, query: str):
    # Your database query logic
    # Return formatted results
    pass
```

## Testing Your Tool

1. **Test basic functionality**:
   ```python
   # Test with minimal input
   result = await tool.your_main_function("test input", __user__={})
   ```

2. **Test error conditions**:
   ```python
   # Test with empty input
   # Test with invalid input
   # Test with missing API key
   ```

3. **Test in OpenWebUI**:
   - Install and test in actual OpenWebUI environment
   - Verify all functions appear correctly
   - Test with real user interactions

## Common Issues and Solutions

### Tool Doesn't Appear
- Check metadata format
- Ensure class is named `Tools`
- Verify file is in correct directory

### Function Not Working
- Check async/await syntax
- Verify parameter signatures
- Check for syntax errors

### Status Updates Not Showing
- Ensure `__event_emitter__` parameter is included
- Check event format
- Test with `if __event_emitter__:` guard

## Next Steps

After customizing this template:

1. **Test thoroughly** with various inputs
2. **Add comprehensive error handling** for your specific use case
3. **Write documentation** for your users
4. **Consider adding multiple functions** if appropriate
5. **Optimize performance** for your specific operations
6. **Add logging** for debugging and monitoring

## Resources

- [OpenWebUI Tools Guide](../openwebui-tools-guide.md)
- [Example Tools](../examples/)
- [OpenWebUI Documentation](https://docs.openwebui.com/features/plugin/tools/)

---

Happy tool building! 🛠️