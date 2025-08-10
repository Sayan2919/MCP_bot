import math
import re
from typing import Dict, Any, Union
from dataclasses import dataclass


@dataclass
class CalculationResult:
    """Data class to hold calculation results"""
    expression: str
    result: Union[float, str]
    operation: str
    timestamp: str
    success: bool
    error_message: str = ""


class CalculatorTool:
    """MCP tool for mathematical calculations and unit conversions"""

    def __init__(self):
        # Supported mathematical operations
        self.operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else None,
            '**': lambda x, y: x ** y,
            '%': lambda x, y: x % y if y != 0 else None,
            '//': lambda x, y: x // y if y != 0 else None
        }
        
        # Scientific functions
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sqrt': math.sqrt,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'abs': abs,
            'floor': math.floor,
            'ceil': math.ceil,
            'round': round,
            'factorial': math.factorial
        }

    def calculate(self, expression: str) -> CalculationResult:
        """
        Evaluate a mathematical expression
        
        Args:
            expression: Mathematical expression as string (e.g., "2 + 3 * 4")
            
        Returns:
            CalculationResult object containing the result
        """
        try:
            # Clean the expression
            clean_expr = self._clean_expression(expression)
            
            # Validate the expression
            if not self._validate_expression(clean_expr):
                return CalculationResult(
                    expression=expression,
                    result="",
                    operation="validation",
                    timestamp=self._get_timestamp(),
                    success=False,
                    error_message="Invalid expression format"
                )
            
            # Evaluate the expression
            result = self._evaluate_expression(clean_expr)
            
            if result is None:
                return CalculationResult(
                    expression=expression,
                    result="",
                    operation="calculation",
                    timestamp=self._get_timestamp(),
                    success=False,
                    error_message="Division by zero or invalid operation"
                )
            
            return CalculationResult(
                expression=expression,
                result=result,
                operation="calculation",
                timestamp=self._get_timestamp(),
                success=True
            )
            
        except Exception as e:
            return CalculationResult(
                expression=expression,
                result="",
                operation="calculation",
                timestamp=self._get_timestamp(),
                success=False,
                error_message=str(e)
            )

    def scientific_function(self, function_name: str, value: float) -> CalculationResult:
        """
        Apply a scientific function to a value
        
        Args:
            function_name: Name of the scientific function
            value: Input value for the function
            
        Returns:
            CalculationResult object containing the result
        """
        try:
            if function_name not in self.functions:
                return CalculationResult(
                    expression=f"{function_name}({value})",
                    result="",
                    operation="scientific_function",
                    timestamp=self._get_timestamp(),
                    success=False,
                    error_message=f"Unknown function: {function_name}"
                )
            
            # Handle special cases
            if function_name == 'sqrt' and value < 0:
                return CalculationResult(
                    expression=f"{function_name}({value})",
                    result="",
                    operation="scientific_function",
                    timestamp=self._get_timestamp(),
                    success=False,
                    error_message="Cannot calculate square root of negative number"
                )
            
            if function_name == 'log' and value <= 0:
                return CalculationResult(
                    expression=f"{function_name}({value})",
                    result="",
                    operation="scientific_function",
                    timestamp=self._get_timestamp(),
                    success=False,
                    error_message="Cannot calculate logarithm of non-positive number"
                )
            
            if function_name == 'factorial' and (value < 0 or value != int(value)):
                return CalculationResult(
                    expression=f"{function_name}({value})",
                    result="",
                    operation="scientific_function",
                    timestamp=self._get_timestamp(),
                    success=False,
                    error_message="Factorial is only defined for non-negative integers"
                )
            
            result = self.functions[function_name](value)
            
            return CalculationResult(
                expression=f"{function_name}({value})",
                result=result,
                operation="scientific_function",
                timestamp=self._get_timestamp(),
                success=True
            )
            
        except Exception as e:
            return CalculationResult(
                expression=f"{function_name}({value})",
                result="",
                operation="scientific_function",
                timestamp=self._get_timestamp(),
                success=False,
                error_message=str(e)
            )

    def unit_conversion(self, value: float, from_unit: str, to_unit: str) -> CalculationResult:
        """
        Convert between different units
        
        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            CalculationResult object containing the converted value
        """
        try:
            # Temperature conversions
            if from_unit.lower() in ['c', 'celsius'] and to_unit.lower() in ['f', 'fahrenheit']:
                result = (value * 9/5) + 32
                operation = f"Temperature conversion: {value}°C to °F"
            elif from_unit.lower() in ['f', 'fahrenheit'] and to_unit.lower() in ['c', 'celsius']:
                result = (value - 32) * 5/9
                operation = f"Temperature conversion: {value}°F to °C"
            elif from_unit.lower() in ['c', 'celsius'] and to_unit.lower() in ['k', 'kelvin']:
                result = value + 273.15
                operation = f"Temperature conversion: {value}°C to K"
            elif from_unit.lower() in ['k', 'kelvin'] and to_unit.lower() in ['c', 'celsius']:
                result = value - 273.15
                operation = f"Temperature conversion: {value}K to °C"
            
            # Length conversions
            elif from_unit.lower() in ['m', 'meters'] and to_unit.lower() in ['ft', 'feet']:
                result = value * 3.28084
                operation = f"Length conversion: {value}m to ft"
            elif from_unit.lower() in ['ft', 'feet'] and to_unit.lower() in ['m', 'meters']:
                result = value / 3.28084
                operation = f"Length conversion: {value}ft to m"
            elif from_unit.lower() in ['km', 'kilometers'] and to_unit.lower() in ['mi', 'miles']:
                result = value * 0.621371
                operation = f"Length conversion: {value}km to mi"
            elif from_unit.lower() in ['mi', 'miles'] and to_unit.lower() in ['km', 'kilometers']:
                result = value / 0.621371
                operation = f"Length conversion: {value}mi to km"
            
            # Weight conversions
            elif from_unit.lower() in ['kg', 'kilograms'] and to_unit.lower() in ['lbs', 'pounds']:
                result = value * 2.20462
                operation = f"Weight conversion: {value}kg to lbs"
            elif from_unit.lower() in ['lbs', 'pounds'] and to_unit.lower() in ['kg', 'kilograms']:
                result = value / 2.20462
                operation = f"Weight conversion: {value}lbs to kg"
            
            else:
                return CalculationResult(
                    expression=f"{value} {from_unit} to {to_unit}",
                    result="",
                    operation="unit_conversion",
                    timestamp=self._get_timestamp(),
                    success=False,
                    error_message=f"Unsupported conversion: {from_unit} to {to_unit}"
                )
            
            return CalculationResult(
                expression=f"{value} {from_unit} to {to_unit}",
                result=round(result, 6),
                operation=operation,
                timestamp=self._get_timestamp(),
                success=True
            )
            
        except Exception as e:
            return CalculationResult(
                expression=f"{value} {from_unit} to {to_unit}",
                result="",
                operation="unit_conversion",
                timestamp=self._get_timestamp(),
                success=False,
                error_message=str(e)
            )

    def _clean_expression(self, expression: str) -> str:
        """Clean and normalize the mathematical expression"""
        # Remove extra whitespace
        clean = re.sub(r'\s+', '', expression)
        # Replace common mathematical symbols
        clean = clean.replace('×', '*').replace('÷', '/').replace('^', '**')
        return clean

    def _validate_expression(self, expression: str) -> bool:
        """Validate the mathematical expression"""
        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            return False
        
        # Check for valid characters
        valid_chars = set('0123456789+-*/.()^%')
        if not all(c in valid_chars for c in expression):
            return False
        
        # Check for consecutive operators
        if re.search(r'[+\-*/^%]{2,}', expression):
            return False
        
        return True

    def _evaluate_expression(self, expression: str) -> Union[float, None]:
        """Safely evaluate the mathematical expression"""
        try:
            # Replace ^ with ** for exponentiation
            expression = expression.replace('^', '**')
            
            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, {})
            
            # Check if result is a number
            if isinstance(result, (int, float)):
                return float(result)
            else:
                return None
                
        except (SyntaxError, NameError, ZeroDivisionError):
            return None

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_supported_functions(self) -> Dict[str, str]:
        """Get list of supported scientific functions"""
        return {
            "Basic": "+, -, *, /, **, %, //",
            "Scientific": ", ".join(self.functions.keys()),
            "Units": "Temperature (C, F, K), Length (m, ft, km, mi), Weight (kg, lbs)"
        }
