# XWeather Home Assistant Integration <a href="https://www.xweather.com/" target="_blank" title="Powered by Vaisala Xweather"><img src="https://www.xweather.com/assets/logos/vaisala-xweather-logo-dark.svg" alt="Vaisala Xweather" height="40" align="right" /></a>

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Component-blue)

<p align="center">
  <img src="docs/logo.png" alt="XWeather Logo" width="400"/>
</p>

**XWeather** is a custom integration for [Home Assistant](https://www.home-assistant.io/)
providing current conditions, forecasts, and air quality data from [XWeather.com](https://xweather.com/).

---

## Features

- Weather entity with:
  - Current conditions
  - Hourly and 7-day daily forecast
  - Extended forecast fields (temperature, humidity, pressure, wind, UV, precipitation probability and amount)
- Individual sensors for:
  - Temperature, humidity, wind, feels-like temperature
  - Cloud coverage, UV, visibility, precipitation
- Air Quality:
  - AQI as primary air quality entity
  - PM2.5, PM10, O3, CO, NO2, SO2 pollutant sensors
- Refresh button for immediate data update
- Respects system setting for units (metric or imperial)
- XWeather device shows all entities and Refresh button

---

## Requirements

- API key and secret from [XWeather.com](https://xweather.com/)
  - If you have a personal weather station, you may be eligible for a free API key
  - Consider the [Contributor Plan](https://signup.xweather.com/pws-contributor)
  - **PWS Upload**: If your weather station does not upload data to PWSWeather, you can use this Home Assistant Blueprint to send your sensor data to the service: [PWS Weather Station Upload](https://community.home-assistant.io/t/pws-weather-station-upload/806415)

---

## Installation

### HACS (Recommended)

1. Add this repo as a **Custom Repository** in HACS:
   `https://github.com/tbclark3/homeassistant-xweather`
2. Select **Integration** category.
3. Restart Home Assistant when prompted.

### Manual Installation

1. Copy the `custom_components/xweather` folder to your Home Assistant `custom_components` directory.
2. Restart Home Assistant.

---

## Configuration

Once the integration is installed (via HACS or manually):

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for and select **XWeather**.
3. Enter your:
   - **Client ID**
   - **Client Secret**
   - **Latitude / Longitude** (defaults to HA location)
   - **Name**: Base name for the weather and sensor entities (default: `xweather`)
   - **Update interval**: Frequency in minutes to poll the API (defaults to 60)
     - Each update uses 4 API calls (conditions, air quality, hourly and daily forecast)

---

## Example

Once configured, you will see:

- **Weather entity**: `weather.xweather`
- **Air Quality entity**: `air_quality.xweather`
- **Sensors**: `sensor.xweather_temperature`, `sensor.xweather_humidity`, etc.
- **Device page** showing all related entities and a **Refresh** button

---
