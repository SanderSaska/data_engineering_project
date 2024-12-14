import requests
import os
import csv
import time
import sys
import argparse
from datetime import datetime

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

def parse_args():
    """Parse optional command-line arguments for start and end date."""
    parser = argparse.ArgumentParser(description="EEA API data downloader.")
    parser.add_argument("--start_date", type=str, default="2020-06-01T00:00:00Z", help="Start date in ISO 8601 format (default: 2020-06-01T00:00:00Z)")
    parser.add_argument("--end_date", type=str, default=datetime.now().strftime("%Y-%m-%dT00:00:00Z"), help="End date in ISO 8601 format (default: today's date)")
    args = parser.parse_args()
    return args.start_date, args.end_date

def get_country_codes():
    """Load geo data from the CSV file."""
    country_codes = []
    with open(geo_data_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            country_codes.append(row['country_code'])
    return country_codes

def fetch_air_quality_data(request_body):
        response = requests.post(apiUrl + endpoint, json=request_body)
        response.raise_for_status()  # Raise an error for HTTP issues

        if "text/csv" in response.headers.get("Content-Type", ""):
            file_path = os.path.join(download_path, csv_filename)
            with open(file_path, 'wb') as output:
                output.write(response.content)
        else:
            raise Exception("Unexpected response content type. Check API response.", response.headers, response.text)


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


def process_csv_and_download():
    csv_file_path = os.path.join(download_path, csv_filename)
    downloaded_files = []

    for _ in range(10):  # Retry for 10 seconds
        if os.path.exists(csv_file_path):
            break
        time.sleep(1)
    else:
        raise Exception("File not found:", csv_file_path)


    with open(csv_file_path, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for i, row in enumerate(reader):
            if i == 0:  # Skip the header row
                continue
            url = row[0]
            file_name = os.path.basename(url)
            save_path = os.path.join(parquet_download_path, file_name)
            download_file(url, save_path)
            downloaded_files.append(save_path)
            if i > 10:#TODO REMOVE THIS
                break

    
    return downloaded_files

def main(start_date, end_date):
    request_body = {
        "countries": get_country_codes(),
        "cities": [],
        "pollutants": ["PM2.5", "PM10", "NO2", "O3"],
        "dataset": 2,
        "source": "API",
        "dateTimeStart": start_date,
        "dateTimeEnd": end_date,
        "aggregationType": "day",
        "email": ""
    }
    
    fetch_air_quality_data(request_body)
    downloaded_files = process_csv_and_download()

    return downloaded_files

if __name__ == "__main__":
    start_date, end_date = parse_args()
    
    files = main(start_date, end_date)

    for file in files:
        print(file)
