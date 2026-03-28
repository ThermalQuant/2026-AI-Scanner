import pandas as pd
import yfinance as yf
from datetime import datetime

print("Starting market scanner...")

# Clean, up-to-date S&P 500 tickers (major ones - easy to expand later)
tickers = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "GOOG", "LLY",
    "JPM", "V", "XOM", "UNH", "MA", "PG", "JNJ", "HD", "MRK", "COST", "ABBV",
    "NFLX", "AMD", "CRM", "TMUS", "LIN", "WMT", "BAC", "CVX", "KO", "PEP", "ACN",
    "MCD", "CSCO", "ADBE", "ABT", "WFC", "INTU", "DIS", "VZ", "CMCSA", "PFE",
    "AMGN", "TXN", "HON", "NEE", "IBM", "RTX", "SPGI", "LOW", "PM", "GS", "CAT",
    "UNP", "GE", "BA", "ELV", "ETN", "SYK", "BLK", "MDT", "ADP", "LMT", "SBUX",
    "NOW", "ISRG", "PLD", "INTC", "SCHW", "REGN", "BKNG", "KLAC", "PANW", "FI",
    "ANET", "KKR", "ADI", "MU", "GILD", "SO", "MO", "ICE", "ZTS", "CME", "ITW",
    "SHW", "DUK", "CL", "WM", "TGT", "EOG", "SNPS", "BSX", "APD", "PGR", "CDNS",
    "MAR", "ORCL", "SLB", "PSX", "OKE", "PH", "ROP", "MPC", "USB", "AON"
]

print(f"Scanning {len(tickers)} tickers...")

data_list = []

for ticker in tickers:
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False, threads=False)
        
        if df.empty:
            continue
            
        latest = df.iloc[-1].copy()  # Get the most recent day
        
        row = {
            'Date': latest.name.strftime('%Y-%m-%d'),
            'Ticker': ticker,
            'Open': round(latest['Open'], 4),
            'High': round(latest['High'], 4),
            'Low': round(latest['Low'], 4),
            'Close': round(latest['Close'], 4),
            'Adj_Close': round(latest['Adj Close'], 4),
            'Volume': int(latest['Volume']),
            'Daily_Change_%': round(((latest['Close'] - df.iloc[-2]['Close']) / df.iloc[-2]['Close']) * 100, 2) if len(df) > 1 else 0.0,
            'Volume_Intensity': round(latest['Volume'] / df['Volume'].rolling(5).mean().iloc[-1], 2) if len(df) >= 5 else 1.0,
        }
        
        # Simple signal
        if row['Volume_Intensity'] > 1.3 and row['Daily_Change_%'] > 0.5:
            row['Signal'] = 1
        elif row['Volume_Intensity'] > 1.3 and row['Daily_Change_%'] < -0.5:
            row['Signal'] = -1
        else:
            row['Signal'] = 0
            
        data_list.append(row)
        
    except Exception as e:
        continue  # Skip bad tickers quietly

# Create final DataFrame
if data_list:
    final_df = pd.DataFrame(data_list)
    final_df = final_df.sort_values(by='Daily_Change_%', ascending=False)
    
    final_df.to_csv('MarketData_Pro.csv', index=False)
    
    print(f"✅ Paper saved successfully! {len(final_df)} tickers processed.")
    print(f"Top 5 gainers:\n{final_df[['Ticker', 'Daily_Change_%', 'Volume_Intensity', 'Signal']].head(5)}")
else:
    print("❌ No data retrieved.")
