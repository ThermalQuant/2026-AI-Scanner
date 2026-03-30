import pandas as pd
import yfinance as yf
from datetime import datetime

print("=== Ultra Simple Scanner Test ===")

tickers = ["AAPL", "NVDA", "TSLA"]

data_list = []

for ticker in tickers:
    try:
        print(f"Downloading {ticker}...")
        df = yf.download(ticker, period="2d", interval="1d", progress=False)
        
        if len(df) < 2:
            print(f"  → Not enough data for {ticker}")
            continue

        latest = df.iloc[-1]
        previous = df.iloc[-2]

        change = ((latest['Close'] - previous['Close']) / previous['Close']) * 100

        row = {
            'Date': latest.name.strftime('%Y-%m-%d'),
            'Ticker': ticker,
            'Close': round(float(latest['Close']), 2),
            'Daily_Change_%': round(float(change), 2),
            'Volume': int(latest['Volume']),
            'Signal': 1 if change > 0 else -1
        }

        data_list.append(row)
        print(f"  → Success for {ticker} | Change: {row['Daily_Change_%']}%")

    except Exception as e:
        print(f"  → Failed {ticker}: {e}")

if data_list:
    final_df = pd.DataFrame(data_list)
    final_df.to_csv('MarketData_Pro.csv', index=False)
    print(f"\n✅ SUCCESS! Created MarketData_Pro.csv with {len(final_df)} rows")
    print(final_df)
else:
    print("\n❌ Still no data collected.")
