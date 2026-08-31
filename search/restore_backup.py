# -*- coding: utf-8 -*-
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

def main():
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SPREADSHEET_ID)
    ws = sh.worksheet('mail_log')

    all_rows = ws.get_all_values()
    print(f"전체 행 수: {len(all_rows)}")

    header = all_rows[0] if all_rows else []
    
    # 실제 데이터가 있는 행만 남기기 (D열=회사명이 있는 행)
    real_rows = [row for row in all_rows[1:] if len(row) > 3 and row[3].strip()]
    print(f"유효한 데이터 행: {len(real_rows)}개")

    # 시트 초기화 후 헤더 + 유효 데이터만 다시 쓰기
    ws.clear()
    ws.update(values=[header], range_name="A1:I1")
    if real_rows:
        ws.append_rows(real_rows, value_input_option='USER_ENTERED')

    print(f"✅ mail_log 정리 완료! {len(real_rows)}행만 남겼습니다.")

if __name__ == "__main__":
    main()
