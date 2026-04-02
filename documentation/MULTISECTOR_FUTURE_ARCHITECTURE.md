# Future Architecture: Multi-Sector Scalability (v4.0)

This document serves as the high-level design specification for extending the Forensic Intelligence Platform to support full industrial partitioning and sector-relative AI analysis.

---

## 1. 🏗️ Orchestration & Data Factory (Dagster)
The pipeline will transition from a monolithic batch process to a **GCP-Scale Partitioned Factory**.

### Key Components:
- **Dynamic Partitioning**: Move from a single "Target Group" to **Partitioned Assets**. Each Sector (e.g., *Energy*, *Healthcare*) will be a unique partition in Dagster.
    - *Benefit*: You can run, re-run, or schedule updates for one industry without affecting another.
- **Micro-Batching**: Instead of extracting all tickers together, Dagster will orchestrate parallel micro-batches to avoid Yahoo/SEC rate limits.
- **Sector-Specific Schedules**: "Volatile" sectors (e.g., Tech) can be scheduled for daily extraction, while "Stable" sectors (e.g., Utilities) can run on a slower weekly cadence.

## 2. 🧠 AI & Machine Learning: Contextual Models
The AI will evolve from "Global" to **"Peer-Aware"**.

### Logic Layer:
- **Z-Score Normalization (Sector-Relative)**: 
    - The AI will calculate the standard deviation for every feature (Debt, Margin, Sentiment) **within its specific industry**. 
    - a "High Debt" flag will only trigger if a company's debt is suspicious compared to other companies in the *same* sector.
- **Specialized Industry Experts**:
    - We will implement **Sub-Models** (e.g., `fraud_model_real_estate.py`, `fraud_model_software.py`). 
    - Different industries use different mathematical bookkeeping standards; specialized models will detect "Mathematical Fingerprints" unique to each.
- **Narrative Benchmarking**: Comparing the CEO's sentiment against the industry average to identify outlier "Panic" or "Obfuscation" in tone.

## 3. 📊 Dashboard Strategy: Sector-Hub UI/UX
The Streamlit interface will become a **Market Intelligence Command Center**.

### Interface Features:
- **Sector Landing Page**: A high-level entry point where users can select a "Watchlist" by industry.
- **Peer-Group Radar (Overlay)**: When analyzing `AAPL`, the UI will automatically overlay `MSFT` and `GOOGL` as "Stable Benchmarks" for a 3-way radar comparison.
- **Sector-Relative Sparklines**: Instead of raw numbers, the "Master Data Matrix" will show "Relative Ranks" within the industry.
- **Volatility Heatmaps**: Identifying which industries are currently experiencing the most "Anomaly Density" across the entire S&P 500.

## 📡 4. Notification Layer: Smart Forensic Alerts
Email alerts will become **Contextual Investigative Memos**.

### Enhancement:
- **Audit Routing**: Alerts for *Financial* tickers can be routed to the Finance-Audit team, while *Healthcare* alerts go elsewhere.
- **Multi-Level Thresholds**: Allow users to set lower "Sensitivity Thresholds" for high-fraud-risk sectors.
- **Comparative Evidence**: Email alerts will explicitly mention the sector context:
    - *EX:* "Entity $X$ is showing a **3.5x Deviation** in Narrative Volatility compared to the **Energy Sector Median**."

---
*This architecture ensures that the Forensic Intelligence Platform scales from a 10-company benchmark to a full-market, enterprise-grade forensic tool.*
