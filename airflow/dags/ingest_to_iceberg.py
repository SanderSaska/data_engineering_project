from pyspark.sql import SparkSession

def ingest_to_iceberg():
    # Initialize Spark with Iceberg support
    spark = SparkSession.builder \
        .config("spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.my_catalog.type", "hadoop") \
        .config("spark.sql.catalog.my_catalog.warehouse", "s3://warehouse/") \
        .getOrCreate()

    # Load CSV data
    weather_data = spark.read.csv("data/weather_data.csv", header=True, inferSchema=True)
    pollution_data = spark.read.csv("data/pollution_data.csv", header=True, inferSchema=True)
    infection_data = spark.read.csv("data/infection_data.csv", header=True, inferSchema=True)

    # Combine datasets
    combined_data = weather_data.join(pollution_data, ["country", "datetime"]) \
                                .join(infection_data, ["country", "datetime"])

    # Write data to Iceberg table
    combined_data.writeTo("my_catalog.default.weather_infection_data").append()

    print("Data successfully ingested into Iceberg.")
