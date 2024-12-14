import streamlit as st
import duckdb
import pandas as pd
import altair as alt
import requests

# DuckDB Database Path
DUCKDB_PATH = "data/my_database.duckdb"

# Iceberg REST API Endpoint
ICEBERG_API = "http://localhost:8181/v1/catalogs/my_catalog/namespaces/default/tables"

# Title
st.title("Data Visualization: DuckDB and Iceberg")

# Connect to DuckDB
def query_duckdb(query):
    """Run a query on DuckDB and return a DataFrame."""
    conn = duckdb.connect(DUCKDB_PATH)
    result = conn.execute(query).fetch_df()
    conn.close()
    return result

# Query Iceberg Table via REST API
def query_iceberg(table_name):
    """Fetch Iceberg metadata or snapshots using the REST API."""
    response = requests.get(f"{ICEBERG_API}/{table_name}/snapshots")
    if response.status_code == 200:
        return pd.DataFrame(response.json()["snapshots"])
    else:
        st.error("Failed to fetch Iceberg data.")
        return pd.DataFrame()

# Sidebar Options
st.sidebar.title("Data Source")
data_source = st.sidebar.radio("Select Data Source", ["DuckDB", "Iceberg"])

if data_source == "DuckDB":
    # DuckDB Sidebar Options
    st.sidebar.title("DuckDB Queries")
    options = st.sidebar.radio(
        "Select Visualization",
        [
            "Infections Over Time",
            "Average Temperature by Country",
            "Infections by Temperature Range",
        ],
    )

    # Query and Plot Based on Selection
    if options == "Infections Over Time":
        st.subheader("Infections Over Time")
        query = """
        SELECT
            datetime::DATE AS date,
            SUM(infection_cases) AS total_infections
        FROM infection_data
        GROUP BY date
        ORDER BY date;
        """
        df = query_duckdb(query)
        st.line_chart(df.set_index("date"))

    elif options == "Average Temperature by Country":
        st.subheader("Average Temperature by Country")
        query = """
        SELECT
            wd.country,
            AVG(wd.temperature) AS avg_temperature
        FROM weather_data wd
        GROUP BY wd.country
        ORDER BY avg_temperature DESC;
        """
        df = query_duckdb(query)
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("avg_temperature", title="Average Temperature"),
            y=alt.Y("country", sort="-x", title="Country"),
        )
        st.altair_chart(chart, use_container_width=True)

    elif options == "Infections by Temperature Range":
        st.subheader("Infections by Temperature Range")
        query = """
        SELECT
            CASE
                WHEN temperature < 0 THEN '< 0°C'
                WHEN temperature BETWEEN 0 AND 10 THEN '0-10°C'
                WHEN temperature BETWEEN 10 AND 20 THEN '10-20°C'
                ELSE '> 20°C'
            END AS temperature_range,
            SUM(infection_cases) AS total_infections
        FROM weather_data wd
        JOIN infection_data id
        ON wd.country = id.country AND wd.datetime = id.datetime
        GROUP BY temperature_range
        ORDER BY temperature_range;
        """
        df = query_duckdb(query)
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("temperature_range", title="Temperature Range"),
            y=alt.Y("total_infections", title="Total Infections"),
        )
        st.altair_chart(chart, use_container_width=True)

elif data_source == "Iceberg":
    # Iceberg Sidebar Options
    st.sidebar.title("Iceberg Queries")
    iceberg_options = st.sidebar.radio(
        "Select Iceberg Action",
        ["View Snapshots", "View Data"],
    )

    if iceberg_options == "View Snapshots":
        st.subheader("Iceberg Table Snapshots")
        table_name = st.text_input("Enter Iceberg Table Name", "weather_infection_data")
        if st.button("Fetch Snapshots"):
            snapshots_df = query_iceberg(table_name)
            if not snapshots_df.empty:
                st.dataframe(snapshots_df)
            else:
                st.warning("No snapshots found.")

    elif iceberg_options == "View Data":
        st.subheader("Query Iceberg Table Data")
        table_name = st.text_input("Enter Iceberg Table Name", "weather_infection_data")
        if st.button("Fetch Data"):
            # Example of querying an Iceberg table via DuckDB
            query = f"""
            SELECT *
            FROM 's3://warehouse/{table_name}'
            LIMIT 100;
            """
            try:
                df = query_duckdb(query)
                st.dataframe(df)
            except Exception as e:
                st.error(f"Failed to query Iceberg data: {e}")
