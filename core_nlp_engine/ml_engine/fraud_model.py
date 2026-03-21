import pandas as pd
import numpy as np
import yfinance as yf
import os
import json
import time
from google.cloud import bigquery
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv

# --- 1. Pathing & Auth ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# GCP Auth
key_path = os.path.join(PROJECT_ROOT, "gcp-service-account.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
client = bigquery.Client()

def run_ml_pipeline():
    print("🧠 Fetching SEC metrics from BigQuery...")
    # Updated to your specific forensic_data table
    query = "SELECT * FROM `forensic-accounting-bot.forensic_data.fct_disclosure_density`"
    sec_df = client.query(query).to_dataframe()
    sec_df.columns = sec_df.columns.str.lower()

    if sec_df.empty:
        print("⚠️ WARNING: BigQuery is empty. Ensure dbt build finished successfully.")
        return

    # --- 2. Inject Sector Metadata ---
    # This connects the "Target Identification" phase to the "ML" phase
    metadata_path = os.path.join(CURRENT_DIR, "../analysis/sector_metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            sector_map = json.load(f)
        sec_df['sector'] = sec_df['ticker'].map(sector_map).fillna('Information Technology')
    else:
        sec_df['sector'] = 'Information Technology'

    # --- 3. Source B: Throttled Market Data (Yahoo Finance) ---
    print(f"📈 Fetching market data for {len(sec_df['ticker'].unique())} tickers...")
    market_data = []

    for ticker in sec_df['ticker'].dropna().unique():
        try:
            print(f"📡 Requesting: {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info
            
            market_data.append({
                'ticker': ticker,
                'short_ratio': info.get('shortRatio', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'return_on_equity': info.get('returnOnEquity', 0),
                'operating_margin': info.get('operatingMargins', 0),
                'held_institutions': info.get('heldPercentInstitutions', 0)
            })
            # --- THE 429 FIX: Wait 1 second between requests ---
            time.sleep(1) 
            
        except Exception as e:
            print(f"⚠️ Yahoo API Throttled or Failed for {ticker}: {e}")
            # Append zeros so the merge still works
            market_data.append({'ticker': ticker, 'short_ratio': 0, 'debt_to_equity': 0, 
                                'return_on_equity': 0, 'operating_margin': 0, 'held_institutions': 0})

    market_df = pd.DataFrame(market_data)
    master_df = pd.merge(sec_df, market_df, on='ticker', how='left').fillna(0)

    # --- 4. The AI Model (Isolation Forest) ---
    print("🤖 Running Sector-Aware Anomaly Detection...")
    
    # Selecting core features for the 'Decision Matrix'
    features = ['sentiment_score', 'density_index', 'short_ratio', 'debt_to_equity', 
                'return_on_equity', 'operating_margin']
    
    X = master_df[features]
    
    # Scale the data (StandardScaler helps Isolation Forest with different units)
    X_scaled = StandardScaler().fit_transform(X)
    
    # Dynamic Contamination: 'auto' is safer for small/variable watchlists
    contamination = 0.10 if len(master_df) > 10 else 'auto' 
    
    model = IsolationForest(contamination=contamination, random_state=42)
    master_df['anomaly_score'] = model.fit_predict(X_scaled)
    
    # Labeling results
    master_df['fraud_risk_status'] = [
        'CRITICAL ANOMALY' if x == -1 else 'NORMAL' 
        for x in master_df['anomaly_score']
    ]

    # --- 5. Export Final Audit Dataset ---
    output_path = os.path.join(CURRENT_DIR, "ai_scored_forensic_dataset.csv")
    master_df.to_csv(output_path, index=False)
    print(f"✅ AI Scoring complete! Results saved to {output_path}")

if __name__ == "__main__":
    run_ml_pipeline()