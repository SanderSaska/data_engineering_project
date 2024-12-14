import os
import pandas as pd
import psycopg2
import argparse

script_dir = os.path.dirname(os.path.abspath(__file__))
parquet_dir = os.path.join(script_dir, "../../raw_data/EEA_Downloads/ParquetFiles")

db_config = {
    'dbname': 'raw_data',              
    'user': 'airflow',                
    'password': 'airflow',            
    'host': 'localhost',               
    'port': '5432'                    
}

def connect_to_db():
    try:
        conn = psycopg2.connect(**db_config)
        print("Successfully connected to the database.")
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

def insert_data_to_db(conn, df, file_name):
    try:
        cursor = conn.cursor()
        insert_query = '''
            INSERT INTO airQuality (Samplingpoint, Pollutant, time_start, time_end, pollutant_value, Unit, AggType, Validity, Verification, ResultTime, DataCapture, FkObservationLog, file_Name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        for index, row in df.iterrows():
            cursor.execute(insert_query, (
                row['Samplingpoint'], row['Pollutant'], pd.to_datetime(row['Start']), pd.to_datetime(row['End']),
                float(row['Value']) if pd.notnull(row['Value']) else None,
                row['Unit'], row['AggType'], int(row['Validity']) if pd.notnull(row['Validity']) else None,
                int(row['Verification']) if pd.notnull(row['Verification']) else None,
                pd.to_datetime(row['ResultTime']), float(row['DataCapture']) if pd.notnull(row['DataCapture']) else None,
                row['FkObservationLog'], file_name
            ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Failed to insert records from {file_name}: {e}")

def process_parquet_files(filelist):
    conn = connect_to_db()
    if conn is None:
        return
    for file_path in filelist:
        try:
            df = pd.read_parquet(file_path)
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
            insert_data_to_db(conn, df, file_path)
        except Exception as e:
            print(f"Failed to process file {file_path}: {e}")
    if conn:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest EEA Parquet files into the database.")
    parser.add_argument('--files', nargs='*', default=[os.path.join(parquet_dir, f) for f in os.listdir(parquet_dir) if f.endswith('.parquet')])
    args = parser.parse_args()
    process_parquet_files(args.files)
