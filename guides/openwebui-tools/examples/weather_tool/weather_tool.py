"""
title: Weather Tool
author: OpenWebUI Community
author_url: https://github.com/open-webui/open-webui
version: 1.0.0
license: MIT
"""

import requests
import os
import json
from typing import Callable, Any, Dict, Optional
from datetime import datetime, timezone
import time

class Tools:
    def __init__(self):
        self.name = "weather_tool"
        self.description = "Weather information tool using OpenWeatherMap One Call API 3.0"
        
        # API configuration
        self.api_key = self._get_api_key()
        self.base_url = "https://api.openweathermap.org"
        self.geocoding_url = f"{self.base_url}/geo/1.0"
        self.onecall_url = f"{self.base_url}/data/3.0/onecall"
        
        # Request session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "OpenWebUI-Weather/1.0"
        })
        
        # Cache for geocoding results to avoid repeated API calls
        self._geocoding_cache = {}

    def _get_api_key(self) -> Optional[str]:
        """Get OpenWeatherMap API key from environment variables"""
        return os.getenv("OPENWEATHER_API_KEY")

    def _validate_api_key(self) -> bool:
        """Validate that API key is available"""
        return self.api_key is not None and len(self.api_key.strip()) > 0

    def get_current_weather(
        self,
        location: str,
        units: str = "metric",
        include_forecast: bool = False,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Get current weather information for a location.
        
        :param location: City name, state/country (e.g., "London", "New York, NY", "Tokyo, Japan")
        :param units: Temperature units - metric (°C), imperial (°F), or kelvin (default: metric)
        :param include_forecast: Include 24-hour forecast (default: False)
        :return: Current weather information
        """
        if not self._validate_api_key():
            return "Error: OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY environment variable."
        
        if not location or len(location.strip()) == 0:
            return "Error: Location cannot be empty"
        
        if units not in ["metric", "imperial", "kelvin"]:
            units = "metric"
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": f"Getting weather for {location}", "done": False},
            })
        
        try:
            # Get coordinates for the location
            coords = self._get_coordinates(location.strip())
            if not coords:
                return f"Error: Location '{location}' not found"
            
            lat, lon = coords["lat"], coords["lon"]
            location_name = coords.get("display_name", location)
            
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": "Fetching weather data...", "done": False},
                })
            
            # Get weather data
            weather_data = self._get_weather_data(lat, lon, units, include_forecast)
            if not weather_data:
                return "Error: Failed to retrieve weather data"
            
            # Format the response
            result = self._format_current_weather(weather_data, location_name, units, include_forecast)
            
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": "Weather data retrieved successfully", "done": True},
                })
            
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error while fetching weather: {str(e)}"
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return f"Error: {error_msg}"

    def get_weather_forecast(
        self,
        location: str,
        days: int = 5,
        units: str = "metric",
        include_hourly: bool = False,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Get weather forecast for a location.
        
        :param location: City name, state/country (e.g., "London", "New York, NY")
        :param days: Number of forecast days (1-8, default: 5)
        :param units: Temperature units - metric (°C), imperial (°F), or kelvin (default: metric)
        :param include_hourly: Include hourly forecast for next 48 hours (default: False)
        :return: Weather forecast information
        """
        if not self._validate_api_key():
            return "Error: OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY environment variable."
        
        if not location or len(location.strip()) == 0:
            return "Error: Location cannot be empty"
        
        if days < 1 or days > 8:
            days = 5
        
        if units not in ["metric", "imperial", "kelvin"]:
            units = "metric"
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": f"Getting {days}-day forecast for {location}", "done": False},
            })
        
        try:
            # Get coordinates for the location
            coords = self._get_coordinates(location.strip())
            if not coords:
                return f"Error: Location '{location}' not found"
            
            lat, lon = coords["lat"], coords["lon"]
            location_name = coords.get("display_name", location)
            
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": "Fetching forecast data...", "done": False},
                })
            
            # Get weather data
            weather_data = self._get_weather_data(lat, lon, units, True)
            if not weather_data:
                return "Error: Failed to retrieve weather data"
            
            # Format the response
            result = self._format_forecast(weather_data, location_name, units, days, include_hourly)
            
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": "Forecast data retrieved successfully", "done": True},
                })
            
            return result
            
        except Exception as e:
            error_msg = f"Error getting forecast: {str(e)}"
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return f"Error: {error_msg}"

    def get_weather_alerts(
        self,
        location: str,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Get weather alerts for a location.
        
        :param location: City name, state/country
        :return: Weather alerts information
        """
        if not self._validate_api_key():
            return "Error: OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY environment variable."
        
        if not location or len(location.strip()) == 0:
            return "Error: Location cannot be empty"
        
        if __event_emitter__:
            __event_emitter__({
                "type": "status",
                "data": {"description": f"Checking weather alerts for {location}", "done": False},
            })
        
        try:
            # Get coordinates for the location
            coords = self._get_coordinates(location.strip())
            if not coords:
                return f"Error: Location '{location}' not found"
            
            lat, lon = coords["lat"], coords["lon"]
            location_name = coords.get("display_name", location)
            
            # Get weather data with alerts
            weather_data = self._get_weather_data(lat, lon, "metric", False)
            if not weather_data:
                return "Error: Failed to retrieve weather data"
            
            # Format alerts
            result = self._format_alerts(weather_data, location_name)
            
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": "Weather alerts checked", "done": True},
                })
            
            return result
            
        except Exception as e:
            error_msg = f"Error getting weather alerts: {str(e)}"
            if __event_emitter__:
                __event_emitter__({
                    "type": "status",
                    "data": {"description": error_msg, "done": True},
                })
            return f"Error: {error_msg}"

    def _get_coordinates(self, location: str) -> Optional[Dict]:
        """Get latitude and longitude for a location using geocoding API"""
        # Check cache first
        if location in self._geocoding_cache:
            return self._geocoding_cache[location]
        
        params = {
            "q": location,
            "limit": 1,
            "appid": self.api_key
        }
        
        response = self.session.get(f"{self.geocoding_url}/direct", params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return None
        
        result = {
            "lat": data[0]["lat"],
            "lon": data[0]["lon"],
            "display_name": f"{data[0]['name']}"
        }
        
        # Add state/country if available
        if "state" in data[0]:
            result["display_name"] += f", {data[0]['state']}"
        if "country" in data[0]:
            result["display_name"] += f", {data[0]['country']}"
        
        # Cache the result
        self._geocoding_cache[location] = result
        return result

    def _get_weather_data(self, lat: float, lon: float, units: str, include_forecast: bool = False) -> Optional[Dict]:
        """Get weather data from OpenWeatherMap One Call API"""
        exclude_parts = []
        if not include_forecast:
            exclude_parts.extend(["minutely", "hourly", "daily"])
        else:
            exclude_parts.append("minutely")
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": units,
        }
        
        if exclude_parts:
            params["exclude"] = ",".join(exclude_parts)
        
        response = self.session.get(self.onecall_url, params=params, timeout=15)
        response.raise_for_status()
        
        return response.json()

    def _format_current_weather(self, data: Dict, location: str, units: str, include_forecast: bool) -> str:
        """Format current weather data"""
        current = data.get("current", {})
        
        # Temperature units
        temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        speed_unit = "m/s" if units == "metric" else "mph" if units == "imperial" else "m/s"
        
        # Current weather
        weather = current.get("weather", [{}])[0]
        temp = current.get("temp", 0)
        feels_like = current.get("feels_like", 0)
        humidity = current.get("humidity", 0)
        pressure = current.get("pressure", 0)
        wind_speed = current.get("wind_speed", 0)
        wind_deg = current.get("wind_deg", 0)
        visibility = current.get("visibility", 0) / 1000  # Convert to km
        uv_index = current.get("uvi", 0)
        
        result = f"## Current Weather in {location}\n\n"
        result += f"**Condition:** {weather.get('description', 'Unknown').title()}\n"
        result += f"**Temperature:** {temp:.1f}{temp_unit} (feels like {feels_like:.1f}{temp_unit})\n"
        result += f"**Humidity:** {humidity}%\n"
        result += f"**Pressure:** {pressure} hPa\n"
        result += f"**Wind:** {wind_speed:.1f} {speed_unit}"
        
        if wind_deg:
            direction = self._get_wind_direction(wind_deg)
            result += f" {direction}"
        result += "\n"
        
        result += f"**Visibility:** {visibility:.1f} km\n"
        result += f"**UV Index:** {uv_index:.1f}\n"
        
        # Sunrise/sunset
        if "sunrise" in current and "sunset" in current:
            sunrise = datetime.fromtimestamp(current["sunrise"], tz=timezone.utc)
            sunset = datetime.fromtimestamp(current["sunset"], tz=timezone.utc)
            result += f"**Sunrise:** {sunrise.strftime('%H:%M UTC')}\n"
            result += f"**Sunset:** {sunset.strftime('%H:%M UTC')}\n"
        
        # Add 24-hour forecast if requested
        if include_forecast and "hourly" in data:
            result += "\n## 24-Hour Forecast\n\n"
            for i, hour_data in enumerate(data["hourly"][:24:3]):  # Every 3 hours
                hour_time = datetime.fromtimestamp(hour_data["dt"], tz=timezone.utc)
                hour_temp = hour_data.get("temp", 0)
                hour_weather = hour_data.get("weather", [{}])[0]
                result += f"**{hour_time.strftime('%H:%M')}:** {hour_temp:.1f}{temp_unit}, {hour_weather.get('description', 'Unknown')}\n"
        
        return result

    def _format_forecast(self, data: Dict, location: str, units: str, days: int, include_hourly: bool) -> str:
        """Format forecast data"""
        temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        
        result = f"## {days}-Day Weather Forecast for {location}\n\n"
        
        # Daily forecast
        daily_data = data.get("daily", [])[:days]
        for i, day_data in enumerate(daily_data):
            date = datetime.fromtimestamp(day_data["dt"], tz=timezone.utc)
            weather = day_data.get("weather", [{}])[0]
            temp_day = day_data.get("temp", {}).get("day", 0)
            temp_night = day_data.get("temp", {}).get("night", 0)
            temp_min = day_data.get("temp", {}).get("min", 0)
            temp_max = day_data.get("temp", {}).get("max", 0)
            humidity = day_data.get("humidity", 0)
            
            day_name = "Today" if i == 0 else date.strftime("%A")
            result += f"### {day_name} ({date.strftime('%Y-%m-%d')})\n"
            result += f"**Condition:** {weather.get('description', 'Unknown').title()}\n"
            result += f"**Temperature:** {temp_min:.1f}{temp_unit} - {temp_max:.1f}{temp_unit}\n"
            result += f"**Day/Night:** {temp_day:.1f}{temp_unit} / {temp_night:.1f}{temp_unit}\n"
            result += f"**Humidity:** {humidity}%\n\n"
        
        # Hourly forecast if requested
        if include_hourly and "hourly" in data:
            result += "## 48-Hour Hourly Forecast\n\n"
            for i, hour_data in enumerate(data["hourly"][:48:6]):  # Every 6 hours
                hour_time = datetime.fromtimestamp(hour_data["dt"], tz=timezone.utc)
                hour_temp = hour_data.get("temp", 0)
                hour_weather = hour_data.get("weather", [{}])[0]
                result += f"**{hour_time.strftime('%a %H:%M')}:** {hour_temp:.1f}{temp_unit}, {hour_weather.get('description', 'Unknown')}\n"
        
        return result

    def _format_alerts(self, data: Dict, location: str) -> str:
        """Format weather alerts"""
        alerts = data.get("alerts", [])
        
        if not alerts:
            return f"## Weather Alerts for {location}\n\nNo active weather alerts."
        
        result = f"## Weather Alerts for {location}\n\n"
        result += f"⚠️ **{len(alerts)} active alert(s)**\n\n"
        
        for i, alert in enumerate(alerts, 1):
            sender = alert.get("sender_name", "Unknown")
            event = alert.get("event", "Weather Alert")
            description = alert.get("description", "No description available")
            start = datetime.fromtimestamp(alert.get("start", 0), tz=timezone.utc)
            end = datetime.fromtimestamp(alert.get("end", 0), tz=timezone.utc)
            
            result += f"### Alert {i}: {event}\n"
            result += f"**Source:** {sender}\n"
            result += f"**Valid:** {start.strftime('%Y-%m-%d %H:%M UTC')} - {end.strftime('%Y-%m-%d %H:%M UTC')}\n"
            result += f"**Description:** {description}\n\n"
        
        return result

    def _get_wind_direction(self, degrees: float) -> str:
        """Convert wind direction degrees to compass direction"""
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                     "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        index = round(degrees / 22.5) % 16
        return directions[index]