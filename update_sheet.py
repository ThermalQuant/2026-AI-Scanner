import json
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Load credentials
creds_dict = json.loads(os.environ['GSHEET_CREDENTIALS'])
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

gc = gspread.authorize(creds)

spreadsheet = gc.open_by_key(os.environ['SPREADSHEET_ID'])
worksheet = spreadsheet.worksheet("Raw Data")

# Read CSV
df = pd.read_csv('MarketData_Pro.csv')

# Fix NaN / inf values so gspread can handle them
df = df.fillna('')                    # Replace NaN with empty string
df = df.replace([float('inf'), float('-inf')], '')   # Replace inf with empty

if df.empty:
    print("❌ No data found in MarketData_Pro.csv")
else:
    # Clear and update
    worksheet.clear()
    worksheet.update([df.columns.tolist()] + df.values.tolist())
    
    print(f"✅ Successfully updated 'Raw Data' with {len(df)} rows and {len(df.columns)} columns.")
    print(f"Columns: {list(df.columns)}")
    print(f"Sample tickers: {df['Ticker'].head(10).tolist()}")
