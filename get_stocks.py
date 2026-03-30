import pandas as pd
import yfinance as yf

print("=== Market Scanner - Minimal Test Version ===")

# Very small, reliable test list
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "AMD"]

data_list = []

for ticker in tickers:
    try:
        print(f"Downloading {ticker}...")
        df = yf.download(ticker, period="5d", interval="1d", progress=False, threads=False)
        
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
            'Adj_Close': round(float(latest.get('Adj Close', 0)), 4),
            'Volume': int(latest.get('Volume', 0)),
            'Daily_Change_%': round(float(daily_change), 2),
            'Volume_Intensity': 1.0,
            'Signal': 0
        }

        data_list.append(row)
        print(f"  → Success for {ticker}")

    except Exception as e:
        print(f"  → Failed for {ticker}: {e}")
        continue

if data_list:
    final_df = pd.DataFrame(data_list)
    final_df = final_df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Daily_Change_%', 'Volume_Intensity', 'Signal']]
    
    final_df.to_csv('MarketData_Pro.csv', index=False)
    
    print(f"✅ SUCCESS! Saved {len(final_df)} rows")
    print(final_df)
else:
    print("❌ No data collected from any ticker.")
