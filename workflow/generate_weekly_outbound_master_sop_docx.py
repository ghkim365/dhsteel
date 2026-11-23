# -*- coding: utf-8 -*-
"""
generate_weekly_outbound_master_sop_docx.py
대흥정밀 B2B 주간 발송 실무 매뉴얼 (메일·반송스캔·팩스) 공식 워드 문서 생성
규칙 준수: 맑은 고딕, 본문 10pt, H1 14pt, H2 12pt, H3 10pt
"""

import os, sys, datetime
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document()

# 마진 0.8인치 설정
for sec in doc.sections:
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.8)
    sec.right_margin = Inches(0.8)

def set_font(run, font_name="맑은 고딕", size_pt=10, bold=False, color_rgb=(51, 51, 51)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    rPr.append(rFonts)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_font(run, "맑은 고딕", 14, bold=True, color_rgb=(15, 32, 67))
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    set_font(run, "맑은 고딕", 12, bold=True, color_rgb=(30, 58, 138))
    return p

def add_heading_3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    set_font(run, "맑은 고딕", 10, bold=True, color_rgb=(31, 41, 55))
    return p

def add_paragraph_text(text, bold=False, bullet=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    if bullet:
        p.paragraph_format.left_indent = Inches(0.2)
        run_bullet = p.add_run("• ")
        set_font(run_bullet, "맑은 고딕", 10, bold=True, color_rgb=(30, 58, 138))
    run = p.add_run(text)
    set_font(run, "맑은 고딕", 10, bold=bold, color_rgb=(51, 51, 51))
    return p

# ── 문서 헤더 / 타이틀 ──
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(4)
run_title = p_title.add_run("대흥정밀 B2B 주간 아웃바운드 통합 실무 매뉴얼")
set_font(run_title, "맑은 고딕", 18, bold=True, color_rgb=(15, 32, 67))

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
run_sub = p_sub.add_run("월요 정기 이메일 발송 · 반송 메일 무인 자동 스캔 · 목요 센드랩스 팩스 발송 및 실패 전환 SOP")
set_font(run_sub, "맑은 고딕", 10.5, color_rgb=(100, 116, 139))

# ── 개요 메타정보 테이블 ──
meta_table = doc.add_table(rows=4, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("문서 관리 번호", "DH-SOP-2026-OUTBOUND-01"),
    ("최종 개정 일자", "2026년 11월 23일 (월)"),
    ("적용 대상 시스템", "구글 스프레드시트 (Apps Script), Gmail API, 센드랩스(SendLabs) 팩스 엔진"),
    ("발송 전용 계정", "dhsteel7@gmail.com (OAuth 2.0 연동 및 트리거 바인딩)")
]
for idx, (k, v) in enumerate(meta_data):
    cell_k = meta_table.cell(idx, 0)
    cell_v = meta_table.cell(idx, 1)
    cell_k.text = k
    cell_v.text = v
    cell_k.width = Inches(1.8)
    cell_v.width = Inches(5.0)
    set_font(cell_k.paragraphs[0].runs[0], "맑은 고딕", 9.5, bold=True, color_rgb=(30, 58, 138))
    set_font(cell_v.paragraphs[0].runs[0], "맑은 고딕", 9.5, color_rgb=(51, 51, 51))
    cell_k._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>'))
    for cell in (cell_k, cell_v):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m in ['top', 'bottom', 'left', 'right']:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), '120' if m in ['top', 'bottom'] else '160')
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

# ── 1. 주간 업무 타임라인 요약 ──
add_heading_1("1. 주간 B2B 아웃바운드 업무 타임라인 (Weekly Schedule)")
add_paragraph_text("대흥정밀 B2B 마케팅은 전국 500개사 파이프/철물/가구 제조 실수요처를 대상으로 매주 월요일과 목요일에 걸쳐 이메일과 팩스를 유기적으로 교차 발송하는 하이브리드 아웃바운드 체계로 운영됩니다.")

sched_table = doc.add_table(rows=5, cols=4)
sched_table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["단계 / 일정", "업무 항목", "실행 채널 및 도구", "핵심 산출물 및 후속 조치"]
for c_idx, h in enumerate(headers):
    cell = sched_table.cell(0, c_idx)
    cell.text = h
    set_font(cell.paragraphs[0].runs[0], "맑은 고딕", 9.5, bold=True, color_rgb=(15, 32, 67))
    cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>'))

sched_rows = [
    ("1단계 | 월 10:00", "정기 이메일 발송 (70건)", "구글 스프레드시트 + Gmail API", "company 및 mail_log 자동 기록, A열 체크 자동 해제"),
    ("2단계 | 월~화 상시", "반송 메일 자동 감지", "백그라운드 트리거 (매 1시간)", "반송 사유 자동 분류(5대 유형), 팩스 전환 대상 자동 선별"),
    ("3단계 | 목 14:00", "정기 팩스 발송 (30건)", "센드랩스(SendLabs) 대량 팩스", "우량 팩스사 + 메일 실패사 흡수, A4 단축 제안서 전송"),
    ("4단계 | 목 16:00", "주간 성과 통합 마감", "Antigravity 에이전트 연계", "schedule 시트 갱신, 주간 결과보고서(.docx) 자동 발행")
]
for r_idx, r_data in enumerate(sched_rows, start=1):
    for c_idx, val in enumerate(r_data):
        cell = sched_table.cell(r_idx, c_idx)
        cell.text = val
        bold_flag = (c_idx == 0 or c_idx == 1)
        set_font(cell.paragraphs[0].runs[0], "맑은 고딕", 9, bold=bold_flag, color_rgb=(51, 51, 51))

