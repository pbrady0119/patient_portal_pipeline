import csv
import uuid
import random
from datetime import datetime, timedelta
import os

NUM_ROWS = random.randint(3, 7)
event_types = ["login", "view_lab", "message_provider", "pay_bill", "schedule_appointment", "update_profile"]
channels = ["web", "mobile"]

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_file = os.path.join(base_dir, "data", "raw", "patient_portal_events.csv")
demographics_file = os.path.join(base_dir, "data", "raw", "patient_demographics.csv")

# Load pat_ids
pat_ids = []
with open(demographics_file, mode='r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pat_ids.append(row["pat_id"])

file_exists = os.path.isfile(csv_file)

with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    fieldnames = ["event_id", "pat_id", "event_timestamp", "event_type", "channel", "created_at"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if not file_exists:
        writer.writeheader()
    for _ in range(NUM_ROWS):
        pat_id = random.choice(pat_ids)
        event_timestamp = (datetime.now() - timedelta(days=random.randint(0, 7),
                                                     hours=random.randint(0, 23),
                                                     minutes=random.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow({
            "event_id": str(uuid.uuid4()),
            "pat_id": pat_id,
            "event_timestamp": event_timestamp,
            "event_type": random.choice(event_types),
            "channel": random.choice(channels),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

print(f"✅ {NUM_ROWS} new patient portal events generated and appended.")