-- Create Tables

--TODO: 
-- * Muuta veergude nimed ja tüübid vastavaks
-- * Lisada veerud mõnele tabelile

-- Weather-related tables
CREATE TABLE airQuality (
    Samplingpoint TEXT,
    Pollutant TEXT,
    Start TIMESTAMP,
    End TIMESTAMP,
    Value NUMERIC,
    Unit TEXT,
    AggType TEXT,
    Validity TEXT,
    Verification TEXT,
    ResultTime TIMESTAMP,
    DataCapture TIMESTAMP,
    FkObservationLog INTEGER
);

CREATE TABLE AirQualityDescriptors (
    URI TEXT,
    Label TEXT,
    Definition TEXT,
    Notation TEXT,
    Status TEXT
);

CREATE TABLE calendar (
    -- Define columns if provided
);

CREATE TABLE country (
    -- Define columns if provided
);

CREATE TABLE weather (
    -- Define columns if provided
);

-- Infections-related tables
CREATE TABLE ILIARIRates (
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    indicator TEXT,
    age TEXT,
    value NUMERIC
);

CREATE TABLE SARIRates (
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    indicator TEXT,
    age TEXT,
    value NUMERIC
);

CREATE TABLE SARITestsDetectionPositivity (
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    indicator TEXT,
    age TEXT,
    value NUMERIC
);

CREATE TABLE activityFluTypeSubtype (
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    indicator TEXT,
    age TEXT,
    value NUMERIC
);

CREATE TABLE nonSentinelSeverity (
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    indicator TEXT,
    age TEXT,
    value NUMERIC
);

CREATE TABLE nonSentinelTestsDetections (
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    indicator TEXT,
    age TEXT,
    value NUMERIC
);

CREATE TABLE sentinelTestsDetectionsPositivity (
    survtype TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    pathogentype TEXT,
    pathogensubtype TEXT,
    indicator TEXT,
    age TEXT,
    value NUMERIC
);

CREATE TABLE sequencingVolumeDetectablePrevalence (
    survtype TEXT,
    datasource TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    indicator TEXT,
    age TEXT,
    value NUMERIC,
    detectableprevalence NUMERIC
);

CREATE TABLE variants (
    survtype TEXT,
    datasource TEXT,
    countryname TEXT,
    yearweek TEXT,
    pathogen TEXT,
    variant TEXT,
    indicator TEXT,
    age TEXT,
    value NUMERIC
);

-- Data Ingestion

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
