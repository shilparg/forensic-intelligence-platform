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

---

## 📊 Page 1: High-Level Risk Overview (Triage)

### 🧬 Data Signal Fidelity
- **⚙️ Feature & Options**: A real-time data-completeness meter.
- **🖱️ Usage**: Automatically updates based on the current BigQuery/API run.
- **🕵️ Observation**: A low percentage (e.g. 40%) is a "Data Hazard" warning. It means your audit results are based on partial information (missing debt or sentiment). Always aim for 85%+ before finalizing a fraud diagnosis.

### 🎯 Audit Priority Heatmap
- **⚙️ Feature & Options**: Altair-powered grid mapping `Ticker` vs `Risk Status`.
- **🖱️ Usage**: Hover over any box to see the exact Sentiment and Debt-to-Equity scores.
- **🕵️ Observation**: Look for "The Red Zone." If a specific company is deep red across multiple years or categories, it indicates **Persistent Structural Instability**.

### 🕸️ AI Decision Matrix (Radar)
- **⚙️ Feature & Options**: Plotly line-polar graph with 4 axes (Short Ratio, Debt/Equity, Word Count, Abs Sentiment).
- **🖱️ Usage**: Select a flagged entity from the dropdown. 
- **🕵️ Observation**: Look for the **"Asymmetric Explosion."** A stable company forms a small, centered circle. A fraud-risk company will "spike" aggressively toward one or two corners—visually isolating whether the risk is caused by narrative (words) or financials (debt).

---

## 🕵️ Page 2: Anomaly Investigation Lab

### ⚔️ Comparative Risk Combat
- **⚙️ Feature & Options**: Dual-trace radar chart comparing a "Suspect" vs. a "Stable Peer."
- **🖱️ Usage**: Select the Flagged Entity (Red) and the Benchmark Entity (Blue).
- **🕵️ Observation**: This is the "Aha!" moment. By overlaying a suspect like *Suspect X* against *Market Leader Y*, you can prove exactly where the suspect's behavior detaches from the industry "standard shape."

### 🔢 Benford's Law Analysis
- **⚙️ Feature & Options**: Scatter plot showing fabrication deviation against tone.
- **🖱️ Usage**: Interactive hover for data details.
- **🕵️ Observation**: Focus on the **"Top-Right Outliers."** These are companies whose reported numbers are mathematically impossible under Benford's Law + their CEO is using defensive/negative language. This is the hallmark of a "Manufactured Narrative."

### 🚬 The 'Smoking Gun' Density Matrix
- **⚙️ Feature & Options**: 3-dimensional bubble chart (Words vs. Tone vs. Risk Score).
- **🖱️ Usage**: Bubble size represents the total AI Risk Priority.
- **🕵️ Observation**: Look for the **"Obfuscation Quadrant"** (High Word Count + Negative Sentiment). Large red bubbles in this zone show management attempting to "drown" bad news in a massive volume of legal text.

---

## 🔮 Page 3: Predictive Risk & Trend Forecasting

### 🔮 The Predictive Radar (XGBoost Metrics)
- **⚙️ Feature & Options**: Metric cards highlighting the most vulnerable target.
- **🕵️ Observation**: If the "Expected Short Spike" is high (e.g. +20%), but the "Current Short Ratio" is low, it means the **AI has found a hidden flaw** that the market has not yet pricing in. This is a "Leading Indicator."

### 📉 Market Trajectory (Slope Chart)
- **⚙️ Feature & Options**: Altair line chart connecting Current -> Future states.
- **🖱️ Usage**: High-level visual for CFOs.
- **🕵️ Observation**: A steep upward slope is a "Sell Signal." It visually demonstrates the AI's confidence that a massive short-seller attack is imminent.

---

## 📈 Page 4: Statistical Anomaly Distributions

### 🎻 Advanced Seaborn Visualizer
- **⚙️ Feature & Options**: Dropdowns for Plot Type (Violin/Box/KDE) and Axis variables.
- **🕵️ Observation (Violin)**: Proves the AI's "Discrimination Power." If the 'Critical Anomaly' violin is physically separated or a different shape than the 'Normal' violin, you have successfully proven that your flags represent a distinct statistical population.

### ⏳ Historical Risk Playback
- **⚙️ Feature & Options**: An animated time-slider (if multi-year data is present).
- **🕵️ Observation**: Use this to find **"The Tipping Point."** You can watch a company that looked "Normal" in 2022 suddenly drift and spike into the "Red Zone" in 2024.

---

## ☁️ Page 5: Data Lineage & Traceability

### 🔄 Narrative Drift Tracker
- **⚙️ Feature & Options**: Bar chart showing Year-Over-Year word count changes.
- **🕵️ Observation**: Look for **"The Disclosure Spike."** A sudden increase of 5,000+ words in a single year usually indicates management adding massive new risk disclaimers after a secret failure.

### ⚙️ Backend SQL Code Blocks
- **⚙️ Feature & Options**: Clickable expanders.
- **🕵️ Observation**: This is your "Defense Mode." If a coach asks how you calculated Benford's Law, you open this to show the exact BigQuery REGEXP logic. It proves the platform is **Scientifically Transparent**.
