import os
import json
import argparse
import requests
import pymongo
import certifi
import re
import warnings
from datetime import datetime
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from dotenv import load_dotenv
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

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

client = get_mongo_client()
collection = client["forensic_accounting"]["raw_sec_filings"]

HEADERS = {
    'User-Agent': os.getenv("SEC_USER_AGENT", "ForensicBot (test@example.com)"), 
    'Accept-Encoding': 'gzip, deflate'
}

# --- 3. Forensic Utilities ---
def calculate_similarity(new_text, ticker):
    prev_doc = collection.find_one({"ticker": ticker}, sort=[("fiscal_year", -1)])
    if not prev_doc or "parsed_text_sample" not in prev_doc:
        return 1.0
    try:
        vec = TfidfVectorizer().fit_transform([prev_doc["parsed_text_sample"], new_text])
        return float(cosine_similarity(vec[0:1], vec[1:2])[0][0])
    except:
        return 1.0

def get_latest_10k_url(cik):
    url = f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200: return None, None, None
        
    filings = response.json()['filings']['recent']
    for idx, form in enumerate(filings['form']):
        if form == '10-K':
            f_date = filings['filingDate'][idx]
            f_year = int(f_date.split('-')[0])
            acc_num = filings['accessionNumber'][idx].replace('-', '')
            doc_name = filings['primaryDocument'][idx]
            doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_num}/{doc_name}"
            return doc_url, f_date, f_year
    return None, None, None

# --- 4. Main Extraction Logic ---
def run_extraction(target_dict):
    print(f"📥 Starting SEC Extraction for {len(target_dict)} targets...")
    
    for ticker, cik in target_dict.items():
        print(f"   - Processing {ticker} (CIK: {cik})...")
        doc_url, filing_date, actual_year = get_latest_10k_url(cik)
        if not doc_url: 
            print(f"     ❌ No 10-K found.")
            continue

        response = requests.get(doc_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, features="lxml")
        filing_text = re.sub(r'\s+', ' ', soup.get_text(separator=' ')).strip()
        
        analysis = TextBlob(filing_text)
        similarity = calculate_similarity(filing_text, ticker)

        # Added subjectivity_score and word_count so dbt metrics calculate correctly!
        collection.insert_one({
            "ticker": ticker,
            "cik": str(cik),
            "fiscal_year": actual_year,
            "sentiment_score": analysis.sentiment.polarity,
            "subjectivity_score": analysis.sentiment.subjectivity,
            "word_count": len(filing_text.split()), 
            "similarity_index": similarity,
            "extraction_timestamp": datetime.now(),
            "parsed_text_sample": filing_text[:30000]
        })
        print(f"     ✅ Successfully extracted and saved FY{actual_year} data.")

# --- 5. Dagster CLI Integration ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker_map", help="JSON string of {ticker: cik} from Dagster UI")
    args = parser.parse_args()

    if args.ticker_map:
        # Dagster passes the config here
        targets = json.loads(args.ticker_map)
        run_extraction(targets)
    else:
        # Fallback for manual testing
        targets = {"AAPL": "320193", "MSFT": "789019", "NVDA": "1045810", "META": "1326801"}
        run_extraction(targets)