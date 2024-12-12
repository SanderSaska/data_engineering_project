import requests
import csv
import os

selected_countries = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Iceland",
    "Ireland",
    "Italy",
    "Latvia",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Norway",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden"
]
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the download path relative to the script's directory
csv_path = os.path.join(script_dir, "../raw_data/geo_data")

csv_filename = "geo_data.csv"

def get_country_data(country_name):
    """
    Makes an API call to Nominatim to fetch geo data for a given country.
    
    Args:
        country_name (str): Name of the country to search.
    
    Returns:
        dict or None: Dictionary with lat, lon, country_code, and name if successful, None otherwise.
    """
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={country_name}&format=json&addressdetails=1&limit=1"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0", "accept-language": "en-GB,en;q=0.8",})
        response.raise_for_status()
        data = response.json()
        
        if data and data[0].get('addresstype') == 'country':
            country_info = {
                'name': data[0].get('display_name'),
                'lat': data[0].get('lat'),
                'lon': data[0].get('lon'),
                'country_code': data[0]['address'].get('country_code')
            }
            return country_info
        else:
            print(f"No valid country data found for {country_name}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {country_name}: {e}")
        return None

def save_country_data_to_csv(country_data_list, filename="geo_data.csv"):
    """
    Saves country geo data to a CSV file.
    
    Args:
        country_data_list (list of dicts): List containing country geo data.
        filename (str): Name of the CSV file.
    """
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(["name", "lat", "lon", "country_code"])
            
            # Write each country's data
            for country_data in country_data_list:
                if country_data:  # Ensure country data is valid
                    writer.writerow([
                        country_data['name'], 
                        country_data['lat'], 
                        country_data['lon'], 
                        country_data['country_code'].upper()
                    ])
        print(f"Successfully saved data to {filename}.")
    except Exception as e:
        print(f"Failed to save data to {filename}: {e}")

def main(country_names):
    country_data_list = []
    for country_name in country_names:
        print(f"Processing {country_name}...")
        country_data = get_country_data(country_name)
        if country_data:
            #print(country_data)
            country_data_list.append(country_data)
    os.makedirs(csv_path, exist_ok=True)
    csv_filepath = os.path.join(csv_path, csv_filename)
    save_country_data_to_csv(country_data_list, csv_filepath)

if __name__ == "__main__":
    main(selected_countries)
