"""
title: Web Search Tool
author: OpenWebUI Guide
author_url: https://github.com/therobrary/AI-assigned-research-projects
version: 1.0.0
"""

from typing import Callable, Any, List, Dict
import aiohttp
import asyncio
import json
import re
import os
from urllib.parse import quote_plus, urljoin


class Tools:
    def __init__(self):
        self.citation = True
        # Configuration - use environment variables or defaults
        self.searxng_url = os.getenv("SEARXNG_URL", "https://search.brave4u.com")
        self.docling_url = os.getenv("DOCLING_URL", "http://localhost:8080")
        self.max_results = 10
        self.timeout = 30
        
    async def search_web(
        self,
        query: str,
        max_results: int = 5,
        extract_content: bool = True,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Search the web using SearXNG and optionally extract content using Docling
        
        :param query: The search query
        :param max_results: Maximum number of results to return (1-10, default: 5)
        :param extract_content: Whether to extract full content from pages (default: True)
        :param __user__: User information
        :param __event_emitter__: Event emitter for real-time updates
        :return: Formatted search results with extracted content
        """
        
        # Validate inputs
        if not query.strip():
            return "Error: Search query cannot be empty"
        
        max_results = max(1, min(max_results, self.max_results))
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Searching for: {query}"}
            })
        
        try:
            # Step 1: Search using SearXNG
            search_results = await self._search_searxng(query, max_results, __event_emitter__)
            
            if not search_results:
                return "No search results found."
            
            # Step 2: Extract content if requested
            if extract_content:
                if __event_emitter__:
                    await __event_emitter__({
                        "type": "status",
                        "data": {"description": "Extracting content from top results..."}
                    })
                
                enhanced_results = await self._extract_content_from_results(
                    search_results, __event_emitter__
                )
            else:
                enhanced_results = search_results
            
            # Step 3: Format results
            formatted_results = self._format_search_results(enhanced_results, query)
            
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "Search complete! 🔍"}
                })
            
            return formatted_results
            
        except Exception as e:
            error_msg = f"Search error: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "error",
                    "data": {"description": error_msg}
                })
            return error_msg
    
    async def _search_searxng(
        self, 
        query: str, 
        max_results: int,
        __event_emitter__: Callable[[dict], Any] = None
    ) -> List[Dict]:
        """Search using SearXNG API"""
        
        search_url = f"{self.searxng_url}/search"
        params = {
            "q": query,
            "format": "json",
            "categories": "general",
            "engines": "google,bing,duckduckgo",
            "safesearch": "0"
        }
        
        headers = {
            "User-Agent": "OpenWebUI-Tool/1.0",
            "Accept": "application/json"
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
            try:
                async with session.get(search_url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = data.get("results", [])
                        
                        # Process and clean results
                        processed_results = []
                        for result in results[:max_results]:
                            processed_result = {
                                "title": result.get("title", ""),
                                "url": result.get("url", ""),
                                "content": result.get("content", ""),
                                "score": result.get("score", 0),
                                "engine": result.get("engine", "unknown")
                            }
                            
                            # Only include results with valid URLs
                            if processed_result["url"] and processed_result["title"]:
                                processed_results.append(processed_result)
                        
                        return processed_results
                    else:
                        raise Exception(f"SearXNG API returned status {response.status}")
                        
            except aiohttp.ClientError as e:
                raise Exception(f"Failed to connect to SearXNG: {str(e)}")
    
    async def _extract_content_from_results(
        self, 
        results: List[Dict],
        __event_emitter__: Callable[[dict], Any] = None
    ) -> List[Dict]:
        """Extract full content from search results using Docling or fallback method"""
        
        enhanced_results = []
        
        for i, result in enumerate(results[:3]):  # Only extract from top 3 results
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Extracting content from result {i+1}/3..."}
                })
            
            try:
                extracted_content = await self._extract_with_docling(result["url"])
                
                if not extracted_content:
                    # Fallback to simple HTTP request
                    extracted_content = await self._extract_with_fallback(result["url"])
                
                result["extracted_content"] = extracted_content
                enhanced_results.append(result)
                
            except Exception as e:
                # If extraction fails, keep original result
                result["extraction_error"] = str(e)
                enhanced_results.append(result)
                
        # Add remaining results without extraction
        enhanced_results.extend(results[3:])
        
        return enhanced_results
    
    async def _extract_with_docling(self, url: str) -> str:
        """Extract content using Docling service"""
        
        if not self.docling_url or self.docling_url == "http://localhost:8080":
            # Skip if Docling is not available
            return ""
        
        docling_endpoint = f"{self.docling_url}/extract"
        payload = {"url": url}
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            try:
                async with session.post(docling_endpoint, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("content", "")
                    return ""
            except:
                return ""
    
    async def _extract_with_fallback(self, url: str) -> str:
        """Fallback content extraction using simple HTTP request"""
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        # Simple text extraction (remove HTML tags)
                        text = re.sub(r'<[^>]+>', '', html)
                        text = re.sub(r'\s+', ' ', text).strip()
                        # Return first 1000 characters
                        return text[:1000] + "..." if len(text) > 1000 else text
                    return ""
            except:
                return ""
    
    def _format_search_results(self, results: List[Dict], query: str) -> str:
        """Format search results for display"""
        
        output = f"# Web Search Results for: '{query}'\n\n"
        output += f"Found {len(results)} results:\n\n"
        
        for i, result in enumerate(results, 1):
            output += f"## {i}. {result['title']}\n\n"
            output += f"**URL:** {result['url']}\n\n"
            
            # Use extracted content if available, otherwise use snippet
            if result.get("extracted_content"):
                content = result["extracted_content"]
                output += f"**Content:** {content}\n\n"
            elif result.get("content"):
                output += f"**Snippet:** {result['content']}\n\n"
            
            if result.get("engine"):
                output += f"**Source:** {result['engine']}\n\n"
            
            if result.get("extraction_error"):
                output += f"*Note: Content extraction failed - {result['extraction_error']}*\n\n"
            
            output += "---\n\n"
        
        return output.strip()
    
    async def quick_search(
        self,
        query: str,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Quick web search with basic results (no content extraction)
        
        :param query: The search query
        :param __user__: User information
        :param __event_emitter__: Event emitter for real-time updates
        :return: Basic search results
        """
        
        return await self.search_web(
            query=query,
            max_results=5,
            extract_content=False,
            __user__=__user,
            __event_emitter__=__event_emitter
        )