import requests
import json
import os

# API Endpoint
url = "https://eeadmz1-downloads-api-appservice.azurewebsites.net/ParquetFile"

# Payload for API request
payload = {
    "countries": ["EE"],  # Example: Estonia
    "cities": ["Tallinn"],  # Example: Tallinn
    "pollutants": ["PM10", "PM2.5"],  # Pollutants of interest
    "dataset": 1,  # Dataset ID (as per Swagger docs)
    "source": "EEA",  # Data source
    "dateTimeStart": "2024-01-01T00:00:00Z",  # Start date
    "dateTimeEnd": "2024-01-07T23:59:59Z",  # End date
    "aggregationType": "day"  # Aggregation type
}

# Headers
headers = {"Content-Type": "application/json"}

# Output file path (in raw_data)
output_path = os.path.join(os.getcwd(), "raw_data", "air_quality_data.parquet")

def fetch_data():
    try:
        # Send the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # Handle response
        if response.status_code == 200:
            # Save the file
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Data successfully saved to {output_path}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_data()
