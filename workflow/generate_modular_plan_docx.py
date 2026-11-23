# -*- coding: utf-8 -*-
"""
generate_modular_plan_docx.py
대흥정밀 마스터 플랜 모듈화 및 Cloudflare 인프라 이전 결과 보고서 생성기
사용자 전역 규칙 엄격 준수:
- 글꼴: 맑은 고딕 (Malgun Gothic)
- 글자 크기: 본문 10pt
- 제목: H1 14pt, H2 12pt, H3 10pt
- 볼드 서식 및 테이블 깔끔한 스타일 적용
"""

import os, sys
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document()

# Page Margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Set Normal Style Font to Malgun Gothic 10pt
style_normal = doc.styles['Normal']
style_normal.font.name = '맑은 고딕'
style_normal.font.size = Pt(10)
style_normal.font.color.rgb = RGBColor(15, 23, 42)
rFonts = style_normal.element.rPr.rFonts
rFonts.set(qn('w:eastAsia'), '맑은 고딕')

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = '맑은 고딕'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(28, 43, 74)
    run._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = '맑은 고딕'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(37, 99, 235)
    run._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')
    return p

def add_p(text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = '맑은 고딕'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
        r_pre._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')
    r_text = p.add_run(text)
    r_text.font.name = '맑은 고딕'
    r_text.font.size = Pt(10)
    r_text.font.color.rgb = RGBColor(51, 65, 85)
    r_text._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')
    return p

def format_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        hdr_cells[i].width = Inches(col_widths[i])
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = '맑은 고딕'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(15, 23, 42)
            r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')
        # Shading
        shading = OxmlElement('w:shd')
        shading.set(qn('w:val'), 'clear')
        shading.set(qn('w:color'), 'auto')
        shading.set(qn('w:fill'), 'F1F5F9')
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)
        
    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            row_cells[col_idx].width = Inches(col_widths[col_idx])
            p = row_cells[col_idx].paragraphs[0]
            if col_idx in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = '맑은 고딕'
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(51, 65, 85)
                r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')

# ─────────────────────────────────────────────────────────────
# Document Title
# ─────────────────────────────────────────────────────────────
p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(4)
r_title = p_title.add_run("대흥정밀 B2B 마스터 플랜 모듈화 및 인프라 이전 완료 보고서")
r_title.font.name = '맑은 고딕'
r_title.font.size = Pt(16)
r_title.font.bold = True
r_title.font.color.rgb = RGBColor(28, 43, 74)
r_title._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')

p_meta = doc.add_paragraph()
p_meta.paragraph_format.space_after = Pt(14)
r_meta = p_meta.add_run("작성일자: 2026년 11월 20일 | 작성자: AI 시스템 총괄 | 상태: 배포 완료 및 전수 검증 통과 (100% PASS)")
r_meta.font.name = '맑은 고딕'
r_meta.font.size = Pt(9.5)
r_meta.font.color.rgb = RGBColor(100, 116, 139)
r_meta._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')

# ─────────────────────────────────────────────────────────────
# 1. 종합 개요
# ─────────────────────────────────────────────────────────────
add_h1("1. 프로젝트 개요 및 배경")
add_p("본 보고서는 대흥정밀 B2B 마케팅 및 웹 인프라를 퍼시스스토어(fursys-store)와 삼협철망(samhyup)의 성공 모델을 바탕으로 완전 모듈화하고, 기존 Vercel 환경에서 발생하던 대역폭 및 배포 제약을 극복하기 위해 Cloudflare Pages 글로벌 Anycast 인프라로 전면 이전 및 고도화한 결과를 종합 정리한 문서입니다.")

