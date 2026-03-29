I'll break down exactly how your Streamlit frontend orchestrates those two input options, and how that choice cascades through the pipeline and reflects on your different dashboard pages!

### 1. The Entry Point: "⚙️ Orchestration Control" Page
This is the only page where the input decision is made. Under the "Target Selection" section, you have a Streamlit radio button `input_method` with two options:

*   **Option A: "Default Tech Benchmark (FAANG)"**
    *   **Behind the Scenes:** The UI sets the pipeline `mode` to `"peer_group"`. It bypasses file uploading entirely and sends a strict payload to the Dagster backend instructing it to use the hardcoded baseline tickers (`AAPL`, `MSFT`, `NVDA`, `GOOGL`).
    *   *Sector Tagging:* The backend automatically tags all of these as `"Information Technology"` for industry indexing.
*   **Option B: "Upload Custom CSV Watchlist"**
    *   **Behind the Scenes:** The UI opens a Streamlit `st.file_uploader` widget. When you drop a file in, it physically saves it to your root directory as `target_tickers.csv`. 
    *   It then actively uses Pandas to verify the file has a `ticker` column. If it succeeds, it sets `mode = "custom"` and sends the parsed list of tickers down into the orchestration payload.
    *   *Sector Tagging:* During the Dagster run, if your custom CSV has an optional `sector` column (e.g. Healthcare, Finance), the ML engine will ingest it! If not, it safely falls back to a default value so the pipeline never crashes.

### 2. How the Pages React to the Input Choice
Because your platform uses a clean **decoupled Medallion Architecture**, the frontend visualization pages (`📊 Executive Summary`, `🕵️ Forensic Deep-Dive`, `🔮 Predictive Forecasting`, etc.) actually **do not care** which input option you picked! 

Here is exactly what happens:
1. Regardless of whether you chose FAANG or uploaded a custom CSV, the background Dagster pipeline generates the exact same final output artifact: `ai_scored_forensic_dataset.csv`.
2. When the pipeline finishes, the Streamlit app simply hard-reloads (`st.cache_data.clear()`).
3. **Every single analytical page** blindly ingests that new `ai_scored_forensic_dataset.csv` and dynamically resizes all charts, arrays, and matrices to fit the new targets.

### 3. The Only UI Difference: The "Global Filters" Sidebar
There is *one* explicit UI feature that reacts dramatically based on whether you used the Default Benchmark vs. a Custom CSV: **The 🔍 Global Filters in the Sidebar.**

If you run the "Default Tech Benchmark", the "Filter by Sector" dropdown will identically lock onto `Information Technology`. However, if you load a massive custom CSV covering multiple industries (like Banking, Real Estate, and Tech) and include a `sector` column, that Streamlit sidebar dropdown will dynamically explode with all your custom sectors! This allows you to globally filter the density matrices, violin plots, and predictive radars by specific industries entirely on the fly. 

It's a beautifully modular design—the input orchestrator and the visualization frontend are entirely physically separated layers connected only by the cleaned data warehouse!