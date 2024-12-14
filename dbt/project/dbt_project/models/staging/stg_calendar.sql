-- models/staging/stg_calendar.sql
WITH raw_calendar AS (
    SELECT *
    FROM {{ source('raw_data', 'calendar') }}
)
SELECT
    id,
    calendar_year,
    calendar_quarter,
    calendar_month,
    calendar_week,
    calendar_day,
    date_time,
    calendar_year_week
FROM raw_calendar
WHERE date_time IS NOT NULL;  -- Filter out any null values
