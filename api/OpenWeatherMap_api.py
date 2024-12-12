
import requests
import os
import csv
import time
import json

OWM_api_K = "a3b9dd2c439b05ff49d6b5c4ed8a9b98"
OWM_api_url = "https://api.openweathermap.org/data/3.0/onecall/day_summary"
json_filename_template = "weather_data_{date}.json"

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the download path relative to the script's directory
download_path = os.path.join(script_dir, "../raw_data/OWM_Downloads")
geo_data_file = os.path.join(script_dir, "../raw_data/geo_data/geo_data.csv")
os.makedirs(download_path, exist_ok=True)

def load_geo_data(file_path):
    """Load geo data from the CSV file."""
    geo_data_list = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                geo_data_list.append({
                    'name': row['name'],
                    'lat': float(row['lat']),
                    'lon': float(row['lon']),
                    'country_code': row['country_code']
                })
        print("Successfully loaded geo data from", file_path)
    except Exception as e:
        print("Error loading geo data from CSV:", e)
    return geo_data_list

def fetch_weather_data(geodata, date):
    """Fetch weather data for a single geolocation and date."""
    try:
        params = {
            "lat": geodata["lat"],
            "lon": geodata["lon"],
            "appid": OWM_api_K,
            "date": date
        }
        response = requests.get(OWM_api_url, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        if response.headers.get("Content-Type", "").startswith("application/json"):
            weather_data = response.json()
            return weather_data
        else:
            print("Unexpected response content type for", geodata["name"], "on", date)
            print("Response Headers:", response.headers)
            print("Response Content:", response.text)  # Debugging unexpected responses
            return None
    except requests.exceptions.RequestException as e:
        print("Error occurred for", geodata["name"], "on", date, ":", e)
        return None

def aggregate_weather_data(geo_data_list, dates):
    """Aggregate weather data for multiple countries and dates and save as JSON files."""
    for date in dates:
        aggregated_data = []
        for geodata in geo_data_list:
            print(f"Fetching weather data for {geodata['name']} on {date}...")
            weather_data = fetch_weather_data(geodata, date)
            if weather_data:
                weather_data["country"] = geodata["name"]  # Add country name to the weather data
                weather_data["country_code"] = geodata["country_code"]  # Add country code to the weather data
                aggregated_data.append(weather_data)
        
        # Save aggregated weather data to a JSON file
        file_path = os.path.join(download_path, json_filename_template.format(date=date))
        try:
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(aggregated_data, json_file, ensure_ascii=False, indent=4)
            print(f"Successfully saved aggregated weather data to {file_path}")
        except Exception as e:
            print("Failed to save JSON file for", date, ":", e)

if __name__ == "__main__":
    geo_data_list = load_geo_data(geo_data_file)
    dates = ['2024-03-04']  # Add more dates if needed
    aggregate_weather_data(geo_data_list, dates)
