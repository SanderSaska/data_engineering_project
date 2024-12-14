from py2neo import Graph, Node, Relationship
import duckdb

def duckdb_to_neo4j():
    # Connect to DuckDB
    duckdb_conn = duckdb.connect("/app/data/my_database.duckdb")  # Adjust the path as necessary

    # Query 1: Low temperature causes infections
    query_low_temp_infections = """
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
        wd.temperature < 10
        AND id.infection_cases > 100;
    """
    result_low_temp_infections = duckdb_conn.execute(query_low_temp_infections).fetchall()

    # Query 2: High humidity causes respiratory issues
    query_high_humidity_respiratory = """
    SELECT
        wd.country,
        wd.datetime,
        wd.humidity,
        rd.respiratory_issues
    FROM
        weather_data wd
    JOIN
        respiratory_data rd
    ON
        wd.country = rd.country AND wd.datetime = rd.datetime
    WHERE
        wd.humidity > 80
        AND rd.respiratory_issues > 50;
    """
    result_high_humidity_respiratory = duckdb_conn.execute(query_high_humidity_respiratory).fetchall()

    # Query 3: High pollution causes asthma cases
    query_high_pollution_asthma = """
    SELECT
        wd.country,
        wd.datetime,
        wd.pollution_level,
        ad.asthma_cases
    FROM
        weather_data wd
    JOIN
        asthma_data ad
    ON
        wd.country = ad.country AND wd.datetime = ad.datetime
    WHERE
        wd.pollution_level > 75
        AND ad.asthma_cases > 30;
    """
    result_high_pollution_asthma = duckdb_conn.execute(query_high_pollution_asthma).fetchall()

    # Connect to Neo4j
    graph = Graph("bolt://neo4j:7687", auth=("neo4j", "neo4jpassword"))

    # Relation 1: Insert Low Temperature -> Infections
    for row in result_low_temp_infections:
        country, datetime, temperature, infection_cases = row
        country_node = Node("Country", name=country)
        graph.merge(country_node, "Country", "name")
        event_node = Node(
            "Event",
            datetime=str(datetime),
            temperature=temperature,
            infections=infection_cases,
        )
        graph.create(event_node)
        causes_rel = Relationship(event_node, "CAUSES", country_node, type="LowTemp_Infections")
        graph.create(causes_rel)

    # Relation 2: Insert High Humidity -> Respiratory Issues
    for row in result_high_humidity_respiratory:
        country, datetime, humidity, respiratory_issues = row
        country_node = Node("Country", name=country)
        graph.merge(country_node, "Country", "name")
        event_node = Node(
            "Event",
            datetime=str(datetime),
            humidity=humidity,
            respiratory_issues=respiratory_issues,
        )
        graph.create(event_node)
        causes_rel = Relationship(event_node, "CAUSES", country_node, type="HighHumidity_RespiratoryIssues")
        graph.create(causes_rel)

    # Relation 3: Insert High Pollution -> Asthma Cases
    for row in result_high_pollution_asthma:
        country, datetime, pollution_level, asthma_cases = row
        country_node = Node("Country", name=country)
        graph.merge(country_node, "Country", "name")
        event_node = Node(
            "Event",
            datetime=str(datetime),
            pollution_level=pollution_level,
            asthma_cases=asthma_cases,
        )
        graph.create(event_node)
        causes_rel = Relationship(event_node, "CAUSES", country_node, type="HighPollution_AsthmaCases")
        graph.create(causes_rel)

    print("All data successfully loaded into Neo4j.")
