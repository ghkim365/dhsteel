# -*- coding: utf-8 -*-
"""
company 시트의 이메일 유효성 체크 스크립트
"""
import re
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

EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
)

INVALID_VALUES = {
    "", "-", "없음", "n/a", "na", "없음", "미확인", "null", "none", "x", "?",
    ".", "..", "모름", "비공개", "정보없음", "미정"
}

def classify_email(val):
    """이메일 유효성 분류. 문제 유형 문자열 반환, 정상이면 None"""
    if not val or val.strip() == "":
        return "빈값"
    
    v = val.strip()
    
    if v.lower() in INVALID_VALUES:
        return f"무효 텍스트: '{v}'"
    
    if "@" not in v:
        return "@가 없음"
    
    parts = v.split("@")
    if len(parts) != 2:
        return "@가 2개 이상"
    
    local, domain = parts
    
    if not local:
        return "@앞(로컬) 부분이 비어있음"
    
    if not domain:
        return "@뒤(도메인) 부분이 비어있음"
    
    if "." not in domain:
        return f"도메인에 점(.)이 없음: '{domain}'"
    
    # 공백 확인
    if " " in v:
        return f"공백 포함"
    
    # 한글 포함 확인
    if re.search(r'[\uAC00-\uD7A3]', v):
        return f"한글 포함"
    
    # 연속된 점
    if ".." in v:
        return "연속된 점(..) 포함"
    
    # 시작/끝 점
    if local.startswith(".") or local.endswith("."):
        return f"로컬 부분 시작/끝에 점"
    
    if domain.startswith(".") or domain.endswith("."):
        return f"도메인 시작/끝에 점"
    
    # TLD 길이 체크
    tld = domain.split(".")[-1]
    if len(tld) < 2:
        return f"TLD가 너무 짧음: '{tld}'"
    
    # 전체 정규식 체크
    if not EMAIL_REGEX.match(v):
        return f"이메일 형식 불일치"
    
    return None  # 정상


def main():
    print("=" * 70)
    print("  Google Sheets company 시트 — 이메일 유효성 체크")
    print("=" * 70)
    
    # 인증
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    gc = gspread.authorize(creds)
    
    # 스프레드시트 열기
    sh = gc.open_by_key(SPREADSHEET_ID)
    
    # 시트 목록 확인
    worksheets = sh.worksheets()
    print(f"\n시트 목록: {[ws.title for ws in worksheets]}\n")
    
    # company 시트 찾기
    company_ws = None
    for ws in worksheets:
        if ws.title.lower() == "company":
            company_ws = ws
            break
    
    if not company_ws:
        print("[ERROR] 'company' 시트를 찾을 수 없습니다!")
        return
    
    print(f"✅ '{company_ws.title}' 시트 발견 (gid={company_ws.id})")
    
    # 전체 데이터 가져오기
    all_rows = company_ws.get_all_values()
    
    if not all_rows:
        print("[ERROR] 데이터가 없습니다!")
        return
    
    header = all_rows[0]
    data_rows = all_rows[1:]
    
    print(f"\n헤더 행: {header}")
    print(f"총 데이터 행 수: {len(data_rows)}행\n")
    
    # 이메일 컬럼 찾기
    email_col_idx = None
    email_col_name = None
    for i, h in enumerate(header):
        if "email" in h.lower() or "이메일" in h or "mail" in h.lower() or "e-mail" in h.lower():
            email_col_idx = i
            email_col_name = h
            break
    
    if email_col_idx is None:
        print("[ERROR] 이메일 컬럼을 찾을 수 없습니다!")
        print("헤더 확인:", header)
        return
    
    col_letter = chr(ord('A') + email_col_idx) if email_col_idx < 26 else f"Col{email_col_idx+1}"
    print(f"📧 이메일 컬럼: '{email_col_name}' ({col_letter}열, 인덱스={email_col_idx})\n")
    
    # 이메일 분석
    valid_emails = []
    invalid_emails = []
    empty_emails = []
    
    # 회사명 컬럼 찾기 (있으면)
    company_col_idx = None
    for kw in ["회사", "company", "기업", "업체", "사명", "company_name", "name"]:
        for i, h in enumerate(header):
            if kw in h.lower():
                company_col_idx = i
                break
        if company_col_idx is not None:
            break
    
    for row_num, row in enumerate(data_rows, start=2):  # 2부터 시작 (헤더=1행)
        # 이메일 값 추출
        email_val = row[email_col_idx].strip() if email_col_idx < len(row) else ""
        company_name = row[company_col_idx].strip() if (company_col_idx is not None and company_col_idx < len(row)) else "(회사명 없음)"
        
        issue = classify_email(email_val)
        
        if issue is None:
            valid_emails.append((row_num, company_name, email_val))
        elif issue == "빈값":
            empty_emails.append((row_num, company_name, email_val))
        else:
            invalid_emails.append((row_num, company_name, email_val, issue))
    
    # 결과 출력
    print("=" * 70)
    print(f"📊 분석 결과 요약")
    print("=" * 70)
    print(f"  총 데이터 행:       {len(data_rows):>5}행")
    print(f"  ✅ 정상 이메일:     {len(valid_emails):>5}개")
    print(f"  ❌ 문제 이메일:     {len(invalid_emails):>5}개")
    print(f"  ⬜ 빈값(이메일없음): {len(empty_emails):>5}개")
    print()
    
    if invalid_emails:
        print("=" * 70)
        print(f"❌ 문제 이메일 목록 ({len(invalid_emails)}건)")
        print("=" * 70)
        print(f"{'행':>4} | {'회사명':<25} | {'이메일 값':<35} | 문제 유형")
        print("-" * 100)
        for row_num, company, email, issue in invalid_emails:
            print(f"{row_num:>4} | {company:<25} | {email:<35} | {issue}")
    
    if empty_emails:
        print()
        print("=" * 70)
        print(f"⬜ 이메일 비어있는 행 ({len(empty_emails)}건)")
        print("=" * 70)
        print(f"{'행':>4} | {'회사명':<25}")
        print("-" * 35)
        for row_num, company, _ in empty_emails:
            print(f"{row_num:>4} | {company:<25}")
    
    print()
    print("=" * 70)
    print("✅ 체크 완료!")
    print("=" * 70)


if __name__ == "__main__":
    main()
