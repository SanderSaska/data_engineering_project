-- Create Tables

-- Air quality tables

CREATE TABLE airQuality (
    id SERIAL PRIMARY KEY,
    Samplingpoint TEXT,
    Pollutant INTEGER,
    time_start TIMESTAMP not null,
    time_end TIMESTAMP not null,
    pollutant_value DECIMAL(38, 18),
    Unit TEXT,
    AggType TEXT,
    Validity INTEGER,
    Verification INTEGER,
    ResultTime TIMESTAMP,
    DataCapture DECIMAL(38, 18),
    FkObservationLog TEXT,
    file_Name TEXT
);

CREATE TABLE airQualityDescriptors (
    id INTEGER PRIMARY KEY,
    Label TEXT,
    label_definition TEXT,
    Notation TEXT
);

-- Calendar

CREATE TABLE calendar (
    id SERIAL PRIMARY KEY,
    calendar_year INTEGER,
    calendar_quarter INTEGER,
    calendar_month INTEGER,
    calendar_week INTEGER,
    calendar_day INTEGER,
    date_time TIMESTAMP
);

-- Weather-related tables

CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    "name" TEXT NOT NULL,
    lat NUMERIC NOT NULL CHECK (lat >= -90 AND lat <= 90),
    lon NUMERIC NOT NULL CHECK (lon >= -180 AND lon <= 180),
    country_code TEXT NOT NULL UNIQUE
);

-- muutub


-- Infection-related tables

CREATE TABLE ILIARIRates (
    id SERIAL PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    inf_indicator TEXT,
    age TEXT,
    inf_value NUMERIC
);

CREATE TABLE SARIRates (
    id SERIAL PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    inf_indicator TEXT,
    age TEXT,
    inf_value NUMERIC
);

CREATE TABLE SARITestsDetectionPositivity (
    id SERIAL PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    inf_indicator TEXT,
    age TEXT,
    inf_value NUMERIC
);

CREATE TABLE activityFluTypeSubtype (
    id SERIAL PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    inf_indicator TEXT,
    age TEXT,
    inf_value NUMERIC
);

CREATE TABLE nonSentinelSeverity (
    id SERIAL PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    inf_indicator TEXT,
    age TEXT,
    inf_value NUMERIC
);

CREATE TABLE nonSentinelTestsDetections (
    id SERIAL PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    inf_indicator TEXT,
    age TEXT,
    inf_value NUMERIC
);

CREATE TABLE sentinelTestsDetectionsPositivity (
    id SERIAL PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    inf_indicator TEXT,
    age TEXT,
    inf_value NUMERIC
);

CREATE TABLE sequencingVolumeDetectablePrevalence (
    id SERIAL PRIMARY KEY,
    survtype TEXT,
    datasource TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    inf_indicator TEXT,
    age TEXT,
    inf_value NUMERIC,
    detectableprevalence TEXT
);

CREATE TABLE variants (
    id SERIAL PRIMARY KEY,
    survtype TEXT,
    datasource TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    variant TEXT,
    inf_indicator TEXT,
    age TEXT,
    inf_value NUMERIC
);

-- Data Ingestion

-- -- airQuality
-- COPY airQuality ("Samplingpoint", "Pollutant", "Start", "End", "Value", "Unit", "AggType", "Validity", "Verification", "ResultTime", "DataCapture", "FkObservationLog", "fileName")
--     FROM '/path/to/your/air_quality.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- airQualityDescriptors
-- COPY airQualityDescriptors ("Label", "Definition", "Notation")
--     FROM '/path/to/your/air_quality_descriptors.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- country
-- COPY country ("name", "lat", "lon", "country_code")
--     FROM '/path/to/your/country.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- weather
-- COPY weather ("lat", "lon", "tz", "date", "units", "cloud_cover_afternoon", "humidity_afternoon", "precipitation_total", "temperature_min", "temperature_max", "temperature_afternoon", "temperature_night", "temperature_evening", "temperature_morning", "pressure_afternoon", "wind_max_speed", "wind_max_direction", "country", "country_code")
--     FROM '/path/to/your/weather.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- ILIARIRates
-- COPY ILIARIRates ("survtype", "countryname", "yearweek", "indicator", "age", "value")
--     FROM '/path/to/your/ILIARI_rates.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- SARIRates
-- COPY SARIRates ("survtype", "countryname", "yearweek", "indicator", "age", "value")
--     FROM '/path/to/your/SARI_rates.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- SARITestsDetectionPositivity
-- COPY SARITestsDetectionPositivity ("survtype", "countryname", "yearweek", "pathogen", "pathogentype", "pathogensubtype", "indicator", "age", "value")
--     FROM '/path/to/your/SARI_tests_detection_positivity.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- activityFluTypeSubtype
-- COPY activityFluTypeSubtype ("survtype", "countryname", "yearweek", "pathogen", "pathogentype", "pathogensubtype", "indicator", "age", "value")
--     FROM '/path/to/your/activity_flu_type_subtype.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- nonSentinelSeverity
-- COPY nonSentinelSeverity ("survtype", "countryname", "yearweek", "pathogen", "pathogentype", "indicator", "age", "value")
--     FROM '/path/to/your/non_sentinel_severity.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- nonSentinelTestsDetections
-- COPY nonSentinelTestsDetections ("survtype", "countryname", "yearweek", "pathogen", "pathogentype", "pathogensubtype", "indicator", "age", "value")
--     FROM '/path/to/your/non_sentinel_tests_detections.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- sentinelTestsDetectionsPositivity
-- COPY sentinelTestsDetectionsPositivity ("survtype", "countryname", "yearweek", "pathogen", "pathogentype", "pathogensubtype", "indicator", "age", "value")
--     FROM '/path/to/your/sentinel_tests_detections_positivity.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- sequencingVolumeDetectablePrevalence
-- COPY sequencingVolumeDetectablePrevalence ("survtype", "datasource", "countryname", "yearweek", "pathogen", "indicator", "age", "value", "detectableprevalence")
--     FROM '/path/to/your/sequencing_volume_detectable_prevalence.csv'
--     DELIMITER ','
--     CSV HEADER;

-- -- variants
-- COPY variants ("survtype", "datasource", "countryname", "yearweek", "pathogen", "variant", "indicator", "age", "value")
--     FROM '/path/to/your/variants.csv'
--     DELIMITER ','
--     CSV HEADER;
