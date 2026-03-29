import json
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

creds_dict = json.loads(os.environ['GSHEET_CREDENTIALS'])
creds = Credentials.from_service_account_info(creds_dict, scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)

worksheet = gc.open_by_key(os.environ['SPREADSHEET_ID']).worksheet("Raw Data")

df = pd.read_csv('MarketData_Pro.csv')

# Force Date to be first column if it exists
if 'Date' in df.columns:
    cols = ['Date'] + [col for col in df.columns if col != 'Date']
    df = df[cols]

df = df.fillna('')
df = df.replace([float('inf'), float('-inf')], '')

worksheet.clear()
worksheet.update([df.columns.tolist()] + df.values.tolist())

print(f"✅ Wrote {len(df)} rows with columns: {list(df.columns)}")
