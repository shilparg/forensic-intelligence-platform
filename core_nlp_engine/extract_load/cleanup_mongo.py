import os
import certifi
import pymongo
from dotenv import load_dotenv

# --- 1. Bulletproof .env Pathing ---
# Dynamically locate the .env file in the root folder, no matter where Dagster runs this from
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))         # /extract_load
ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))    # /core_nlp_engine
PROJECT_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, ".."))   # /forensic-intelligence-platform

env_path = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(env_path, override=True)

def get_mongo_client():
    """Forces secure Atlas SSL connections using certifi."""
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        # This will trigger the 'non-zero exit status' Dagster needs to stop the run
        print("🚨 CRITICAL ERROR: MONGO_URI is missing in .env.")
        exit(1) 
    
    # We remove the fallback and force the CA file immediately
    # This is the most reliable way to connect to Atlas in a headless Dagster environment
    return pymongo.MongoClient(
        mongo_uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000 # Fails fast (5s) instead of hanging the pipeline
    )

def sanitize_landing_zone():
    print("🧹 Starting MongoDB Sanitization (Pre-Audit Cleanup)...")
    
    # 2. Setup Connection using the safe wrapper
    client = get_mongo_client()
    db = client["forensic_accounting"]
    collection = db["raw_sec_filings"]

    # 3. Execute Cleanup Logic
    # Remove records with missing Fiscal Year
    result_fy = collection.delete_many({"fiscal_year": None})
    
    # Remove records with empty text (Prevents ML model from crashing)
    result_text = collection.delete_many({"parsed_text_sample": ""})
    
    # NEW RECONCILIATION: Remove records missing core NLP scores
    # This ensures dbt's weighted risk calculation doesn't fail
    result_scores = collection.delete_many({
        "$or": [
            {"sentiment_score": {"$exists": False}},
            {"subjectivity_score": {"$exists": False}}
        ]
    })

    print(f"✅ Cleanup Complete:")
    print(f"   - Removed {result_fy.deleted_count} records with missing years.")
    print(f"   - Removed {result_text.deleted_count} records with empty text.")
    print(f"   - Removed {result_scores.deleted_count} records with corrupted NLP metadata.")

if __name__ == "__main__":
    sanitize_landing_zone()