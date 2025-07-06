-- Clean patient_demographics
CREATE TABLE patient_portal_pipeline.patient_demographics_clean AS
SELECT
 pat_id
,first_name
,last_name
,COALESCE(
    TO_TIMESTAMP_NULLABLE(dob, 'YYYY-MM-DD')
    ,TO_TIMESTAMP_NULLABLE(dob, 'MM/DD/YYYY')
    ,TO_TIMESTAMP_NULLABLE(dob, 'Month DD, YYYY')
    ,TO_TIMESTAMP_NULLABLE(dob, 'YYYY/MM/DD')
)::DATE AS dob
,LOWER(NULLIF(gender, '')) AS gender
,LOWER(NULLIF(race, '')) AS race
,NULLIF(zip_code, '') AS zip_code
,NULLIF(state, '') AS state

FROM patient_portal_pipeline.patient_demographics_raw;


-- Clean activations
CREATE TABLE patient_portal_pipeline.activations_clean AS
SELECT
 activation_id
,pat_id
,COALESCE(
    TO_TIMESTAMP_NULLABLE(activation_date, 'YYYY-MM-DD')
    ,TO_TIMESTAMP_NULLABLE(activation_date, 'MM/DD/YYYY')
    ,TO_TIMESTAMP_NULLABLE(activation_date, 'Month DD, YYYY')
    ,TO_TIMESTAMP_NULLABLE(activation_date, 'YYYY/MM/DD')
)::DATE AS activation_date
,LOWER(NULLIF(activation_channel, '')) AS activation_channel
,LOWER(NULLIF(status, '')) AS status
,LOWER(NULLIF(method, '')) AS method
,created_at

FROM patient_portal_pipeline.activations_raw;


-- Clean patient_portal_events
CREATE TABLE patient_portal_pipeline.patient_portal_events_clean AS
SELECT
 event_id
,pat_id
,COALESCE(
    TO_TIMESTAMP_NULLABLE(event_timestamp, 'YYYY-MM-DD HH24:MI:SS')
    ,TO_TIMESTAMP_NULLABLE(event_timestamp, 'MM/DD/YYYY HH24:MI')
    ,TO_TIMESTAMP_NULLABLE(event_timestamp, 'Month DD, YYYY HH24:MI')
    ,TO_TIMESTAMP_NULLABLE(event_timestamp, 'YYYY/MM/DD HH24:MI')
) AS event_timestamp
,LOWER(NULLIF(event_type, '')) AS event_type
,LOWER(NULLIF(channel, '')) AS channel
,CASE
    WHEN LOWER(successful) = 'true' THEN TRUE
    WHEN LOWER(successful) = 'false' THEN FALSE
    ELSE NULL
 END AS successful
,NULLIF(metadata, '') AS metadata
,created_at

FROM patient_portal_pipeline.patient_portal_events_raw;


-- Clean visits
CREATE TABLE patient_portal_pipeline.visits_clean AS
SELECT
 visit_id
,pat_id
,COALESCE(
    TO_TIMESTAMP_NULLABLE(visit_date, 'YYYY-MM-DD')
    ,TO_TIMESTAMP_NULLABLE(visit_date, 'MM/DD/YYYY')
    ,TO_TIMESTAMP_NULLABLE(visit_date, 'Month DD, YYYY')
    ,TO_TIMESTAMP_NULLABLE(visit_date, 'YYYY/MM/DD')
)::DATE AS visit_date
,LOWER(NULLIF(visit_type, '')) AS visit_type
,LOWER(NULLIF(department, '')) AS department
,created_at

FROM patient_portal_pipeline.visits_raw;
