# Forensic Intelligence Platform: Use Case & AI Behavior Matrix

This document explains how the current **v3.0 AI Engine** handles different targeting scenarios. Use this as a reference for your technical defense and presentation Q&A.

---

## 🚦 Summary of Current Handling

| Scenario | Handling Logic | AI Behavior | Output Expectation |
| :--- | :--- | :--- | :--- |
| **Single Sector** | Internal Peer Scan | The `StandardScaler` uses the sector-specific mean for all normalization. | High-precision industry-internal triage. |
| **Multi-Sector** | Global Portfolio Scan | Metrics are pooled together into a single global distribution for scaling. | Identifies "Extreme Outliers" regardless of industry. |
| **Small Batch** | Auto-Confidence | The model switches `contamination='auto'` to avoid "forced" flags. | Higher confidence; only extreme outliers are flagged. |
| **Large Batch** | Fixed 10% Audit | The model identifies the top 10% most suspicious patterns as anomalies. | Guaranteed prioritization of the most at-risk entities. |

---

## 🛠️ Technical Defense (The "Math" Behind It)

### 1. How is the data scaled?
The code uses `StandardScaler().fit_transform(X)`. This converts raw values (like $2.5 billion in debt) into a **Z-Score** (e.g., +2.4 standard deviations from the batch mean).
- **In a Single Sector**: This Z-score represents how much a company deviates from its **Peers**.
- **In a Mixed Batch**: This Z-score represents how much a company deviates from the **Market Average**.

### 2. How are anomalies detected?
We use the **Isolation Forest** algorithm. It works by "isolating" observations. Anomalies are easier to isolate (require fewer splits in a decision tree) than normal data points.
- **Current Behavior**: The model builds its trees based on the **Global Distribution** of the current run.

### 3. Future Scaling (v4.0 Roadmap)
While v3.0 is a robust "Global Scouter," the **v4.0 Roadmap** includes **Sector-Contextual Normalization**. In that version, the math will automatically calculate Z-scores relative to the industry median even within a mixed batch. 

---
*This document ensures the auditor knows exactly what the AI is "thinking" when it generates a Risk Score.*
