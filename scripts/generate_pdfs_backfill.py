from fpdf import FPDF
import uuid
import random
from datetime import datetime, timedelta
import os
import csv

# -------------------------------
#  Configuration
# -------------------------------
NUM_PDFS_TO_GENERATE = 1000  # ~1000 PDFs for realistic 2-year backfill
DOC_TYPES = ["insurance_card", "consent_form", "lab_report"]

# -------------------------------
#  Directory Setup
# -------------------------------
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_dir = os.path.join(base_dir, "pdfs")
os.makedirs(pdf_dir, exist_ok=True)

csv_file = os.path.join(base_dir, "data", "raw", "uploaded_documents.csv")
os.makedirs(os.path.dirname(csv_file), exist_ok=True)

demographics_file = os.path.join(base_dir, "data", "raw", "patient_demographics.csv")

# -------------------------------
#  Load pat_ids from demographics
# -------------------------------
pat_ids = []
with open(demographics_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        pat_ids.append(row['pat_id'])

# -------------------------------
#  Check if CSV already exists
# -------------------------------
file_exists = os.path.isfile(csv_file)

# -------------------------------
#  Create PDFs and Metadata
# -------------------------------
metadata_records = []

for _ in range(NUM_PDFS_TO_GENERATE):
    pat_id = random.choice(pat_ids)
    
    # Create upload_timestamp across last 730 days (2 years)
    days_back = random.randint(0, 730)
    upload_timestamp_dt = datetime.now() - timedelta(days=days_back, hours=random.randint(0, 23), minutes=random.randint(0, 59))
    upload_timestamp = upload_timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")

    doc_type = random.choice(DOC_TYPES)
    page_count = random.randint(1, 3)
    document_id = str(uuid.uuid4())
    
    # created_at = slightly after upload_timestamp (simulating processing delay)
    created_at_dt = upload_timestamp_dt + timedelta(minutes=random.randint(1, 1440))  # up to 1 day later
    created_at = created_at_dt.strftime("%Y-%m-%d %H:%M:%S")

    file_name = f"{document_id}_{doc_type}.pdf"
    file_path = os.path.join(pdf_dir, file_name)

    # Generate PDF
    pdf = FPDF()
    for page in range(page_count):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"{doc_type.replace('_', ' ').title()} - Page {page + 1}", ln=True, align='C')
        pdf.ln(10)
        pdf.multi_cell(0, 10, txt=f"Patient ID: {pat_id}\nUpload Timestamp: {upload_timestamp}\nDocument Type: {doc_type}")
    pdf.output(file_path)

    # Collect metadata
    metadata_records.append({
        "document_id": document_id,
        "pat_id": pat_id,
        "upload_timestamp": upload_timestamp,
        "doc_type": doc_type,
        "page_count": page_count,
        "file_name": file_name,
        "created_at": created_at
    })

# -------------------------------
#  Write Metadata to CSV
# -------------------------------
with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    fieldnames = ["document_id", "pat_id", "upload_timestamp", "doc_type", "page_count", "file_name", "created_at"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    if not file_exists:
        writer.writeheader()

    writer.writerows(metadata_records)

print(f"✅ {NUM_PDFS_TO_GENERATE} PDFs generated across 2 years in {pdf_dir}")
print(f"✅ Backfill metadata appended to {csv_file}")
