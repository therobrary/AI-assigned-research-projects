"""
title: Your Tool Name
author: Your Name
author_url: https://github.com/yourusername
funding_url: https://github.com/sponsors/yourusername
version: 1.0.0
"""

from typing import Callable, Any, Dict, List, Optional
import asyncio
import aiohttp
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Tools:
    def __init__(self):
        """
        Initialize your tool
        
        Set up any configuration, API keys, or initial state here.
        """
        # Enable citations if your tool returns external content
        self.citation = False
        
        # Configuration from environment variables
        self.api_key = os.getenv("YOUR_API_KEY")
        self.base_url = os.getenv("YOUR_API_URL", "https://api.example.com")
        self.timeout = 30
        
        # Validate required configuration
        if not self.api_key:
            logger.warning("YOUR_API_KEY environment variable not set")
    
    async def your_main_function(
        self,
        input_parameter: str,
        optional_parameter: str = "default_value",
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Your main tool function - this will appear in the OpenWebUI interface
        
        :param input_parameter: Description of the main input parameter
        :param optional_parameter: Description of optional parameter with default
        :param __user__: User information (automatically provided by OpenWebUI)
        :param __event_emitter__: Function to emit real-time updates (automatically provided)
        :return: The result of your tool operation
        """
        
        # Validate inputs
        if not input_parameter.strip():
            return "Error: Input parameter cannot be empty"
        
        # Log the operation
        user_id = __user__.get("id", "unknown") if __user__ else "unknown"
        logger.info(f"Tool function called by user {user_id}")
        
        try:
            # Send status update to user
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "Starting processing..."}
                })
            
            # Your main logic goes here
            result = await self._process_input(input_parameter, optional_parameter, __event_emitter__)
            
            # Final status update
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "Processing complete! ✅"}
                })
            
            return result
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(f"Tool error: {error_msg}")
            
            if __event_emitter__:
                await __event_emitter__({
                    "type": "error",
                    "data": {"description": error_msg}
                })
            
            return error_msg
    
    async def _process_input(
        self, 
        input_data: str, 
        option: str,
        __event_emitter__: Callable[[dict], Any] = None
    ) -> str:
        """
        Private method to handle the main processing logic
        
        :param input_data: The input to process
        :param option: Processing option
        :param __event_emitter__: Event emitter for status updates
        :return: Processed result
        """
        
        # Update progress
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": "Processing input data..."}
            })
        
        # Simulate some processing time
        await asyncio.sleep(1)
        
        # Your processing logic here
        # This is where you'd call external APIs, process data, etc.
        
        # Example: Simple text processing
        processed = f"Processed '{input_data}' with option '{option}'"
        
        return processed
    
    async def _call_external_api(self, endpoint: str, data: Dict) -> Dict:
        """
        Helper method for making external API calls
        
        :param endpoint: API endpoint to call
        :param data: Data to send to the API
        :return: API response data
        """
        
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "OpenWebUI-Tool/1.0"
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 401:
                        raise Exception("Invalid API key")
                    else:
                        raise Exception(f"API returned status {response.status}")
                        
            except aiohttp.ClientError as e:
                raise Exception(f"Failed to connect to API: {str(e)}")
    
    def _validate_input(self, input_data: str) -> bool:
        """
        Validate input data
        
        :param input_data: Data to validate
        :return: True if valid, False otherwise
        """
        
        if not input_data or not input_data.strip():
            return False
        
        # Add your validation logic here
        # Examples:
        # - Check string length
        # - Validate format (email, URL, etc.)
        # - Check against allowed values
        
        return True
    
    def _format_output(self, data: Dict) -> str:
        """
        Format output data for display
        
        :param data: Data to format
        :return: Formatted string
        """
        
        # Format your output here
        # Examples:
        # - Create markdown tables
        # - Add emojis and formatting
        # - Structure data clearly
        
        output = "# Tool Results\n\n"
        
        for key, value in data.items():
            output += f"**{key.title()}:** {value}\n"
        
        return output
    
    # Optional: Add more functions that will appear as separate tools
    async def helper_function(
        self,
        simple_input: str,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        A simpler helper function
        
        :param simple_input: Simple input parameter
        :param __user__: User information
        :param __event_emitter__: Event emitter
        :return: Simple result
        """
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": "Processing helper function..."}
            })
        
        result = f"Helper result for: {simple_input}"
        
        return result