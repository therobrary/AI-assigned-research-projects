# Hello World Tool

A simple demonstration tool for OpenWebUI that shows basic functionality including:

- Simple greeting function
- User information access
- Event emitter usage
- Input validation
- Multiple function examples

## Functions

### `hello_world(name)`
Generates a personalized greeting message.

**Parameters:**
- `name` (str): The name to greet

**Example Usage:**
```
Use hello_world tool with name "Alice"
```

### `echo_message(message, times)`
Echoes a message a specified number of times.

**Parameters:**
- `message` (str): The message to echo
- `times` (int): Number of repetitions (1-10, default: 1)

**Example Usage:**
```
Use echo_message tool with message "Hello OpenWebUI!" and times 3
```

## Installation

1. Copy `main.py` to your OpenWebUI tools directory
2. Restart OpenWebUI (if required)
3. The tool will appear in your tools list

## Features Demonstrated

- ✅ Basic tool structure
- ✅ Function metadata and docstrings
- ✅ User information access (`__user__` parameter)
- ✅ Real-time status updates (`__event_emitter__`)
- ✅ Input validation
- ✅ Multiple functions in one tool
- ✅ Error handling
- ✅ Async/await patterns

This tool serves as a starting point for building more complex OpenWebUI tools.