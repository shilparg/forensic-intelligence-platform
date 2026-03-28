***

# 🕵️‍♂️ Forensic AI: SEC Financial Anomaly Detector
**Authors:** Shilpa Kangya & Kamlesh Kangya  
**Version:** Enterprise Capstone v3.0  

## 📖 1. Executive Summary & Business Value
Traditional financial auditing relies heavily on structured numerical data, often missing the "human element" of financial fraud: **Executive Obfuscation**. This platform introduces a **Decoupled Triangulation Architecture** that cross-references qualitative CEO narrative tone (extracted via AI) with quantitative market pressure. 

By identifying mathematical anomalies where management is highly defensive while simultaneously facing massive market pessimism and high debt, the system isolates high-risk entities and automatically dispatches Gen-AI crafted executive memos to the audit team.

---

## 🏗️ 2. Enterprise Architecture & Data Flow
The system operates on a Medallion Data Architecture (Bronze -> Silver -> Gold), physically separating the unstructured NLP pipelines from the structured financial pipelines before joining them in the cloud.

### Step-by-Step Data Flow:
1. **Engine A (Unstructured NLP - The Text):** * Scrapes SEC 10-K HTML/Text filings.
   * Feeds text into **FinBERT** (Financial NLP Transformer) to calculate `sentiment_score` (defensiveness) and `subjectivity_score`.
   * Calculates `word_count` to measure disclosure density.
2. **Engine B (Structured ELT - The Numbers):** * Uses **Meltano** to extract quantitative market data (Short Interest Ratio, Debt-to-Equity, Institutional Holdings) from Yahoo Finance.
   * *Critical Engineering Fix:* Patched the Meltano MongoDB loader `pip_url` with the `certifi` package to bypass enterprise SSL handshake blocks.
3. **Bronze Layer (Ingestion):** Both engines dump their raw, untransformed JSON data into a **MongoDB Atlas** cluster (NoSQL is required for the messy, variable-length HTML).
4. **Silver/Gold Layer (BigQuery Transformation):** * Data is synced to **Google BigQuery**.
   * We execute advanced SQL to clean, extract, and join the textual and financial data into a single `forensic_dataset` table.
5. **Machine Learning (The Decider):** An **Isolation Forest** ML model evaluates the joined dataset. It mathematically isolates outlier companies (`CRITICAL ANOMALY`).
6. **Gen-AI & Alerting:** **Gemini 1.5 Pro/Flash** synthesizes the ML output into a consolidated 3-bullet executive memo.

---

## ✨ 3. Frontend: The 7-Page Streamlit Dashboard
The UI is styled with custom Enterprise CSS to look like a production SaaS application.

1. **📊 Executive Summary:** High-level triage screen featuring an **Audit Priority Heatmap** and dynamic KPIs (Critical Anomalies, Avg Sentiment).
2. **🕵️ Forensic Deep-Dive:** Contains the Master Audit Ledger (exportable to CSV), Market Correlation regression, and the "Smoking Gun" Density Matrix.
3. **📈 Interactive Analytics (Seaborn):** A dynamic plotting lab for generating Violin, Box, and KDE plots to analyze statistical distributions.
4. **☁️ Cloud SQL Visualizer:** Simulates BigQuery operations for non-technical users. It visualizes the output of our `LAG()` window functions and Regex extractions.
5. **📖 Educational Glossary:** Translates Data Science/Finance jargon for business stakeholders.
6. **🏗️ Architecture & Flow:** A visual HTML/CSS map of the Medallion data flow.
7. **⚙️ Orchestration Control:** The command center. Users upload custom CSV watchlists, toggle email alerts, and trigger the background Dagster pipeline.

---

## 🗂️ 4. Project Directory Structure

```text
forensic_ai_capstone/
├── .env                              # Master configuration file (Ignored by Git)
├── run_config.json                   # Strict-type payload for Dagster orchestration
├── ui_state.json                     # Lightweight state manager for Streamlit/Alerter
├── target_tickers.csv                # Custom watchlist upload for pipeline runs
├── meltano_elt_engine/
│   └── meltano.yml                   # ELT configuration (Yahoo Finance -> MongoDB)
├── core_nlp_engine/
│   ├── orchestrate/
│   │   └── assets.py                 # Dagster pipeline definitions
│   ├── ml_engine/
│   │   ├── fraud_model.py            # Isolation Forest ML implementation
│   │   └── ai_scored_forensic_dataset.csv # Final output consumed by Streamlit
│   └── analysis/
│       ├── forensic_alerter.py       # Gemini Gen-AI Memo & Email Dispatcher
│       └── plots/                    # Output directory for Matplotlib/Seaborn charts
├── bigquery_sql_models/              # dbt / BigQuery Transformation Layer
│   ├── Accounting_Narrative_Drift.sql
│   ├── Find_Key_Financial_Terms.sql
│   └── Red_Flag_Report.sql
└── streamlit_dashboard/
    └── app.py                        # The 7-page interactive frontend application
```

---

## 🚀 5. Installation, Setup & Team Build Guide

