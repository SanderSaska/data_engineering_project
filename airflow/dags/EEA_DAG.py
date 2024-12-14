from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from api.EEA_api import fetch_eea_data
import pandas as pd
import psycopg2

def transform_eea_data(ti):
    # Fetch the raw data from the task instance
    raw_data = ti.xcom_pull(task_ids='fetch_eea_data')

    # Apply your transformation logic here
    # Example: Convert data to a DataFrame and clean or modify it
    transformed_data = pd.DataFrame(raw_data)  # Example transformation
    # Add any necessary transformation logic here

    return transformed_data

def insert_eea_data(ti):
    # Fetch the transformed data from the task instance
    transformed_data = ti.xcom_pull(task_ids='transform_eea_data')

    # Connect to your PostgreSQL database and insert the data
    conn = psycopg2.connect("dbname=your_db user=your_user password=your_password host=localhost")
    cursor = conn.cursor()

    # Example insert logic - modify according to your data structure
    for _, row in transformed_data.iterrows():
        cursor.execute("INSERT INTO eea_table (column1, column2) VALUES (%s, %s)", (row['column1'], row['column2']))

    conn.commit()
    cursor.close()
    conn.close()

# Define the DAG for EEA API
dag = DAG(
    'eea_api_data_pipeline',
    description='Fetch, transform, and insert EEA API data into PostgreSQL',
    schedule_interval=None,  # Set your schedule here
    start_date=datetime(2024, 12, 12),
    catchup=False,
)

# Task to fetch EEA data
fetch_eea_task = PythonOperator(
    task_id='fetch_eea_data',
    python_callable=fetch_eea_data,
    dag=dag,
)

# Task to transform EEA data
transform_eea_task = PythonOperator(
    task_id='transform_eea_data',
    python_callable=transform_eea_data,
    provide_context=True,
    dag=dag,
)

# Task to insert transformed data into PostgreSQL
insert_eea_task = PythonOperator(
    task_id='insert_eea_data',
    python_callable=insert_eea_data,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
fetch_eea_task >> transform_eea_task >> insert_eea_task
