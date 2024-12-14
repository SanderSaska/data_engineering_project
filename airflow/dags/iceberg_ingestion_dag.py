from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from ingest_to_iceberg import ingest_to_iceberg  # Import the ingestion function

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
}

# DAG definition
with DAG(
    'iceberg_ingestion_pipeline',
    default_args=default_args,
    description='Ingest data into Iceberg and query it',
    schedule_interval='@daily',
    start_date=datetime(2024, 12, 14),
    catchup=False,
) as dag:

    # Task: Ingest data into Iceberg
    ingest_data = PythonOperator(
        task_id='ingest_to_iceberg',
        python_callable=ingest_to_iceberg  # Directly call the function
    )

    ingest_data
