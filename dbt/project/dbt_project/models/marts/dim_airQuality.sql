-- models/marts/dim_air_quality.sql
WITH staging_data AS (
    SELECT * FROM {{ ref('stg_air_quality') }}  -- Reference to the staging model
)
SELECT
    id AS air_quality_id,
    Samplingpoint,
    Pollutant,
    Unit,
    AggType
FROM staging_data;
