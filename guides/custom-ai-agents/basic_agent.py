#!/usr/bin/env python3
"""
Simple AI Agent - A minimal implementation in under 50 lines of code.

This example demonstrates how to build a basic conversational AI agent
with memory persistence and error handling using minimal dependencies.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv


class SimpleAgent:
    def __init__(self, system_prompt="You are a helpful AI assistant."):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.messages = [{"role": "system", "content": system_prompt}]
    
    def chat(self, user_input):
        """Send a message to the agent and get a response."""
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": assistant_message})
            return assistant_message
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def save_memory(self, filename="memory.json"):
        """Save conversation history to file."""
        with open(filename, 'w') as f:
            json.dump(self.messages, f, indent=2)
    
    def load_memory(self, filename="memory.json"):
        """Load conversation history from file."""
        try:
            with open(filename, 'r') as f:
                self.messages = json.load(f)
        except FileNotFoundError:
            pass  # Use default system prompt if no memory file exists


if __name__ == "__main__":
    # Example usage
    agent = SimpleAgent("You are a helpful coding assistant who provides concise, accurate answers.")
    agent.load_memory()
    
    print("Simple AI Agent (type 'quit' to exit)")
    print("=" * 40)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            agent.save_memory()
            print("Goodbye! Memory saved.")
            break
        
        response = agent.chat(user_input)
        print(f"Agent: {response}")