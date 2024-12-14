from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    'insert_data_postgres_to_duckdb',
    default_args=default_args,
    description='Inserts raw data from PostgreSQL to DuckDB staging using dbt',
    schedule_interval=None,  # Set as per your needs, e.g., '0 0 * * *' for daily
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Task: Run dbt models for staging
    run_staging = BashOperator(
        task_id='run_dbt_staging',
        bash_command="""
        export DBT_TARGET=postgres_source &&
        dbt run --models staging
        """,
        env={'DBT_TARGET': 'postgres_source'},  # Ensure the correct target is set
    )
