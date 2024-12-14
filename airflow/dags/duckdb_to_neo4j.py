from py2neo import Graph, Node, Relationship
import duckdb

def duckdb_to_neo4j():
    # Connect to DuckDB
    duckdb_conn = duckdb.connect("/app/data/my_database.duckdb")  # Adjust path to match your setup

    # Query DuckDB
    query = """
    SELECT
        wd.country,
        wd.datetime,
        wd.temperature,
        id.infection_cases
    FROM
        weather_data wd
    JOIN
        infection_data id
    ON
        wd.country = id.country AND wd.datetime = id.datetime
    WHERE
        wd.temperature < 10  -- Example threshold for low temperature
        AND id.infection_cases > 100;  -- Example threshold for infections
    """
    result = duckdb_conn.execute(query).fetchall()

    # Connect to Neo4j
    graph = Graph("bolt://neo4j:7687", auth=("neo4j", "neo4jpassword"))  # Update with your credentials

    # Insert data into Neo4j
    for row in result:
        country, datetime, temperature, infection_cases = row

        # Create or find Country node
        country_node = Node("Country", name=country)
        graph.merge(country_node, "Country", "name")

        # Create Event node
        event_node = Node(
            "Event",
            datetime=str(datetime),
            temperature=temperature,
            infections=infection_cases,
        )
        graph.create(event_node)

        # Create relationship
        causes_rel = Relationship(event_node, "CAUSES", country_node)
        graph.create(causes_rel)

    print("Data successfully loaded into Neo4j.")
