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

# Styles
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
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.name = "맑은 고딕"
        set_font(p.runs[0], "맑은 고딕", 10, bold=True, color_rgb=(255, 255, 255))
        shading = parse_xml(r'<w:shd {} w:fill="1E3A8A"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)

    # Data Rows
    for r_idx, row_data in enumerate(data_rows):
        row_cells = table.add_row().cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            p = row_cells[c_idx].paragraphs[0]
            # align numbers to center or right
            if c_idx == 0 or "%" in str(val) or "~" in str(val):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if str(val).isdigit() else WD_ALIGN_PARAGRAPH.LEFT
            set_font(p.runs[0], "맑은 고딕", 10, bold=(r_idx == len(data_rows)-1), color_rgb=(51, 51, 51))
            shading = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), bg_color))
            row_cells[c_idx]._tc.get_or_add_tcPr().append(shading)

    # Set Column widths
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

# Title
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(4)
run_title = p_title.add_run("대흥정밀 B2B 아웃바운드 통합 발송 분석 & 스케줄 보고서")
set_font(run_title, "맑은 고딕", 16, bold=True, color_rgb=(15, 32, 67))

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
run_sub = p_sub.add_run(f"기준일자: 2026-11-09 (월) | 작성 대상: schedule, mail_log, fax_log, company 시트 연동")
set_font(run_sub, "맑은 고딕", 10, color_rgb=(100, 116, 139))

# Section 1
add_heading_1("1. 아웃바운드 총괄 집행 요약 (Executive Summary)")
add_paragraph_text("대흥정밀 B2B 영업 마케팅은 메일(Gmail API)과 웹팩스(SendLabs) 2개 채널을 유기적으로 교차 운영하고 있으며, 2026년 8월 31일부터 11월 9일 현재까지 총 471건의 아웃바운드 영업이 집행되었습니다.")
add_paragraph_text("총 발송 집행 건수: 471건 (이메일 359건, 팩스 112건)", bullet=True)
add_paragraph_text("누적 성공 건수: 346건 (전체 평균 성공률 73.5%)", bullet=True)
add_paragraph_text("11월 팩스 성과 대폭 상승: 10월 23.5%에서 11월 71.0%로 성공률 급상승 (이메일 발송군 대상 유효 팩스 2차 전환 효과 입증)", bullet=True)

# Section 2: Monthly Table
add_heading_1("2. 월간 아웃바운드 발송 종합 현황 (Monthly Analysis)")
m_headers = ["발송월", "총발송", "메일발송", "메일성공", "성공률", "팩스발송", "팩스성공", "성공률", "총성공", "종합성공률"]
m_widths = [Inches(0.9), Inches(0.6), Inches(0.65), Inches(0.65), Inches(0.6), Inches(0.65), Inches(0.65), Inches(0.6), Inches(0.65), Inches(0.7)]
m_rows = [
    ["2026-08월", "20", "20", "15", "75.0%", "0", "0", "-", "15", "75.0%"],
    ["2026-09월", "240", "240", "192", "80.0%", "0", "0", "-", "192", "80.0%"],
    ["2026-10월", "180", "99", "97", "98.0%", "81", "19", "23.5%", "116", "64.4%"],
    ["2026-11월", "31", "0", "0", "-", "31", "22", "71.0%", "22", "71.0%"],
    ["합계/평균", "471", "359", "304", "84.7%", "112", "41", "36.6%", "346", "73.5%"]
]
t1 = doc.add_table(rows=1, cols=len(m_headers))
style_table(t1, m_widths, m_headers, m_rows)

