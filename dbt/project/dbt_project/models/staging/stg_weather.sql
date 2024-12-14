-- models/staging/stg_weather.sql
WITH raw_weather_data AS (
    SELECT
        id,
        weather_code,
        country_name,
        weather_date,
        temperature_2m_max,
        temperature_2m_min,
        apparent_temperature_max,
        apparent_temperature_min,
        precipitation_sum,
        rain_sum,
        showers_sum,
        snowfall_sum,
        wind_speed_10m_max,
        wind_gusts_10m_max
    FROM {{ source('raw_data', 'weather') }}
)
SELECT
    id,
    weather_date,
    country_name,
    weather_code,
    temperature_2m_max,
    temperature_2m_min,
    apparent_temperature_max,
    apparent_temperature_min,
    precipitation_sum,
    rain_sum,
    showers_sum,
    snowfall_sum,
    wind_speed_10m_max,
    wind_gusts_10m_max
FROM raw_weather_data;
