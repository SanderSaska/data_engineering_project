-- models/staging/stg_air_quality.sql
WITH raw_air_quality AS (
    SELECT *
    FROM {{ source('raw_data', 'airquality') }}
)
SELECT
    id,
    Samplingpoint,
    Pollutant,
    time_start,
    time_end,
    pollutant_value,
    Unit,
    AggType,
    Validity,
    Verification,
    ResultTime,
    DataCapture,
    FkObservationLog,
    file_Name
FROM raw_air_quality
WHERE pollutant_value IS NOT NULL