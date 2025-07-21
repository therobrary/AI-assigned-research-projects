"""
title: Weather Tool
author: OpenWebUI Guide
author_url: https://github.com/therobrary/AI-assigned-research-projects
version: 1.0.0
"""

from typing import Callable, Any, Dict, List
import aiohttp
import asyncio
import json
import os
from datetime import datetime, timezone


class Tools:
    def __init__(self):
        self.citation = True
        # OpenWeatherMap API configuration
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org"
        self.onecall_url = f"{self.base_url}/data/3.0/onecall"
        self.geo_url = f"{self.base_url}/geo/1.0/direct"
        self.timeout = 30
        
        if not self.api_key:
            self.api_key = "demo_key"  # For demonstration - will need real key
    
    async def get_weather(
        self,
        location: str,
        units: str = "metric",
        include_forecast: bool = True,
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Get current weather and forecast for a location using OpenWeatherMap One Call API 3.0
        
        :param location: City name, state/country (e.g., "London, UK" or "New York, NY, US")
        :param units: Temperature units - "metric" (°C), "imperial" (°F), or "kelvin" (default: metric)
        :param include_forecast: Whether to include 7-day forecast (default: True)
        :param __user__: User information
        :param __event_emitter__: Event emitter for real-time updates
        :return: Formatted weather information
        """
        
        if not location.strip():
            return "Error: Location cannot be empty"
        
        if units not in ["metric", "imperial", "kelvin"]:
            units = "metric"
        
        if self.api_key == "demo_key":
            return self._demo_weather_response(location, units, include_forecast)
        
        try:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": f"Looking up coordinates for {location}..."}
                })
            
            # Step 1: Get coordinates for the location
            coords = await self._get_coordinates(location)
            if not coords:
                return f"Error: Could not find coordinates for '{location}'"
            
            lat, lon = coords["lat"], coords["lon"]
            country = coords.get("country", "")
            state = coords.get("state", "")
            
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "Fetching weather data..."}
                })
            
            # Step 2: Get weather data using One Call API 3.0
            weather_data = await self._get_weather_data(lat, lon, units)
            if not weather_data:
                return "Error: Could not fetch weather data"
            
            # Step 3: Format the response
            formatted_weather = self._format_weather_response(
                weather_data, location, country, state, units, include_forecast
            )
            
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "Weather data retrieved! 🌤️"}
                })
            
            return formatted_weather
            
        except Exception as e:
            error_msg = f"Weather error: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({
                    "type": "error",
                    "data": {"description": error_msg}
                })
            return error_msg
    
    async def _get_coordinates(self, location: str) -> Dict:
        """Get latitude and longitude for a location"""
        
        params = {
            "q": location,
            "limit": 1,
            "appid": self.api_key
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
            try:
                async with session.get(self.geo_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data:
                            return data[0]
                    elif response.status == 401:
                        raise Exception("Invalid API key")
                    else:
                        raise Exception(f"Geocoding API returned status {response.status}")
                    
            except aiohttp.ClientError as e:
                raise Exception(f"Failed to connect to geocoding API: {str(e)}")
        
        return None
    
    async def _get_weather_data(self, lat: float, lon: float, units: str) -> Dict:
        """Get weather data from One Call API 3.0"""
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": units,
            "exclude": "minutely,alerts"  # Exclude minutely and alerts for simplicity
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
            try:
                async with session.get(self.onecall_url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 401:
                        raise Exception("Invalid API key")
                    else:
                        raise Exception(f"Weather API returned status {response.status}")
                        
            except aiohttp.ClientError as e:
                raise Exception(f"Failed to connect to weather API: {str(e)}")
    
    def _format_weather_response(
        self, 
        data: Dict, 
        location: str, 
        country: str, 
        state: str,
        units: str, 
        include_forecast: bool
    ) -> str:
        """Format weather data for display"""
        
        # Unit symbols
        temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        speed_unit = "m/s" if units == "metric" else "mph" if units == "imperial" else "m/s"
        
        # Current weather
        current = data.get("current", {})
        
        output = f"# 🌤️ Weather for {location}"
        if state:
            output += f", {state}"
        if country:
            output += f", {country}"
        output += "\n\n"
        
        # Current conditions
        output += "## Current Conditions\n\n"
        output += f"**Temperature:** {current.get('temp', 'N/A')}{temp_unit}\n"
        output += f"**Feels like:** {current.get('feels_like', 'N/A')}{temp_unit}\n"
        output += f"**Humidity:** {current.get('humidity', 'N/A')}%\n"
        output += f"**Pressure:** {current.get('pressure', 'N/A')} hPa\n"
        output += f"**Visibility:** {current.get('visibility', 'N/A')} m\n"
        output += f"**UV Index:** {current.get('uvi', 'N/A')}\n"
        output += f"**Wind Speed:** {current.get('wind_speed', 'N/A')} {speed_unit}\n"
        
        if current.get('wind_deg'):
            output += f"**Wind Direction:** {current['wind_deg']}° ({self._wind_direction(current['wind_deg'])})\n"
        
        # Weather description
        weather = current.get('weather', [])
        if weather:
            desc = weather[0].get('description', '').title()
            icon = self._weather_emoji(weather[0].get('icon', ''))
            output += f"**Conditions:** {desc} {icon}\n"
        
        # Sunrise/sunset
        if current.get('sunrise') and current.get('sunset'):
            sunrise = datetime.fromtimestamp(current['sunrise'], tz=timezone.utc).strftime('%H:%M UTC')
            sunset = datetime.fromtimestamp(current['sunset'], tz=timezone.utc).strftime('%H:%M UTC')
            output += f"**Sunrise:** {sunrise}\n"
            output += f"**Sunset:** {sunset}\n"
        
        output += "\n"
        
        # Hourly forecast (next 12 hours)
        if data.get('hourly') and include_forecast:
            output += "## Hourly Forecast (Next 12 Hours)\n\n"
            hourly = data['hourly'][:12]
            
            for hour_data in hourly:
                time = datetime.fromtimestamp(hour_data['dt'], tz=timezone.utc).strftime('%H:%M')
                temp = hour_data.get('temp', 'N/A')
                desc = hour_data.get('weather', [{}])[0].get('main', '')
                icon = self._weather_emoji(hour_data.get('weather', [{}])[0].get('icon', ''))
                pop = int(hour_data.get('pop', 0) * 100)  # Probability of precipitation
                
                output += f"**{time}:** {temp}{temp_unit} - {desc} {icon}"
                if pop > 0:
                    output += f" (Rain: {pop}%)"
                output += "\n"
            
            output += "\n"
        
        # Daily forecast (7 days)
        if data.get('daily') and include_forecast:
            output += "## 7-Day Forecast\n\n"
            daily = data['daily']
            
            for day_data in daily:
                date = datetime.fromtimestamp(day_data['dt'], tz=timezone.utc).strftime('%Y-%m-%d (%A)')
                temp_min = day_data.get('temp', {}).get('min', 'N/A')
                temp_max = day_data.get('temp', {}).get('max', 'N/A')
                desc = day_data.get('weather', [{}])[0].get('description', '').title()
                icon = self._weather_emoji(day_data.get('weather', [{}])[0].get('icon', ''))
                pop = int(day_data.get('pop', 0) * 100)
                
                output += f"**{date}**\n"
                output += f"High: {temp_max}{temp_unit} | Low: {temp_min}{temp_unit}\n"
                output += f"{desc} {icon}"
                if pop > 0:
                    output += f" | Rain: {pop}%"
                output += "\n\n"
        
        return output.strip()
    
    def _wind_direction(self, degrees: float) -> str:
        """Convert wind degrees to cardinal direction"""
        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                     "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        index = int((degrees + 11.25) / 22.5) % 16
        return directions[index]
    
    def _weather_emoji(self, icon: str) -> str:
        """Get emoji for weather icon"""
        emoji_map = {
            "01d": "☀️", "01n": "🌙",  # clear sky
            "02d": "⛅", "02n": "☁️",  # few clouds
            "03d": "☁️", "03n": "☁️",  # scattered clouds
            "04d": "☁️", "04n": "☁️",  # broken clouds
            "09d": "🌧️", "09n": "🌧️",  # shower rain
            "10d": "🌦️", "10n": "🌧️",  # rain
            "11d": "⛈️", "11n": "⛈️",  # thunderstorm
            "13d": "❄️", "13n": "❄️",  # snow
            "50d": "🌫️", "50n": "🌫️",  # mist
        }
        return emoji_map.get(icon, "🌤️")
    
    def _demo_weather_response(self, location: str, units: str, include_forecast: bool) -> str:
        """Demo response when no API key is provided"""
        
        temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
        demo_temp = "22" if units == "metric" else "72" if units == "imperial" else "295"
        
        output = f"# 🌤️ Weather for {location} (DEMO MODE)\n\n"
        output += "## Current Conditions\n\n"
        output += f"**Temperature:** {demo_temp}{temp_unit}\n"
        output += f"**Feels like:** {demo_temp}{temp_unit}\n"
        output += f"**Humidity:** 65%\n"
        output += f"**Pressure:** 1013 hPa\n"
        output += f"**Conditions:** Partly Cloudy ⛅\n"
        output += f"**Wind Speed:** 5 {'m/s' if units == 'metric' else 'mph'}\n\n"
        
        output += "⚠️ **Demo Mode**: To get real weather data, set the `OPENWEATHER_API_KEY` environment variable with your OpenWeatherMap API key.\n\n"
        output += "Get a free API key at: https://openweathermap.org/api\n"
        
        return output
    
    async def get_current_weather(
        self,
        location: str,
        units: str = "metric",
        __user__: dict = None,
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Get only current weather conditions (no forecast)
        
        :param location: City name, state/country
        :param units: Temperature units - "metric", "imperial", or "kelvin"
        :param __user__: User information
        :param __event_emitter__: Event emitter for real-time updates
        :return: Current weather information
        """
        
        return await self.get_weather(
            location=location,
            units=units,
            include_forecast=False,
            __user__=__user,
            __event_emitter__=__event_emitter
        )