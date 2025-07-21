"""
title: Web Search Tool
author: OpenWebUI Community
author_url: https://github.com/open-webui/open-webui
version: 1.0.0
license: MIT
"""

import requests
import json
import re
from typing import Callable, Any, Dict, List, Optional
from urllib.parse import quote_plus, urljoin
import time

class Tools:
    def __init__(self):
        self.name = "web_search"
        self.description = "Advanced web search tool using SearxNG with content extraction via Docling"
        
        # Default SearxNG instance (can be configured via environment variables)
        self.searx_base_url = "https://searx.be"  # Public instance
        self.docling_endpoint = None  # Optional Docling endpoint for content extraction
        
        # Request session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "OpenWebUI-WebSearch/1.0",
            "Accept": "application/json"
        })

    def search_web(
        self,
        query: str,
        num_results: int = 5,
        search_engines: str = "google,bing,duckduckgo",
        categories: str = "general",
        language: str = "en",
        safesearch: int = 1,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Search the web using SearxNG and return formatted results.
        
        :param query: Search query
        :param num_results: Number of results to return (default: 5)
        :param search_engines: Comma-separated list of engines (default: "google,bing,duckduckgo")
        :param categories: Search categories (default: "general")
        :param language: Language code (default: "en")
        :param safesearch: Safe search level 0-2 (default: 1)
        :return: Formatted search results
        """
        if not query or len(query.strip()) == 0:
            return "Error: Search query cannot be empty"
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": f"Searching for: {query}", "done": False},
            })
        
        try:
            # Prepare search parameters
            params = {
                "q": query.strip(),
                "format": "json",
                "engines": search_engines,
                "categories": categories,
                "language": language,
                "safesearch": safesearch,
                "pageno": 1
            }
            
            # Make search request
            search_url = f"{self.searx_base_url}/search"
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            search_data = response.json()
            results = search_data.get("results", [])
            
            if not results:
                return f"No results found for query: {query}"
            
            if __event_emitter__:
                __event_emitter__({
                    "type": "status", 
                    "data": {"description": f"Found {len(results)} results, formatting...", "done": False},
                })
            
            # Format results
            formatted_results = self._format_search_results(results[:num_results], query)
            
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": "Search completed successfully", "done": True},
                })
            
            return formatted_results
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Search request failed: {str(e)}"
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Unexpected error during search: {str(e)}"
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return f"Error: {error_msg}"

    def search_and_extract(
        self,
        query: str,
        num_results: int = 3,
        extract_content: bool = True,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Search the web and extract content from top results for better LLM processing.
        
        :param query: Search query
        :param num_results: Number of results to extract content from (default: 3)
        :param extract_content: Whether to extract full content (default: True)
        :return: Search results with extracted content
        """
        if not query or len(query.strip()) == 0:
            return "Error: Search query cannot be empty"
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": f"Searching and extracting content for: {query}", "done": False},
            })
        
        try:
            # First, get search results
            search_results = self._get_raw_search_results(query, num_results * 2)  # Get more to filter
            
            if not search_results:
                return f"No results found for query: {query}"
            
            # Filter and extract content from top results
            extracted_results = []
            processed = 0
            
            for result in search_results:
                if processed >= num_results:
                    break
                    
                if __event_emitter__:
                    __event_emitter__({
                        "type": "status",
                        "data": {"description": f"Extracting content from result {processed + 1}/{num_results}", "done": False},
                    })
                
                extracted_result = self._extract_content_from_result(result, extract_content)
                if extracted_result:
                    extracted_results.append(extracted_result)
                    processed += 1
                
                # Small delay to be respectful to servers
                time.sleep(0.5)
            
            formatted_output = self._format_extracted_results(extracted_results, query)
            
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": "Content extraction completed", "done": True},
                })
            
            return formatted_output
            
        except Exception as e:
            error_msg = f"Error during search and extraction: {str(e)}"
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return f"Error: {error_msg}"

    def _get_raw_search_results(self, query: str, num_results: int = 10) -> List[Dict]:
        """Get raw search results from SearxNG"""
        params = {
            "q": query.strip(),
            "format": "json",
            "engines": "google,bing,duckduckgo",
            "categories": "general",
            "language": "en",
            "safesearch": 1,
            "pageno": 1
        }
        
        search_url = f"{self.searx_base_url}/search"
        response = self.session.get(search_url, params=params, timeout=30)
        response.raise_for_status()
        
        search_data = response.json()
        return search_data.get("results", [])[:num_results]

    def _extract_content_from_result(self, result: Dict, extract_content: bool = True) -> Optional[Dict]:
        """Extract content from a search result"""
        url = result.get("url", "")
        title = result.get("title", "")
        content = result.get("content", "")
        
        if not url or not title:
            return None
        
        extracted_result = {
            "title": title,
            "url": url,
            "snippet": content,
            "extracted_content": ""
        }
        
        if extract_content and url:
            try:
                # Try to extract content directly (simplified approach)
                page_response = self.session.get(url, timeout=15, headers={
                    "User-Agent": "Mozilla/5.0 (compatible; OpenWebUI-Bot/1.0)"
                })
                page_response.raise_for_status()
                
                # Simple text extraction (in a real implementation, you'd use proper HTML parsing)
                page_content = page_response.text
                extracted_text = self._extract_text_from_html(page_content)
                
                # Limit extracted content length
                if len(extracted_text) > 2000:
                    extracted_text = extracted_text[:2000] + "..."
                
                extracted_result["extracted_content"] = extracted_text
                
            except Exception as e:
                # If content extraction fails, use the snippet
                extracted_result["extracted_content"] = content
        
        return extracted_result

    def _extract_text_from_html(self, html_content: str) -> str:
        """Simple HTML text extraction (simplified implementation)"""
        # Remove script and style elements
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common navigation and footer text patterns
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if len(line) > 20 and not any(nav_word in line.lower() for nav_word in 
                                        ['cookie', 'privacy policy', 'terms of service', 'navigation', 'menu']):
                cleaned_lines.append(line)
        
        return ' '.join(cleaned_lines).strip()

    def _format_search_results(self, results: List[Dict], query: str) -> str:
        """Format search results for display"""
        if not results:
            return f"No results found for: {query}"
        
        formatted = f"## Search Results for: {query}\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "")
            content = result.get("content", "No description available")
            
            formatted += f"### {i}. {title}\n"
            formatted += f"**URL:** {url}\n"
            formatted += f"**Description:** {content}\n\n"
        
        return formatted

    def _format_extracted_results(self, results: List[Dict], query: str) -> str:
        """Format extracted results for LLM processing"""
        if not results:
            return f"No content extracted for: {query}"
        
        formatted = f"## Extracted Content for: {query}\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "")
            snippet = result.get("snippet", "")
            extracted_content = result.get("extracted_content", "")
            
            formatted += f"### Source {i}: {title}\n"
            formatted += f"**URL:** {url}\n"
            
            if snippet:
                formatted += f"**Snippet:** {snippet}\n"
            
            if extracted_content and len(extracted_content) > len(snippet):
                formatted += f"**Extracted Content:**\n{extracted_content}\n"
            
            formatted += "\n---\n\n"
        
        return formatted