# -*- coding: utf-8 -*-
import os, sys, datetime
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

doc = docx.Document()

# Page Margins
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

def style_table(table, col_widths, headers, data_rows):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_font(p.runs[0], "맑은 고딕", 10, bold=True, color_rgb=(255, 255, 255))
        shading = parse_xml(r'<w:shd {} w:fill="1E3A8A"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)

    for r_idx, row_data in enumerate(data_rows):
        row_cells = table.add_row().cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            p = row_cells[c_idx].paragraphs[0]
            if c_idx in (0, 1) or "%" in str(val) or "~" in str(val):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_font(p.runs[0], "맑은 고딕", 10, bold=(r_idx == len(data_rows)-1 and "합계" in row_data[0]), color_rgb=(51, 51, 51))
            shading = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), bg_color))
            row_cells[c_idx]._tc.get_or_add_tcPr().append(shading)

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

# Document Title
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(4)
run_title = p_title.add_run("대흥정밀 11월 월요일 정기 아웃바운드 로드맵 & 11/09 발송 계획서")
set_font(run_title, "맑은 고딕", 16, bold=True, color_rgb=(15, 32, 67))

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
run_sub = p_sub.add_run("기준일자: 2026-11-09 (월) | 전용 발송 시트: '2026-11-09' (검증 70개사 세팅)")
set_font(run_sub, "맑은 고딕", 10, color_rgb=(100, 116, 139))

# Section 1
add_heading_1("1. 11월 4주간 월요일 정기 로테이션 확정 스케줄")
add_paragraph_text("대흥정밀 B2B 영업 마케팅의 피로도를 최소화하고 전환율을 극대화하기 위해 매주 월요일 채널(메일/팩스) 및 타겟군(검증군/신규군)을 교차 운영하는 11월 종합 로드맵을 확정하였습니다.")

r_headers = ["일정", "요일", "영업 채널", "대상 타겟군", "예상 규모", "운영 목적 및 세부 내용"]
r_widths = [Inches(1.0), Inches(0.6), Inches(1.1), Inches(1.3), Inches(0.9), Inches(2.3)]
r_rows = [
    ["11월 09일", "월", "📧 이메일", "기존 검증 성공업체", "70개사", "2차 정기 후속 메일 발송 (시트: 2026-11-09)"],
    ["11월 16일", "월", "📠 팩스", "기존 검증 성공업체", "30개사", "11/02 성공 22건 포함 유효 팩스 재발송 (샌드랩스)"],
    ["11월 23일", "월", "🔄 복합", "신규 크롤링 + 기존 재검증", "50~70개사", "지침서 기준 전국 20개 산업 지역 신규 수집 + 기존 미응답 보정"],
    ["11월 30일", "월", "📧+📠", "신규 + 검증 복합 타겟", "100개사+", "11월 총결산 하이브리드 대량 아웃바운드 전개"]
]
t1 = doc.add_table(rows=1, cols=len(r_headers))
style_table(t1, r_widths, r_headers, r_rows)

# Section 2
add_heading_1("2. 오늘(11/09) 발송 대상 '2026-11-09' 시트 구축 현황")
add_paragraph_text("과거 발송 이력에서 정상 수신이 검증된 70개사만을 엄선하여 별도의 '2026-11-09' 전용 시트를 생성하였습니다.", bullet=True)
add_paragraph_text("모든 행(70행)의 A열(발송 체크박스)을 'TRUE'로 일괄 설정하고, M열(발송대기/회차)을 '2차 정기(11/09)'로 자동 세팅 완료하였습니다.", bullet=True)
add_paragraph_text("발송 후 결과는 기존 mail_log에 동일하게 실시간 기록되어 schedule 대시보드에 자동으로 누적 반영됩니다.", bullet=True)

# Section 3
add_heading_1("3. 발송 집행 방법 (원클릭 가이드)")
add_paragraph_text("1. 구글 스프레드시트에서 새로 생성된 [2026-11-09] 시트를 확인합니다.")
add_paragraph_text("2. 상단 맞춤 메뉴 [대흥 아웃바운드] → [📧 대흥정밀 메일 일괄 발송]을 클릭하면 세팅된 70개사에 즉시 발송이 개시됩니다.")
add_paragraph_text("3. 발송 완료 후 schedule 시트에서 주간/월간 수치가 자동 갱신됩니다.")

out_docx = r"E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-09_dhsteel_november_roadmap.docx"
doc.save(out_docx)
print(f"Roadmap report saved to {out_docx}")

