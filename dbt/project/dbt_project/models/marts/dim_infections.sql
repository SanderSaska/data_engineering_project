-- models/marts/dim_infections.sql
WITH staging_data AS (
    SELECT * FROM {{ ref('stg_infections') }}  -- Reference to the staging model
)
SELECT
    infection_id,
    inf_source,
    pathogen,
    pathogentype,
    pathogensubtype,
    age,
    inf_indicator
FROM staging_data;
