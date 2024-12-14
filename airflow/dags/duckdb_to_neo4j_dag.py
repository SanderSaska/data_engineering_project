from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from duckdb_to_neo4j import duckdb_to_neo4j  # Import the function

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
}

with DAG('duckdb_to_neo4j_pipeline',
         default_args=default_args,
         description='Pipeline from DuckDB to Neo4j',
         schedule_interval='@daily',
         start_date=datetime(2024, 12, 14),
         catchup=False) as dag:

    transfer_task = PythonOperator(
        task_id='transfer_duckdb_to_neo4j',
        python_callable=duckdb_to_neo4j
    )

    transfer_task
