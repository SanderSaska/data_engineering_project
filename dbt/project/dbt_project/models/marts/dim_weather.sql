-- models/marts/dim_weather.sql
WITH stg_weather_clean AS (
    SELECT *
    FROM {{ ref('stg_weather') }}  -- Reference the cleaned staging table (stg_weather)
)
SELECT
    id AS weather_id,  -- Create a unique identifier for this dimension
    weather_code
FROM stg_weather_clean