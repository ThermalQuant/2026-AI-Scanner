import pandas as pd
import yfinance as yf

print("=== Starting Market Scanner v4 - Force Date First ===")

tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "GOOG", "LLY", "JPM", "V", "XOM", "UNH", "MA", "PG", "JNJ", "HD", "MRK", "COST", "ABBV", "NFLX", "AMD", "CRM", "TMUS", "LIN", "WMT", "BAC", "CVX", "KO", "PEP", "ACN", "MCD", "CSCO", "ADBE", "ABT", "WFC", "INTU", "DIS", "VZ", "CMCSA", "PFE", "AMGN", "TXN", "HON", "NEE", "IBM", "RTX", "SPGI", "LOW", "PM", "GS", "CAT", "UNP", "GE", "BA", "ELV", "ETN", "SYK", "BLK", "MDT", "ADP", "LMT", "SBUX", "NOW", "ISRG", "PLD", "INTC", "SCHW", "REGN", "BKNG", "KLAC", "PANW", "FI", "ANET", "KKR", "ADI", "MU", "GILD", "SO", "MO", "ICE", "ZTS", "CME", "ITW", "SHW", "DUK", "CL", "WM", "TGT", "EOG", "SNPS", "BSX", "APD", "PGR", "CDNS", "MAR", "ORCL", "SLB", "PSX", "OKE", "PH", "ROP", "MPC", "USB", "AON"]

data_list = []

for ticker in tickers:
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False, threads=False)
        if len(df) < 2:
            continue

        latest = df.iloc[-1]
        previous = df.iloc[-2]

        daily_change = ((latest['Close'] - previous['Close']) / previous['Close']) * 100

        row = {
            'Date': latest.name.strftime('%Y-%m-%d'),
            'Ticker': ticker,
            'Open': round(float(latest['Open']), 4),
            'High': round(float(latest['High']), 4),
            'Low': round(float(latest['Low']), 4),
            'Close': round(float(latest['Close']), 4),
            'Adj_Close': round(float(latest['Adj Close']), 4),
            'Volume': int(latest['Volume']),
            'Daily_Change_%': round(float(daily_change), 2),
            'Volume_Intensity': round(float(latest['Volume'] / df['Volume'].rolling(5).mean().iloc[-1]), 2) if len(df) >= 5 else 1.0,
            'Signal': 0
        }

        if row['Volume_Intensity'] > 1.5 and abs(row['Daily_Change_%']) > 1.0:
            row['Signal'] = 1 if row['Daily_Change_%'] > 0 else -1

        data_list.append(row)

    except:
        continue

if data_list:
    final_df = pd.DataFrame(data_list)
    
    # Force 'Date' to be the first column
    cols = ['Date'] + [col for col in final_df.columns if col != 'Date']
    final_df = final_df[cols]
    
    final_df = final_df.sort_values(by='Daily_Change_%', ascending=False).reset_index(drop=True)
    
    final_df.to_csv('MarketData_Pro.csv', index=False)
    
    print(f"✅ Saved {len(final_df)} rows")
    print("Columns in order:", list(final_df.columns))
    print(final_df.head(5)[['Date', 'Ticker', 'Close', 'Daily_Change_%', 'Signal']])
else:
    print("No data retrieved.")
