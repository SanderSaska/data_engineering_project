import os
import pandas as pd
import psycopg2
from psycopg2 import sql

script_dir = os.path.dirname(os.path.abspath(__file__))
# Directory containing Parquet files
parquet_dir = os.path.join(script_dir, "../../raw_data/EEA_Downloads/ParquetFiles")

# Database connection parameters
db_config = {
    'dbname': 'raw_data',              
    'user': 'airflow',                
    'password': 'airflow',            
    'host': 'localhost',  # Localhost since Docker forwards 5432:5432               
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

def insert_data_to_db(conn, df, file_name):
    """
    Insert data from DataFrame into the PostgreSQL table.
    
    Args:
        conn: Database connection object.
        df: DataFrame containing the data to be inserted.
        file_name: Name of the source Parquet file.
    """
    try:
        cursor = conn.cursor()
        
        # Create an insert query
        insert_query = sql.SQL('''
            INSERT INTO airQuality (
                Samplingpoint,
                Pollutant,
                time_start,
                time_end,
                pollutant_value,
                Unit,
                AggType,
                Validity,
                Verification,
                ResultTime,
                DataCapture,
                FkObservationLog,
                file_Name
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''')
        
        # Loop through DataFrame rows and insert each record
        for index, row in df.iterrows():
            cursor.execute(insert_query, (
                row['Samplingpoint'],
                row['Pollutant'],
                pd.to_datetime(row['Start']),
                pd.to_datetime(row['End']),
                float(row['Value']) if pd.notnull(row['Value']) else None,
                row['Unit'],
                row['AggType'],
                int(row['Validity']) if pd.notnull(row['Validity']) else None,
                int(row['Verification']) if pd.notnull(row['Verification']) else None,
                pd.to_datetime(row['ResultTime']),
                float(row['DataCapture']) if pd.notnull(row['DataCapture']) else None,
                row['FkObservationLog'],
                file_name
            ))
        
        # Commit the transaction
        conn.commit()
        print(f"Successfully inserted {len(df)} records from {file_name}.")
    except Exception as e:
        conn.rollback()
        print(f"Failed to insert records from {file_name} into the database: {e}")

def process_parquet_files():
    """Process each Parquet file in the specified directory and insert its data into the database."""
    conn = connect_to_db()
    if conn is None:
        return
    
    for file_name in os.listdir(parquet_dir):
        if file_name.endswith('.parquet'):
            file_path = os.path.join(parquet_dir, file_name)
            print(f"Processing file: {file_path}")
            
            try:
                # Read the Parquet file into a DataFrame
                df = pd.read_parquet(file_path)
                
                # Ensure DataFrame has the same column names as the table
                df.rename(columns={
                    'Samplingpoint': 'Samplingpoint',
                    'Pollutant': 'Pollutant',
                    'Start': 'Start',
                    'End': 'End',
                    'Value': 'Value',
                    'Unit': 'Unit',
                    'AggType': 'AggType',
                    'Validity': 'Validity',
                    'Verification': 'Verification',
                    'ResultTime': 'ResultTime',
                    'DataCapture': 'DataCapture',
                    'FkObservationLog': 'FkObservationLog'
                }, inplace=True)
                
                # Insert the DataFrame into the database
                insert_data_to_db(conn, df, file_name)
            except Exception as e:
                print(f"Failed to process file {file_name}: {e}")
    
    # Close the database connection
    if conn:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    process_parquet_files()