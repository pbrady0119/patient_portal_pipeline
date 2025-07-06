# GPT-Powered Patient Portal Engagement Pipeline

This repository contains a complete, realistic synthetic patient portal engagement pipeline for portfolio demonstration and technical practice. All data used and generated in this project is completely synthetic and fabricated, ensuring no patient or confidential information is present while retaining realistic patterns for advanced data engineering workflows.

## Folder Structure

```
patient_portal_pipeline/
│
├── data/
│   └── raw/
│
├── scripts/
│   ├── .env.example
│   ├── generate_activations.py
│   ├── generate_patient_demographics.py
│   ├── generate_patient_portal_events.py
│   ├── generate_pdfs_backfill.py
│   ├── generate_pdfs.py
│   ├── generate_visits.py
│   ├── daily_pipeline_generation.bat
│   ├── refresh_pipeline.bat
│   ├── nql_query_ui.py
│
├── sql/
│   ├── 01_create_schema.sql
│   ├── 02_create_raw_tables.sql
│   ├── 03_to_timestamp_nullable_function.sql
│   ├── 04_clean_staging_tables.sql
│   ├── 05_derived_tables.sql
│   ├── 06_uploaded_documents.sql
│   ├── 07_refresh_pipeline_stored_proc.sql
│
├── README.md
└── .gitignore
```

## Usage

### 1. Clone the Repository

```
git clone https://github.com/yourusername/patient_portal_pipeline.git
cd patient_portal_pipeline
```

### 2. Environment Configuration

Copy the example environment file and update with local values:

```
cp scripts/.env.example scripts/.env
```

Add the OpenAI API key and Postgres credentials.

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Generate Synthetic Data

Run the generation scripts in `scripts/` to populate `data/raw/` with synthetic patient demographics, activations, visits, portal events, and uploaded documents.

### 5. Set Up the Postgres Pipeline

Execute the SQL scripts in the `sql/` directory in order to create the schema, raw tables, clean staging tables, derived tables, and stored procedures.

### 6. Run the GPT-Powered NQL UI

Launch the GPT-powered Natural Language Query interface using Streamlit:

```
streamlit run scripts/nql_query_ui.py
```

This interface allows exploration of the synthetic dataset using natural language, leveraging GPT for dynamic SQL generation, execution, and result retrieval with optional insights.

### 7. Optional: Simulate Daily Incremental Loads

Use the provided batch scripts (`daily_pipeline_generation.bat` and `refresh_pipeline.bat`) to simulate daily incremental data generation and pipeline refresh logic.

## License

MIT License.

## .gitignore

```
__pycache__/
*.pyc
.env
data/clean/
notebooks/
```

## .env.example

```
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DB_HOST="localhost"
DB_NAME="postgres"
DB_USER="postgres"
DB_PASS="yourpassword"
DB_PORT="5432"
```

## requirements.txt

```
pandas
numpy
faker
fpdf
psycopg2-binary
streamlit
openai
python-dotenv
```

