# -*- coding: utf-8 -*-
import os
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_summary_docx():
    doc = Document()
    
    # 1. Page Margins
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.9)
        sec.right_margin = Inches(0.9)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = '맑은 고딕'
    normal_font.size = Pt(10)
    normal_font.color.rgb = RGBColor(51, 65, 85) # #334155
    normal_style._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
    normal_style.paragraph_format.line_spacing = 1.35
    normal_style.paragraph_format.space_after = Pt(4)
    
    def set_cell_background(cell, hex_color):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = '맑은 고딕'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(21, 40, 77) # #15284D
        run._r.get_or_add_rPr().set(qn('w:eastAsia'), '맑은 고딕')
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
        run.font.color.rgb = RGBColor(30, 41, 59) # #1E293B
        run._r.get_or_add_rPr().set(qn('w:eastAsia'), '맑은 고딕')
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = '맑은 고딕'
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(37, 99, 235) # #2563EB
        run._r.get_or_add_rPr().set(qn('w:eastAsia'), '맑은 고딕')
        return p

    def add_p(text, bold_prefix="", color=None):
        p = doc.add_paragraph()
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = '맑은 고딕'
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            if color:
                r_pre.font.color.rgb = color
            r_pre._r.get_or_add_rPr().set(qn('w:eastAsia'), '맑은 고딕')
        r = p.add_run(text)
        r.font.name = '맑은 고딕'
        r.font.size = Pt(10)
        if color:
            r.font.color.rgb = color
        r._r.get_or_add_rPr().set(qn('w:eastAsia'), '맑은 고딕')
        return p

    # --- Title Banner ---
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_t = title_p.add_run("대흥정밀 B2B 마케팅 & 인프라 플랜 2026 — 일일 작업 완료 보고서")
    run_t.font.name = '맑은 고딕'
    run_t.font.size = Pt(16)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(21, 40, 77)
    run_t._r.get_or_add_rPr().set(qn('w:eastAsia'), '맑은 고딕')

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("PHASE 21 신설 • 모바일 대시보드 개선 • 고객 중심 루트 라우팅 • Claude/Antigravity 대화록 구축")
    run_sub.font.name = '맑은 고딕'
    run_sub.font.size = Pt(10)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    # --- Meta Table ---
    tbl = doc.add_table(rows=4, cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    meta_data = [
        [("보고서 번호", True), ("DHSTEEL-PLAN-20261124-01", False), ("작업 일자", True), ("2026년 11월 24일", False)],
        [("프로젝트", True), ("대흥정밀 (builder-dhsteel-sales)", False), ("담당 에이전트", True), ("Antigravity (Gemini) & Claude Code", False)],
        [("배포 서비스", True), ("https://dhsteel.pages.dev", False), ("인프라 환경", True), ("Cloudflare Pages & GitHub origin/main", False)],
        [("마스터 플랜", True), ("plan/dhsteel_plan_2026.html (PHASE 21)", False), ("대화록 생성", True), ("HTML/MD 2종 (ramines 양식 완비)", False)]
    ]

    for row_idx, row in enumerate(meta_data):
        for col_idx, (text, is_hdr) in enumerate(row):
            cell = tbl.cell(row_idx, col_idx)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if is_hdr else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = '맑은 고딕'
            r.font.size = Pt(9.5)
            r.font.bold = is_hdr
            if is_hdr:
                set_cell_background(cell, "F1F4FA")
                r.font.color.rgb = RGBColor(21, 40, 77)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- 1. 작업 개요 ---
    add_h1("1. 작업 개요 및 마스터 플랜 반영 현황")
    add_p("2026년 11월 24일 진행된 대시보드 모바일(362px) 반응형 개선, 고객 중심 루트 라우팅(모바일 카탈로그 직결) 개편, GAS 타임아웃 15초 상향 조치 및 삼협철망 인수인계 지침서 작성을 종합하여 마스터 플랜(plan/dhsteel_plan_2026.html)에 PHASE 21로 공식 등재하였습니다.")
    add_p("또한 ramines 프로젝트(plan/claude_chat_history_20261123.html, antigravity_chat_history_20261123.html)의 디자인 서식과 동일한 구조로 오늘 오간 모든 에이전트 대화 내역을 HTML 및 Markdown 파일로 추출·생성하여 브라우저 열람과 구글 독스(Ctrl+A ➔ Ctrl+C ➔ Ctrl+V) 복사를 완벽히 지원하도록 조치하였습니다.")

    # --- 2. 핵심 4대 작업 상세 ---
    add_h1("2. 오늘(2026-11-24) 완료된 4대 핵심 작업 상세")

    add_h2("가. 대시보드 모바일(362px) 반응형 전면 최적화 (Claude Code)")
    add_p("• 레거시 65px 사이드바 충돌 완전 제거: 기존 @media(max-width: 768px) 블록에 남아있던 .sidebar { width: 65px; } 구형 스타일을 삭제하여 모바일에서 사이드바가 좌측 화면을 가리던 현상을 원천 차단하였습니다.")
    add_p("• 하단 고정 탭바(Bottom Tab Bar) 강제 적용: position: fixed; bottom: 0; width: 100%; z-index: 1000 속성으로 모바일 한 손 터치 접근성을 보장하였습니다.")
    add_p("• 테이블 카드형 UI 변환: 견적/로그 표를 카드 목록형으로 변환하여 가로 폭 362px 화면에서도 스크롤 없이 회사명과 상세 정보를 한눈에 열람 가능하도록 개선하였습니다.")
    add_p("• 차트 및 슬라이더 1열 재배치: Google Ads 시뮬레이터와 Chart.js 캔버스에 max-width: 100% 및 overflow: hidden을 적용하여 우측 잘림을 방지하였습니다. (커밋: 402224f, 0fef1fd, 6ed034a)")

    add_h2("나. 고객 메인 접속 구조 개편 & 은폐 관리자 게이트 구축 (Antigravity)")
    add_p("• 루트(/) 및 index.html 카탈로그 직결: 일반 고객이나 거래처가 dhsteel.pages.dev 접속 시 관리자 로그인 화면이 노출되지 않고, 직관적인 모바일 카탈로그(catalog/index_catalog.html)가 302 리다이렉트로 즉시 열리도록 _redirects 및 index.html을 개편하였습니다.")
    add_p("• 상단 헤더 브로슈어 연결: 카탈로그 상단 네비게이션에 [📄 브로슈어 ↗] 버튼을 신설하여 4페이지 B2B 기술 브로슈어로 바로 이동할 수 있도록 연결하였습니다.")
    add_p("• 푸터 카피라이트 은폐 관리자 진입로: 카탈로그 최하단 푸터의 저작권 문구(&copy; 2026 대흥정밀.)에 비밀 클릭 이벤트(#adminGate)를 부여하여, 고객에게는 감추고 대표님만 클릭 시 관리자 대시보드(index_dashboard.html)로 진입할 수 있도록 구현하였습니다. (커밋: ab23c7e, a46042c)")

    add_h2("다. Google Apps Script 15초 타임아웃 상향 및 0건 데이터 방어")
    add_p("• 원인 규명: index_dashboard.html 내 fetchJSONP 함수에 하드코딩되어 있던 5000ms(5초) 타임아웃이 497행의 구글 시트 데이터를 연산·조회할 때 초과되어 빈 객체({ visits: 0, quotes: [] })로 폴백되는 오류를 확인하였습니다.")
    add_p("• 해결 조치: 타임아웃을 15000ms(15초)로 3배 늘리고, 네트워크 지연이나 일시 오류 발생 시에도 기존 localStorage 캐시 데이터를 보존하여 화면에 '0건 / 0.0%'이 노출되는 문제를 완벽하게 방어하였습니다.")

    add_h2("라. 삼협철망(builder-samhyup-sales) 프로젝트 인수인계 지침서 완비")
    add_p("• 대흥정밀에서 완벽히 검증된 모바일 반응형 개선안과 고객 중심 카탈로그 루트 라우팅 및 은폐 관리자 게이트를 삼협철망 프로젝트에 즉시 이식할 수 있도록 전달용 SOP 마크다운(workflow/2026-11-24_samhyup_mobile_layout_and_routing_instruction.md)과 맑은 고딕 10pt 워드 문서를 작성하였습니다.")

    # --- 3. 대화 내역 HTML/MD 생성 결과 ---
    add_h1("3. Claude Code 및 Antigravity 대화록 추출 결과")
    add_p("E:\\Antigravity\\ramines\\plan\\ 샘플과 100% 동일한 Pretendard 타이포그래피, 사용자/에이전트 컬러 구분 말풍선, 타임스탬프 및 복사 가이드가 포함된 독립 HTML 및 Markdown 파일을 plan 디렉토리에 생성하였습니다.")

    tbl_chat = doc.add_table(rows=3, cols=4)
    tbl_chat.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_chat.autofit = False

    chat_rows = [
        [("구분", True), ("파일 경로", True), ("대화 턴 수", True), ("특징 및 용도", True)],
        [("Claude Code", False), ("plan/claude_chat_history_20261124.html\nplan/claude_chat_history_20261124.md", False), ("57개 턴", False), ("모바일 반응형 CSS/JS 코드 수정 및 실시간 트러블슈팅 전문", False)],
        [("Antigravity", False), ("plan/antigravity_chat_history_20261124.html\nplan/antigravity_chat_history_20261124.md", False), ("157개 턴", False), ("고객 접속 구조 개편, GAS 타임아웃 규명, Cloudflare 검증, SOP 발행 전문", False)]
    ]

    for r_idx, r in enumerate(chat_rows):
        for c_idx, (txt, is_h) in enumerate(r):
            cell = tbl_chat.cell(r_idx, c_idx)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            cell.text = ""
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (is_h or c_idx == 0 or c_idx == 2) else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(txt)
            run.font.name = '맑은 고딕'
            run.font.size = Pt(9.5)
            run.font.bold = is_h
            if is_h:
                set_cell_background(cell, "F1F4FA")
                run.font.color.rgb = RGBColor(21, 40, 77)
            else:
                run.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    add_p("💡 구글 독스 복사 팁: 생성된 HTML 파일을 브라우저에서 열고 Ctrl+A(전체 선택) ➔ Ctrl+C(복사) 후 구글 독스에 Ctrl+V(붙여넣기)하시면, 말풍선 배경색과 폰트 크기 및 줄바꿈 서식이 깨지지 않고 그대로 깔끔하게 붙여넣어집니다.", bold_prefix="[안내] ", color=RGBColor(37, 99, 235))

    # --- 4. 배포 동기화 현황 ---
    add_h1("4. 배포 패키지(dist_deploy) 빌드 및 검증 현황")
    add_p("build_dist_deploy.py 스크립트를 업데이트하여 plan 디렉토리 내의 모든 HTML/MD 대화 내역 및 플랜 문서가 dist_deploy 패키지에 자동 포함되도록 구성하였습니다.")
    add_p("• 빌드 결과: 총 222개 파일 (58.99 MB) 패키징 완료")
    add_p("• 포함 파일: dhsteel_plan_2026.html, claude_chat_history_20261124.html, antigravity_chat_history_20261124.html, index.html, index_dashboard.html, catalog 전 문서")
    add_p("• 라우팅 규칙: dist_deploy/_redirects 내 루트 302 리다이렉트(/ -> /catalog/index_catalog.html) 탑재 완료")

    out_docx_path = r'E:\Antigravity\builder-dhsteel-sales\workflow\2026-11-24_dhsteel_plan_and_chat_summary.docx'
    doc.save(out_docx_path)
    print(f"Successfully generated DOCX: {out_docx_path}")

if __name__ == '__main__':
    create_summary_docx()

