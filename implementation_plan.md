# Ultimate Capstone Roadmap: Medallion Architecture & Advanced Forensics

This is the definitive, step-by-step master plan. It combines the structural transition to a pure Medallion ELT pipeline with the implementation of three academically rigorous forensic accounting ML metrics, culminating in a pristine Dashboard visualization.

## User Review Required

> [!IMPORTANT]
> **To proceed with Phase 1, I need to know:** Is your Meltano ingestion pipeline currently capable of fetching Yahoo Finance data efficiently, or do we need to start by writing a Python ingestion script for Engine B first?

---

## 🛠️ Phase 1: Engine B Ingestion (Bronze & Silver)
**Goal:** Extract Yahoo Finance data away from the local ML Python script and push it directly into the Cloud.

1. **[NEW] `meltano_elt_engine/yahoo_to_bq.py`**
   - We will write a lightweight script or configure Meltano to officially extract `short_ratio`, `debt_to_equity`, and other metrics for the target companies and dump them into BigQuery at `raw_sec_landing.raw_financials`.

---

## 🏗️ Phase 2: dbt Transformation & Advanced Analytics (Gold)
**Goal:** Securely clean Engine B data, build mathematically complex AI features, and join everything into one massive Gold table.

1. **[NEW] `stg_financials.sql`**
   - Reads directly from `{{ source('sec_sources', 'raw_financials') }}`, casting all ratios to standard floats to permanently prevent metric mismatch.

2. **[NEW] `fct_benfords_law.sql`**
   - Applies BigQuery `UNNEST(REGEXP_EXTRACT_ALL())` to parse the millions of characters in `filing_text`, counts leading integer distributions, and algorithmically compares them to the `LOG10(1 + 1/Digit)` Benford curve to flag purely fabricated financial statements.

3. **[NEW] `fct_sentiment_volatility.sql`**
   - Replaces static logic with a 3-Year Trailing Window (`STDDEV_SAMP(...) OVER (PARTITION BY ticker ORDER BY fiscal_year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`). Sudden managerial panic or drastic shifts in tone are flagged immediately.

4. **[NEW] `int_peer_benchmarking.sql`**
   - Groups companies by their macroeconomic sector (e.g., tech vs healthcare) explicitly using BigQuery Window averages to make sure financial metrics are scored appropriately.

5. **[MODIFY] `int_forensic_metrics.sql` (The Hub)**
   - Executes a unified `LEFT JOIN` on `ticker` combining Engine A (Text Context), Engine B (Market Metrics), Benford Deviations, and Volatility Scores into a single masterpiece column-set.

---

## 🧠 Phase 3: Machine Learning Refactor
**Goal:** Dramatically speed up ML execution and remove the slow internet dependency.

1. **[MODIFY] `core_nlp_engine/ml_engine/fraud_model.py`**
   - Completely delete the `yfinance` rate-limited `for` loop.
   - Adjust the primary BigQuery `SELECT` query to ingest the brand new `forensic_data.int_forensic_metrics` Gold table.
   - Feed the new features (Benford, Volatility, Benchmark) into the Isolation Forest AI to significantly boost its predictive fraud accuracy.
   - Export the unified `ai_scored_forensic_dataset.csv` for Streamlit.

---

## 📊 Phase 4: Streamlit Dashboard Enhancements
**Goal:** Add dynamic control and beautifully visualize the new Capstone metrics.

1. **[MODIFY] `streamlit_dashboard/app.py` UI Filtering**
   - Add dynamic `st.sidebar.multiselect()` tools allowing users to filter the entire presentation down by specific Sectors, Risk Tiers, or Years.

2. **[MODIFY] `streamlit_dashboard/app.py` Benford Visualizer**
   - In the "**🕵️ Forensic Deep-Dive**" tab, introduce a brand new Benford's Law interactive line chart that explicitly visualizes the AI’s capability to detect mathematically manipulated 10-K text.
