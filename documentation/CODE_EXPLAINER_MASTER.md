# 📘 Capstone Pitch: Technical Code Explainer & Briefing Guide

This document provides a deep-dive explanation of the **Forensic Intelligence Platform's** architecture, code flow, and technical implementation. It is designed to help you and your team understand the "How" and "Why" behind the platform.

---

## 🏛️ Part 0: Core Forensic Concepts (The "Why")

Before diving into the code, it is important to understand the three core concepts that drive the platform's logic:

### 1. The Triangulation Concept
**Concept:** Fraud rarely exists in a single data point. It is hidden in the gaps between what management says and what the numbers show.
**Implementation:** We cross-reference **Narrative Fear** (Engine A) with **Financial Fact** (Engine B) and **Market Pressure** (XGBoost). Our AI only fires when these three signals converge.

### 2. The Obfuscation Concept (Management Fear)
**Concept:** Corporate fraudsters often attempt to "smother" bad news with complexity. This is called **Narrative Obfuscation**.
**Implementation:** We calculate a **Density Index**. If a company's word count spikes significantly year-over-year while their metrics are flat, the AI flags this as a primary risk indicator for deliberate obfuscation.

### 3. The Medallion Data Concept
**Concept:** Forensic data is "messy" at the source and must be refined through strict layers to maintain its legal and audit integrity.
**Implementation:**
- **🥉 Bronze (Raw)**: Ingesting messy SEC text into MongoDB.
- **🥈 Silver (Standardized)**: Moving cleaned and deduped tables into BigQuery.
- **🥇 Gold (Insight)**: The final, high-fidelity dataset where all dbt transforms (Benford's Law, Drift) have been applied.

---

## 🤖 Part 0-B: ML & AI Research Methodology

We utilize a "Dual-Model Architecture" to ensure we are capturing both structural anomalies (today) and predictive market pressure (tomorrow).

### 1. Unsupervised Anomaly Detection (Isolation Forest)
**Concept:** Real-world fraud is a "Cold Start" problem. We don’t have thousands of labeled examples of corporate crime. 
**Logic:** We use **Isolation Forest**. Instead of training the AI on "what fraud looks like," we train it on "what normal looks like." The model then isolates the outliers that are mathematically most difficult to fit into the normal crowd. 

**The 10-Feature Forensic Space:**
The AI analyzes a multi-dimensional vector for every company:
1.  **Engine A (Textual)**: `sentiment_score`, `density_index`.
2.  **Engine B (Market)**: `short_ratio`, `debt_to_equity`, `return_on_equity`, `operating_margin`, `insider_ownership`, `current_ratio`.
3.  **Engine C (Forensic Math)**: `benfords_deviation`, `sentiment_volatility` (Historical Tone Drift). This is the **Convergence Layer** where cleaned SEC text and Yahoo metrics are mathematically joined to find hidden anomalies.

> [!NOTE]
> **V3.0 Global Batch Scaling**: The current AI uses **Global Batch Normalization** (StandardScaler). All companies processed in a single run are scaled together, allowing the AI to identify the "Extreme Outliers" of the entire portfolio. Our **v4.0 Roadmap** includes **Sector-Contextual Normalization** for industry-relative isolation.

### 2. Supervised Risk Forecasting (XGBoost)
**Concept:** Forensic metrics are leading indicators of market behavior (e.g., short-selling spikes).
**Logic:** We use **XGBoost (Extreme Gradient Boosting)** as a **Forensic Forecaster**. It is a supervised model trained on historical patterns. If the AI detects a specific combination of Narrative Fear (A) and Benford's Deviation (C), it forecasts how much a professional short-seller is likely to bet against that company in the next 12 months.


### 3. Explainable AI (The SHAP Concept)
**Concept:** Auditors cannot testify in court or to a board based on a "Black Box." 
**Logic:** We use **SHAP (SHapley Additive exPlanations)**. This is a game-theoretic approach that assigns an "attribution percentage" to every feature. If a company is flagged at 90% risk, SHAP proves exactly how much of that 90% came from "Sentiment" vs. "Benford's Deviation."

---

## 🗺️ Part 1: The 6-Phase Pipeline Map (The Code Flow)

The platform operates as a massive industrial data factory, moving from raw identification to predictive intelligence across six distinct phases orchestrated by **Dagster**.

### 🏁 Phase 1: Target Identification & Sector Mapping
- **Function**: `determine_targets` in `assets.py`
- **Logic**: 
    1. Fetches the official **SEC Master Index** (`company_tickers.json`) to map human-readable Tickers (e.g., AAPL) to Central Index Keys (CIKs).
    2. **Target Selection Modes**: Supports either a **Static Peer Group** (FAANG) for benchmarking or a **Custom CSV Upload** for targeted auditor deep-dives.
    3. Generates `sector_metadata.json`. This is crucial for the ML Engine later, as it ensures the AI compares a "Tech" company against other "Tech" companies rather than a "Utility" firm.
- **Output**: A JSON map of active targets and a cached metadata file.

### 🏗️ Phase 2: Dual-Engine Data Ingestion
The platform physically separates its "qualitative" and "quantitative" pipelines to prevent bottlenecks.
- **Engine A (Unstructured)**: `run_unstructured_extraction`
    - Scrapes the **MD&A (Management's Discussion & Analysis)** section of SEC 10-K filings using `extract_sec_data.py`.
    - Stores the massive raw HTML/Text in **MongoDB** (NoSQL), which excels at handling high-volume, variable-length text.
- **Engine B (Structured)**: `run_meltano_structured_sync`
    - Uses **Meltano** to pull live market metrics (Short Ratio, Debt-to-Equity, etc.) from Yahoo Finance via `yahoo_to_bq.py`.
    - **Structural Flattening**: Uses a specialized Python flattener (`pandas_to_bq.py`) to convert raw NoSQL JSONB Mongo data into structural BigQuery columns for SQL analytical readiness.

### ☁️ Phase 3: Cloud Synchronization (Migration)
- **Function**: `cloud_sync` calling `mongo_to_bigquery.py`
- **Logic**: Once Engine A finishes its local NLP processing (Sentiment/Density), the "Bronze" data in MongoDB is pushed into **Google BigQuery** (The Silver Layer). This transforms messy NoSQL documents into structured SQL tables.

### 🔄 Phase 4: Transformation (The dbt Brain)
- **Function**: `run_dbt_models` calling `dbt build`
- **Logic**: This is where the core "Forensic Math" happens. We use **dbt (Data Build Tool)** to execute complex SQL models in BigQuery:
    - **Benford's Law**: Extracts leading digits from text to find manufactured numbers.
    - **Narrative Drift**: Uses `LAG()` window functions to compare this year's filing to last year's.
- **Output**: The "Gold Layer"—a perfectly joined table of narrative and financial signals.

### 🧠 Phase 5: ML Scoring & Analytics
- **Functions**: `fraud_model.py` (Isolation Forest) & `predictive_market_model.py` (XGBoost)
- **Logic**:
    1. **Isolation Forest**: An unsupervised model that finds "weird" outliers without needing past fraud examples.
    2. **SHAP (XAI)**: Calculates the exact weight of each feature (e.g., "Why was TSLA flagged? Because of 45% Narrative Drift").
    3. **XGBoost**: A supervised model that predicts the *future* short-interest spike based on current forensic markers.

### 📧 Phase 6: Reporting & Gen-AI Alerting
- **Function**: `forensic_alerter.py`
- **Logic**: 
    1. Pulls the ML scores and SHAP factors.
    2. Sends them to **Google Gemini 1.5 Pro**.
    3. Gemini synthesizes a professional executive memo.
    4. The memo is dispatched via **SMTP/SendGrid** to the audit team's email.

---

## 🧬 Part 2: Deep-Dive Technical Logic

### 1. Orchestration: Why Dagster?
Traditional "Cron jobs" are dangerous for forensic work. If one step fails, the whole audit is corrupted. **Dagster** treats data as "Assets-as-Code." It tracks the "Lineage" of each piece of data. If the SEC scraper fails, Dagster knows *exactly* where to resume, ensuring the final Risk Score is always based on fresh, valid data.

### 2. Database Architecture: NoSQL vs. OLAP
- **MongoDB (NoSQL)**: We use this because SEC filings are messy. One 10-K might be 50KB, another might be 5MB. MongoDB stores this "unstructured" text easily.
- **BigQuery (OLAP)**: We use this for the "Gold" layer because it is optimized for massive SQL transformations. You cannot run a "Benford's Law" regex across 10,000 documents in MongoDB as fast as you can in BigQuery.

### 3. Isolation Forest: The Multi-Dimensional Detective
Traditional fraud detection relies on "Rules" (e.g., *Is debt > X?*). Our **Isolation Forest** (Model 1) uses a multi-dimensional approach to find what "normal" looks like.

- **Engine C Integration**: The model treats `benfords_deviation` and `sentiment_volatility` as core coordinates in its search space.
- **The "Cold Start" Solution**: Because real fraud is rare, we don't train on past labeled examples. Instead, we isolate the points that are mathematically most difficult to fit into the "Normal" crowd. A high Benford's Deviation often becomes the primary reason a record is isolated.
- **Probability Scoring**: We invert the model's `decision_function` to create a human-readable **0-100% Risk Probability** score, making it easier for auditors to triage.

### 4. Engine C: The Convergence Layer (Forensic Math)
Engine C is not a single file, but a **Logical Layer** in the dbt transformation phase. It is where the "Bronze" data from SEC and Yahoo Finance are refined into "Gold" insights.

**Benford's Law SQL:** In `fct_benfords_law.sql`, we use:
```sql
UNNEST(REGEXP_EXTRACT_ALL(filing_text, r'\b([1-9])\d*')) AS digit
```
This mines every single leading digit mentioned in a 100-page filing. By unnesting these digits directly in BigQuery's analytical engine, we can process thousands of documents in seconds. 

> [!IMPORTANT]
> **Statistical Significance (The Coach Requirement):** We implement a `WHERE total_digits > 100` constraint. This ensures the sample size of numbers in a filing is large enough to satisfy the **Law of Large Numbers**, preventing false anomalies caused by small datasets.

### 4. The XGBoost Forecaster: Predicting the "Short Attack"
While the Isolation Forest (Model 1) identifies **current** anomalies, XGBoost (Model 2) provides **forward-looking intelligence**.

- **The Features**: It consumes the outputs of Engine A, B, and C as its feature set.
- **The Prediction**: It is trained to predict the `short_ratio` (the intensity of professional short-selling). 
- **The Output**: It calculates an `expected_short_spike_pct`. If Engine C shows a high mathematical deviation, XGBoost forecasts a corresponding spike in market skepticism. 


### 4. AI Interpretability: SHAP vs. Black Box
Machine Learning often tells you *what* is wrong but not *why*. We use **SHAP (SHapley Additive exPlanations)**. It breaks down the 1.0 (Anomaly) score into its component parts. This allows the auditor to defend their finding: *"I am auditing Company X because the AI attributed 60% of its risk to its defensive Narrative Tone."*

### 5. State Management: The `ui_state.json` Bridge
Streamlit is a web UI, but Dagster is a heavy-duty backend. To connect them, we use a "Dual-State" strategy:
- **`run_config.json`**: Tells Dagster which tickers to run.
- **`ui_state.json`**: Persists UI settings (like email alerts on/off) so that the backend `forensic_alerter.py` knows the user's current preferences even when the web session is closed.

### 6. The Auditor Command Center (UI/UX Architecture)
Streamlit serves as the high-stakes interface between the auditor and the Dagster pipeline. 
- **Reactive State Management**: We leverage `st.session_state` to ensure the dashboard remains interactive without losing work. Toggle-based configurations are synced to `ui_state.json`, creating a persistent "Memory" between the frontend and the backend bot.
- **The Multi-Library Visualization Strategy**: 
    - **Seaborn**: Used for **High-Fidelity Statistical Proving**. Unlike basic web charts, Seaborn provides professional "Violin Plots" and "KDE Densities" that prove the statistical significance of our anomaly detection layer.
    - **Plotly**: Used for interactive, "Zoomable" time-series market forecasting (XGBoost results).
    - **Altair**: Used for relational heatmaps and "Audit Matrix" grids on the Triage page.
- **Data Signal Fidelity Engine**: A real-time verification layer that scans the dataset for non-zero completeness. It warns the auditor if the "Confidence" of the current run is low due to upstream API throttling.

### 7. Engineering Achievement: 15-Minute to 1-Second Scale
One of the core technical breakthroughs of this project was the **Architectural Re-platforming** of how the AI models retrieve their data.

- **The Traditional Bottleneck (15+ Minutes)**: Initially, the AI script used "Serial Fetching"—looping through each ticker and making individual requests to databases or APIs. This was throttled by network latency and API rate limits (HTTP 429).
- **The Modern Solution (1-Second)**: We moved the "Intelligence" into the **BigQuery/dbt Layer**. By pre-joining the Engine A, B, and C features into a single "Gold" table, the [fraud_model.py](file:///home/kangy/data_analytics/capstone/forensic-intelligence-platform/core_nlp_engine/ml_engine/fraud_model.py) now performs a **single, batched SQL fetch**.
- **The Result**: The AI can now score 10,000 companies as fast as it scores 10, bypassing API rate limits entirely and bringing the retrieval time down from 15 minutes to approximately **1 second**.

---

## 🎓 Summary for Team Briefing
When explaining this to your team, highlight the **Triangulation Principle**: We don't just look at debt; we look at the **Tone** of how that debt is explained. Our platform is the first to bridge the gap between "Messy Text" (NLP) and "Hard Numbers" (Financials) in a single, automated industrial pipeline.
