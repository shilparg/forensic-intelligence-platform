import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- 1. Bulletproof Pathing ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))         
ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))    
DATA_PATH = os.path.join(ENGINE_DIR, "ml_engine", "ai_scored_forensic_dataset.csv")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "plots")

def run_density_visualization():
    print("📊 Generating Forensic Density JointPlot...")
    
    # 2. Safety Check
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"🚨 Could not find ML output at: {DATA_PATH}\nEnsure fraud_model.py ran successfully first.")

    df = pd.read_csv(DATA_PATH)

    # 3. Set Visual Theme
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 8))

    # 4. Reconciled JointPlot Logic
    g = sns.jointplot(
        data=df,
        x="word_count", 
        y="sentiment_score",
        hue="fraud_risk_status",
        palette={"CRITICAL ANOMALY": "#e74c3c", "NORMAL": "#2ecc71"},
        kind="scatter",
        height=8,
        marginal_kws=dict(fill=True)
    )

    # 5. Add Clear Forensic Labels
    g.fig.suptitle("Forensic Triangulation: SEC Obfuscation vs. AI Risk Scoring", y=1.02, fontsize=16)
    g.set_axis_labels("Disclosure Density (Word Count)", "Management Sentiment Score", fontsize=12)

    # 6. Save the Output for the Capstone Presentation
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_path = os.path.join(OUTPUT_DIR, "forensic_density_matrix.png")
    
    plt.savefig(save_path, bbox_inches='tight')
    print(f"✅ Success! JointPlot saved to: {save_path}")

if __name__ == "__main__":
    run_density_visualization()