### Step 1: Infrastructure Setup
1. Create a **MongoDB Atlas** cluster (M0 free tier) for the Bronze layer.
2. Set up a **Google BigQuery** project. Create datasets: `raw_sec_landing` and `forensic_data`.
3. Create a `.env` file in the root directory. **CRITICAL:** Do not place quotation marks around the `MONGO_URI` string.

```env
# Database Connections
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
GOOGLE_APPLICATION_CREDENTIALS=./gcp-service-account.json

# AI Credentials
GEMINI_API_KEY=your_google_gemini_key

# Notification Truth Table (Master Switch)
EMAIL_ALERTS_ENABLED=false     # Set 'true' for prod, 'false' for safe live-demos
EMAIL_PROVIDER=gmail           # Options: 'gmail' or 'sendgrid'
AUDIT_EMAIL_RECIPIENT=audit.team@example.com

# Email Routing Credentials
GMAIL_USER=your_bot_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
SENDGRID_API_KEY=your_sendgrid_key
SENDGRID_FROM_EMAIL=alerts@yourdomain.com
SMTP_NAME="Forensic AI Auditor"
```

### Step 2: Dependencies & Initialization
```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install Python requirements
pip install streamlit pandas seaborn matplotlib dagster dagster-webserver google-generativeai pymongo sendgrid

# 3. Initialize Meltano (Ensures MongoDB certifi patch is active)
cd meltano_elt_engine
meltano install
```

---

## 💻 6. Execution Instructions

**1. Start the Orchestrator:**
To view the background pipeline execution natively, start the Dagster UI in a terminal:
```bash
export DAGSTER_HOME=~/.dagster
dagster-webserver -f core_nlp_engine/orchestrate/assets.py
```

**2. Launch the Frontend:**
In a separate terminal:
```bash
streamlit run streamlit_dashboard/app.py
```

**3. Run an Audit:**
Navigate to the **"⚙️ Orchestration Control"** page, select your target tickers, toggle notification preferences, and click **"🚀 Execute Forensic Pipeline"**.

---

## 🧠 7. Cloud SQL Engineering (The BigQuery Vault)
This project proves advanced Data Warehousing capabilities by executing logic natively in the cloud prior to ML ingestion:
* **The Narrative Drift Tracker (`LAG()`):** Uses Window Functions (`LAG(LENGTH(text)) OVER (PARTITION BY ticker ORDER BY fiscal_year)`) to track year-over-year changes in disclosure length. Spikes indicate "Obfuscation".
* **Regex Financial Extraction:** Uses `REGEXP_EXTRACT(LOWER(text), r'total debt.{0,50}?\$([0-9,.]+)')` to mine precise dollar amounts directly out of unstructured HTML paragraphs.
* **Weighted Risk Scoring:** A custom SQL formula: `((1 - Sentiment) * 40) + (Subjectivity * 30) + (Similarity * 30)` to rank audit priority natively.
* **Metadata Discovery:** Uses `INFORMATION_SCHEMA` to audit the BigQuery table structure itself.

---

## ⚙️ 8. Orchestration & Security: The "Shared Brain"
Integrating a Streamlit UI directly with Dagster creates "Strict Type" configuration errors. 

**The Architectural Fix (Config Splitter):** When the user clicks "Execute", Streamlit generates *two* JSON files: 
* `run_config.json`: Contains strictly-typed instructions for Dagster.
* `ui_state.json`: Contains the UI toggle states, which bypasses Dagster and is read silently by the Python Alerter script.

**Daemon Binding:** We forced the Python `subprocess` to share the exact same environment as the local machine using `my_env["DAGSTER_HOME"] = os.path.expanduser("~/.dagster")` so the Live Tracker link works flawlessly.

---

## 🔒 9. The Smart Notification "Truth Table"
Automated emails pose a severe spam/security risk during live demos. We engineered a **Dual-Switch Control System**.

| `.env` Master Switch | Streamlit UI Toggle | System Action | Dashboard UI State |
| :--- | :--- | :--- | :--- |
| **FALSE** | *(Disabled)* | 🔕 **NO EMAIL** | Warning box displayed: "System Override." Toggle locked. |
| **TRUE** | **FALSE** | 🔕 **NO EMAIL** | Toggle is active. User left it off. Logs memo locally. |
| **TRUE** | **TRUE** | 📧 **SEND EMAIL** | User opted-in. Gemini drafts memo & dispatches. |

---

## 📉 10. Statistical & Plot Interpretation Guide
To prove the mathematical accuracy of the AI flags, we utilize advanced Seaborn/Matplotlib visualization. Here is the logic for interpreting the dashboard:

