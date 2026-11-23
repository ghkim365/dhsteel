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
run_title = p_title.add_run("대흥정밀 11/09 메일 발송 결과 및 반송 보정 조치 보고서")
set_font(run_title, "맑은 고딕", 16, bold=True, color_rgb=(15, 32, 67))

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
run_sub = p_sub.add_run("기준일자: 2026-11-09 (월) 10:55 | 집행 건수: 70건 | 실성공: 67건 (95.7%)")
set_font(run_sub, "맑은 고딕", 10, color_rgb=(100, 116, 139))

add_heading_1("1. 당일(11/09) 발송 및 수신 결과 요약")
add_paragraph_text("2026년 11월 9일 10시 45분, 사전 검증된 70개사를 대상으로 구글 스프레드시트 연동 Gmail API 일괄 발송이 정상 집행되었습니다.")
add_paragraph_text("발송 시도: 총 70개사 (Gmail API 전송 성공 100%)", bullet=True)
add_paragraph_text("실제 도달 성공: 67개사 (실도달 성공률 95.7%)", bullet=True)
add_paragraph_text("반송/오류 발생: 3개사 (실시간 보정 및 채널 전환 완료)", bullet=True)

add_heading_1("2. 반송 3개사 세부 분석 및 조치 내역")
c_headers = ["업체명", "시트 행", "등록 이메일", "오류 원인", "완료된 조치 내용", "후속 운영 방향"]
c_widths = [Inches(1.0), Inches(0.6), Inches(1.3), Inches(1.2), Inches(1.4), Inches(1.3)]
c_rows = [
    ["코베아", "211행", "sales40@kovea.co", "도메인 오타(.co)", "sales40@kovea.co.kr 보정", "정상 주소로 재전송 대기"],
    ["금경이노텍", "147행", "jbb6689@naver.com", "네이버 계정 탈퇴/삭제", "상태 '실패(계정삭제)' 표기", "메일 제외, 타 채널 탐색"],
    ["(주)아이디오", "239행", "song01245@idomagicon.com", "수신 메일 서버 차단", "상태 '실패(차단)' 및 팩스 전환", "보유 팩스(041-548-8238) 활용"]
]
t1 = doc.add_table(rows=1, cols=len(c_headers))
style_table(t1, c_widths, c_headers, c_rows)

add_heading_1("3. 향후 로테이션 발송 일정 (11월 잔여)")
add_paragraph_text("11월 16일 (월): 팩스 검증 업체 30개사 샌드랩스 대량 재발송 (아이디오 포함)", bullet=True)
add_paragraph_text("11월 23일 (월): 전국 20개 산업 지역 신규 리드 크롤링 수집 + 기존 미응답 번호 보정", bullet=True)
add_paragraph_text("11월 30일 (월): 신규 + 검증 복합 하이브리드 대량 아웃바운드 집행", bullet=True)

out_docx = r"E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-09_dhsteel_bounce_correction_report.docx"
doc.save(out_docx)
print(f"Correction report saved to {out_docx}")

