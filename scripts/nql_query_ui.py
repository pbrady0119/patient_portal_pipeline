import streamlit as st
from openai import OpenAI
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Streamlit UI
st.title("🔍 GPT-Powered Natural Language Query on Patient Portal Pipeline")

with st.expander("💡 Example questions you can ask:", expanded=False):
    st.markdown("""
- **How many active patients have there been in the last 30 days?**
- **List the number of activated patients by activation channel.**
- **Show the number of successful logins by channel in the last 90 days.**
- **List departments with the most visits by activated patients.**
- **How many lab reports have been uploaded after visits by department?**
- **Show the number of patients who have logged in after activation.**
- **How many telehealth visits occurred for pediatrics in the last year?**
- **List the top 5 departments by unique activated patients.**
- **Show the number of document uploads by type in the last 60 days.**
- **How many patients have both activated their accounts and messaged a provider?**
""")


st.write("Ask a question about your pipeline data, and GPT will generate and run the SQL for you.")

# User input
user_query = st.text_input("Enter your natural language query:", "")

run_query = st.button("Run Query")

if user_query and run_query or user_query and not run_query:
    with st.spinner("Generating SQL with GPT..."):
        # Advanced semantic system prompt
        system_prompt = (
            "You are a Postgres SQL expert generating safe, syntactically correct SQL queries for a healthcare patient portal pipeline dataset.\n"
            "Always use clear syntax and fully qualified table names (schema.table).\n\n"
            "## Tables and Key Columns:\n"
            "- patient_portal_pipeline.activations_clean (activation_id UUID, pat_id UUID, activation_date DATE, activation_channel TEXT [phone, email, in-person, web], status TEXT [activated, unknown, failed, pending], method TEXT [standard, auto_activation_attempt], created_at TIMESTAMP)\n"
            "- patient_portal_pipeline.visits_clean (visit_id UUID, pat_id UUID, visit_date DATE, visit_type TEXT [phone, in-person, telehealth], department TEXT [primary care, urology, cardiology, dermatology, endocrinology, gastroenterology, pediatrics, orthopedics, oncology, neurology], created_at TIMESTAMP)\n"
            "- patient_portal_pipeline.patient_portal_events_clean (event_id UUID, pat_id UUID, event_timestamp TIMESTAMP, event_type TEXT [update_profile, login, view_lab, pay_bill, schedule_appointment, message_provider], channel TEXT [mobile app, web, tablet], successful BOOLEAN [true, false], metadata TEXT, created_at TIMESTAMP)\n"
            "- patient_portal_pipeline.uploaded_documents_clean (document_id UUID, pat_id UUID, upload_timestamp TIMESTAMP, doc_type TEXT [lab_report, insurance_card, consent_form], page_count INTEGER, file_name TEXT, created_at TIMESTAMP)\n\n"
            "## Semantic Mappings:\n"
            "- Treat 'active patients' as status = 'activated'.\n"
            "- Treat 'successful logins' as event_type = 'login' AND successful = true.\n"
            "- Treat 'lab reports' as doc_type = 'lab_report'.\n"
            "- Use CURRENT_DATE - INTERVAL 'X days' for 'last X days' filters.\n\n"
            "## Joins and Temporal Logic:\n"
            "- If the question requires data across tables, use INNER JOIN on pat_id.\n"
            "- For 'events after activation', use patient_portal_events_clean.event_timestamp > activations_clean.activation_date.\n"
            "- For 'uploads after visit', use uploaded_documents_clean.upload_timestamp > visits_clean.visit_date.\n\n"
            "## Aggregations:\n"
            "- Use GROUP BY for counts by department, channel, or event_type if the question requires it.\n"
            "- Use COUNT(DISTINCT pat_id) for distinct patient counts.\n\n"
            "Return ONLY the clean SQL code without markdown formatting or explanations. If unsure about a question, return a syntactically valid SQL that reflects the best guess based on the instructions."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )

        sql_code = response.choices[0].message.content.strip()

        # Clean potential markdown formatting
        if sql_code.startswith("```"):
            sql_code = sql_code.strip("`").strip()
            if sql_code.startswith("sql"):
                sql_code = sql_code[3:].strip()

        # Lightweight synonym mapping for 'status'
        if "status = 'active'" in sql_code:
            sql_code = sql_code.replace("status = 'active'", "status = 'activated'")

        st.subheader("Generated SQL:")
        st.code(sql_code, language="sql")

        try:
            with st.spinner("Executing SQL on your database..."):
                # Database connection
                conn = psycopg2.connect(
                    host="localhost",
                    database="postgres",
                    user="postgres",
                    password="Fit.rip.pie5",  # Replace with your actual password
                    port="5432"
                )
                cursor = conn.cursor()

                cursor.execute(sql_code)

                if cursor.description is not None:
                    # Fetch results into DataFrame
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    df = pd.DataFrame(rows, columns=columns)

                    if df.shape == (1, 1):
                        st.subheader("Result:")
                        st.metric(label="Value", value=df.iloc[0, 0])
                    else:
                        st.subheader("Query Results:")
                        st.dataframe(df)
                else:
                    st.success("Query executed successfully. No results returned.")

                cursor.close()
                conn.close()


                # Insights Chatbot block starts here
                if not df.empty:
                    csv_data = df.head(20).to_csv(index=False)
                    insights_prompt = (
                        "You are a senior data analyst reviewing the following CSV data from a SQL query:\n\n"
                        f"{csv_data}\n\n"
                        "If you notice any meaningful trends, patterns, or interesting points in this data, summarize them clearly and professionally in a friendly tone. "
                        "Use bullet points if helpful, but keep your response short and straightforward. "
                        "If the data is simple or there is nothing notable to mention, simply reply: 'No notable insights at this time.' "
                        "Do not invent data or explain obvious details."
                    )


                    with st.spinner("Generating insights from GPT..."):
                        insights_response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "You are a friendly, senior data analyst. You provide clear, concise, and factual insights based only on structured CSV data. You avoid inventing data or unnecessary explanations. If there is nothing notable, simply respond: 'No notable insights at this time.'"},
                                {"role": "user", "content": insights_prompt}
                            ]
                        )

                        insights_text = insights_response.choices[0].message.content.strip()

                    st.subheader("💡 Insights on Your Data")
                    st.write(insights_text)

                else:
                    st.info("No insights available: your query returned no data.")



        except Exception as e:
            st.error(f"An error occurred: {e}")
