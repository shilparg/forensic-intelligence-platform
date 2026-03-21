import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. Bulletproof Pathing ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))         
ENGINE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))    
DATA_PATH = os.path.join(ENGINE_DIR, "ml_engine", "ai_scored_forensic_dataset.csv")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "plots")

def run_presentation_visuals():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"🚨 Could not find ML output at: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    sns.set_theme(style="whitegrid")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ==========================================
    # VISUAL 1: The Correlation Heatmap (Migrated from visualize_risk.py)
    # ==========================================
    print("📊 Generating Correlation Heatmap...")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    if not numeric_df.empty:
        corr_matrix = numeric_df.corr()
        plt.figure(figsize=(10, 8))
        plt.title("Forensic Triangulation: Metric Correlation Matrix", fontsize=14, pad=15)
        
        sns.heatmap(
            corr_matrix, 
            annot=True, 
            fmt=".2f", 
            cmap="coolwarm", 
            vmin=-1, vmax=1, 
            center=0, 
            linewidths=0.5, 
            cbar_kws={"shrink": .8}
        )
        plt.tight_layout()
        
        # Save silently instead of using plt.show()
        heatmap_path = os.path.join(OUTPUT_DIR, "correlation_heatmap.png")
        plt.savefig(heatmap_path, bbox_inches='tight')
        plt.close()
        print("✅ Saved Correlation Heatmap.")

    # ==========================================
    # VISUAL 2: Multi-Ticker Radar Charts
    # ==========================================
    print("🕸️ Generating AI Decision Radar Charts...")
    avg = df.mean(numeric_only=True)
    labels = ['Sentiment', 'Density/Words', 'Short Ratio', 'Debt/Equity']
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1] 

    avg_stats = [
        avg.get('sentiment_score', 0), 
        avg.get('density_index', avg.get('word_count', 0)), 
        avg.get('short_ratio', 0), 
        avg.get('debt_to_equity', 0)
    ]
    avg_stats += avg_stats[:1]

    anomalies = df[df['fraud_risk_status'] == 'CRITICAL ANOMALY']
    
    if anomalies.empty:
        print("✅ No anomalies to plot for radar charts.")
    else:
        for idx, target in anomalies.iterrows():
            ticker = target['ticker']
            
            target_stats = [
                target.get('sentiment_score', 0), 
                target.get('density_index', target.get('word_count', 0)), 
                target.get('short_ratio', 0), 
                target.get('debt_to_equity', 0)
            ]
            target_stats += target_stats[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles, target_stats, color='red', linewidth=2, label=f"Anomaly: {ticker}")
            ax.fill(angles, target_stats, color='red', alpha=0.25)
            ax.plot(angles, avg_stats, color='gray', linewidth=2, linestyle='dashed', label='Industry Average')
            
            ax.set_yticklabels([])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            plt.title(f"AI Decision Matrix: {ticker}", y=1.08)
            
            save_path = os.path.join(OUTPUT_DIR, f"ai_radar_chart_{ticker}.png")
            plt.savefig(save_path, bbox_inches='tight')
            plt.close() 
            print(f"✅ Saved Radar Chart for {ticker}.")

if __name__ == "__main__":
    run_presentation_visuals()