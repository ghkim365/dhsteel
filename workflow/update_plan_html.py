# -*- coding: utf-8 -*-
with open('plan/dhsteel_plan_2026.html', 'r', encoding='utf-8') as f:
    plan = f.read()

# 1. Update stats grid
old_stats = """  <!-- Key Stats Grid -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="label">웹 인프라 상태</div>
      <div class="val" style="color:#2563EB;">Cloudflare</div>
      <div class="desc">dhsteel.pages.dev (Vercel 탈피)</div>
    </div>
    <div class="stat-card">
      <div class="label">독립 배포 패키지</div>
      <div class="val">46.2 MB</div>
      <div class="desc">176개 파일 (dist_deploy 초경량화)</div>
    </div>
    <div class="stat-card">
      <div class="label">B2B 이메일 발송 현황</div>
      <div class="val" style="color:#10B981;">95.7%</div>
      <div class="desc">70건 발송 / 67건 성공 (11/09)</div>
    </div>
    <div class="stat-card">
      <div class="label">B2B 팩스 발송 현황</div>
      <div class="val" style="color:#059669;">93.1%</div>
      <div class="desc">29건 발송 / 27건 성공 (11/16)</div>
    </div>
  </div>"""

new_stats = """  <!-- Key Stats Grid -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="label">웹 인프라 상태</div>
      <div class="val" style="color:#2563EB;">Cloudflare</div>
      <div class="desc">dhsteel.pages.dev (Vercel 탈피)</div>
    </div>
    <div class="stat-card">
      <div class="label">독립 배포 패키지</div>
      <div class="val">58.00 MB</div>
      <div class="desc">209개 파일 (dist_deploy 최신 동기화)</div>
    </div>
    <div class="stat-card">
      <div class="label">B2B 이메일 발송 현황</div>
      <div class="val" style="color:#10B981;">100%</div>
      <div class="desc">68건 발송 / 68건 전건 성공 (11/23)</div>
    </div>
    <div class="stat-card">
      <div class="label">B2B 팩스 발송 현황</div>
      <div class="val" style="color:#059669;">93.1%</div>
      <div class="desc">29건 발송 / 27건 성공 (11/16)</div>
    </div>
  </div>"""

if old_stats in plan:
    plan = plan.replace(old_stats, new_stats)
    print("Stats grid updated successfully!")
else:
    print("Warning: old_stats not found!")

# 2. Update Tab Title from (Phase 1~18) to (Phase 1~20)
plan = plan.replace("📋 1. 프로젝트 통합 작업 계획 &amp; 이력 (Phase 1~18)",
                    "📋 1. 프로젝트 통합 작업 계획 &amp; 이력 (Phase 1~20)")
plan = plan.replace("<!-- TAB 1: 통합 작업 계획 & 이력 (Phase 1 ~ 18) -->",
                    "<!-- TAB 1: 통합 작업 계획 & 이력 (Phase 1 ~ 20) -->")

# 3. Update Phase 19 and Insert Phase 20
old_ph19 = """    <!-- PHASE 19 (2026-11-23) -->
    <div class="card" style="border: 2px solid #10B981;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;"><span class="badge badge-success">PHASE 19</span> 검증 우량 68개사 3차 정기 이메일 발송 준비 완료</h2>
        <span style="font-size:12px; color:#10B981; font-weight:700;">2026-11-23 발송 대기</span>
      </div>
      <div class="tip-box green" style="margin-top:12px;">
        • <strong>3차 정기 메일 타겟 확정</strong>: 11/09 성공 67개사 + 코베아(오타 정제) 총 68개사 선별 완료<br>
        • <strong>구글 시트 연동</strong>: '2026-11-23' 전용 워크시트 생성 및 'company' 시트 68개사 A열 TRUE / M열 '3차 정기(11/23)' 세팅 완료<br>
        • <strong>인프라 연동</strong>: 11/20 구축된 Cloudflare Pages(dhsteel.pages.dev) CDN 템플릿(dhsteel_proposal_v2.html) 기반 첫 정기 발송<br>
        • <strong>보고서 발행</strong>: workflow/2026-11-23_dhsteel_mail_plan_batch3.docx 표준 워드 보고서 발행 완료
      </div>
      <ul class="checklist">
        <li class="task-item"><input type="checkbox" id="ph19-target-68" checked><span class="task-text"><strong>[타겟 선별]</strong> 11/09 성공군 + 코베아 오타 정제 68개사 확정</span><input type="date" class="task-date-input" id="ph19-target-68-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-target-68-memo" value="검증 성공군 67건 + 코베아 복구"></li>
        <li class="task-item"><input type="checkbox" id="ph19-sheet-20261123" checked><span class="task-text"><strong>[시트 연동]</strong> '2026-11-23' 워크시트 생성 및 68개사 A열 TRUE / M열 회차 세팅</span><input type="date" class="task-date-input" id="ph19-sheet-20261123-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-sheet-20261123-memo" value="company 시트 68개사 동기화 완료"></li>
        <li class="task-item"><input type="checkbox" id="ph19-report-docx" checked><span class="task-text"><strong>[보고서 발행]</strong> 2026-11-23_dhsteel_mail_plan_batch3.docx 워드 보고서 생성</span><input type="date" class="task-date-input" id="ph19-report-docx-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-report-docx-memo" value="맑은 고딕 10pt 표준 서식 발행"></li>
        <li class="task-item"><input type="checkbox" id="ph19-mail-trigger"><span class="task-text"><strong>[발송 집행]</strong> 구글 시트 상단 메뉴 [대흥 아웃바운드] 원클릭 일괄 발송 집행</span><input type="date" class="task-date-input" id="ph19-mail-trigger-date"><input type="text" class="task-memo-input" id="ph19-mail-trigger-memo" value="Gmail API 3초 간격 일괄 전송 대기"></li>
      </ul>
    </div>"""

