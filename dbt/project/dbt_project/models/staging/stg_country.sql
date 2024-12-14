-- models/staging/stg_country.sql
WITH raw_country AS (
    SELECT *
    FROM {{ source('raw_data', 'country') }}
)
SELECT
    id,
    name as country_name,
    lat,
    lon,
    country_code
FROM raw_country
WHERE lat IS NOT NULL AND lon IS NOT NULL;  -- Filter out incomplete records
