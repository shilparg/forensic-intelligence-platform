import pandas as pd
import json
import os
from google.cloud import bigquery
from dotenv import load_dotenv

# --- 1. Bulletproof Pathing ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))         
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))   

# Load environment variables
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)

# Authenticate with Google Cloud securely
key_path = os.path.join(PROJECT_ROOT, "gcp-service-account.json")
if not os.path.exists(key_path):
    raise FileNotFoundError(f"🚨 Could not find GCP key at {key_path}")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# Locate the Meltano output file dynamically
file_path = os.path.join(CURRENT_DIR, "output", "raw_sec_filings.jsonl")

print(f"Reading raw data from {file_path}...")

# --- 2. Extract the raw dictionaries ---
data = []
try:
    with open(file_path, "r") as f:
        for line in f:
            try:
                row = json.loads(line.strip())
                if "document" in row:
                    data.append(row["document"])
                elif "ticker" in row:
                    data.append(row)
            except json.JSONDecodeError:
                continue
except FileNotFoundError:
    print(f"ERROR: Could not find {file_path}. Did Meltano run successfully?")
    exit(1)

# --- 3. THE MAGIC TRICKS (Your Schema Flattener) ---
df = pd.json_normalize(data)

# BigQuery hates periods in column names
df.columns = [str(c).replace(".", "_").replace(" ", "_") for c in df.columns]

# Convert any lingering complex lists or nested objects into JSON strings
for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)

# Force MongoDB ObjectIDs to be standard strings
if "_id" in df.columns:
    df["_id"] = df["_id"].astype(str)

print(f"Extracted {len(df)} records and expanded them into {len(df.columns)} distinct columns!")

# --- 4. Push to BigQuery ---
project_id = os.getenv("GCP_PROJECT_ID", "forensic-accounting-bot")
table_id = f"{project_id}.raw_sec_landing.raw_sec_filings"

client = bigquery.Client(project=project_id)
job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

print(f"Uploading to {table_id}...")
try:
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  
    print(f"\n✅ SUCCESS! {job.output_rows} rows securely loaded with all {len(df.columns)} parameters captured.")
except Exception as e:
    print(f"\n❌ Upload failed: {e}")
    exit(1)