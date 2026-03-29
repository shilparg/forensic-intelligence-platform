import os
import json
import time
import pandas as pd
import yfinance as yf
from google.cloud import bigquery
from dotenv import load_dotenv

# --- 1. Pathing & Cloud Configuration ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)

# Authenticate GCP
key_path = os.path.join(PROJECT_ROOT, "gcp-service-account.json")
if os.path.exists(key_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

client = bigquery.Client()

def extract_and_load_financials():
    print("📈 ENGINE B: Extracting Market Data from Yahoo Finance...")
    
    # 🌟 Read target tracking from Engine A (Phase 1)
    metadata_path = os.path.join(PROJECT_ROOT, "core_nlp_engine", "analysis", "sector_metadata.json")
    if not os.path.exists(metadata_path):
        print("⚠️ No sector_metadata.json found. Ensure 'determine_targets' ran first.")
        return

    with open(metadata_path, 'r') as f:
        sector_map = json.load(f)
        
    tickers = list(sector_map.keys())
    print(f"📡 Found {len(tickers)} companies to process...")

    # --- 2. Extraction & Flattening ---
    market_data = []
    
    for ticker in tickers:
        try:
            print(f"   -> Extracting {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract standard core metrics & advanced forensic metrics
            market_data.append({
                'ticker': ticker,
                'short_ratio': info.get('shortRatio', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'return_on_equity': info.get('returnOnEquity', 0),
                'operating_margin': info.get('operatingMargins', 0),
                'held_institutions': info.get('heldPercentInstitutions', 0),
                # --- NEW Forensic Accounting Metrics ---
                'insider_ownership': info.get('heldPercentInsiders', 0),  # Mass Executive Dumping Warning
                'current_ratio': info.get('currentRatio', 0),     # Liquidity Risk
                'quick_ratio': info.get('quickRatio', 0),         # Strict Liquidity Risk
                'revenue_growth': info.get('revenueGrowth', 0),   # Pressure to fake sales
                'earnings_growth': info.get('earningsGrowth', 0), # Pressure to fake EPS
                'profit_margins': info.get('profitMargins', 0),   # Bottom line truth
                'free_cashflow': info.get('freeCashflow', 0)      # Cash vs Accounting Profits
            })
            
            # The throttle sits here natively, away from the ML model
            time.sleep(1) 
        except Exception as e:
            print(f"   ❌ Yahoo API Failed for {ticker}: {e}")
            # Insert standard fallback numericals directly to BigQuery
            market_data.append({
                'ticker': ticker, 'short_ratio': 0, 'debt_to_equity': 0, 
                'return_on_equity': 0, 'operating_margin': 0, 'held_institutions': 0,
                'insider_ownership': 0, 'current_ratio': 0, 'quick_ratio': 0, 'revenue_growth': 0,
                'earnings_growth': 0, 'profit_margins': 0, 'free_cashflow': 0
            })

    # Convert to pure tabular format for Silver
    df = pd.DataFrame(market_data)
    
    # --- 3. Loading to Silver Layer (BigQuery) ---
    project_id = os.getenv("GCP_PROJECT_ID", "forensic-accounting-bot")
    dataset_id = "raw_sec_landing"
    table_name = "raw_financials"
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    
    print(f"🚀 Pushing {len(df)} numerical records securely directly to {table_id}...")
    
    # Ensure Silver Dataset exists
    dataset_ref = client.dataset(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "asia-southeast1"
    client.create_dataset(dataset, exists_ok=True) 

    # WRITE_TRUNCATE overwrites the table with fresh numbers every time Engine B runs
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    
    try:
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  
        print(f"✅ SUCCESS! Engine B loaded market metrics into the Silver BigQuery node.")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        exit(1)

if __name__ == "__main__":
    extract_and_load_financials()
