import requests
import csv
import os
import time
import argparse
from datetime import datetime

# Define the API URL
api_url = "https://historical-forecast-api.open-meteo.com/v1/forecast"


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
    Retries up to 2 times if a 504 Gateway Timeout error occurs.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": daily_metrics
    }
    max_retries = 2
    attempt = 0
    
    while attempt <= max_retries:
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            return response.json()
        except requests.exceptions.RequestException as e:
            if response.status_code == 504:  # Handle 504 Gateway Timeout
                attempt += 1
                if attempt <= max_retries:
                    time.sleep(10)
                else:
                    raise e
            else:
                raise e

def save_weather_data_to_csv(country_name, data):
    """
    Save the weather data to a CSV file named after the country name.
    """
    if not data:
        return None

    file_name = f"{country_name.replace(' ', '_').lower()}_weather_{START_DATE}_{END_DATE}.csv"
    file_path = os.path.join(output_dir, file_name)
    

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
    return file_path


def main(start_date, end_date):
    """
    Main execution function to read geo data, fetch weather data, and save it to a file.
    """
    generated_files = []

    
    # Step 1: Read geo data from the CSV file
    geo_data = read_geo_data(geo_csv_path)
    
    for location in geo_data:
        country_name = location['name']
        latitude = location['latitude']
        longitude = location['longitude']
        
        print(f"INFO: Fetching weather data for {country_name} (lat: {latitude}, lon: {longitude})...")
        
        # Step 2: Fetch weather data for the location
        weather_data = fetch_weather_data(latitude, longitude)
        
        # Step 3: Save the weather data to a CSV file
        file_path = save_weather_data_to_csv(country_name, weather_data)
        if file_path:
            generated_files.append(file_path)

        time.sleep(5)
    
    return generated_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch weather data from start_date to end_date.")
    parser.add_argument(
        '--start_date', 
        type=lambda s: datetime.strptime(s, '%Y-%m-%d').strftime("%Y-%m-%d"), 
        default=datetime(2020, 6, 1).strftime("%Y-%m-%d"), 
        help="Start date in YYYY-MM-DD format (default: 2020-06-01)"
    )
    parser.add_argument(
        '--end_date', 
        type=lambda s: datetime.strptime(s, '%Y-%m-%d').strftime("%Y-%m-%d"), 
        default=datetime.now().strftime("%Y-%m-%d"), 
        help="End date in YYYY-MM-DD format (default: today's date)"
    )
    
    args = parser.parse_args()
    START_DATE = args.start_date  # Update START_DATE with parsed argument
    END_DATE = args.end_date      # Update END_DATE with parsed argument

    generated_files = main(args.start_date, args.end_date)
    for file_path in generated_files:
        print(file_path)
