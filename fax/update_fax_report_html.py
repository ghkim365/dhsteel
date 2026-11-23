# -*- coding: utf-8 -*-
import os, sys, json
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding='utf-8')

CREDS_PATH = r'E:\Antigravity\credentials\ghkim\ghkim_credentials_crawler-hifus_20260221.json'
SS_ID = '1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic'
creds = Credentials.from_service_account_file(CREDS_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets'])
client = gspread.authorize(creds)
doc_ss = client.open_by_key(SS_ID)

fax_log = doc_ss.worksheet('fax_log')
rows = fax_log.get_all_values()[1:]

# Format into allFaxLogs format:
# { "id": "141", "date": "2026-11-16", "company": "삼일기업", "fax": "0315443186", "round": "팩스 6회차(정기)", "status": "성공", "detail": "정상 수신 완료 (10:49)", "note": "샌드랩스 대량 팩스" }
all_logs = []
for r in rows:
    seq = r[1].strip()
    date_val = r[2].strip()[:10]
    company = r[3].strip()
    fax_clean = r[4].replace('-', '').strip()
    round_val = r[5].strip()
    # Normalize round name for dropdown grouping
    if '6' in round_val:
        round_val = '팩스 6회차(정기)'
    elif '5' in round_val:
        round_val = '팩스 5회차(2차전환)'
    status = r[6].strip()
    detail = r[7].strip()
    note = r[8].strip() or '샌드랩스 대량 팩스'
    
    all_logs.append({
        "id": seq,
        "date": date_val,
        "company": company,
        "fax": fax_clean,
        "round": round_val,
        "status": status,
        "detail": detail,
        "note": note
    })

# Reverse so latest is first
all_logs.reverse()

html_path = r'E:\Antigravity\builder-dhsteel-sales\fax\fax_report.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

target_start = 'let allFaxLogs = ['
idx_start = html.find(target_start)
if idx_start == -1:
    print('Error: let allFaxLogs not found!')
    sys.exit(1)

idx_end = html.find('];', idx_start)
if idx_end == -1:
    print('Error: closing bracket of allFaxLogs not found!')
    sys.exit(1)

new_json_str = 'let allFaxLogs = ' + json.dumps(all_logs, ensure_ascii=False, indent=8) + ';'

html = html[:idx_start] + new_json_str + html[idx_end+2:]

# Update document date / number if needed
html = html.replace('2026.11.02', '2026.11.16')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Successfully updated fax_report.html with {len(all_logs)} entries!')

