from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from api.geo_api import fetch_geo_data
import pandas as pd
import psycopg2

def transform_geo_data(ti):
    # Fetch the raw data from the task instance
    raw_data = ti.xcom_pull(task_ids='fetch_geo_data')

    # Apply your transformation logic here
    # Example: Convert data to a DataFrame and clean or modify it
    transformed_data = pd.DataFrame(raw_data)  # Example transformation
    # Add any necessary transformation logic here

    return transformed_data

def insert_geo_data(ti):
    # Fetch the transformed data from the task instance
    transformed_data = ti.xcom_pull(task_ids='transform_geo_data')

    # Connect to your PostgreSQL database and insert the data
    conn = psycopg2.connect("dbname=your_db user=your_user password=your_password host=localhost")
    cursor = conn.cursor()

    # Example insert logic - modify according to your data structure
    for _, row in transformed_data.iterrows():
        cursor.execute("INSERT INTO geo_table (column1, column2) VALUES (%s, %s)", (row['column1'], row['column2']))

    conn.commit()
    cursor.close()
    conn.close()

# Define the DAG for Geo API
dag = DAG(
    'geo_api_data_pipeline',
    description='Fetch, transform, and insert Geo API data into PostgreSQL',
    schedule_interval=None,  # Set your schedule here
    start_date=datetime(2024, 12, 12),
    catchup=False,
)

# Task to fetch Geo data
fetch_geo_task = PythonOperator(
    task_id='fetch_geo_data',
    python_callable=fetch_geo_data,
    dag=dag,
)

# Task to transform Geo data
transform_geo_task = PythonOperator(
    task_id='transform_geo_data',
    python_callable=transform_geo_data,
    provide_context=True,
    dag=dag,
)

# Task to insert transformed data into PostgreSQL
insert_geo_task = PythonOperator(
    task_id='insert_geo_data',
    python_callable=insert_geo_data,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
fetch_geo_task >> transform_geo_task >> insert_geo_task
