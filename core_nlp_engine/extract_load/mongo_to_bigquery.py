import os
import certifi
import json
from pymongo import MongoClient
from google.cloud import bigquery
from dotenv import load_dotenv
from datetime import datetime

# --- 1. Bulletproof Pathing for WSL & Dagster ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))         # /extract_load
ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))    # /core_nlp_engine
PROJECT_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, ".."))   # /forensic-intelligence-platform

env_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(env_path, override=True)

# --- 2. Smart GCP Authentication Gateway ---
# Automatically adapt between Local Dev (JSON keys) and Cloud environments (ADC)
env_cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if env_cred_path:
    if not os.path.isabs(env_cred_path):
        env_cred_path = os.path.join(PROJECT_ROOT, env_cred_path)

    if os.path.exists(env_cred_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = env_cred_path
        print(f"🔐 Authenticated via local Service Account JSON file.")
    else:
        print(f"⚠️ Local key file not found. Falling back to Application Default Credentials (ADC).")
        os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
project_id = os.getenv("GCP_PROJECT_ID", "forensic-accounting-bot")

# Initialize client using standard Google App Default Credentials (bypasses missing local key issues)
bq_client = bigquery.Client(project=project_id)

# --- 3. Safe MongoDB Setup ---
def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("🚨 CRITICAL ERROR: MONGO_URI is missing. Could not find .env file.")
    try:
        ca = certifi.where()
        return MongoClient(mongo_uri, tlsCAFile=ca)
    except Exception as e:
        print(f"⚠️ Warning: SSL connection failed, trying standard connection. Error: {e}")
        return MongoClient(mongo_uri)

mongo_client = get_mongo_client()
# RESTORED: Your exact DB and Collection names
db = mongo_client["forensic_accounting"]
collection = db["raw_sec_filings"]

# --- 4. Main Sync Logic ---
def sync_mongo_to_bigquery():
    project_id = bq_client.project
    dataset_id = os.getenv("BQ_DATASET_ID", "forensic_data")
    table_id = f"{project_id}.{dataset_id}.raw_filings"

    # NEW: Ensure the dataset exists before loading (prevents 404 errors)
    dataset = bigquery.Dataset(f"{project_id}.{dataset_id}")
    dataset.location = "asia-southeast1"
    bq_client.create_dataset(dataset, exists_ok=True)

    print(f"[{datetime.now()}] 🔄 Syncing MongoDB ➔ BigQuery Table: {table_id}")
    
    mongo_docs = list(collection.find({}))
    if not mongo_docs:
        print("⚠️ No data found in MongoDB. Ensure extraction ran successfully.")
        return

    # Schema Mapping (Bridges Extraction to dbt)
    rows_to_insert = []
    for doc in mongo_docs:
        # Handling the timestamp conversion safely
        ext_ts = doc.get("extraction_timestamp")
        formatted_ts = ext_ts.isoformat() if isinstance(ext_ts, datetime) else None

        row = {
            "ticker": str(doc.get("ticker")).upper(),
            "cik": str(doc.get("cik")).zfill(10),
            "fiscal_year": int(doc.get("fiscal_year")) if doc.get("fiscal_year") else None,
            "filing_date": str(doc.get("filing_date", "")),
            "sentiment_score": float(doc.get("sentiment_score", 0.0)),
            "subjectivity_score": float(doc.get("subjectivity_score", 0.0)),
            "word_count": int(doc.get("word_count", 0)), # ADDED: Crucial for Density Index!
            "similarity_index": float(doc.get("similarity_index", 1.0)),
            "source_url": str(doc.get("source_url", "")),
            "extraction_timestamp": formatted_ts,
            "parsed_text_sample": str(doc.get("parsed_text_sample", ""))[:40000]
        }
        rows_to_insert.append(row)

    # BigQuery Job Configuration
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("ticker", "STRING"),
            bigquery.SchemaField("cik", "STRING"),
            bigquery.SchemaField("fiscal_year", "INTEGER"),
            bigquery.SchemaField("filing_date", "STRING"),
            bigquery.SchemaField("sentiment_score", "FLOAT"),
            bigquery.SchemaField("subjectivity_score", "FLOAT"),
            bigquery.SchemaField("word_count", "INTEGER"), # ADDED: Crucial for Density Index!
            bigquery.SchemaField("similarity_index", "FLOAT"),
            bigquery.SchemaField("source_url", "STRING"),
            bigquery.SchemaField("extraction_timestamp", "TIMESTAMP"),
            bigquery.SchemaField("parsed_text_sample", "STRING"),
        ],
        write_disposition="WRITE_TRUNCATE", # Replaces old data with the latest audit batch
    )

    print(f"⏳ Loading {len(rows_to_insert)} records into BigQuery...")
    # Using your preferred load_table_from_json method
    job = bq_client.load_table_from_json(rows_to_insert, table_id, job_config=job_config)
    job.result()  # Wait for completion

    print(f"✅ SUCCESS: {len(rows_to_insert)} records are now live for dbt transformations.")

if __name__ == "__main__":
    sync_mongo_to_bigquery()