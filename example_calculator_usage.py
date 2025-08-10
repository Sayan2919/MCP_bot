#!/usr/bin/env python3
"""
Example usage of the Calculator tool

This script demonstrates the various calculator functions available in the MCP bot.
"""

import os
import sys

# Add the project root to Python path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.tools.calculator import CalculatorTool


def main():
    """Example usage of the CalculatorTool class"""
    
    try:
        # Initialize the calculator tool
        calculator_tool = CalculatorTool()
        print("✅ Calculator tool initialized successfully")
        
        # Example 1: Basic arithmetic calculations
        print("\n🧮 Basic Arithmetic Examples:")
        expressions = [
            "2 + 3 * 4",
            "10 / 2 + 5",
            "2 ** 8",
            "15 % 4",
            "20 // 3"
        ]
        
        for expr in expressions:
            result = calculator_tool.calculate(expr)
            if result.success:
                print(f"  {expr} = {result.result}")
            else:
                print(f"  {expr} = Error: {result.error_message}")
        
        # Example 2: Scientific functions
        print("\n🔬 Scientific Functions Examples:")
        scientific_tests = [
            ("sin", 45),
            ("cos", 60),
            ("sqrt", 16),
            ("log", 100),
            ("factorial", 5),
            ("abs", -42)
        ]
        
        for func_name, value in scientific_tests:
            result = calculator_tool.scientific_function(func_name, value)
            if result.success:
                print(f"  {func_name}({value}) = {result.result}")
            else:
                print(f"  {func_name}({value}) = Error: {result.error_message}")
        
        # Example 3: Unit conversions
        print("\n📏 Unit Conversion Examples:")
        conversions = [
            (25, "C", "F"),      # Celsius to Fahrenheit
            (68, "F", "C"),      # Fahrenheit to Celsius
            (100, "C", "K"),     # Celsius to Kelvin
            (5, "km", "mi"),     # Kilometers to miles
            (10, "m", "ft"),     # Meters to feet
            (70, "kg", "lbs")    # Kilograms to pounds
        ]
        
        for value, from_unit, to_unit in conversions:
            result = calculator_tool.unit_conversion(value, from_unit, to_unit)
            if result.success:
                print(f"  {value} {from_unit} = {result.result} {to_unit}")
            else:
                print(f"  {value} {from_unit} to {to_unit} = Error: {result.error_message}")
        
        # Example 4: Get supported functions
        print("\n📚 Supported Functions:")
        functions = calculator_tool.get_supported_functions()
        for category, funcs in functions.items():
            print(f"  {category}: {funcs}")
        
        # Example 5: Error handling examples
        print("\n⚠️  Error Handling Examples:")
        error_tests = [
            "2 + + 3",           # Invalid expression
            "sqrt(-4)",          # Invalid input for sqrt
            "factorial(-1)",     # Invalid input for factorial
            "unknown_func(5)",   # Unknown function
            "10 / 0"             # Division by zero
        ]
        
        for expr in error_tests:
            if "(" in expr and ")" in expr:
                # It's a function call
                func_name = expr.split("(")[0]
                value = float(expr.split("(")[1].split(")")[0])
                result = calculator_tool.scientific_function(func_name, value)
            else:
                # It's a regular expression
                result = calculator_tool.calculate(expr)
            
            if result.success:
                print(f"  {expr} = {result.result}")
            else:
                print(f"  {expr} = Error: {result.error_message}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
