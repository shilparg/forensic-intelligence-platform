Here is the complete, end-to-end breakdown of how both of your engines flow through your Medallion architecture:

### 🥉 The Bronze Layer (Raw Ingestion & NoSQL Storage)
*The wild west. Data lands here exactly as it was extracted, with no rigid schemas enforced.*

- **Engine A (Python NLP Scraper):** Connects to the SEC EDGAR database, pulls raw HTML 10-K filings, strips the text, and calculates initial FinBERT sentiment scores. Because text is messy and dynamic, it dumps this straight into a schemaless **MongoDB Atlas collection called `sec_filings`**.
- **Engine B (Meltano):** Your ELT engine connects to Yahoo Finance APIs, pulling completely different, highly structured numerical data (short ratios, debt-to-equity, institutional holdings). It dumps this raw JSON into **a separate MongoDB Atlas collection called `yahoo_finance`**.

> [!NOTE] 
> Even though both engines land their data in the same Bronze MongoDB database, they are strictly isolated into separate collections so a failure in one engine doesn't corrupt the other.

---

### 🥈 The Silver Layer (Structured Cloud Staging)
*The cleaning layer. Data is moved into the cloud data warehouse and forced into strict rows and columns, but it is not joined together yet.*

- **Engine A's Path:** A sync job (likely Dagster/Meltano) extracts the `sec_filings` collection from MongoDB and loads it into your BigQuery `raw_sec_landing` dataset to create the **`raw_filings`** table.
- **Engine B's Path:** A parallel sync job extracts the `yahoo_finance` collection from MongoDB and loads it into the very same BigQuery dataset to create the **`raw_financials`** table.

> [!TIP]
> At the Silver layer, Engine A and Engine B now live in the exact same relational dataset (`raw_sec_landing`), but they remain completely separate tables. 

---

### 🥇 The Gold Layer (Unified Machine Learning & Analytics)
*The business logic layer. Data is joined, aggregated, and optimized for consumption.*

- **The dbt Transformation:** Your dbt staging models (`stg_sec_filings.sql` and `stg_financials.sql`) query those two separate Silver tables and cast their columns into strict, clean data types. 
- **The Great Convergence:** Inside a dbt mart model (like `int_forensic_metrics`), dbt executes a massive BigQuery `LEFT JOIN`—matching Engine A's data and Engine B's data together using the company `ticker` and `fiscal_year`.
- **The Final Destination:** The result of this join is written into your final **`forensic_data`** Gold dataset.

> [!IMPORTANT]
> This single, unified Gold table is the ultimate product of your pipeline! Your **Streamlit Dashboard** and your **Isolation Forest AI Model** only ever connect to this one final Gold table—they never have to talk to MongoDB or Yahoo Finance APIs directly!