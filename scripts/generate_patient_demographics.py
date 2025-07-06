import os 
from faker import Faker
import uuid
import random
import csv

# Initialize Faker
fake = Faker()
random.seed(42)
Faker.seed(42)

# Set number of patients
num_patients = 10000

# Define races and weights
races = ['White', 'Black', 'Asian', 'Hispanic', 'Other']
race_weights = [0.6, 0.15, 0.1, 0.1, 0.05]

# Prepare output CSV
output_file = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'data',
    'raw',
    'patient_demographics.csv'
)

#state of residence with weights to improve realism
states = [
    'MA', 'NH', 'VT', 'ME', 'RI', 'CT',
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'DE', 'FL', 'GA', 'HI', 'ID',
    'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'MD', 'MI', 'MN', 'MS', 'MO',
    'MT', 'NE', 'NV', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR',
    'PA', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'WA', 'WV', 'WI', 'WY'
]
state_weights = []

for state in states:
    if state == 'MA':
        state_weights.append(0.5)
    elif state in ['NH','VT','ME','RI','CT']:
        state_weights.append(0.2/5)

    else:
        state_weights.append(0.3/(len(states)-6))


with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['pat_id', 'first_name', 'last_name', 'dob', 'gender', 'race', 'zip_code','state'])
    
    for _ in range(num_patients):
        pat_id = str(uuid.uuid4())
        first_name = fake.first_name()
        last_name = fake.last_name()
        dob = fake.date_of_birth(minimum_age=0, maximum_age=100)
        gender = random.choice(['Male', 'Female'])
        race = random.choices(races, weights=race_weights, k=1)[0]
        zip_code = fake.zipcode()
        state = random.choices(states,weights=state_weights, k=1)[0]
        
        writer.writerow([pat_id, first_name, last_name, dob, gender, race, zip_code,state])

print(f"✅ Generated {num_patients} patient records in {output_file}")