add_p(" • 이전 일시: 2026년 11월 20일 (금)", bold_prefix="주요 전환 지표:")
add_p(" • 신규 공식 서비스 URL: https://dhsteel.pages.dev (루트 접속 시 대시보드로 자동 연결)", bold_prefix="")
add_p(" • 배포 패키지 경량화: 기존 250MB+ (디버그 프로필 포함) → 46.2MB (176개 파일, dist_deploy/ 구축)", bold_prefix="")
add_p(" • 라이브 전수 검증: 메인, 대시보드, 카탈로그, 마스터플랜, 메일/팩스 리포트 및 이미지 전수 HTTP 200 통과", bold_prefix="")

# ─────────────────────────────────────────────────────────────
# 2. 마스터 플랜 5대 독립 탭(Tab) 모듈화 개편
# ─────────────────────────────────────────────────────────────
add_h1("2. 마스터 플랜 5대 독립 탭(Tab) 모듈화 개편")
add_p("퍼시스스토어 플랜(fursys-store_plan_2026.html)의 인터랙티브 탭 네비게이션을 이식하여, 배포/이메일/팩스/통합이력/SOP를 명확하게 분리함으로써 운영 효율성과 가독성을 극대화하였습니다.")

tbl_tabs = doc.add_table(rows=1, cols=3)
format_table(
    tbl_tabs,
    [1.8, 2.2, 2.8],
    ["독립 탭 명칭", "핵심 관제 영역", "주요 구성 요소 및 세부 내용"],
    [
        ["📋 1. 통합 작업 이력", "PHASE 1 ~ 18 전체 타임라인", "기초 구축부터 오늘 Phase 18(Cloudflare 전환)까지의 종합 누적 히스토리 및 체크리스트"],
        ["☁️ 2. Cloudflare 배포 매뉴얼", "인프라 이전 및 배포 가이드", "Vercel 탈피 배경, 파일명 표준화 규격, dist_deploy 빌드 스크립트, 30초 직접 업로드 절차"],
        ["📬 3. 이메일 발송 관리", "B2B 이메일 70개사 정기 발송", "Gmail API 발송 스펙, 신규 도메인 57개소 전환, 이미지 15종 CDN 호스팅, 반송 3종 정제 프로토콜"],
        ["📠 4. 팩스 발송 관리", "B2B 팩스 30개사 대량 발송", "센드랩스(SendLabs) 연동 체계, 업로드 엑셀/CSV 규격, 141건 누적 팩스 DB 및 1장 단축 제안서"],
        ["📖 5. 정기 발송 SOP", "월/목 주간 로테이션 표준절차", "타겟 선별(D-1) → 사전 인프라 점검 → 발송 집행 → 사후 정제 및 보고서 4단계 프로세스"]
    ]
)

# ─────────────────────────────────────────────────────────────
# 3. Cloudflare Pages 인프라 이전 및 최적화
# ─────────────────────────────────────────────────────────────
add_h1("3. Cloudflare Pages 인프라 이전 및 최적화 상세")
add_h2("가. 파일명 표준화 및 라우팅 체계 구축")
add_p(" • index_dashboard.html: 기존 dashboard.html에서 표준화하여 삼협/퍼시스와 동일한 관리자 규격 적용")
add_p(" • catalog/index_catalog.html: 기존 catalog/index.html의 모바일 카탈로그 파일명 표준화")
add_p(" • index.html & _redirects: 루트(/) 접속 시 /index_dashboard.html로 200 Rewrite 및 /gallery/*, /images/* CDN 서빙 라우팅 완비")

add_h2("나. 대시보드 UI 삼협철망 스타일 고도화")
add_p(" • 관리자 인증 모달 심볼 교체: 임시 텍스트 'D'를 제거하고 대흥정밀 공식 CI 로고(logo.png)로 교체")
add_p(" • 모달 내 카탈로그 바로가기: [📱 모바일 카탈로그], [📄 기업 제안서] 바로가기 2개 버튼 신설")
add_p(" • 대시보드 상단 퀵 버튼: 헤더 영역에 [📱 카탈로그 ↗], [📄 브로슈어 ↗] 캡슐 버튼 탑재")
add_p(" • 에러 리포트 버튼 시각적 안정화: 강렬한 붉은색을 차분하고 신뢰감 있는 다크 네이비(#1C2B4A)로 톤앤매너 개선")

