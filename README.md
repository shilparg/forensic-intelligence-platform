# 🕵️‍♂️ Forensic Intelligence Platform: SEC Financial Anomaly Detector
**Authors:** Shilpa Kangya & Kamlesh Kangya  
**Version:** Enterprise Capstone v3.0  

***

### 📚 Project Documentation Hub
All technical manuals, presentation decks, and installation guides are located in the **[documentation/](documentation/)** directory:
- **[Installation Manual](documentation/INSTALLATION_GUIDE.md)**: How to set up and run the platform.
- **[Presentation Slide Deck](documentation/CAPSTONE_PRESENTATION_MASTER.md)**: The Capstone pitch.
- **[Technical Code Explainer](documentation/CODE_EXPLAINER_MASTER.md)**: Deep-dive for dev teams.
- **[Architecture & Visual Flow](documentation/ARCHITECTURE_VISUALS.md)**: Technical & Executive diagrams.
- **[Streamlit UI User Manual](documentation/STREAMLIT_USER_MANUAL.md)**: Feature-by-feature forensic visual guide.
- **[Technical Data Walkthrough](notebooks/02_FORENSIC_WALKTHROUGH.ipynb)**: Jupyter Notebook investigation.
- **[Environment Check Utility](notebooks/01_ENVIRONMENT_CHECK.ipynb)**: Pre-flight connection & dependency test.

---

## 📖 1. Executive Summary & Business Value
Traditional financial auditing relies heavily on structured numerical data, often missing the "human element" of executive fraud: **Narrative Obfuscation**. This platform introduces a **Decoupled Triangulation Architecture** that cross-references qualitative CEO narrative tone (extracted via NLP) with quantitative market pressure. 

By identifying mathematical anomalies where management uses defensive language while simultaneously facing high debt and massive market pessimism, the system isolates high-risk entities and automatically dispatches Gen-AI crafted executive memos to the audit team.

---

## 🛠️ 2. Tech Stack & Industrial Toolchain
- **Data Engineering**: **Dagster** (Assets-as-Code Orchestration), **Meltano** (Singer-Spec Infrastructure & Structural JSONB Flattening), **dbt Core** (Analytical Transformation).
- **Backend & Cloud**: **Google BigQuery** (High-Performance OLAP & SQL Analytical Scaling), **MongoDB Atlas** (NoSQL Unstructured Staging).
- **Machine Learning**: **Scikit-Learn** (Sector-Aware Isolation Forest), **XGBoost** (Predictive Market Forecasts).
- **NLP & Gen-AI**: **Google Gemini 1.5 Pro** (Gen-AI Audit Memos), **SHAP** (Explainable AI / XAI).
- **Frontend**: **Streamlit** (Enterprise Command Center), **Seaborn/Plotly** (Statistical Anomaly Distributions).

---

## 🏗️ 3. Enterprise Architecture & 6-Phase Pipeline
The system operates on a Medallion Data Architecture (Bronze -> Silver -> Gold), physically separating the unstructured NLP pipelines from the structured financial pipelines before joining them in the cloud.

### The Decoupled Data Flow:
1.  **Phase 1: Target Identification**: Maps Tickers to CIKs using the SEC Master Index and initializes sector clusters.
2.  **Phase 2: Ingestion Engines**: 
    - **Engine A (Qualitative)**: SEC text scraped into MongoDB.
    - **Engine B (Quantitative)**: Meltano pulls financial metrics into JSONB landing zones.
3.  **Phase 3: Cloud Migration**: Flattens NoSQL data and migrates it to BigQuery (Silver Layer).
4.  **Phase 4: dbt Brain**: Executes **Benford's Law Algorithms** and **Narrative Drift** window functions.
5.  **Phase 5: ML Matrix**: Runs **Isolation Forest** (Anomaly) and **XGBoost** (Prediction) scored via **SHAP**.
6.  **Phase 6: AI Reporting**: Gemini 1.5 Pro synthesizes insights into professional audit memos.

---

## 🧠 4. AI Methodology (The Brains)
- **Isolation Forest (Unsupervised)**: Detects "weird" outliers without needing past fraud examples.
- **XGBoost (Supervised)**: Forecasts future market pressure and short-interest spikes based on historical patterns.
- **SHAP (XAI)**: Provides feature-level attribution (e.g., "Why was AAPL flagged? Because of 40% Narrative Drift").
- **Benford's Law**: Mathematically proves manufactured numbers by detecting deviations from logarithmic probability.

---

## 🛠️ 5. Engineering Challenges & Technical Fixes
- **SSL Handshake Blocks**: Bypassed using custom environment-injected `certifi` layers in the ELT engine.
- **1-Second AI Scale**: Eliminated the Yahoo 429 bottleneck by re-engineering to a **Unified Batch Retrieval** model in BigQuery.
- **State management**: Solved UI-to-Backend variable collisions via a **Dual-JSON state splitter** strategy.
- **Data Fidelity Meter**: Built a custom "Trust Engine" in Streamlit to warn auditors when upstream APIs are throttled.

---

## ✨ 6. The Frontend: Auditor Command Center
The UI provides an executive-grade experience across 8 specialized modules:
1.  **📊 Risk Triage**: High-level Priority Heatmaps and "Data Fidelity" indicators.
2.  **🕵️ Investigation Lab**: The "Master Ledger" with AI evidence explainers and Benford Scatter plots.
3.  **🔮 Predictive Hub**: XGBoost-powered market forecasting slope charts.
4.  **📈 Statistical Gallery**: Advanced Seaborn distributions (Violin/Box) for academic validation.
5.  **☁️ Data Lineage**: Professional transparency showing the BigQuery SQL logic behind the models.

---

## 🔒 7. Security & Data Governance
- **Principle of Least Privilege (PoLP)**: Dedicated service accounts for Pipeline (Write) and Dashboard (Read).
- **Environment Integrity**: All credentials git-ignored; system state is managed via **Variable-Driven Portability**, allowing zero-code re-targeting of BigQuery datasets.
- **Traceability**: Full asset lineage tracked via Dagster to ensure every Risk Score is verifiable.

---

## 🚀 8. Installation & Deployment
Refer to the **[INSTALLATION_GUIDE.md](documentation/INSTALLATION_GUIDE.md)** for environment setup, GCP authorization, and local orchestration instructions.

## 🔮 9. Future Roadmap (v2.0 - v4.0)
The platform is built on an extensible **Industrial Data Factory** architecture. For a deep dive into the **Alternative Data Integration**, **Real-Time Sentiment Streaming**, and **Multi-Modal AI** plans, refer to the:
👉 **[FUTURE_ROADMAP.md](documentation/FUTURE_ROADMAP.md)**

---

## 🔤 10. Glossary & Visual Terms
- **Industrial Data Factory**: The Dagster-orchestrated 6-phase lifecycle.
- **Quant Engine**: The Meltano-powered structured financial pipeline.
- **NLP Engine**: The SEC text-mining sentiment logic.
- **The Triage Heatmap**: The primary screen for auditor focus prioritization.

***
