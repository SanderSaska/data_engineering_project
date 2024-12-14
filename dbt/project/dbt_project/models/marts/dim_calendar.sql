-- models/marts/dim_calendar.sql
WITH staging_data AS (
    SELECT * FROM {{ ref('stg_calendar') }}  -- Reference to the staging model
)
SELECT
    id AS calendar_id,
    calendar_year,
    calendar_quarter,
    calendar_month,
    calendar_week,
    calendar_day,
    date_time,
    calendar_year_week
FROM staging_data
