from typing import Dict, Any
from fastmcp import FastMCP
from src.core.tools.weather import WeatherTool
from src.core.tools.calculator import CalculatorTool
from src.core.tools.youtube_transcript import YouTubeTranscriptTool

weather_mcp = FastMCP("Weather Bot 🌤️")
calculator_mcp = FastMCP("Calculator Bot 🧮")
youtube_transcript_mcp = FastMCP("YouTube Transcript Bot 🎥")


@weather_mcp.tool
def get_weather(location: str, units: str = "metric") -> Dict[str, Any]:
    """
    Get current weather for a specific location
    
    Args:
        location: City name, state, or country (e.g., "London", "New York, US")
        units: Temperature units - 'metric' (Celsius), 'imperial' (Fahrenheit), or 'kelvin'
    
    Returns:
        Dictionary containing current weather information
    """
    try:
        weather_tool = WeatherTool()
        weather_info = weather_tool.get_current_weather(location, units)
        
        return {
            "success": True,
            "data": {
                "location": weather_info.location,
                "temperature": weather_info.temperature,
                "feels_like": weather_info.feels_like,
                "humidity": weather_info.humidity,
                "description": weather_info.description,
                "wind_speed": weather_info.wind_speed,
                "pressure": weather_info.pressure,
                "visibility": weather_info.visibility,
                "sunrise": weather_info.sunrise,
                "sunset": weather_info.sunset,
                "units": units,
                "timestamp": weather_info.timestamp
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@weather_mcp.tool
def get_weather_forecast(location: str, days: int = 5, units: str = "metric") -> Dict[str, Any]:
    """
    Get weather forecast for a specific location
    
    Args:
        location: City name, state, or country (e.g., "London", "New York, US")
        days: Number of days for forecast (1-14, WeatherAPI.com supports up to 14 days)
        units: Temperature units - 'metric' (Celsius), 'imperial' (Fahrenheit), or 'kelvin'
    
    Returns:
        Dictionary containing weather forecast information
    """
    try:
        if not 1 <= days <= 14:
            return {
                "success": False,
                "error": "Forecast days must be between 1 and 14"
            }
        
        weather_tool = WeatherTool()
        forecast_data = weather_tool.get_weather_forecast(location, days, units)
        
        return {
            "success": True,
            "data": forecast_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@weather_mcp.tool
def search_locations(query: str) -> Dict[str, Any]:
    """
    Search for locations by name
    
    Args:
        query: Location name to search for
    
    Returns:
        Dictionary containing matching locations
    """
    try:
        weather_tool = WeatherTool()
        coords = weather_tool._get_coordinates(query)
        
        if coords:
            return {
                "success": True,
                "data": {
                    "query": query,
                    "coordinates": coords
                }
            }
        else:
            return {
                "success": False,
                "error": f"No locations found for query: {query}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Calculator Tools
@calculator_mcp.tool
def calculate_expression(expression: str) -> Dict[str, Any]:
    """
    Evaluate a mathematical expression
    
    Args:
        expression: Mathematical expression as string (e.g., "2 + 3 * 4", "sin(45)", "sqrt(16)")
    
    Returns:
        Dictionary containing calculation result
    """
    try:
        calculator_tool = CalculatorTool()
        result = calculator_tool.calculate(expression)
        
        if result.success:
            return {
                "success": True,
                "data": {
                    "expression": result.expression,
                    "result": result.result,
                    "operation": result.operation,
                    "timestamp": result.timestamp
                }
            }
        else:
            return {
                "success": False,
                "error": result.error_message
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@calculator_mcp.tool
def apply_scientific_function(function_name: str, value: float) -> Dict[str, Any]:
    """
    Apply a scientific function to a value
    
    Args:
        function_name: Name of the scientific function (e.g., "sin", "cos", "sqrt", "log")
        value: Input value for the function
    
    Returns:
        Dictionary containing function result
    """
    try:
        calculator_tool = CalculatorTool()
        result = calculator_tool.scientific_function(function_name, value)
        
        if result.success:
            return {
                "success": True,
                "data": {
                    "function": f"{function_name}({value})",
                    "result": result.result,
                    "operation": result.operation,
                    "timestamp": result.timestamp
                }
            }
        else:
            return {
                "success": False,
                "error": result.error_message
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@calculator_mcp.tool
def convert_units(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """
    Convert between different units
    
    Args:
        value: Value to convert
        from_unit: Source unit (e.g., "C", "m", "kg")
        to_unit: Target unit (e.g., "F", "ft", "lbs")
    
    Returns:
        Dictionary containing converted value
    """
    try:
        calculator_tool = CalculatorTool()
        result = calculator_tool.unit_conversion(value, from_unit, to_unit)
        
        if result.success:
            return {
                "success": True,
                "data": {
                    "conversion": f"{value} {from_unit} to {to_unit}",
                    "result": result.result,
                    "operation": result.operation,
                    "timestamp": result.timestamp
                }
            }
        else:
            return {
                "success": False,
                "error": result.error_message
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@calculator_mcp.tool
def get_supported_calculator_functions() -> Dict[str, Any]:
    """
    Get list of supported calculator functions and operations
    
    Returns:
        Dictionary containing supported functions and operations
    """
    try:
        calculator_tool = CalculatorTool()
        functions = calculator_tool.get_supported_functions()
        
        return {
            "success": True,
            "data": functions
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# YouTube Transcript Tools
@youtube_transcript_mcp.tool
def generate_youtube_transcript(
    video_url: str,
    model_size: str = "base"
) -> Dict[str, Any]:
    """
    Generate transcript from a YouTube video using Whisper AI
    
    Args:
        video_url: YouTube video URL
        model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
    
    Returns:
        Dictionary containing transcript information
    """
    try:
        transcript_tool = YouTubeTranscriptTool(model_size)
        result = transcript_tool.get_transcript(video_url)
        
        if result.success:
            return {
                "success": True,
                "data": {
                    "video_url": result.video_url,
                    "video_title": result.video_title,
                    "transcript": result.transcript,
                    "model_size": model_size
                }
            }
        else:
            return {
                "success": False,
                "error": result.error_message
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


