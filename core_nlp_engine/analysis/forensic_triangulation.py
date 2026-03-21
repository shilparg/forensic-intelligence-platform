import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- 1. Bulletproof Pathing ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))         
ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))    
DATA_PATH = os.path.join(ENGINE_DIR, "ml_engine", "ai_scored_forensic_dataset.csv")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "plots")

def run_triangulation_plots():
    # 2. Safety Check
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"🚨 Could not find ML output at: {DATA_PATH}\nEnsure fraud_model.py ran successfully first.")

    df = pd.read_csv(DATA_PATH)
    sns.set_theme(style="darkgrid")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- PLOT 1: The "Smoking Gun" Regression ---
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='sentiment_score', y='short_ratio', 
                scatter_kws={'s':100, 'alpha':0.5}, line_kws={'color':'red'})
    
    for i in range(len(df)):
        if df.iloc[i]['fraud_risk_status'] == 'CRITICAL ANOMALY':
            plt.text(df.iloc[i]['sentiment_score'], df.iloc[i]['short_ratio'], 
                     df.iloc[i]['ticker'], color='black', weight='bold')
                     
    plt.title("Source 1 vs Source 2: Sentiment vs. Market Short Interest", fontsize=14)
    plt.savefig(os.path.join(OUTPUT_DIR, "forensic_regression_analysis.png"))
    print("✅ Saved Regression Analysis.")

    # --- PLOT 2: Audit Priority Matrix ---
    plt.figure(figsize=(12, 4))
    target_metric = 'risk_score' if 'risk_score' in df.columns else 'sentiment_score'
    pivot_df = df.pivot_table(index='ticker', columns='fiscal_year', values=target_metric)

    sns.heatmap(pivot_df, annot=True, cmap="YlOrRd", cbar_kws={'label': 'Weighted Risk Score'})
    plt.title("Executive Audit Priority: Heatmap of Weighted Risk Scores", fontsize=14)
    plt.savefig(os.path.join(OUTPUT_DIR, "audit_priority_heatmap.png"))
    print("✅ Saved Audit Priority Heatmap.")

if __name__ == "__main__":
    run_triangulation_plots()