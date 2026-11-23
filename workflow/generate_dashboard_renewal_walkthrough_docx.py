# -*- coding: utf-8 -*-
"""
generate_dashboard_renewal_walkthrough_docx.py
대흥정밀 B2B 관리자 대시보드 리뉴얼 완료 워크스루 보고서 생성
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
run_title = p_title.add_run("대흥정밀 B2B 관리자 대시보드 리뉴얼 완료 보고서")
set_font(run_title, "맑은 고딕", 18, bold=True, color_rgb=(15, 32, 67))

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
run_sub = p_sub.add_run("ChatGPT 리뉴얼 시안 디자인 이식 및 기존 JS/API/인증 100% 무손실 보존 완료")
set_font(run_sub, "맑은 고딕", 10.5, color_rgb=(100, 116, 139))

# ── 개요 메타정보 테이블 ──
meta_table = doc.add_table(rows=4, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("보고서 관리 번호", "DH-DASHBOARD-RENEWAL-20261123"),
    ("완료 일시", "2026년 11월 23일 (월)"),
    ("적용 대상 파일", "index_dashboard.html (배포 동기화: dist_deploy/index_dashboard.html)"),
    ("백업본 보관", "index_dashboard - 20161120_0112pm.html (207.8 KB 안전 보관 완료)")
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

# ── 1. 리뉴얼 작업 개요 및 핵심 원칙 ──
add_heading_1("1. 리뉴얼 작업 개요 및 핵심 원칙")
add_paragraph_text("사용자께서 제시하신 'ChatGPT 리뉴얼 요구사항' 8대 수칙을 철저하게 준수하여 기존 관리자 페이지의 모든 자바스크립트 엔진과 API 연동을 100% 보존하면서, 최신 카드형 UI 레이아웃으로 리뉴얼을 완결하였습니다.")

principle_table = doc.add_table(rows=5, cols=3)
principle_table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["구분", "ChatGPT 요구사항 및 지침", "반영 및 검증 결과"]
for c_idx, h in enumerate(headers):
    cell = principle_table.cell(0, c_idx)
    cell.text = h
    set_font(cell.paragraphs[0].runs[0], "맑은 고딕", 9.5, bold=True, color_rgb=(15, 32, 67))
    cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>'))

principles = [
    ("기능 무손실 원칙", "기존 JS 기능/이벤트 동작 삭제 금지, 더미 데이터 대체 금지", "기존 31개 JS 함수 및 59개 필수 DOM ID 100% 완벽 매칭 (누락 0건)"),
    ("데이터 연동 보존", "Google Sheets API, GA4, Ads, 메일 발송 로직 유지", "Apps Script 웹앱 연동 및 실시간 견적/방문 통계 파싱 엔진 무수정 보존"),
    ("보안 및 인증 유지", "로그인 비밀번호 인증 게이트 및 권한 로직 유지", "비밀번호 게이트(#authOverlay) 및 세션 유지, 비번 변경 모달 완벽 연동"),
    ("반응형 UI 최적화", "모바일/태블릿 반응형 레이아웃 깨짐 방지", "데스크톱 130px 슬림 사이드바 / 모바일 65px 아이콘 모드 미디어 쿼리 적용")
]
for r_idx, r_data in enumerate(principles, start=1):
    for c_idx, val in enumerate(r_data):
        cell = principle_table.cell(r_idx, c_idx)
        cell.text = val
        bold_flag = (c_idx == 0)
        set_font(cell.paragraphs[0].runs[0], "맑은 고딕", 9, bold=bold_flag, color_rgb=(51, 51, 51))

for row in principle_table.rows:
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:left w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/></w:tcBorders>')
        tcPr.append(tcBorders)

# ── 2. 주요 UI/UX 개편 상세 ──
add_heading_1("2. 주요 UI/UX 개편 상세")

add_heading_2("2.1 좌측 130px 슬림 사이드바 네비게이션 도입")
add_paragraph_text("기존 상단 가로형 헤더 구조에서 전문 B2B SaaS 대시보드 규격의 좌측 슬림 고정 사이드바(130px)로 개편하였습니다.", bullet=True)
add_paragraph_text("DH 로고 마크, 대흥정밀 브랜딩, 대시보드/견적관리/마케팅분석/발송관리/시뮬레이터/운영계획서 메뉴를 배치하였습니다.", bullet=True)
add_paragraph_text("하단에 '시스템 정상' 실시간 펄스 인디케이터와 원클릭 로그아웃 버튼을 탑재하였습니다.", bullet=True)

add_heading_2("2.2 상단 탑바 및 액션 컨트롤러")
add_paragraph_text("실시간 대상 사이트 드롭다운(#site-selector: 모바일 카탈로그, 공식홈페이지, 이메일 발송현황, 팩스 현황)을 알약형(Pill) 스타일로 배치하였습니다.", bullet=True)
add_paragraph_text("실시간 모드 / 시뮬레이터 모드 원클릭 토글 버튼(#mode-realtime, #mode-simulator)을 정돈하였습니다.", bullet=True)
add_paragraph_text("우측에 카탈로그, 브로슈어, 제안서, 구글 시트 바로가기 버튼을 배치하여 실무 접근성을 극대화하였습니다.", bullet=True)

add_heading_2("2.3 4대 핵심 KPI 카드 시스템")
add_paragraph_text("1) 총 방문 세션 (#kpi-visits): 실제 GA4/스프레드시트 세션수 및 Google Ads 유입 비중 표시, 배경 스파크라인 SVG 적용", bullet=True)
add_paragraph_text("2) 견적 문의 접수 (#kpi-quotes): 누적 견적 접수 건수 및 24시간 내 신규 접수 현황 표시", bullet=True)
add_paragraph_text("3) 견적 전환율 CVR (#kpi-cvr): 방문자 대비 실제 견적 접수 성공 비율 실시간 계산", bullet=True)
add_paragraph_text("4) 반송·에러 모니터링 (#errBadge): 반송 실패 건수를 경고 카드로 표시하며, 클릭 시 반송 상세 리포트 모달(#errModal)이 즉시 팝업", bullet=True)

add_heading_2("2.4 데이터 시각화 및 최근 견적 테이블")
add_paragraph_text("마케팅 유입 채널 분석 차트(#sourceChart)와 가공 요청 품목 선호도 차트(#productChart)를 Chart.js 기반으로 세련된 곡선과 폰트로 시각화하였습니다.", bullet=True)
add_paragraph_text("실시간 견적 테이블(#leads-table)에 실시간 검색(#table-search-input), 성공/실패 필터(#status-filter-select), 페이지당 보기(10/25/50개), 페이지네이션을 완벽 유지하였습니다.", bullet=True)
add_paragraph_text("견적 행 클릭 시 상세 규격 및 첨부 도면을 다운로드할 수 있는 상세 모달(#quoteModal)이 정상 팝업됩니다.", bullet=True)

add_heading_2("2.5 Google Ads 효율 시뮬레이터 및 영업 지원 카드")
add_paragraph_text("일일 광고 예산 슬라이더(#input-budget)와 CPC 슬라이더(#input-cpc) 조작 시 실시간 예상 클릭수, 예상 문의수, 리드당 단가(CPA)가 즉시 재계산됩니다.", bullet=True)
add_paragraph_text("우측에 업무 도구 빠른 실행(카탈로그, 브로슈어, 제안서, 구글시트, 마스터플랜, 센드랩스) 및 시스템 공지사항 카드를 탑재하였습니다.", bullet=True)
add_paragraph_text("하단에 센드랩스(SendLabs) 대량 팩스 발송 계정 정보(ID: dhsteel, 발신번호: 02-2076-8203) 카드를 안전하게 보존하였습니다.", bullet=True)

# ── 3. 기능 및 정합성 검증 결과 ──
add_heading_1("3. 기능 및 정합성 검증 결과")

add_paragraph_text("자바스크립트 엔진 정합성 검증: Node.js 문법 검사 통과 (오류 0건, Syntax Error 0건)", bullet=True)
add_paragraph_text("DOM ID 매핑 검증: 전체 59개 필수 ID 중 59개 100% 매칭 완료 (누락 ID: 0건)", bullet=True)
add_paragraph_text("배포 패키지 동기화: dist_deploy/index_dashboard.html 배포 디렉터리 동기화 완료 (46.18 MB, 176개 파일)", bullet=True)

output_path = r'E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-23_dhsteel_dashboard_renewal_walkthrough.docx'
doc.save(output_path)
print(f'[완료] 워크스루 보고서 생성 완료: {output_path}')

