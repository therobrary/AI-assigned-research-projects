# Web Search Tool

A comprehensive web search tool for OpenWebUI that combines SearXNG search with optional content extraction using Docling or fallback methods.

## Features

- 🔍 Web search using SearXNG
- 📄 Content extraction from web pages
- 🔄 Fallback extraction methods
- ⚡ Real-time status updates
- 🎛️ Configurable result limits
- 🛡️ Error handling and validation

## Functions

### `search_web(query, max_results, extract_content)`
Comprehensive web search with optional content extraction.

**Parameters:**
- `query` (str): The search query
- `max_results` (int): Maximum results to return (1-10, default: 5)
- `extract_content` (bool): Whether to extract full content (default: True)

**Example Usage:**
```
Use search_web tool with query "OpenWebUI tutorials" and max_results 3
```

### `quick_search(query)`
Quick search with basic results (no content extraction).

**Parameters:**
- `query` (str): The search query

**Example Usage:**
```
Use quick_search tool with query "latest AI news"
```

## Configuration

The tool can be configured using environment variables:

```bash
# SearXNG instance URL (default: https://search.brave4u.com)
export SEARXNG_URL="https://your-searxng-instance.com"

# Docling service URL for content extraction (optional)
export DOCLING_URL="http://your-docling-service:8080"
```

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `main.py` to your OpenWebUI tools directory

3. (Optional) Set up environment variables for custom SearXNG/Docling instances

4. Restart OpenWebUI

## Architecture

The tool follows a multi-step process:

1. **Search Phase**: Queries SearXNG API for web results
2. **Extraction Phase**: Extracts full content from top results using:
   - Docling service (if available)
   - Fallback HTTP extraction
3. **Formatting Phase**: Presents results in a structured format

## SearXNG Integration

This tool requires a SearXNG instance for web searches. Options:

1. **Public Instance**: Uses `https://search.brave4u.com` by default
2. **Self-hosted**: Set `SEARXNG_URL` environment variable
3. **Docker**: Run your own SearXNG container

### Setting up SearXNG (Optional)

```bash
# Using Docker
docker run -d -p 8888:8080 searxng/searxng
export SEARXNG_URL="http://localhost:8888"
```

## Docling Integration

Docling provides advanced content extraction. To use:

1. Set up a Docling service
2. Set `DOCLING_URL` environment variable
3. The tool will automatically use it for content extraction

If Docling is not available, the tool falls back to simple HTML parsing.

## Error Handling

The tool includes comprehensive error handling:

- ✅ Invalid query validation
- ✅ Network timeout handling
- ✅ API error responses
- ✅ Content extraction failures
- ✅ Graceful fallbacks

## Performance Notes

- Content extraction is limited to top 3 results for performance
- 30-second timeout for search requests
- 10-second timeout for content extraction
- Concurrent processing where possible

## Limitations

- Requires internet access
- Dependent on SearXNG availability
- Content extraction may fail for some sites
- Rate limiting may apply depending on SearXNG instance

## Troubleshooting

### Common Issues

1. **No search results**: Check SearXNG URL and connectivity
2. **Slow responses**: Disable content extraction or reduce max_results
3. **Extraction failures**: Check Docling service or rely on fallback
4. **Rate limiting**: Use your own SearXNG instance

### Debug Mode

Set `SEARXNG_URL` to a local instance for testing:
```bash
export SEARXNG_URL="http://localhost:8888"
```