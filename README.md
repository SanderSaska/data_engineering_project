//et kontrollida kas tabelid on loodud
docker exec -it postgres psql -U airflow -d airflow
\dt

