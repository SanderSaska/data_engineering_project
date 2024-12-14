//et kontrollida kas tabelid on loodud
docker exec -it postgres psql -U airflow -d airflow
\dt


Not ready yet, however:

1) docker-compose up --build
2) raw data - http://localhost:5050/browser/
3) air flow - http://localhost:8081/home
4) visualization - http://localhost:8501/

Problems:
1) moving tables with dbt
2) not all DAGs or airflow seem to work
3) data govenance OPM to do
4) Iceberg to improve


Idea:
1) Everything is orchestrated with Airflow
2) Data imported through APIs to FS
3) Data moved to postgres
4) data transformed into star schema with dbt
5) star schema moved to duckDB (possibly we would change the star schema creation to be in duckDB, however right now it works with postgres)
6) data in duckDB transformed and pushed to Neo4J to analyse and created relationships
7) Iceberg on top of duckDB to generate views 
8) streamlit to vizualise the data