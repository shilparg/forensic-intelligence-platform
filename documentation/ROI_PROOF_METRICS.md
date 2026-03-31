# 📉 ROI Evidence: The 400-Hour Calculation

This document provides the mathematical proof behind the "400 Human-Hours Saved" claim on Slide 9 of the Capstone Presentation. Use this as your defensive evidence during the Q&A session.

---

## 🕒 The "Manual Audit" Baseline
*   **The Task**: An auditor manually reads a 100-page SEC 10-K filing (~25,000 words), highlights MD&A sections, and cross-references financial ratios with Yahoo Finance.
*   **Time per Filing**: At a professional pace, a "first-pass" forensic review takes approximately **25 minutes**.
*   **Batch Total**: 1,000 filings × 25 minutes = 25,000 minutes = **~416 Human Hours**.

---

## ⚡ The "Forensic Platform" Reality
*   **The Task**: The AI scans, scripts, and mathematically scores 1,000 filings in a single batch.
*   **Processing Time**: As documented in the **15-Minute to 1-Second Scale** achievement, the BigQuery/dbt architecture handles the data fetch and join in **~1 second**.
*   **The "Human-in-the-Loop" Phase**: The auditor no longer reads every filing. They only review the **Top 5%** (those flagged as "CRITICAL ANOMALIES" by the Isolation Forest).
*   **Human Review Time**: 50 companies × 20-minute deep-dives = 1,000 minutes = **~16.6 Human Hours**.

---

## 📊 The Final Proof (The Delta)

| Metric | Manual Auditor | Forensic AI Platform |
| :--- | :--- | :--- |
| **Search & Triage** | 25,000 Minutes (Full Portfolio) | ~1 Second (Automated Scalability) |
| **Deep-Dive Review** | 0 Minutes (Exhausted) | 1,000 Minutes (Focused on Top 5% Risk) |
| **Total Human Effort** | **416 Hours** | **16.6 Hours** |
| **Labor Efficiency** | **Baseline** | **+96% Faster** |

---

## 🎤 Presentation Pitch Script
"Our platform doesn't replace the auditor—it replaces the **searching**. By automating 400 hours of manual reading for every 1,000 filings, we give the auditor 400 hours of extra time to actually **investigate** the smoking guns we find. We are increasing audit 'Depth' while decreasing 'Drudgery'."
