# Forensic Intelligence Platform: Code Review & Capstone Enhancements

This document provides a comprehensive review of your current pipeline, identifies minor bugs, and proposes brand new analytical features to make your capstone project truly stand out.

---

## 🖥️ Streamlit Dashboard Review (`app.py`)

### Minor Bugs & Hardcoded Paths (Fix Required)
1. **SQL Visualizer Desync**: On Page 4 (`☁️ Cloud SQL Visualizer`), the UI shows hardcoded SQL text explaining how BigQuery works. It uses `` `{os.getenv("GCP_PROJECT_ID")}.forensic_data.raw_filings` `` and `` `...raw_sec_landing.raw_sec_filings` ``. 
   - **The Bug**: We recently agreed to the Medallion architecture where the source table is `raw_sec_landing.raw_filings`. The UI code currently displays incorrect dataset names to the users.
   - **The Fix**: Update lines 263 and 285 in `app.py` to correctly reflect the `raw_sec_landing.raw_filings` silver layer.

### UI & Feature Enhancements
1. **Dynamic Sidebar Filtering**: Currently, the charts show all data at once. You should add a Streamlit multi-select filter in the sidebar (e.g., `st.sidebar.multiselect("Filter by Sector")`) that recalculates the `display_df` globally so the user can drill down into specific industries (like Tech vs. Finance).
2. **Missing Value Handler for Altair**: If a company lacks financial metrics (because the Yahoo API failed before), Altair will silently drop the bubble. We should add an explicit `st.warning()` if `df.isna().sum()` reveals missing variables in the dashboard.

---

## 🗄️ dbt SQL Models Review

Your current dbt models (`fct_disclosure_density`, `fct_narrative_drift`, `fct_anomaly_detection`) are excellent and strongly utilize advanced built-in BigQuery functions like `LAG()` and `STDDEV()`. Your use of `COALESCE()` for NULL handling is also great.

However, to guarantee an "A+" on a Forensic Analytics Capstone, you should introduce more complex accounting patterns. I suggest adding the following three powerful SQL models:

### 1. Benford's Law Fraud Detector (`fct_benfords_law.sql`)
Benford's Law states that in naturally occurring financial statements, the leading digit "1" should appear ~30% of the time, "2" ~17% of the time, etc. Fabricated numbers do not follow this curve.
- **The SQL Concept**: You can use BigQuery Regex `REGEXP_EXTRACT_ALL(filing_text, r'\b([1-9])\d*')` to extract every leading number in the 10-K, count the frequency of each digit, and flag companies that wildly deviate from the 30.1% expected threshold.

### 2. Trailing 3-Year Sentiment Volatility (`fct_sentiment_volatility.sql`)
Instead of just looking at the current year's sentiment, forensic accounting looks for *sudden changes in managerial tone*.
- **The SQL Concept**: Instead of a simple `LAG()`, we use a moving window: `STDDEV_SAMP(sentiment_score) OVER (PARTITION BY ticker ORDER BY fiscal_year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`. If the standard deviation spikes, it means the CEO's tone drastically changed, signaling internal panic.

### 3. Sector-Pegged Peer Benchmarking (`int_peer_benchmarking.sql`)
Comparing Apple to Ford is mathematically flawed. Financials must be compared against their direct peers.
- **The SQL Concept**: Calculate an industry average dynamically: `AVG(debt_to_equity) OVER (PARTITION BY sector, fiscal_year)`. Then, calculate how far the company deviates from its *own sector* using `(debt_to_equity - sector_avg) / sector_stddev`.

---

> [!IMPORTANT]
> **Next Steps:**
> Review the suggestions above! Would you like me to first fix the minor UI bugs in the Streamlit dashboard, or should I go ahead and write the advanced Benford's Law and Volatility SQL models for your dbt project?
