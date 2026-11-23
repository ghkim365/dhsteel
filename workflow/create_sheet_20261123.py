# -*- coding: utf-8 -*-
"""
create_sheet_20261123.py
1. 구글 스프레드시트에 '2026-11-23' 전용 워크시트 생성 (검증 우량 68개사)
2. 'company' 시트 A열 체크박스 및 M열 회차('3차 정기(11/23)') 동기화
3. 코베아 오타 도메인(kovea.co.kr) 정제 반영, 금경이노텍/아이디오 제외 완료
"""

import os, sys, datetime
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding='utf-8')

CREDS_PATH = r'E:\Antigravity\credentials\ghkim\ghkim_credentials_crawler-hifus_20260221.json'
SS_ID = '1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic'

creds = Credentials.from_service_account_file(CREDS_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets'])
client = gspread.authorize(creds)
doc_ss = client.open_by_key(SS_ID)

# 1. 11/09 시트에서 검증 70개사 로드
ws_09 = doc_ss.worksheet('2026-11-09')
rows_09 = ws_09.get_all_values()
headers = rows_09[0]

targets_68 = []
target_names = set()

for r in rows_09[1:]:
    name = r[2].strip()
    email = r[5].strip()
    
    # 제외 대상 2곳
    if name == '금경이노텍' or '(주)금경이노텍' in name:
        continue
    if name == '아이디오' or '(주)아이디오' in name:
        continue
        
    # 코베아 도메인 오타 정제
    if name == '코베아' or '(주)코베아' in name or 'kovea' in email:
        r[5] = 'kovea@kovea.co.kr'
        
    # 행 규격 패딩
    row_copy = list(r)
    while len(row_copy) < len(headers):
        row_copy.append('')
        
    row_copy[0] = 'TRUE'
    row_copy[12] = '3차 정기(11/23)'
    
    targets_68.append(row_copy)
    target_names.add(name)

print(f'[선별 완료] 총 {len(targets_68)}개사 검증 타겟 확정.')

# 2. '2026-11-23' 워크시트 생성 또는 재생성
target_title = '2026-11-23'
existing = [s for s in doc_ss.worksheets() if s.title == target_title]
if existing:
    doc_ss.del_worksheet(existing[0])
    print(f'[기존 시트 삭제] {target_title}')

new_ws = doc_ss.add_worksheet(title=target_title, rows=len(targets_68) + 20, cols=len(headers))

# 헤더 + 데이터 업데이트
all_rows_to_insert = [headers] + targets_68
new_ws.update(all_rows_to_insert, 'A1')

# 헤더 스타일링
new_ws.format('A1:V1', {
    'backgroundColor': {'red': 0.11, 'green': 0.17, 'blue': 0.29},
    'textFormat': {'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}, 'fontSize': 10, 'bold': True}
})
print(f'[시트 생성 성공] {target_title} 워크시트에 68개사 등록 완료.')

# 3. 메인 'company' 시트 A열 및 M열 동기화
comp_ws = doc_ss.worksheet('company')
comp_rows = comp_ws.get_all_values()

updates_A = [] # A열 체크박스
updates_M = [] # M열 회차
matched_count = 0

for idx, r in enumerate(comp_rows[1:], start=2):
    c_name = r[2].strip() if len(r) > 2 else ''
    
    if c_name in target_names:
        updates_A.append({'range': f'A{idx}', 'values': [['TRUE']]})
        updates_M.append({'range': f'M{idx}', 'values': [['3차 정기(11/23)']]})
        if c_name == '코베아' or '(주)코베아' in c_name:
            comp_ws.update([[ 'kovea@kovea.co.kr' ]], f'F{idx}')
        matched_count += 1
    else:
        # 비대상은 A열 체크 해제
        if len(r) > 0 and r[0] == 'TRUE':
            updates_A.append({'range': f'A{idx}', 'values': [['FALSE']]})

print(f'[company 시트 매칭] {matched_count}개사 A열 체크 및 M열 회차 동기화 준비 중...')

# Batch update A열 및 M열
comp_ws.batch_update(updates_A + updates_M)
print(f'[company 시트 동기화 완료] 68개사 A열 TRUE 및 회차 세팅 완료!')