for row in sched_table.rows:
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/></w:tcBorders>')
        tcPr.append(tcBorders)

# ── 2. 이메일 발송 실무 프로세스 ──
add_heading_1("2. 파트 1: 주간 이메일 발송 실무 프로세스 (매주 월요일)")
add_heading_2("2.1 사전 점검 (체크박스 불리언 타입 필수)")
add_paragraph_text("스프레드시트 company 및 주차별 전용 시트에서 A열(체크)의 데이터 형식을 반드시 점검해야 합니다.", bullet=True)
add_paragraph_text("치명적 주의: A열 셀에 문자열 'TRUE'가 들어가면 스크립트 코드(values[r][0] !== true)의 엄격 일치 검사에 걸려 발송 대상에서 제외(스킵)됩니다.", bullet=True)
add_paragraph_text("반드시 데이터 유효성 검사(BOOLEAN)가 적용된 실제 상호작용 가능한 네모 체크박스(☑ True) 형태여야 정상 발송됩니다.", bullet=True)

add_heading_2("2.2 발송 전용 계정 로그인 확인")
add_paragraph_text("Gmail API 발송 프로그램은 스프레드시트를 열고 있는 브라우저의 구글 계정 권한으로 발송됩니다.", bullet=True)
add_paragraph_text("반드시 발송 공식 계정인 'dhsteel7@gmail.com'으로 로그인되어 있는지 크롬 상단 프로필을 확인합니다.", bullet=True)

add_heading_2("2.3 원클릭 발송 실행")
add_paragraph_text("1) 스프레드시트 상단 메뉴바에서 [대흥 아웃바운드] 메뉴를 클릭합니다.", bullet=True)
add_paragraph_text("2) [선택 제안서 발송 (v1/v2 자동분기)]를 클릭합니다.", bullet=True)
add_paragraph_text("3) 프로그램이 이전 발송 성공 이력을 자동 판별하여 신규 제안서(v1) 또는 정기 리마인드(v2) 맞춤 HTML을 자동 분기 전송합니다.", bullet=True)
add_paragraph_text("4) '발송 완료: 성공 N건 / 실패 0건' 팝업창을 확인하고 [확인]을 누릅니다.", bullet=True)

add_heading_2("2.4 사후 자동 기록 확인")
add_paragraph_text("company 시트: 발송 완료된 행의 A열 체크가 자동 해제(False)되며, N열(성공), O열(일시), P열(결과)이 즉시 갱신됩니다.", bullet=True)
add_paragraph_text("mail_log 시트: 맨 하단에 신규 발송 이력 N건이 누적되어 보관됩니다.", bullet=True)

# ── 3. 반송 메일 감지 및 스캔 프로세스 ──
add_heading_1("3. 파트 2: 반송 메일 감지 & 스캔 프로세스 (수동 캡처 완전 배제)")
add_paragraph_text("더 이상 사용자가 보낸메일함이나 받은편지함을 수동으로 확인하고 캡처해서 전달할 필요가 없습니다. 스프레드시트에 내장된 반송 자동 파싱 엔진이 100% 무인 처리합니다.")

add_heading_2("3.1 두 가지 반송 감지 모드")
add_paragraph_text("1) [상시 무인 감지 (권장)]: 메뉴에서 [⏰ 자동 스캔 트리거 설치 (1회)]를 최초 1회만 등록해 두면, 구글 클라우드 서버가 매 1시간마다 Gmail 수신함을 자동 조회하여 반송 발생 시 즉시 실패 처리 및 대표님 네이버 메일로 요약 통보합니다.", bullet=True)
add_paragraph_text("2) [즉시 수동 확인]: 발송 직후 실시간으로 반송 여부를 즉시 확인하고 싶다면, 메뉴에서 [📧 반송 메일 지금 스캔]을 클릭하면 캡처 없이 원클릭으로 실시간 정밀 스캔이 완료됩니다.", bullet=True)

add_heading_2("3.2 5대 반송 에러 유형 및 자동 분류 체계")
add_paragraph_text("시스템은 반송 알림 메일(Mailer-Daemon)의 프로토콜 오류 코드를 분석하여 아래 5대 유형으로 자동 분류합니다:")

err_table = doc.add_table(rows=6, cols=3)
err_table.alignment = WD_TABLE_ALIGNMENT.CENTER
err_headers = ["에러 분류", "프로토콜 감지 키워드", "후속 조치 방안"]
for c_idx, h in enumerate(err_headers):
    cell = err_table.cell(0, c_idx)
    cell.text = h
    set_font(cell.paragraphs[0].runs[0], "맑은 고딕", 9.5, bold=True, color_rgb=(15, 32, 67))
    cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>'))

