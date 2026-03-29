import os
import json
import subprocess
import sys
import requests
import pandas as pd
from dagster import Config, asset, Definitions, AssetExecutionContext, define_asset_job

# --- 0. Bulletproof Pathing ---
# Dynamically locate the project structure to ensure it runs on any machine
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(ENGINE_DIR, ".."))
MELTANO_DIR = os.path.join(PROJECT_ROOT, "meltano_elt_engine")

# Define Binary Paths inside the virtual environment
VENV_BIN = os.path.join(PROJECT_ROOT, "venv", "bin")
PYTHON_EXE = sys.executable
MELTANO_EXE = os.path.join(VENV_BIN, "meltano")
DBT_EXE = os.path.join(VENV_BIN, "dbt")

# --- 1. Web UI Configuration Panel ---
class AuditConfig(Config):
    run_mode: str = "peer_group"  # Options: 'peer_group', 'all_sec', 'custom'
    custom_tickers: list[str] = ["AAPL", "MSFT"]

# --- 2. PHASE 1: Target Identification & Sector Mapping ---
@asset
def determine_targets(context: AssetExecutionContext, config: AuditConfig) -> str:
    """
    PHASE 1: Maps Tickers to CIKs and CODE-GENERATES sector_metadata.json.
    """
    target_map = {}
    sector_map = {} 
    headers = {'User-Agent': os.getenv("SEC_USER_AGENT", "ForensicBot (test@test.com)")}
    
    # Load SEC Master Index for CIK lookup
    try:
        response = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
        sec_data = response.json()
        master_lookup = {v['ticker']: str(v['cik_str']) for k, v in sec_data.items()}
    except Exception as e:
        context.log.error(f"Failed to fetch SEC Master Index: {e}")
        master_lookup = {}

    if config.run_mode == "custom":
        csv_path = os.path.join(PROJECT_ROOT, "target_tickers.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                ticker = str(row['ticker']).upper().strip()
                if ticker in master_lookup:
                    target_map[ticker] = master_lookup[ticker]
                    # This line is crucial for the ML engine's industry benchmarks
                    sector_map[ticker] = row.get('sector', 'Information Technology')
        else:
            context.log.warning("⚠️ target_tickers.csv not found. Falling back to manual list.")
            for ticker in config.custom_tickers:
                t = ticker.upper().strip()
                if t in master_lookup:
                    target_map[t] = master_lookup[t]
                    sector_map[t] = "Information Technology"

    elif config.run_mode == "peer_group":
        target_map = {"AAPL": "320193", "MSFT": "789019", "NVDA": "1045810", "GOOGL": "1652044"}
        sector_map = {t: "Information Technology" for t in target_map}

    # CRITICAL: Save Sector Metadata Bridge for the ML Engine and UI Visuals
    metadata_dir = os.path.join(ENGINE_DIR, "analysis")
    os.makedirs(metadata_dir, exist_ok=True)
    metadata_path = os.path.join(metadata_dir, "sector_metadata.json")
    
    with open(metadata_path, "w") as f:
        json.dump(sector_map, f)
        
    context.log.info(f"✅ Targets identified. Sector metadata cached for {len(sector_map)} firms.")
    return json.dumps(target_map)

# --- 3. PHASE 2: Dual-Engine Ingestion ---
@asset(deps=[determine_targets])
def run_meltano_structured_sync(context: AssetExecutionContext):
    """ENGINE B: Triggers Meltano + Python Schema Flattener."""
    context.log.info("🚀 ENGINE B: Starting Meltano Structured Sync...")
    subprocess.run([MELTANO_EXE, "run", "tap-mongodb", "target-jsonl"], 
                   cwd=MELTANO_DIR, check=True, env=os.environ)
    
    loader_script = os.path.join(MELTANO_DIR, "pandas_to_bq.py")
    context.log.info(f"📤 ENGINE B: Loading flattened Mongo data to BigQuery via {loader_script}")
    subprocess.run([PYTHON_EXE, loader_script], check=True, env=os.environ)
    
    # Phase 1: New Yahoo Finance Script execution
    yahoo_script = os.path.join(MELTANO_DIR, "yahoo_to_bq.py")
    context.log.info(f"📤 ENGINE B: Ingesting live Yahoo Finance metrics via {yahoo_script}")
    subprocess.run([PYTHON_EXE, yahoo_script], check=True, env=os.environ)
    
    return "Structured Sync Complete"

@asset
def run_unstructured_extraction(context: AssetExecutionContext, determine_targets: str):
    """ENGINE A: SEC 10-K text extraction and verification."""
    context.log.info("🧹 ENGINE A: Sanitizing MongoDB...")
    subprocess.run([PYTHON_EXE, os.path.join(ENGINE_DIR, "extract_load/cleanup_mongo.py")], 
                   check=True, env=os.environ)
    
    context.log.info("📥 ENGINE A: Extracting SEC Text...")
    # Passing the ticker_map as a CLI argument to the extractor script
    subprocess.run([PYTHON_EXE, os.path.join(ENGINE_DIR, "extract_load/extract_sec_data.py"), 
                    "--ticker_map", determine_targets], check=True, env=os.environ)
    
    context.log.info("🛡️ ENGINE A: Running Quality Gate...")
    subprocess.run([PYTHON_EXE, os.path.join(ENGINE_DIR, "extract_load/verify_mongo.py")], 
                   check=True, env=os.environ)
    return "Unstructured Extraction Passed"

# --- 4. PHASE 3: Cloud Synchronization & dbt ---
@asset(deps=[run_unstructured_extraction])
def cloud_sync(context: AssetExecutionContext):
    """Pushes validated SEC NLP payloads into BigQuery."""
    context.log.info("☁️ Phase 3: Syncing NLP data to BigQuery...")
    subprocess.run([PYTHON_EXE, os.path.join(ENGINE_DIR, "extract_load/mongo_to_bigquery.py")], 
                   check=True, env=os.environ)
    return "SEC Data Synced"

@asset(deps=[cloud_sync, run_meltano_structured_sync])
def run_dbt_models(context: AssetExecutionContext):
    """Executes dbt transformations once BOTH engines finish."""
    context.log.info("🔄 Phase 4: Executing dbt Analytical Models...")
    dbt_dir = os.path.join(ENGINE_DIR, "transform_dbt")
    subprocess.run([DBT_EXE, "build", "--profiles-dir", "."], 
                   cwd=dbt_dir, check=True, env=os.environ)
    return "dbt Logic Applied"

# --- 5. PHASE 4: AI & Executive Reporting ---
@asset(deps=[run_dbt_models])
def ai_analysis_and_output(context: AssetExecutionContext):
    """Scores anomalies and generates presentation visuals."""
    context.log.info("🧠 Phase 5a: Running Machine Learning (Isolation Forest)...")
    subprocess.run([PYTHON_EXE, os.path.join(ENGINE_DIR, "ml_engine/fraud_model.py")], 
                   check=True, env=os.environ)
                   
    context.log.info("📈 Phase 5a-B: Running Predictive ML Forecasts (XGBoost)...")
    subprocess.run([PYTHON_EXE, os.path.join(ENGINE_DIR, "ml_engine/predictive_market_model.py")], 
                   check=True, env=os.environ)
    
    context.log.info("📊 Phase 5b: Generating Multi-Ticker Executive Visuals...")
    # These scripts generate the .png files that Streamlit displays
    scripts = ["density_visualizer.py", "forensic_benchmarks.py", "forensic_triangulation.py", "executive_visuals.py"]
    for script in scripts:
        subprocess.run([PYTHON_EXE, os.path.join(ENGINE_DIR, f"analysis/{script}")], 
                       check=True, env=os.environ)
    
    context.log.info("📧 Phase 5c: Dispatching Gen-AI Forensic Memos...")
    subprocess.run([PYTHON_EXE, os.path.join(ENGINE_DIR, "analysis/forensic_alerter.py")], 
                   check=True, env=os.environ)
    
    return "Audit Platform Execution Complete"

# --- 6. Definitions & Enterprise Job Binding ---

# THE FIX: Bind all assets into a unified Job so Streamlit can trigger it securely with configurations.
forensic_audit_job = define_asset_job(
    name="forensic_audit_job",
    selection="*"
)

defs = Definitions(
    assets=[
        determine_targets, 
        run_meltano_structured_sync,
        run_unstructured_extraction, 
        cloud_sync, 
        run_dbt_models, 
        ai_analysis_and_output
    ],
    jobs=[forensic_audit_job]  # Expose the job to the Dagster Daemon
)