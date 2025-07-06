CREATE TABLE IF NOT EXISTS patient_portal_pipeline.uploaded_documents_raw (
    document_id UUID,
    pat_id UUID,
    upload_timestamp TEXT,
    doc_type TEXT,
    page_count INTEGER,
    file_name TEXT,
    created_at TIMESTAMP
);


CREATE TABLE IF NOT EXISTS patient_portal_pipeline.uploaded_documents_clean AS
SELECT
    document_id,
    pat_id,
    COALESCE(
        TO_TIMESTAMP_NULLABLE(upload_timestamp, 'YYYY-MM-DD HH24:MI:SS'),
        TO_TIMESTAMP_NULLABLE(upload_timestamp, 'YYYY-MM-DD')
    ) AS upload_timestamp,
    LOWER(NULLIF(doc_type, '')) AS doc_type,
    page_count,
    file_name,
    created_at
FROM patient_portal_pipeline.uploaded_documents_raw
WHERE FALSE; -- Initialize as empty for incremental loads