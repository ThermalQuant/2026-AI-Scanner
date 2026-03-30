import pandas as pd
import yfinance as yf
from datetime import datetime

print("=== Market Scanner - Alternative Download Method ===")

tickers = ["AAPL", "MSFT", "NVDA", "TSLA"]

data_list = []

for ticker in tickers:
    try:
        print(f"Downloading {ticker}...")

        # Alternative download method
        stock = yf.Ticker(ticker)
        df = stock.history(period="5d")

        if len(df) < 2:
            print(f"  → Not enough data for {ticker}")
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
            'Adj_Close': round(float(latest.get('Close', 0)), 4),   # using Close as fallback
            'Volume': int(latest.get('Volume', 0)),
            'Daily_Change_%': round(float(daily_change), 2),
            'Volume_Intensity': 1.0,
            'Signal': 1 if daily_change > 0 else -1
        }

        data_list.append(row)
        print(f"  → Success for {ticker} | Change: {row['Daily_Change_%']}%")

    except Exception as e:
        print(f"  → Failed {ticker}: {e}")
        continue

if data_list:
    final_df = pd.DataFrame(data_list)
    final_df = final_df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Daily_Change_%', 'Volume_Intensity', 'Signal']]
    
    final_df.to_csv('MarketData_Pro.csv', index=False)
    
    print(f"\n✅ SUCCESS! Saved {len(final_df)} rows")
    print(final_df)
else:
    print("\n❌ No data collected.")
