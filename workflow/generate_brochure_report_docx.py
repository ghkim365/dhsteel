# -*- coding: utf-8 -*-
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_report():
    doc = docx.Document()
    
    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = '맑은 고딕'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x33, 0x41, 0x55) # slate-700
    normal_style._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = '맑은 고딕'
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(0x15, 0x28, 0x4D) # navy
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.font.name = '맑은 고딕'
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = RGBColor(0x25, 0x63, 0xEB) # blue
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.25
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = '맑은 고딕'
            r_bold.font.size = Pt(10)
            r_bold.bold = True
            r_bold._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
        run = p.add_run(text)
        run.font.name = '맑은 고딕'
        run.font.size = Pt(10)
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1.5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = 1.2
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = '맑은 고딕'
            r_bold.font.size = Pt(10)
            r_bold.bold = True
            r_bold._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
        run = p.add_run(text)
        run.font.name = '맑은 고딕'
        run.font.size = Pt(10)
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')
        return p

    # Title Banner
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(6)
    t_run = title_p.add_run("대흥정밀(DHSTEEL) B2B 정식 파이프 임가공 카탈로그 브로슈어 구축 보고서")
    t_run.font.name = '맑은 고딕'
    t_run.font.size = Pt(16)
    t_run.bold = True
    t_run.font.color.rgb = RGBColor(0x15, 0x28, 0x4D)
    t_run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(12)
    s_run = sub_p.add_run("A4 멀티페이지 인쇄 최적화 · 소구경(22Φ~50Φ) CAD 규격도 반영 · 배포 패키지 동기화 완료 | 2026-11-23")
    s_run.font.name = '맑은 고딕'
    s_run.font.size = Pt(9.5)
    s_run.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    s_run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

    # Divider
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(8)
    p_div_border = parse_xml(r'<w:pBdr {}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="2563EB"/></w:pBdr>'.format(nsdecls('w')))
    p_div._p.get_or_add_pPr().append(p_div_border)

    # 1. 작업 개요 및 목적
    add_h1("1. 작업 개요 및 추진 목적")
    add_p("기존 임시 단일 파일(대흥정밀 B2B 파이프 임가공 제안서_미리보기.html)을 대체하여, 삼협철망의 고품질 A4 인쇄용 브로슈어(index_brochure.html) 규격을 완벽히 계승한 대흥정밀(DHSTEEL) 정식 B2B 소구경 파이프 임가공 카탈로그 브로슈어를 신규 제작하고 대시보드 및 운영 계획서 인프라에 통합 배포하였습니다.")
    add_bullet("삼협철망 브로슈어의 .a4-page 멀티페이지 구조 및 인쇄 전용 CSS 미디어 쿼리 완벽 적용", "• A4 인쇄/PDF 저장 최적화: ")
    add_bullet("소구경 원형 파이프(22Φ, 25Φ, 38Φ, 50Φ) 전문 가공에 맞추어 대형 플랜트 사진을 완전 배제하고 CAD 정밀 규격도 배치", "• 소구경(22Φ~50Φ) 특화 반영: ")
    add_bullet("어두운 배경을 완전 배제하고 화이트 및 연회색(Slate-50) 베이스의 깔끔한 B2B 엔지니어링 감성 구축", "• 사용자 선호 클린 라이트 테마: ")
    add_bullet("과도한 두꺼운 볼드(Bold 800/900)를 배제하고 가독성 높은 Semi-Bold(600) 및 Medium(500) 타이포그래피 적용", "• Semi-bold 타이포그래피: ")
    add_bullet("우측 하단 원클릭 A4 인쇄/PDF 저장 버튼 및 직영 공장 대표번호 원터치 다이얼 연동", "• 반응형 플로팅 액션 바: ")

    # 2. 브로슈어 4-Page 구성 내역
    add_h1("2. 대흥정밀 B2B 브로슈어 상세 페이지 구성 (총 4페이지)")
    
    add_h2("Page 1: 표지 및 회사 개요 & 메인 가공 인프라")
    add_bullet("공식 CI 로고(images/logo_dhsteel.png), 소구경 파이프(22Φ~50Φ) 정밀 가공 솔루션 캐치프레이즈", "• 헤더 및 브랜딩: ")
    add_bullet("시흥 직영 300평 가공 라인, 대용량 유압 프레스, 정밀 스웨이징 금형, 정밀 수직 드릴링 라인 실물 사진 4종 쇼케이스", "• 직영 공장 인프라 쇼케이스: ")
    add_bullet("소구경 확관, 축관(스웨이징), CNC 밴딩, 복합 임가공의 보유 라인, 규격 범위(22Φ~50Φ), 허용 공차 요약표 수록", "• 핵심 설비 제원표: ")
    add_bullet("공장 직영 원가 절감(15%+), 정밀 금형 공차(±0.1mm), 무상 초도 샘플 제작, 24시간 신속 견적", "• 4대 핵심 가치: ")

    add_h2("Page 2: 핵심 가공 기술 제원 1 - 소구경 확관 & 축관 (22Φ ~ 50Φ)")
    add_bullet("소구경 확관/비딩 정밀 CAD 규격도(fax_cad_pipe_forming_bead.png) 적용, 단차 턱 성형 및 슬리브 결합 사양", "• 01 소구경 파이프 확관: ")
    add_bullet("22Φ, 25Φ, 38Φ, 50Φ (단부 가공 50mm 이하, 두께 0.7~2.3t, 허용 공차 ±0.10mm), 실물 샘플 3종 갤러리", "• 확관 스펙 & 갤러리: ")
    add_bullet("사용자 지정 공식 규격도(fax_cad_pipe_specs.png) 적용, 22Φ~50Φ(길이 400mm 이하, 단부 50mm 이하) 스웨이징", "• 02 소구경 파이프 축관: ")
    add_bullet("22Φ, 25Φ, 38Φ, 50Φ 원추 테이퍼(공차 ±0.08~±0.10mm), 철재 가구 다리/기계 부품 샘플 3종 갤러리", "• 축관 스펙 & 갤러리: ")

    add_h2("Page 3: 핵심 가공 기술 제원 2 - CNC 밴딩 & 복합 정밀 임가공")
    add_bullet("정밀 밴딩 CAD 규격도(fax_cad_pipe_bending.png) 적용, 원형 22Φ~50Φ / 각파이프 20~40각, 1°~180° 곡선 가공", "• 03 CNC 파이프 밴딩: ")
    add_bullet("맨드릴 내부 지지 주름 방지 가공, 가구 프레임 밴딩품 실물 3종 갤러리", "• 밴딩 스펙 & 갤러리: ")
    add_bullet("정밀 드릴링 CAD 규격도(fax_cad_pipe_drillijg.png) 적용, 고속 절단, 면취, 프레스 펀칭 홀타공, 수직 드릴링", "• 04 복합 정밀 임가공: ")
    add_bullet("원자재 입고검사 → 정밀절단·면취 → 확관/축관/밴딩 → 드릴링·타공 → 용접조립 → 전수검사·출하 6단계 일관 공정", "• One-Stop 공정 흐름도: ")

    add_h2("Page 4: 실물 생산 갤러리 & B2B 맞춤 견적 의뢰서 & 오시는 길")
    add_bullet("정밀 조립 파이프, 구조용 체결관, 단차 확관, 다단 밴딩, 슬림 원추 축관, 특수 주문 맞춤품 6종 실물 타일", "• 15종 생산 갤러리: ")
    add_bullet("소구경 규격(22Φ, 25Φ, 38Φ, 50Φ, 길이 400mm 이하) 맞춤 발주 양식 수록 (인쇄/FAX/온라인)", "• B2B 즉시 견적 의뢰서: ")
    add_bullet("직영 공장 위치(경기도 시흥시 범안로390번길 63), 직통전화(010-9014-9373), 대표전화(031-432-9373), 카탈로그 웹 링크", "• 직영 공장 콘택트 배너: ")

    # 3. 파일 연동 및 배포 현황
    add_h1("3. 관련 파일 연동 및 배포 동기화 현황")
    
    # Table
    table = doc.add_table(rows=1, cols=3)
    table.autofit = False
    
    # Header row
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "구분 및 대상 파일"
    hdr_cells[1].text = "반영 작업 내용"
    hdr_cells[2].text = "상태"
    for cell in hdr_cells:
        cell_xml = cell._tc.get_or_add_tcPr()
        shd = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
        cell_xml.append(shd)
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.name = '맑은 고딕'
                r.font.size = Pt(9.5)
                r.bold = True
                r._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

    data = [
        ("catalog/index_brochure.html", "소구경(22Φ~50Φ) CAD 규격도 및 제원표 전면 개정 반영 (47.4 KB)", "완료"),
        ("catalog/images/cad/", "fax_cad_pipe_specs.png 외 공식 소구경 CAD 규격 이미지 5종 배치", "완료"),
        ("index_dashboard.html", "상단 헤더 퀵버튼 및 대시보드 퀵메뉴 링크를 정식 브로슈어로 연결 갱신", "완료"),
        ("plan/dhsteel_plan_2026.html", "마스터플랜 헤더 네비게이션에 [📄 공식 브로슈어 ↗] 바로가기 추가", "완료"),
        ("dist_deploy (209개 파일 / 58.44MB)", "새 브로슈어 및 CAD 이미지 전체 동기화 빌드 완료", "배포 준비 완료")
    ]

    for item in data:
        row_cells = table.add_row().cells
        row_cells[0].text = item[0]
        row_cells[1].text = item[1]
        row_cells[2].text = item[2]
        for idx, cell in enumerate(row_cells):
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = '맑은 고딕'
                    r.font.size = Pt(9)
                    if idx == 2:
                        r.bold = True
                        r.font.color.rgb = RGBColor(0x05, 0x96, 0x69)
                    r._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

    output_path = r'e:\Antigravity\builder-dhsteel-sales\workflow\2026-11-23_dhsteel_brochure_creation_report.docx'
    doc.save(output_path)
    print(f"Report saved to {output_path}")

if __name__ == '__main__':
    create_report()
