import json
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# === Load credentials from GitHub secret ===
creds_dict = json.loads(os.environ['GSHEET_CREDENTIALS'])
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)

gc = gspread.authorize(creds)

# === Open your spreadsheet and worksheet ===
spreadsheet = gc.open_by_key(os.environ['SPREADSHEET_ID'])
worksheet = spreadsheet.worksheet("Raw Data")

# === Read the CSV produced by get_stocks.py ===
df = pd.read_csv('MarketData_Pro.csv')

# === Clear old data and write fresh data (with headers) ===
worksheet.clear()
worksheet.update([df.columns.tolist()] + df.values.tolist())

print(f"Success: Successfully updated 'Raw Data' with {len(df)} rows and {len(df.columns)} columns.")
print(f"Columns: {list(df.columns)}")
