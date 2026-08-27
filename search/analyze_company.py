# -*- coding: utf-8 -*-
"""
company 시트 전체 데이터 분석 - 업종/카테고리 분포 확인
"""
import sys
import gspread
from google.oauth2.service_account import Credentials
from collections import Counter

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
data_rows = all_rows[1:]

print(f"헤더: {header}")
print(f"총 행 수: {len(data_rows)}\n")

# 컬럼 인덱스
cat_idx = header.index('주요 품목/카테고리')
quality_idx = header.index('품질')
email_idx = header.index('이메일')

# 품질 분포
quality_counter = Counter()
for row in data_rows:
    q = row[quality_idx].strip() if quality_idx < len(row) else ""
    quality_counter[q] += 1

print("=== 품질(L열) 분포 ===")
for k, v in sorted(quality_counter.items(), key=lambda x: -x[1]):
    print(f"  '{k}': {v}건")

print()

# 카테고리 분포
cat_counter = Counter()
for row in data_rows:
    c = row[cat_idx].strip() if cat_idx < len(row) else ""
    cat_counter[c] += 1

print("=== 주요 품목/카테고리(D열) 분포 (상위 40개) ===")
for k, v in sorted(cat_counter.items(), key=lambda x: -x[1])[:40]:
    print(f"  '{k}': {v}건")

print()

# 유효 이메일 있는 행 기준으로 샘플 출력
print("=== 유효 이메일 있는 행 샘플 (처음 20개) ===")
count = 0
for i, row in enumerate(data_rows, start=2):
    email = row[email_idx].strip() if email_idx < len(row) else ""
    cat = row[cat_idx].strip() if cat_idx < len(row) else ""
    quality = row[quality_idx].strip() if quality_idx < len(row) else ""
    company = row[2].strip() if len(row) > 2 else ""
    if "@" in email and count < 20:
        print(f"  행{i:>3} | 품질={quality:<5} | {company:<20} | {cat:<30} | {email}")
        count += 1