# Section 3: Weekly Table
add_heading_1("3. 주간별 발송 추이 (Weekly Dispatch Tracking)")
w_headers = ["주차 (ISO)", "기간", "메일", "성공", "성공률", "팩스", "성공", "성공률", "주간합계", "주간성공률"]
w_widths = [Inches(0.9), Inches(0.9), Inches(0.55), Inches(0.55), Inches(0.6), Inches(0.55), Inches(0.55), Inches(0.6), Inches(0.65), Inches(0.7)]
w_rows = [
    ["2026-W36", "08/31~09/06", "60", "41", "68.3%", "0", "0", "-", "60", "68.3%"],
    ["2026-W37", "09/07~09/13", "80", "62", "77.5%", "0", "0", "-", "80", "77.5%"],
    ["2026-W38", "09/14~09/20", "120", "104", "86.7%", "0", "0", "-", "120", "86.7%"],
    ["2026-W40", "09/28~10/04", "48", "46", "95.8%", "0", "0", "-", "48", "95.8%"],
    ["2026-W41", "10/05~10/11", "0", "0", "-", "13", "4", "30.8%", "13", "30.8%"],
    ["2026-W42", "10/12~10/18", "0", "0", "-", "29", "7", "24.1%", "29", "24.1%"],
    ["2026-W43", "10/19~10/25", "0", "0", "-", "39", "8", "20.5%", "39", "20.5%"],
    ["2026-W44", "10/26~11/01", "51", "51", "100.0%", "0", "0", "-", "51", "100.0%"],
    ["2026-W45", "11/02~11/08", "0", "0", "-", "31", "22", "71.0%", "31", "71.0%"]
]
t2 = doc.add_table(rows=1, cols=len(w_headers))
style_table(t2, w_widths, w_headers, w_rows)

# Section 4: Batch Sendable Pool
add_heading_1("4. 한번에 전송 가능한 채널별 타겟 풀 분석 (Batch Sendable Pool)")
add_paragraph_text("현재 company 시트에서 유효 연락처가 확보되어 원클릭 또는 엑셀 업로드로 즉시 전송 가능한 모수 현황입니다.")

b_headers = ["영업 채널", "전체 보유수", "성공 완료", "실패(보정대상)", "미발송(대기)", "한번에 전송 규모", "실행 방식"]
b_widths = [Inches(1.1), Inches(0.7), Inches(0.7), Inches(0.9), Inches(0.8), Inches(1.1), Inches(1.4)]
b_rows = [
    ["📧 이메일 타겟", "83건", "80건", "3건", "0건", "83개사 일괄 전송", "GAS 상단 메뉴 원클릭 전송"],
    ["📠 팩스 타겟", "69건", "30건", "36건", "3건", "69개사 대량 업로드", "샌드랩스 엑셀(XLSX) 일괄 업로드"],
    ["🔄 크로스채널 복합", "32건", "22건", "10건", "0건", "32개사 복합 전송", "메일 발송 후 팩스 연계 전송"]
]
t3 = doc.add_table(rows=1, cols=len(b_headers))
style_table(t3, b_widths, b_headers, b_rows)

add_heading_2("💡 실무자를 위한 원클릭/대량 전송 가이드")
add_paragraph_text("1. 이메일 일괄 전송: 구글 스프레드시트 상단 메뉴 [대흥 아웃바운드] → [📧 대흥정밀 메일 일괄 발송]을 실행하면 대상 업체에 개인화 제안서가 자동 발송되며 mail_log에 실시간 기록됩니다.", bullet=True)
add_paragraph_text("2. 팩스 대량 업로드: sales/fax 폴더 내 생성된 전용 엑셀(xlsx) 또는 csv 파일을 샌드랩스(SendLabs) 웹팩스 대량 전송에 업로드하면 1분 이내에 수십~수백 건을 동시 전송할 수 있습니다.", bullet=True)
add_paragraph_text("3. 실패 번호 보정: 팩스 실패 36건 중 11/02 발생 9건(응답없음 5, 연결오류 4)은 일반 유선전화와 팩스 겸용 회선일 수 있으므로 번호 확인 후 재발송을 권장합니다.", bullet=True)

out_docx = r"E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-09_dhsteel_schedule_analysis.docx"
doc.save(out_docx)
print(f"Report saved successfully to {out_docx}")

