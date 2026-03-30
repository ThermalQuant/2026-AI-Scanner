import json
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

print("=== Daily Scanner - Append Mode (Safe) ===")

# Load credentials
creds_dict = json.loads(os.environ['GSHEET_CREDENTIALS'])
creds = Credentials.from_service_account_info(creds_dict, scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)

worksheet = gc.open_by_key(os.environ['SPREADSHEET_ID']).worksheet("Raw Data")

# Check if CSV exists
if not os.path.exists('MarketData_Pro.csv'):
    print("❌ MarketData_Pro.csv not found! Scanner probably failed.")
    worksheet.append_row([f"Scanner failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - No CSV generated"])
    exit(1)

# Read the new scan
df = pd.read_csv('MarketData_Pro.csv')

if df.empty:
    print("❌ CSV is empty")
    worksheet.append_row(["CSV was empty"])
else:
    # Add scan timestamp
    df['Scan_Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Append to sheet
    worksheet.append_rows([df.columns.tolist()] + df.values.tolist(), value_input_option='RAW')
    
    print(f"✅ Appended {len(df)} new rows to 'Raw Data' sheet")
    print(f"Scan time: {df['Scan_Time'].iloc[0]}")
    print(f"Columns: {list(df.columns)}")

print("=== Append finished ===")
