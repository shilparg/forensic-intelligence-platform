Here is the complete, professional-grade `README.md` tailored specifically for your capstone defense. 

This document is designed to act as your "Executive Briefing." When the grading panel opens your GitHub repository, this README immediately explains the business value, the architectural flow, the directory structure, and the exact steps to run the platform.

You can copy this entire block and paste it directly into your `README.md` file in the root of your project.

***

```markdown
# 🕵️‍♂️ Forensic Intelligence Platform
**An AI-Driven Modern Data Stack for Audit Risk Triangulation**

## 📖 Executive Summary
Financial obfuscation rarely begins in the ledger; it begins in the narrative. Traditional audit methodologies rely heavily on manual, retrospective document sampling, creating a critical blind spot regarding management tone and real-time market pressure.

The **Forensic Intelligence Platform** modernizes the audit engagement by acting as an automated, first-pass forensic investigator. By orchestrating a highly decoupled, dual-engine data architecture, this platform systematically ingests unstructured SEC 10-K disclosures, quantifies linguistic obfuscation, and triangulates management's internal sentiment against external market realities (such as institutional short-selling and debt leverage).

---

## 🏗️ System Architecture & Data Flow
The platform operates on a classic "Hub and Spoke" data engineering model, ensuring complete decoupling between extraction, transformation, machine learning, and visualization.

### Phase 1: Dual-Engine Ingestion (The Spokes)
* **Core NLP Engine (Unstructured):** A custom Python/Dagster pipeline that scrapes SEC EDGAR for 10-K filings. It uses Natural Language Processing (`TextBlob`, `Scikit-Learn`) to calculate Management Sentiment, Disclosure Density (Word Count), and Year-over-Year Narrative Drift.
* **Meltano ELT Engine (Structured):** A Meltano-driven pipeline that extracts raw, structured financial datasets from a NoSQL MongoDB database, flattens the nested dictionaries using Pandas, and prepares them for cloud syncing.

### Phase 2: The Data Warehouse (The Hub)
* Both ingestion engines push their respective data into **Google Cloud BigQuery**. 
* **dbt (Data Build Tool)** is used within BigQuery to join the unstructured NLP metrics with the structured financial data, creating a unified forensic fact table.

### Phase 3: The AI Auditor (Machine Learning)
* The unified dataset is fed into an **Isolation Forest** anomaly detection algorithm. Instead of static rules, the AI evaluates the entire industry peer group and mathematically isolates companies exhibiting "Critical Fraud Risk" based on contradictory data (e.g., highly positive sentiment vs. aggressive short-selling).

### Phase 4: Executive Serving & Alerting (The Outputs)
* **Pull Reporting:** A live **Streamlit** dashboard allows Audit Directors to query BigQuery and Yahoo Finance in real-time, filtering high-risk targets dynamically.
* **Push Reporting:** The moment a "Critical Anomaly" is flagged, the platform passes the metrics to **Google Gemini 1.5 Flash**, which automatically drafts and dispatches a clinical, 3-bullet-point executive risk memo to the Audit Partner.

---

## 🗂️ Directory Structure
```text
forensic-intelligence-platform/
│
├── .gitignore                       # Protects passwords, API keys, and local environments
├── README.md                        # Executive overview and execution steps
├── requirements.txt                 # Master Python dependency list
├── gcp-service-account.json         # Google Cloud credentials (Not tracked in git)
│
├── core_nlp_engine/                 # ⚙️ SPIGOT 1: Unstructured Data Pipeline
│   ├── orchestrate/                 # Dagster orchestrator assets
│   ├── extract_load/                # SEC EDGAR scrapers and MongoDB push
│   └── transform_dbt/               # SQL transformations and data modeling
│
├── meltano_elt_engine/              # ⚙️ SPIGOT 2: Structured Data Pipeline
│   ├── meltano.yml                  # Meltano extraction configuration
│   ├── pandas_to_bq.py              # NoSQL to SQL flattening logic
│   ├── fraud_model.py               # Isolation Forest Machine Learning script
│   └── visualize_risk.py            # Seaborn static chart generation
│
├── streamlit_dashboard/             # 📊 OUTPUT 1: The Interactive BI UI
│   └── app.py                       # Streamlit web application
│
└── automated_alerting/              # 🚨 OUTPUT 2: Gen-AI Risk Memos
    └── forensic_alerter.py          # Google Gemini integration and SendGrid dispatcher
```

---

## 🚀 Execution Guide: How to Run the Platform

### Prerequisites
1. Python 3.9+ installed.
2. A valid `gcp-service-account.json` file placed in the root directory.
3. Environment variables configured for SEC EDGAR access and `GEMINI_API_KEY`.

### Step 1: Environment Setup
Install all required dependencies across the entire architecture:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Ingestion Pipelines
To extract the latest data, execute the Meltano pipeline followed by the BigQuery sync:
```bash
cd meltano_elt_engine
meltano run extract-mongodb target-jsonl
python pandas_to_bq.py
```

### Step 3: Execute the AI Risk Model
Run the Isolation Forest model to detect anomalies and generate the `comprehensive_forensic_dataset.csv`:
```bash
python fraud_model.py
```

### Step 4: Launch the Executive Dashboard
Spin up the interactive UI to visualize the risk landscape:
```bash
cd ../streamlit_dashboard
streamlit run app.py
```
*(The dashboard will automatically open in your default web browser at `http://localhost:8501`)*

### Step 5: Trigger the Gen-AI Alerter
To generate the automated Audit Partner risk memos for any detected critical anomalies:
```bash
cd ../automated_alerting
python forensic_alerter.py
```

---

## 🛠️ Technology Stack
* **Language:** Python
* **Orchestration:** Dagster
* **Extraction:** Meltano, BeautifulSoup, Requests
* **Warehouse & Transformation:** Google BigQuery, dbt
* **Machine Learning & NLP:** Scikit-Learn, Pandas, TextBlob
* **Visualization:** Streamlit, Seaborn, Matplotlib
* **Generative AI:** Google Gemini 1.5 Flash
```

***