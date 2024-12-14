import os
import glob
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import argparse

# Database configuration
db_config = {
    'dbname': 'raw_data',              
    'user': 'airflow',                
    'password': 'airflow',            
    'host': 'localhost',  # Use localhost if running from local, or postgres if running from a container
    'port': '5432'                    
}

# Directory containing the CSV files
csv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../raw_data/weather_data')

# Table name in the database
table_name = 'weather'


def get_country_name_from_filename(filename):
    """
    Extracts the country name from the file name.
    Assumes the file name is in the format {country_name}_weather_{START_DATE}_{END_DATE}.csv.
    """
    base_name = os.path.basename(filename)
    # Remove the suffix '_weather_{START_DATE}_{END_DATE}.csv' to get the country name
    country_name = base_name.split('_weather_')[0]
    return country_name.capitalize()  # Capitalize to make it look cleaner

def read_weather_csv(file_path):
    """
    Reads a CSV file into a DataFrame.
    """
    df = pd.read_csv(file_path)
    return df


def transform_data(df, country_name):
    """
    Transforms the DataFrame to fit the database schema.
    
    Args:
        df (DataFrame): The DataFrame with weather data.
        country_name (str): The name of the country to be added as a new column.
    
    Returns:
        DataFrame: Transformed DataFrame ready for database insertion.
    """
    df['country_name'] = country_name
    df.rename(columns={
        'date': 'weather_date',
        'weather_code': 'weather_code',
        'temperature_2m_max': 'temperature_2m_max',
        'temperature_2m_min': 'temperature_2m_min',
        'apparent_temperature_max': 'apparent_temperature_max',
        'apparent_temperature_min': 'apparent_temperature_min',
        'precipitation_sum': 'precipitation_sum',
        'rain_sum': 'rain_sum',
        'showers_sum': 'showers_sum',
        'snowfall_sum': 'snowfall_sum',
        'wind_speed_10m_max': 'wind_speed_10m_max',
        'wind_gusts_10m_max': 'wind_gusts_10m_max'
    }, inplace=True)
    
    # Convert date column to timestamp
    df['weather_date'] = pd.to_datetime(df['weather_date'])
    return df


def insert_data_to_db(df, conn):
    """
    Inserts the DataFrame into the database.
    
    Args:
        df (DataFrame): The DataFrame to be inserted.
        conn (psycopg2 connection): Connection to the PostgreSQL database.
    """
    with conn.cursor() as cur:
        # Define the SQL query for inserting data
        sql = f"""INSERT INTO {table_name} (
            country_name, weather_date, weather_code, temperature_2m_max, temperature_2m_min, 
            apparent_temperature_max, apparent_temperature_min, precipitation_sum, rain_sum, 
            showers_sum, snowfall_sum, wind_speed_10m_max, wind_gusts_10m_max
        ) VALUES %s"""

        # Convert the DataFrame to a list of tuples (required for psycopg2's execute_values)
        data_tuples = [
            (
                row['country_name'], row['weather_date'], row['weather_code'], row['temperature_2m_max'], row['temperature_2m_min'], 
                row['apparent_temperature_max'], row['apparent_temperature_min'], row['precipitation_sum'], row['rain_sum'], 
                row['showers_sum'], row['snowfall_sum'], row['wind_speed_10m_max'], row['wind_gusts_10m_max']
            ) for index, row in df.iterrows()
        ]

        # Use execute_values to efficiently insert multiple rows
        execute_values(cur, sql, data_tuples)
        conn.commit()
        print(f"Inserted {len(data_tuples)} rows into {table_name}.")


def main(csv_files):
    """
    Main function to ingest all weather CSV files into the database.
    """
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_config)
        print("Connected to the database successfully.")
        
        # Get all CSV files from the specified directory
        print(f"Found {len(csv_files)} files to ingest.")
        
        for file_path in csv_files:
            try:
                country_name = get_country_name_from_filename(file_path)
                print(f"Processing file: {file_path} (Country: {country_name})")
                
                # Step 1: Read the CSV file
                df = read_weather_csv(file_path)
                
                # Step 2: Transform the DataFrame to match the database table
                df = transform_data(df, country_name)
                
                # Step 3: Insert the data into the PostgreSQL database
                insert_data_to_db(df, conn)
            except Exception as e:
                print(f"Failed to process file {file_path}: {e}")
        
    except Exception as e:
        print(f"Error connecting to the database: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    # Argument parser to accept optional files parameter
    parser = argparse.ArgumentParser(description="Ingest weather data files into the database.")
    parser.add_argument(
        '--files', 
        nargs='*',  # Accept zero or more file paths as a list
        default=glob.glob(os.path.join(csv_dir, "*_weather_*_*.csv")),  # Default glob logic
        help="List of weather CSV files to ingest. Defaults to all files matching *_weather_*_*.csv."
    )
    
    args = parser.parse_args()
    csv_files = args.files
    
    # Print the files that are being processed for debug purposes
    print(f"Files to process: {csv_files}")
    
    main(csv_files)
