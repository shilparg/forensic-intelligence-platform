import streamlit as st
import pandas as pd
import subprocess
import json
import os
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
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
        "⚙️ Medallion Pipeline & Extraction Control",
        "📊 Executive Triage Dashboard", 
        "🕵️ Forensic Analyst Deep-Dive", 
        "🔮 Predictive AI Forecasting Hub",
        "📈 Interactive Risk Distributions",
        "☁️ BigQuery Execution Trace",
        "📖 Educational Glossary & Methodology",
        "🏗️ System Architecture & Data Flow"
    ])
    st.markdown("---")
    st.markdown("**Authors:**<br>Shilpa Kangya<br>Kamlesh Kangya", unsafe_allow_html=True)
    
    if not display_df.empty:
        st.markdown("---")
        st.markdown("### 🔍 Global Filters")
        selected_sector = st.multiselect("Filter by Sector", options=display_df['sector'].unique(), default=display_df['sector'].unique())
        if 'fiscal_year' in display_df.columns:
            selected_year = st.multiselect("Filter by Year", options=display_df['fiscal_year'].sort_values().unique(), default=display_df['fiscal_year'].unique())
        else:
            selected_year = []
            
        display_df = display_df[
            (display_df['sector'].isin(selected_sector)) & 
            (display_df['fiscal_year'].isin(selected_year) if 'fiscal_year' in display_df.columns else True)
        ]

