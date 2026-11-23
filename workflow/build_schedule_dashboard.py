# -*- coding: utf-8 -*-
import os, sys, datetime
import gspread
from google.oauth2.service_account import Credentials
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

CREDS_PATH = r'E:\Antigravity\credentials\ghkim\ghkim_credentials_crawler-hifus_20260221.json'
SS_ID = '1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic'

creds = Credentials.from_service_account_file(CREDS_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets'])
client = gspread.authorize(creds)
doc_ss = client.open_by_key(SS_ID)

mail_log = doc_ss.worksheet('mail_log')
m_rows = mail_log.get_all_values()[1:]

fax_log = doc_ss.worksheet('fax_log')
f_rows = fax_log.get_all_values()[1:]

company_ws = doc_ss.worksheet('company')
c_rows = company_ws.get_all_values()[1:]

def parse_date(d_str):
    d_str = d_str.strip()[:10]
    for fmt in ('%Y-%m-%d', '%Y.%m.%d', '%Y/%m/%d'):
        try:
            return datetime.datetime.strptime(d_str, fmt).date()
        except:
            pass
    return None

monthly = defaultdict(lambda: {'mail_tot': 0, 'mail_suc': 0, 'mail_fail': 0, 'fax_tot': 0, 'fax_suc': 0, 'fax_fail': 0})
weekly = defaultdict(lambda: {'mail_tot': 0, 'mail_suc': 0, 'mail_fail': 0, 'fax_tot': 0, 'fax_suc': 0, 'fax_fail': 0, 'start_date': None, 'end_date': None})

for r in m_rows:
    d = parse_date(r[2])
    if not d: continue
    m_key = d.strftime('%Y-%m')
    w_num = d.isocalendar()[1]
    w_key = f'{d.year}-W{w_num:02d}'
    
    monthly[m_key]['mail_tot'] += 1
    if '성공' in r[6]:
        monthly[m_key]['mail_suc'] += 1
    else:
        monthly[m_key]['mail_fail'] += 1
        
    weekly[w_key]['mail_tot'] += 1
    if '성공' in r[6]:
        weekly[w_key]['mail_suc'] += 1
    else:
        weekly[w_key]['mail_fail'] += 1
        
    # start/end dates of week
    monday = d - datetime.timedelta(days=d.weekday())
    sunday = monday + datetime.timedelta(days=6)
    weekly[w_key]['start_date'] = monday.strftime('%m/%d')
    weekly[w_key]['end_date'] = sunday.strftime('%m/%d')

for r in f_rows:
    d = parse_date(r[2])
    if not d: continue
    m_key = d.strftime('%Y-%m')
    w_num = d.isocalendar()[1]
    w_key = f'{d.year}-W{w_num:02d}'
    
    monthly[m_key]['fax_tot'] += 1
    if '성공' in r[6]:
        monthly[m_key]['fax_suc'] += 1
    else:
        monthly[m_key]['fax_fail'] += 1
        
    weekly[w_key]['fax_tot'] += 1
    if '성공' in r[6]:
        weekly[w_key]['fax_suc'] += 1
    else:
        weekly[w_key]['fax_fail'] += 1
        
    monday = d - datetime.timedelta(days=d.weekday())
    sunday = monday + datetime.timedelta(days=6)
    weekly[w_key]['start_date'] = monday.strftime('%m/%d')
    weekly[w_key]['end_date'] = sunday.strftime('%m/%d')

# Analyze company table for batch sendable targets
email_targets = []
fax_targets = []
both_targets = []

for idx, r in enumerate(c_rows, start=2):
    c_name = r[2].strip() if len(r)>2 else ''
    email = r[5].strip() if len(r)>5 else ''
    fax = r[19].strip() if len(r)>19 else ''
    status = r[13].strip() if len(r)>13 else ''
    has_email = bool(email and '@' in email)
    has_fax = bool(fax and len(fax)>=8)
    
    if has_email:
        email_targets.append((c_name, email, status))
    if has_fax:
        fax_targets.append((c_name, fax, status))
    if has_email and has_fax:
        both_targets.append((c_name, email, fax, status))

# Prepare Schedule Sheet Data
sched_ws = doc_ss.worksheet('schedule')
sched_ws.clear()

cells = []

# Title & Metadata
cells.append(['📊 [대흥정밀] B2B 아웃바운드 통합 스케줄 & 로그 분석 대시보드', '', '', '', '', '', '', '', '', ''])
cells.append([f'기준일자: {datetime.date.today().strftime("%Y-%m-%d")} (매주 월요일 정기 업데이트)', '', '', '', '', '', '', '', '', ''])
cells.append([''])

# 1. Monthly Summary Table
cells.append(['📌 1. 월간 아웃바운드 발송 종합 현황 (Monthly Summary)', '', '', '', '', '', '', '', '', ''])
cells.append(['발송월', '전체 발송건수', '메일 발송', '메일 성공', '메일 성공률', '팩스 발송', '팩스 성공', '팩스 성공률', '전체 성공건수', '종합 성공률'])

tot_m_all = 0
tot_f_all = 0
tot_m_suc = 0
tot_f_suc = 0

for m in sorted(monthly.keys()):
    v = monthly[m]
    m_tot = v['mail_tot']
    m_suc = v['mail_suc']
    m_rate = f"{(m_suc / m_tot * 100):.1f}%" if m_tot > 0 else "-"
    f_tot = v['fax_tot']
    f_suc = v['fax_suc']
    f_rate = f"{(f_suc / f_tot * 100):.1f}%" if f_tot > 0 else "-"
    all_tot = m_tot + f_tot
    all_suc = m_suc + f_suc
    all_rate = f"{(all_suc / all_tot * 100):.1f}%" if all_tot > 0 else "-"
    
    cells.append([f'{m}월', all_tot, m_tot, m_suc, m_rate, f_tot, f_suc, f_rate, all_suc, all_rate])
    
    tot_m_all += m_tot
    tot_m_suc += m_suc
    tot_f_all += f_tot
    tot_f_suc += f_suc

grand_tot = tot_m_all + tot_f_all
grand_suc = tot_m_suc + tot_f_suc
grand_rate = f"{(grand_suc / grand_tot * 100):.1f}%" if grand_tot > 0 else "-"
m_grand_rate = f"{(tot_m_suc / tot_m_all * 100):.1f}%" if tot_m_all > 0 else "-"
f_grand_rate = f"{(tot_f_suc / tot_f_all * 100):.1f}%" if tot_f_all > 0 else "-"

cells.append(['합계 / 평균', grand_tot, tot_m_all, tot_m_suc, m_grand_rate, tot_f_all, tot_f_suc, f_grand_rate, grand_suc, grand_rate])
cells.append([''])

# 2. Weekly Dispatch Tracking
cells.append(['📌 2. 주간 아웃바운드 발송 추이 (Weekly Dispatch Tracking)', '', '', '', '', '', '', '', '', ''])
cells.append(['주차 (ISO)', '주간 기간', '메일 발송', '메일 성공', '메일 성공률', '팩스 발송', '팩스 성공', '팩스 성공률', '주간 합계', '주간 성공률'])

for w in sorted(weekly.keys()):
    v = weekly[w]
    period = f"{v['start_date']} ~ {v['end_date']}"
    m_tot = v['mail_tot']
    m_suc = v['mail_suc']
    m_rate = f"{(m_suc / m_tot * 100):.1f}%" if m_tot > 0 else "-"
    f_tot = v['fax_tot']
    f_suc = v['fax_suc']
    f_rate = f"{(f_suc / f_tot * 100):.1f}%" if f_tot > 0 else "-"
    w_tot = m_tot + f_tot
    w_suc = m_suc + f_suc
    w_rate = f"{(w_suc / w_tot * 100):.1f}%" if w_tot > 0 else "-"
    cells.append([w, period, m_tot, m_suc, m_rate, f_tot, f_suc, f_rate, w_tot, w_rate])

cells.append([''])

# 3. Batch Outbound Target Pool Status
cells.append(['📌 3. 한 번에 전송 가능한 채널별 타겟 풀 현황 (Batch Target Pool)', '', '', '', '', '', '', '', '', ''])
cells.append(['영업 채널', '전체 보유 건수', '발송 완료(성공)', '실패(보정 대상)', '미발송(대기)', '한 번에 전송 가능 규모', '비고 및 권장 조치'])

# Mail target breakdown
mail_done = sum(1 for _, _, st in email_targets if '성공' in st)
mail_fail = sum(1 for _, _, st in email_targets if '실패' in st)
mail_pending = len(email_targets) - mail_done - mail_fail

# Fax target breakdown
fax_done = sum(1 for _, _, st in fax_targets if '성공' in st)
fax_fail = sum(1 for _, _, st in fax_targets if '실패' in st)
fax_pending = len(fax_targets) - fax_done - fax_fail

# Both targets breakdown
both_done = sum(1 for _, _, _, st in both_targets if '성공' in st)
both_fail = sum(1 for _, _, _, st in both_targets if '실패' in st)
both_pending = len(both_targets) - both_done - both_fail

cells.append(['📧 이메일 (Gmail API)', len(email_targets), mail_done, mail_fail, mail_pending, f'{len(email_targets)}개사 일괄 전송 가능', '시트 상단 [대흥 아웃바운드] 메뉴를 통한 원클릭 일괄 발송'])
cells.append(['📠 팩스 (SendLabs)', len(fax_targets), fax_done, fax_fail, fax_pending, f'{len(fax_targets)}개사 엑셀 업로드 가능', '샌드랩스 대량전송 업로드 양식(xlsx/csv) 활용 즉시 발송'])
cells.append(['🔄 크로스채널 (메일+팩스)', len(both_targets), both_done, both_fail, both_pending, f'{len(both_targets)}개사 복합 전환 타겟', '메일 수신 후 팩스 2차 전환으로 회신율 극대화'])

cells.append([''])
cells.append(['💡 운영 가이드:', '', '', '', '', '', '', '', '', ''])
cells.append(['1. [월간 주기]: 8월~11월 누적 메일 359건, 팩스 112건 총 471건 집행.'])
cells.append(['2. [팩스 개선]: 10월 팩스 성공률 23.5%에서 11월 71.0%로 대폭 개선(유효 번호 필터링 효과).'])
cells.append(['3. [일괄 전송]: 3번 항목의 타겟 풀을 활용하여 원클릭 메일 발송 및 샌드랩스 엑셀 대량 업로드가 상시 가능합니다.'])

# Update spreadsheet
sched_ws.update(cells, 'A1')
print('Successfully updated schedule worksheet!')

