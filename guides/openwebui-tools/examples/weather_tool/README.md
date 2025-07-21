# Weather Tool

A comprehensive weather tool for OpenWebUI that provides current weather conditions and forecasts using the OpenWeatherMap One Call API 3.0.

## Features

- 🌤️ Current weather conditions
- 📅 7-day weather forecast
- ⏰ Hourly forecast (next 12 hours)
- 🌡️ Multiple temperature units (Celsius, Fahrenheit, Kelvin)
- 🧭 Wind direction and speed
- 🌅 Sunrise/sunset times
- ☔ Precipitation probability
- 🌈 Weather emojis and visual indicators
- 🔍 Automatic location geocoding

## Functions

### `get_weather(location, units, include_forecast)`
Get comprehensive weather information including current conditions and forecasts.

**Parameters:**
- `location` (str): City name, state/country (e.g., "London, UK", "New York, NY, US")
- `units` (str): Temperature units - "metric" (°C), "imperial" (°F), or "kelvin" (default: metric)
- `include_forecast` (bool): Whether to include 7-day forecast (default: True)

**Example Usage:**
```
Use get_weather tool with location "Tokyo, Japan" and units "metric"
```

### `get_current_weather(location, units)`
Get only current weather conditions (no forecast).

**Parameters:**
- `location` (str): City name, state/country
- `units` (str): Temperature units (default: metric)

**Example Usage:**
```
Use get_current_weather tool with location "Paris, France"
```

## Setup

### 1. Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Subscribe to the "One Call API 3.0" plan
4. Get your API key from the dashboard

### 2. Configure Environment Variable

Set your API key as an environment variable:

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tool

Copy `main.py` to your OpenWebUI tools directory and restart OpenWebUI.

## Configuration

The tool can be configured using environment variables:

```bash
# Required: Your OpenWeatherMap API key
export OPENWEATHER_API_KEY="your_api_key_here"
```

## Demo Mode

If no API key is provided, the tool runs in demo mode showing sample weather data. This is useful for testing the tool structure without an API key.

## API Information

This tool uses the **OpenWeatherMap One Call API 3.0**, which provides:

- Current weather data
- 48-hour hourly forecast
- 8-day daily forecast
- Weather alerts (excluded for simplicity)
- Historical weather data (not used)

### API Pricing

- **Free tier**: 1,000 calls/day
- **Paid plans**: Available for higher usage

Visit [OpenWeatherMap Pricing](https://openweathermap.org/price) for details.

## Weather Data Included

### Current Conditions
- Temperature and "feels like" temperature
- Humidity and atmospheric pressure
- Visibility and UV index
- Wind speed and direction
- Weather description with emoji
- Sunrise and sunset times

### Hourly Forecast (12 hours)
- Temperature for each hour
- Weather conditions
- Precipitation probability

### Daily Forecast (7 days)
- High and low temperatures
- Weather description
- Precipitation probability
- Day of week

## Location Handling

The tool uses OpenWeatherMap's geocoding API to convert location names to coordinates. Supported formats:

- City name: `"London"`
- City, Country: `"London, UK"`
- City, State, Country: `"New York, NY, US"`
- Coordinates: Use specific lat/lon if needed

## Error Handling

The tool includes comprehensive error handling:

- ✅ Invalid API key detection
- ✅ Location not found handling
- ✅ Network timeout management
- ✅ API rate limit awareness
- ✅ Graceful fallback to demo mode

## Troubleshooting

### Common Issues

1. **"Demo Mode" appears**: Set `OPENWEATHER_API_KEY` environment variable
2. **"Location not found"**: Try different location formats or be more specific
3. **"Invalid API key"**: Verify your API key and One Call API subscription
4. **Slow responses**: Check internet connection and API status

### Testing

Test the tool with various locations:

```bash
# Major cities
"Tokyo, Japan"
"New York, NY, US"
"London, UK"

# Different formats
"Paris"
"Sydney, Australia" 
"Toronto, ON, CA"
```

## Limitations

- Requires internet connection
- Needs valid OpenWeatherMap API key for real data
- Subject to API rate limits (1,000 calls/day free tier)
- Weather alerts not included (can be added if needed)

## Customization

The tool can be extended with additional features:

- Weather alerts and warnings
- Historical weather data
- Weather maps and radar
- Severe weather notifications
- Multiple location comparison

## Support

For issues with the tool:
1. Check API key configuration
2. Verify internet connectivity
3. Test with demo mode first
4. Check OpenWeatherMap API status

For OpenWeatherMap API issues:
- Visit [OpenWeatherMap Support](https://openweathermap.org/support)
- Check [API Documentation](https://openweathermap.org/api/one-call-3)