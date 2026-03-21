import streamlit as st
import pandas as pd
import subprocess
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# --- 1. Enterprise Configuration & CSS ---
st.set_page_config(page_title="Forensic Analytics", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC; 
        color: #0F172A; 
    }
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}
    
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    [data-testid="stMetricLabel"] { font-weight: 500; color: #64748B; font-size: 0.875rem; }
    [data-testid="stMetricValue"] { font-weight: 600; color: #0F172A; }

    button[kind="primary"] {
        background-color: #4F46E5; 
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
    }
    button[kind="primary"]:hover { background-color: #4338CA; color: white; }

    .stDataFrame { border-radius: 8px; overflow: hidden; border: 1px solid #E2E8F0; }
    
    /* Custom Tabs Styling */
    button[data-baseweb="tab"] { font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Pathing ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
load_dotenv(os.path.join(root_dir, ".env"))

ML_OUTPUT_PATH = os.path.join(root_dir, "core_nlp_engine", "ml_engine", "ai_scored_forensic_dataset.csv")
PLOTS_DIR = os.path.join(root_dir, "core_nlp_engine", "analysis", "plots")
DAGSTER_SCRIPT = os.path.join(root_dir, "core_nlp_engine", "orchestrate", "assets.py")

# --- 3. Logic: Dagster Trigger ---
def trigger_dagster_pipeline(run_mode, tickers_list=None):
    config_payload = {"ops": {"determine_targets": {"config": {"run_mode": run_mode, "custom_tickers": tickers_list or []}}}}
    config_path = os.path.join(root_dir, "run_config.json")
    with open(config_path, "w") as f: json.dump(config_payload, f)

    cmd = ["dagster", "job", "execute", "-f", DAGSTER_SCRIPT, "-j", "forensic_audit_job", "-c", config_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_dir)
        return (True, "Success") if result.returncode == 0 else (False, result.stderr)
    except Exception as e:
        return False, str(e)

# --- 4. Sidebar Configuration ---
with st.sidebar:
    st.markdown("### Forensic Analytics")
    st.caption("v2.1.0 Enterprise Framework")
    
    st.markdown(
        """
        <div style="background-color: #EEF2FF; padding: 10px; border-radius: 6px; border-left: 4px solid #4F46E5; margin-bottom: 15px;">
            <span style="font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 600;">Capstone Project By:</span><br>
            <span style="font-size: 0.95rem; color: #312E81; font-weight: 600;">Shilpa Kangya & Kamlesh Kangya</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.divider()
    
    data_source = st.radio("Pipeline Mode", ["View Cached Results", "Execute New Pipeline"])
    
    if data_source == "Execute New Pipeline":
        st.markdown("#### Input Parameters")
        input_method = st.radio("Target Selection", ["Default Tech Benchmark", "Upload Custom CSV"])
        
        target_tickers = []
        mode = "peer_group"
        
        if input_method == "Upload Custom CSV":
            mode = "custom"
            up_file = st.file_uploader("Upload Watchlist (CSV)", type=['csv'])
            if up_file:
                save_path = os.path.join(root_dir, "target_tickers.csv")
                with open(save_path, "wb") as f: f.write(up_file.getbuffer())
                df_temp = pd.read_csv(save_path)
                if 'ticker' in df_temp.columns:
                    target_tickers = df_temp['ticker'].astype(str).str.upper().str.strip().tolist()
                    st.success(f"Parsed {len(target_tickers)} valid entities.")
                else:
                    st.error("CSV must contain a 'ticker' column.")

        if st.button("Execute Pipeline", type="primary", use_container_width=True):
            if mode == "custom" and not target_tickers:
                st.warning("Please upload a valid CSV first.")
            else:
                with st.status("Initializing Orchestration...", expanded=True) as status:
                    st.write("Connecting to Dagster daemon...")
                    success, logs = trigger_dagster_pipeline(mode, target_tickers)
                    
                    if success:
                        status.update(label="Pipeline Executed Successfully", state="complete", expanded=False)
                        st.rerun()
                    else:
                        status.update(label="Orchestration Failed", state="error", expanded=True)
                        st.error("Dagster encountered a fatal error:")
                        st.code(logs)

    st.divider()
    st.markdown("#### Backend Services")
    st.link_button("⚙️ Open Dagster Orchestrator", "http://localhost:3000", use_container_width=True)

# --- 5. Main Dashboard Canvas ---
st.markdown("## Analytical Summary")
st.markdown(f"<span style='color:#64748B; font-size:14px;'>Latest Synchronization: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>", unsafe_allow_html=True)

display_df = pd.DataFrame()
if os.path.exists(ML_OUTPUT_PATH):
    display_df = pd.read_csv(ML_OUTPUT_PATH)

if not display_df.empty:
    st.markdown("<br>", unsafe_allow_html=True) 
    
    # KPI Row
    m1, m2, m3, m4 = st.columns(4)
    anomalies = display_df[display_df['fraud_risk_status'] == 'CRITICAL ANOMALY']
    
    m1.metric("Total Entities Scanned", len(display_df))
    m2.metric("High-Risk Flags", len(anomalies), delta=f"{len(anomalies)} anomalies", delta_color="inverse")
    
    avg_sent = display_df['sentiment_score'].mean() if 'sentiment_score' in display_df.columns else 0
    avg_short = display_df['short_ratio'].mean() if 'short_ratio' in display_df.columns else 0
    m3.metric("Mean Sentiment Index (SEC)", f"{avg_sent:.3f}")
    m4.metric("Avg Short Interest (Meltano)", f"{avg_short:.1f}%")

    # --- NEW: Dual Engine Telemetry UI ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ⚙️ Data Provenance & Orchestration")
    e1, e2 = st.columns(2)
    with e1:
        st.markdown("""
        <div style="padding: 15px; border-radius: 8px; border-left: 4px solid #0EA5E9; background-color: #F0F9FF; height: 100%;">
            <strong style="color: #0369A1;">🧠 Engine A: SEC Unstructured NLP</strong><br>
            <span style="font-size: 0.85rem; color: #475569;">Extracted raw 10-K text, computed <i>sentiment_score</i> and <i>density_index</i> using FinBERT NLP models.</span>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown("""
        <div style="padding: 15px; border-radius: 8px; border-left: 4px solid #10B981; background-color: #ECFDF5; height: 100%;">
            <strong style="color: #047857;">🚀 Engine B: Meltano ELT Sync</strong><br>
            <span style="font-size: 0.85rem; color: #475569;">Synchronized structured market profiles (<i>short_ratio</i>, <i>debt_to_equity</i>, <i>operating_margin</i>) into the master schema.</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # --- NEW: Tabbed Data Presentation ---
    c1, c2 = st.columns([4, 1])
    with c1: st.markdown("#### 📁 Audit Ledgers")
    with c2:
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Export Master CSV", data=csv_data, file_name="forensic_audit_results.csv", mime="text/csv", use_container_width=True)

    tab1, tab2, tab3 = st.tabs(["Unified AI Decision Matrix", "🚀 Meltano Structured Stream", "🧠 SEC NLP Stream"])

    # Formatting logic
    def color_risk_status(val):
        if val == 'CRITICAL ANOMALY': return 'background-color: #FEE2E2; color: #DC2626; font-weight: 600;'
        return 'background-color: #D1FAE5; color: #059669; font-weight: 500;'

    format_dict = {col: '{:.3f}' for col in ['sentiment_score', 'anomaly_score', 'density_index'] if col in display_df.columns}
    if 'short_ratio' in display_df.columns: format_dict['short_ratio'] = '{:.2f}%'
    if 'debt_to_equity' in display_df.columns: format_dict['debt_to_equity'] = '{:.2f}'

    with tab1:
        # Full Master Dataset
        styled_df = display_df.style.map(color_risk_status, subset=['fraud_risk_status']).format(format_dict)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

    with tab2:
        # Isolate Meltano Columns
        meltano_cols = [c for c in ['ticker', 'sector', 'short_ratio', 'debt_to_equity', 'return_on_equity', 'operating_margin'] if c in display_df.columns]
        meltano_df = display_df[meltano_cols]
        st.caption("Data generated and synchronized by Meltano ELT Extractors:")
        st.dataframe(meltano_df.style.format(format_dict), use_container_width=True, hide_index=True)

    with tab3:
        # Isolate NLP Columns
        nlp_cols = [c for c in ['ticker', 'sector', 'sentiment_score', 'density_index'] if c in display_df.columns]
        nlp_df = display_df[nlp_cols]
        st.caption("Data extracted and scored by the Python NLP Text Engine:")
        st.dataframe(nlp_df.style.format(format_dict), use_container_width=True, hide_index=True)

    st.divider()
    
    # Visual Analytics
    st.markdown("#### Visual Analytics")
    v1, v2 = st.columns(2)

    with v1:
        st.markdown("**Feature Correlation Matrix**")
        h_path = os.path.join(PLOTS_DIR, "correlation_heatmap.png")
        if os.path.exists(h_path): st.image(h_path, use_container_width=True)
        else: st.info("Correlation matrix not available.")

    with v2:
        st.markdown("**Entity Risk Profile**")
        if not anomalies.empty:
            sel_ticker = st.selectbox("Select flagged entity to render details:", anomalies['ticker'].unique(), label_visibility="collapsed")
            r_path = os.path.join(PLOTS_DIR, f"ai_radar_chart_{sel_ticker}.png")
            if os.path.exists(r_path): st.image(r_path, use_container_width=True)
            else: st.info(f"Radar chart for {sel_ticker} generating...")
        else:
            st.success("No anomalies detected. Baseline metrics are within normal parameters.")

else:
    st.info("System idle. Select 'Execute New Pipeline' in the sidebar to initiate a scan.")