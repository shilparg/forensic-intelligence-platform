import pandas as pd
import xgboost as xgb
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_DIR, "ai_scored_forensic_dataset.csv")

def generate_market_predictions():
    print("📈 Initializing Supervised Market Predictive AI (XGBoost)...")
    
    if not os.path.exists(DATA_PATH):
        print(f"🚨 Error: Could not find dataset at {DATA_PATH}. Run Model 1 first.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # 1. Define the Predictive Feature Space
    # Crucially, Model 2 ingests the output probability of Model 1! This is a stacked ensemble!
    required_features = [
        'fraud_probability_score', 
        'sentiment_score', 
        'benfords_deviation', 
        'sentiment_volatility', 
        'insider_ownership', 
        'debt_to_equity'
    ]
    
    # Check if Model 1 actually produced the probability scale
    for col in required_features:
        if col not in df.columns:
            print(f"🚨 Missing mandatory feature `{col}`. Did you run the updated fraud_model.py?")
            return
            
    X = df[required_features].fillna(0)
    y = df['short_ratio'].fillna(0)
    
    # 2. Compile the Regression Forecaster
    # XGBoost is the gold standard for structured tabular financial forecasting
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        max_depth=4,
        random_state=42
    )
    
    print("🧠 Training XGBoost Regressor to predict future Wall Street Short Sell Attacks...")
    model.fit(X, y)
    
    # 3. Generate Future Forecasts & Mathematical Deltas
    df['projected_short_ratio'] = model.predict(X).round(2)
    
    # Calculate percentage change (handling divide by zero if stock currently has zero shorts)
    df['expected_short_spike_pct'] = ((df['projected_short_ratio'] - df['short_ratio']) / df['short_ratio'].replace(0, 0.01)) * 100
    df['expected_short_spike_pct'] = df['expected_short_spike_pct'].round(1)
    
    # 4. Native Resave
    df.to_csv(DATA_PATH, index=False)
    print("✅ Future Short Seller predictions dynamically calculated and merged directly into the dataset!")

if __name__ == "__main__":
    generate_market_predictions()
