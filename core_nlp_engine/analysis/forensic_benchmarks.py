import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- 1. Bulletproof Pathing ---
# Calculate the exact directories based on where this script is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))         # /core_nlp_engine/analysis
ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))    # /core_nlp_engine

# Explicitly target the ml_engine folder for input and the local plots folder for output
DATA_PATH = os.path.join(ENGINE_DIR, "ml_engine", "ai_scored_forensic_dataset.csv")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "plots")

def run_benchmark_plots():
    # 2. Safety Check before loading
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"🚨 Could not find ML output at: {DATA_PATH}\nEnsure fraud_model.py ran successfully first.")

    df = pd.read_csv(DATA_PATH)
    sns.set_theme(style="white")
    
    # Create the plots directory if it doesn't exist yet
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- PLOT 1: Industry Sentiment Boxplot ---
    # Highlights the outliers (Z-Score anomalies)
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='ticker', y='sentiment_score', palette="Set3")
    plt.title("Industry Sentiment Distribution: Identifying Outliers", fontsize=14)
    
    # Save using the absolute output directory
    plt.savefig(os.path.join(OUTPUT_DIR, "industry_sentiment_boxplot.png"))
    print(f"✅ Saved Industry Boxplot to {OUTPUT_DIR}")

    # --- PLOT 2: Forensic Correlation Heatmap ---
    # Shows if Negative Sentiment correlates with High Debt or Short Interest
    plt.figure(figsize=(10, 8))
    
    # Dynamically select columns that actually exist in the CSV
    desired_cols = ['sentiment_score', 'risk_score', 'short_ratio', 'debt_to_equity', 'word_count', 'similarity_index']
    corr_cols = [col for col in desired_cols if col in df.columns]
    
    corr_matrix = df[corr_cols].corr(numeric_only=True) # Added numeric_only to prevent string errors

    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Forensic Triangulation: SEC Metrics vs. Market Pressure", fontsize=14)
    
    # Save using the absolute output directory
    plt.savefig(os.path.join(OUTPUT_DIR, "forensic_correlation_heatmap.png"))
    print(f"✅ Saved Correlation Heatmap to {OUTPUT_DIR}")

if __name__ == "__main__":
    run_benchmark_plots()