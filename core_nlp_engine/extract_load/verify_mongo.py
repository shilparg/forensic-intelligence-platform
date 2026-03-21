import os
import sys
import pymongo
import certifi
from dotenv import load_dotenv

# --- 1. Bulletproof .env Pathing ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))         # /extract_load
ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))    # /core_nlp_engine
PROJECT_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, ".."))   # /forensic-intelligence-platform

env_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(env_path, override=True)

# --- 2. Safe MongoDB Connection ---
def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("🚨 CRITICAL ERROR: MONGO_URI is missing. Could not find .env file.")
    try:
        ca = certifi.where()
        return pymongo.MongoClient(mongo_uri, tlsCAFile=ca)
    except Exception as e:
        print(f"⚠️ Warning: SSL connection failed, trying standard connection. Error: {e}")
        return pymongo.MongoClient(mongo_uri)

def verify_extraction_quality():
    """
    Reconciled: Acts as a Data Quality Gate before Cloud Sync.
    Ensures all fields for the 'Weighted Risk Score' are present.
    """
    print(f"🔌 Connecting to MongoDB Atlas for Quality Audit...")
    client = get_mongo_client()
    db = client["forensic_accounting"]
    collection = db["raw_sec_filings"]

    # 3. Audit the Collection
    doc_count = collection.count_documents({})
    print(f"📊 Total documents in Landing Zone: {doc_count}")

    if doc_count == 0:
        print("❌ FATAL: Landing Zone is empty. Extraction failed.")
        sys.exit(1) # Forces Dagster to halt the pipeline

    # 4. Deep Forensic Audit (Checking specific fields for BQ/dbt)
    print("\n📋 Forensic Integrity Check (Latest Batch):")
    recent_docs = collection.find().sort("extraction_timestamp", -1).limit(5)

    valid_records = 0
    ticker = "UNKNOWN"
    for d in recent_docs:
        ticker = d.get('ticker', 'UNKNOWN')
        
        # Check for 'The Missing Payload' fields
        has_sentiment = 'sentiment_score' in d
        has_subjectivity = 'subjectivity_score' in d # Required for Red Flag Report
        has_word_count = 'word_count' in d           # Added to protect the AI Density Index
        has_text = len(d.get('parsed_text_sample', '')) > 1000
        
        status = "✅ PASS" if (has_sentiment and has_subjectivity and has_word_count and has_text) else "❌ FAIL"
        
        print(f"   -> Ticker: {ticker:<5} | Sent: {has_sentiment} | Subj: {has_subjectivity} | Words: {has_word_count} | Text: {has_text} | Status: {status}")
        
        if status == "✅ PASS":
            valid_records += 1

    # 5. Content Integrity Check
    latest_doc = collection.find_one(sort=[("extraction_timestamp", -1)])
    if latest_doc:
        text = latest_doc.get('parsed_text_sample', 'EMPTY')
        print(f"\n--- 📝 Content Sample ({latest_doc.get('ticker', 'UNKNOWN')}) ---")
        print(f"{text[:300]}...")

    if valid_records > 0:
        print(f"\n🟢 Quality Check Passed: {valid_records} records ready for BigQuery Sync.")
    else:
        print("\n🔴 Quality Check Failed: No valid records found for downstream AI.")
        sys.exit(1) # Forces Dagster to halt the pipeline before BigQuery Sync

if __name__ == "__main__":
    verify_extraction_quality()