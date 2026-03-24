import logging

# Create a log file so you can see if the script failed while you were sleeping
logging.basicConfig(filename='market_scanner.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

try:
    # Your existing download code here
    logging.info("Scan Successful: Data saved.")
except Exception as e:
    logging.error(f"Scan Failed: {e}")

import pandas as pd
import yfinance as yf
import os

# 1. Tickers (The 2026 AI Infrastructure Kings)
tickers = ["NVDA", "VRT", "CEG", "GEV", "CCJ", "PLTR", "APLD", "NEE"]

# 2. Download Data
print("Scanning 2026 AI Infrastructure Market...")
raw_data = yf.download(tickers, period="1mo", group_by='ticker')

# 3. Process the "Performance" Columns
processed_list = []

for ticker in tickers:
    # Extract this ticker's data
    df = raw_data[ticker].copy()
    df['Ticker'] = ticker
    
    # CALCULATE: Daily % Change
    df['Daily_Change_%'] = df['Close'].pct_change() * 100
    
    # CALCULATE: Volume Intensity (Today's Vol / 5-Day Avg Vol)
    df['Vol_Intensity'] = df['Volume'] / df['Volume'].rolling(window=5).mean()
    
    processed_list.append(df)

# Combine everything into one clean sheet
final_df = pd.concat(processed_list).sort_index()

# 4. Save the File
current_folder = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_folder, 'MarketData_Pro.csv')
final_df.to_csv(file_path)

print(f"\nSUCCESS! Daily % Change and Volume Intensity calculated.")
print(f"File saved as: MarketData_Pro.csv")
