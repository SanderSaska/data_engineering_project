import requests
import mysql.connector
from mysql.connector import Error

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

def save_country_data_to_db(country_data, connection):
    """
    Saves country geo data to the MySQL database.
    
    Args:
        country_data (dict): Dictionary containing the country's geo data.
        connection (mysql.connector.connection_cext.CMySQLConnection): MySQL database connection.
    """
    try:
        if country_data:
            cursor = connection.cursor()
            query = """
            INSERT INTO geo_data (name, lat, lon, country_code) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (country_data['name'], country_data['lat'], country_data['lon'], country_data['country_code']))
            connection.commit()
            print(f"Successfully saved data for {country_data['name']} to the database.")
    except Error as e:
        print(f"Failed to insert data for {country_data['name']}: {e}")

def connect_to_db():
    """
    Connects to the MySQL database.
    
    Returns:
        mysql.connector.connection_cext.CMySQLConnection: Database connection object.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='your_database_name',
            user='your_username',
            password='your_password'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def main(country_names):
    '''
    connection = connect_to_db()
    if connection is None:
        print("Unable to connect to the database. Exiting...")
        return
    '''
    for country_name in country_names:
        print(f"Processing {country_name}...")
        country_data = get_country_data(country_name)
        if country_data:
            print(country_data)
            #save_country_data_to_db(country_data, connection)
    '''
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
        '''

if __name__ == "__main__":
    main(selected_countries)
