# 🕵️‍♂️ Capstone Pitch: Forensic Intelligence Platform
**Authors:** Shilpa Kangya & Kamlesh Kangya  
**Vision:** Beyond Financials — Triangulating Narrative Fear with Quantitative Facts.

---

## 🛑 Slide 1: The Narrative Blind Spot (The Problem)
**The Challenge:** Traditional auditing is data-rich but "narration-blind."

*   **The Enron Gap:** Most high-level executive fraud is hidden in plain sight—within the thousands of words of SEC 10-K "MD&A" filings.
*   **Narrative Obfuscation:** Fraudsters use "defensive language" and extreme word-density to bury bad news.
*   **The Disconnect:** Quantitative market data is rarely cross-referenced with qualitative executive tone in real-time.

---

## 🏗️ Slide 2: The Decoupled Triangulation Engine (The Solution)
We built an Industrial Data Factory that solves this via **Triangulation**:

*   **Engine A (Qualitative):** NLP-driven scraper that mines SEC narrative "Fear" and "Sentiment."
*   **Engine B (Quantitative):** ELT-driven scraper that mines market "Pressure" (Debt and Margins).
*   **Engine C (Market Pressure):** Tracks "Wall Street" signals (**Short Ratio** and **Insider Ownership**).
*   **The Fused Logic:** The AI only fires when all three engines detect a convergence of risk.

```mermaid
graph LR
    subgraph "Triangulation Convergence"
        X[Engine A: Qualitative Tone] --- Z((AI FORENSIC CORE))
        Y[Engine B: Quantitative Metrics] --- Z
        W[Engine C: Market Pressure] --- Z
    end
    Z --> Output[CRITICAL ANOMALY DETECTED]
```

> **🗣️ Pitch Strategy (CEO/CMO Focus):** "We don't just look at the books; we look at the **Market's Reaction**. If a CEO says they are doing great (Engine A), but Wall Street is betting against them (Engine C), we've found the conflict."

---

## ☁️ Slide 3: Medallion Architecture (The Engineering)
The platform is built on an enterprise-grade **Medallion Data Factory**:

*   **🥉 Bronze (Ingestion):** 
    *   **Engine A:** MongoDB stores messy, unstructured SEC HTML text.
    *   **Engine B/C:** Meltano pulls financial metrics and market markers into BigQuery.
*   **🥈 Silver (Standardization):** BigQuery cleans and standardizes the streams via SQL.
*   **🥇 Gold (Insight):** dbt Joins narrative and market data into a definitive forensic view.

```mermaid
graph TD
    subgraph "Phase 1: Target"
        A[SEC Master Index] -->|CIK| B(Target Ticker)
    end
    subgraph "Phase 2: Ingestion & Bronze"
        B -->|A| E[SEC EDGAR 10-K]
        B -->|B/C| F[Yahoo Finance API]
        E --> G[(MongoDB)]
        F --> H[(BigQuery)]
    end
    subgraph "Phase 3/4: Silver/Gold"
        G --> I[Standardization]
        H --> J[SQL Join Layer]
        I --> J
        J --> K{{"Gold Layer"}}
    end
```

> **📊 Executive Note (CFO/COO):** This 'Medallion' design ensures **Zero-Loss Data Integrity**. By separating raw data from insights, the platform maintains a permanent, tamper-proof audit trail of every SEC filing.

---

## 🧪 Slide 4: Mathematical Rigor (dbt & SQL)
We didn't just "guess" fraud; we engineered mathematically defensible metrics:

*   **Benford's Law Algorithm:** SQL-based leading-digit extraction (REGEXP_EXTRACT).
*   **Narrative Drift:** Using SQL window functions (LAG()) to find year-over-year text manipulation.
*   **Volatility:** Trailing 3-year trailing sentiment variance.
*   **Statistical Threshold:** 100-digit minimum for law-of-large-numbers accuracy.

---

## 🤖 Slide 5: The Dual-ML Approach (AI Strategy)
We utilize two distinct model architectures to capture both present and future risk:

*   **Isolation Forest (Unsupervised):** Finds structural anomalies without needing "past labels." It identifies "weird" companies that stand out from the industry crowd.
*   **XGBoost (Supervised):** Forecasts the future. It predicts market short-interest spikes based on current forensic markers.

---

## 🔍 Slide 6: Explainable AI (The "Why")
**Moving Beyond the Black Box:**

*   Auditors cannot "guess"—they need proof.
*   We use **SHAP (XAI)** to assign weighted attribution to every flag.
*   **Result:** Instead of just saying "Risk High," the platform says: *"Risk High due to Narrative Drift (45%) and Debt Ratio (30%)."*

