# -*- coding: utf-8 -*-
"""
generate_mail_plan_docx_20261123.py
2026-11-23(월) 대흥정밀 B2B 이메일 3차 정기 발송 계획 및 타겟 분석 보고서
사용자 전역 규칙 엄격 준수:
- 글꼴: 맑은 고딕 (Malgun Gothic)
- 글자 크기: 본문 10pt
- 제목: H1 14pt, H2 12pt, H3 10pt
- 테이블 스타일 및 볼드 서식 적용
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

# Normal Style
style_normal = doc.styles['Normal']
style_normal.font.name = '맑은 고딕'
style_normal.font.size = Pt(10)
style_normal.font.color.rgb = RGBColor(15, 23, 42)
style_normal.element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

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

# Title
p_title = doc.add_paragraph()
r_title = p_title.add_run("대흥정밀 B2B 이메일 3차 정기 발송 계획서 (2026-11-23)")
r_title.font.name = '맑은 고딕'
r_title.font.size = Pt(16)
r_title.font.bold = True
r_title.font.color.rgb = RGBColor(28, 43, 74)
r_title._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')

p_meta = doc.add_paragraph()
p_meta.paragraph_format.space_after = Pt(14)
r_meta = p_meta.add_run("발송일자: 2026년 11월 23일(월) | 발송 채널: Gmail API | 대상: 우량 검증 68개사 | 인프라: Cloudflare CDN 적용")
r_meta.font.name = '맑은 고딕'
r_meta.font.size = Pt(9.5)
r_meta.font.color.rgb = RGBColor(100, 116, 139)
r_meta._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), '맑은 고딕')

# 1. 발송 개요
add_h1("1. 발송 개요 및 전략적 배경")
add_p("금일(2026년 11월 23일) 집행되는 3차 정기 B2B 이메일 아웃바운드는 지난 11월 20일 완료된 Cloudflare Pages 글로벌 Anycast 인프라(https://dhsteel.pages.dev) 이전 이후 첫 번째로 진행되는 정기 발송 캠페인입니다.")
add_p(" • 발송 일시: 2026년 11월 23일 (월) 오전", bold_prefix="발송 핵심 지표:")
add_p(" • 발송 타겟: 총 68개사 (11/09 도달 성공 67개사 + 도메인 오타 정제 완료 1개사)", bold_prefix="")
add_p(" • 발송 템플릿: catalog/templates/dhsteel_proposal_v2.html (Cloudflare CDN 57개소 반영)", bold_prefix="")
add_p(" • 발송 계정: dhsteel7@gmail.com (Gmail API 연동, 3초 안전 발송)", bold_prefix="")

# 2. 타겟 정제 내역
add_h1("2. 타겟 정제 및 제외/보정 내역")
add_p("지난 11/09 메일 발송에서 발생한 3건의 이슈를 정밀 반영하여 발송 무결성을 확보하였습니다.")

tbl_refine = doc.add_table(rows=1, cols=4)
format_table(
    tbl_refine,
    [1.5, 2.0, 1.5, 1.8],
    ["업체명", "기존 상태", "정제 조치", "금일(11/23) 처리"],
    [
        ["(주)코베아", "kovea.co (오타 도메인)", "kovea@kovea.co.kr 수정", "✅ 정상 발송군 포함 (68개사)"],
        ["금경이노텍", "550 계정 삭제/부존재", "A열 N 세팅 (영구제외)", "❌ 발송 제외"],
        ["(주)아이디오", "사내 보안 메일 수신차단", "11/16 팩스 전환(수신완료)", "❌ 메일 제외 (팩스 관리)"]
    ]
)

# 3. 인프라 무결성 검증
add_h1("3. 신규 Cloudflare CDN 기반 이미지 호스팅 검증")
add_p("기존 Vercel 호스팅에서 발생할 수 있었던 이미지 엑박(Broken Image) 위험을 원천 차단하고, 수신자가 메일을 열람했을 때 초고속으로 사진이 렌더링되도록 15종 전 제품 사진을 전수 점검 완료하였습니다.")
add_p(" • 헤더 로고: https://dhsteel.pages.dev/images/logo_dhsteel.png (HTTP 200, 476 KB)", bold_prefix="호스팅 상태:")
add_p(" • 파이프 스웨이징 갤러리: https://dhsteel.pages.dev/gallery/swaging_01.jpg (HTTP 200, 106 KB)", bold_prefix="")
add_p(" • 파이프 벤딩 갤러리: https://dhsteel.pages.dev/gallery/bending_01.jpg (HTTP 200, 82 KB)", bold_prefix="")
add_p(" • 파이프 포밍 갤러리: https://dhsteel.pages.dev/gallery/forming_01.jpg (HTTP 200, 40 KB)", bold_prefix="")

# 4. 구글 시트 연동 구조
add_h1("4. 구글 스프레드시트 연동 구조")
add_p(" • 워크시트 생성: '2026-11-23' 전용 워크시트 신설 및 68개사 전체 데이터 매핑 완료")
add_p(" • 회차 세팅: M열(발송대기)을 '3차 정기(11/23)'로 일괄 지정하여 이전 회차 로그와 완벽 분리")
add_p(" • 발송 연동: 메인 'company' 시트 A열 체크박스 TRUE 동기화로 원클릭 즉시 발송 가능")

output_docx = r'E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-23_dhsteel_mail_plan_batch3.docx'
doc.save(output_docx)
print(f'[Created] Mail Plan Word Report saved to: {output_docx}')

