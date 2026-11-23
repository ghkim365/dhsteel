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
    t_run = title_p.add_run("대흥정밀 마스터플랜(dhsteel_plan_2026.html) 2026-11-23 작업 내역 갱신 보고서")
    t_run.font.name = '맑은 고딕'
    t_run.font.size = Pt(16)
    t_run.bold = True
    t_run.font.color.rgb = RGBColor(0x15, 0x28, 0x4D)
    t_run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(12)
    s_run = sub_p.add_run("PHASE 19 발송 완료 100% 검증 · PHASE 20 브로슈어 & 보고서 UI 리뉴얼 · 삼협철망 인프라 구축 완료 | 2026-11-23")
    s_run.font.name = '맑은 고딕'
    s_run.font.size = Pt(9.5)
    s_run.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
    s_run._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은 고딕')

    # Divider
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(8)
    p_div_border = parse_xml(r'<w:pBdr {}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="2563EB"/></w:pBdr>'.format(nsdecls('w')))
    p_div._p.get_or_add_pPr().append(p_div_border)

    # 1. 개요
    add_h1("1. 마스터플랜 갱신 개요 및 상단 지표 최신화")
    add_p("오늘(2026-11-23) 대흥정밀 프로젝트에서 수행된 B2B 아웃바운드 3차 정기 발송 전수 집행, B2B 공식 브로슈어 신규 제작, 보고서 2종 디자인 UI 전면 리뉴얼, 삼협철망 프로젝트 이식 인프라 구축 내역을 통합 마스터플랜(plan/dhsteel_plan_2026.html)에 완벽하게 반영하였습니다.")
    add_bullet("독립 배포 패키지: 46.2 MB(176개) ➔ 58.01 MB(209개 파일, 최신 배포 패키지 동기화 및 GitHub 배포 완료)", "• 배포 패키지 현황: ")
    add_bullet("B2B 이메일 발송 현황: 68건 발송 중 66건 성공 (성공률 97.1%), 2건 반송 자동 감지 및 시트 실패 실시간 갱신 완료", "• 이메일 성과 지표: ")
    add_bullet("탭 타이틀 표기: '프로젝트 통합 작업 계획 & 이력 (Phase 1~18)' ➔ '(Phase 1~20)' 확장", "• 작업 계획 확장: ")

    # 2. 신규 Phase 상세 내역
    add_h1("2. Phase 19 및 Phase 20 반영 내역")
    
    add_h2("가. PHASE 19: 검증 우량 68개사 3차 정기 이메일 발송 집행 및 반송 자동감지 완료")
    add_bullet("사전 불량 업체(아이디오, 금경이노텍) 제외 및 코베아(kovea.co.kr) 오타 정제 완료", "• 타겟 확정: ")
    add_bullet("11/23 오전 10:14~10:15 Gmail API 68건 송신 완료 (서부금속산업 QQ메일 자동회신 수신 확인)", "• 발송 집행: ")
    add_bullet("13:21 GAS 반송 메일 감지 엔진(scanBounceEmails) 가동, 지연 반송 2건 자동 감지 (코베아 일시 오류, 코리아세일즈 계정 없음)", "• 반송 자동감지: ")
    add_bullet("구글 스프레드시트 mail_log(472·474행) 및 company(211·213행) 실패 자동 갱신 완료 ➔ 최종 66건 성공 (도달률 97.1%)", "• 시트 동기화: ")

    add_h2("나. PHASE 20: B2B 브로슈어 신규 제작 및 메일·팩스 보고서 UI 디자인 전면 리뉴얼")
    add_bullet("catalog/index_brochure.html 제작, 소구경(22Φ~50Φ) CAD 도면 기술 그래픽 전면 적용", "• B2B 공식 브로슈어: ")
    add_bullet("상단 컨트롤러, 탭, A4 본문을 1020px로 수직 플러시 정렬하여 좌우 여백 불일치 해소", "• 1020px 가로폭 정렬: ")
    add_bullet("Pretendard 웹폰트 및 Semi-bold(600) 타이포그래피 전환, 두꺼운 볼드 제거", "• 타이포그래피 혁신: ")
    add_bullet("본문 13px, 표 12.5px~13.5px 확대 및 JS renderTable 내 인라인 폰트(10px) 전면 수정", "• 글자 크기 가독성 확대: ")
    add_bullet("표 내부의 중복 문구('(샌드랩스 대량 팩스)', 'Gmail API 발송 완료') 제거 및 상단 일괄 표기", "• 중복 문구 정제: ")
    add_bullet("공식 심볼 로고를 Base64 인라인 Data URI로 탑재하여 file:/// 환경 Tainted canvas 보안 오류 차단", "• 캔버스 로고 보안 처리: ")
    add_bullet("삼협철망(builder-samhyup-sales) 전용 작업 지침서(MD/DOCX) 및 자동 백업/리뉴얼 스크립트 구축 완료", "• 삼협철망 인프라 구축: ")

    # 3. 배포 현황
    add_h1("3. 배포 패키지 및 관련 산출물 현황")
    
    table = doc.add_table(rows=1, cols=3)
    table.autofit = False
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "파일명 및 경로"
    hdr_cells[1].text = "작업 내용"
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
        ("plan/dhsteel_plan_2026.html", "Phase 19 완료 갱신 + Phase 20 신설 + 상단 통계(68건 100%, 58MB) 갱신", "반영 완료"),
        ("dist_deploy/plan/dhsteel_plan_2026.html", "배포 패키지 동기화 빌드 완료 (209개 파일, 58.00 MB)", "배포 완료"),
        ("E:/Antigravity/builder-samhyup-sales/workflow/", "삼협철망 전용 작업 지침서(MD/DOCX) 및 자동 백업/리뉴얼 스크립트", "저장 완료")
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

    output_path = r'e:\Antigravity\builder-dhsteel-sales\workflow\2026-11-23_dhsteel_master_plan_update.docx'
    doc.save(output_path)
    print(f"Report saved to {output_path}")

if __name__ == '__main__':
    create_report()

