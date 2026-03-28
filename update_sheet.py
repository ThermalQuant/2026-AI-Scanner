import json
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

print("=== Starting Google Sheets Update ===")

# Load credentials
creds_dict = json.loads(os.environ['GSHEET_CREDENTIALS'])
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

gc = gspread.authorize(creds)

spreadsheet = gc.open_by_key(os.environ['SPREADSHEET_ID'])
worksheet = spreadsheet.worksheet("Raw Data")

print(f"Opened spreadsheet. Worksheet: 'Raw Data'")

# Check if CSV exists and show info
if os.path.exists('MarketData_Pro.csv'):
    df = pd.read_csv('MarketData_Pro.csv')
    print(f"✅ CSV found with {len(df)} rows and columns: {list(df.columns)}")
    print(f"First 3 tickers: {df['Ticker'].head(3).tolist() if 'Ticker' in df.columns else 'No Ticker column'}")
    
    # Handle NaN values
    df = df.fillna('')
    df = df.replace([float('inf'), float('-inf')], '')
    
    # Clear and update
    worksheet.clear()
    worksheet.update([df.columns.tolist()] + df.values.tolist())
    
    print(f"✅ Successfully wrote {len(df)} rows to 'Raw Data' sheet")
else:
    print("❌ MarketData_Pro.csv not found!")

print("=== Update finished ===")
