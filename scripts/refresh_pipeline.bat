@echo off
echo Running refresh_pipeline stored procedure...

"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d postgres -c "CALL patient_portal_pipeline.refresh_pipeline();"

echo Stored procedure execution completed.
pause