# ==========================================
# PAGE 1: EXECUTIVE SUMMARY
# ==========================================
if page == "📊 Executive Triage Dashboard":
    st.title("📊 Executive Triage Dashboard")
    st.markdown(f"**Latest Pipeline Synchronization:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if display_df.empty:
        st.warning("⚠️ No data available. Please go to  Data Ingestion & Control to run the pipeline.")
    else:
        anomalies = display_df[display_df['fraud_risk_status'] == 'CRITICAL ANOMALY']
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'>{len(display_df)}</div><div class='metric-label'>Entities Scanned</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#DC2626;'>{len(anomalies)}</div><div class='metric-label'>Critical Anomalies</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value'>{display_df['sentiment_score'].mean():.3f}</div><div class='metric-label'>Avg Sentiment</div></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='metric-card'><div class='metric-value'>{display_df['short_ratio'].mean():.1f}%</div><div class='metric-label'>Avg Short Ratio</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---- PREDICTIVE LAYER WARNING BANNER ----
        if 'expected_short_spike_pct' in display_df.columns:
            max_spike = display_df['expected_short_spike_pct'].max()
            if max_spike > 0:
                highest_target = display_df[display_df['expected_short_spike_pct'] == max_spike].iloc[0]['ticker']
                st.error(f"🚨 **PREDICTIVE AI FORECAST:** The XGBoost Engine projects a massive **+{max_spike}%** pre-emptive short seller spike for `{highest_target}` in the next 12 months.")

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
elif page == "🕵️ Forensic Analyst Deep-Dive":
    st.title("🕵️ Forensic Analyst Deep-Dive")

    if not display_df.empty:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Matrix", "🔢 Benford's Law Analysis", "🏛️ Executive Insider Risk", "Density & Obfuscation", "Market Correlation"])
        
        with tab1:
            st.markdown("#### Master Audit Ledger")
            st.dataframe(
                display_df,
                column_config={
                    "fraud_risk_status": st.column_config.TextColumn("Risk Status"),
                    "fraud_probability_score": st.column_config.ProgressColumn("Predictive Fraud Prob %", min_value=0.0, max_value=100.0, format="%d%%"),
                    "sentiment_score": st.column_config.ProgressColumn("Sentiment", min_value=-1.0, max_value=1.0, format="%.3f"),
                    "short_ratio": st.column_config.NumberColumn("Short Ratio %", format="%.2f"),
                    "expected_short_spike_pct": st.column_config.NumberColumn("Predicted Short Spike %", format="%+.1f%%"),
                    "projected_short_ratio": st.column_config.NumberColumn("Projected Short Ratio", format="%.2f")
                },
                use_container_width=True, hide_index=True
            )
            csv = display_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Evidence (CSV)", data=csv, file_name="forensic_evidence.csv", mime="text/csv")

        with tab2:
            st.markdown("#### 🔢 Benford's Law Algorithmic Verification")
            st.markdown("<div class='explanation-box'>This AI feature mathematically proves fabricated numbers. A high <b>Benford's Deviation</b> means the numbers actively typed within the SEC filing do not match the expected biological logarithmic curve of natural financial reporting!</div>", unsafe_allow_html=True)
            
            if 'benfords_deviation' in display_df.columns:
                benford_chart = alt.Chart(display_df).mark_circle(size=180).encode(
                    x=alt.X('benfords_deviation:Q', title="Benford's Deviation Score (Higher = Fraud Risk)"),
                    y=alt.X('sentiment_score:Q', title="CEO Sentiment Tone"),
                    color=alt.Color('fraud_risk_status:N', scale=alt.Scale(domain=['NORMAL', 'CRITICAL ANOMALY'], range=['#3B82F6', '#EF4444'])),
                    tooltip=['ticker', 'fiscal_year', 'sector', 'benfords_deviation', 'sentiment_score', 'fraud_risk_status']
                ).interactive()
                st.altair_chart(benford_chart, use_container_width=True)
                with st.expander("💡 How to read this Benford's Law Chart"):
                    st.write("Each dot represents a company. The higher the dot on the X-axis, the more their reported numbers deviate from natural mathematical probability (Benford's Law). Red dots with high deviation strongly indicate fabricated numbers.")
            else:
                st.warning("Benford's Law metrics are pending dbt BigQuery pipeline execution.")

        with tab3:
            st.markdown("#### 🏛️ Executive Insider Trading Risk vs Panic")
            st.markdown("<div class='explanation-box'>Cross-examines the CEO's 'Trailing 3-Year Sentiment Volatility' (textual panic) against how much stock executives are actively abandoning.</div>", unsafe_allow_html=True)
            
            if 'insider_ownership' in display_df.columns:
                insider_chart = alt.Chart(display_df).mark_circle(size=180).encode(
                    x=alt.X('insider_ownership:Q', title="Executive Insider Total Ownership %"),
                    y=alt.X('sentiment_volatility:Q', title="3-Year Trailing Sentiment Volatility"),
                    color=alt.Color('fraud_risk_status:N', scale=alt.Scale(domain=['NORMAL', 'CRITICAL ANOMALY'], range=['#3B82F6', '#EF4444'])),
                    tooltip=['ticker', 'fiscal_year', 'sector', 'insider_ownership', 'sentiment_volatility', 'fraud_risk_status']
                ).interactive()
                st.altair_chart(insider_chart, use_container_width=True)
                with st.expander("💡 How to read this Insider Risk Chart"):
                    st.write("This plots Executive stock ownership against the CEO's 'Sentiment Volatility'. Large sentiment swings (Y-axis) combined with low/dropping executive ownership (X-axis) suggests the leadership is panicking and abandoning ship.")
            else:
                st.warning("Insider Trading metrics are pending Medallion pipeline execution.")

        with tab4:
            st.markdown("#### The 'Smoking Gun' Density Matrix")
            path = os.path.join(PLOTS_DIR, "forensic_density_matrix.png")
            if os.path.exists(path): st.image(path, use_container_width=True)
            with st.expander("💡 How to read this Density Matrix"):
                st.write("This graph plots **Word Count (X-axis)** against **Sentiment (Y-axis)**. Fraudsters often use long, confusing sentences to hide bad news. If you see a red dot in the bottom right corner (Lots of words + Very negative/defensive sentiment), that is a 'Smoking Gun' for obfuscation.")

        with tab5:
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
                with st.expander("💡 How to read this Correlation Matrix"):
                    st.write("Dark red = strong positive correlation (both metrics rise together). Dark blue = strong negative correlation (one rises as the other falls). Near-white = no relationship. Look for unexpected correlations, e.g. Benford's Deviation and Short Ratio aligning suggests the market already suspects the same fraud the AI detected.")

# ==========================================
# PAGE 3: PREDICTIVE FORECASTING
# ==========================================
elif page == "🔮 Predictive AI Forecasting Hub":
    st.title("🔮 Predictive AI Forecasting Hub")
    st.caption("Forward-looking market pressure simulations powered by Supervised XGBoost Regressors.")

    if not display_df.empty and 'expected_short_spike_pct' in display_df.columns:
        # Sort by most vulnerable
        pred_df = display_df.sort_values(by="expected_short_spike_pct", ascending=False)
        top_target = pred_df.iloc[0]

        st.markdown("### 🚨 The Predictive Radar")
        st.markdown(f"<div class='explanation-box'>The AI is specifically projecting that Wall Street is going to heavily short-sell <b>{top_target['ticker']}</b> in the coming months based on the isolation patterns detected.</div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='metric-card'><div class='metric-value'> {top_target['ticker']} </div><div class='metric-label'>Highest At-Risk Entity</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#DC2626;'>+{top_target['expected_short_spike_pct']}%</div><div class='metric-label'>Expected Short Spike</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='metric-card'><div class='metric-value'>{top_target['fraud_probability_score']}%</div><div class='metric-label'>12-Mo Fraud Probability Score</div></div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📉 Forward-Looking Market Projection", unsafe_allow_html=True)
        st.markdown("Comparing current Wall Street short-interest levels against the XGBoost forecasted future attack levels.")
        
        melted_df = pd.melt(pred_df, id_vars=['ticker'], value_vars=['short_ratio', 'projected_short_ratio'], 
                            var_name='Timeline', value_name='Short Interest (%)')
        
        melted_df['Timeline'] = melted_df['Timeline'].replace({
            'short_ratio': '1. Current Short Ratio', 
            'projected_short_ratio': '2. Projected Short Attack'
        })
        
        altair_slope = alt.Chart(melted_df).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white", size=100)).encode(
            x=alt.X('Timeline:O', title="Timeline", axis=alt.Axis(labelFontSize=13, titleFontSize=15)),
            y=alt.X('Short Interest (%):Q', title="Short Interest %", axis=alt.Axis(labelFontSize=13, titleFontSize=15)),
            color=alt.Color('ticker:N', scale=alt.Scale(scheme='category10'), legend=alt.Legend(title="Entity", labelFontSize=13, titleFontSize=15)),
            tooltip=['ticker', 'Timeline', 'Short Interest (%)']
        ).properties(height=450, title="Expected Market Trajectory (XGBoost Projection)")
        
        altair_slope = altair_slope.configure_title(fontSize=18, font='Inter').configure_axis(labelFont='Inter', titleFont='Inter').configure_legend(labelFont='Inter', titleFont='Inter')
        
        st.altair_chart(altair_slope, use_container_width=True)
        with st.expander("💡 How to read this Slope Chart"):
            st.write("The lines connect the current actual Wall Street Short Ratio to the AI's predicted future Short Ratio. An upward sloping line means the AI predicts Wall Street will aggressively target this company soon.")

        st.markdown("### 📋 The Vulnerability Leaderboard")
        st.dataframe(
            pred_df[['ticker', 'sector', 'short_ratio', 'projected_short_ratio', 'expected_short_spike_pct', 'fraud_probability_score']],
            column_config={
                "fraud_probability_score": st.column_config.ProgressColumn("Predictive Fraud Prob %", min_value=0.0, max_value=100.0, format="%d%%"),
                "short_ratio": st.column_config.NumberColumn("Current Short Ratio %", format="%.2f"),
                "expected_short_spike_pct": st.column_config.NumberColumn("Predicted Spike %", format="%+.1f%%"),
                "projected_short_ratio": st.column_config.NumberColumn("Future AI Projection", format="%.2f")
            },
            use_container_width=True, hide_index=True
        )
    else:
        st.warning("⚠️ Predictive data not found. Please ensure the full Medallion pipeline and ML scripts have successfully executed.")

