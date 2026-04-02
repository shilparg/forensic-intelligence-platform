# Forensic Intelligence Platform: Future Roadmap (v2.0 - v4.0)

The Forensic Intelligence Platform is designed as an extensible **Industrial Data Factory**. While the current MVP delivers a full-stack forensic scan, the following phases represent the strategic evolution of the product:

---

## 🚀 Phase 2: Engine Deep-Integration (Performance)
*   **UI-Driven AI Sensitivity**: Connecting the Streamlit "Forensic Sensitivity" slider directly to the `Isolation Forest` contamination parameter. Changing the slider will trigger a targeted Dagster re-scan of the anomaly layer.
*   **Multi-Document NLP Ingestion**: Expanding Engine A to ingest 10-Q (Quarterly), 8-K (Current Events), and Proxy Statements for high-frequency, 360-degree sentiment tracking.
*   **Sector-Contextual Anomaly Detection**: Upgrading the Isolation Forest AI to be "Industry-Aware." Instead of global comparisons, the AI will evaluate a company's Risk Drift relative to its specific industrial peers (e.g., comparing Healthcare Debt to Healthcare Medians).
*   **Cross-Filing Narrative Linkage**: Detecting "Narrative Contradictions" when a CEO changes their story between a voluntary press release and a mandatory SEC filing.

## 📡 Phase 3: Alternative Data & Real-Time Signals
*   **Off-Ledger Intelligence**: Integrating satellite imagery (supply chain activity), ESG scores, and Glassdoor executive sentiment to detect "Cultural Decay" as a precursor to accounting fraud-pressure.
*   **News Streaming Engine**: Transitioning from batch fetches to a real-time GDELT news-monitoring WebSocket to flag anomalies as news breaks mid-day.
*   **Multi-Modal AI (Vision)**: Implementing OCR and Vision Transformers to parse complex financial tables, trend-charts, and mathematical footnotes directly from SEC PDF attachments.

## 🏢 Phase 4: Enterprise-Grade Architecture
*   **Containerized Portability (Docker)**: Wrapping the entire stack—Meltano, Dagster, dbt, and Streamlit—into a multi-container Docker Compose setup for "One-Click" deployment on corporate intranets.
*   **Blockchain-Verified Audit Trail**: Hashing every forensic decision and model score onto a private ledger to ensure an immutable, defensible record of audit independence for regulatory defense.
*   **Human-in-the-loop (HITL) Retraining**: Allowing expert auditors to "Thumb Up/Down" anomaly flags in the dashboard, with these labels feeding back into a supervised learning layer to reduce future false positives.

---
*This roadmap ensures the platform remains at the cutting edge of Forensic Engineering and Data Integrity.*
