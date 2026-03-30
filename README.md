***

### 📚 Project Documentation Hub
All technical manuals, presentation decks, and installation guides are located in the **[documentation/](file:///home/shilpakk/data_analytic/capstone/forensic-intelligence-platform/documentation/)** directory:
- **[Installation Manual](file:///home/shilpakk/data_analytic/capstone/forensic-intelligence-platform/documentation/INSTALLATION_GUIDE.md)**: How to set up and run the platform.
- **[Presentation Slide Deck](file:///home/shilpakk/data_analytic/capstone/forensic-intelligence-platform/documentation/Capstone_Presentation_Master.md)**: The "World-Class" capstone pitch.
- **[Technical Code Explainer](file:///home/shilpakk/data_analytic/capstone/forensic-intelligence-platform/documentation/CODE_EXPLAINER_MASTER.md)**: Deep-dive for dev teams.
- **[Defense Q&A Master](file:///home/shilpakk/data_analytic/capstone/forensic-intelligence-platform/documentation/QA_Defense_Master.md)**: Presentation preparation cheat-sheet.
- **[Architecture & Visual Flow](file:///home/shilpakk/data_analytic/capstone/forensic-intelligence-platform/documentation/ARCHITECTURE_VISUALS.md)**: Technical & Executive diagrams.
- **[Technical Data Walkthrough](file:///home/shilpakk/data_analytic/capstone/forensic-intelligence-platform/documentation/FORENSIC_DATA_WALKTHROUGH.ipynb)**: Jupyter Notebook investigation.
- **[Environment Check Utility](file:///home/shilpakk/data_analytic/capstone/forensic-intelligence-platform/documentation/ENVIRONMENT_CHECK_UTILITY.ipynb)**: Pre-flight connection & dependency test.
- **[Streamlit UI User Manual](file:///home/shilpakk/data_analytic/capstone/forensic-intelligence-platform/documentation/STREAMLIT_USER_MANUAL.md)**: Feature-by-feature forensic visual guide.

---

# 🕵️‍♂️ Forensic Intelligence Platform: SEC Financial Anomaly Detector
**Authors:** Shilpa Kangya & Kamlesh Kangya  
**Version:** Enterprise Capstone v3.0  

## 📖 1. Executive Summary & Business Value
Traditional financial auditing relies heavily on structured numerical data, often missing the "human element" of executive fraud: **Narrative Obfuscation**. This platform introduces a **Decoupled Triangulation Architecture** that cross-references qualitative CEO narrative tone (extracted via NLP) with quantitative market pressure. 

By identifying mathematical anomalies where management uses defensive language while simultaneously facing high debt and massive market pessimism, the system isolates high-risk entities and automatically dispatches Gen-AI crafted executive memos to the audit team.

---

## 🛠️ Tech Stack & Toolchain
- **Data Engineering**: **Dagster** (Assets-as-Code Orchestration), **Meltano** (Singer-Spec Infrastructure & Structural JSONB Flattening), **dbt Core** (Analytical Transformation).
- **Backend & Cloud**: **Google BigQuery** (High-Performance OLAP & SQL Analytical Scaling), **MongoDB Atlas** (NoSQL Unstructured Staging).
- **Machine Learning**: **Scikit-Learn** (Sector-Aware Isolation Forest), **XGBoost** (Predictive Market Forecasts).
- **NLP & Gen-AI**: **Google Gemini 1.5 Pro** (Gen-AI Audit Memos), **TextBlob** (Sentiment & Density Polarity).
- **Frontend**: **Streamlit** (Enterprise Command Center), **Seaborn/Plotly** (Statistical Anomaly Distributions).
- **Infrastructure**: **SMTP/SendGrid** (Automated Forensic Alerting Pipeline), **GCP IAM** (Principle of Least Privilege Security).

---

### 🏗️ 4. System Architecture & "Structural Defense"
The platform's architecture is built on a **Decoupled 6-Phase Pipeline** (Orchestrated by Dagster). In the dashboard, we categorize our technical journey into two distinct columns to demonstrate engineering maturity:

#### 🛠️ Industrial Challenges (The Hurdles)
- **SSL Handshake Blocks**: Bypassed using custom environment-injected `certifi` layers.
- **1-Second AI Scale**: Solved the Yahoo 429 rate-limit bottleneck by re-engineering retrieval to a batch-fetching model.
- **State Sync**: Solved Dagster-to-UI variable collisions via a **Dual-JSON state splitter**.

#### 💡 Forensic Innovations (The Brilliance)
- **The Medallion 'Gold' Join**: Using dbt SQL to join massive unstructured NoSQL text with rigid financial OLAP columns.
- **SHAP Explainable AI (XAI)**: Providing mathematically weighted feature attribution for every anomaly.
- **The Triangulation Principle**: Cross-referencing qualitative sentiment with quantitative financials and predictive market pressure.

---

## 🏗️ 2. Enterprise Architecture & Data Flow (The 6-Phase Pipeline)
The system operates on a Medallion Data Architecture (Bronze -> Silver -> Gold), physically separating the unstructured NLP pipelines from the structured financial pipelines before joining them in the cloud.

### Step-by-Step Data Flow:
1.  **Phase 1: Target Identification & Sector Mapping**: Maps Tickers to CIKs using the SEC Master Index and initializes sector-level benchmarks for ML comparison.
4.  **Phase 4: dbt Transformation Layer**: Executes 10+ SQL models in BigQuery to compute corporate risk metrics.
    *   **Benford's Law Algorithm**: Uses `REGEXP_EXTRACT_ALL` to mine leading digits from 10-K text and compares them against the **Log10 Logarithmic Curve**. A minimum threshold of 100 digits ensures the statistical significance of the deviation score.
    *   **Narrative Drift**: Uses `LAG()` window functions to track year-over-year obfuscation patterns.
    *   **Volatility**: Tracks standard deviation of executive tone over a 3-year trailing window.
5.  **Phase 5: Machine Learning (The Dual-Process Logic)**:
    *   **Isolation Forest (Unsupervised)**: Detects immediate structural anomalies in the joined dataset.
    *   **XGBoost (Supervised)**: Forecasts future market pressure and short-interest spikes based on historical patterns.
6.  **Phase 6: Reporting & Gen-AI Alerting**: **Gemini 1.5** synthesizes the ML outputs into a 24-hour executive memo, dispatched via the automated Email Alerter.

### 🧠 Explainable AI (XAI) Integration
Unlike traditional "black box" models, this platform utilizes **SHAP (SHapley Additive exPlanations)**. For every entity flagged as a `CRITICAL ANOMALY`, the system calculates the exact feature contribution percentage (e.g., "Narrative Drift (42%) | Benford's Deviation (30%)"). This provides auditors with the "Why" behind the "What," significantly reducing manual investigation time.

### ⚡ Feature Spotlight: The Dynamic Thresholding Engine
The platform includes a **Real-Time Audit Paranoia Slider** in the UI. This is not just a visual filter; it dynamically re-calculates the `fraud_risk_status` by shifting the decision boundary of the anomaly scores, allowing auditors to adjust sensitivity for different market conditions.

---

## 🛠️ 3. Engineering Challenges & Technical Solutions
Building a cross-domain forensic platform introduced several industrial engineering hurdles:

### Challenge 1: SSL Handshake Blocks in Secure Environments
**The Problem**: Meltano's default MongoDB extractor failed in enterprise-secure environments due to certificate validation errors.
**The Fix**: Engineered a custom `pip_url` patch in `meltano.yml` that injects `certifi` and `dnspython` directly into the extraction environment.

### Challenge 2: Yahoo Finance Rate Limiting
**The Problem**: Frequent extraction runs led to Yahoo's servers blocking the IP, resulting in `0` values across the board.
**The Fix**: Implemented a **Safe-Fallback Mechanism** in the Python extractor and added a "Data Quality Intelligence" warning in the Streamlit UI to notify users when fallback data is being displayed.

### Challenge 3: Streamlit-Dagster State Syncing
**The Problem**: Dagster's strict-type configuration engine
### 6. Frontend Connection: Streamlit & The Glossary
Streamlit acts as the "Command Center." To ensure the audit team understands the technology, we have implemented:
- **`ui_state.json`**: A bridge between the UI and the Dagster backend.
- **Educational Glossary**: A 5-tab reference guide covering **Financials**, **Data Science**, **AI Concepts**, **System Architecture**, and a dedicated **🔤 Abbreviations & Acronyms** cheat sheet.

### Challenge 4: Data Join Complexity (NoSQL to OLAP)
**The Problem**: Joining messy, variable-length SEC text from MongoDB with rigid financial columns in BigQuery.
**The Fix**: Leveraged **dbt (Data Build Tool)** to perform the "Gold" layer join inside BigQuery after the data was cleaned and standardized in the "Silver" layer.

### Challenge 5: The "Throttling Loop" (Scalability Optimization)
**The Problem**: Early versions of the ML engine fetched data via individual API calls per ticker, leading to severe **HTTP 429 (Too Many Requests)** errors and 15-minute wait times.
**The Fix**: Re-architected the ML engine to fetch a **Unified Forensic View** directly from BigQuery in a single batch. Data retrieval time was reduced from 15 minutes to **under 1 second**, ensuring the platform can scale to thousands of tickers.

---

## ✨ 4. Frontend: The Dashboard Experience
The UI is styled with custom Enterprise CSS to look like a production SaaS application.

1.  **📊 High-Level Risk Overview (Triage)**: High-level triage screen featuring an **Audit Priority Heatmap** and dynamic KPIs.
2.  **🕵️ Anomaly Investigation Lab**: Contains the Master Audit Ledger, Benford's Law algorithmic verification, and Market Correlation regression.
3.  **🔮 Predictive Risk & Trend Forecasting**: XGBoost-powered forward-looking market projections.
4.  **📈 Statistical Anomaly Distributions**: Advanced Seaborn plotting lab for Violin, Box, and KDE plots.
5.  **☁️ Data Lineage & Traceability**: Simulates BigQuery operations and visualizes SQL `LAG()` window functions and regex extractions.
6.  **📖 Educational Glossary**: Translates DS/Finance jargon for business stakeholders.
7.  **🏗️ System Architecture & Data Flow**: A visual map of the 6-phase pipeline.
8.  **⚙️ Medallion Pipeline & Extraction Control**: Command center for triggering Dagster runs and toggling notification preferences.

---

## 🎤 5. Presentation Defense (Coaching Q&A)

**Q: Why use a "Triangulation" model?**
> **A:** Because one data point can lie. A CEO might have a "bad day", or a company might have high debt for growth. But when you have **Negative Sentiment + High Debt + High Short Interest**, the probability of a "Smoking Gun" is mathematically much higher.

**Q: Why use MongoDB AND BigQuery? Isn't one database enough?**
> **A:** MongoDB is required to ingest highly variable, messy SEC HTML text (NoSQL). However, NoSQL is poor for analytics. We use BigQuery (an OLAP warehouse) to run structured SQL transformations and window functions at scale.

**Q: How do you prevent the AI from "Hallucinating" fraud?**
> **A:** The Gen-AI (Gemini) does *not* make the decision. The mathematical model detects the anomaly first based strictly on statistical deviation. Gemini only acts as an "Audit Translator," turning those complex numbers into a readable memo.

**Q: What is "Narrative Drift" and why does it matter?**
> **A:** It tracks year-over-year changes in disclosure length. Spikes indicate "Obfuscation"—management suddenly adding 50% more text to explain the exact same financials. We calculate this in BigQuery using the `LAG()` window function.

**Q: Why separate the ML models?**
> **A:** We use **Isolation Forest** to find *what is weird today* (Unsupervised) and **XGBoost** to predict *what that weirdness predicts for the market tomorrow* (Supervised). This gives auditors both present-state and forward-looking intelligence.

---

## 📖 6. Visual Terms & Glossary
*   **Isolation Forest**: "The detective." It doesn't look for 'good' or 'bad'; it looks for 'different' or 'weird'.
*   **FinBERT**: "The Financial Specialist." A deep-learning model that understands the exact nuance of accounting and market language.
*   **SHAP (XAI)**: "The Reasoner." Explains exactly why the AI flagged a specific company.
*   **Sentiment Score**: "The CEO's mood." It measures if the narrative is confident or defensive.
*   **Short Ratio**: "The Market's Vote." If this is high, the smartest investors in the world are betting against the company.
*   **Data Lineage & Traceability**: "The Engine Room." Proves that the backend data warehouse is doing the heavy lifting.

---

## 🔒 7. Security & Governance (IAM)
To maintain the integrity of the forensic ledger, this platform enforces a strict **Principle of Least Privilege (PoLP)**:
*   **Pipeline Bot**: Dedicated service account limited to BigQuery Write/Job permissions.
*   **Dashboard Viewer**: Read-only service account for Streamlit to ensure the UI cannot modify forensic data.
*   **Credential Management**: All keys injected via environment variables and strictly git-ignored.

***