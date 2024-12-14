from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from api.erviss_api import fetch_erviss_data
import pandas as pd
import psycopg2

def transform_erviss_data(ti):
    # Fetch the raw data from the task instance
    raw_data = ti.xcom_pull(task_ids='fetch_erviss_data')

    # Apply your transformation logic here
    # Example: Convert data to a DataFrame and clean or modify it
    transformed_data = pd.DataFrame(raw_data)  # Example transformation
    # Add any necessary transformation logic here

    return transformed_data

def insert_erviss_data(ti):
    # Fetch the transformed data from the task instance
    transformed_data = ti.xcom_pull(task_ids='transform_erviss_data')

    # Connect to your PostgreSQL database and insert the data
    conn = psycopg2.connect("dbname=your_db user=your_user password=your_password host=localhost")
    cursor = conn.cursor()

    # Example insert logic - modify according to your data structure
    for _, row in transformed_data.iterrows():
        cursor.execute("INSERT INTO erviss_table (column1, column2) VALUES (%s, %s)", (row['column1'], row['column2']))

    conn.commit()
    cursor.close()
    conn.close()

# Define the DAG for Erviss API
dag = DAG(
    'erviss_api_data_pipeline',
    description='Fetch, transform, and insert Erviss API data into PostgreSQL',
    schedule_interval=None,  # Set your schedule here
    start_date=datetime(2024, 12, 12),
    catchup=False,
)

# Task to fetch Erviss data
fetch_erviss_task = PythonOperator(
    task_id='fetch_erviss_data',
    python_callable=fetch_erviss_data,
    dag=dag,
)

# Task to transform Erviss data
transform_erviss_task = PythonOperator(
    task_id='transform_erviss_data',
    python_callable=transform_erviss_data,
    provide_context=True,
    dag=dag,
)

# Task to insert transformed data into PostgreSQL
insert_erviss_task = PythonOperator(
    task_id='insert_erviss_data',
    python_callable=insert_erviss_data,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
fetch_erviss_task >> transform_erviss_task >> insert_erviss_task
