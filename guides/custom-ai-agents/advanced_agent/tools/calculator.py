"""Calculator tool for mathematical operations."""

import ast
import operator
from typing import Dict, Any, Union
from .base_tool import BaseTool


class CalculatorTool(BaseTool):
    """
    A safe calculator tool for basic mathematical operations.
    
    Supports arithmetic operations like +, -, *, /, ** (power), and parentheses.
    Uses AST evaluation for safety (no exec/eval of arbitrary code).
    """
    
    # Supported operations
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.BitXor: operator.xor,
        ast.USub: operator.neg,
    }
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Performs safe mathematical calculations. Supports +, -, *, /, ** (power), and parentheses."
        )
    
    def execute(self, parameters: Dict[str, Any]) -> Union[float, str]:
        """
        Execute a mathematical calculation.
        
        Args:
            parameters: Dictionary containing 'expression' key with math expression
            
        Returns:
            The calculation result or error message
        """
        expression = parameters.get('expression', '').strip()
        
        if not expression:
            return "Error: No expression provided"
        
        try:
            result = self._safe_eval(expression)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _safe_eval(self, expression: str) -> float:
        """
        Safely evaluate a mathematical expression using AST.
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            The calculated result
        """
        try:
            node = ast.parse(expression, mode='eval')
            return self._eval_node(node.body)
        except Exception as e:
            raise ValueError(f"Invalid expression: {expression}")
    
    def _eval_node(self, node) -> float:
        """Recursively evaluate AST nodes."""
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = self.operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operation: {type(node.op)}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            op = self.operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operation: {type(node.op)}")
            return op(operand)
        else:
            raise ValueError(f"Unsupported node type: {type(node)}")
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate that expression parameter is provided."""
        return 'expression' in parameters and isinstance(parameters['expression'], str)
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the tool's parameter schema."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')"
                    }
                },
                "required": ["expression"]
            }
        }