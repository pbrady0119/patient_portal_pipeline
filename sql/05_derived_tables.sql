-- Patient Portal Logins
CREATE TABLE patient_portal_pipeline.patient_portal_logins AS
SELECT
 event_id
,pat_id
,event_timestamp
,channel
,successful
FROM patient_portal_pipeline.patient_portal_events_clean
WHERE event_type = 'login';

-- Post Login Usage Events

CREATE TABLE patient_portal_pipeline.patient_portal_post_login_usage AS
WITH logins AS (
    SELECT
         pat_id
        ,event_timestamp AS login_timestamp
    FROM patient_portal_pipeline.patient_portal_logins
    WHERE successful = TRUE
)
SELECT
     e.event_id
    ,e.pat_id
    ,e.event_timestamp
    ,e.event_type
    ,e.channel
FROM patient_portal_pipeline.patient_portal_events_clean e
JOIN logins l
    ON e.pat_id = l.pat_id
    AND e.event_timestamp >= l.login_timestamp
    AND e.event_timestamp <= l.login_timestamp + interval '2 hours'  -- any event within 2 hours of a login. 
WHERE e.event_type IN (
    'view_lab'
    ,'message_provider'
    ,'pay_bill'
    ,'schedule_appointment'
    ,'update_profile'
);

-- Latest Activation Status Per Patient
CREATE TABLE patient_portal_pipeline.latest_activation_status AS
WITH ranked_activations AS (
    SELECT
         pat_id
        ,activation_date
        ,status
        ,ROW_NUMBER() OVER (PARTITION BY pat_id ORDER BY activation_date DESC) AS rn
    FROM patient_portal_pipeline.activations_clean
    WHERE method = 'standard'
)
SELECT
 pat_id
,activation_date AS latest_activation_date
,status AS latest_activation_status
FROM ranked_activations
WHERE rn = 1;

-- Patient Login Counts (Engagement Metric)
CREATE TABLE patient_portal_pipeline.patient_login_counts AS
SELECT
 pat_id
,COUNT(*) AS login_count
,MIN(event_timestamp) AS first_login
,MAX(event_timestamp) AS last_login
FROM patient_portal_pipeline.patient_portal_logins
WHERE successful = TRUE
GROUP BY pat_id;
