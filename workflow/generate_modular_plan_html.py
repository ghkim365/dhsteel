# -*- coding: utf-8 -*-
"""
generate_modular_plan_html.py
대흥정밀 마스터 플랜을 퍼시스스토어 스타일의 5대 독립 탭(Tab) 구조로 모듈화 개편
1. [📋 1. 프로젝트 통합 작업 계획 & 이력 (Phase 1~18)]
2. [☁️ 2. Cloudflare Pages 등록·배포 완벽 매뉴얼 (2026-11-20)]
3. [📬 3. B2B 이메일 발송 자동화 및 템플릿·도메인 관리]
4. [📠 4. B2B 팩스 대량 발송 운영 체계 & 센드랩스 연동]
5. [📖 5. B2B 정기 발송 표준운영절차 (SOP)]
"""

import os, sys

sys.stdout.reconfigure(encoding='utf-8')

plan_path = r'E:\Antigravity\builder-dhsteel-sales\plan\dhsteel_plan_2026.html'

html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>대흥정밀 B2B 마케팅 &amp; 인프라 마스터 플랜 2026</title>
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <style>
    :root {
      --primary: #1C2B4A;
      --primary-light: #2C3E6A;
      --accent: #2563EB;
      --accent-light: #3B82F6;
      --bg: #F8FAFC;
      --card-bg: #FFFFFF;
      --text-main: #0F172A;
      --text-muted: #64748B;
      --border: #E2E8F0;
      --border-dark: #CBD5E1;
      --success: #10B981;
      --warning: #F59E0B;
      --danger: #EF4444;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text-main);
      line-height: 1.6;
      padding: 30px 20px;
    }
    .container {
      max-width: 1280px;
      margin: 0 auto;
    }
    
    /* Header - Clean Light Theme */
    .header-panel {
      background: #FFFFFF;
      color: #0F172A;
      border: 1px solid var(--border);
      padding: 26px 30px;
      border-radius: 14px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }
    .header-title h1 {
      font-size: 24px;
      font-weight: 800;
      color: #1C2B4A;
      letter-spacing: -0.5px;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .header-title p {
      color: #64748B;
      font-size: 13.5px;
    }
    .header-links {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .header-btn {
      background: #F8FAFC;
      color: #334155;
      border: 1.5px solid #CBD5E1;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .header-btn:hover {
      background: #E2E8F0;
      color: #0F172A;
      transform: translateY(-1px);
    }
    .header-btn.primary {
      background: #2563EB;
      color: #FFFFFF;
      border-color: #2563EB;
      box-shadow: 0 2px 6px rgba(37, 99, 235, 0.25);
    }
    .header-btn.primary:hover {
      background: #1D4ED8;
      color: #FFFFFF;
    }

    /* Tab Navigation Styles (Fursys-Store Mirror) */
    .plan-tab-nav {
      display: flex;
      gap: 8px;
      margin-top: 10px;
      margin-bottom: 24px;
      border-bottom: 2px solid #E2E8F0;
      padding-bottom: 0;
      flex-wrap: wrap;
    }
    .plan-tab-btn {
      padding: 13px 22px;
      font-size: 14.5px;
      font-weight: 700;
      color: #64748B;
      background: #F1F5F9;
      border: 1px solid #CBD5E1;
      border-bottom: none;
      border-radius: 10px 10px 0 0;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      text-decoration: none;
    }
    .plan-tab-btn:hover {
      background: #E2E8F0;
      color: #0F172A;
    }
    .plan-tab-btn.active {
      background: #FFFFFF;
      color: #2563EB;
      border-color: #2563EB #2563EB #FFFFFF;
      border-top: 3.5px solid #2563EB;
      margin-bottom: -2px;
      font-weight: 800;
      box-shadow: 0 -4px 10px rgba(37, 99, 235, 0.08);
    }
    
    .plan-tab-pane {
      display: none;
    }
    .plan-tab-pane.active {
      display: block;
    }

    /* Cards & Content */
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 26px 30px;
      margin-bottom: 20px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
    }
    .card-title {
      font-size: 18px;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
      border-bottom: 1.5px solid #F1F5F9;
      padding-bottom: 10px;
    }
    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 700;
    }
    .badge-primary { background: #E0E7FF; color: #3730A3; }
    .badge-success { background: #DCFCE7; color: #166534; }
    .badge-warning { background: #FEF3C7; color: #92400E; }
    .badge-info { background: #E0F2FE; color: #075985; }

    /* Tables */
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0 20px 0;
      font-size: 13.5px;
    }
    table.data-table th, table.data-table td {
      padding: 11px 14px;
      border: 1px solid var(--border);
      text-align: left;
    }
    table.data-table th {
      background-color: #F8FAFC;
      color: #334155;
      font-weight: 700;
    }
    table.data-table tr:hover td {
      background-color: #F8FAFC;
    }

    /* Checklist */
    ul.checklist {
      list-style: none;
      margin: 12px 0;
    }
    ul.checklist li {
      padding: 10px 14px;
      border-bottom: 1px solid #F1F5F9;
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 13.5px;
    }
    ul.checklist li:last-child {
      border-bottom: none;
    }
    .task-item input[type="checkbox"] {
      width: 17px;
      height: 17px;
      cursor: pointer;
      accent-color: var(--accent);
    }
    .task-text {
      flex: 1;
    }
    .task-date-input, .task-memo-input {
      padding: 4px 8px;
      border: 1px solid #CBD5E1;
      border-radius: 4px;
      font-size: 12px;
      color: #475569;
    }
    .task-date-input { width: 125px; }
    .task-memo-input { width: 280px; }

    /* Tip Boxes & Code */
    .tip-box {
      background: #F0F9FF;
      border-left: 4px solid #0284C7;
      padding: 14px 18px;
      border-radius: 0 8px 8px 0;
      font-size: 13px;
      color: #0369A1;
      margin: 14px 0;
      line-height: 1.6;
    }
    .tip-box.green {
      background: #F0FDF4;
      border-left-color: #16A34A;
      color: #15803D;
    }
    .tip-box.yellow {
      background: #FEFCE8;
      border-left-color: #CA8A04;
      color: #854D0E;
    }
    code {
      font-family: "JetBrains Mono", Consolas, monospace;
      background: #F1F5F9;
      color: #2563EB;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 12.5px;
      font-weight: 600;
    }
    pre {
      background: #F8FAFC;
      color: #1E293B;
      border: 1px solid #E2E8F0;
      padding: 16px 20px;
      border-radius: 10px;
      font-family: "JetBrains Mono", Consolas, monospace;
      font-size: 12.5px;
      overflow-x: auto;
      margin: 14px 0;
      line-height: 1.5;
    }
    
    /* Stats Grid */
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
      margin-bottom: 24px;
    }
    .stat-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 18px 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .stat-card .label {
      font-size: 12.5px;
      color: var(--text-muted);
      font-weight: 600;
      margin-bottom: 6px;
    }
    .stat-card .val {
      font-size: 24px;
      font-weight: 800;
      color: var(--primary);
    }
    .stat-card .desc {
      font-size: 11.5px;
      color: #94A3B8;
      margin-top: 4px;
    }
  </style>
</head>
<body>

<div class="container">

  <!-- Header -->
  <div class="header-panel">
    <div class="header-title">
      <h1>🏭 대흥정밀 B2B 마케팅 &amp; 인프라 마스터 플랜 2026</h1>
      <p>Cloudflare Pages 이전 완료 • 파이프 임가공 아웃바운드(메일/팩스) 자동화 및 인프라 통합 관제</p>
    </div>
    <div class="header-links">
      <a href="https://dhsteel.pages.dev" target="_blank" class="header-btn primary">🌐 대시보드 바로가기 ↗</a>
      <a href="https://dhsteel.pages.dev/catalog/index_catalog.html" target="_blank" class="header-btn">📱 e-카탈로그 ↗</a>
      <a href="https://dhsteel.pages.dev/mailling/mail_report.html" target="_blank" class="header-btn">✉️ 메일 리포트 ↗</a>
      <a href="https://dhsteel.pages.dev/fax/fax_report.html" target="_blank" class="header-btn">📠 팩스 리포트 ↗</a>
    </div>
  </div>

  <!-- Key Stats Grid -->
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
  </div>

  <!-- Tab Controls (Fursys-Store Mirror) -->
  <div class="plan-tab-nav">
    <button type="button" class="plan-tab-btn active" onclick="switchPlanTab('tab-history')">
      📋 1. 프로젝트 통합 작업 계획 &amp; 이력 (Phase 1~18)
    </button>
    <button type="button" class="plan-tab-btn" onclick="switchPlanTab('tab-deploy')">
      ☁️ 2. Cloudflare Pages 배포 매뉴얼 (2026-11-20 인프라 이전)
    </button>
    <button type="button" class="plan-tab-btn" onclick="switchPlanTab('tab-mail')">
      📬 3. B2B 이메일 발송 자동화 및 템플릿·도메인 관리
    </button>
    <button type="button" class="plan-tab-btn" onclick="switchPlanTab('tab-fax')">
      📠 4. B2B 팩스 대량 발송 운영 체계 &amp; 센드랩스 연동
    </button>
    <button type="button" class="plan-tab-btn" onclick="switchPlanTab('tab-sop')">
      📖 5. B2B 정기 발송 표준운영절차 (SOP)
    </button>
  </div>

  <!-- ============================================================== -->
  <!-- TAB 1: 통합 작업 계획 & 이력 (Phase 1 ~ 18) -->
  <!-- ============================================================== -->
  <div id="tab-history" class="plan-tab-pane active">
    
    <!-- PHASE 18 (NEW - 2026-11-20) -->
    <div class="card" style="border: 2px solid #2563EB;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;"><span class="badge badge-primary">PHASE 18</span> Cloudflare Pages 인프라 이전 및 파일명 표준화·배포 검증 완료</h2>
        <span style="font-size:12px; color:#2563EB; font-weight:700;">2026-11-20 완료</span>
      </div>
      <div class="tip-box green" style="margin-top:12px;">
        • <strong>Cloudflare Pages 인프라 이전</strong>: 기존 Vercel(<code>dhsteel.vercel.app</code>)에서 Cloudflare Pages(<code>dhsteel.pages.dev</code>)로 완전히 이전하여 대역폭 및 배포 속도 대폭 개선<br>
        • <strong>파일명 표준화</strong>: <code>index_dashboard.html</code>, <code>catalog/index_catalog.html</code>, 루트 <code>index.html</code> 리다이렉터 체계 정립<br>
        • <strong>배포 패키지 경량화</strong>: 200MB가 넘던 디버그 캐시 삭제 및 46.2MB(176개 파일) 규모의 <code>dist_deploy/</code> 자동 빌드 시스템 구축<br>
        • <strong>대시보드 UI 삼협철망 스타일 고도화</strong>: 관리자 인증 모달 상단 CI 로고, 모바일 카탈로그 &amp; 제안서 바로가기, 상단 퀵 버튼 2종, 에러 리포트 다크네이비 톤 다운 완료<br>
        • <strong>이메일 발송 도메인 57개소 전수 전환</strong>: 제안서 템플릿 내 이미지/링크 및 GAS 연동 주소를 <code>https://dhsteel.pages.dev</code>로 일괄 갱신<br>
        • <strong>라이브 배포 전수 검증 통과</strong>: 메인, 대시보드, 카탈로그, 마스터플랜, 메일/팩스 리포트 및 이미지 서빙 등 전 항목 HTTP 200 검증 완료
      </div>
      <ul class="checklist">
        <li class="task-item"><input type="checkbox" id="ph18-infra-migration"><span class="task-text"><strong>[인프라 이전]</strong> Cloudflare Pages 인프라 이전 및 dhsteel.pages.dev 라이브 오픈</span><input type="date" class="task-date-input" id="ph18-infra-migration-date"><input type="text" class="task-memo-input" id="ph18-infra-migration-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph18-file-standardize"><span class="task-text"><strong>[파일명 표준화]</strong> index_dashboard.html / index_catalog.html / 루트 index.html 표준화</span><input type="date" class="task-date-input" id="ph18-file-standardize-date"><input type="text" class="task-memo-input" id="ph18-file-standardize-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph18-dist-deploy-build"><span class="task-text"><strong>[패키지 구축]</strong> build_dist_deploy.py 빌드 스크립트 작성 및 46.2MB 초경량 dist_deploy 구축</span><input type="date" class="task-date-input" id="ph18-dist-deploy-build-date"><input type="text" class="task-memo-input" id="ph18-dist-deploy-build-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph18-dashboard-ui-polish"><span class="task-text"><strong>[대시보드 UI]</strong> 인증창 로고, 카탈로그 바로가기, 상단 퀵버튼 2종, 에러버튼 톤다운 완료</span><input type="date" class="task-date-input" id="ph18-dashboard-ui-polish-date"><input type="text" class="task-memo-input" id="ph18-dashboard-ui-polish-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph18-email-domain-sync"><span class="task-text"><strong>[이메일 도메인]</strong> 메일 템플릿(dhsteel_proposal_v2.html) 및 GAS 내 57개소 도메인 전환</span><input type="date" class="task-date-input" id="ph18-email-domain-sync-date"><input type="text" class="task-memo-input" id="ph18-email-domain-sync-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph18-live-audit-pass"><span class="task-text"><strong>[라이브 검증]</strong> Cloudflare Pages 전 엔드포인트 HTTP 200 전수 검증 100% 통과</span><input type="date" class="task-date-input" id="ph18-live-audit-pass-date"><input type="text" class="task-memo-input" id="ph18-live-audit-pass-memo"></li>
      </ul>
    </div>

    <!-- PHASE 17 (2026-11-16) -->
    <div class="card" id="sec-ph17">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;"><span class="badge badge-success">PHASE 17</span> 팩스 6회차 검증 30개사 대량 발송 준비 및 집행</h2>
        <span style="font-size:12px; color:#6b7280; font-weight:600;">2026-11-16 완료</span>
      </div>
      <div class="tip-box" style="margin-top:12px;">
        • <strong>팩스 6회차 타겟 확정</strong>: 11/02 수신 성공 22건 + 우량 팩스 고객사 + 메일 차단 전환 아이디오 포함 총 30개사 선별<br>
        • <strong>샌드랩스 업로드 파일 생성</strong>: sales/fax/fax_targets_20261116.xlsx 및 .csv 생성 완료<br>
        • <strong>집행 결과</strong>: 29건 전송 중 27건 성공 (성공률 93.1%), 2건 실패(삼원금속 번호오류, 유풍 무응답)<br>
        • <strong>보고서 발행</strong>: sales/fax/2026-11-16_fax_result_batch6.docx 표준 서식 보고서 발행 완료
      </div>
      <ul class="checklist">
        <li class="task-item"><input type="checkbox" id="ph17-fax-targets-30"><span class="task-text"><strong>[타겟 선별]</strong> 11/02 성공군 및 우량 팩스 고객사 30개사 확정 선별</span><input type="date" class="task-date-input" id="ph17-fax-targets-30-date"><input type="text" class="task-memo-input" id="ph17-fax-targets-30-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph17-sendlabs-files"><span class="task-text"><strong>[발송 파일 생성]</strong> 샌드랩스 대량 업로드용 엑셀(xlsx) 및 CSV 파일 생성 완료</span><input type="date" class="task-date-input" id="ph17-sendlabs-files-date"><input type="text" class="task-memo-input" id="ph17-sendlabs-files-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph17-sheet-20261116"><span class="task-text"><strong>[시트 연동]</strong> '2026-11-16' 전용 시트 생성 및 30개사 발송 회차 세팅</span><input type="date" class="task-date-input" id="ph17-sheet-20261116-date"><input type="text" class="task-memo-input" id="ph17-sheet-20261116-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph17-fax-report-docx"><span class="task-text"><strong>[보고서 발행]</strong> 2026-11-16_fax_result_batch6.docx 워드 보고서 생성 완료</span><input type="date" class="task-date-input" id="ph17-fax-report-docx-date"><input type="text" class="task-memo-input" id="ph17-fax-report-docx-memo"></li>
      </ul>
    </div>

    <!-- PHASE 16 (2026-11-09) -->
    <div class="card" id="sec-ph16">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;"><span class="badge badge-success">PHASE 16</span> 통합 스케줄 대시보드 구축 및 검증 70개사 2차 정기 메일 발송</h2>
        <span style="font-size:12px; color:#6b7280; font-weight:600;">2026-11-09 완료</span>
      </div>
      <div class="tip-box" style="margin-top:12px;">
        • <strong>검증 70개사 타겟 확정</strong>: 7대 필터링(홈페이지 3중검증, 반송이력 배제 등) 통과 70개사 선정<br>
        • <strong>Gmail API 대량 발송</strong>: 70건 발송 중 67건 성공 (도달률 95.7%), 3건 반송 즉시 대응 완료<br>
        • <strong>반송 3건 조치</strong>: 코베아(.co -> .co.kr 도메인 수정), 금경이노텍(퇴사/삭제 계정 확인), 아이디오(팩스 채널로 전환)
      </div>
      <ul class="checklist">
        <li class="task-item"><input type="checkbox" id="ph16-schedule-dashboard"><span class="task-text"><strong>[대시보드 구축]</strong> schedule_dashboard.html 인터랙티브 캘린더 제작</span><input type="date" class="task-date-input" id="ph16-schedule-dashboard-date"><input type="text" class="task-memo-input" id="ph16-schedule-dashboard-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph16-sheet-20261109"><span class="task-text"><strong>[시트 생성]</strong> '2026-11-09' 전용 시트 생성 및 70개사 매핑 완료</span><input type="date" class="task-date-input" id="ph16-sheet-20261109-date"><input type="text" class="task-memo-input" id="ph16-sheet-20261109-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph16-mail-send-70"><span class="task-text"><strong>[메일 발송]</strong> 70개사 전송 집행 (성공 67건, 도달률 95.7%)</span><input type="date" class="task-date-input" id="ph16-mail-send-70-date"><input type="text" class="task-memo-input" id="ph16-mail-send-70-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph16-bounce-refine"><span class="task-text"><strong>[반송 정제]</strong> 코베아 오타 수정, 금경이노텍 플래그, 아이디오 팩스 전환</span><input type="date" class="task-date-input" id="ph16-bounce-refine-date"><input type="text" class="task-memo-input" id="ph16-bounce-refine-memo"></li>
      </ul>
    </div>

    <!-- PHASE 15 (2026-11-02) -->
    <div class="card" id="sec-ph15">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;"><span class="badge badge-success">PHASE 15</span> 팩스 5회차 대량 발송 및 누적 전수 데이터 동기화</h2>
        <span style="font-size:12px; color:#6b7280; font-weight:600;">2026-11-02 완료</span>
      </div>
      <div class="tip-box" style="margin-top:12px;">
        • <strong>팩스 5회차 집행</strong>: 25개사 대상 샌드랩스 전송 집행, 22개사 수신 성공 (성공률 88.0%)<br>
        • <strong>누적 팩스 DB 동기화</strong>: 팩스 누적 발송 112건 완료 및 스프레드시트 <code>fax_log</code> 전수 동기화
      </div>
      <ul class="checklist">
        <li class="task-item"><input type="checkbox" id="ph15-fax-sync"><span class="task-text"><strong>[팩스 동기화]</strong> 팩스 5회차 25개사 집행 및 22개사 성공 데이터 시트 반영</span><input type="date" class="task-date-input" id="ph15-fax-sync-date"><input type="text" class="task-memo-input" id="ph15-fax-sync-memo"></li>
        <li class="task-item"><input type="checkbox" id="ph15-report-docx"><span class="task-text"><strong>[보고서 발행]</strong> 2026-11-02_dhsteel_final_work_summary.docx 보고서 작성 완료</span><input type="date" class="task-date-input" id="ph15-report-docx-date"><input type="text" class="task-memo-input" id="ph15-report-docx-memo"></li>
      </ul>
    </div>

    <!-- Summary of Earlier Phases (Phase 1 ~ 14) -->
    <div class="card">
      <h3 class="card-title">기초 인프라 및 아웃바운드 구축 이력 요약 (PHASE 1 ~ 14)</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th width="12%">Phase</th>
            <th width="20%">구분</th>
            <th>주요 수행 내용</th>
            <th width="14%">완료일자</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>PHASE 1~3</strong></td>
            <td>모바일 카탈로그 구축</td>
            <td>파이프 가공 반응형 모바일 카탈로그(스웨이징/벤딩/포밍) 설계 및 갤러리 구축</td>
            <td>2026-08 완료</td>
          </tr>
          <tr>
            <td><strong>PHASE 4~6</strong></td>
            <td>B2B 제안서 체계</td>
            <td>HTML/PDF 이메일 및 팩스 전용 A4 제안서 4종 설계 및 Google Apps Script 연동</td>
            <td>2026-09 완료</td>
          </tr>
          <tr>
            <td><strong>PHASE 7~9</strong></td>
            <td>통합 관제 대시보드</td>
            <td>트래픽 분석, Google Ads 연동, 에러 메일 리포트 및 관리자 인증 보안 게이트웨이 구축</td>
            <td>2026-09 완료</td>
          </tr>
          <tr>
            <td><strong>PHASE 10~12</strong></td>
            <td>팩스 영업 인프라</td>
            <td>샌드랩스 대량 팩스 발송 연동 모듈, 단축 제안서 1장 규격화, 팩스 로그 시트 체계화</td>
            <td>2026-10 완료</td>
          </tr>
          <tr>
            <td><strong>PHASE 13~14</strong></td>
            <td>실수요처 정밀 발굴</td>
            <td>전국 파이프/철물/가구 실수요처 3중 크롤링 및 500개사 우량 타겟 DB 구축 완료</td>
            <td>2026-10 완료</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>

  <!-- ============================================================== -->
  <!-- TAB 2: Cloudflare Pages 등록·배포 완벽 매뉴얼 (배포 독립 탭) -->
  <!-- ============================================================== -->
  <div id="tab-deploy" class="plan-tab-pane">
    
    <div class="card">
      <h3 class="card-title">🌐 1. Cloudflare Pages 인프라 이전 개요</h3>
      <p style="font-size:14px; margin-bottom:12px;">
        기존 Vercel 무료 플랜의 대역폭 한계 및 불필요한 빌드 복잡도를 해결하기 위해,
        <strong>삼협철망(samhyup) 및 퍼시스스토어(fursys-store)와 동일한 Cloudflare Pages 정적 호스팅 환경</strong>으로 전면 이전하였습니다.
      </p>
      <table class="data-table">
        <thead>
          <tr>
            <th width="20%">항목</th>
            <th width="40%">기존 (Vercel)</th>
            <th width="40%">신규 (Cloudflare Pages)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>공식 서비스 도메인</strong></td>
            <td><code>dhsteel.vercel.app</code></td>
            <td><strong style="color:#2563EB;"><code>https://dhsteel.pages.dev</code></strong></td>
          </tr>
          <tr>
            <td><strong>트래픽 / 대역폭</strong></td>
            <td>월 100GB 제한 (초과 시 서스펜드 위험)</td>
            <td><strong>무제한 대역폭</strong> (Cloudflare 글로벌 Anycast CDN)</td>
          </tr>
          <tr>
            <td><strong>배포 방식</strong></td>
            <td>Git 푸시 기반 서버 빌드</td>
            <td><strong>독립 <code>dist_deploy/</code> 자산 직접 업로드 (Direct Upload)</strong></td>
          </tr>
          <tr>
            <td><strong>프로젝트 네임스페이스</strong></td>
            <td><code>daeheungsteel</code></td>
            <td><strong><code>dhsteel</code></strong> (Pages 표준 네이밍 선점)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <h3 class="card-title">📁 2. 표준 파일명 및 라우팅 규칙</h3>
      <p style="font-size:14px; margin-bottom:12px;">혼선을 방지하고 일관된 표준을 유지하기 위해 핵심 웹 문서의 파일명을 통일하였습니다:</p>
      <ul class="checklist">
        <li><strong>메인 대시보드</strong>: <code>index_dashboard.html</code> (기존 dashboard.html에서 표준화)</li>
        <li><strong>모바일 e-카탈로그</strong>: <code>catalog/index_catalog.html</code> (기존 index.html에서 표준화)</li>
        <li><strong>루트 리다이렉터</strong>: <code>index.html</code> (루트 접속 시 /index_dashboard.html로 자동 안내)</li>
        <li><strong>Cloudflare 라우팅 파일</strong>: <code>_redirects</code> (루트 및 이미지 갤러리 경로 rewrite)</li>
      </ul>
      <pre># Cloudflare Pages _redirects 설정 규격
/             /index_dashboard.html       200
/gallery/*    /catalog/gallery/:splat     200
/images/*     /catalog/images/:splat      200</pre>
    </div>

    <div class="card">
      <h3 class="card-title">⚡ 3. 초경량 배포 패키지 빌드 시스템 (dist_deploy)</h3>
      <p style="font-size:14px; margin-bottom:12px;">
        프로젝트 루트의 무거운 개발 파일, 임시 백업, 파이썬 스크립트를 완전히 배제하고,
        오직 웹 서비스에 필요한 <strong>176개 순수 정적 파일(46.2MB)</strong>만 추출하여 <code>dist_deploy/</code> 폴더로 패키징합니다.
      </p>
      <div class="tip-box">
        <strong>빌드 명령어 실행 방법:</strong><br>
        터미널에서 <code>py build_dist_deploy.py</code> 실행 시 기존 폴더를 청소하고 3초 만에 완벽한 배포 패키지를 생성합니다.
      </div>
    </div>

    <div class="card">
      <h3 class="card-title">🚀 4. Cloudflare Pages 30초 배포 절차 매뉴얼</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th width="15%">단계</th>
            <th width="35%">작업 내용</th>
            <th width="50%">세부 가이드</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>STEP 1</strong></td>
            <td>패키지 최신 빌드</td>
            <td>로컬 터미널에서 <code>py build_dist_deploy.py</code> 실행</td>
          </tr>
          <tr>
            <td><strong>STEP 2</strong></td>
            <td>Cloudflare 접속</td>
            <td><a href="https://dash.cloudflare.com/68c2f5e55eb61025c5ec0e7b715f3ab6/pages/view/dhsteel" target="_blank" style="color:#2563EB; font-weight:700;">dhsteel 프로젝트 관리 페이지 ↗</a> 이동</td>
          </tr>
          <tr>
            <td><strong>STEP 3</strong></td>
            <td>자산 업로드</td>
            <td><strong>[Create deployment]</strong> 클릭 후 <code>E:\Antigravity\builder-dhsteel-sales\dist_deploy</code> 폴더를 드래그 앤 드롭</td>
          </tr>
          <tr>
            <td><strong>STEP 4</strong></td>
            <td>배포 확정</td>
            <td><strong>[Save and Deploy]</strong> 버튼 클릭 시 5초 이내에 글로벌 CDN 즉각 배포 완료</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <h3 class="card-title">✅ 5. 라이브 전수 검증 결과 (2026-11-20 통과)</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th>검증 엔드포인트</th>
            <th>HTTP 상태</th>
            <th>파일 용량</th>
            <th>비고</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>https://dhsteel.pages.dev/</code></td>
            <td><span class="badge badge-success">HTTP 200</span></td>
            <td>207 KB</td>
            <td>대시보드로 자동 리다이렉트 정상</td>
          </tr>
          <tr>
            <td><code>https://dhsteel.pages.dev/index_dashboard</code></td>
            <td><span class="badge badge-success">HTTP 200</span></td>
            <td>207 KB</td>
            <td>로고, 퀵버튼 2종, 다크네이비 에러버튼 정상 노출</td>
          </tr>
          <tr>
            <td><code>https://dhsteel.pages.dev/catalog/index_catalog.html</code></td>
            <td><span class="badge badge-success">HTTP 200</span></td>
            <td>48 KB</td>
            <td>모바일 e-카탈로그 전체 기능 정상 서빙</td>
          </tr>
          <tr>
            <td><code>https://dhsteel.pages.dev/images/logo_dhsteel.png</code></td>
            <td><span class="badge badge-success">HTTP 200</span></td>
            <td>476 KB</td>
            <td>메일링 호스팅 로고 정상 호출</td>
          </tr>
          <tr>
            <td><code>https://dhsteel.pages.dev/gallery/swaging_01.jpg</code></td>
            <td><span class="badge badge-success">HTTP 200</span></td>
            <td>106 KB</td>
            <td>메일 본문 제품 사진 CDN 정상 호출 (엑박 0건)</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>

  <!-- ============================================================== -->
  <!-- TAB 3: B2B 이메일 발송 자동화 및 템플릿 관리 (이메일 독립 탭) -->
  <!-- ============================================================== -->
  <div id="tab-mail" class="plan-tab-pane">
    
    <div class="card">
      <h3 class="card-title">✉️ 1. 주간 70개사 정기 이메일 발송 체계</h3>
      <p style="font-size:14px; margin-bottom:12px;">
        대흥정밀은 전국 500개사 파이프/철물/가구 제조 실수요처 중 <strong>매주 월요일 70개사</strong>를 정밀 선별하여
        Gmail API 및 Google Apps Script 기반의 1:1 맞춤형 B2B 제안서를 정기 발송합니다.
      </p>
      <div class="tip-box green">
        • <strong>발신 계정</strong>: <code>dhsteel7@gmail.com</code> (Gmail API OAuth 2.0 연동)<br>
        • <strong>발송 주기</strong>: 매주 월요일 오전 10:00 (주간 로테이션)<br>
        • <strong>발송 템플릿</strong>: <code>catalog/templates/dhsteel_proposal_v2.html</code> (모바일 최적화 반응형 HTML)<br>
        • <strong>고객 회신 및 DB</strong>: 구글 스프레드시트 <code>mail_log</code> 및 <code>schedule</code> 자동 동기화
      </div>
    </div>

    <div class="card">
      <h3 class="card-title">🌐 2. 이메일 템플릿 Cloudflare 도메인 57개소 전수 전환</h3>
      <p style="font-size:14px; margin-bottom:12px;">
        Cloudflare 이전 완료에 따라, 메일 본문에 포함된 모든 로고, 가공 샘플 사진(15종), 견적 문의 버튼 링크를
        신규 도메인(<code>https://dhsteel.pages.dev</code>)으로 100% 갱신하였습니다.
      </p>
      <table class="data-table">
        <thead>
          <tr>
            <th>대상 파일</th>
            <th>치환 건수</th>
            <th>주요 변경 항목</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>catalog/templates/dhsteel_proposal_v2.html</code></td>
            <td><strong>17개소</strong></td>
            <td>헤더 로고, 스웨이징/벤딩/포밍 갤러리 15장, 카탈로그 바로가기 링크</td>
          </tr>
          <tr>
            <td><code>catalog/templates/dhsteel_proposal.html</code></td>
            <td><strong>29개소</strong></td>
            <td>표준 B2B 제안서 내 모든 이미지 및 바로가기 URL</td>
          </tr>
          <tr>
            <td><code>google_apps_script_outbound.js</code></td>
            <td><strong>2개소</strong></td>
            <td>엔진 기본 URL: <code>var BASE_URL = "https://dhsteel.pages.dev/";</code></td>
          </tr>
          <tr>
            <td><code>catalog/templates/dhsteel_proposal_preview.html</code></td>
            <td><strong>2개소</strong></td>
            <td>제안서 미리보기 내 절대 경로</td>
          </tr>
          <tr>
            <td><code>catalog/templates/dhsteel_blog_post.html</code> 외</td>
            <td><strong>7개소</strong></td>
            <td>블로그 및 제안서 미리보기 연동 URL</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <h3 class="card-title">🛡️ 3. 반송 메일(Bounce) 분석 및 실시간 정제 프로토콜</h3>
      <p style="font-size:14px; margin-bottom:12px;">
        11/09 집행 결과(70건 중 67건 성공, 3건 실패)를 바탕으로 확립된 표준 정제 기준입니다:
      </p>
      <table class="data-table">
        <thead>
          <tr>
            <th width="20%">구분</th>
            <th width="30%">발생 원인</th>
            <th width="50%">조치 및 정제 프로토콜</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>오타 도메인</strong></td>
            <td><code>kovea.co</code> (.kr 누락)</td>
            <td><code>kovea.co.kr</code> 즉시 오타 수정 및 재발송 타겟 유지</td>
          </tr>
          <tr>
            <td><strong>계정 부존재 (550)</strong></td>
            <td>담당자 퇴사 또는 계정 삭제</td>
            <td>스프레드시트 내 영구 발송 제외 처리(A열 N 세팅)</td>
          </tr>
          <tr>
            <td><strong>메일 수신 거부/차단</strong></td>
            <td>서버 보안 정책으로 수신 차단</td>
            <td><strong>즉시 팩스(FAX) 채널로 전환</strong>하여 단축 제안서 발송 (아이디오 등)</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>

  <!-- ============================================================== -->
  <!-- TAB 4: B2B 팩스 대량 발송 운영 체계 & 센드랩스 연동 (팩스 독립 탭) -->
  <!-- ============================================================== -->
  <div id="tab-fax" class="plan-tab-pane">
    
    <div class="card">
      <h3 class="card-title">📠 1. 주간 30개사 정기 팩스 발송 체계</h3>
      <p style="font-size:14px; margin-bottom:12px;">
        이메일 확인율이 낮거나 현장 공장이 중심인 제조기업을 위해,
        <strong>매주 목요일 30개사</strong>를 대상으로 <strong>센드랩스(SendLabs) 대량 팩스 엔진</strong>을 통해 직관적인 1장 규격의 단축 제안서를 발송합니다.
      </p>
      <div class="tip-box green">
        • <strong>발송 플랫폼</strong>: 센드랩스 (https://www.sendlabs.co.kr)<br>
        • <strong>발송 주기</strong>: 매주 목요일 오후 14:00 (주간 로테이션)<br>
        • <strong>발송 문서</strong>: <code>sales/대흥정밀_파이프임가공_팩스전용_단축제안서.pdf</code> (A4 1장 흑백 가독성 최적화)<br>
        • <strong>누적 전송 이력</strong>: 총 141건 누적 (평균 성공률 91.5% 유지)
      </div>
    </div>

    <div class="card">
      <h3 class="card-title">📊 2. 팩스 6회차(2026-11-16) 집행 결과 분석</h3>
      <table class="data-table">
        <thead>
          <tr>
            <th>항목</th>
            <th>수치</th>
            <th>비율</th>
            <th>세부 내용</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>선별 타겟사</strong></td>
            <td>30개사</td>
            <td>100.0%</td>
            <td>11/02 성공 22건 + 우량 팩스사 + 메일 차단 전환군(아이디오)</td>
          </tr>
          <tr>
            <td><strong>실제 전송 건수</strong></td>
            <td>29건</td>
            <td>-</td>
            <td>1개사 중복 번호 자동 병합</td>
          </tr>
          <tr>
            <td><strong>수신 성공</strong></td>
            <td><strong>27건</strong></td>
            <td><strong style="color:#059669;">93.1%</strong></td>
            <td>아이디오 포함 27개 기업 정상 수신 확인</td>
          </tr>
          <tr>
            <td><strong>수신 실패</strong></td>
            <td>2건</td>
            <td>6.9%</td>
            <td>삼원금속(번호 오류), 유풍(무응답 결번)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <h3 class="card-title">📋 3. 샌드랩스 대량 업로드 표준 파일 규격</h3>
      <p style="font-size:14px; margin-bottom:12px;">
        팩스 발송 시 수작업 입력을 방지하기 위해 파이썬 자동화 스크립트로 엑셀 및 CSV를 사전 생성합니다:
      </p>
      <ul class="checklist">
        <li><strong>엑셀 규격</strong>: <code>sales/fax/fax_targets_20261116.xlsx</code> (업체명, 팩스번호, 대표자, 업종 컬럼 구성)</li>
        <li><strong>CSV 규격</strong>: <code>sales/fax/fax_targets_20261116.csv</code> (UTF-8 인코딩 샌드랩스 일괄 등록용)</li>
        <li><strong>시트 동기화</strong>: 구글 스프레드시트 <code>fax_log</code> 탭에 전송 결과 및 상태 코드 영구 기록</li>
      </ul>
    </div>

  </div>

  <!-- ============================================================== -->
  <!-- TAB 5: B2B 정기 발송 표준운영절차 (SOP) -->
  <!-- ============================================================== -->
  <div id="tab-sop" class="plan-tab-pane">
    
    <div class="card">
      <h3 class="card-title">📖 대흥정밀 B2B 정기 발송 표준운영절차 (Standard Operating Procedure)</h3>
      <p style="font-size:14px; margin-bottom:14px;">
        본 절차서는 에이전트와 운영자가 매주 정기 발송(이메일 70건, 팩스 30건)을 오차 없이 집행하기 위한 표준 업무 지침입니다.
      </p>
      
      <table class="data-table">
        <thead>
          <tr>
            <th width="15%">구분</th>
            <th width="35%">월요일 루틴 (이메일 70건)</th>
            <th width="50%">목요일 루틴 (팩스 30건)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>1. 타겟 선별<br>(D-1 준비)</strong></td>
            <td>
              • 스프레드시트 <code>company</code> 탭에서 A열 Y, 미발송 우량 고객 70개사 선별<br>
              • 반송 플래그(DNS/550) 제외 확인<br>
              • <code>YYYY-MM-DD</code> 전용 워크시트 생성
            </td>
            <td>
              • <code>company</code> 탭 팩스번호 유효 고객 30개사 선별<br>
              • 직전 메일 반송사 중 팩스 보유 업체 우선 배정<br>
              • <code>sales/fax/fax_targets_YYYYMMDD.xlsx</code> 생성
            </td>
          </tr>
          <tr>
            <td><strong>2. 사전 점검<br>(인프라 검증)</strong></td>
            <td>
              • Cloudflare Pages(<code>dhsteel.pages.dev</code>) 라이브 상태 점검<br>
              • 제안서 내 이미지 CDN 정상 서빙 확인<br>
              • Gmail API 발송 쿼터(잔여 1,000건+) 확인
            </td>
            <td>
              • 샌드랩스 잔여 캐시/포인트 확인<br>
              • 팩스용 단축 제안서 PDF 파일 무결성 확인<br>
              • 팩스 번호 하이픈(-) 정규화 검증
            </td>
          </tr>
          <tr>
            <td><strong>3. 발송 집행</strong></td>
            <td>
              • Gmail API 일괄 발송 트리거 실행<br>
              • 3초 딜레이 안전 발송 모니터링<br>
              • <code>mail_log</code>에 전송 타임스탬프 기록
            </td>
            <td>
              • 샌드랩스 대량 팩스 업로드 후 예약/즉시 발송<br>
              • 전송 결과 보고서 다운로드<br>
              • <code>fax_log</code>에 성공/실패 코드 기록
            </td>
          </tr>
          <tr>
            <td><strong>4. 사후 정제 및<br>보고서 발행</strong></td>
            <td>
              • 수신 거부 및 반송 3종 분류 정제<br>
              • 차주 팩스 전환 대상 리스트업<br>
              • 워드 결과 보고서(<code>.docx</code>) 발행
            </td>
            <td>
              • 결번/오류 번호 수정 및 <code>company</code> 탭 갱신<br>
              • 팩스 성공 고객사 대시보드 모니터링 연동<br>
              • 워드 결과 보고서(<code>.docx</code>) 발행
            </td>
          </tr>
        </tbody>
      </table>

      <div class="tip-box yellow">
        ⚠️ <strong>에러 발생 시 즉각 대응 지침:</strong><br>
        1. Cloudflare 접속 불가 시 <code>dist_deploy/</code> 즉시 재업로드<br>
        2. 메일 반송률이 10%를 초과할 경우 즉시 발송을 일시 중단하고 MX 레코드 정밀 검증 실시<br>
        3. 모든 변경 사항 및 작업 결과는 본 마스터 플랜 및 표준 워드 보고서에 동시 등재할 것
      </div>
    </div>

  </div>

</div>

<!-- Tab Switching Script -->
<script>
  function switchPlanTab(tabId) {
    // 1. Reset all buttons
    var buttons = document.querySelectorAll('.plan-tab-btn');
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].classList.remove('active');
    }

    // 2. Hide all panes
    var panes = document.querySelectorAll('.plan-tab-pane');
    for (var j = 0; j < panes.length; j++) {
      panes[j].classList.remove('active');
    }

    // 3. Activate target button & pane
    event.currentTarget.classList.add('active');
    var target = document.getElementById(tabId);
    if (target) {
      target.classList.add('active');
    }
  }

  // Auto-init checklist states from memory
  const defaults = {
    'ph18-infra-migration': { checked: true, date: '2026-11-20', memo: 'Cloudflare Pages 이전 및 dhsteel.pages.dev 라이브 오픈' },
    'ph18-file-standardize': { checked: true, date: '2026-11-20', memo: 'index_dashboard.html, index_catalog.html 표준화' },
    'ph18-dist-deploy-build': { checked: true, date: '2026-11-20', memo: '46.2MB 초경량 배포 패키지 구축' },
    'ph18-dashboard-ui-polish': { checked: true, date: '2026-11-20', memo: '인증창 로고, 상단 퀵버튼 2종, 에러버튼 톤다운 완료' },
    'ph18-email-domain-sync': { checked: true, date: '2026-11-20', memo: '메일 템플릿 및 GAS 내 57개소 도메인 전환' },
    'ph18-live-audit-pass': { checked: true, date: '2026-11-20', memo: '전 엔드포인트 HTTP 200 검증 100% 통과' },
    'ph17-fax-targets-30': { checked: true, date: '2026-11-16', memo: '11/02 성공군 및 우량 팩스 30개사 선별' },
    'ph17-sendlabs-files': { checked: true, date: '2026-11-16', memo: '샌드랩스 업로드용 xlsx/csv 생성 완료' },
    'ph17-sheet-20261116': { checked: true, date: '2026-11-16', memo: '2026-11-16 시트 신설 및 회차 세팅' },
    'ph17-fax-report-docx': { checked: true, date: '2026-11-16', memo: '2026-11-16_fax_result_batch6.docx 발행' },
    'ph16-schedule-dashboard': { checked: true, date: '2026-11-09', memo: '스케줄 대시보드 캘린더 구축' },
    'ph16-sheet-20261109': { checked: true, date: '2026-11-09', memo: '2026-11-09 시트 신설 및 70개사 매핑' },
    'ph16-mail-send-70': { checked: true, date: '2026-11-09', memo: '70개사 발송 (도달률 95.7%)' },
    'ph16-bounce-refine': { checked: true, date: '2026-11-09', memo: '반송 3건 조치 완료' },
    'ph15-fax-sync': { checked: true, date: '2026-11-02', memo: '팩스 5회차 25개사 집행 및 시트 반영' },
    'ph15-report-docx': { checked: true, date: '2026-11-02', memo: 'final_work_summary.docx 발행' }
  };

  const checkboxes = document.querySelectorAll('.task-item input[type="checkbox"]');
  checkboxes.forEach(cb => {
    const id = cb.id;
    const def = defaults[id] || {};
    const saved = localStorage.getItem('dhsteel_task_' + id);
    if (saved !== null) {
      cb.checked = saved === 'true';
    } else if (def.checked !== undefined) {
      cb.checked = def.checked;
    }
    const dInput = document.getElementById(id + '-date');
    if (dInput) {
      const sDate = localStorage.getItem('dhsteel_date_' + id);
      dInput.value = sDate || def.date || '';
      dInput.addEventListener('change', () => localStorage.setItem('dhsteel_date_' + id, dInput.value));
    }
    const mInput = document.getElementById(id + '-memo');
    if (mInput) {
      const sMemo = localStorage.getItem('dhsteel_memo_' + id);
      mInput.value = sMemo || def.memo || '';
      mInput.addEventListener('change', () => localStorage.setItem('dhsteel_memo_' + id, mInput.value));
    }
    cb.addEventListener('change', () => localStorage.setItem('dhsteel_task_' + id, cb.checked));
  });
</script>

</body>
</html>
"""

with open(plan_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'[Updated] Successfully wrote modular 5-tab plan to: {plan_path}')

