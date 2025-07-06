import csv
import uuid
import random
from datetime import datetime, timedelta
import os

NUM_ROWS = random.randint(3, 7)
departments = ["cardiology", "dermatology", "oncology", "pediatrics", "primary_care"]

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file = os.path.join(base_dir, "data", "raw", "visits.csv")
demographics_file = os.path.join(base_dir, "data", "raw", "patient_demographics.csv")

# Load pat_ids
pat_ids = []
with open(demographics_file, mode='r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pat_ids.append(row["pat_id"])

file_exists = os.path.isfile(csv_file)

with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    fieldnames = ["visit_id", "pat_id", "visit_date", "department", "created_at"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    for _ in range(NUM_ROWS):
        pat_id = random.choice(pat_ids)
        visit_date = (datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
        writer.writerow({
            "visit_id": str(uuid.uuid4()),
            "pat_id": pat_id,
            "visit_date": visit_date,
            "department": random.choice(departments),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

print(f"✅ {NUM_ROWS} new visits generated and appended.")