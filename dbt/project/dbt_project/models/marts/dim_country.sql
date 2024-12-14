-- models/marts/dim_country.sql
WITH staging_data AS (
    SELECT * FROM {{ ref('stg_country') }}  -- Reference to the staging model
)
SELECT
    id AS country_id,
    country_name,
    lat,
    lon,
    country_code
FROM staging_data
