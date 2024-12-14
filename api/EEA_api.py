import requests
import os
import csv
import time

# Check: https://eeadmz1-downloads-webapp.azurewebsites.net/content/documentation/How_To_Downloads.pdf

apiUrl = "https://eeadmz1-downloads-api-appservice.azurewebsites.net/"
endpoint = "ParquetFile\\urls"
# Get the directory where the script resides
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the download path relative to the script's directory
download_path = os.path.join(script_dir, "../raw_data/EEA_Downloads")

csv_filename = "ParquetFileUrls.csv"
parquet_download_path = os.path.join(download_path, "ParquetFiles")

# Ensure the directory exists
os.makedirs(download_path, exist_ok=True)
os.makedirs(parquet_download_path, exist_ok=True)

geo_data_file = os.path.join(script_dir, "../raw_data/geo_data/geo_data.csv")

# Request body
request_body = {
    "countries": [
        "HR",
        "BE",
        "AT",
        "DE",
    ],
    "cities": [
    ],
    "pollutants": [
        "PM2.5",
        "PM10",
        "NO2",
        "O3"
    ],
    "dataset": 2,
    "source": "API",
    "dateTimeStart": "2020-06-01T00:00:00Z",
    "dateTimeEnd": "2024-12-31T00:00:00Z",
    "aggregationType": "day",
    "email": ""
}

def get_country_codes():
    """Load geo data from the CSV file."""
    country_codes = []
    try:
        with open(geo_data_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                country_codes.append(row['country_code'])
        print("Successfully loaded country codes from", geo_data_file)
    except Exception as e:
        print("Error loading country codes from CSV:", e)
    return country_codes

def fetch_air_quality_data():
    try:
        response = requests.post(apiUrl + endpoint, json=request_body)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Check if response contains a file
        if "text/csv" in response.headers.get("Content-Type", ""):
            # Save the file
            file_path = os.path.join(download_path, csv_filename)
            with open(file_path, 'wb') as output:
                output.write(response.content)
            print(f"File successfully downloaded to {file_path}")
        else:
            print("Unexpected response content type. Check API response.")
            print("Response Headers:", response.headers)
            print("Response Content:", response.text)  # Debugging unexpected responses

    except requests.exceptions.RequestException as e:
        print("Error occurred:", e)

def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for HTTP issues
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def process_csv_and_download():
    csv_file_path = os.path.join(download_path, csv_filename)

    # Wait until the file exists
    for _ in range(10):  # Retry for 10 seconds
        if os.path.exists(csv_file_path):
            break
        time.sleep(1)
    else:
        print(f"CSV file not found after waiting: {csv_file_path}")
        return

    try:
        with open(csv_file_path, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for i, row in enumerate(reader):
                if i == 0:  # Skip the header row
                    continue
                url = row[0]  # Assuming the URL is in the first column
                file_name = os.path.basename(url)
                save_path = os.path.join(parquet_download_path, file_name)
                download_file(url, save_path)
    except Exception as e:
        print(f"Error processing CSV: {e}")

def main():
    codes = get_country_codes()
    request_body['countries'] = codes
    fetch_air_quality_data()
    process_csv_and_download()

if __name__ == "__main__":
    main()
