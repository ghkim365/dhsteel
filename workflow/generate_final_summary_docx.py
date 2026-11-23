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

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(4)
run_title = p_title.add_run("대흥정밀 B2B 아웃바운드 정기 로테이션 최종 업무 완료 보고서")
set_font(run_title, "맑은 고딕", 16, bold=True, color_rgb=(15, 32, 67))

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
run_sub = p_sub.add_run("기준일자: 2026-11-09 (월) | 작성자: AI Coding Assistant (Antigravity)")
set_font(run_sub, "맑은 고딕", 10, color_rgb=(100, 116, 139))

add_heading_1("1. 오늘(11/09) 주요 업무 집행 총괄")
add_paragraph_text("대흥정밀 B2B 정기 로테이션 일정에 맞추어 통합 로그 분석, 대시보드 구축, 70개사 일괄 메일 발송 및 반송 데이터 실시간 보정까지 전 과정을 원스톱으로 집행 완료하였습니다.")
add_paragraph_text("schedule 시트 대시보드 구축: 월간/주간/배치풀 3대 영역 자동 집계 반영", bullet=True)
add_paragraph_text("2026-11-09 전용 발송 시트 생성: 검증 70개사 A열 체크/M열 '2차 정기' 세팅", bullet=True)
add_paragraph_text("Gmail API 일괄 발송 완료: 70개사 전량 발송 집행", bullet=True)
add_paragraph_text("반송 3건 실시간 분석 및 보정: 코베아 도메인 오타 수정, 금경이노텍 실패 처리, 아이디오 팩스 전환", bullet=True)
add_paragraph_text("최종 성과 일치 완료: 실도달 성공 67건 (95.7%) / 실패 3건 (4.3%) 전수 동기화", bullet=True)

add_heading_1("2. 11월 4주간 확정 로드맵 및 차주(11/16) 준비 현황")
r_headers = ["일정", "요일", "영업 채널", "대상 타겟군", "규모", "진행 현황"]
r_widths = [Inches(1.0), Inches(0.6), Inches(1.1), Inches(1.8), Inches(1.0), Inches(1.5)]
r_rows = [
    ["11월 09일", "월", "📧 이메일", "기존 검증 성공업체", "70개사", "✅ 발송 완료 (성공 67 / 실패 3)"],
    ["11월 16일", "월", "📠 팩스", "기존 검증 성공업체", "30개사", "준비 완료 (30개사 사전 선별 완료)"],
    ["11월 23일", "월", "🔄 복합", "신규 크롤링 + 기존 재검증", "50~70개사", "예정 (전국 20개 지역 대상)"],
    ["11월 30일", "월", "📧+📠", "신규 + 검증 복합 타겟", "100개사+", "예정 (11월 총결산 하이브리드)"]
]
t1 = doc.add_table(rows=1, cols=len(r_headers))
style_table(t1, r_widths, r_headers, r_rows)

add_heading_2("차주 11/16(월) 팩스 30개사 사전 준비 내용")
add_paragraph_text("11/02 수신 성공이 확인된 22개사와 우량 팩스 번호 보유사, 그리고 오늘 메일 차단으로 팩스 전환된 (주)아이디오(041-548-8238)를 포함하여 총 30개사의 타겟 풀을 확정하였으며, 차주 월요일 샌드랩스 대량 업로드로 즉시 집행 가능합니다.")

out_docx = r"E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-09_dhsteel_final_work_summary.docx"
doc.save(out_docx)
print(f"Final work summary docx saved to {out_docx}")

