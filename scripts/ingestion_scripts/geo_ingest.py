import os
import pandas as pd
import psycopg2
from psycopg2 import sql

# Get the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the geo_data.csv file
csv_path = os.path.join(script_dir, "../../raw_data/geo_data/geo_data.csv")

# Database connection parameters
db_config = {
    'dbname': 'raw_data',              
    'user': 'airflow',                
    'password': 'airflow',            
    'host': 'localhost',  # Use localhost if running from local, or postgres if running from a container
    'port': '5432'                    
}

def connect_to_db():
    """Create a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**db_config)
        print("Successfully connected to the database.")
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

def insert_data_to_db(conn, df):
    """
    Insert data from DataFrame into the PostgreSQL 'country' table.
    
    Args:
        conn: Database connection object.
        df: DataFrame containing the data to be inserted.
    """
    try:
        cursor = conn.cursor()
        
        # Create an insert query
        insert_query = sql.SQL('''
            INSERT INTO country (
                country_name, 
                lat, 
                lon, 
                country_code
            ) VALUES (%s, %s, %s, %s)
        ''')
        
        # Loop through DataFrame rows and insert each record
        for index, row in df.iterrows():
            cursor.execute(insert_query, (
                row['name'],
                float(row['lat']) if pd.notnull(row['lat']) else None,
                float(row['lon']) if pd.notnull(row['lon']) else None,
                row['country_code']
            ))
        
        # Commit the transaction
        conn.commit()
        print(f"Successfully inserted {len(df)} records into the 'country' table.")
    except Exception as e:
        conn.rollback()
        print(f"Failed to insert records into the 'country' table: {e}")

def process_csv_file():
    """Read the CSV file and insert its data into the PostgreSQL 'country' table."""
    conn = connect_to_db()
    if conn is None:
        return
    
    try:
        # Read the CSV file into a DataFrame
        print(f"Processing file: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Ensure DataFrame has the same column names as the table
        df.rename(columns={
            'name': 'name',
            'lat': 'lat',
            'lon': 'lon',
            'country_code': 'country_code'
        }, inplace=True)
        
        # Insert the DataFrame into the database
        insert_data_to_db(conn, df)
    except Exception as e:
        print(f"Failed to process file {csv_path}: {e}")
    
    # Close the database connection
    if conn:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    process_csv_file()
