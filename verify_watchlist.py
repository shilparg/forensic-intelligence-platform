import pandas as pd
import yfinance as yf
import os

def verify_sectors(csv_filename="target_tickers.csv"):
    if not os.path.exists(csv_filename):
        print(f"❌ Error: {csv_filename} not found.")
        return

    df = pd.read_csv(csv_filename)
    print(f"🔍 Verifying sectors for {len(df)} tickers...\n")
    print(f"{'Ticker':<8} | {'Your Sector':<25} | {'Official Sector':<25} | {'Status'}")
    print("-" * 80)

    for _, row in df.iterrows():
        ticker_sym = str(row['ticker']).upper().strip()
        your_sector = str(row['sector']).strip()
        
        try:
            # Fetch official sector from Yahoo Finance
            ticker_obj = yf.Ticker(ticker_sym)
            official_sector = ticker_obj.info.get('sector', 'N/A')
            
            # Simple check (case-insensitive)
            status = "✅ MATCH" if your_sector.lower() in official_sector.lower() or official_sector == 'N/A' else "⚠️ MISMATCH"
            
            print(f"{ticker_sym:<8} | {your_sector:<25} | {official_sector:<25} | {status}")
        except Exception as e:
            print(f"{ticker_sym:<8} | {your_sector:<25} | ERROR: {str(e)[:20]}...")

if __name__ == "__main__":
    verify_sectors()