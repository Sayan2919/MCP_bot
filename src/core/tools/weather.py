import os
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
import requests


@dataclass
class WeatherInfo:
    """Data class to hold weather information"""
    location: str
    temperature: float
    feels_like: float
    humidity: int
    description: str
    wind_speed: float
    pressure: int
    visibility: int
    sunrise: str
    sunset: str
    timestamp: str


class WeatherTool:
    """MCP tool for fetching weather information using WeatherAPI.com"""

    def __init__(self):
        self.api_key = os.getenv("WEATHERAPI_KEY")
        self.base_url = os.getenv("WEATHERAPI_BASE_URL")

        if not self.api_key:
            raise ValueError(
                "WEATHERAPI_KEY environment variable not set. "
                "Please set it with your WeatherAPI.com API key."
            )

    def get_current_weather(self, location: str, units: str = "metric") -> WeatherInfo:
        """
        Get current weather for a specific location using WeatherAPI.com
        
        Args:
            location: City name, coordinates, or city ID
            units: Temperature units ('metric', 'imperial', or 'kelvin')
            
        Returns:
            WeatherInfo object containing weather details
        """
        try:
            # Fetch current weather using WeatherAPI.com
            weather_url = f"{self.base_url}/current.json"
            params = {
                "key": self.api_key,
                "q": location,
                "aqi": "no"  # Disable air quality data for simplicity
            }

            response = requests.get(weather_url, params=params, timeout=60)
            response.raise_for_status()
            weather_data = response.json()

            return self._parse_weather_data(weather_data, location)
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch weather data: {str(e)}") from e
        except Exception as e:
            raise Exception(f"Error getting weather: {str(e)}") from e

    def get_weather_forecast(
        self,
        location: str,
        days: int = 5,
        units: str = "metric"
        ) -> Dict[str, Any]:
        """
        Get weather forecast for a specific location using WeatherAPI.com
        
        Args:
            location: City name, coordinates, or city ID
            days: Number of days for forecast (1-14, WeatherAPI.com supports up to 14 days)
            units: Temperature units ('metric', 'imperial', or 'kelvin')
            
        Returns:
            Dictionary containing forecast data
        """
        try:
            # Validate days parameter (WeatherAPI.com supports 1-14 days)
            if not 1 <= days <= 14:
                raise ValueError("Forecast days must be between 1 and 14")

            # Fetch forecast using WeatherAPI.com
            forecast_url = f"{self.base_url}/forecast.json"
            params = {
                "key": self.api_key,
                "q": location,
                "days": days,
                "aqi": "no",  # Disable air quality data for simplicity
                "alerts": "no"  # Disable alerts for simplicity
            }

            response = requests.get(forecast_url, params=params, timeout=60)
            response.raise_for_status()
            forecast_data = response.json()
            return self._parse_forecast_data(forecast_data, location, days)
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch forecast data: {str(e)}") from e
        except Exception as e:
            raise Exception(f"Error getting forecast: {str(e)}") from e

    def _get_coordinates(self, location: str) -> Optional[Dict[str, float]]:
        """Get coordinates for a location using WeatherAPI.com Search API"""
        try:
            search_url = f"{self.base_url}/search.json"
            params = {
                "key": self.api_key,
                "q": location
            }

            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data and len(data) > 0:
                return {
                    "lat": data[0]["lat"],
                    "lon": data[0]["lon"]
                }
            return None

        except Exception:
            return None

    def _parse_weather_data(self, weather_data: Dict[str, Any], location: str) -> WeatherInfo:
        """Parse WeatherAPI.com weather response into WeatherInfo object"""
        current = weather_data.get("current", {})
        location_info = weather_data.get("location", {})
        
        # Convert temperature based on units (WeatherAPI.com returns Celsius by default)
        temp_c = current.get("temp_c", 0)
        feels_like_c = current.get("feelslike_c", 0)
        
        # Convert wind speed (WeatherAPI.com returns km/h)
        wind_kph = current.get("wind_kph", 0)
        
        # Convert pressure (WeatherAPI.com returns mb)
        pressure_mb = current.get("pressure_mb", 0)
        
        # Convert visibility (WeatherAPI.com returns km)
        vis_km = current.get("vis_km", 0)

        return WeatherInfo(
            location=location_info.get("name", location),
            temperature=temp_c,
            feels_like=feels_like_c,
            humidity=current.get("humidity", 0),
            description=current.get("condition", {}).get("text", ""),
            wind_speed=wind_kph,
            pressure=pressure_mb,
            visibility=vis_km,
            sunrise=location_info.get("localtime", ""),  # WeatherAPI.com doesn't provide sunrise/sunset in current weather
            sunset=location_info.get("localtime", ""),  # We'll need to use astronomy API for this
            timestamp=current.get("last_updated", "")
        )

    def _parse_forecast_data(
        self,
        forecast_data: Dict[str, Any],
        location: str,
        days: int) -> Dict[str, Any]:
        """Parse WeatherAPI.com forecast response into structured format"""
        forecasts = []
        forecast_days = forecast_data.get("forecast", {}).get("forecastday", [])

        for day_data in forecast_days[:days]:
            date = day_data.get("date", "")
            day_info = day_data.get("day", {})
            astro = day_data.get("astro", {})
            
            # Get hourly data for the day
            hour_data = day_data.get("hour", [])
            
            # Create daily summary
            daily_forecast = {
                "date": date,
                "max_temp": day_info.get("maxtemp_c", 0),
                "min_temp": day_info.get("mintemp_c", 0),
                "avg_temp": day_info.get("avgtemp_c", 0),
                "max_humidity": day_info.get("maxhumidity", 0),
                "min_humidity": day_info.get("minhumidity", 0),
                "avg_humidity": day_info.get("avghumidity", 0),
                "description": day_info.get("condition", {}).get("text", ""),
                "max_wind_kph": day_info.get("maxwind_kph", 0),
                "total_precip_mm": day_info.get("totalprecip_mm", 0),
                "sunrise": astro.get("sunrise", ""),
                "sunset": astro.get("sunset", ""),
                "hourly_data": []
            }
            
            # Add hourly data if available
            for hour in hour_data:
                hourly_forecast = {
                    "time": hour.get("time", ""),
                    "temperature": hour.get("temp_c", 0),
                    "feels_like": hour.get("feelslike_c", 0),
                    "humidity": hour.get("humidity", 0),
                    "description": hour.get("condition", {}).get("text", ""),
                    "wind_kph": hour.get("wind_kph", 0),
                    "pressure_mb": hour.get("pressure_mb", 0),
                    "precip_mm": hour.get("precip_mm", 0),
                    "visibility_km": hour.get("vis_km", 0)
                }
                daily_forecast["hourly_data"].append(hourly_forecast)
            
            forecasts.append(daily_forecast)

        return {
            "location": forecast_data.get("location", {}).get("name", location),
            "forecast_days": days,
            "forecasts": forecasts,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
