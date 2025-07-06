-- patient_demographics_raw
CREATE TABLE patient_portal_pipeline.patient_demographics_raw (
    pat_id UUID,
    first_name TEXT,
    last_name TEXT,
    dob TEXT,
    gender TEXT,
    race TEXT,
    zip_code TEXT,
    state TEXT
);

-- activations_raw
CREATE TABLE patient_portal_pipeline.activations_raw (
    activation_id UUID,
    pat_id UUID,
    activation_date TEXT,
    activation_channel TEXT,
    status TEXT,
    method TEXT,
    created_at TIMESTAMP
);

-- patient_portal_events_raw
CREATE TABLE patient_portal_pipeline.patient_portal_events_raw (
    event_id UUID,
    pat_id UUID,
    event_timestamp TEXT,
    event_type TEXT,
    channel TEXT,
    successful TEXT,
    metadata TEXT,
    created_at TIMESTAMP    
);

-- visits_raw
CREATE TABLE patient_portal_pipeline.visits_raw (
    visit_id UUID,
    pat_id UUID,
    visit_date TEXT,
    visit_type TEXT,
    department TEXT,
    created_at TIMESTAMP    
);
