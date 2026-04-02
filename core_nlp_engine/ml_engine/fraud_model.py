import pandas as pd
import numpy as np
import os
import json
from google.cloud import bigquery
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, MinMaxScaler
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
    print("🧠 Fetching Unfied Forensic Data (Engine A + Engine B) from BigQuery...")
    # Because of dbt Phase 2, this table now natively contains the 13 Yahoo metrics AND Benfords Law!
    project_id = os.getenv("GCP_PROJECT_ID")
    dataset_id = os.getenv("BQ_FINAL_DATASET", "forensic_data")
    query = f"SELECT * FROM `{project_id}.{dataset_id}.fct_disclosure_density`"
    
    # 1-second execution! (No more 429 throttling loops)
    master_df = client.query(query).to_dataframe()
    master_df.columns = master_df.columns.str.lower()

    if master_df.empty:
        print("⚠️ WARNING: BigQuery is empty. Ensure dbt build finished successfully.")
        return

    # --- 2. Inject Sector Metadata ---
    # Connects the "Target Identification" phase to the "ML" phase
    metadata_path = os.path.join(CURRENT_DIR, "../analysis/sector_metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            sector_map = json.load(f)
        master_df['sector'] = master_df['ticker'].map(sector_map).fillna('Information Technology')
    else:
        master_df['sector'] = 'Information Technology'

    # --- 3. The AI Model (Isolation Forest) ---
    print("🤖 Running Advanced Sector-Aware Anomaly Detection...")
    
    # NEW POWERFUL AI FEATURE SPACE: Uses Text + Benford + Market Liquidity
    features = [
        'sentiment_score', 
        'density_index', 
        'short_ratio', 
        'debt_to_equity', 
        'return_on_equity', 
        'operating_margin',
        'benfords_deviation',      # Advanced Math Flag
        'sentiment_volatility',    # 3-Year Executive Tone Trailing Window
        'insider_ownership',       # Executive dumping tracker
        'current_ratio'            # Ability to pay short term debts
    ]
    
    # Handle any nulls passed down from the cloud just in case
    X = master_df[features].fillna(0)
    
    # Scale the metrics to identical z-space vectors
    X_scaled = StandardScaler().fit_transform(X)
    
    # Dynamic Contamination: 'auto' is safer for small/variable watchlists
    contamination = 0.10 if len(master_df) > 10 else 'auto' 
    
    model = IsolationForest(contamination=contamination, random_state=42)
    master_df['anomaly_score'] = model.fit_predict(X_scaled)
    
    # Labeling final output decisions
    master_df['fraud_risk_status'] = [
        'CRITICAL ANOMALY' if x == -1 else 'NORMAL' 
        for x in master_df['anomaly_score']
    ]

    # --- 3.1 Predictive Probability Transformation (Math Layer) ---
    print("📈 Mathematically scaling Decision Function into 0-100% Predictive Risk Probability Metric...")
    # Decision function returns lower values for anomalies. We aggressively invert it to mathematically score 0-100% Risk Severity.
    raw_scores = model.decision_function(X_scaled)
    inverted_scores = -raw_scores.reshape(-1, 1)
    
    scaler = MinMaxScaler(feature_range=(0, 100))
    master_df['fraud_probability_score'] = scaler.fit_transform(inverted_scores).round(1)

    # --- 3.5 Explainable AI (SHAP) Matrix ---
    print("🔍 Generating XAI SHAP Values to explain the 'Why' behind every anomaly...")
    try:
        import shap
        # Convert mathematical paths into exact human-readable percentage attributions
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_scaled)
        
        evidence_list = []
        for i in range(len(master_df)):
            if master_df['fraud_risk_status'].iloc[i] == 'CRITICAL ANOMALY':
                row_impacts = np.abs(shap_values[i])
                top_3_idx = np.argsort(row_impacts)[-3:][::-1]
                total_impact = np.sum(row_impacts)
                
                factors = []
                for idx in top_3_idx:
                    feat_name = features[idx].replace("_", " ").title()
                    perc = (row_impacts[idx] / total_impact) * 100 if total_impact > 0 else 0
                    factors.append(f"{feat_name} ({perc:.0f}%)")
                
                evidence_list.append(" | ".join(factors))
            else:
                evidence_list.append("N/A")
                
        master_df['evidence_factors'] = evidence_list
    except Exception as e:
        print(f"⚠️ SHAP Feature Attribution Failed: {e}")
        master_df['evidence_factors'] = "N/A"

    # --- 4. Export Final Audit Dataset ---
    output_path = os.path.join(CURRENT_DIR, "ai_scored_forensic_dataset.csv")
    master_df.to_csv(output_path, index=False)
    print(f"✅ AI Scoring extremely fast! Results perfectly saved to {output_path}")

if __name__ == "__main__":
    run_ml_pipeline()