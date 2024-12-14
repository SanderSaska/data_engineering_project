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
    'create_star_schema',
    default_args=default_args,
    description='Creates a star schema in DuckDB using dbt',
    schedule_interval=None,  # Set as per your needs
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Task: Run dbt models for star schema
    run_star_schema = BashOperator(
        task_id='run_dbt_marts',
        bash_command="""
        export DBT_TARGET=duckdb_target &&
        dbt run --models marts
        """,
        env={'DBT_TARGET': 'duckdb_target'},  # Ensure the correct target is set
    )