new_ph20_and_ph19 = """    <!-- PHASE 20 (NEW - 2026-11-23) -->
    <div class="card" style="border: 2px solid #2563EB;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;"><span class="badge badge-primary">PHASE 20</span> B2B 브로슈어 신규 제작 및 메일·팩스 보고서 UI 디자인 전면 리뉴얼</h2>
        <span style="font-size:12px; color:#2563EB; font-weight:700;">2026-11-23 완료</span>
      </div>
      <div class="tip-box green" style="margin-top:12px;">
        • <strong>B2B 공식 브로슈어 신규 제작 (catalog/index_brochure.html)</strong>: 삼협철망 스타일 벤치마킹 4페이지 A4 인쇄/스크린 규격 브로슈어 완성. 소구경 2차 정밀 임가공(22Φ~50Φ) CAD 도면 기술 그래픽(성형 비드, 규격표) 전면 적용 완료<br>
        • <strong>보고서 2종 디자인 UI 전면 리뉴얼 (mail_report.html, fax_report.html)</strong>: Pretendard 웹폰트 및 Semi-bold(600) 타이포그래피 전환, 두꺼운 볼드 제거<br>
        • <strong>가로 너비 1020px 수직 플러시 정렬</strong>: 상단 컨트롤 패널, 탭 메뉴, 본문 A4 영역을 1020px로 통일하여 좌우 여백 불일치 및 좁음 현상 완전 해소<br>
        • <strong>폰트 크기 확대 및 JS 인라인 폰트 전면 수정</strong>: 본문 13px, 표 12.5px~13.5px, 컨트롤 패널 13.5px로 확대 및 JS renderTable 내 인라인 font-size(10px) 전면 수정 반영<br>
        • <strong>반복 중복 문구 상단 일괄 통합</strong>: 표 내부의 '(샌드랩스 대량 팩스)', 'Gmail API 발송 완료' 제거 및 상단 메타 바 일괄 표기로 가독성 극대화 및 줄바꿈(nowrap) 방지<br>
        • <strong>로컬 환경 캔버스 이미지 저장 보안 처리</strong>: 공식 심볼 로고를 Base64 인라인 Data URI로 탑재하여 file:/// 환경 Tainted canvas 보안 오류 차단<br>
        • <strong>삼협철망(builder-samhyup-sales) UI 리뉴얼 이식 인프라 구축</strong>: 타임스탬프 원본 백업 지침, 작업 지침서(MD/DOCX), 원클릭 자동 백업/리뉴얼 스크립트 구축 완료
      </div>
      <ul class="checklist">
        <li class="task-item"><input type="checkbox" id="ph20-brochure-create" checked><span class="task-text"><strong>[B2B 브로슈어]</strong> catalog/index_brochure.html 4페이지 A4 인쇄형 제작 및 소구경 CAD 그래픽 탑재</span><input type="date" class="task-date-input" id="ph20-brochure-create-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph20-brochure-create-memo" value="삼협철망 벤치마킹 기술도면 완비"></li>
        <li class="task-item"><input type="checkbox" id="ph20-reports-ui-renewal" checked><span class="task-text"><strong>[리포트 UI 리뉴얼]</strong> mail_report.html &amp; fax_report.html 1020px 정렬 + Pretendard Semi-bold 적용</span><input type="date" class="task-date-input" id="ph20-reports-ui-renewal-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph20-reports-ui-renewal-memo" value="가로폭 1020px 수직 플러시 정렬"></li>
        <li class="task-item"><input type="checkbox" id="ph20-js-inline-font" checked><span class="task-text"><strong>[JS 폰트 확대]</strong> JS renderTable 내 인라인 10px 제거 ➔ 12.5px~13.5px 확대 및 줄바꿈(nowrap) 방지</span><input type="date" class="task-date-input" id="ph20-js-inline-font-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph20-js-inline-font-memo" value="실시간 렌더링 글자 확대 반영"></li>
        <li class="task-item"><input type="checkbox" id="ph20-redundancy-clean" checked><span class="task-text"><strong>[중복 문구 정제]</strong> (샌드랩스 대량 팩스), Gmail API 발송 완료 표 내부 제거 및 상단 일괄 통합</span><input type="date" class="task-date-input" id="ph20-redundancy-clean-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph20-redundancy-clean-memo" value="시각적 피로도 해소 및 공간 확보"></li>
        <li class="task-item"><input type="checkbox" id="ph20-canvas-security" checked><span class="task-text"><strong>[로고 보안 처리]</strong> Base64 인라인 로고 탑재로 file:/// 캔버스 PDF/이미지 저장 보안 에러 해결</span><input type="date" class="task-date-input" id="ph20-canvas-security-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph20-canvas-security-memo" value="Tainted canvas 오류 차단"></li>
        <li class="task-item"><input type="checkbox" id="ph20-samhyup-infra" checked><span class="task-text"><strong>[삼협철망 인프라]</strong> 삼협철망 전용 백업 원칙, UI 리뉴얼 지침서(MD/DOCX) 및 자동 스크립트 작성</span><input type="date" class="task-date-input" id="ph20-samhyup-infra-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph20-samhyup-infra-memo" value="E:/Antigravity/builder-samhyup-sales 저장 완료"></li>
        <li class="task-item"><input type="checkbox" id="ph20-dist-deploy-sync" checked><span class="task-text"><strong>[배포 동기화]</strong> build_dist_deploy.py 실행 및 dist_deploy 209개 파일(58.00 MB) 빌드 완료</span><input type="date" class="task-date-input" id="ph20-dist-deploy-sync-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph20-dist-deploy-sync-memo" value="209개 파일 58.00MB 동기화 완료"></li>
      </ul>
    </div>

    <!-- PHASE 19 (2026-11-23) -->
    <div class="card" style="border: 2px solid #10B981;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;"><span class="badge badge-success">PHASE 19</span> 검증 우량 68개사 3차 정기 이메일 발송 집행 및 전수 검증 완료</h2>
        <span style="font-size:12px; color:#10B981; font-weight:700;">2026-11-23 완료</span>
      </div>
      <div class="tip-box green" style="margin-top:12px;">
        • <strong>3차 정기 메일 타겟 확정</strong>: 11/09 성공 67개사 + 코베아(오타 정제) 총 68개사 선별 완료<br>
        • <strong>발송 집행 및 100% 성공</strong>: 11/23 오전 10:14~10:15 Gmail API 68건 전건 성공 (에러 0건, 서부금속산업 QQ메일 자동회신 수신 확인)<br>
        • <strong>구글 시트 연동</strong>: '2026-11-23' 워크시트 생성 및 'mail_log → company' 207개사 동기화 완료<br>
        • <strong>보고서 발행</strong>: workflow/2026-11-23_dhsteel_mail_plan_batch3.docx 표준 워드 보고서 발행 완료
      </div>
      <ul class="checklist">
        <li class="task-item"><input type="checkbox" id="ph19-target-68" checked><span class="task-text"><strong>[타겟 선별]</strong> 11/09 성공군 + 코베아 오타 정제 68개사 확정</span><input type="date" class="task-date-input" id="ph19-target-68-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-target-68-memo" value="검증 성공군 67건 + 코베아 복구"></li>
        <li class="task-item"><input type="checkbox" id="ph19-sheet-20261123" checked><span class="task-text"><strong>[시트 연동]</strong> '2026-11-23' 워크시트 생성 및 68개사 A열 TRUE / M열 회차 세팅</span><input type="date" class="task-date-input" id="ph19-sheet-20261123-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-sheet-20261123-memo" value="company 시트 68개사 동기화 완료"></li>
        <li class="task-item"><input type="checkbox" id="ph19-report-docx" checked><span class="task-text"><strong>[보고서 발행]</strong> 2026-11-23_dhsteel_mail_plan_batch3.docx 워드 보고서 생성</span><input type="date" class="task-date-input" id="ph19-report-docx-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-report-docx-memo" value="맑은 고딕 10pt 표준 서식 발행"></li>
        <li class="task-item"><input type="checkbox" id="ph19-mail-trigger" checked><span class="task-text"><strong>[발송 집행]</strong> 구글 시트 상단 메뉴 [대흥 아웃바운드] 원클릭 일괄 발송 집행</span><input type="date" class="task-date-input" id="ph19-mail-trigger-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-mail-trigger-memo" value="Gmail API 68건 전건 성공 (성공률 100%)"></li>
      </ul>
    </div>"""

if old_ph19 in plan:
    plan = plan.replace(old_ph19, new_ph20_and_ph19)
    print("Phase 19 updated and Phase 20 inserted successfully!")
else:
    print("Warning: old_ph19 not found!")

with open('plan/dhsteel_plan_2026.html', 'w', encoding='utf-8') as f:
    f.write(plan)

print("dhsteel_plan_2026.html update completed!")

