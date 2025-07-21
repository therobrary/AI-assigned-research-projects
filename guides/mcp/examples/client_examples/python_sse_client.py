#!/usr/bin/env python3
"""
MCP SSE (Server-Sent Events) Client Example

This script demonstrates how to connect to and interact with an MCP SSE server
through the MCP Gateway. SSE servers are designed for real-time streaming data.

Usage:
    python python_sse_client.py
"""

import os
import json
import time
import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional, AsyncGenerator
from urllib.parse import urljoin


class MCPSSEClient:
    """Async client for interacting with MCP SSE servers via the Gateway."""
    
    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        api_key: Optional[str] = None,
        timeout: int = 300,
        verify_ssl: bool = True
    ):
        """
        Initialize the MCP SSE client.
        
        Args:
            base_url: Base URL of the MCP Gateway
            api_key: API key for authentication
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv('MCP_API_KEY')
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.verify_ssl = verify_ssl
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Setup headers
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'text/event-stream',
            'Cache-Control': 'no-cache'
        }
        
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'
    
    async def _create_session(self) -> aiohttp.ClientSession:
        """Create an aiohttp session with proper configuration."""
        connector = aiohttp.TCPConnector(verify_ssl=self.verify_ssl)
        return aiohttp.ClientSession(
            connector=connector,
            timeout=self.timeout,
            headers=self.headers
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the SSE server.
        
        Returns:
            Dictionary containing health status
        """
        async with self._create_session() as session:
            try:
                async with session.get(
                    urljoin(self.base_url, '/api/v1/sse/health')
                ) as response:
                    response.raise_for_status()
                    return await response.json()
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Health check failed: {e}")
                raise
    
    async def stream_generate(
        self,
        prompt: str,
        max_tokens: int = 100,
        temperature: float = 0.7,
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream text generation from SSE server.
        
        Args:
            prompt: Input prompt for generation
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Yields:
            Dictionary containing streaming response chunks
        """
        payload = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'stream': True,
            **kwargs
        }
        
        self.logger.info(f"Starting stream generation for prompt: {prompt[:50]}...")
        
        async with self._create_session() as session:
            try:
                async with session.post(
                    urljoin(self.base_url, '/api/v1/sse/generate'),
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        
                        # Skip empty lines and comments
                        if not line or line.startswith('#'):
                            continue
                        
                        # Parse SSE format
                        if line.startswith('data: '):
                            data = line[6:]  # Remove 'data: ' prefix
                            
                            # Handle special SSE messages
                            if data == '[DONE]':
                                self.logger.info("Stream generation completed")
                                break
                            
                            try:
                                event_data = json.loads(data)
                                yield event_data
                            except json.JSONDecodeError:
                                self.logger.warning(f"Failed to parse SSE data: {data}")
                                continue
                                
            except aiohttp.ClientError as e:
                self.logger.error(f"Stream generation failed: {e}")
                raise
    
    async def stream_chat(
        self,
        messages: list,
        max_tokens: int = 150,
        temperature: float = 0.7,
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream chat completion from SSE server.
        
        Args:
            messages: List of message objects
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Yields:
            Dictionary containing streaming chat response chunks
        """
        payload = {
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'stream': True,
            **kwargs
        }
        
        self.logger.info(f"Starting stream chat with {len(messages)} messages")
        
        async with self._create_session() as session:
            try:
                async with session.post(
                    urljoin(self.base_url, '/api/v1/sse/chat'),
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        
                        if not line or line.startswith('#'):
                            continue
                        
                        if line.startswith('data: '):
                            data = line[6:]
                            
                            if data == '[DONE]':
                                self.logger.info("Stream chat completed")
                                break
                            
                            try:
                                event_data = json.loads(data)
                                yield event_data
                            except json.JSONDecodeError:
                                self.logger.warning(f"Failed to parse SSE data: {data}")
                                continue
                                
            except aiohttp.ClientError as e:
                self.logger.error(f"Stream chat failed: {e}")
                raise
    
    async def subscribe_events(
        self,
        event_types: list = None,
        filters: Dict[str, Any] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Subscribe to real-time events from SSE server.
        
        Args:
            event_types: List of event types to subscribe to
            filters: Additional filters for events
            
        Yields:
            Dictionary containing event data
        """
        payload = {
            'event_types': event_types or ['*'],
            'filters': filters or {}
        }
        
        self.logger.info(f"Subscribing to events: {event_types}")
        
        async with self._create_session() as session:
            try:
                async with session.post(
                    urljoin(self.base_url, '/api/v1/sse/subscribe'),
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        
                        if not line:
                            continue
                        
                        # Handle different SSE event types
                        if line.startswith('event: '):
                            event_type = line[7:]
                            continue
                        elif line.startswith('data: '):
                            data = line[6:]
                            
                            try:
                                event_data = json.loads(data)
                                event_data['event_type'] = event_type if 'event_type' in locals() else 'message'
                                yield event_data
                            except json.JSONDecodeError:
                                self.logger.warning(f"Failed to parse event data: {data}")
                                continue
                                
            except aiohttp.ClientError as e:
                self.logger.error(f"Event subscription failed: {e}")
                raise
    
    async def get_active_streams(self) -> Dict[str, Any]:
        """
        Get information about active streams.
        
        Returns:
            Dictionary containing active stream information
        """
        async with self._create_session() as session:
            try:
                async with session.get(
                    urljoin(self.base_url, '/api/v1/sse/streams')
                ) as response:
                    response.raise_for_status()
                    return await response.json()
                    
            except aiohttp.ClientError as e:
                self.logger.error(f"Failed to get active streams: {e}")
                raise


async def main():
    """Example usage of the MCP SSE client."""
    # Initialize client
    client = MCPSSEClient(
        base_url=os.getenv('MCP_GATEWAY_URL', 'http://localhost:8080'),
        api_key=os.getenv('MCP_API_KEY')
    )
    
    try:
        # Health check
        print("=== Health Check ===")
        health = await client.health_check()
        print(f"Health Status: {json.dumps(health, indent=2)}")
        
        # Stream text generation
        print("\n=== Streaming Text Generation ===")
        full_response = ""
        async for chunk in client.stream_generate(
            prompt="Write a short story about a robot learning to paint:",
            max_tokens=200,
            temperature=0.8
        ):
            if 'text' in chunk:
                text_chunk = chunk['text']
                print(text_chunk, end='', flush=True)
                full_response += text_chunk
        print(f"\n\nFull response length: {len(full_response)} characters")
        
        # Stream chat
        print("\n=== Streaming Chat ===")
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": "Explain how Docker networking works"}
        ]
        
        chat_response = ""
        async for chunk in client.stream_chat(messages=messages, max_tokens=300):
            if 'delta' in chunk and 'content' in chunk['delta']:
                content = chunk['delta']['content']
                print(content, end='', flush=True)
                chat_response += content
        print(f"\n\nChat response length: {len(chat_response)} characters")
        
        # Event subscription (run for a short time)
        print("\n=== Event Subscription ===")
        print("Subscribing to events for 10 seconds...")
        
        event_count = 0
        async for event in client.subscribe_events(event_types=['system', 'user']):
            print(f"Event: {event.get('event_type')} - {event.get('message', event)}")
            event_count += 1
            
            # Limit to avoid infinite loop in demo
            if event_count >= 5:
                break
        
        # Get active streams
        print(f"\n=== Active Streams ===")
        streams = await client.get_active_streams()
        print(f"Active Streams: {json.dumps(streams, indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Example environment variables
    print("MCP SSE Client Example")
    print("======================")
    print("Environment variables:")
    print(f"MCP_GATEWAY_URL: {os.getenv('MCP_GATEWAY_URL', 'http://localhost:8080')}")
    print(f"MCP_API_KEY: {'Set' if os.getenv('MCP_API_KEY') else 'Not set'}")
    print()
    
    # Run the async main function
    asyncio.run(main())