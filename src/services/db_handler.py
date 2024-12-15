from google.cloud import bigquery
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class BigQueryConnector:
    def __init__(self):
        self.client = bigquery.Client()
        self.project_id = os.getenv("PROJECT_ID")
        self.dataset_name = "case_crafter_db"

    def insert_case_notes(
            self, session_id, client_id, client_name, therapist_id, llm_case_notes):
        table_name = "case-notes"
        table_id = f"{self.project_id}.{self.dataset_name}.{table_name}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows_to_insert = [
            {
                "session_id": session_id,
                "client_id": client_id,
                "client_name": client_name,
                "therapist_id": therapist_id,
                "llm_case_notes": llm_case_notes,
                "submitted_at": timestamp,
            }
        ]
        
        try:
            errors = self.client.insert_rows_json(table_id, rows_to_insert)
            if errors == []:
                print(f"Data successfully inserted into table {table_name}.")
            else:
                print(f"Failed to insert rows: {errors}")
        except Exception as e:
            raise Exception(f"Error inserting data into BigQuery: {e}")
        
    def insert_progress_notes(
            self, session_id, client_id, client_name, therapist_id,
            client_presentation, response_treatment, client_status,
            risk_assessment):
        table_name = "progress-notes"
        table_id = f"{self.project_id}.{self.dataset_name}.{table_name}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows_to_insert = [
            {
                "session_id": session_id,
                "client_id": client_id,
                "client_name": client_name,
                "therapist_id": therapist_id,
                "client_presentation": client_presentation,
                "response_treatment": response_treatment,
                "client_status": client_status,
                "risk_assessment": risk_assessment,
                "submitted_at": timestamp,
            }
        ]

        try:
            errors = self.client.insert_rows_json(table_id, rows_to_insert)
            if errors == []:
                print(f"Data successfully inserted into table {table_name}.")
            else:
                print(f"Failed to insert rows: {errors}")
        except Exception as e:
            raise Exception(f"Error inserting data into BigQuery: {e}")
        
    def insert_feedback(self, session_id, feedback):
        table_name = "feedback"
        table_id = f"{self.project_id}.{self.dataset_name}.{table_name}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows_to_insert = [
            {
                "session_id": session_id,
                "feedback": feedback,
                "submitted_at": timestamp,
            }
        ]

        try:
            errors = self.client.insert_rows_json(table_id, rows_to_insert)
            if errors == []:
                print(f"Feedback successfully inserted into table {table_name}.")
            else:
                print(f"Failed to insert rows: {errors}")
        except Exception as e:
            raise Exception(f"Error inserting feedback into BigQuery: {e}")

    def close_connection(self):
        self.client = None
        print("BigQuery connection closed.")

    def setup_tables(self):
        schemas = {
            "case-notes": [
                bigquery.SchemaField("session_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("client_name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("therapist_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("llm_case_notes", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("submitted_at", "TIMESTAMP", mode="REQUIRED"),
            ],
            "progress-notes": [
                bigquery.SchemaField("session_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("client_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("client_name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("therapist_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("client_presentation", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("response_treatment", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("client_status", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("risk_assessment", "STRING", mode="NULLABLE"),
                bigquery.SchemaField("submitted_at", "TIMESTAMP", mode="REQUIRED"),
            ],
            "feedback": [
                bigquery.SchemaField("session_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("feedback", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("submitted_at", "TIMESTAMP", mode="REQUIRED"),
            ],
        }

        for table_name, schema in schemas.items():
            self.create_table_if_not_exists(table_name, schema)