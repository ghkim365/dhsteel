# -*- coding: utf-8 -*-
"""
company 시트 발송 배치 배정 스크립트
- M열 헤더: "발송일" → "발송대기"로 변경
- O열 헤더: "발송일" 추가 (없으면)
- M열에 우선순위 기반 "1일차"~"N일차" 배정 (20개씩)
  우선순위: 1순위 카테고리 > 2순위 > 3순위, 동일 순위 내 ✅ 정상 우선
"""
import sys
import gspread
from google.oauth2.service_account import Credentials

sys.stdout.reconfigure(encoding='utf-8')

CREDS_PATH     = r"D:\Antigravity\credentials\ghkim\ghkim_credentials.json"
SPREADSHEET_ID = "1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
DAILY_LIMIT = 20

def priority_score(category, quality):
    score = 0
    if   '1순위' in category: score += 100
    elif '2순위' in category: score += 60
    elif '3순위' in category: score += 30
    else:                      score += 10
    if '✅' in quality or '정상' in quality: score += 10
    return score

def col_letter(idx_0based):
    """0-based 인덱스 → A, B, ... Z, AA, AB..."""
    n = idx_0based
    result = ''
    while True:
        result = chr(ord('A') + n % 26) + result
        n = n // 26 - 1
        if n < 0:
            break
    return result

# ── 연결 ──────────────────────────────────────────────
creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
gc    = gspread.authorize(creds)
sh    = gc.open_by_key(SPREADSHEET_ID)
ws    = sh.worksheet("company")

all_rows = ws.get_all_values()
header   = all_rows[0]
data     = all_rows[1:]

print(f"현재 헤더: {header}")
print(f"데이터 행 수: {len(data)}\n")

# ── 컬럼 인덱스 파악 ───────────────────────────────────
email_idx    = next((i for i, h in enumerate(header) if '이메일' in h or 'email' in h.lower()), 5)
category_idx = next((i for i, h in enumerate(header) if '품목' in h or '카테고리' in h), 3)
quality_idx  = next((i for i, h in enumerate(header) if '품질' in h), 11)
m_idx        = next((i for i, h in enumerate(header) if h.strip() in ['발송일', '발송대기']), None)
n_idx        = next((i for i, h in enumerate(header) if '발송상태' in h), None)
o_idx        = next((i for i, h in enumerate(header) if h.strip() == '발송일' and i != m_idx), None)

print(f"이메일 컬럼:  {col_letter(email_idx)}열 (idx={email_idx})")
print(f"카테고리 컬럼: {col_letter(category_idx)}열 (idx={category_idx})")
print(f"품질 컬럼:    {col_letter(quality_idx)}열 (idx={quality_idx})")
print(f"M열 현재 헤더: '{header[m_idx] if m_idx is not None else '없음'}'")
print(f"N열 현재 헤더: '{header[n_idx] if n_idx is not None else '없음'}'")
print()

# ── Step 1: M열 헤더 → "발송대기" 변경 ─────────────────
if m_idx is not None and header[m_idx].strip() != '발송대기':
    ws.update_cell(1, m_idx + 1, '발송대기')
    print(f"✅ {col_letter(m_idx)}열 헤더 변경: '{header[m_idx]}' → '발송대기'")
    header[m_idx] = '발송대기'
else:
    print(f"ℹ️  M열 헤더 이미 '발송대기' 또는 없음")

# ── Step 2: N열 헤더 "발송상태" 확인 ────────────────────
if n_idx is not None:
    print(f"ℹ️  N열 헤더 확인: '{header[n_idx]}' (변경 없음)")
else:
    # N열 없으면 추가
    n_idx = len(header)
    ws.update_cell(1, n_idx + 1, '발송상태')
    header.append('발송상태')
    print(f"✅ N열 헤더 추가: '발송상태'")

# ── Step 3: O열 헤더 "발송일" 확인/추가 ─────────────────
o_header_idx = next((i for i, h in enumerate(header) if h.strip() == '발송일' and i > n_idx), None)
if o_header_idx is not None:
    print(f"ℹ️  O열 헤더 확인: '{header[o_header_idx]}' ({col_letter(o_header_idx)}열, 변경 없음)")
    o_idx = o_header_idx
else:
    # M열 다음 N열 다음이 O열
    o_idx = max(n_idx, m_idx if m_idx else 0) + 1
    ws.update_cell(1, o_idx + 1, '발송일')
    if o_idx < len(header):
        header[o_idx] = '발송일'
    else:
        header.append('발송일')
    print(f"✅ {col_letter(o_idx)}열 헤더 추가: '발송일'")

print()

# ── Step 4: 유효 이메일 + 미배정 행 수집 ────────────────
candidates = []
for r, row in enumerate(data, start=2):
    email    = row[email_idx].strip()    if email_idx    < len(row) else ''
    category = row[category_idx].strip() if category_idx < len(row) else ''
    quality  = row[quality_idx].strip()  if quality_idx  < len(row) else ''
    m_val    = row[m_idx].strip()        if m_idx is not None and m_idx < len(row) else ''

    if not email or '@' not in email:
        continue  # 이메일 없음 스킵
    if m_val:
        continue  # 이미 배정된 행 스킵 (재실행 안전)

    candidates.append({
        'row': r,
        'category': category,
        'quality': quality,
        'score': priority_score(category, quality),
    })

# 우선순위 정렬 (점수 높은 순 → 행 번호 오름차순)
candidates.sort(key=lambda x: (-x['score'], x['row']))

print(f"배정 대상 업체 수: {len(candidates)}개")
print(f"예상 일차 수: {-(-len(candidates)//DAILY_LIMIT)}일차 (하루 {DAILY_LIMIT}개 기준)\n")

# ── Step 5: M열에 "N일차" 배정 ───────────────────────────
batch_updates = []  # (row_num, day_label)
for i, c in enumerate(candidates):
    day_num   = i // DAILY_LIMIT + 1
    day_label = f"{day_num}일차"
    batch_updates.append((c['row'], day_label))

# 배치 업데이트 (gspread batch)
print("M열 배정 중...")
cell_list = []
for row_num, day_label in batch_updates:
    cell_list.append(gspread.Cell(row_num, m_idx + 1, day_label))

ws.update_cells(cell_list, value_input_option='RAW')
print(f"✅ 총 {len(cell_list)}개 업체에 발송대기(일차) 배정 완료!\n")

# ── 결과 요약 ─────────────────────────────────────────────
from collections import Counter
day_counter = Counter(b[1] for b in batch_updates)
print("=" * 45)
print("  발송 배치 배정 결과")
print("=" * 45)
for day in sorted(day_counter.keys(), key=lambda x: int(x.replace('일차', ''))):
    print(f"  {day}: {day_counter[day]}개")
print(f"\n  합계: {len(batch_updates)}개")
print("=" * 45)
print("\n✅ 완료! 시트의 M열(발송대기)을 확인하세요.")
