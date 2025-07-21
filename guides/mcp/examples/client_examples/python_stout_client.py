#!/usr/bin/env python3
"""
MCP Stout Server Client Example

This script demonstrates how to connect to and interact with an MCP Stout server
through the MCP Gateway. Stout servers are designed for high-throughput
request/response processing.

Usage:
    python python_stout_client.py
"""

import os
import json
import time
import requests
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin


class MCPStoutClient:
    """Client for interacting with MCP Stout servers via the Gateway."""
    
    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        api_key: Optional[str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        """
        Initialize the MCP Stout client.
        
        Args:
            base_url: Base URL of the MCP Gateway
            api_key: API key for authentication
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv('MCP_API_KEY')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Setup session
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            })
        
        # Verify connection
        self._verify_connection()
    
    def _verify_connection(self) -> None:
        """Verify connection to the MCP Gateway."""
        try:
            response = self.session.get(
                urljoin(self.base_url, '/health'),
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            self.logger.info("Successfully connected to MCP Gateway")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to connect to MCP Gateway: {e}")
            raise
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 100,
        temperature: float = 0.7,
        top_p: float = 0.9,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text using the stout server.
        
        Args:
            prompt: Input prompt for generation
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            top_p: Top-p sampling parameter
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing the generated response
        """
        payload = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            **kwargs
        }
        
        self.logger.info(f"Generating text for prompt: {prompt[:50]}...")
        
        try:
            response = self.session.post(
                urljoin(self.base_url, '/api/v1/stout/generate'),
                json=payload,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            result = response.json()
            self.logger.info("Text generation completed successfully")
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to generate text: {e}")
            raise
    
    def chat(
        self,
        messages: list,
        max_tokens: int = 150,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Chat completion using the stout server.
        
        Args:
            messages: List of message objects [{"role": "user", "content": "..."}]
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing the chat response
        """
        payload = {
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': temperature,
            **kwargs
        }
        
        self.logger.info(f"Processing chat with {len(messages)} messages")
        
        try:
            response = self.session.post(
                urljoin(self.base_url, '/api/v1/stout/chat'),
                json=payload,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            result = response.json()
            self.logger.info("Chat completion successful")
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to process chat: {e}")
            raise
    
    def embed(self, text: str) -> Dict[str, Any]:
        """
        Generate embeddings for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Dictionary containing embeddings
        """
        payload = {'text': text}
        
        self.logger.info(f"Generating embeddings for text: {text[:50]}...")
        
        try:
            response = self.session.post(
                urljoin(self.base_url, '/api/v1/stout/embed'),
                json=payload,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            
            result = response.json()
            self.logger.info("Embedding generation completed")
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to generate embeddings: {e}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the stout server.
        
        Returns:
            Dictionary containing health status
        """
        try:
            response = self.session.get(
                urljoin(self.base_url, '/api/v1/stout/health'),
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Health check failed: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get server statistics.
        
        Returns:
            Dictionary containing server stats
        """
        try:
            response = self.session.get(
                urljoin(self.base_url, '/api/v1/stout/stats'),
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to get stats: {e}")
            raise
    
    def close(self):
        """Close the client session."""
        self.session.close()
        self.logger.info("Client session closed")


def main():
    """Example usage of the MCP Stout client."""
    # Initialize client
    client = MCPStoutClient(
        base_url=os.getenv('MCP_GATEWAY_URL', 'http://localhost:8080'),
        api_key=os.getenv('MCP_API_KEY')
    )
    
    try:
        # Health check
        print("=== Health Check ===")
        health = client.health_check()
        print(f"Health Status: {json.dumps(health, indent=2)}")
        
        # Simple text generation
        print("\n=== Text Generation ===")
        response = client.generate(
            prompt="Explain the concept of artificial intelligence in simple terms:",
            max_tokens=100,
            temperature=0.7
        )
        print(f"Generated Text: {response.get('text', 'No text generated')}")
        
        # Chat completion
        print("\n=== Chat Completion ===")
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What are the benefits of using Docker containers?"}
        ]
        chat_response = client.chat(messages=messages, max_tokens=150)
        print(f"Chat Response: {chat_response.get('message', {}).get('content', 'No response')}")
        
        # Embeddings
        print("\n=== Text Embeddings ===")
        embed_response = client.embed("Docker containers provide lightweight virtualization")
        embeddings = embed_response.get('embeddings', [])
        print(f"Embedding dimensions: {len(embeddings) if embeddings else 0}")
        
        # Server statistics
        print("\n=== Server Statistics ===")
        stats = client.get_stats()
        print(f"Server Stats: {json.dumps(stats, indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up
        client.close()


if __name__ == "__main__":
    # Example environment variables
    print("MCP Stout Client Example")
    print("========================")
    print("Environment variables:")
    print(f"MCP_GATEWAY_URL: {os.getenv('MCP_GATEWAY_URL', 'http://localhost:8080')}")
    print(f"MCP_API_KEY: {'Set' if os.getenv('MCP_API_KEY') else 'Not set'}")
    print()
    
    main()