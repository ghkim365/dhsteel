# -*- coding: utf-8 -*-
import os, sys, datetime
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding='utf-8')

CREDS_PATH = r'E:\Antigravity\credentials\ghkim\ghkim_credentials_crawler-hifus_20260221.json'
SS_ID = '1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic'

creds = Credentials.from_service_account_file(CREDS_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets'])
client = gspread.authorize(creds)
doc_ss = client.open_by_key(SS_ID)

company = doc_ss.worksheet('company')
rows = company.get_all_values()
headers = rows[0]

# 1. Check if '2026-11-09' sheet exists, create or recreate
target_title = '2026-11-09'
existing = [s for s in doc_ss.worksheets() if s.title == target_title]
if existing:
    doc_ss.del_worksheet(existing[0])
    print(f'Existing {target_title} deleted.')

new_ws = doc_ss.add_worksheet(title=target_title, rows=100, cols=len(headers))

# Filter verified 70 companies
verified_rows = []
verified_rows.append(headers)

target_count = 0
for idx, r in enumerate(rows[1:], start=2):
    email = r[5].strip() if len(r) > 5 else ''
    status = r[13].strip() if len(r) > 13 else ''
    if email and '@' in email and '성공' in status:
        new_row = list(r)
        # Pad row to match header length
        while len(new_row) < len(headers):
            new_row.append('')
        # Set A col to TRUE (checkbox)
        new_row[0] = 'TRUE'
        # Set M col to '2차 정기(11/09)'
        new_row[12] = '2차 정기(11/09)'
        verified_rows.append(new_row)
        target_count += 1

print(f'Extracted {target_count} verified targets.')

# Update the new sheet
new_ws.update(verified_rows, 'A1')

# Format headers and checkboxes
new_ws.format('A1:V1', {
    'backgroundColor': {'red': 0.12, 'green': 0.23, 'blue': 0.36},
    'textFormat': {'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}, 'fontSize': 10, 'bold': True}
})

print(f'Successfully created and populated {target_title} sheet with {target_count} companies!')

