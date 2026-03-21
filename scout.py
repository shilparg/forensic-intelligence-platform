import os
from google.cloud import bigquery

# Connect to BigQuery using your root credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-service-account.json"
client = bigquery.Client()

print("🔍 Inspecting BigQuery Table Schema...")
try:
    query = "SELECT * FROM `forensic-accounting-bot.forensic_data.fct_disclosure_density` LIMIT 1"
    df = client.query(query).to_dataframe()
    
    print("\n✅ TABLE FOUND! Here are the exact column names:")
    for col in df.columns:
        print(f" - {col}")
        
except Exception as e:
    print(f"\n❌ Query Failed: {e}")