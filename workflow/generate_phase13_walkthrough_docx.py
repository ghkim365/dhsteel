# -*- coding: utf-8 -*-
"""
PHASE 13 작업 완료 워크스루 Word 보고서 자동 생성기
- 사용자 전역 규칙: 맑은 고딕(Malgun Gothic), 본문 10pt, H1 14pt, H2 12pt, H3 10pt
"""

import os
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_report():
    doc = Document()
    
    # 페이지 여백
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
    # 스타일 기본 설정
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = '맑은 고딕'
    font.size = Pt(10)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(4)
    
    # ── 타이틀 ──
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_title.add_run("대흥정밀 B2B 마케팅 & 자동화 파이프라인\n")
    run_sub.font.size = Pt(10.5)
    run_sub.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    
    run_title = p_title.add_run("[PHASE 13] 실수요처 정밀 발굴 & 환경 동기화 완료 보고서")
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1C, 0x2B, 0x4A)
    
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_meta = p_meta.add_run("작업일자: 2026-10-21  |  작성자: Antigravity AI Pair Programmer")
    r_meta.font.size = Pt(8.5)
    r_meta.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    
    # ── 1. 개요 및 긴급 조치 내역 ──
    h1 = doc.add_paragraph()
    r = h1.add_run("1. 작업 개요 및 환경 동기화 조치")
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1C, 0x2B, 0x4A)
    
    t1 = doc.add_table(rows=5, cols=2)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False
    
    headers_info = [
        ("항목", "조치 내용 및 결과"),
        ("작업 전체 백업", "D:\\Antigravity_back\\builder-dhsteel-sales 에 이전 작업 전체 완전 백업 완료 (Exit code 1, 성공)"),
        ("IDE 환경 백업 (회사/집)", "H:\\Antigravity\\backup_com\\environment 및 backup_home\\environment 로 미러링 동기화 완료"),
        ("드라이브 경로 치환 (D: ➔ E:)", "프로젝트 내 94개 파일(HTML, JS, PY, MD 등)의 D:/Antigravity 경로를 E:/Antigravity 로 전수 안전 치환"),
        ("구글 스프레드시트 연동", "Search 시트(gid: 1498229330) 2행부터 크롤링 적재 파이프라인 및 서비스 계정 인증 정상화")
    ]
    
    for row_idx, (c0, c1) in enumerate(headers_info):
        row = t1.rows[row_idx]
        cell0, cell1 = row.cells[0], row.cells[1]
        cell0.width = Inches(2.2)
        cell1.width = Inches(4.5)
        
        p0 = cell0.paragraphs[0]
        r0 = p0.add_run(c0)
        p1 = cell1.paragraphs[0]
        r1 = p1.add_run(c1)
        
        if row_idx == 0:
            set_cell_background(cell0, "1C2B4A")
            set_cell_background(cell1, "1C2B4A")
            r0.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r0.font.bold = True
            r1.font.bold = True
        else:
            set_cell_background(cell0, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_background(cell1, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            r0.font.bold = True
            r0.font.size = Pt(9.5)
            r1.font.size = Pt(9.5)
        set_cell_margins(cell0, 80, 80, 100, 100)
        set_cell_margins(cell1, 80, 80, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # ── 2. PHASE 13 실수요처 발굴 원칙 및 네거티브 필터링 ──
    h2 = doc.add_paragraph()
    r = h2.add_run("2. PHASE 13 실수요처 발굴 핵심 원칙")
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1C, 0x2B, 0x4A)
    
    p = doc.add_paragraph()
    r = p.add_run("• 치명적 원인 반성: ")
    r.font.bold = True
    p.add_run("대흥정밀의 자체 가공 기술 키워드('축관', '확관', '포밍', '스웨이징')로 검색하여 전국의 동종 임가공 경쟁업체(138개사, 46%)가 대거 수집되었던 참사를 전면 차단함.\n")
    
    r = p.add_run("• 새로운 원칙: ")
    r.font.bold = True
    p.add_run("기술 키워드를 영구 폐기하고, 19Φ~50Φ 파이프 부품을 외주 발주하는 ")
    r_target = p.add_run("완제품·장비 조립 제조업체")
    r_target.font.bold = True
    r_target.font.color.rgb = RGBColor(0x15, 0x80, 0x3D)
    p.add_run("를 1차 타깃으로 지정함.\n")
    
    r = p.add_run("• 절대 취급 제외 조건 (공식 기준): ")
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)
    p.add_run("건설 배관 / 토목 배관 / 아파트 설비 배관 / 소방 공사용 현장 배관 전면 배제 및 ")
    r_med = p.add_run("초정밀 의료 부품 전면 배제(**추가사항)")
    r_med.font.bold = True
    r_med.font.color.rgb = RGBColor(0x99, 0x1B, 0x1B)
    p.add_run("를 확정 반영함.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # ── 3. 타깃 3대 우선순위 및 적재 프로세스 ──
    h3 = doc.add_paragraph()
    r = h3.add_run("3. 타깃 우선순위 및 3단계 유효성 검증 파이프라인")
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1C, 0x2B, 0x4A)
    
    t2 = doc.add_table(rows=4, cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False
    
    pipeline_info = [
        ("구분", "타깃 산업군 & 세부 검색어", "가공 실수요 용도"),
        ("🥇 1순위\n(집중 크롤링)", "• 열교환기/오일쿨러/라디에이터/냉동공조\n• 특장차/농기계/트랙터/지게차 부품\n• 전동침대/병원침대/휠체어/재활복지기기\n• 헬스기구/피트니스/철재가구/모션데스크", "• 호스 체결부 비딩(Bead) 성형\n• 튜브 소켓 결합 확관(Expansion)\n• 단단/테이퍼 정밀 감면(Reduction)\n• 프레임 간 끼움 조립"),
        ("🥈 2순위", "• 자동화설비, 산업기계 프레임, 공작기계 커버\n• 콘베이어 롤러, 로봇 안전펜스", "• 직경 피치 드릴링 타공\n• 양단 면취 및 정밀 절단 일괄"),
        ("🥉 3순위", "• 파이프 핸들, 차량 안전바, 산업용 카트", "• 주름 없는 정밀 곡면 R 벤딩")
    ]
    
    for row_idx, (c0, c1, c2) in enumerate(pipeline_info):
        row = t2.rows[row_idx]
        cell0, cell1, cell2 = row.cells[0], row.cells[1], row.cells[2]
        cell0.width = Inches(1.5)
        cell1.width = Inches(3.2)
        cell2.width = Inches(2.0)
        
        p0, p1, p2 = cell0.paragraphs[0], cell1.paragraphs[0], cell2.paragraphs[0]
        r0, r1, r2 = p0.add_run(c0), p1.add_run(c1), p2.add_run(c2)
        
        if row_idx == 0:
            set_cell_background(cell0, "1C2B4A")
            set_cell_background(cell1, "1C2B4A")
            set_cell_background(cell2, "1C2B4A")
            for r_item in [r0, r1, r2]:
                r_item.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                r_item.font.bold = True
        else:
            set_cell_background(cell0, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_background(cell1, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_background(cell2, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            r0.font.bold = True
            r0.font.size = Pt(9.5)
            r1.font.size = Pt(9)
            r2.font.size = Pt(9)
        set_cell_margins(cell0, 80, 80, 100, 100)
        set_cell_margins(cell1, 80, 80, 100, 100)
        set_cell_margins(cell2, 80, 80, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # ── 4. 데이터 적재 및 시트 격리 프로세스 ──
    h4 = doc.add_paragraph()
    r = h4.add_run("4. 데이터 적재 및 3단계 검증 흐름도")
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1C, 0x2B, 0x4A)
    
    p_flow = doc.add_paragraph()
    p_flow.add_run("1) [1단계 크롤링 ➔ Search 시트 적재]: ")
    p_flow.runs[0].font.bold = True
    p_flow.add_run("수집된 데이터는 기존 DB 오염을 막기 위해 company 시트가 아닌 ")
    r_s = p_flow.add_run("Search 시트 (gid: 1498229330)의 2행부터")
    r_s.font.bold = True
    r_s.font.color.rgb = RGBColor(0x1D, 0x4E, 0xD8)
    p_flow.add_run(" 우선 적재됨.\n")
    
    p_flow.add_run("2) [2단계 네거티브 필터링 & 격리]: ")
    p_flow.runs[len(p_flow.runs)-1].font.bold = True
    p_flow.add_run("동종업체 키워드 및 비규격(건설/토목/소방 배관, 초정밀 의료 부품) 포함 기업은 company_exception 시트로 자동 격리.\n")
    
    p_flow.add_run("3) [3단계 실재성 및 연락처 검증]: ")
    p_flow.runs[len(p_flow.runs)-1].font.bold = True
    p_flow.add_run("국세청 사업자등록 상태(휴·폐업) 및 가상번호(0507) 배제, 팩스/유선 회선 검증 통과 기업만 선별.\n")
    
    p_flow.add_run("4) [최종 정식 이관]: ")
    p_flow.runs[len(p_flow.runs)-1].font.bold = True
    p_flow.add_run("검증 통과 클린 실수요 DB만 company 시트로 정식 이관하여 팩스 5차 발송 대열로 편성.")
    
    output_path = r"E:\Antigravity\builder-dhsteel-sales\workflow\PHASE13_실수요처_크롤링_마스터플랜_결과보고서.docx"
    doc.save(output_path)
    print(f"✅ Word 보고서 저장 완료: {output_path}")

if __name__ == "__main__":
    create_report()
