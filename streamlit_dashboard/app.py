import streamlit as st
import pandas as pd
import subprocess
import json
import os
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv

# --- 1. Enterprise Configuration & CSS ---
st.set_page_config(page_title="Forensic Analytics", page_icon="🕵️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC; color: #0F172A; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
    .metric-card { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); text-align: center; }
    .metric-value { font-size: 2rem; font-weight: 600; color: #0F172A; }
    .metric-label { font-size: 0.9rem; font-weight: 500; color: #64748B; text-transform: uppercase; }
    .arch-node { padding: 15px; border-radius: 8px; border-left: 5px solid; margin-bottom: 10px; background-color: #FFFFFF; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .node-engine-a { border-color: #0EA5E9; }
    .node-engine-b { border-color: #10B981; }
    .node-cloud { border-color: #8B5CF6; }
    .node-ai { border-color: #F59E0B; }
    .explanation-box { background-color: #FFFBEB; border-left: 4px solid #F59E0B; padding: 10px; border-radius: 4px; font-size: 0.9rem; margin-bottom: 15px;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. Pathing & Loading ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
load_dotenv(os.path.join(root_dir, ".env"))

ML_OUTPUT_PATH = os.path.join(root_dir, "core_nlp_engine", "ml_engine", "ai_scored_forensic_dataset.csv")
PLOTS_DIR = os.path.join(root_dir, "core_nlp_engine", "analysis", "plots")
DAGSTER_SCRIPT = os.path.join(root_dir, "core_nlp_engine", "orchestrate", "assets.py")

@st.cache_data
def load_data():
    if os.path.exists(ML_OUTPUT_PATH):
        return pd.read_csv(ML_OUTPUT_PATH)
    return pd.DataFrame()

display_df = load_data()

# --- 3. Dagster Trigger Logic (WITH DAGSTER FIX) ---
def trigger_dagster_pipeline(run_mode, tickers_list=None, enable_alerts=False):
    # 1. Dagster's Strict Config (Only what Dagster expects)
    dagster_payload = {
        "ops": {
            "determine_targets": {"config": {"run_mode": run_mode, "custom_tickers": tickers_list or []}}
        }
    }
    config_path = os.path.join(root_dir, "run_config.json")
    with open(config_path, "w") as f: 
        json.dump(dagster_payload, f)

    # 2. UI State Config (Saved separately for the Email Alerter)
    ui_path = os.path.join(root_dir, "ui_state.json")
    with open(ui_path, "w") as f: 
        json.dump({"enable_alerts": enable_alerts}, f)

    my_env = os.environ.copy()
    my_env["DAGSTER_HOME"] = os.path.expanduser("~/.dagster")
    os.makedirs(my_env["DAGSTER_HOME"], exist_ok=True)

    cmd = ["dagster", "job", "execute", "-f", DAGSTER_SCRIPT, "-j", "forensic_audit_job", "--config", config_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_dir, env=my_env)
        return (True, "Success") if result.returncode == 0 else (False, result.stderr)
    except Exception as e:
        return False, str(e)

# --- 4. Sidebar Navigation ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620544.png", width=60)
    st.markdown("## Forensic AI")
    st.caption("Capstone Project v3.0")
    
    st.markdown("---")
    page = st.radio("Navigation", [
        "📊 Executive Summary", 
        "🕵️ Forensic Deep-Dive", 
        "📈 Interactive Analytics",
        "☁️ Cloud SQL Visualizer",
        "📖 Educational Glossary",
        "🏗️ Architecture & Flow",
        "⚙️ Orchestration Control"
    ])
    st.markdown("---")
    st.markdown("**Authors:**<br>Shilpa Kangya<br>Kamlesh Kangya", unsafe_allow_html=True)

# ==========================================
# PAGE 1: EXECUTIVE SUMMARY
# ==========================================
if page == "📊 Executive Summary":
    st.title("Executive Audit Summary")
    st.markdown(f"**Latest Pipeline Synchronization:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if display_df.empty:
        st.warning("⚠️ No data available. Please go to Orchestration Control to run the pipeline.")
    else:
        anomalies = display_df[display_df['fraud_risk_status'] == 'CRITICAL ANOMALY']
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(display_df)}</div><div class='metric-label'>Entities Scanned</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#DC2626;'>{len(anomalies)}</div><div class='metric-label'>Critical Anomalies</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value'>{display_df['sentiment_score'].mean():.3f}</div><div class='metric-label'>Avg Sentiment</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='metric-card'><div class='metric-value'>{display_df['short_ratio'].mean():.1f}%</div><div class='metric-label'>Avg Short Ratio</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        v1, v2 = st.columns([1, 1])
        with v1:
            st.markdown("### 🎯 Audit Priority Heatmap")
            path = os.path.join(PLOTS_DIR, "audit_priority_heatmap.png")
            if os.path.exists(path): st.image(path, use_container_width=True)
            with st.expander("💡 How to read this Heatmap"):
                st.write("This shows a 'Risk Score' for each company. Darker/red colors mean the AI detected highly defensive language combined with suspicious financial numbers. Auditors should look at the red boxes first.")

        with v2:
            st.markdown("### 🕸️ AI Decision Matrix (Radar)")
            if not anomalies.empty:
                sel_ticker = st.selectbox("Select flagged entity:", anomalies['ticker'].unique())
                path = os.path.join(PLOTS_DIR, f"ai_radar_chart_{sel_ticker}.png")
                if os.path.exists(path): st.image(path, use_container_width=True)
                with st.expander("💡 How to read this Radar Chart"):
                    st.write("The gray dashed line is the 'Normal Industry Average'. The red shape is the selected company. If the red shape spikes way outside the gray circle (e.g., extremely high Debt or extremely low Sentiment), it indicates a massive deviation from normal behavior.")
            else:
                st.success("✅ No critical anomalies detected in current batch.")

# ==========================================
# PAGE 2: FORENSIC DEEP-DIVE
# ==========================================
elif page == "🕵️ Forensic Deep-Dive":
    st.title("Forensic Analyst Deep-Dive")

    if not display_df.empty:
        tab1, tab2, tab3 = st.tabs(["Data Matrix", "Density & Obfuscation", "Market Correlation"])
        
        with tab1:
            st.markdown("#### Master Audit Ledger")
            st.dataframe(
                display_df,
                column_config={
                    "fraud_risk_status": st.column_config.TextColumn("Risk Status"),
                    "sentiment_score": st.column_config.ProgressColumn("Sentiment", min_value=-1.0, max_value=1.0, format="%.3f"),
                    "short_ratio": st.column_config.NumberColumn("Short Ratio %", format="%.2f")
                },
                use_container_width=True, hide_index=True
            )
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Evidence (CSV)", data=csv, file_name="forensic_evidence.csv", mime="text/csv")

        with tab2:
            st.markdown("#### The 'Smoking Gun' Density Matrix")
            path = os.path.join(PLOTS_DIR, "forensic_density_matrix.png")
            if os.path.exists(path): st.image(path, use_container_width=True)
            with st.expander("💡 How to read this Density Matrix"):
                st.write("This graph plots **Word Count (X-axis)** against **Sentiment (Y-axis)**. Fraudsters often use long, confusing sentences to hide bad news. If you see a red dot in the bottom right corner (Lots of words + Very negative/defensive sentiment), that is a 'Smoking Gun' for obfuscation.")

        with tab3:
            st.markdown("#### Market Pressure vs. Narrative Tone")
            c1, c2 = st.columns(2)
            with c1:
                path = os.path.join(PLOTS_DIR, "forensic_regression_analysis.png")
                if os.path.exists(path): st.image(path, use_container_width=True)
                with st.expander("💡 How to read the Regression"):
                    st.write("Does Wall Street agree with the AI? This plots AI Sentiment against Wall Street Short Sellers. A downward trend line proves that when the AI detects negative CEO language, Wall Street investors are simultaneously betting against the company.")
            with c2:
                path = os.path.join(PLOTS_DIR, "correlation_heatmap.png")
                if os.path.exists(path): st.image(path, use_container_width=True)

# ==========================================
# PAGE 3: INTERACTIVE ANALYTICS (SEABORN GENERATOR)
# ==========================================
elif page == "📈 Interactive Analytics":
    st.title("Interactive Market Analytics")
    st.caption("Customizable charts to explore the financial health of the analyzed companies.")

    if not display_df.empty:
        st.markdown("### 1. Advanced Seaborn Visualizer")
        st.markdown("<div class='explanation-box'>Generate complex statistical distributions instantly using Seaborn. Compare the AI's risk flags against raw market data.</div>", unsafe_allow_html=True)
        
        sb_col1, sb_col2, sb_col3 = st.columns(3)
        with sb_col1:
            plot_type = st.selectbox("Select Seaborn Plot Type:", ["Violin Plot (Distribution)", "Box Plot (Outliers)", "KDE Plot (Density Layering)"])
        with sb_col2:
            x_ax = st.selectbox("X-Axis (Categorical):", ["fraud_risk_status", "sector", "ticker"])
        with sb_col3:
            y_ax = st.selectbox("Y-Axis (Numeric Measure):", ["sentiment_score", "short_ratio", "debt_to_equity", "density_index"])

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.set_theme(style="whitegrid")
        
        if "Violin" in plot_type:
            sns.violinplot(data=display_df, x=x_ax, y=y_ax, palette="muted", inner="quartile", ax=ax)
            plt.title(f"Violin Distribution of {y_ax} by {x_ax}")
        elif "Box" in plot_type:
            sns.boxplot(data=display_df, x=x_ax, y=y_ax, palette="Set2", ax=ax)
            sns.stripplot(data=display_df, x=x_ax, y=y_ax, color=".3", size=4, ax=ax)
            plt.title(f"Outlier Box Plot of {y_ax} by {x_ax}")
        else:
            sns.kdeplot(data=display_df, x=y_ax, hue=x_ax, fill=True, common_norm=False, palette="crest", alpha=.5, linewidth=0, ax=ax)
            plt.title(f"KDE Density Overlay of {y_ax} grouped by {x_ax}")
            
        st.pyplot(fig)
        
        st.markdown("---")

        st.markdown("### 2. Financial Health vs. Investor Trust")
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("Select X-Axis (Financial Health):", ["operating_margin", "return_on_equity", "debt_to_equity", "word_count"], index=2)
        with col2:
            y_axis = st.selectbox("Select Y-Axis (Market Reaction/AI):", ["held_institutions", "short_ratio", "sentiment_score", "density_index"], index=1)
            
        st.scatter_chart(data=display_df, x=x_axis, y=y_axis, color="fraud_risk_status", use_container_width=True)

# ==========================================
# PAGE 4: CLOUD SQL VISUALIZER
# ==========================================
elif page == "☁️ Cloud SQL Visualizer":
    st.title("BigQuery SQL Insights")
    st.markdown("Instead of just showing raw SQL code, this page executes the logic of our BigQuery models (like `Accounting_Narrative_Drift.sql`) and visualizes the results dynamically.")

    if not display_df.empty:
        st.markdown("### 1. The Narrative Drift Tracker")
        st.markdown("<div class='explanation-box'>This chart simulates our BigQuery <code>LAG()</code> window function. It tracks how a company's disclosure length changes year-over-year. Massive spikes indicate potential 'Obfuscation' (hiding bad news with long text).</div>", unsafe_allow_html=True)

        if 'fiscal_year' in display_df.columns:
            # Simulate the SQL LAG() function in Pandas for visualization
            drift_df = display_df.sort_values(by=['ticker', 'fiscal_year'])
            drift_df['narrative_drift'] = drift_df.groupby('ticker')['word_count'].diff().fillna(0)

            drift_ticker = st.selectbox("Select Company to View Drift:", drift_df['ticker'].unique())
            chart_data = drift_df[drift_df['ticker'] == drift_ticker].set_index('fiscal_year')[['narrative_drift']]

            st.bar_chart(chart_data, color="#F59E0B")
            with st.expander("💡 View the backend SQL driving this chart"):
                st.code("""
SELECT ticker, fiscal_year, LENGTH(parsed_text_sample) as word_count,
  -- Calculate word count growth/shrinkage from previous year
  LENGTH(parsed_text_sample) - LAG(LENGTH(parsed_text_sample)) 
    OVER (PARTITION BY ticker ORDER BY fiscal_year) as narrative_drift
FROM `forensic-accounting-bot.forensic_data.raw_filings`
                """, language="sql")
        else:
            st.info("Fiscal Year column not found for time-series drift.")

        st.markdown("---")

        st.markdown("### 2. Extracted Financials vs. Market Reality")
        st.markdown("<div class='explanation-box'>Visualizing the output of our <b>Key Financial Terms</b> SQL Extraction. We compare the company's internal reported Debt-to-Equity against Wall Street's Short Ratio.</div>", unsafe_allow_html=True)

        # Plotting the multi-bar chart
        if 'debt_to_equity' in display_df.columns and 'short_ratio' in display_df.columns:
            financial_df = display_df[['ticker', 'debt_to_equity', 'short_ratio']].groupby('ticker').mean()
            st.bar_chart(financial_df)
        
            with st.expander("💡 View the backend SQL driving this extraction"):
                st.code("""
SELECT ticker, fiscal_year,
    -- Extract Total Debt using Regex
    REGEXP_EXTRACT(LOWER(parsed_text_sample), r'total debt.{0,50}?\$([0-9,.]+)') AS extracted_debt,
    -- Extract Liabilities
    REGEXP_EXTRACT(LOWER(parsed_text_sample), r'total liabilit.{0,50}?\$([0-9,.]+)') AS extracted_liabilities
FROM `forensic-accounting-bot.raw_sec_landing.raw_sec_filings`
                """, language="sql")

# ==========================================
# PAGE 5: EDUCATIONAL GLOSSARY
# ==========================================
elif page == "📖 Educational Glossary":
    st.title("Glossary & Methodology")
    st.markdown("Understanding the terms used by the AI and the Financial Markets.")

    st.markdown("### 🧠 Artificial Intelligence Terms")
    st.info("**Sentiment Score (-1.0 to 1.0):** The AI reads the CEO's official SEC filings and grades their 'mood'. A score near `1.0` means they are confident and optimistic. A score below `0.0` means they are using defensive, legalistic, or panicked language.")
    st.info("**Disclosure Density / Word Count:** How many words management uses to explain their financials. When companies are performing poorly, executives tend to write massive, confusing paragraphs to hide the bad news. We call this 'Obfuscation'.")
    st.info("**Isolation Forest (Anomaly Score):** An advanced Machine Learning algorithm. Instead of looking for what is 'normal', it hunts for the 'weirdest' companies in the dataset that deviate mathematically from their peers.")

    st.markdown("### 📈 Financial Market Terms")
    st.success("**Short Ratio (Short Interest):** The percentage of Wall Street investors who are actively betting that the company's stock price will crash. A high number (>5%) means the market suspects the company is in trouble.")
    st.success("**Debt-to-Equity Ratio:** How much of the company is funded by loans (Debt) versus actual shareholder money (Equity). Highly indebted companies are under extreme pressure to fake their profits to avoid bankruptcy.")

# ==========================================
# PAGE 6: ARCHITECTURE
# ==========================================
elif page == "🏗️ Architecture & Flow":
    st.title("System Architecture & Data Flow")
    st.markdown("""
    <div class="arch-node node-engine-a">
        <h4 style="color: #0369A1; margin-top:0;">1️⃣ Engine A: Unstructured NLP Pipeline</h4>
        <p>Scrapes textual SEC 10-K filings and uses FinBERT AI to calculate Sentiment and Density.</p>
    </div>
    <div class="arch-node node-engine-b">
        <h4 style="color: #047857; margin-top:0;">2️⃣ Engine B: Structured ELT Pipeline</h4>
        <p>Meltano pulls quantitative market pressure data (Short Interest, Debt) from Yahoo Finance.</p>
    </div>
    <div class="arch-node node-cloud">
        <h4 style="color: #6D28D9; margin-top:0;">3️⃣ Cloud Synchronization & dbt Transformations</h4>
        <p>Dagster orchestrates the fusion of both engines into Google BigQuery for SQL cleaning.</p>
    </div>
    <div class="arch-node node-ai">
        <h4 style="color: #B45309; margin-top:0;">4️⃣ Machine Learning & Gen-AI Alerting</h4>
        <p>An Isolation Forest model detects anomalies, and Gemini drafts an alert email to auditors.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 7: ORCHESTRATION CONTROL
# ==========================================
elif page == "⚙️ Orchestration Control":
    st.title("Pipeline Orchestration Control")
    st.markdown("Trigger full end-to-end extraction, transformation, and AI scoring.")

    st.markdown("### 1. Target Selection")
    input_method = st.radio("Choose Target Group:", ["Default Tech Benchmark (FAANG)", "Upload Custom CSV Watchlist"])
    target_tickers = []
    mode = "peer_group"
    
    if input_method == "Upload Custom CSV Watchlist":
        mode = "custom"
        up_file = st.file_uploader("Upload Watchlist (CSV must contain 'ticker' column)", type=['csv'])
        if up_file:
            save_path = os.path.join(root_dir, "target_tickers.csv")
            with open(save_path, "wb") as f: f.write(up_file.getbuffer())
            df_temp = pd.read_csv(save_path)
            if 'ticker' in df_temp.columns:
                target_tickers = df_temp['ticker'].astype(str).str.upper().str.strip().tolist()
                st.success(f"✅ Parsed {len(target_tickers)} valid entities.")
            else:
                st.error("❌ CSV must contain a 'ticker' column.")

    st.markdown("---")
    
    # --- THE SMART UI TOGGLE ---
    st.markdown("### 2. Notification Settings")
    
    # Read Master Switch from .env
    env_email_setting = os.getenv("EMAIL_ALERTS_ENABLED", "false").lower()
    
    # Truth Table Implementation
    if env_email_setting == "false":
        st.warning("🔒 **System Override:** Automated emails are disabled at the server level (.env) for safety.")
        send_emails = st.toggle("📧 Enable Automated Email Alerts", value=False, disabled=True)
    else:
        send_emails = st.toggle("📧 Enable Automated Email Alerts", value=False, help="If checked, the AI will actively email the audit team.")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Execute Forensic Pipeline", type="primary", use_container_width=True):
        if mode == "custom" and not target_tickers:
            st.warning("Please upload a valid CSV first.")
        else:
            st.markdown(
                """
                <a href="http://localhost:3000/runs" target="_blank" style="text-decoration:none;">
                    <div style="background-color:#EEF2FF; padding:15px; border-radius:8px; border: 1px solid #4F46E5; text-align:center; margin-bottom: 15px; transition: 0.3s;">
                        <span style="font-size: 1.1rem; font-weight: 600; color:#312E81;">
                            📡 Click Here to Open Dagster & Watch Live Execution
                        </span>
                    </div>
                </a>
                """, unsafe_allow_html=True
            )
            
            with st.status("⚙️ Executing Background Orchestration...", expanded=True) as status:
                success, logs = trigger_dagster_pipeline(mode, target_tickers, send_emails)
                if success:
                    status.update(label="Pipeline Executed Successfully!", state="complete", expanded=False)
                    st.toast("✅ Data Pipeline Complete! Check the Executive Summary.", icon="🎉")
                    st.cache_data.clear() 
                else:
                    status.update(label="Orchestration Interrupted", state="error", expanded=True)
                    st.error("⚠️ A backend service failed during execution.")
                    with st.expander("🔍 View Technical Diagnostic Logs (For Admins)"):
                        st.code(logs)