-- Create Tables

--TODO: 
-- * Muuta veergude nimed ja tüübid vastavaks
-- * Lisada veerud mõnele tabelile

-- Weather-related tables
CREATE TABLE airQuality (
    "ID" INTEGER PRIMARY KEY,
    "Samplingpoint" TEXT,
    "Pollutant" INTEGER,
    "Start" TIMESTAMP,
    "End" TIMESTAMP,
    "Value" DECIMAL(38, 18),
    "Unit" TEXT,
    "AggType" TEXT,
    "Validity" INTEGER,
    "Verification" INTEGER,
    "ResultTime" TIMESTAMP,
    "DataCapture" DECIMAL(38, 18),
    "FkObservationLog" TEXT,
    "FileName" TEXT
);

CREATE TABLE airQualityDescriptors (
    "ID" SERIAL PRIMARY KEY,
    URI TEXT,
    Label TEXT,
    "Definition" TEXT,
    Notation TEXT,
    "Status" TEXT
);

CREATE TABLE calendar (
    "ID" SERIAL PRIMARY KEY,
    "Year" INTEGER,
    "Quarter" INTEGER,
    "Month" INTEGER,
    "Week" INTEGER,
    "Day" INTEGER,  -- Fixed the typo here
    Date_time TIMESTAMP
);

CREATE TABLE country (
    "ID" SERIAL PRIMARY KEY,
    "Name" TEXT,
    Lat NUMERIC,
    Lon NUMERIC,
    Country_code TEXT
);

CREATE TABLE weather (
    "ID" SERIAL PRIMARY KEY,
    Temperature NUMERIC,  -- Example column, update as needed
    Humidity NUMERIC,     -- Example column, update as needed
    WindSpeed NUMERIC     -- Example column, update as needed
);

CREATE TABLE ILIARIRates (
    "ID" SERIAL PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

CREATE TABLE SARIRates (
    "ID" SERIAL PRIMARY KEY,
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC
);

CREATE TABLE SARITestsDetectionPositivity (
    "ID" SERIAL PRIMARY KEY,
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
    "ID" SERIAL PRIMARY KEY,
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
    "ID" SERIAL PRIMARY KEY,
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
    "ID" SERIAL PRIMARY KEY,
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
    "ID" SERIAL PRIMARY KEY,
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
    "ID" SERIAL PRIMARY KEY,
    survtype TEXT,
    datasource TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    indicator TEXT,
    age TEXT,
    "value" NUMERIC,
    detectableprevalence NUMERIC
);

CREATE TABLE variants (
    "ID" SERIAL PRIMARY KEY,
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
/*
COPY airQuality (Samplingpoint, Pollutant, Start, End, Value, Unit, AggType, Validity, Verification, ResultTime, DataCapture, FkObservationLog)
   FROM '/path/to/your/air_quality.csv'
   DELIMITER ','
   CSV HEADER;

COPY ILIARIRates (survtype, countryname, yearweek, indicator, age, value)
   FROM '/path/to/your/ILIARIRates.csv'
   DELIMITER ','
   CSV HEADER;

COPY SARIRates (survtype, countryname, yearweek, indicator, age, value)
   FROM '/path/to/your/SARIRates.csv'
   DELIMITER ','
   CSV HEADER;

COPY SARITestsDetectionPositivity (survtype, countryname, yearweek, pathogen, pathogentype, pathogensubtype, indicator, age, value)
   FROM '/path/to/your/SARITestsDetectionsPositivity.csv'
   DELIMITER ','
   CSV HEADER;

COPY activityFluTypeSubtype (survtype, countryname, yearweek, pathogen, pathogentype, pathogensubtype, indicator, age, value)
   FROM '/path/to/your/activityFluTypeSubtype.csv'
   DELIMITER ','
   CSV HEADER;

COPY nonSentinelSeverity (survtype, countryname, yearweek, pathogen, pathogentype, indicator, age, value)
   FROM '/path/to/your/nonSentinelSeverity.csv'
   DELIMITER ','
   CSV HEADER;

COPY nonSentinelTestsDetections (survtype, countryname, yearweek, pathogen, pathogentype, pathogensubtype, indicator, age, value)
   FROM '/path/to/your/nonSentinelTestsDetections.csv'
   DELIMITER ','
   CSV HEADER;

COPY sentinelTestsDetectionsPositivity (survtype, countryname, yearweek, pathogen, pathogentype, pathogensubtype, indicator, age, value)
   FROM '/path/to/your/sentinelTestsDetectionsPositivity.csv'
   DELIMITER ','
   CSV HEADER;

COPY sequencingVolumeDetectablePrevalence (survtype, datasource, countryname, yearweek, pathogen, indicator, age, value, detectableprevalence)
   FROM '/path/to/your/sequencingVolumeDetectablePrevalence.csv'
   DELIMITER ','
   CSV HEADER;

COPY variants (survtype, datasource, countryname, yearweek, pathogen, variant, indicator, age, value)
   FROM '/path/to/your/variants.csv'
   DELIMITER ','
   CSV HEADER;
