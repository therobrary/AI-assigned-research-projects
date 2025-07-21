# Weather Tool

A comprehensive weather information tool for OpenWebUI that integrates with OpenWeatherMap's One Call API 3.0 to provide current weather, forecasts, and weather alerts.

## Features

- **Current Weather**: Real-time weather conditions with detailed metrics
- **Weather Forecasts**: Up to 8-day daily forecasts with optional hourly data
- **Weather Alerts**: Active weather warnings and advisories
- **Multiple Units**: Support for metric (°C), imperial (°F), and Kelvin
- **Location Flexibility**: Supports city names, coordinates, and full location strings
- **Intelligent Caching**: Caches geocoding results to reduce API calls
- **Comprehensive Data**: Temperature, humidity, pressure, wind, UV index, visibility

## Prerequisites

### OpenWeatherMap API Key

This tool requires an OpenWeatherMap API key with access to the One Call API 3.0:

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Subscribe to the One Call API 3.0 (first 1,000 calls/day are free)
3. Get your API key from the dashboard

### Environment Setup

Set your API key as an environment variable:

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

Or add it to your OpenWebUI environment configuration.

## Installation

1. Copy `weather_tool.py` to your OpenWebUI tools directory
2. Install required dependencies (if not already available):
   ```bash
   pip install requests
   ```
3. Set the `OPENWEATHER_API_KEY` environment variable
4. Restart OpenWebUI or refresh the tools list

## Usage Examples

### Current Weather
```
"What's the current weather in London?"
```

### Weather with Forecast
```
"Get current weather and 24-hour forecast for Tokyo, Japan"
```

### Multi-day Forecast
```
"Show me a 7-day weather forecast for New York with hourly details"
```

### Weather Alerts
```
"Are there any weather alerts for Miami, Florida?"
```

### Different Units
```
"Get the weather in Paris using Fahrenheit"
```

## Actions

### 1. get_current_weather()

Retrieves current weather conditions for a specified location.

**Parameters:**
- `location` (required): City name, state/country (e.g., "London", "New York, NY", "Tokyo, Japan")
- `units` (optional): Temperature units - "metric" (°C), "imperial" (°F), or "kelvin" (default: "metric")
- `include_forecast` (optional): Include 24-hour forecast (default: False)

**Returns:** Formatted current weather information including:
- Weather condition and description
- Temperature (current and feels-like)
- Humidity and atmospheric pressure
- Wind speed and direction
- Visibility and UV index
- Sunrise and sunset times
- Optional 24-hour forecast

### 2. get_weather_forecast()

Provides detailed weather forecasts for multiple days.

**Parameters:**
- `location` (required): City name, state/country
- `days` (optional): Number of forecast days (1-8, default: 5)
- `units` (optional): Temperature units (default: "metric")
- `include_hourly` (optional): Include hourly forecast for next 48 hours (default: False)

**Returns:** Formatted forecast including:
- Daily weather conditions
- High and low temperatures
- Day and night temperatures
- Humidity levels
- Optional hourly breakdown

### 3. get_weather_alerts()

Checks for active weather alerts and warnings.

**Parameters:**
- `location` (required): City name, state/country

**Returns:** Weather alerts information including:
- Alert type and severity
- Source organization
- Valid time period
- Detailed description

## Technical Details

### API Integration

The tool integrates with two OpenWeatherMap APIs:
1. **Geocoding API**: Converts location names to coordinates
2. **One Call API 3.0**: Provides comprehensive weather data

### Data Processing

- **Geocoding Cache**: Stores location coordinates to reduce API calls
- **Unit Conversion**: Handles metric, imperial, and Kelvin units
- **Time Formatting**: Converts UTC timestamps to readable formats
- **Wind Direction**: Converts degrees to compass directions

### Error Handling

- API key validation
- Network timeout handling (10-15 second timeouts)
- Location not found handling
- Graceful degradation for missing data
- User-friendly error messages

### Rate Limiting

The tool implements respectful API usage:
- Connection pooling for efficient requests
- Caching to reduce redundant calls
- Reasonable timeouts to prevent hanging

## Configuration

### Custom API Endpoints

If using a different OpenWeatherMap setup:

```python
# In the __init__ method
self.base_url = "https://your-custom-endpoint.com"
```

### Cache Configuration

Adjust caching behavior:

```python
# Clear cache periodically
import time
if time.time() - self._last_cache_clear > 3600:  # 1 hour
    self._geocoding_cache.clear()
    self._last_cache_clear = time.time()
```

### Default Units

Change default temperature units:

```python
def get_current_weather(self, location: str, units: str = "imperial", ...):
```

## Data Examples

### Current Weather Response
```
## Current Weather in London, England, GB

**Condition:** Partly Cloudy
**Temperature:** 18.5°C (feels like 19.2°C)
**Humidity:** 65%
**Pressure:** 1013 hPa
**Wind:** 3.2 m/s NW
**Visibility:** 10.0 km
**UV Index:** 4.2
**Sunrise:** 06:45 UTC
**Sunset:** 19:30 UTC
```

### Forecast Response
```
## 5-Day Weather Forecast for Paris, France

### Today (2024-01-15)
**Condition:** Light Rain
**Temperature:** 8.1°C - 12.4°C
**Day/Night:** 11.2°C / 9.1°C
**Humidity:** 78%

### Tuesday (2024-01-16)
**Condition:** Overcast Clouds
**Temperature:** 6.5°C - 10.8°C
**Day/Night:** 9.2°C / 7.1°C
**Humidity:** 82%
```

## Security Considerations

1. **API Key Protection**: Store API keys in environment variables
2. **Input Validation**: Validates location strings to prevent injection
3. **Rate Limiting**: Prevents abuse of OpenWeatherMap services
4. **Error Handling**: Doesn't expose internal errors to users

## Troubleshooting

### Common Issues

1. **"API key not found" error**
   - Ensure `OPENWEATHER_API_KEY` environment variable is set
   - Verify the API key is valid and active

2. **"Location not found" error**
   - Try different location formats (e.g., "City, Country")
   - Use more specific location names
   - Check spelling of location names

3. **Network timeout errors**
   - Check internet connectivity
   - Verify OpenWeatherMap service status
   - Try again after a short delay

4. **"Failed to retrieve weather data" error**
   - Check API key permissions for One Call API 3.0
   - Verify API quota hasn't been exceeded
   - Check OpenWeatherMap service status

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add debug statements
logger.debug(f"Making API request to: {url}")
logger.debug(f"Response: {response.json()}")
```

### Testing API Key

Test your API key manually:

```bash
curl "https://api.openweathermap.org/data/3.0/onecall?lat=51.5074&lon=-0.1278&appid=YOUR_API_KEY"
```

## Performance Tips

1. **Use Caching**: Location geocoding is cached automatically
2. **Limit Forecast Days**: Fewer days = faster responses
3. **Skip Hourly Data**: Don't include hourly forecasts unless needed
4. **Batch Requests**: If checking multiple locations, space out requests

## API Limits

OpenWeatherMap One Call API 3.0 limits:
- **Free Tier**: 1,000 calls/day
- **Rate Limit**: 60 calls/minute
- **Data Retention**: Current + 8 days forecast

## Future Enhancements

- Historical weather data
- Weather maps integration
- Air quality information
- Severe weather notifications
- Multi-language support
- Weather-based recommendations

This tool provides comprehensive weather information and can be easily extended for specific use cases or integrated with other OpenWebUI tools.