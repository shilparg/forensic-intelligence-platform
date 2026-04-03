# 🕵️‍♂️ Capstone Pitch: Streamlit User Manual (Extended)

This manual provides a professional, feature-by-feature guide to the **Forensic Intelligence Platform**. Each section includes the technical options available and the "Professional Observation" (Audit Red Flag) to look for.

---

## 🗺️ 1. Navigation & Global Controls

### ⚠️ Audit Paranoia Slider
- **⚙️ Feature & Options**: A 0-100% threshold slider located in the sidebar.
- **🖱️ Usage**: Drag to adjust the AI's sensitivity. 
- **🕵️ Observation**: High scores (75-90%) represent the "Strict Filter"—showing only the most dangerous entities. Dropping this to 40-50% expands the audit to include "Borderline" cases where the AI is less certain but still finds structural anomalies.

### 📥 Master Audit Dossier (.md)
- **⚙️ Feature & Options**: A push-button generator that compiles SHAP factors and Risk Scores.
- **🖱️ Usage**: Click to generate a text-based report of all "Critical Anomalies" currently in the view.
- **🕵️ Observation**: This creates your "Evidence Paper Trail." It translates the visual dashboard into a formal document for Board-level reporting.

### 🔍 Forensic Global Filters
- **⚙️ Feature & Options**: Multiselect dropdowns for **Sector** and **Fiscal Year**.
- **🖱️ Usage**: Filter the dashboard to focus on a specific industry (e.g., *Healthcare*).
- **🕵️ Observation**: This allows for **Regional or Sector-Specific Deep-Dives**. If you are an industry specialist, you can immediately hide irrelevant sectors to focus on your specific domain.

---

## 📊 Page 1: High-Level Risk Overview (Triage)

### 🎯 Audit Priority Heatmap
- **⚙️ Feature & Options**: Altair-powered grid mapping `Ticker` vs `Risk Status`.
- **🖱️ Usage**: Hover over any box to see the exact Sentiment and Debt-to-Equity scores.
- **🕵️ Observation**: Look for "The Red Zone." If a specific company is deep red across multiple years, it indicates **Persistent Structural Instability**. This is your primary triage tool for prioritizing where to spend your limited audit hours.

### 🕸️ AI Decision Matrix (Radar)
- **⚙️ Feature & Options**: Plotly line-polar graph with 4 axes (Short Ratio, Debt/Equity, Word Count, Abs Sentiment).
- **🖱️ Usage**: Select a flagged entity from the dropdown. 
- **🕵️ Observation**: Look for the **"Asymmetric Explosion."** A stable company forms a small, centered circle. A fraud-risk company will "spike" aggressively toward the **Short Ratio (Engine C)** or **Debt/Equity (Engine B)** corners—visually isolating whether the risk is caused by market pressure or internal financials.

---

## 🔮 Page 3: Predictive Risk & Trend Forecasting

### 📉 Forward-Looking Market Projection (Slope Chart)
- **⚙️ Feature & Options**: An Altair-powered slope chart comparing **Present Short Interest** vs. **AI-Projected Future Shorting**.
- **🕵️ Observation**: A rising slope indicates that the **XGBoost Engine** predicts Wall Street is about to "Attack" the stock. This is a leading indicator for traders to exit positions before the narrative collapse hits the news.

---

## 🕵️ Page 2: Anomaly Investigation Lab

### 📁 Master Data Matrix
- **⚙️ Feature & Options**: Full DataFrame view of the entire BigQuery Gold layer.
- **🕵️ Observation**: This is your "Ground Truth." Unlike the visual triage screens, this ledger shows every tracked company (Normal or Critical). It is the source for the **CSV Evidence Export**, which now includes an AI-Paranoia Metadata header to ensure audit traceability.

### 🔢 Benford's Law Analysis
- **⚙️ Feature & Options**: Scatter plot showing fabrication deviation against tone.
- **🖱️ Usage**: Interactive hover for data details.
- **🕵️ Observation**: Focus on the **"Top-Right Outliers."** These are companies whose reported numbers are mathematically impossible under Benford's Law + their CEO is using defensive/negative language. This is the hallmark of a "Manufactured Narrative."

### 🚬 The 'Smoking Gun' Density Matrix
- **⚙️ Feature & Options**: 3-dimensional bubble chart (Words vs. Tone vs. Risk Score).
- **🕵️ Observation**: Look for the **"Obfuscation Quadrant"** (High Word Count + Negative Sentiment). Large red bubbles in this zone show management attempting to "drown" bad news in a massive volume of legal text.

---

## 📊 Page 5: Statistical Anomaly Distributions

### 📈 Advanced Seaborn Visualizer
- **⚙️ Feature & Options**: Dynamic plot generation (Violin, Box, KDE) across 15+ forensic dimensions.
- **🕵️ Observation (Statistical Significance)**: Use the **Violin Plot** to compare "Normal" vs. "Critical Anomaly" groups. If the shapes are drastically different, it proves the Isolation Forest is successfully separating the "Signal" (Fraud) from the "Noise" (Market Volatility).

---

## ⏳ Page 4: Historical Risk Playback (Time-Series)

### 📽️ The Velocity of Risk (Animation)
- **⚙️ Feature & Options**: An interactive time-slider (X: Debt, Y: Tone, Size: Probability).
- **🕵️ Observation (The Downward Spiral)**: Watch for the **"South-East Drift."** The most dangerous forensic signal is a dot moving from the top-left (High Sentiment, Low Debt) toward the bottom-right (Low Sentiment, High Debt) while **growing in size**. This visually captures a management team attempting to "talk their way out" of insolvency.

---

## ☁️ Page 5: Data Lineage & Traceability

### 🛠️ Admin: JSON Ingestion Buffer
- **⚙️ Feature & Options**: Raw JSON payload expander.
- **🕵️ Observation (Anti-Black-Box Protocol)**: This proves the platform's **Zero-Manipulation Policy**. By showing the raw data before the ML Engine scales it, we provide an "Immaculate Audit Trail" that can be defended in a court of law or a regulatory review.

### ⚙️ Backend SQL Code Blocks
- **⚙️ Feature & Options**: Clickable expanders.
- **🕵️ Observation**: This is your "Defense Mode." If a coach asks how you calculated Benford's Law, you open this to show the exact BigQuery REGEXP logic. It proves the platform is **Scientifically Transparent**.

---

## ⚙️ Page 6: Medallion Pipeline & Extraction Control
*This section controls the industrial ingestion of the platform.*

### 🎯 Target Selection Panel
- **⚙️ Feature & Options**: Radio Buttons for **Benchmark** or **Custom CSV Watchlist**.
- **🖱️ Usage**: Choose between a static FAANG peer group or upload a CSV with specific tickers you wish to audit.
- **🕵️ Observation**: This is the "Orchestration Control." It allows the auditor to dynamically define the scope of the day's investigation.

### 📧 Automated Notification Toggle
- **⚙️ Feature & Options**: A persistent UI toggle that connects to the `forensic_alerter.py` backend.
- **🕵️ Observation**: If toggled **ON**, the AI will automatically dispatch an executive memo for every flagged anomaly discovered in the run.
