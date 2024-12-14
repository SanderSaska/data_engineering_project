#!/bin/bash

# Define the path to the DuckDB database file
DB_FILE="/app/data/my_database.duckdb"

# Check if the database already exists
if [ ! -f "$DB_FILE" ]; then
  echo "DuckDB database not found. Creating a new one at $DB_FILE"
  # Create an empty DuckDB database by simply launching DuckDB with the database file
  duckdb $DB_FILE "SELECT 'Database created successfully' AS message;"
else
  echo "DuckDB database found at $DB_FILE. Using existing database."
fi

# Execute the command passed to the container (default is to start DuckDB CLI)
exec "$@"
