CREATE OR REPLACE PROCEDURE patient_portal_pipeline.refresh_pipeline()
LANGUAGE plpgsql
AS $$
BEGIN

-------------------------
-- Incremental Load: Activations
-------------------------
INSERT INTO patient_portal_pipeline.activations_clean (
    activation_id,
    pat_id,
    activation_date,
    activation_channel,
    status,
    method,
    created_at
)
SELECT
    r.activation_id,
    r.pat_id,
    COALESCE(
        TO_TIMESTAMP_NULLABLE(r.activation_date, 'YYYY-MM-DD'),
        TO_TIMESTAMP_NULLABLE(r.activation_date, 'MM/DD/YYYY'),
        TO_TIMESTAMP_NULLABLE(r.activation_date, 'Month DD, YYYY'),
        TO_TIMESTAMP_NULLABLE(r.activation_date, 'YYYY/MM/DD')
    )::DATE,
    LOWER(NULLIF(r.activation_channel, '')),
    LOWER(NULLIF(r.status, '')),
    LOWER(NULLIF(r.method, '')),
    r.created_at
FROM patient_portal_pipeline.activations_raw r
LEFT JOIN (
    SELECT pat_id, MAX(created_at) AS max_created_at
    FROM patient_portal_pipeline.activations_clean
    GROUP BY pat_id
) cmax
ON r.pat_id = cmax.pat_id
WHERE cmax.max_created_at IS NULL OR r.created_at > cmax.max_created_at;   -- only load data when created_at is > than the data in the table per patient

-------------------------
-- Incremental Load: Visits
-------------------------
INSERT INTO patient_portal_pipeline.visits_clean (
    visit_id,
    pat_id,
    visit_date,
    visit_type,
    department,
    created_at
)
SELECT
    r.visit_id,
    r.pat_id,
    COALESCE(
        TO_TIMESTAMP_NULLABLE(r.visit_date, 'YYYY-MM-DD'),
        TO_TIMESTAMP_NULLABLE(r.visit_date, 'MM/DD/YYYY'),
        TO_TIMESTAMP_NULLABLE(r.visit_date, 'Month DD, YYYY'),
        TO_TIMESTAMP_NULLABLE(r.visit_date, 'YYYY/MM/DD')
    )::DATE,
    LOWER(NULLIF(r.visit_type, '')),
    LOWER(NULLIF(r.department, '')),
    r.created_at
FROM patient_portal_pipeline.visits_raw r
LEFT JOIN (
    SELECT pat_id, MAX(created_at) AS max_created_at
    FROM patient_portal_pipeline.visits_clean
    GROUP BY pat_id
) cmax
ON r.pat_id = cmax.pat_id
WHERE cmax.max_created_at IS NULL OR r.created_at > cmax.max_created_at;

-------------------------
-- Incremental Load: Patient Portal Events
-------------------------
INSERT INTO patient_portal_pipeline.patient_portal_events_clean (
    event_id,
    pat_id,
    event_timestamp,
    event_type,
    channel,
    successful,
    metadata,
    created_at
)
SELECT
    r.event_id,
    r.pat_id,
    COALESCE(
        TO_TIMESTAMP_NULLABLE(r.event_timestamp, 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP_NULLABLE(r.event_timestamp, 'MM/DD/YYYY HH24:MI'),
        TO_TIMESTAMP_NULLABLE(r.event_timestamp, 'Month DD, YYYY HH24:MI'),
        TO_TIMESTAMP_NULLABLE(r.event_timestamp, 'YYYY/MM/DD HH24:MI')
    ),
    LOWER(NULLIF(r.event_type, '')),
    LOWER(NULLIF(r.channel, '')),
    CASE
        WHEN LOWER(r.successful) = 'true' THEN TRUE
        WHEN LOWER(r.successful) = 'false' THEN FALSE
        ELSE NULL
    END,
    NULLIF(r.metadata, ''),
    r.created_at
FROM patient_portal_pipeline.patient_portal_events_raw r
LEFT JOIN (
    SELECT pat_id, MAX(created_at) AS max_created_at
    FROM patient_portal_pipeline.patient_portal_events_clean
    GROUP BY pat_id
) cmax
ON r.pat_id = cmax.pat_id
WHERE cmax.max_created_at IS NULL OR r.created_at > cmax.max_created_at;

-------------------------
-- Incremental Load: Uploaded Documents
-------------------------
INSERT INTO patient_portal_pipeline.uploaded_documents_clean (
    document_id,
    pat_id,
    upload_timestamp,
    doc_type,
    page_count,
    file_name,
    created_at
)
SELECT
    r.document_id,
    r.pat_id,
    COALESCE(
        TO_TIMESTAMP_NULLABLE(r.upload_timestamp, 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP_NULLABLE(r.upload_timestamp, 'MM/DD/YYYY HH24:MI'),
        TO_TIMESTAMP_NULLABLE(r.upload_timestamp, 'Month DD, YYYY HH24:MI'),
        TO_TIMESTAMP_NULLABLE(r.upload_timestamp, 'YYYY/MM/DD HH24:MI')
    ),
    LOWER(NULLIF(r.doc_type, '')),
    r.page_count,
    r.file_name,
    r.created_at
FROM patient_portal_pipeline.uploaded_documents_raw r
LEFT JOIN (
    SELECT pat_id, MAX(created_at) AS max_created_at
    FROM patient_portal_pipeline.uploaded_documents_clean
    GROUP BY pat_id
) cmax
ON r.pat_id = cmax.pat_id
WHERE cmax.max_created_at IS NULL OR r.created_at > cmax.max_created_at;

END;
$$;
