import pandas as pd
import yfinance as yf

print("=== Daily Market Scanner - Clean + Alerts ===")

tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "AMD", "AVGO", "LLY"]

data_list = []

for ticker in tickers:
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if len(df) < 2:
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
            'Volume_Intensity': round(float(latest.get('Volume', 0) / df['Volume'].rolling(5).mean().iloc[-1]), 2) if len(df) >= 5 else 1.0,
            'Signal': 0,
            'Alert': ''
        }

        # Simple Alert Rules
        if row['Volume_Intensity'] > 1.8:
            row['Alert'] = 'HIGH VOLUME'
        if abs(row['Daily_Change_%']) > 2.0:
            row['Alert'] = 'STRONG MOVE'
        if row['Volume_Intensity'] > 1.8 and abs(row['Daily_Change_%']) > 2.0:
            row['Alert'] = '🚨 VOLUME + MOVE'

        if abs(row['Daily_Change_%']) > 1.0:
            row['Signal'] = 1 if row['Daily_Change_%'] > 0 else -1

        data_list.append(row)

    except:
        continue

if data_list:
    final_df = pd.DataFrame(data_list)
    
    # Force Date as first column
    cols = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 
            'Daily_Change_%', 'Volume_Intensity', 'Signal', 'Alert']
    final_df = final_df[[col for col in cols if col in final_df.columns]]
    
    final_df.to_csv('MarketData_Pro.csv', index=False)
    
    print(f"✅ Saved {len(final_df)} rows")
    print(final_df[['Date', 'Ticker', 'Close', 'Daily_Change_%', 'Volume_Intensity', 'Alert']])
else:
    print("❌ No data collected.")
