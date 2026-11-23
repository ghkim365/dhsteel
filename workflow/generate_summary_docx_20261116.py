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
            if c_idx in (0, 1) or "%" in str(val):
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
run_title = p_title.add_run("대흥정밀 B2B 정기 로테이션 업무 최종 완료 보고서 (11/16)")
set_font(run_title, "맑은 고딕", 16, bold=True, color_rgb=(15, 32, 67))

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
run_sub = p_sub.add_run("기준일자: 2026-11-16 (월) | 작성자: AI Coding Assistant (Antigravity)")
set_font(run_sub, "맑은 고딕", 10, color_rgb=(100, 116, 139))

add_heading_1("1. 오늘(11/16) 주요 업무 집행 성과")
add_paragraph_text("대흥정밀 11월 정기 로테이션 2주차 팩스 발송 캠페인 및 인프라 표준화 작업이 성공적으로 완결되었습니다.")
add_paragraph_text("플랜 자료 폴더 분리: plan/ 폴더 신설 및 마스터 플랜 10개 파일 체계적 이관 완료", bullet=True)
add_paragraph_text("대시보드 링크 정상화: dashboard.html 상단 '2026 계획서' 링크 경로 신규 plan/으로 수정 완료", bullet=True)
add_paragraph_text("팩스 6회차 발송 성공: 샌드랩스 29건 발송 중 27건 성공 (성공률 93.1% 달성)", bullet=True)
add_paragraph_text("크로스채널 전환 성공: 지난주 메일 보안 차단된 (주)아이디오에 팩스 정상 수신 완결", bullet=True)
add_paragraph_text("대시보드 3종 전수 동기화: dashboard.html, fax_report.html, 워드 결과 보고서 100% 일치", bullet=True)
add_paragraph_text("정기 발송 SOP 구축: 매주 반복 업무 표준화를 위한 전용 SOP.md 및 플랜 웹 탭 탑재 완료", bullet=True)

add_heading_1("2. 팩스 6회차 발송 성과 요약")
f_headers = ["구분", "발송 시도", "정상 수신(성공)", "수신 실패", "성공률", "주요 비고"]
f_widths = [Inches(1.2), Inches(0.9), Inches(1.1), Inches(0.9), Inches(0.9), Inches(1.8)]
f_rows = [
    ["팩스 6회차 (11/16)", "29건", "27건", "2건", "93.1%", "역대 최고 성공률 달성"],
    ["누적 1~6회차 총괄", "141건", "68건", "73건", "48.2%", "11월 발송군 성공률 81.7%"]
]
t1 = doc.add_table(rows=1, cols=len(f_headers))
style_table(t1, f_widths, f_headers, f_rows)

add_heading_1("3. 차주(11/23 월) 예정 업무")
add_paragraph_text("11월 3주차 로드맵에 따라 전국 20개 산업 지역 대상 신규 B2B 리드 크롤링 수집(지침서 B안, 50~70개사) 및 기존 미응답 번호 재검증을 진행할 예정입니다.")

out_docx = r"E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-16_dhsteel_final_work_summary.docx"
doc.save(out_docx)
print(f"Final summary docx saved to {out_docx}")

