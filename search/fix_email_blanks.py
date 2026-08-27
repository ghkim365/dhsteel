# -*- coding: utf-8 -*-
"""
"이메일없음" 텍스트 → 빈칸으로 수정
"""
import sys
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding='utf-8')

CREDS_PATH = r"D:\Antigravity\credentials\ghkim\ghkim_credentials.json"
SPREADSHEET_ID = "1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SPREADSHEET_ID)
ws = sh.worksheet("company")

all_rows = ws.get_all_values()
header = all_rows[0]
email_col_idx = header.index('이메일')  # 0-based
email_col_num = email_col_idx + 1       # 1-based (Sheets API)

fixed = 0
for row_num, row in enumerate(all_rows[1:], start=2):
    val = row[email_col_idx].strip() if email_col_idx < len(row) else ""
    if val.lower() in {"이메일없음", "없음", "n/a", "na", "-"}:
        ws.update_cell(row_num, email_col_num, "")
        company = row[2].strip() if len(row) > 2 else "(회사명없음)"
        print(f"  행{row_num:>3} | {company} | '{val}' → 빈칸으로 수정")
        fixed += 1

print(f"\n✅ 총 {fixed}개 셀 수정 완료")
