-- models/marts/f_data.sql
WITH all_data AS (
    SELECT 
      cal.id as cal_id, 
      we.id as we_id, 
      co.id as co_id, 
      aq.id as aq_id, 
      infect.infection_id as infect_id,
      aq.pollutant_value as pollutant_value,
      infect.inf_value as infection_value,
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
    FROM {{ ref('stg_calendar') }} cal
    JOIN {{ ref('stg_weather') }} we on cal.date_time = we.weather_date
    JOIN {{ ref('stg_country') }} co on co.country_name = we.country_name
    JOIN {{ ref('stg_airQuality') }} aq on left(aq.Samplingpoint, 2) = co.country_code and aq.time_start = cal.date_time
    JOIN {{ ref('stg_infections') }} infect on infect.yearweek = cal.calendar_year_week and infect.countryname = co.country_name
)
SELECT
  cal.calendar_id,
  we.weather_id,
  co.country_id,
  aq.air_quality_id,
  infect.infection_id,
  ad.pollutant_value,
  ad.infection_value, 
  ad.temperature_2m_max,
  ad.temperature_2m_min,
  ad.apparent_temperature_max,
  ad.apparent_temperature_min,
  ad.precipitation_sum,
  ad.rain_sum,
  ad.showers_sum,
  ad.snowfall_sum,
  ad.wind_speed_10m_max,
  ad.wind_gusts_10m_max
FROM all_data ad
JOIN {{ ref('dim_calendar') }} cal on ad.cal_id = cal.calendar_id
JOIN {{ ref('dim_weather') }} we on ad.we_id = we.weather_id
JOIN {{ ref('dim_country') }} co on ad.co_id = co.country_id
JOIN {{ ref('dim_airQuality') }} aq on ad.aq_id = aq.air_quality_id
JOIN {{ ref('dim_infections') }} infect on ad.infect_id = infect.infection_id;