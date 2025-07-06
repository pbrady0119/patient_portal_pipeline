@echo off
echo Starting daily pipeline data generation...

"C:\Users\patri\AppData\Local\Programs\Python\Python313\python.exe" generate_activations.py
"C:\Users\patri\AppData\Local\Programs\Python\Python313\python.exe" generate_visits.py
"C:\Users\patri\AppData\Local\Programs\Python\Python313\python.exe" generate_patient_portal_events.py
"C:\Users\patri\AppData\Local\Programs\Python\Python313\python.exe" generate_pdfs.py

echo All generation scripts completed.
pause