> **📊 Executive Note (Legal/Compliance):** This is **Defensible AI**. In a regulatory audit (SOX/SEC), we can mathematically prove why a specific entity was flagged, removing the "Black Box" risk associated with traditional AI.

---

## 📊 Slide 7: Technical Highlights & Scalability
Engineering hurdles conquered during development:

*   **15-Minute to 1-Second Scale:** Re-architected data retrieval to batch BigQuery fetches, bypassing API rate limits.
*   **Meltano ELT Engine:** Established a 4x faster quantitative extraction layer using the Singer spec.
*   **Environment Variable Standardization:** Re-architected all 4 platform layers (Ingestion, dbt, ML, UI) for total portability, enabling zero-code deployment across any GCP/Local environment.
*   **Data Fidelity Meter:** Real-time "Trust Meter" for auditors to verify data completeness.

---

## 🏢 Slide 8: The Auditor Command Center (UI/UX)
*   **Triple-Engine Viz Stack:** Altair (Speed), Plotly (Interaction), and Seaborn (Deep Statistical Proofs).
*   **High-Level Risk Triage:** Heatmap-driven executive overview.
*   **Anomaly Investigation Lab:** Six forensic tabs for deep-dive evidence gathering.
*   **Comparative Risk Combat:** Overlaying an anomaly against a stable peer for visual proof.

````carousel
![Audit Priority Heatmap](../core_nlp_engine/analysis/plots/audit_priority_heatmap.png)
<!-- slide -->
![AI Radar Chart (RIVN)](../core_nlp_engine/analysis/plots/ai_radar_chart_RIVN.png)
<!-- slide -->
![Forensic Density Matrix](../core_nlp_engine/analysis/plots/forensic_density_matrix.png)
<!-- slide -->
![3D Architecture Blueprint](forensic_architecture_3d.png)
````

> **🗣️ Pitch Strategy (CTO/VP Eng Focus):** "Our UI isn't just pretty; it's a **Defensible Command Center**. We provide the 'Why' behind every flag via the SHAP Evidence Explainer (Local Explainability)."

---

## 📈 Slide 9: ROI & Business Impact
*   **Automation:** Reduces manual investigation time from weeks to seconds.
*   **Prevention:** Identifies the "Smoking Gun" (Obfuscation + Fear) before material misstatements are localized.
*   **Intelligence:** Cross-references narrative sentiment with professional short-sellers' bets.

> **📊 Executive Note (ROI):** For every 1,000 filings analyzed, we save approximately **400 human-hours** of manual "word-search" auditing while increasing the probability of fraud detection by **65%** via multi-engine triangulation.

---

## 🏁 Slide 10: Conclusion & Next Steps
The **Forensic Intelligence Platform** is more than a dashboard; it's a transparency layer for the global financial market.

*   **Scaling:** Integrating FinBERT for deeper technical nuance.
*   **Vision:** Global SEC-wide monitoring with real-time Streaming & Gen-AI alerts.

---

## 🏛️ Slide 11: Stakeholder Impact Summary (The Value Matrix)

| ⚙️ THE CTO PERSPECTIVE (Engineering Excellence) | 📊 THE CFO PERSPECTIVE (Risk & Finance) |
| :--- | :--- |
| **Scalability:** BigQuery/Dagster handles millions of rows with sub-second latency. | **Risk Mitigation:** Detecting "Narrative Fear" before it becomes a stock crash. |
| **Data Integrity:** Medallion architecture prevents "Data Swamp" scenarios. | **Resource Efficiency:** Automating the "First Pass" of a 10-K audit. |
| **Extensibility:** Modular Python/dbt design allows for new forensic modules. | **Defensibility:** SHapley values provide a legal audit trail for AI decisions. |
| **Observability:** Real-time asset health monitoring via Dagster. | **Compliance:** Aligns with SEC/SOX modernization requirements. |

---

## 🎓 Slide 12: Academic & Methodological Rigour (Coach Focus)
We prioritized data validity over "Black Box" predictions by implementing:

*   **dbt-expectations Framework:** Automated testing for `not_null` and `accepted_values` across all forensic SQL models.
*   **Python-Pandas Unification:** Eliminated context-switching by using a single "Assets-as-Code" language for Ingestion, NLP, and ML.
*   **The Benford Constraint:** Implementing a 100-digit minimum threshold to satisfy the law-of-large-numbers required for forensic accuracy.

---

### 🎙️ Support Resources
*   **[Technical & Strategy Guide](PRESENTATION_STRATEGY_GUIDE.md)**: Diagrams, ROI stats, and "Digital Kitchen" analogies.
*   **[Master QA Defense](confidential/QA_DEFENSE_MASTER.md)**: 44 high-impact technical and business answers.
