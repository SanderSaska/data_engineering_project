from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from neo4j import GraphDatabase

# Define a function to connect to Neo4j and run a query
def connect_to_neo4j():
    # Connection details
    uri = "bolt://neo4j:7687"  # Host and port of the Neo4j service
    username = "neo4j"
    password = "neo4jpassword"

    # Connect to Neo4j
    driver = GraphDatabase.driver(uri, auth=(username, password))

    # Create a sample node in Neo4j
    query = """
    CREATE (n:AirflowDemo {name: 'Neo4j from Airflow', created_at: $timestamp})
    """
    params = {"timestamp": datetime.utcnow().isoformat()}

    with driver.session() as session:
        session.run(query, **params)
        print("Node created successfully in Neo4j!")

    # Close the driver
    driver.close()

# Define the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 12, 13),
    "retries": 1,
}

dag = DAG(
    "neo4j_dag",
    default_args=default_args,
    description="A simple DAG to interact with Neo4j",
    schedule_interval="@daily",
)

# Define the Python task
create_neo4j_node = PythonOperator(
    task_id="create_neo4j_node",
    python_callable=connect_to_neo4j,
    dag=dag,
)

# Define the task order
create_neo4j_node

