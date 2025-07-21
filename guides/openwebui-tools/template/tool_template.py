"""
title: My Custom Tool
author: Your Name
author_url: https://your-website.com
funding_url: https://github.com/sponsors/yourusername
version: 0.1.0
license: MIT
"""

import requests
import os
import json
from typing import Callable, Any, Dict, List, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Tools:
    def __init__(self):
        """
        Initialize the tool.
        
        Set up any configuration, API clients, or persistent data here.
        """
        self.name = "my_custom_tool"
        self.description = "Brief description of what this tool does"
        
        # Configuration
        self.api_key = os.getenv("MY_API_KEY")  # Get API key from environment
        self.base_url = "https://api.example.com"
        
        # HTTP session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "OpenWebUI-MyTool/1.0",
            "Accept": "application/json"
        })
        
        # Optional: Initialize any caches or state
        self._cache = {}

    def my_action(
        self,
        required_param: str,
        optional_param: str = "default_value",
        number_param: int = 10,
        boolean_param: bool = False,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Description of what this action does.
        
        This is the main action that users will interact with. Provide a clear
        description of the action's purpose and expected behavior.
        
        :param required_param: Description of the required parameter
        :param optional_param: Description of optional parameter (default: "default_value")
        :param number_param: Numeric parameter description (default: 10)
        :param boolean_param: Boolean parameter description (default: False)
        :return: Description of what the action returns
        """
        # Input validation
        if not required_param or len(required_param.strip()) == 0:
            return "Error: Required parameter cannot be empty"
        
        if number_param < 1 or number_param > 100:
            return "Error: Number parameter must be between 1 and 100"
        
        # Emit status update (optional)
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": f"Processing {required_param}...", "done": False},
            })
        
        try:
            # Your main logic here
            result = self._process_data(required_param, optional_param, number_param, boolean_param)
            
            # Success status update
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": "Processing completed successfully", "done": True},
                })
            
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error: {str(e)}"
            logger.error(error_msg)
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return f"Error: {error_msg}"
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return f"Error: {error_msg}"

    def secondary_action(
        self,
        data: str,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Secondary action example.
        
        You can have multiple actions in a single tool. Each action should be
        a separate method with clear documentation.
        
        :param data: Input data to process
        :return: Processed result
        """
        if not data:
            return "Error: Data parameter is required"
        
        try:
            # Simple processing example
            result = f"Processed: {data.upper()}"
            
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": "Secondary action completed", "done": True},
                })
            
            return result
            
        except Exception as e:
            error_msg = f"Error in secondary action: {str(e)}"
            logger.error(error_msg)
            return f"Error: {error_msg}"

    def get_status(
        self,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Get tool status and configuration.
        
        This is a utility action that can help with debugging and
        understanding the tool's current state.
        
        :return: Status information
        """
        status = {
            "tool_name": self.name,
            "description": self.description,
            "api_configured": bool(self.api_key),
            "cache_size": len(self._cache),
        }
        
        result = "## Tool Status\n\n"
        for key, value in status.items():
            result += f"**{key.replace('_', ' ').title()}:** {value}\n"
        
        return result

    def _process_data(self, required_param: str, optional_param: str, number_param: int, boolean_param: bool) -> str:
        """
        Private method for processing data.
        
        Use private methods (starting with _) for internal logic that
        shouldn't be directly accessible to users.
        """
        # Example processing logic
        result = f"Processing '{required_param}' with options: "
        result += f"optional='{optional_param}', number={number_param}, boolean={boolean_param}"
        
        # Simulate some work
        import time
        time.sleep(0.1)
        
        # Example API call (if needed)
        if self.api_key:
            api_result = self._make_api_call(required_param)
            if api_result:
                result += f"\nAPI Response: {api_result}"
        
        return result

    def _make_api_call(self, data: str) -> Optional[Dict]:
        """
        Example API call method.
        
        Implement your external API integration here.
        """
        try:
            # Example API call
            params = {
                "query": data,
                "api_key": self.api_key
            }
            
            response = self.session.get(
                f"{self.base_url}/endpoint",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {str(e)}")
            return None

    def _validate_input(self, input_string: str, max_length: int = 1000) -> str:
        """
        Example input validation method.
        
        Always validate user inputs to prevent issues.
        """
        if not input_string:
            raise ValueError("Input cannot be empty")
        
        input_string = input_string.strip()
        
        if len(input_string) > max_length:
            raise ValueError(f"Input too long (max {max_length} characters)")
        
        # Add any other validation logic here
        return input_string

    def _format_response(self, data: Dict) -> str:
        """
        Example response formatting method.
        
        Format your responses consistently for better user experience.
        """
        if not data:
            return "No data available"
        
        formatted = "## Results\n\n"
        
        for key, value in data.items():
            formatted += f"**{key.replace('_', ' ').title()}:** {value}\n"
        
        return formatted