import requests
import os
import csv
import time


OWM_api_K = "a3b9dd2c439b05ff49d6b5c4ed8a9b98"
OWM_api_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
json_filename = "weather_data.json"

# Get the directory where the script resides
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the download path relative to the script's directory
download_path = os.path.join(script_dir, "OWM_Downloads")
os.makedirs(download_path, exist_ok=True)



OWM_api_params = {
    "lat": 51.5074,
    "lon": 0.1278,
    "appid": OWM_api_K,
    "dt": 1634054400  # 13th October 2021
}
OWM_geo_url = "http://api.openweathermap.org/geo/1.0/direct"


def fetch_weather_data(geodata):
    try:
        OWM_api_params["lat"] = geodata["lat"]
        OWM_api_params["lon"] = geodata["lon"]
        OWM_api_params["dt"] = int(time.time())
        response = requests.get(OWM_api_url, params=OWM_api_params)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Check if response contains a file
        if "application/json" in response.headers.get("Content-Type", ""):
            # Save the file
            file_path = os.path.join(download_path, json_filename)
            with open(file_path, 'wb') as output:
                output.write(response.content)
            print(f"File successfully downloaded to {file_path}")
        else:
            print("Unexpected response content type. Check API response.")
            print("Response Headers:", response.headers)
            print("Response Content:", response.text)  # Debugging unexpected responses

    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)

if __name__ == "__main__":
    # TODO: Add existing city fetching and loop each city
    city = "London"
    geodata = fetch_geo_data(city)
    fetch_weather_data(geodata)