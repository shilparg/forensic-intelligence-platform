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

---

## 🍳 4. The "Forensic Kitchen" Analogies (Simple Explanation)

Use these analogies when explaining the AI's behavior to non-technical stakeholders (e.g., HR or Business Directors) during your presentation.

### 🍱 A. Small Batch vs. Large Batch (The "Security" Analogy)

*   **Small Batch (The "VIP Party")**:
    *   *AI Logic:* 
    *   *Analogy:* Imagine a security guard at a small VIP dinner with 5 guests. If everyone is behaving well, the guard doesn't "force" an arrest just to meet a quota. They only step in if someone starts "throwing plates" (an extreme outlier).
    *   *Result:* Only **extreme** anomalies are flagged. If the group is healthy, you get **0 flags**.

*   **Large Batch (The "Airport Security")**:
    *   *AI Logic:* 
    *   *Analogy:* Imagine a busy airport security line with 1,000 people. The rule is: "Always pull aside the **10% most suspicious-looking people** for a bag check." Even if they aren't criminals, they are the **highest risk** in that specific crowd.
    *   *Result:* You always get a **Top 10%** priority list of who to audit first.

### 🍰 B. Single Sector vs. Multi-Sector (The "Contest" Analogy)

*   **Single Sector (The "Baking Contest")**:
    *   *Analogy:* You are a judge at a **Baking Contest**. You are only tasting cakes. If one cake is "salty," it sticks out immediately because every other cake is sweet.
    *   *Result:* Finds the **"Black Sheep"** that is cheating compared to its industry peers.

*   **Multi-Sector (The "Food Festival")**:
    *   *Analogy:* You are at a **Global Food Festival**. You are tasting cakes, pizzas, and steaks all at once. You aren't looking for "sweetness"; you are looking for **"spoilage."** You want to find the one dish that is bad/rotten, regardless of whether it’s supposed to be sweet or savory.
    *   *Result:* Finds **"Global Outliers"** that look suspicious across the entire market (e.g., manufactured numbers or extreme executive fear).

---

## 📊 5. The "Forensic Pulse" (The 10 Monitoring Parameters)

To decide if a company is "Aged Meat" or a "Fresh Ingredient," the AI measures these 10 markers simultaneously:

1.  **Benford’s Deviation**: Do the digits in the data look "hand-typed" rather than natural? (Catches manufactured accounting).
2.  **Sentiment Score**: Does the CEO’s tone hide "fear" or "obfuscation"?
3.  **Sentiment Volatility**: Has the tone changed drastically in the last 3 years? (Sudden narrative shifts).
4.  **Density Index**: Is the report 500 pages long just to hide a small error? (Measuring "Verbiage Bloat").
5.  **Debt-to-Equity**: Is the company drowning in debt compared to the group?
6.  **Operating Margin**: Is the business actually making a profit, or is it a "paper tiger"?
7.  **Short Ratio**: Is Wall Street "betting a lot" that this company will fail?
8.  **Insider Ownership**: Are the bosses dumping their own shares? (Mass executive exits).
9.  **Current Ratio**: Can they actually pay their bills this month?
10. **Return on Equity**: Are they using shareholder money efficiently?

---

## 🧐 6. Deep-Dive: The Small Batch Decision (Peer Comparison)

When you audit **10 or fewer** companies, the AI doesn't have a "pre-set" definition of evil. It compares the 10 against each other.

### Scenario A: The "Honest Group" (0 Anomalies)
*   **The Data:** All 10 companies have "Normal" levels for all 10 parameters (e.g., Debt < 30%, Positive tone, Natural numbers).
*   **AI Interpretation:** *"This entire group looks healthy and similar. No one is a sore thumb."*
*   **Result:** **0 flags**. The AI is smart enough to stay quiet when everyone is behaving.

### Scenario B: The "Black Sheep" (1 Anomaly)
*   **The Data:** 9 companies look like Scenario A, but **Company #10** has 500% Debt and a "Naturalness Score" of zero.
*   **AI Interpretation:** *"Company #10 is completely 'isolated' from the others—it doesn't belong."*
*   **Result:** **1 CRITICAL ANOMALY**. The AI only "shouts" when a company stands out like a sore thumb in its specific peer group.

---

## 🛫 7. Deep-Dive: The Large Batch Decision (The 10% Quota)

When you audit **more than 10** companies, the AI switches from "Auto-Confidence" to a **Mandatory Priority Audit**.

### The Logic: "Prioritized Bag Check"
*   **The Data:** You are auditing 1,000 companies. Most are "okay," but 200 of them have some minor debt or sentiment issues.
*   **AI Interpretation:** *"I cannot tell the auditor to check all 1,000. I must find the 100 (10%) that are the objectively most suspicious in this entire crowd."*
*   **Goal:** To ensure the auditor has a **guaranteed daily to-do list** of the highest risks.
*   **Result:** **100 CRITICAL ANOMALIES**. Even if they aren't "criminals," they are the 10% most likely to be hiding something based on the 10 Forensic Pulse markers.

---

## 🌍 8. Deep-Dive: Multi-Sector (The Global Scouter)

When you audit companies from **different industries** at the same time (e.g., a Bank vs. a Tech Company), the AI acts as a "Universal Truth" detector.

### The Problem: "Apples vs. Oranges"
*   **Sector Reality:** A **Railroad** company naturally has massive debt (for trains). A **Software** company naturally has almost zero debt.
*   **The Risk:** If the AI is too simple, it might flag every Railroad company just for having debt.

### The Multi-Sector Solution: "The Universal Pulse"
*   **Global Scouter Logic:** The AI looks for patterns that are **suspicious in any industry**. 
    *   *Example:* **Manufactured Numbers (Benford's Law)** or **Executive Fear (Sentiment)** are red flags whether you sell software or locomotives.
*   **Result:** The AI identifies "Extreme Outliers" that look weird when compared to the **Global Market Average**. It finds the "vulnerability" that transcends industry boundaries.
