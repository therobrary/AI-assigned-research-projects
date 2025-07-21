# MCP Client Examples

This directory contains example client implementations for connecting to MCP (Managed Capabilities Platform) servers through the Docker MCP Gateway.

## Available Clients

### 1. Python Stout Client (`python_stout_client.py`)

High-performance synchronous client for request/response operations with stout servers.

**Features:**
- Text generation
- Chat completion
- Embeddings generation
- Health monitoring
- Server statistics

**Usage:**
```bash
# Set environment variables
export MCP_GATEWAY_URL="http://localhost:8080"
export MCP_API_KEY="your-api-key"

# Run the client
python python_stout_client.py
```

**Dependencies:**
```bash
pip install requests
```

### 2. Python SSE Client (`python_sse_client.py`)

Asynchronous client for real-time streaming operations with SSE (Server-Sent Events) servers.

**Features:**
- Streaming text generation
- Real-time chat streaming
- Event subscription
- Active stream monitoring

**Usage:**
```bash
# Set environment variables
export MCP_GATEWAY_URL="http://localhost:8080"
export MCP_API_KEY="your-api-key"

# Run the client
python python_sse_client.py
```

**Dependencies:**
```bash
pip install aiohttp asyncio
```

### 3. Streamable HTTP Client (`streamable_http_request.sh`)

Shell script client for handling large data transfers with streamable HTTP servers.

**Features:**
- File upload and processing
- Large dataset streaming
- Progress monitoring
- Batch operations

**Usage:**
```bash
# Make executable
chmod +x streamable_http_request.sh

# Health check
./streamable_http_request.sh

# Upload and process file
./streamable_http_request.sh -f input.pdf -o processed.json

# Download large dataset
./streamable_http_request.sh -o dataset.csv

# Help
./streamable_http_request.sh --help
```

**Dependencies:**
- `curl` - HTTP client
- `jq` - JSON processor

## Environment Variables

All clients support the following environment variables:

- `MCP_GATEWAY_URL`: Base URL of the MCP Gateway (default: http://localhost:8080)
- `MCP_API_KEY`: API key for authentication

## Authentication

### API Key Authentication

Set your API key in the environment:

```bash
export MCP_API_KEY="your-secure-api-key"
```

Or pass it directly to clients:

```python
# Python clients
client = MCPStoutClient(api_key="your-api-key")
```

```bash
# Shell script
./streamable_http_request.sh -k "your-api-key"
```

### OAuth2 Authentication

For OAuth2 authentication, use the appropriate flow for your application:

```python
# Example OAuth2 flow (pseudo-code)
import requests

# Step 1: Get authorization URL
auth_url = f"{gateway_url}/auth/authorize?client_id={client_id}&redirect_uri={redirect_uri}"

# Step 2: Exchange code for token
token_response = requests.post(f"{gateway_url}/auth/token", data={
    "code": auth_code,
    "client_id": client_id,
    "client_secret": client_secret
})

# Step 3: Use access token
access_token = token_response.json()["access_token"]
```

## Error Handling

All clients include comprehensive error handling:

### Python Clients

```python
try:
    response = client.generate("Hello, world!")
    print(response)
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except json.JSONDecodeError as e:
    print(f"Invalid JSON response: {e}")
```

### Shell Script

The shell script includes colored logging and proper exit codes:

```bash
# Check exit code
./streamable_http_request.sh
if [ $? -eq 0 ]; then
    echo "Success"
else
    echo "Failed"
fi
```

## Examples

### Simple Text Generation

```python
from python_stout_client import MCPStoutClient

client = MCPStoutClient()
response = client.generate(
    prompt="Explain quantum computing:",
    max_tokens=100,
    temperature=0.7
)
print(response["text"])
```

### Streaming Chat

```python
import asyncio
from python_sse_client import MCPSSEClient

async def chat_example():
    client = MCPSSEClient()
    messages = [
        {"role": "user", "content": "Tell me a story"}
    ]
    
    async for chunk in client.stream_chat(messages):
        if "delta" in chunk:
            print(chunk["delta"]["content"], end="", flush=True)

asyncio.run(chat_example())
```

### File Processing

```bash
# Upload and process a document
./streamable_http_request.sh \
    --file document.pdf \
    --output processed_output.json \
    --verbose
```

## Troubleshooting

### Common Issues

1. **Connection refused**
   ```
   Error: Failed to connect to MCP Gateway
   ```
   - Check if the MCP Gateway is running
   - Verify the URL and port
   - Check firewall settings

2. **Authentication failed**
   ```
   Error: 401 Unauthorized
   ```
   - Verify API key is correct
   - Check if API key is properly set in environment
   - Ensure API key has required permissions

3. **Timeout errors**
   ```
   Error: Request timeout
   ```
   - Increase timeout values
   - Check network connectivity
   - Verify server health

### Debug Mode

Enable verbose logging for troubleshooting:

```python
# Python clients
import logging
logging.basicConfig(level=logging.DEBUG)
```

```bash
# Shell script
./streamable_http_request.sh --verbose
```

### Health Checks

All clients include health check functionality:

```python
# Python
health = client.health_check()
print(health)
```

```bash
# Shell script
./streamable_http_request.sh  # Includes automatic health check
```

## Performance Tips

1. **Connection Pooling**: Python clients use session objects for connection reuse
2. **Async Operations**: Use SSE client for multiple concurrent operations
3. **Chunked Transfers**: Streamable client handles large files efficiently
4. **Timeouts**: Adjust timeout values based on expected response times

## Security Best Practices

1. **API Key Storage**: Never hardcode API keys in source code
2. **Environment Variables**: Use environment variables for sensitive data
3. **HTTPS**: Use HTTPS in production environments
4. **Rate Limiting**: Respect rate limits and implement backoff strategies
5. **Input Validation**: Validate all user inputs before sending to servers

## Contributing

To add new client examples:

1. Follow the existing naming convention
2. Include comprehensive error handling
3. Add usage examples and documentation
4. Test with all server types
5. Include dependencies and requirements