import pandas as pd
import yfinance as yf
import os

# 1. THE TICKERS (S&P 500 + YOUR CORE LIST)
# You can add all 500 here later, but let's start with these to ensure it runs!
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL", "AMZN", "META", "APLD", "PLTR", "VRT"] 

# 2. Download Data
raw_data = yf.download(tickers, period="1mo", group_by='ticker')

processed_list = []
for ticker in tickers:
    df = raw_data[ticker].copy()
    df['Ticker'] = ticker
    
    # CALCULATE: Daily % Change
    df['Daily_Change_%'] = df['Close'].pct_change() * 100
    
    # CALCULATE: Volume Intensity
    df['Vol_Intensity'] = df['Volume'] / df['Volume'].rolling(window=5).mean()
    
    # NEW: CALCULATE SIGNAL (1 = BUY, -1 = SELL, 0 = WAIT)
    df['Signal'] = 0
    df.loc[(df['Vol_Intensity'] > 1.2) & (df['Daily_Change_%'] > 0), 'Signal'] = 1
    df.loc[(df['Vol_Intensity'] > 1.2) & (df['Daily_Change_%'] < 0), 'Signal'] = -1

    processed_list.append(df.tail(1)) # Only keep the latest data point

# 3. Save the File
final_df = pd.concat(processed_list)
file_path = 'MarketData_Pro.csv'
final_df.to_csv(file_path, index=False)

print("SUCCESS: Intensity and Signals Calculated.")
