#!/usr/bin/env python3
"""
Example usage of the WeatherAPI.com weather tool

Before running this script, make sure to:
1. Sign up at https://www.weatherapi.com/ to get your API key
2. Set the environment variable: export WEATHERAPI_KEY="your_api_key_here"
"""

import os
import sys

# Add the project root to Python path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.tools.weather import WeatherTool


def main():
    """Example usage of the WeatherTool class"""
    
    # Check if API key is set
    if not os.getenv("WEATHERAPI_KEY"):
        print("❌ Error: WEATHERAPI_KEY environment variable not set")
        print("Please sign up at https://www.weatherapi.com/ and set your API key:")
        print("export WEATHERAPI_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize the weather tool
        weather_tool = WeatherTool()
        print("✅ Weather tool initialized successfully")
        
        # Example 1: Get current weather for London
        print("\n🌤️  Getting current weather for London...")
        current_weather = weather_tool.get_current_weather("London")
        print(f"Location: {current_weather.location}")
        print(f"Temperature: {current_weather.temperature}°C")
        print(f"Feels like: {current_weather.feels_like}°C")
        print(f"Humidity: {current_weather.humidity}%")
        print(f"Description: {current_weather.description}")
        print(f"Wind Speed: {current_weather.wind_speed} km/h")
        print(f"Pressure: {current_weather.pressure} mb")
        print(f"Visibility: {current_weather.visibility} km")
        print(f"Last Updated: {current_weather.timestamp}")
        
        # Example 2: Get 3-day forecast for New York
        print("\n📅 Getting 3-day forecast for New York...")
        forecast = weather_tool.get_weather_forecast("New York", days=3)
        print(f"Location: {forecast['location']}")
        print(f"Forecast Days: {forecast['forecast_days']}")
        
        for day_forecast in forecast['forecasts']:
            print(f"\n📆 {day_forecast['date']}:")
            print(f"   High: {day_forecast['max_temp']}°C, Low: {day_forecast['min_temp']}°C")
            print(f"   Description: {day_forecast['description']}")
            print(f"   Humidity: {day_forecast['avg_humidity']}%")
            print(f"   Wind: {day_forecast['max_wind_kph']} km/h")
            print(f"   Sunrise: {day_forecast['sunrise']}, Sunset: {day_forecast['sunset']}")
            
            # Show first few hourly forecasts
            if day_forecast['hourly_data']:
                print("   Hourly (first 3):")
                for hour in day_forecast['hourly_data'][:3]:
                    print(f"     {hour['time']}: {hour['temperature']}°C, {hour['description']}")
        
        # Example 3: Search for locations
        print("\n🔍 Searching for locations containing 'Paris'...")
        coords = weather_tool._get_coordinates("Paris")
        if coords:
            print(f"Found coordinates: {coords}")
        else:
            print("No coordinates found")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
