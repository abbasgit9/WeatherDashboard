#Features
Select a German city from a dropdown and fetch real-time weather data.
Display temperature, humidity, pressure, description, min/max temperature.
Plot weather data using Matplotlib graphs (temperature, humidity, pressure).
Save favorite cities and manage them (add, view, remove).
Load favorite cities quickly by double-clicking.
Export weather data to a CSV file.
Scrollable frame for weather graphs.

Technologies Used
Python 3
Tkinter (GUI)
Matplotlib (charts/graphs)
Requests (API calls)
JSON & CSV (data storage and export)

Prerequisites
Install Python 3.
Install dependencies:

Get a free API key from OpenWeatherMap.

Usage
Clone this repository or copy the script.
Replace the placeholder API key in the script with your own:

Run the script

Select a city from the dropdown and click Get Weather.
Use options to:
Save to Favorites
Load favorites by double-click
Remove from Favorites
Download Weather Data (CSV)

Files Generated
favorite_cities.json → Stores favorite cities.
<city_name>_weather.csv → Weather data export file.

Example Graphs
Temperature comparison (Min, Current, Max).
Humidity (%).
Pressure (hPa).

Notes
API key must be valid. Free tier has rate limits.
Only German cities included by default, but you can expand the list in german_cities.
