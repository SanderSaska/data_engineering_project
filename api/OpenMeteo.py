import requests
import csv
import os
import json
import time

# Define the API URL
api_url = "https://historical-forecast-api.open-meteo.com/v1/forecast"

# Define the parameters for the API request
START_DATE = "2020-06-01"
END_DATE = "2024-12-11"
daily_metrics = [
    "weather_code", 
    "temperature_2m_max", 
    "temperature_2m_min", 
    "apparent_temperature_max", 
    "apparent_temperature_min", 
    "precipitation_sum", 
    "rain_sum", 
    "showers_sum", 
    "snowfall_sum", 
    "wind_speed_10m_max", 
    "wind_gusts_10m_max"
]

# Define the output directory to save API responses
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "../raw_data/weather_data")
os.makedirs(output_dir, exist_ok=True)
# Define the path to the CSV file
geo_csv_path = os.path.join(script_dir, "../raw_data/geo_data/geo_data.csv")

def read_geo_data(file_path):
    """
    Reads the geo data from a CSV file and returns a list of dictionaries
    Each dictionary contains 'name', 'lat', 'lon', and 'country_code' keys.
    """
    geo_data = []
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            geo_data.append({
                'name': row['name'],
                'latitude': float(row['lat']),
                'longitude': float(row['lon']),
                'country_code': row['country_code']
            })

    return geo_data

def fetch_weather_data(latitude, longitude):
    """
    Fetch weather data from the Open-Meteo API for the specified latitude and longitude.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": daily_metrics
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for lat: {latitude}, lon: {longitude} - {e}")
        return None

def save_weather_data_to_csv(country_name, data):
    """
    Save the weather data to a CSV file named after the country name.
    """
    if not data:
        print(f"No data to save for {country_name}")
        return

    file_name = f"{country_name.replace(' ', '_').lower()}_weather.csv"
    file_path = os.path.join(output_dir, file_name)
    
    try:
        # Extract the daily data
        daily_data = data.get('daily', {})
        time_series = daily_data.get('time', [])
        
        # Open the CSV file for writing
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header
            header = ['date'] + daily_metrics
            writer.writerow(header)
            
            # Write the daily weather data
            for i, date in enumerate(time_series):
                row = [date]
                for metric in daily_metrics:
                    metric_values = daily_data.get(metric, [])
                    row.append(metric_values[i] if i < len(metric_values) else None)
                writer.writerow(row)
        
        print(f"Successfully saved weather data for {country_name} at {file_path}")
    except Exception as e:
        print(f"Error saving data for {country_name}: {e}")

def main():
    """
    Main execution function to read geo data, fetch weather data, and save it to a file.
    """
    # Step 1: Read geo data from the CSV file
    geo_data = read_geo_data(geo_csv_path)
    
    for location in geo_data:
        country_name = location['name']
        latitude = location['latitude']
        longitude = location['longitude']
        
        print(f"Fetching weather data for {country_name} (lat: {latitude}, lon: {longitude})...")
        
        # Step 2: Fetch weather data for the location
        weather_data = fetch_weather_data(latitude, longitude)
        
        # Step 3: Save the weather data to a CSV file
        save_weather_data_to_csv(country_name, weather_data)

        time.sleep(5)

if __name__ == "__main__":
    main()
