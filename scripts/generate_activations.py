import csv
import uuid
import random
from datetime import datetime, timedelta
import os

NUM_ROWS = random.randint(3, 7)
channels = ["email", "phone", "in_person"]
statuses = ["activated", "pending", "deactivated"]
methods = ["standard", "auto"]

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file = os.path.join(base_dir, "data", "raw", "activations.csv")
demographics_file = os.path.join(base_dir, "data", "raw", "patient_demographics.csv")

# Load pat_ids
pat_ids = []
with open(demographics_file, mode='r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pat_ids.append(row["pat_id"])

file_exists = os.path.isfile(csv_file)

with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    fieldnames = ["activation_id", "pat_id", "activation_date", "activation_channel", "status", "method", "created_at"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    for _ in range(NUM_ROWS):
        pat_id = random.choice(pat_ids)
        activation_date = (datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
        writer.writerow({
            "activation_id": str(uuid.uuid4()),
            "pat_id": pat_id,
            "activation_date": activation_date,
            "activation_channel": random.choice(channels),
            "status": random.choice(statuses),
            "method": random.choice(methods),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

print(f"✅ {NUM_ROWS} new activations generated and appended.")