err_data = [
    ("수신자 없음 (주소 오류)", "550 No such user, invalid address", "즉시 목요일 팩스 발송군으로 자동 전환 흡수"),
    ("도메인 없음", "No MX, Domain not found", "영구 제외 처리 또는 신규 사업자 팩스번호 조회"),
    ("메일함 용량 초과", "Mailbox full, Over quota", "차주 1회 재발송 시도 후 미수신 시 팩스 전환"),
    ("스팸/차단 거부", "554 Blocked, Rejected, Spam", "사내 보안 게이트웨이 차단이므로 팩스 발송군으로 우선 전환"),
    ("일시적 오류", "Connection refused, Timeout", "상대 서버 일시 점검이므로 차주 정상 재발송 유지")
]
for r_idx, r_data in enumerate(err_data, start=1):
    for c_idx, val in enumerate(r_data):
        cell = err_table.cell(r_idx, c_idx)
        cell.text = val
        bold_flag = (c_idx == 0)
        set_font(cell.paragraphs[0].runs[0], "맑은 고딕", 9, bold=bold_flag, color_rgb=(51, 51, 51))

for row in err_table.rows:
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/></w:tcBorders>')
        tcPr.append(tcBorders)

add_heading_2("3.3 계정 바인딩 핵심 원칙 (중요)")
add_paragraph_text("구글 보안 정책상 프로그램은 트리거를 설치한 바로 그 구글 계정의 메일함만 조회할 수 있습니다.", bullet=True)
add_paragraph_text("반드시 발송과 시트 관리는 공식 계정(dhsteel7@gmail.com) 하나로만 로그인하여 사용해야 합니다.", bullet=True)
add_paragraph_text("계정 변경 시에는 새 계정으로 로그인 후 [⏰ 자동 스캔 트리거 설치 (1회)]를 다시 실행하면 감시 계정이 즉시 변경됩니다.", bullet=True)

# ── 4. 팩스 발송 및 메일 실패 전환 프로세스 ──
add_heading_1("4. 파트 3: 주간 팩스 발송 & 메일 실패 전환 프로세스 (매주 목요일)")
add_heading_2("4.1 타겟 선정 및 하이브리드 연동")
add_paragraph_text("대흥정밀 팩스 발송은 매주 목요일 오후 14:00에 30개사를 대상으로 집행됩니다.", bullet=True)
add_paragraph_text("핵심 타겟 (20~22개사): 파이프 클램프, 조인트, 농가용/가구용 밴딩 가공 실수요처 중 팩스 선호 제조기업", bullet=True)
add_paragraph_text("전환 타겟 (8~10개사): 월요일 이메일 발송에서 반송(수신자 없음) 및 기업 차단으로 확인된 업체를 팩스로 즉시 전환하여 협력 제안서 도달률을 100%로 보정 (예: 아이디오, 대명기업 등 실전 성공 사례)", bullet=True)

add_heading_2("4.2 발송 플랫폼 및 규격")
add_paragraph_text("발송 엔진: 센드랩스 (https://www.sendlabs.co.kr) 대량 전송 엔진", bullet=True)
add_paragraph_text("발송 문서: sales/대흥정밀_파이프임가공_팩스전용_단축제안서.pdf (A4 1장 가독성 최적화, 흑백 명암비 보정)", bullet=True)

add_heading_2("4.3 목요일 팩스 실무 4단계")
add_paragraph_text("1) 명단 추출: company 시트에서 팩스 대상사 30개사 번호(D열) 확인", bullet=True)
add_paragraph_text("2) 센드랩스 로그인: 잔여 전송 캐시(30건분) 확인", bullet=True)
add_paragraph_text("3) 제안서 PDF 업로드 및 일괄 전송 클릭", bullet=True)
add_paragraph_text("4) 결과 반영: fax_log 시트에 전송 결과 기록 및 company 시트 N열을 '팩스 성공'으로 갱신", bullet=True)

# ── 5. 에이전트 연계 후속 마감 ──
add_heading_1("5. 파트 4: 에이전트 연계 후속 마감 및 통합 대시보드 SOP")
add_paragraph_text("발송 작업 후 사용자는 복잡한 수기 정리 없이 Antigravity 에이전트에게 간편하게 전달합니다.")
add_paragraph_text("1) 사용자: 채팅창에 '오늘 발송 완료했어. 로그 정리하고 주간 보고서 작성해줘' 라고 전달", bullet=True)
add_paragraph_text("2) 에이전트: mail_log 및 fax_log 실시간 검증 -> schedule 시트 동기화 -> 표준 워드 보고서(.docx) 자동 생성 및 링크 제공 -> 마스터 플랜 및 dist_deploy 패키지 최신화", bullet=True)

output_path = r'E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-23_dhsteel_weekly_outbound_master_sop.docx'
doc.save(output_path)
print(f'[완료] 워드 매뉴얼 생성 완료: {output_path}')