# ─────────────────────────────────────────────────────────────
# 4. B2B 이메일 발송 시스템 도메인 전환 (57개소)
# ─────────────────────────────────────────────────────────────
add_h1("4. B2B 이메일 발송 도메인 전수 전환 내역")
add_p("메일 본문에 포함된 모든 이미지 호스팅 URL과 카탈로그 연결 링크를 신규 Cloudflare 도메인(https://dhsteel.pages.dev)으로 일괄 전환하여 수신 고객의 엑박(Broken Image) 발생을 완벽 차단하였습니다.")

tbl_mail = doc.add_table(rows=1, cols=3)
format_table(
    tbl_mail,
    [2.8, 1.2, 2.8],
    ["대상 파일 및 템플릿", "치환 건수", "반영 내용"],
    [
        ["catalog/templates/dhsteel_proposal_v2.html", "17건", "헤더 로고, 스웨이징/벤딩/포밍 15종 사진, 카탈로그 링크"],
        ["catalog/templates/dhsteel_proposal.html", "29건", "표준 HTML 제안서 내 모든 이미지 및 버튼 경로"],
        ["google_apps_script_outbound.js", "2건", "BASE_URL = 'https://dhsteel.pages.dev/' 갱신"],
        ["catalog/templates/dhsteel_proposal_preview.html", "2건", "제안서 미리보기 연동 절대 경로 갱신"],
        ["catalog/templates/dhsteel_blog_post.html 외", "7건", "블로그 시안 및 제안서 미리보기 파일 경로 갱신"]
    ]
)

# ─────────────────────────────────────────────────────────────
# 5. 라이브 배포 전수 검증 결과 (100% 통과)
# ─────────────────────────────────────────────────────────────
add_h1("5. 라이브 배포 전수 검증 결과 (100% 통과)")
add_p("Cloudflare Pages 배포 완료 직후, 파이썬 기반 자동 검증 스크립트를 통해 전체 서비스 엔드포인트의 HTTP 응답 상태 및 자산 서빙 무결성을 전수 확인하였습니다.")

tbl_test = doc.add_table(rows=1, cols=4)
format_table(
    tbl_test,
    [2.4, 1.0, 1.4, 2.0],
    ["검증 대상 URL", "응답 코드", "파일 크기", "검증 판정"],
    [
        ["https://dhsteel.pages.dev/", "HTTP 200", "207 KB", "✅ PASS (대시보드 리다이렉트)"],
        ["https://dhsteel.pages.dev/index_dashboard", "HTTP 200", "207 KB", "✅ PASS (대시보드 UI 정상)"],
        ["https://dhsteel.pages.dev/catalog/index_catalog.html", "HTTP 200", "48 KB", "✅ PASS (모바일 카탈로그 서빙)"],
        ["https://dhsteel.pages.dev/images/logo_dhsteel.png", "HTTP 200", "476 KB", "✅ PASS (메일 로고 CDN 호스팅)"],
        ["https://dhsteel.pages.dev/gallery/swaging_01.jpg", "HTTP 200", "106 KB", "✅ PASS (스웨이징 사진 CDN 호스팅)"],
        ["https://dhsteel.pages.dev/gallery/bending_01.jpg", "HTTP 200", "82 KB", "✅ PASS (벤딩 사진 CDN 호스팅)"],
        ["https://dhsteel.pages.dev/gallery/forming_01.jpg", "HTTP 200", "40 KB", "✅ PASS (포밍 사진 CDN 호스팅)"],
        ["https://dhsteel.pages.dev/plan/dhsteel_plan_2026.html", "HTTP 200", "102 KB", "✅ PASS (모듈화 마스터플랜 서빙)"]
    ]
)

# Save Document
output_docx = r'E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-20_dhsteel_modular_plan_report.docx'
doc.save(output_docx)
print(f'[Created] Word Report saved to: {output_docx}')

