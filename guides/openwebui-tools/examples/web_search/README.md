# Web Search Tool

An advanced web search tool for OpenWebUI that integrates with SearxNG search engines and provides content extraction capabilities for better LLM processing.

## Features

- **Multi-engine search**: Supports Google, Bing, DuckDuckGo, and other SearxNG engines
- **Content extraction**: Extracts full page content for comprehensive analysis
- **Customizable results**: Configure number of results, search engines, and categories
- **Rate limiting**: Respectful delays between requests
- **Error handling**: Robust error handling for network issues
- **Real-time updates**: Progress feedback via event emitters

## Prerequisites

This tool requires access to a SearxNG instance. You can use:
- Public instances (like searx.be - used by default)
- Self-hosted SearxNG instance
- Custom SearxNG deployment

### Optional: Docling Integration

For enhanced content extraction, you can integrate with Docling endpoints (not implemented in this basic version but can be extended).

## Installation

1. Copy `web_search.py` to your OpenWebUI tools directory
2. Install required dependencies (if not already available):
   ```bash
   pip install requests
   ```
3. Restart OpenWebUI or refresh the tools list

## Configuration

### Environment Variables (Optional)

```bash
# Custom SearxNG instance
export SEARX_BASE_URL="https://your-searx-instance.com"

# Custom Docling endpoint for content extraction
export DOCLING_ENDPOINT="https://your-docling-instance.com"
```

## Usage Examples

### Basic Web Search
```
"Search for 'OpenWebUI plugins tutorial'"
```

### Customized Search
```
"Search for 'climate change' using 5 results from google and bing"
```

### Content Extraction
```
"Search and extract content about 'machine learning algorithms'"
```

## Actions

### 1. search_web()

Basic web search with customizable parameters.

**Parameters:**
- `query` (required): Search query string
- `num_results` (optional): Number of results (default: 5)
- `search_engines` (optional): Engines to use (default: "google,bing,duckduckgo")
- `categories` (optional): Search categories (default: "general")
- `language` (optional): Language code (default: "en")
- `safesearch` (optional): Safe search level 0-2 (default: 1)

### 2. search_and_extract()

Advanced search with content extraction for better LLM processing.

**Parameters:**
- `query` (required): Search query string
- `num_results` (optional): Number of results to extract (default: 3)
- `extract_content` (optional): Whether to extract full content (default: True)

## Technical Details

### Search Process

1. **Query Processing**: Validates and sanitizes search queries
2. **SearxNG Integration**: Sends requests to SearxNG instance with specified parameters
3. **Result Filtering**: Processes and filters search results
4. **Content Extraction**: Optionally extracts full page content
5. **Formatting**: Formats results for optimal LLM consumption

### Content Extraction

The tool implements a simplified content extraction process:
- Removes script and style elements
- Strips HTML tags
- Cleans whitespace and formatting
- Filters out navigation and boilerplate content
- Limits content length to prevent token overflow

### Error Handling

- Network timeout handling (30-second timeout)
- HTTP error status checking
- Graceful degradation when content extraction fails
- User-friendly error messages

### Rate Limiting

- 0.5-second delays between content extraction requests
- Connection pooling for efficient HTTP requests
- Respectful user-agent headers

## Customization

### Adding New Search Engines

Modify the `search_engines` parameter to include additional SearxNG-supported engines:
```python
search_engines = "google,bing,duckduckgo,startpage,qwant"
```

### Custom Content Extraction

Extend the `_extract_text_from_html()` method to use more sophisticated HTML parsing:
```python
from bs4 import BeautifulSoup

def _extract_text_from_html(self, html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    # Remove unwanted elements
    for element in soup(['script', 'style', 'nav', 'footer']):
        element.decompose()
    return soup.get_text(strip=True)
```

### Integration with Docling

For production use, integrate with Docling for better content extraction:
```python
def _extract_with_docling(self, url: str) -> str:
    if not self.docling_endpoint:
        return ""
    
    response = self.session.post(
        f"{self.docling_endpoint}/extract",
        json={"url": url}
    )
    return response.json().get("extracted_text", "")
```

## Security Considerations

1. **Input Validation**: All queries are sanitized before processing
2. **Rate Limiting**: Prevents abuse of external services
3. **Timeout Limits**: Prevents hanging requests
4. **User Agent**: Identifies the bot appropriately
5. **Content Length**: Limits extracted content to prevent memory issues

## Troubleshooting

### Common Issues

1. **No results found**: Check SearxNG instance availability
2. **Timeout errors**: Verify network connectivity and reduce `num_results`
3. **Content extraction fails**: Check if target sites block bots

### Debug Mode

Add logging to debug issues:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Tips

1. **Reduce results**: Lower `num_results` for faster responses
2. **Skip extraction**: Set `extract_content=False` for quick searches
3. **Cache results**: Implement caching for repeated queries
4. **Use fewer engines**: Reduce `search_engines` list for faster searches

## Future Enhancements

- Integration with real Docling service
- Caching mechanism for repeated searches
- Image and video search capabilities
- Advanced filtering and ranking
- Search history and bookmarking
- Custom search engine configuration UI

This tool provides a solid foundation for web search capabilities in OpenWebUI and can be extended based on specific requirements.