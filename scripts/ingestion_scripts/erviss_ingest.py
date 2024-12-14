import os
import pandas as pd
import psycopg2
from psycopg2 import sql

# Get the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the directory containing all the CSV files
csv_dir = os.path.join(script_dir, "../../raw_data/Respiratory_viruses_weekly_data/data")

# Database connection parameters
db_config = {
    'dbname': 'raw_data',              
    'user': 'airflow',                
    'password': 'airflow',            
    'host': 'localhost',  # Use localhost if running from local, or postgres if running from a container
    'port': '5432'                    
}

table_mapping = {
    "activityFluTypeSubtype.csv": "activityflutypesubtype",
    "ILIARIRates.csv": "iliarirates",
    "nonSentinelSeverity.csv": "nonsentinelseverity",
    "nonSentinelTestsDetections.csv": "nonsentineltestsdetections",
    "SARIRates.csv": "sarirates",
    "SARITestsDetectionsPositivity.csv": "saritestsdetectionpositivity",
    "sentinelTestsDetectionsPositivity.csv": "sentineltestsdetectionspositivity",
    "sequencingVolumeDetectablePrevalence.csv": "sequencingvolumedetectableprevalence",
    "variants.csv": "variants"
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

def insert_data_to_db(conn, df, table_name):
    """
    Insert data from DataFrame into the PostgreSQL table.
    
    Args:
        conn: Database connection object.
        df: DataFrame containing the data to be inserted.
        table_name: Name of the table where the data will be inserted.
    """
    try:
        # Get the latest week from the db
        latest_week = pd.read_sql(
            f"SELECT yearweek FROM {table_name} ORDER BY CAST(SPLIT_PART(yearweek, '-W', 1) AS INTEGER) DESC, CAST(SPLIT_PART(yearweek, '-W', 2) AS INTEGER) DESC LIMIT 1;", 
            conn
        )
        if not latest_week.empty:
            latest_week_value = latest_week.iloc[0, 0]  # Safely access the value
            latest_year, latest_week = map(int, latest_week_value.split('-W'))

        else:
            latest_week_value = None  # No result, set a default value (like None)
            latest_year, latest_week = None, None  # Set default values
        
        
        cursor = conn.cursor()
        
        # Dynamically build the insert query
        columns = list(df.columns)
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(placeholders)
        )
        counter = 0
        
        # Loop through DataFrame rows and insert each record
        for index, row in df.iterrows():

            # Skip the row if the week is equal or less than the latest week in the db
            if latest_week_value is not None:
                row_year, row_week = map(int, row['yearweek'].split('-W'))
                # Compare year and week correctly
                if (row_year < latest_year) or (row_year == latest_year and row_week <= latest_week):
                    continue

            cursor.execute(insert_query, tuple(row))
            
        
        # Commit the transaction
        conn.commit()
        print(f"Successfully inserted {counter} records into '{table_name}'.")
    except Exception as e:
        conn.rollback()
        print(f"Failed to insert records into '{table_name}': {e}")

def process_csv_files():
    """Read each CSV file in the specified directory and insert its data into the appropriate PostgreSQL table."""
    conn = connect_to_db()
    if conn is None:
        return
    
    for file_name, table_name in table_mapping.items():
        file_path = os.path.join(csv_dir, file_name)
        if os.path.isfile(file_path):
            print(f"Processing file: {file_path}")
            try:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(file_path)
                
                # Ensure DataFrame has the same column names as the table
                df.rename(columns=lambda x: x.strip().lower(), inplace=True) # Normalize column names
                df.rename(columns={'indicator': 'inf_indicator', 'value': 'inf_value'}, inplace=True)
                # Insert the DataFrame into the database
                insert_data_to_db(conn, df, table_name)
            except Exception as e:
                print(f"Failed to process file {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")
    
    # Close the database connection
    if conn:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    process_csv_files()
