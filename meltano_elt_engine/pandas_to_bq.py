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

# Authenticate with Google Cloud
# Prioritize the key file we found in PROJECT_ROOT
key_path = os.path.join(PROJECT_ROOT, "gcp-service-account.json")
if os.path.exists(key_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    print(f"🔐 Authenticated via Service Account: {key_path}")
elif not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    raise FileNotFoundError(f"🚨 Could not find GCP key at {key_path} and no environment variable set.")

# Locate the Meltano output file dynamically
# Note: Ensure Meltano's target-jsonl is configured to output here
file_path = os.path.join(CURRENT_DIR, "output", "raw_sec_filings.jsonl")

print(f"📂 Reading raw data from {file_path}...")

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
                elif "value" in row: # Common Meltano wrapper
                    data.append(row["value"])
                else:
                    data.append(row)
            except json.JSONDecodeError:
                continue
except FileNotFoundError:
    print(f"❌ ERROR: Could not find {file_path}. Ensure Meltano 'target-jsonl' ran successfully.")
    exit(1)

if not data:
    print("⚠️ No data found in JSONL file. Skipping upload.")
    exit(0)

# --- 3. THE MAGIC TRICKS (Your Schema Flattener) ---
df = pd.json_normalize(data)

# BigQuery hates periods or spaces in column names
df.columns = [str(c).replace(".", "_").replace(" ", "_") for c in df.columns]

# Convert complex lists/dicts into JSON strings (BQ doesn't like raw Python objects)
for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)

# Force MongoDB ObjectIDs to be standard strings
if "_id" in df.columns:
    df["_id"] = df["_id"].astype(str)

print(f"✨ Flattened {len(df)} records into {len(df.columns)} clean columns.")

# --- 4. Push to BigQuery ---
project_id = os.getenv("GCP_PROJECT_ID", "forensic-accounting-bot")
dataset_id = "raw_sec_landing"
table_name = "raw_sec_filings"
table_id = f"{project_id}.{dataset_id}.{table_name}"

client = bigquery.Client(project=project_id)

# Ensure Dataset exists
dataset_ref = client.dataset(dataset_id)
dataset = bigquery.Dataset(dataset_ref)
dataset.location = "asia-southeast1"
client.create_dataset(dataset, exists_ok=True) 

job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

print(f"🚀 Uploading to {table_id}...")
try:
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  
    print(f"✅ SUCCESS! {len(df)} rows securely loaded to BigQuery.")
except Exception as e:
    print(f"❌ Upload failed: {e}")
    exit(1)