"""
title: Hello World Tool
author: OpenWebUI Guide
author_url: https://github.com/therobrary/AI-assigned-research-projects
version: 1.0.0
"""

from typing import Callable, Any
import asyncio


class Tools:
    def __init__(self):
        self.citation = False
        
    async def hello_world(
        self,
        name: str,
        __user__: dict,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        A simple hello world function that greets the user
        
        :param name: The name to greet
        :param __user__: User information
        :param __event_emitter__: Event emitter for real-time updates
        :return: A greeting message
        """
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status", 
                "data": {"description": "Generating personalized greeting..."}
            })
        
        # Simulate some processing time
        await asyncio.sleep(1)
        
        user_id = __user__.get("id", "unknown")
        user_role = __user__.get("role", "user")
        
        greeting = f"Hello, {name}! 👋\n\n"
        greeting += f"Welcome to OpenWebUI tools!\n"
        greeting += f"User ID: {user_id}\n"
        greeting += f"Role: {user_role}\n"
        greeting += f"This is a demonstration of a simple OpenWebUI tool."
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status", 
                "data": {"description": "Greeting complete! ✅"}
            })
        
        return greeting
    
    async def echo_message(
        self,
        message: str,
        times: int = 1,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Echo a message a specified number of times
        
        :param message: The message to echo
        :param times: Number of times to repeat the message (default: 1, max: 10)
        :param __user__: User information
        :param __event_emitter__: Event emitter for real-time updates
        :return: The echoed message
        """
        
        # Validate input
        if times < 1:
            return "Error: Number of times must be at least 1"
        if times > 10:
            return "Error: Maximum 10 repetitions allowed"
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": f"Echoing message {times} time(s)..."}
            })
        
        result = []
        for i in range(times):
            result.append(f"{i+1}. {message}")
            
            # Add a small delay for demonstration
            if times > 1:
                await asyncio.sleep(0.5)
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {"description": "Echo complete! 🔊"}
            })
        
        return "\n".join(result)