# ==========================================
# PAGE 4: INTERACTIVE ANALYTICS (SEABORN GENERATOR)
# ==========================================
elif page == "📈 Interactive Risk Distributions":
    st.title("📈 Interactive Risk Distributions")
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
            y_ax = st.selectbox("Y-Axis (Numeric Measure):", ["sentiment_score", "short_ratio", "debt_to_equity", "density_index", "benfords_deviation", "current_ratio", "insider_ownership"])

        fig, ax = plt.subplots(figsize=(11, 6))
        
        # Enforce globally consistent Enterprise typography and scaling on Seaborn
        sns.set_theme(style="whitegrid", rc={"font.family": "sans-serif", "font.sans-serif": ["Inter", "Arial"]})
        sns.set_context("notebook", font_scale=1.15)
        
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
        with st.expander("💡 How to read these Seaborn Plots"):
            st.write("These charts test for statistical significance between the AI's risk flags and raw metrics. For example, a 'Violin Plot' shows where the bulk of the data lies. If the 'Critical Anomaly' shapes are drastically different from 'Normal' shapes, it proves the AI successfully isolated bizarre financial behavior.")
        
        st.markdown("---")

        st.markdown("### 2. Financial Health vs. Investor Trust")
        st.markdown("<div class='explanation-box'>Analyze core financials against market investor sentiment. Use the dropdowns to examine correlations.</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("Select X-Axis (Financial Health):", ["operating_margin", "return_on_equity", "debt_to_equity", "word_count", "current_ratio", "free_cashflow"], index=2)
        with col2:
            y_axis = st.selectbox("Select Y-Axis (Market Reaction/AI):", ["held_institutions", "short_ratio", "sentiment_score", "density_index", "benfords_deviation"], index=1)
            
        tab1, tab2 = st.tabs(["📊 Interactive Altair Chart (Hover for Tickers)", "🔵 Classic Scatter Chart"])
        
        with tab1:
            altair_chart = alt.Chart(display_df).mark_circle(size=80).encode(
                x=x_axis,
                y=y_axis,
                color=alt.Color("fraud_risk_status:N", scale=alt.Scale(domain=["NORMAL", "CRITICAL ANOMALY"], range=["#3B82F6", "#EF4444"])),
                tooltip=["ticker", x_axis, y_axis, "fraud_risk_status"]
            ).interactive()
            st.altair_chart(altair_chart, use_container_width=True)
            with st.expander("💡 How to read this Correlation Plot"):
                st.write("This allows you to customize the X and Y axis to discover new relationships. Try plotting 'word_count' against 'sentiment_score' to spot obfuscation, or 'debt_to_equity' against 'short_ratio' to see if high debt triggers market attacks. Red dots indicate companies our ML model flagged.")
            
        with tab2:
            st.scatter_chart(data=display_df, x=x_axis, y=y_axis, color="fraud_risk_status", use_container_width=True)
            with st.expander("💡 How to read this Scatter Chart"):
                st.write("Each dot is a company. Red dots are AI-flagged anomalies, blue are normal. Clusters of red dots in the extreme corners (e.g. very high debt AND very high short ratio) reveal a pattern of companies in distress. Isolated red dots far from the blue cluster are unique outliers worth investigating.")

# ==========================================
# PAGE 5: CLOUD DATA WAREHOUSE METRICS
# ==========================================
elif page == "☁️ BigQuery Execution Trace":
    st.title("☁️ BigQuery Execution Trace")
    st.markdown("Instead of just showing raw SQL code, this page executes the logic of our BigQuery models (like `Accounting_Narrative_Drift.sql`) and visualizes the results dynamically.")

    if not display_df.empty:
        st.markdown("### 0. 🔢 Benford's Law Deviation by Company")
        st.markdown("<div class='explanation-box'>This chart shows the <b>Benford's Law Deviation Score</b> for each company — calculated by our dbt BigQuery model. A higher bar means the company's reported financial numbers deviate further from natural mathematical probability, indicating potential fabrication.</div>", unsafe_allow_html=True)

        if 'benfords_deviation' in display_df.columns:
            benford_bar_df = display_df.groupby('ticker')['benfords_deviation'].mean().reset_index().sort_values('benfords_deviation', ascending=False)
            benford_bar = alt.Chart(benford_bar_df).mark_bar().encode(
                x=alt.X('ticker:N', sort='-y', title='Company Ticker', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('benfords_deviation:Q', title="Benford's Deviation Score"),
                color=alt.condition(
                    alt.datum.benfords_deviation > benford_bar_df['benfords_deviation'].median(),
                    alt.value('#EF4444'),   # Red for high risk
                    alt.value('#3B82F6')    # Blue for normal
                ),
                tooltip=['ticker', alt.Tooltip('benfords_deviation:Q', format='.4f', title="Deviation Score")]
            ).properties(height=380, title="Benford's Law Deviation — Higher = Greater Fabrication Risk").interactive()
            st.altair_chart(benford_bar, use_container_width=True)
            with st.expander("💡 How to read this chart"):
                st.write("Red bars = deviation above the dataset median (elevated fabrication risk). The taller the bar, the more the company's numbers deviate from what nature predicts. Any company with a score above 0.5 warrants closer manual inspection.")
            with st.expander("🔍 View the backend dbt SQL that generated this metric"):
                st.code("""
SELECT
    ticker, fiscal_year,
    -- Sum of geometric absolute deviations against the expected logarithmic curve
    SUM(ABS(actual_distribution - LOG10(1 + 1/CAST(leading_digit AS FLOAT64)))) as benfords_deviation
FROM benfords_distribution
WHERE total_digits > 100 
GROUP BY ticker, fiscal_year
                """, language="sql")
        else:
            st.info("Benford's Law data will appear here after the full BigQuery pipeline has executed.")


        st.markdown("### 1. The Narrative Drift Tracker")
        st.markdown("<div class='explanation-box'>This chart simulates our BigQuery <code>LAG()</code> window function. It tracks how a company's disclosure length changes year-over-year. Massive spikes indicate potential 'Obfuscation' (hiding bad news with long text).</div>", unsafe_allow_html=True)

        if 'fiscal_year' in display_df.columns:
            # Simulate the SQL LAG() function in Pandas for visualization
            drift_df = display_df.sort_values(by=['ticker', 'fiscal_year'])
            drift_df['narrative_drift'] = drift_df.groupby('ticker')['word_count'].diff().fillna(0)

            drift_ticker = st.selectbox("Select Company to View Drift:", drift_df['ticker'].unique())
            chart_data = drift_df[drift_df['ticker'] == drift_ticker].set_index('fiscal_year')[['narrative_drift']]

            st.bar_chart(chart_data, color="#F59E0B")
            with st.expander("💡 How to read this Narrative Drift Chart"):
                st.write("Each bar shows the year-over-year change in a company's SEC filing word count. A large positive bar (filing got much longer) can indicate 'Obfuscation' — management adding excessive complexity to hide bad news. A large negative bar (filing got much shorter) can indicate important details are being suppressed.")
            with st.expander("💡 View the backend SQL driving this chart"):
                st.code(f"""
SELECT ticker, fiscal_year, LENGTH(parsed_text_sample) as word_count,
  -- Calculate word count growth/shrinkage from previous year
  LENGTH(parsed_text_sample) - LAG(LENGTH(parsed_text_sample)) 
    OVER (PARTITION BY ticker ORDER BY fiscal_year) as narrative_drift
FROM `{os.getenv("GCP_PROJECT_ID")}.raw_sec_landing.raw_filings`
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
            with st.expander("💡 How to read this Financial Health Chart"):
                st.write("This compares Debt-to-Equity (how leveraged the company is) against Short Ratio (what Wall Street thinks). Companies with both a high Debt bar AND a high Short Ratio bar are being simultaneously strangled by their own debt while Wall Street bets on their collapse — the classic pre-fraud warning pattern.")
        
            with st.expander("💡 View the backend SQL driving this extraction"):
                st.code(rf"""
SELECT ticker, fiscal_year,
    -- Extract Total Debt using Regex
    REGEXP_EXTRACT(LOWER(parsed_text_sample), r'total debt.{{0,50}}?\$([0-9,.]+)') AS extracted_debt,
    -- Extract Liabilities
    REGEXP_EXTRACT(LOWER(parsed_text_sample), r'total liabilit.{{0,50}}?\$([0-9,.]+)') AS extracted_liabilities
FROM `{os.getenv("GCP_PROJECT_ID")}.raw_sec_landing.raw_filings`
                """, language="sql")

# ==========================================
# PAGE 5: EDUCATIONAL GLOSSARY
# ==========================================
elif page == "📖 Educational Glossary & Methodology":
    st.title("📖 Educational Glossary & Methodology")
    st.markdown("A comprehensive reference guide to every term used across the Forensic Intelligence Platform — from Wall Street jargon to cutting-edge AI concepts.")

    tab_fin, tab_ds, tab_ml, tab_pipe = st.tabs([
        "💰 Financial Terms",
        "📐 Data Science Terms",
        "🤖 ML & AI Terms",
        "🏗️ Pipeline & Architecture"
    ])

    # ============================================================
    # TAB 1: FINANCIAL TERMS
    # ============================================================
    with tab_fin:
        st.markdown("### 💰 Financial Market & Accounting Terms")
        st.caption("Terms used in the Master Audit Ledger and Executive Triage Dashboard.")

        with st.expander("📌 Short Ratio (Short Interest)"):
            st.markdown("""
**Definition:** The percentage of a company's available shares that investors are actively betting will fall in price (i.e., 'shorting').

**Forensic Significance:** A high Short Ratio (>5%) means Wall Street suspects the company is overvalued or concealing problems. Our AI cross-checks this against CEO language — if both the AI and the market raise red flags simultaneously, the risk multiplies.

**Example:** If SNOW has a Short Ratio of 12.3%, it means 12.3% of all tradeable shares are held by investors *betting on failure*.
            """)

        with st.expander("📌 Debt-to-Equity Ratio (D/E)"):
            st.markdown("""
**Definition:** How much of the company runs on borrowed money vs. real shareholder investment. Formula: Total Liabilities ÷ Shareholder Equity.

**Forensic Significance:** Highly leveraged companies (D/E > 2.0) are under extreme pressure to meet debt covenants. This pressure incentivizes executives to manipulate reported earnings.

**Example:** A D/E of 5.0 means for every $1 of real equity, the company owes $5. Even a small revenue miss triggers a debt spiral.
            """)

        with st.expander("📌 Operating Margin"):
            st.markdown("""
**Definition:** The percentage of revenue left after paying all operating costs, before interest and taxes. Formula: Operating Income ÷ Revenue.

**Forensic Significance:** Sudden drops in operating margin — especially when management claims strong revenue — is a classic sign of cost manipulation or revenue inflation.
            """)

        with st.expander("📌 Return on Equity (ROE)"):
            st.markdown("""
**Definition:** How efficiently a company generates profit from shareholders' money. Formula: Net Income ÷ Shareholder Equity.

**Forensic Significance:** Artificially high ROE can result from buying back shares (reducing equity denominator) to make the ratio look healthy. Our AI checks ROE against sentiment and narrative language.
            """)

        with st.expander("📌 Current Ratio & Quick Ratio"):
            st.markdown("""
**Current Ratio:** Short-term assets ÷ Short-term liabilities. Measures ability to cover immediate debts. A ratio below 1.0 is a liquidity warning.

**Quick Ratio:** The same, but excludes slow-to-sell inventory. A stricter snapshot of survival capability.

**Forensic Significance:** Companies hiding insolvency often inflate current assets on paper, making these ratios appear healthy until a sudden collapse occurs (e.g. Enron).
            """)

        with st.expander("📌 Insider Ownership %"):
            st.markdown("""
**Definition:** The percentage of company shares held by executives, directors, and other corporate insiders.

**Forensic Significance:** Rapid declines in insider ownership (executives selling off their own shares) is a powerful leading indicator that leadership knows *something is wrong* before it becomes public. Cross-referenced by the AI against CEO panic language.
            """)

        with st.expander("📌 Free Cash Flow (FCF)"):
            st.markdown("""
**Definition:** The actual cash a company generates after paying for physical assets (CapEx). Formula: Operating Cash Flow − Capital Expenditures.

**Forensic Significance:** A company can report high profits while generating negative Free Cash Flow. This 'profits without cash' pattern is a hallmark of accounting fraud (e.g. WorldCom). Our analysis compares FCF directly against reported profit margins.
            """)

        with st.expander("📌 Benford's Law Deviation"):
            st.markdown("""
**Definition:** A mathematical law that predicts the natural frequency of first digits in large datasets. In honest financial data, '1' appears as the first digit ~30% of the time, '2' ~17%, etc.

**Forensic Significance:** When financial numbers are fabricated, humans tend to distribute them too evenly (e.g. they choose '7' too often). Our AI measures how far a company's reported numbers deviate from Benford's expected distribution. A high deviation score is a mathematical proof of potential fabrication.
            """)

        with st.expander("📌 Revenue Growth & Earnings Growth"):
            st.markdown("""
**Revenue Growth:** Year-over-year percentage change in total sales.

**Earnings Growth:** Year-over-year change in net profit.

**Forensic Significance:** When a company's revenue growth far outpaces its free cash flow growth, it suggests revenue is being 'recognized' prematurely — a common fraud technique known as 'channel stuffing'.
            """)

    # ============================================================
    # TAB 2: DATA SCIENCE TERMS
    # ============================================================
    with tab_ds:
        st.markdown("### 📐 Data Science & Analytics Terms")
        st.caption("Terms used in the Statistical Risk Distributions and Cloud Data Warehouse pages.")

        with st.expander("📌 Correlation (Heatmap)"):
            st.markdown("""
**Definition:** A statistical measure of how strongly two variables move together. Ranges from -1.0 (perfect opposite) to +1.0 (perfect same direction).

**In this platform:** The Metric Correlation Matrix reveals hidden structural patterns — for example, if `benfords_deviation` and `short_ratio` are strongly correlated (+0.7), it means Wall Street is detecting the same accounting anomalies as our AI.
            """)

        with st.expander("📌 Sentiment Score (-1.0 to 1.0)"):
            st.markdown("""
**Definition:** A numeric measure of the emotional tone in a text. Generated by running SEC 10-K filings through TextBlob NLP analysis.

- **+1.0:** Extremely positive/confident language
- **0.0:** Neutral/factual
- **-1.0:** Extremely negative/defensive/panicked language

**Forensic Significance:** Guilty executives often use legalistic, hedging language. Our AI translates this into a measurable negative sentiment score.
            """)

        with st.expander("📌 Similarity Index (Cosine Similarity)"):
            st.markdown("""
**Definition:** Measures how similar two texts are, on a scale of 0 (completely different) to 1.0 (identical). Calculated using TF-IDF vectorization + cosine similarity.

**In this platform:** Compares a company's current 10-K filing to the previous year's. A score of **1.0** means the text is copied (no new disclosures). A sudden drop suggests a major change in narrative.

**Forensic Significance:** Companies in trouble often change their story dramatically in the year before a scandal breaks.
            """)

        with st.expander("📌 Sentiment Volatility"):
            st.markdown("""
**Definition:** The standard deviation of a company's sentiment score over a trailing 3-year window.

**In this platform:** Calculated using a SQL window function: `STDDEV_SAMP(sentiment_score) OVER (PARTITION BY ticker ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.

**Forensic Significance:** A high volatility score means the CEO's communication style is erratic and inconsistent — a behavioural red flag. Stable, honest companies tend to maintain a consistent narrative tone.
            """)

        with st.expander("📌 Narrative Drift"):
            st.markdown("""
**Definition:** Year-over-year change in a company's 10-K filing word count. Calculated using the SQL `LAG()` window function.

**Forensic Significance:** A massive positive spike (filing got much longer) often indicates executives dumping excessive legal boilerplate to bury bad news within a wall of text — a technique called **Obfuscation**. A sudden shrinkage may indicate omission of previously disclosed risks.
            """)

        with st.expander("📌 Density Index"):
            st.markdown("""
**Definition:** A proprietary forensic metric: `Word Count ÷ |Sentiment Score|`. A large word count combined with near-zero sentiment produces an extremely high density index.

**Forensic Significance:** High density means the filing is simultaneously very long AND very emotionally neutral. This is the textbook pattern of a document written by lawyers specifically to disclose nothing while technically complying with SEC rules.
            """)

        with st.expander("📌 Standard Deviation (StdDev)"):
            st.markdown("""
**Definition:** A measure of how spread out values are around the average. A low StdDev means values cluster tightly around the mean; a high StdDev means they are widely dispersed.

**In this platform:** Used in Violin Plots and Box Plots to show how anomalous companies deviate from their peer group's expected behavior.
            """)

        with st.expander("📌 KDE Plot (Kernel Density Estimate)"):
            st.markdown("""
**Definition:** A smoothed statistical curve showing the probability distribution of a dataset — essentially a smoothed-out histogram.

**In this platform:** Use the KDE plot to see if 'Critical Anomaly' companies cluster in a distinctly different zone from 'Normal' companies. Overlapping distributions mean our metrics are less discriminating; separated peaks prove the AI is finding real signal.
            """)

    # ============================================================
    # TAB 3: ML & AI TERMS
    # ============================================================
    with tab_ml:
        st.markdown("### 🤖 Machine Learning & AI Terms")
        st.caption("Terms used in the ML Predictive Forecasting and Executive Triage Dashboard pages.")

        with st.expander("📌 Isolation Forest (Anomaly Detection)"):
            st.markdown("""
**Definition:** An unsupervised machine learning algorithm designed to find outliers. It randomly partitions data; anomalous points require fewer partitions to isolate.

**How it works here:** Given all company metrics (sentiment, Benford's, financial ratios), the algorithm asks: "Which companies are hardest to blend in with the crowd?" Those that stand out are flagged as `CRITICAL ANOMALY`.

**Output:** An `anomaly_score` (higher = more anomalous) and a binary `fraud_risk_status` label.

**Why it's powerful:** It requires NO labelled examples of past fraud — it detects novelty purely from data structure.
            """)

        with st.expander("📌 XGBoost Regressor (Predictive Forecasting)"):
            st.markdown("""
**Definition:** Extreme Gradient Boosting — a supervised machine learning algorithm that builds many sequential decision trees, each correcting the errors of the previous one.

**How it works here:** Trained on historical patterns between fraud indicators and future short-selling activity. Given today's forensic metrics, it predicts **what the short ratio will be in the next 12 months** (`projected_short_ratio`) and the **expected percentage spike** (`expected_short_spike_pct`).

**Output:** A forward-looking market pressure forecast for each company.
            """)

        with st.expander("📌 Fraud Probability Score"):
            st.markdown("""
**Definition:** A composite score (0-100%) that combines the Isolation Forest anomaly score with the XGBoost predicted short spike into a single human-readable risk percentage.

**Interpretation:**
- **0-25%:** Low risk. Metrics align with honest industry peers.
- **25-60%:** Moderate risk. Some flags raised; watch list candidate.
- **60-85%:** High risk. Multiple forensic signals converging. Audit recommended.
- **85-100%:** Critical. AI is highly confident of material misstatement risk.
            """)

        with st.expander("📌 TF-IDF (Text Feature Extraction)"):
            st.markdown("""
**Definition:** Term Frequency–Inverse Document Frequency. Converts raw text into numerical vectors by weighting words that are *frequent in one document but rare across all documents*.

**In this platform:** Used in the Similarity Index calculation. If AAPL's 2024 10-K contains many words that were also in their 2023 10-K, the TF-IDF vectors will be very similar (high cosine similarity score).
            """)

        with st.expander("📌 TextBlob NLP (Sentiment Engine)"):
            st.markdown("""
**Definition:** A Python natural language processing library that uses a pre-trained lexicon of positive/negative English words to calculate a sentiment polarity score.

**Limitations:** TextBlob is a general-purpose tool. It may not perfectly interpret highly technical financial language. For improved accuracy, the platform is architected to be upgradeable to FinBERT (a finance-specific BERT transformer model).
            """)

        with st.expander("📌 Radar Chart (AI Decision Matrix)"):
            st.markdown("""
**Definition:** A multi-dimensional chart that plots several metrics simultaneously on axes radiating from a center point.

**In this platform:** Shows 4 key forensic signals (Sentiment, Density/Words, Short Ratio, Debt/Equity) simultaneously. The **gray dashed shape** is the industry peer average. The **red shape** is the flagged company. The further the red shape extends beyond the gray circle on any axis, the more extreme that company's deviation from its peers.
            """)

        with st.expander("📌 Unsupervised vs Supervised Learning"):
            st.markdown("""
**Unsupervised Learning (Isolation Forest):** Learns patterns from data with NO pre-labelled examples. Discovers hidden structure purely from statistical properties. Used when past fraud labels are unavailable or unreliable.

**Supervised Learning (XGBoost):** Learns from historical labelled data to make future predictions. Trained on historical short ratio movements to forecast future ones.

**Why we use both:** Unsupervised learns *what is unusual today*. Supervised learns *what unusual patterns historically predicted in the market*.
            """)

    # ============================================================
    # TAB 4: PIPELINE & ARCHITECTURE
    # ============================================================
    with tab_pipe:
        st.markdown("### 🏗️ Pipeline & Data Architecture Terms")
        st.caption("Terms used in the Architecture & Flow and Cloud Data Warehouse pages.")

        with st.expander("📌 Medallion Architecture (Bronze / Silver / Gold)"):
            st.markdown("""
A data engineering best practice for organizing data pipelines into progressive quality layers:

| Layer | Contents | This Platform |
|-------|----------|---------------|
| **🥉 Bronze** | Raw, unprocessed data as extracted | MongoDB raw SEC text + raw Yahoo Finance JSON |
| **🥈 Silver** | Cleaned, validated, structured data | BigQuery `raw_sec_landing` dataset |
| **🥇 Gold** | Business-ready, analytics-optimized | dbt-transformed `int_forensic_metrics` table |
            """)

        with st.expander("📌 Dagster (Orchestration)"):
            st.markdown("""
**Definition:** An open-source data pipeline orchestrator that manages the execution order, scheduling, retry logic, and monitoring of data assets.

**In this platform:** Dagster ensures Engine A (SEC text) and Engine B (Yahoo Finance) run in the correct sequence before the ML models execute. It provides a visual DAG (Directed Acyclic Graph) of all asset dependencies at `http://localhost:3000`.
            """)

        with st.expander("📌 dbt (Data Build Tool)"):
            st.markdown("""
**Definition:** A transformation framework that runs SQL models inside a cloud data warehouse (BigQuery) with built-in testing, documentation, and dependency management.

**In this platform:** dbt runs the `int_forensic_metrics.sql` model which JOINs the SEC text data with the Yahoo Finance data, applies Benford's Law calculations, and computes window functions for Drift and Volatility.
            """)

        with st.expander("📌 Meltano (ELT Engine)"):
            st.markdown("""
**Definition:** An open-source Extract, Load, Transform (ELT) platform that connects data sources via standardized Singer taps and targets.

**in this platform:** Used as Engine B to extract structured financial data from MongoDB (`tap-mongodb`) and load it to JSON files for downstream processing.
            """)

        with st.expander("📌 Google BigQuery"):
            st.markdown("""
**Definition:** Google's fully managed, serverless cloud data warehouse built for analytical SQL workloads at massive scale.

**In this platform:** The Silver and Gold data layers live in BigQuery. dbt models run directly inside BigQuery using BigQuery's compute engine, and results are used by the ML models for final scoring.
            """)

        with st.expander("📌 MongoDB (Document Store)"):
            st.markdown("""
**Definition:** A NoSQL document database that stores data in flexible JSON-like documents rather than rigid relational tables.

**In this platform:** Acts as the Bronze landing zone for Engine A. Raw SEC 10-K text, NLP scores (sentiment, similarity), and metadata are stored as documents in the `forensic_accounting.raw_sec_filings` collection.
            """)

        with st.expander("📌 upsert (Update + Insert)"):
            st.markdown("""
**Definition:** A database operation that updates an existing record if it exists, or inserts a new one if it doesn't.

**In this platform:** Used in `extract_sec_data.py` to prevent duplicate filings when re-running the pipeline. If AAPL FY2024 already exists in MongoDB, it updates the record rather than creating a duplicate row.
            """)


# ==========================================
# PAGE 6: ARCHITECTURE
# ==========================================
elif page == "🏗️ System Architecture & Data Flow":
    st.title("🏗️ System Architecture & Data Flow")
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
# PAGE 8: ORCHESTRATION CONTROL
# ==========================================
elif page == "⚙️ Medallion Pipeline & Extraction Control":
    st.title("⚙️ Medallion Pipeline & Extraction Control")
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