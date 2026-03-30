# 🛠️ Forensic Intelligence Platform: Installation & Setup Manual

Follow this guide to successfully deploy and run the Forensic Intelligence Platform. This manual ensures the industrial pipeline (Dagster), the cloud data warehouse (BigQuery), and the frontend (Streamlit) are correctly synchronized.

---

## 🏗️ 1. Prerequisites
Before beginning, ensure you have the following accounts and tools:
- **Python**: Version 3.8 or higher.
- **Google Cloud Platform (GCP)**: A project with **BigQuery API** enabled.
- **MongoDB Atlas**: A cluster with a database named `forensic_accounting`.
- **Google Gemini API Key**: For generating forensic memos.
- **Meltano**: For structured financial data synchronization.

---

## 🐍 2. Local Environment Setup

1. **Clone the Repository**:
   ```bash
   git clone [repository_url]
   cd forensic-intelligence-platform
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## ☁️ 3. Cloud & Database Configuration

### A. Google Cloud (BigQuery)
1. **Service Account**: Create a Service Account in GCP with `BigQuery Admin` permissions.
2. **Key File**: Download the Service Account JSON key. Save it as `gcp-service-account.json` in the project root.
   > [!IMPORTANT]
   > Never commit this file to version control (Git).

### B. Environment Variables (.env)
Create a file named `.env` in the project root and populate it with your specific credentials:
```env
GCP_PROJECT_ID=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=gcp-service-account.json
MONGO_URI=your-mongodb-atlas-connection-string
GEMINI_API_KEY=your-gemini-api-key
SEC_USER_AGENT=ForensicBot (your-email@example.com)
```

---

## 🚀 4. Executing the Platform

The platform is designed to be run in two main parts: The **Data Factory** (Backend) and the **Command Center** (Frontend).

### Part A: The Data Factory (Pipeline Orchestration)
> [!IMPORTANT]
> You **MUST** run this command from the project root: `~/data_analytic/capstone/forensic-intelligence-platform`

1. Open a terminal and run:
   ```bash
   cd ~/data_analytic/capstone/forensic-intelligence-platform
   export DAGSTER_HOME=~/.dagster
   dagster dev -f core_nlp_engine/orchestrate/assets.py
   ```
2. Navigate to `http://localhost:3000` to monitor the pipeline.
3. Trigger the `forensic_audit_job`.

### Part B: The Command Center (Streamlit Dashboard)
> [!IMPORTANT]
> You **MUST** run this command from the project root: `~/data_analytic/capstone/forensic-intelligence-platform`

1. Open a second terminal and run:
   ```bash
   cd ~/data_analytic/capstone/forensic-intelligence-platform
   streamlit run streamlit_dashboard/app.py
   ```
2. Navigate to `http://localhost:8501`.

---

## 🛡️ 5. Troubleshooting & Engineering Notes

### SSL Handshake Errors
If your pipeline fails during the Meltano sync due to SSL certificate errors, the platform includes a custom patch. We use `certifi` and `dnspython` in the **Migration Bot** to bypass localized handshake restrictions common in enterprise environments.

### API Rate Limiting (Yahoo Finance)
If you see a "Signal Fidelity" warning in the UI, it means you have exceeded the Yahoo Finance rate limits.
- **Fix**: Wait 2 hours before re-triggering the pipeline, or reduce the number of tickers in your `target_tickers.csv`.

### dbt Profile Sync
Ensure your `profiles.yml` (located in `core_nlp_engine/transform_dbt/`) matches your GCP project ID. The pipeline automatically injects the project ID from your `.env` during execution.

---
