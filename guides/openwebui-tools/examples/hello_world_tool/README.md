# Hello World Tool

This is a minimal example of an OpenWebUI tool that demonstrates basic functionality.

## Features

- **Multi-language greetings**: Generate greetings in 9 different languages
- **Farewell messages**: Say goodbye in multiple languages
- **Language support**: List all supported languages
- **Event emission**: Provides real-time status updates

## Installation

1. Copy `hello_world.py` to your OpenWebUI tools directory
2. Restart OpenWebUI or refresh the tools list
3. The tool will appear as "Hello World Tool" in your available tools

## Usage Examples

### Basic Greeting
```
"Say hello to Alice"
```
Result: "Hello, Alice!"

### Multi-language Greeting
```
"Greet me in Spanish"
```
Result: "¡Hola, World!"

### Custom Name and Language
```
"Say hello to Maria in French"
```
Result: "Bonjour, Maria!"

### Farewell Messages
```
"Say goodbye to John in German"
```
Result: "Auf Wiedersehen, John!"

### Get Supported Languages
```
"What languages does the greeting tool support?"
```
Result: Lists all supported language codes and names

## Supported Languages

- **en**: English
- **es**: Spanish  
- **fr**: French
- **de**: German
- **it**: Italian
- **pt**: Portuguese
- **ru**: Russian
- **ja**: Japanese
- **zh**: Chinese

## Code Structure

The tool consists of three main actions:

1. **greet()**: Generates greeting messages
2. **farewell()**: Generates farewell messages  
3. **get_supported_languages()**: Lists supported languages

Each action includes:
- Type hints for parameters
- Comprehensive docstrings
- Event emission for status updates
- Sensible default values

## Learning Points

This example demonstrates:
- Basic tool structure and metadata
- Parameter handling with defaults
- Event emission for user feedback
- Multi-language support
- Proper documentation and error handling

## Next Steps

After understanding this example, you can:
1. Modify the supported languages
2. Add new greeting types (morning, evening, etc.)
3. Integrate with external translation APIs
4. Add user preference storage

This tool serves as a foundation for understanding OpenWebUI tool development before moving on to more complex examples like the web search or weather tools.