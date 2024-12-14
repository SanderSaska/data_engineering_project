-- models/staging/stg_infections.sql
WITH raw_infections AS (
    select * from (
    Select id, 'activityFluTypeSubtype' as inf_source, countryname, yearweek, pathogen, pathogentype, pathogensubtype, age, inf_indicator, inf_value
    from {{ source('raw_data', 'activityflutypesubtype') }}
    Union
    Select id, 'ILIARIRates' as inf_source, countryname, yearweek, '' , '', '', age, inf_indicator, inf_value
    from {{ source('raw_data', 'iliarirates') }}
    Union
    Select id, 'nonSentinelSeverity' as inf_source, countryname, yearweek, pathogen, pathogentype, '', age, inf_indicator, inf_value
    from {{ source('raw_data', 'nonsentinelseverity') }}
    Union
    Select id, 'nonSentinelTestsDetections' as inf_source, countryname, yearweek, pathogen, pathogentype, pathogensubtype, age, inf_indicator, inf_value
    from {{ source('raw_data', 'nonsentineltestsdetections') }}
    Union
    Select id, 'SARIRates' as inf_source, countryname, yearweek, '', '', '', age, inf_indicator, inf_value
    from {{ source('raw_data', 'sarirates') }}
    Union
    Select id, 'SARITestsDetectionPositivity' as inf_source, countryname, yearweek, pathogen, pathogentype, pathogensubtype, age, inf_indicator, inf_value
    from {{ source('raw_data', 'saritestsdetectionpositivity') }}
    Union
    Select id, 'sentinelTestsDetectionsPositivity' as inf_source, countryname, yearweek, pathogen, pathogentype, pathogensubtype, age, inf_indicator, inf_value
    from {{ source('raw_data', 'sentineltestsdetectionspositivity') }})


)
SELECT
    concat(id, source) as infection_id,
    inf_source,
    countryname,
    yearweek,
    pathogen,
    pathogentype,
    pathogensubtype,
    age,
    inf_indicator,
    inf_value
FROM raw_infections;
