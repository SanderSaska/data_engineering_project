-- Create Tables

-- Air quality tables

CREATE TABLE airQuality (
    id SERIAL PRIMARY KEY,
    Samplingpoint TEXT,
    Pollutant INTEGER,
    "Start" TIMESTAMP,
    "End" TIMESTAMP,
    "Value" DECIMAL(38, 18),
    Unit TEXT,
    AggType TEXT,
    Validity INTEGER,
    Verification INTEGER,
    ResultTime TIMESTAMP,
    DataCapture DECIMAL(38, 18),
    FkObservationLog TEXT,
    "fileName" TEXT
);

CREATE TABLE airQualityDescriptors (
    id INTEGER PRIMARY KEY,
    Label TEXT,
    "Definition" TEXT,
    Notation TEXT
);

-- Calendar

CREATE TABLE calendar (
    id INTEGER PRIMARY KEY,
    "Year" INTEGER,
    "Quarter" INTEGER,
    "Month" INTEGER,
    "Week" INTEGER,
    "Day" INTEGER,
    Date_time TIMESTAMP
);

-- Weather-related tables

CREATE TABLE country (
    id INTEGER PRIMARY KEY,
    "name" TEXT,
    lat NUMERIC,
    lon NUMERIC,
    country_code TEXT
);

CREATE TABLE weather (
    id INTEGER PRIMARY KEY,
    lat NUMERIC,
    lon NUMERIC,
    tz TEXT,
    "date" TEXT,
    units TEXT,
    cloud_cover_afternoon  INTEGER,
    humidity_afternoon INTEGER,
    precipitation_total INTEGER,
    temperature_min NUMERIC,
    temperature_max NUMERIC,
    temperature_afternoon NUMERIC,
    temperature_night NUMERIC,
    temperature_evening NUMERIC,
    temperature_morning NUMERIC,
    pressure_afternoon INTEGER,
    wind_max_speed NUMERIC,
    wind_max_direction NUMERIC,
    country TEXT,
    country_code TEXT
);

-- Infection-related tables

CREATE TABLE ILIARIRates (
    id INTEGER PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

CREATE TABLE SARIRates (
    id INTEGER PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

CREATE TABLE SARITestsDetectionPositivity (
    id INTEGER PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

CREATE TABLE activityFluTypeSubtype (
    id INTEGER PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

CREATE TABLE nonSentinelSeverity (
    id INTEGER PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

CREATE TABLE nonSentinelTestsDetections (
    id INTEGER PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

CREATE TABLE sentinelTestsDetectionsPositivity (
    id INTEGER PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

CREATE TABLE sequencingVolumeDetectablePrevalence (
    id INTEGER PRIMARY KEY,
    survtype TEXT,
    datasource TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC,
    detectableprevalence TEXT
);

CREATE TABLE variants (
    id INTEGER PRIMARY KEY,
    survtype TEXT,
    datasource TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    variant TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

-- Data Ingestion

-- TODO: FROM: add correct path

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
