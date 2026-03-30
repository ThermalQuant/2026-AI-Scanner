import pandas as pd
import yfinance as yf
from datetime import datetime

print("=== Market Scanner - Simple Reliable Version ===")

# Small, stable list for testing
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "AMD", "AVGO", "LLY"]

data_list = []

for ticker in tickers:
    try:
        print(f"Downloading {ticker}...")
        df = yf.download(ticker, period="5d", interval="1d", progress=False, threads=False)
        
        if len(df) < 2:
            print(f"  → Skipped {ticker} (not enough data)")
            continue

        latest = df.iloc[-1]
        previous = df.iloc[-2]

        daily_change = ((latest['Close'] - previous['Close']) / previous['Close']) * 100

        row = {
            'Date': latest.name.strftime('%Y-%m-%d'),
            'Ticker': ticker,
            'Open': round(float(latest.get('Open', 0)), 4),
            'High': round(float(latest.get('High', 0)), 4),
            'Low': round(float(latest.get('Low', 0)), 4),
            'Close': round(float(latest.get('Close', 0)), 4),
            'Adj_Close': round(float(latest.get('Adj Close', 0)), 4),
            'Volume': int(latest.get('Volume', 0)),
            'Daily_Change_%': round(float(daily_change), 2),
            'Volume_Intensity': 1.0,
            'Signal': 0
        }

        if abs(row['Daily_Change_%']) > 1.0:
            row['Signal'] = 1 if row['Daily_Change_%'] > 0 else -1

        data_list.append(row)
        print(f"  → Success: {ticker} | Change: {row['Daily_Change_%']}%")

    except Exception as e:
        print(f"  → Failed {ticker}: {e}")
        continue

if data_list:
    final_df = pd.DataFrame(data_list)
    final_df = final_df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Daily_Change_%', 'Volume_Intensity', 'Signal']]
    
    final_df.to_csv('MarketData_Pro.csv', index=False)
    
    print(f"\n✅ SUCCESS! Saved {len(final_df)} rows to MarketData_Pro.csv")
    print(final_df[['Date', 'Ticker', 'Close', 'Daily_Change_%', 'Signal']])
else:
    print("\n❌ No data was collected from any ticker.")
