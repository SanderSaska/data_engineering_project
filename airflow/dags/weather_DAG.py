from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from api.OpenWeatherMap_api import fetch_weather_data
import pandas as pd
import psycopg2

def transform_weather_data(ti):
    # Fetch the raw data from the task instance
    raw_data = ti.xcom_pull(task_ids='fetch_weather_data')

    # Apply your transformation logic here
    # Example: Convert data to a DataFrame and clean or modify it
    transformed_data = pd.DataFrame(raw_data)  # Example transformation
    # Add any necessary transformation logic here

    return transformed_data

def insert_weather_data(ti):
    # Fetch the transformed data from the task instance
    transformed_data = ti.xcom_pull(task_ids='transform_weather_data')

    # Connect to your PostgreSQL database and insert the data
    conn = psycopg2.connect("dbname=your_db user=your_user password=your_password host=localhost")
    cursor = conn.cursor()

    # Example insert logic - modify according to your data structure
    for _, row in transformed_data.iterrows():
        cursor.execute("INSERT INTO weather_table (column1, column2) VALUES (%s, %s)", (row['column1'], row['column2']))

    conn.commit()
    cursor.close()
    conn.close()

# Define the DAG for Weather API
dag = DAG(
    'weather_api_data_pipeline',
    description='Fetch, transform, and insert Weather API data into PostgreSQL',
    schedule_interval=None,  # Set your schedule here
    start_date=datetime(2024, 12, 12),
    catchup=False,
)

# Task to fetch weather data
fetch_weather_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    dag=dag,
)

# Task to transform weather data
transform_weather_task = PythonOperator(
    task_id='transform_weather_data',
    python_callable=transform_weather_data,
    provide_context=True,
    dag=dag,
)

# Task to insert transformed data into PostgreSQL
insert_weather_task = PythonOperator(
    task_id='insert_weather_data',
    python_callable=insert_weather_data,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
fetch_weather_task >> transform_weather_task >> insert_weather_task