* **The Audit Priority Heatmap (2D Density):** Our triage screen. Darker/red colors mean the AI detected highly defensive language combined with suspicious financial numbers. 
* **AI Decision Matrix (Radar Chart):** The gray dashed line represents the 'Normal Industry Average'. The red shape is the selected company. If the red shape spikes outside the gray circle, it visually proves a massive deviation.
* **The 'Smoking Gun' Density Matrix (Scatter Plot):** Plots Word Count against Sentiment. A red dot isolated in the bottom right corner (Lots of words + Very negative/defensive sentiment) is a 'Smoking Gun' for narrative obfuscation.
* **Market Pressure vs. Narrative Tone (Regression Line):** Does Wall Street agree with our AI? A downward trend line proves that when the AI detects negative CEO language, Wall Street investors are simultaneously betting heavily against the company.
* **Advanced Distributions (Violin & KDE Plots):** Basic charts just show a dot. Seaborn allows us to visualize the *Statistical Shape* of the fraud risk. A Violin plot proves whether a flagged company is just a slight deviation or completely detached from the interquartile range.
* **The Narrative Drift Tracker (Bar Chart):** Simulates the output of a BigQuery `LAG()` window function over time. Massive upward spikes indicate sudden 'Obfuscation'—management is suddenly writing 50% more text to explain the exact same financials.

---

## 📖 11. Visual Terms & Glossary
* **Isolation Forest:** "The detective." It doesn't look for 'good' or 'bad'; it looks for 'different' or 'weird'.
* **Sentiment Score:** "The CEO's mood." It measures if the narrative is confident or defensive.
* **Short Ratio:** "The Market's Vote." If this is high, the smartest investors in the world are betting against the company.
* **Cloud SQL Visualizer:** "The Engine Room." Proves that the backend data warehouse is doing the heavy lifting.

---

## 🎤 12. Presentation Defense (Anticipated Q&A)

**Q: Why use a "Triangulation" model?**
> **A:** Because one data point can lie. A CEO might have a "bad day", or a company might have high debt for growth. But when you have **Negative Sentiment + High Debt + High Short Interest**, the probability of a "Smoking Gun" is mathematically much higher.

**Q: Why use MongoDB AND BigQuery? Isn't one database enough?**
> **A:** We used a "Best-of-Breed" pipeline. MongoDB is a NoSQL database, which is required to ingest highly variable, messy SEC HTML text. However, NoSQL is poor for analytics. We use BigQuery (an OLAP warehouse) to run structured SQL transformations and window functions at scale.

**Q: How do you prevent the AI from "Hallucinating" fraud?**
> **A:** We use **Triangulation**. The Gen-AI (Gemini) does *not* make the decision. The mathematical **Isolation Forest** model detects the anomaly first based strictly on statistical deviation. Gemini only acts as an "Audit Translator," turning those complex numbers into a readable memo.

**Q: Your 'Narrative Drift' focuses on word count. Couldn't a company just be more detailed without being fraudulent?**
> **A:** Yes, which is why a word count spike alone isn't a red flag. But when a spike happens *simultaneously* with a drop in CEO Sentiment and an increase in the Short Ratio, the probability of 'Narrative Obfuscation' increases significantly. The math filters out the noise.

**Q: Why did you use Seaborn instead of standard Streamlit charts?**
> **A:** Streamlit charts are great for simple trends, but Seaborn allows us to visualize **Statistical Distributions**. By using Violin and KDE plots, we don't just show a dot; we prove the 'Shape of Fraud'.

**Q: Why have a Master Switch in `.env` if the user has a toggle on the screen?**
> **A:** DevOps safety. The `.env` switch is a server-level lock to prevent accidental spamming of real executives during development or a live demo. By having both, we ensure the system is 'Secure by Default.'

**Q: Why separate `run_config.json` and `ui_state.json`?**
> **A:** Dagster is a strictly-typed orchestrator. If we pass UI-specific variables into its config payload, it throws a `ConfigValidationError` and crashes. Splitting the state allows our UI to govern social features without breaking the industrial data pipeline.

---

## ☑️ 13. Final Build Checklist
* [ ] MongoDB Atlas connection string verified (No quotes in `.env`).
* [ ] `GOOGLE_APPLICATION_CREDENTIALS` path verified.
* [ ] BigQuery Schema Discovery query run to verify table structure.
* [ ] `ui_state.json` exists to prevent Dagster validation crashes.
* [ ] `EMAIL_ALERTS_ENABLED` set to `false` for the live presentation.

***

## ☑️ 14. 🔐 Security & Governance (IAM)
To maintain the integrity of the forensic ledger, this platform enforces a strict **Principle of Least Privilege (PoLP)** using Google Cloud IAM:

* **The Orchestration Bot (`forensic-pipeline-bot`):** A dedicated Service Account utilized by Dagster and Meltano. It is strictly limited to `BigQuery Data Editor` and `BigQuery Job User` roles, allowing it to write to tables and execute ML compute, but preventing it from modifying the underlying dataset architecture.
* **The Dashboard Viewer (`forensic-dashboard-viewer`):** The Streamlit frontend operates on a completely separate, read-only Service Account restricted to the `BigQuery Data Viewer` role. This ensures that a compromised frontend UI cannot maliciously alter or delete the underlying forensic evidence.
* **Credential Management:** All service account JSON keys are injected via local environment variables (`GOOGLE_APPLICATION_CREDENTIALS`) and strictly `.gitignore`'d to prevent credential leakage.