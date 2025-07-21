"""Base tool interface for AI agent tools."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):
    """
    Abstract base class for agent tools.
    
    Tools extend the agent's capabilities by providing access to external
    functions, APIs, databases, or other services.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, parameters: Dict[str, Any]) -> Any:
        """
        Execute the tool with given parameters.
        
        Args:
            parameters: Dictionary of parameters for tool execution
            
        Returns:
            The result of tool execution
        """
        pass
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate parameters before execution.
        
        Args:
            parameters: Dictionary of parameters to validate
            
        Returns:
            True if parameters are valid, False otherwise
        """
        return True  # Default implementation accepts any parameters
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Get the tool's parameter schema.
        
        Returns:
            JSON schema describing the tool's parameters
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }