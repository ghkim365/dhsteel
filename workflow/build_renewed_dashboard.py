# -*- coding: utf-8 -*-
"""
build_renewed_dashboard.py (v2: 100% ID 완벽 매칭)
기존 index_dashboard.html의 모든 기능/로직/API/인증/모달을 100% 보존하면서
리뉴얼 시안(dhsteel_dashboard_redesign_2nd.html)의 세련된 UI 디자인/레이아웃/컬러를 결합하여 새 index_dashboard.html 빌드
"""

import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

# 1. 기존 index_dashboard.html 로드 (백업본 또는 원본)
backup_path = 'index_dashboard - 20161120_0112pm.html'
with open(backup_path, 'r', encoding='utf-8') as f:
    orig_html = f.read()

# 2. 기존 자바스크립트 스크립트 블록들 추출
scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', orig_html, re.DOTALL)
main_js = scripts[1]
err_js = scripts[2]

print(f'Extracted main_js: {len(main_js)} bytes, err_js: {len(err_js)} bytes')

# 3. 새로운 통합 index_dashboard.html 작성
renewed_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>대흥정밀 B2B 비즈니스 &amp; 마케팅 대시보드</title>
    <!-- Google Fonts & Pretendard -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {{
            --navy: #15284d;
            --navy-deep: #111B31;
            --blue: #2d67c8;
            --blue-light: #e8f0fe;
            --bg: #F1F4FA;
            --card: #FFFFFF;
            --text: #172B52;
            --muted: #71809B;
            --line: #E6EBF4;
            --border-color: #DDE1E7;
            --border-light: #EAEDF1;
            --gold: #D2A23C;
            --gold-light: #F5EDD3;
            --green: #20B783;
            --green-light: #DCF7EB;
            --orange: #F6A33B;
            --red: #EF4444;
            --red-light: #FFE5E6;
            --shadow: 0 4px 14px rgba(20, 43, 83, 0.06);
            --shadow-sm: 0 2px 6px rgba(0, 0, 0, 0.04);
            --font-main: "Pretendard", "Inter", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
            --panel-bg: #FFFFFF;
            --primary: var(--navy);
            --accent: #2563EB;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--bg);
            font-family: var(--font-main);
            color: var(--text);
            font-size: 13px;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }}

        /* ============================================================== */
        /* AUTH OVERLAY MODAL                                             */
        /* ============================================================== */
        .auth-overlay {{
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(8px);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .auth-card {{
            background: #FFFFFF;
            border-radius: 16px;
            padding: 36px 32px;
            width: 100%;
            max-width: 420px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            text-align: center;
            border: 1px solid #CBD5E1;
        }}
        .auth-card h2 {{
            font-size: 20px;
            font-weight: 800;
            color: var(--navy);
            margin-bottom: 8px;
        }}
        .auth-card p {{
            font-size: 13px;
            color: var(--muted);
            margin-bottom: 22px;
        }}
        .auth-input-group {{
            margin-bottom: 16px;
        }}
        .auth-input-group input {{
            width: 100%;
            padding: 13px;
            font-size: 18px;
            letter-spacing: 6px;
            text-align: center;
            border: 2px solid #CBD5E1;
            border-radius: 10px;
            outline: none;
            transition: border-color 0.2s;
        }}
        .auth-input-group input:focus {{
            border-color: var(--blue);
        }}
        .auth-error {{
            color: var(--red);
            font-size: 12px;
            font-weight: 700;
            min-height: 18px;
            margin-bottom: 12px;
        }}
        .btn-auth {{
            width: 100%;
            padding: 13px;
            font-size: 14.5px;
            font-weight: 800;
            background: var(--navy);
            color: #FFFFFF;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .btn-auth:hover {{
            background: #1e3a6a;
        }}

        /* ============================================================== */
        /* SIDEBAR (Renewal 130px Layout)                                */
        /* ============================================================== */
        .sidebar {{
            width: 130px;
            position: fixed;
            inset: 0 auto 0 0;
            background: linear-gradient(180deg, #122442 0%, #1b2f50 100%);
            color: #FFFFFF;
            padding: 24px 8px 18px;
            display: flex;
            flex-direction: column;
            z-index: 100;
            box-shadow: 2px 0 10px rgba(0,0,0,0.08);
        }}
        .logo {{
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            padding-bottom: 16px;
            margin-bottom: 16px;
        }}
        .logo-mark {{
            font-size: 26px;
            font-weight: 900;
            letter-spacing: -2px;
            color: #E9F2FF;
            line-height: 1;
        }}
        .logo-name {{
            font-size: 13px;
            font-weight: 800;
            margin-top: 5px;
            color: #FFFFFF;
        }}
        .logo-sub {{
            font-size: 7.5px;
            color: #A8B9D4;
            letter-spacing: 0.8px;
            margin-top: 2px;
        }}
        .nav {{
            display: grid;
            gap: 6px;
        }}
        .nav a {{
            color: #DCE6F6;
            text-decoration: none;
            padding: 10px 8px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11.5px;
            font-weight: 600;
            transition: all 0.2s;
        }}
        .nav a:hover {{
            background: rgba(255,255,255,0.08);
            color: #FFFFFF;
        }}
        .nav a.active {{
            background: linear-gradient(90deg, #C99A39 0%, #E0B84F 100%);
            color: #152A4B;
            font-weight: 800;
            box-shadow: 0 3px 8px rgba(201,154,57,0.3);
        }}
        .nav .ico {{
            width: 18px;
            text-align: center;
            font-size: 15px;
            flex-shrink: 0;
        }}
        .side-bottom {{
            margin-top: auto;
            border: 1px solid #3B5273;
            border-radius: 9px;
            padding: 10px 8px;
            font-size: 10px;
            color: #C9D7EB;
            text-align: center;
        }}
        .status-dot {{
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #25C58B;
            margin-right: 4px;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.4; transform: scale(1.15); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
        .side-bottom button {{
            width: 100%;
            background: transparent;
            color: #DBE6F4;
            border: 1px solid #536781;
            border-radius: 6px;
            padding: 6px;
            margin-top: 8px;
            font-size: 10px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .side-bottom button:hover {{
            background: rgba(255,255,255,0.1);
            color: #FFFFFF;
        }}

        /* ============================================================== */
        /* MAIN LAYOUT (Margin 130px)                                     */
        /* ============================================================== */
        .main {{
            margin-left: 130px;
            padding: 22px 20px 40px;
            max-width: calc(100% - 130px);
        }}

        /* Topbar */
        .topbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 14px;
        }}
        .heading h1 {{
            font-size: 20px;
            margin: 0 0 4px;
            font-weight: 850;
            color: var(--navy);
            letter-spacing: -0.5px;
        }}
        .heading p {{
            margin: 0;
            color: var(--muted);
            font-size: 12px;
        }}
        .top-actions {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .pillselect {{
            border: 1px solid #D1D9E6;
            background: #FFFFFF;
            color: #344D76;
            border-radius: 20px;
            padding: 8px 12px;
            font-weight: 700;
            font-size: 11.5px;
            outline: none;
            cursor: pointer;
            box-shadow: var(--shadow-sm);
        }}
        .pillbtn {{
            border: 1px solid #D1D9E6;
            background: #FFFFFF;
            color: #344D76;
            border-radius: 20px;
            padding: 8px 13px;
            font-weight: 700;
            font-size: 11.5px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            cursor: pointer;
            box-shadow: var(--shadow-sm);
            transition: all 0.2s;
            white-space: nowrap;
        }}
        .pillbtn:hover {{
            background: #F8FAFC;
            color: var(--blue);
            transform: translateY(-1px);
        }}
        .pillbtn.primary {{
            background: var(--navy);
            color: #FFFFFF;
            border-color: var(--navy);
        }}
        .pillbtn.primary:hover {{
            background: #1e3a6a;
            color: #FFFFFF;
        }}
        .pillbtn.active {{
            background: #DCFCE7;
            color: #166534;
            border-color: #86EFAC;
        }}

        /* Mode Selector */
        .mode-group {{
            display: flex;
            background: #E2E8F0;
            border-radius: 20px;
            padding: 3px;
            gap: 2px;
        }}
        .mode-btn {{
            border: none;
            background: transparent;
            color: #475569;
            font-size: 11px;
            font-weight: 700;
            padding: 5px 10px;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .mode-btn.active {{
            background: #FFFFFF;
            color: var(--navy);
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }}

        /* Cards General */
        .card {{
            background: var(--card);
            border: 1px solid #E8EDF5;
            border-radius: 12px;
            box-shadow: var(--shadow);
        }}

        /* 4 KPI Cards Grid */
        .grid4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 18px;
        }}
        .kpi {{
            padding: 16px 18px 14px;
            min-height: 124px;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .kpi .label {{
            font-weight: 700;
            font-size: 12px;
            color: #64748B;
            display: flex;
            gap: 6px;
            align-items: center;
        }}
        .kpi .value {{
            font-size: 30px;
            font-weight: 850;
            letter-spacing: -0.8px;
            color: var(--navy);
            margin: 4px 0 2px;
            line-height: 1.1;
        }}
        .delta {{
            font-size: 11px;
            color: #1CB67D;
            font-weight: 700;
        }}
        .kpi.warn {{
            background: #FFFDF8;
            border-color: #FDE68A;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        .kpi.warn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(245, 158, 11, 0.15);
        }}
        .kpi.warn .value {{
            color: #B45309;
        }}

        /* Content Grid (Charts) */
        .content-grid {{
            display: grid;
            grid-template-columns: 1.6fr 1fr;
            gap: 14px;
            margin-bottom: 18px;
        }}
        .chart-card {{
            padding: 18px 20px;
            min-height: 330px;
            display: flex;
            flex-direction: column;
        }}
        .cardtitle {{
            font-size: 15px;
            font-weight: 800;
            color: var(--navy);
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .subtitle {{
            font-size: 11px;
            color: #8794AA;
            margin-bottom: 12px;
        }}
        .chart-container {{
            flex: 1;
            position: relative;
            width: 100%;
            height: 250px;
        }}

        /* Leads Table Card */
        .table-card {{
            padding: 18px 20px 14px;
            margin-bottom: 18px;
        }}
        .tablehead {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .table-controls {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .search-box {{
            display: flex;
            align-items: center;
            gap: 6px;
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            padding: 6px 10px;
            min-width: 240px;
        }}
        .search-box input {{
            border: none;
            background: transparent;
            font-size: 12px;
            outline: none;
            width: 100%;
            font-family: inherit;
        }}
        .table-scroll {{
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 760px;
        }}
        thead {{
            background: #F1F4FA;
            color: #6A7B98;
            font-size: 11.5px;
        }}
        th, td {{
            text-align: left;
            padding: 10px 12px;
            border-bottom: 1px solid #E8EDF5;
            white-space: nowrap;
            font-size: 11.5px;
        }}
        th {{ font-weight: 700; }}
        td {{ color: #263B5E; }}
        tbody tr:hover {{
            background: #F8FAFF;
        }}
        .badge {{
            border-radius: 12px;
            padding: 4px 8px;
            font-weight: 700;
            font-size: 10.5px;
            display: inline-block;
        }}
        .badge.red {{ background: #FFE5E6; color: #C33D50; }}
        .badge.orange {{ background: #FFF0D9; color: #B7791B; }}
        .badge.blue {{ background: #E2EFFF; color: #2E6AC5; }}
        .badge.green {{ background: #DCF7EB; color: #178B62; }}
        .badge-product {{
            background: #EDE9FE;
            color: #6D28D9;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
        }}
        .detail {{
            border: 1px solid #CCD7E9;
            background: #FFFFFF;
            border-radius: 6px;
            color: #345174;
            padding: 5px 8px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .detail:hover {{
            background: var(--blue);
            color: #FFFFFF;
            border-color: var(--blue);
        }}

        /* Bottom Grid (Simulator & Quick Cards) */
        .bottomgrid {{
            display: grid;
            grid-template-columns: 1.55fr 1fr;
            gap: 14px;
            margin-bottom: 18px;
        }}
        .simcard {{
            padding: 18px 20px;
        }}
        .sim-layout {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 14px;
        }}
        .control label {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 700;
            font-size: 11.5px;
            margin-bottom: 8px;
        }}
        .control input[type="range"] {{
            width: 100%;
            accent-color: #2868C9;
        }}
        .amount {{
            border: 1px solid #DCE5F3;
            border-radius: 6px;
            padding: 3px 8px;
            font-weight: 800;
            color: var(--blue);
            background: #F8FAFC;
        }}
        .simtable {{
            border: 1px solid #E3E9F2;
            border-radius: 8px;
            overflow: hidden;
            font-size: 11.5px;
        }}
        .simtable div {{
            display: grid;
            grid-template-columns: 1.2fr 1fr 1fr;
            padding: 9px 12px;
            border-bottom: 1px solid #EDF1F7;
        }}
        .simtable div:first-child {{
            background: #F1F4FA;
            font-weight: 800;
            color: var(--navy);
        }}
        .simtable div:last-child {{
            border-bottom: none;
        }}

        .quick-card {{
            padding: 18px 20px;
        }}
        .quickgrid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 12px 0;
        }}
        .quick {{
            border: 1px solid #E6EBF4;
            border-radius: 10px;
            background: #FFFFFF;
            box-shadow: 0 3px 8px rgba(25, 48, 88, 0.04);
            padding: 14px 6px;
            text-align: center;
            color: #334D75;
            font-size: 11px;
            font-weight: 700;
            text-decoration: none;
            display: block;
            transition: all 0.2s;
        }}
        .quick:hover {{
            transform: translateY(-2px);
            border-color: #CBD5E1;
            box-shadow: 0 5px 12px rgba(0,0,0,0.08);
            color: var(--blue);
        }}
        .quick .qico {{
            font-size: 20px;
            margin-bottom: 6px;
        }}

        .notice {{
            padding: 16px 20px;
            margin-top: 14px;
        }}
        .notice ul {{
            list-style: none;
            padding: 0;
            margin: 10px 0 0;
        }}
        .notice li {{
            padding: 8px 0;
            border-bottom: 1px solid #EDF1F6;
            font-size: 11.5px;
            display: flex;
            justify-content: space-between;
        }}
        .notice li:last-child {{
            border-bottom: none;
        }}
        .notice-date {{
            color: #8896AD;
            font-size: 10.5px;
        }}

        /* ============================================================== */
        /* MODALS (Quote Detail & Error Report)                           */
        /* ============================================================== */
        .modal-overlay {{
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(4px);
            z-index: 999;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .modal-overlay.active {{
            display: flex;
        }}
        .modal-card {{
            background: #FFFFFF;
            border-radius: 14px;
            width: 100%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            border: 1px solid #CBD5E1;
        }}
        .modal-header {{
            padding: 16px 20px;
            border-bottom: 1px solid #E2E8F0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .modal-title {{
            font-size: 16px;
            font-weight: 800;
            color: var(--navy);
        }}
        .modal-close {{
            background: transparent;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: #64748B;
        }}
        .modal-body {{
            padding: 20px;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 14px;
        }}
        .info-item label {{
            display: block;
            font-size: 11px;
            color: #64748B;
            font-weight: 700;
            margin-bottom: 4px;
        }}
        .info-item p {{
            font-size: 13px;
            font-weight: 600;
            color: var(--text);
        }}
        .info-item-full {{
            grid-column: span 2;
        }}
        .specs-display-box {{
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 12px;
            font-size: 12.5px;
            white-space: pre-wrap;
            line-height: 1.6;
        }}

        /* Responsive Breakpoints */
        @media(max-width: 1024px) {{
            .grid4 {{ grid-template-columns: repeat(2, 1fr); }}
            .content-grid, .bottomgrid {{ grid-template-columns: 1fr; }}
        }}
        @media(max-width: 768px) {{
            .sidebar {{ width: 65px; padding: 16px 4px; }}
            .logo-name, .logo-sub {{ display: none; }}
            .nav a {{ justify-content: center; padding: 12px 0; }}
            .nav a .navtext {{ display: none; }}
            .side-bottom {{ display: none; }}
            .main {{ margin-left: 65px; max-width: calc(100% - 65px); padding: 14px 10px; }}
            .heading h1 {{ font-size: 17px; }}
        }}
    </style>
</head>

<body>

    <!-- ============================================================== -->
    <!-- PASSWORD AUTH OVERLAY GATE                                     -->
    <!-- ============================================================== -->
    <div id="authOverlay" class="auth-overlay">
        <div class="auth-card">
            <div style="width: 48px; height: 48px; margin: 0 auto 16px;">
                <img src="assets/logo_dhsteel.png" alt="대흥정밀" style="width:100%; height:100%; object-fit:contain;">
            </div>
            <h2>대흥정밀 관리자 인증</h2>
            <p>보안 데이터 및 실시간 현황 조회를 위해 비밀번호를 입력해주세요.</p>
            <div class="auth-input-group">
                <input type="password" id="authPassword" placeholder="••••" maxlength="8" autocomplete="off"
                    onkeydown="if(event.key === 'Enter') verifyPassword()">
            </div>
            <div id="authError" class="auth-error"></div>
            <button class="btn-auth" onclick="verifyPassword()">인증하기</button>

            <!-- 방문자 링크 안내 -->
            <div style="margin-top: 22px; padding-top: 16px; border-top: 1px solid #E2E8F0; text-align: center;">
                <p style="font-size: 12px; color: #64748B; margin-bottom: 10px; font-weight: 600;">
                    💡 제품 카탈로그 또는 기업 소개를 찾으시나요?
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                    <a href="catalog/index_catalog.html" target="_blank" class="pillbtn" style="justify-content:center;">📱 모바일 카탈로그</a>
                    <a href="https://dhsteel.pages.dev/" target="_blank" class="pillbtn" style="justify-content:center;">🌐 협력 제안서</a>
                </div>
            </div>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- SIDEBAR NAVIGATION (130px)                                     -->
    <!-- ============================================================== -->
    <aside class="sidebar">
        <div class="logo">
            <div class="logo-mark">DH</div>
            <div class="logo-name">대흥정밀</div>
            <div class="logo-sub">DAEHEUNG PRECISION</div>
        </div>
        <nav class="nav">
            <a class="active" href="#"><span class="ico">⌂</span><span class="navtext">대시보드</span></a>
            <a href="#quotes"><span class="ico">✉</span><span class="navtext">견적 관리</span></a>
            <a href="#analytics"><span class="ico">📊</span><span class="navtext">마케팅 분석</span></a>
            <a href="javascript:void(0)" onclick="switchSite('mailling')"><span class="ico">📬</span><span class="navtext">메일 발송</span></a>
            <a href="javascript:void(0)" onclick="switchSite('fax')"><span class="ico">📠</span><span class="navtext">팩스 현황</span></a>
            <a href="#sim"><span class="ico">▦</span><span class="navtext">시뮬레이터</span></a>
            <a href="plan/dhsteel_plan_2026.html" target="_blank"><span class="ico">📋</span><span class="navtext">운영계획서</span></a>
            <a href="javascript:void(0)" onclick="changeAdminPassword()"><span class="ico">🔑</span><span class="navtext">비번 변경</span></a>
        </nav>
        <div class="side-bottom">
            <div><span class="status-dot"></span>시스템 정상</div>
            <div style="margin:6px 0 2px; color:#91A4BF; font-size:9.5px;">최근 동기화</div>
            <strong style="color:#FFFFFF; font-size:10px;">2026.11.23 LIVE</strong>
            <button onclick="sessionStorage.removeItem('dhsteel_auth'); location.reload();">로그아웃</button>
        </div>
    </aside>

    <!-- ============================================================== -->
    <!-- MAIN DASHBOARD CONTENT                                         -->
    <!-- ============================================================== -->
    <main class="main" id="dashboard-wrapper">
        
        <!-- TOPBAR -->
        <header class="topbar">
            <div class="heading">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
                    <h1 id="brand-title" style="margin-bottom:0;">대흥정밀 B2B 비즈니스 대시보드</h1>
                    <div id="badge-google-ads" style="display:inline-flex; align-items:center; gap:5px; font-size:11px; color:#166534; background:#DCF7EB; padding:3px 8px; border-radius:12px; font-weight:700;">
                        <span class="status-dot"></span>Google Ads (dhsteel 651-167-5293): Active
                    </div>
                </div>
                <p id="brand-subtitle">실시간 데이터로 스마트한 마케팅과 영업을 시작하세요</p>
            </div>
            <div class="top-actions">
                <!-- Target Site Selector -->
                <select id="site-selector" class="pillselect" onchange="switchSite(this.value)">
                    <option value="catalog">📱 모바일 카탈로그</option>
                    <option value="main_site">🌐 공식 홈페이지 (daeheungsteel.co.kr)</option>
                    <option value="mailling">✉️ B2B 이메일 발송 현황</option>
                    <option value="fax">📠 B2B 팩스 발송 현황</option>
                </select>

                <!-- Report View Button (Dynamic) -->
                <button id="btn-report-view" class="pillbtn primary" onclick="openMailReport()" style="display:none;">
                    📊 발송 상세 리포트 ↗
                </button>

                <!-- Mode Selector -->
                <div class="mode-group">
                    <button id="mode-realtime" class="mode-btn active" onclick="switchMode('realtime')">🔴 실시간</button>
                    <button id="mode-simulator" class="mode-btn" onclick="switchMode('simulator')">⚙️ 시뮬</button>
                </div>

                <!-- Quick Action Buttons -->
                <a href="catalog/index_catalog.html" target="_blank" class="pillbtn">📱 카탈로그 ↗</a>
                <a href="catalog/대흥정밀 B2B 파이프 임가공 제안서_미리보기.html" target="_blank" class="pillbtn">📄 브로슈어 ↗</a>
                <a href="https://dhsteel.pages.dev/" target="_blank" class="pillbtn">🌐 제안서 ↗</a>
                <a href="https://docs.google.com/spreadsheets/d/1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic/edit?pli=1&gid=1031257647#gid=1031257647" 
                   target="_blank" id="btn-gsheet-link" class="pillbtn">📊 구글시트 ↗</a>
            </div>
        </header>

        <!-- KPI 4 CARDS GRID -->
        <section class="grid4">
            <!-- KPI 1: 총 방문 세션 -->
            <article class="card kpi">
                <div class="label" id="kpi-title-1">
                    <span>👤</span> 총 방문 세션
                </div>
                <div class="value" id="kpi-visits">-</div>
                <div class="delta" id="kpi-visits-ratio">Google Ads 유입 0%</div>
                <!-- Sparkline SVG -->
                <svg style="position:absolute; bottom:0; right:0; width:110px; height:45px; opacity:0.35;" viewBox="0 0 120 48">
                    <polyline points="0,45 20,40 35,38 48,30 60,33 77,21 92,20 108,7 120,4" fill="none" stroke="#2563EB" stroke-width="2.5"/>
                </svg>
            </article>

            <!-- KPI 2: 누적 견적 문의 -->
            <article class="card kpi">
                <div class="label" id="kpi-title-2">
                    <span>✉️</span> 견적 문의 접수
                </div>
                <div class="value" id="kpi-quotes">-</div>
                <div class="delta" id="kpi-subtitle-2">
                    최근 24시간 <span id="kpi-quotes-today">0건</span> 추가 접수
                </div>
                <!-- Sparkline SVG -->
                <svg style="position:absolute; bottom:0; right:0; width:110px; height:45px; opacity:0.35;" viewBox="0 0 120 48">
                    <polyline points="0,45 20,42 35,35 48,34 60,25 77,22 92,15 108,12 120,5" fill="none" stroke="#8B5CF6" stroke-width="2.5"/>
                </svg>
            </article>

            <!-- KPI 3: 견적 전환율 -->
            <article class="card kpi">
                <div class="label" id="kpi-title-3">
                    <span>🎯</span> 견적 전환율 (CVR)
                </div>
                <div class="value" id="kpi-cvr">-%</div>
                <div class="delta" id="kpi-subtitle-3" style="color:#64748B;">
                    방문 대비 견적 성공율
                </div>
                <!-- Sparkline SVG -->
                <svg style="position:absolute; bottom:0; right:0; width:110px; height:45px; opacity:0.35;" viewBox="0 0 120 48">
                    <polyline points="0,42 20,38 35,35 48,28 60,30 77,18 92,16 108,10 120,6" fill="none" stroke="#10B981" stroke-width="2.5"/>
                </svg>
            </article>

            <!-- KPI 4: 반송 에러 / 미처리 문의 알림 -->
            <article class="card kpi warn" onclick="openErrModal()" title="클릭하여 반송 에러 리포트 열기">
                <div class="label" style="color:#B45309;">
                    <span>⚠️</span> 반송·에러 모니터링
                </div>
                <div class="value" id="errBadge">0건</div>
                <div style="font-weight:800; font-size:11px; color:#D97706;">
                    반송 내역 확인하기 ›
                </div>
                <!-- Sparkline SVG -->
                <svg style="position:absolute; bottom:0; right:0; width:110px; height:45px; opacity:0.35;" viewBox="0 0 120 48">
                    <polyline points="0,45 20,40 35,36 48,32 60,35 77,28 92,20 108,18 120,10" fill="none" stroke="#F59E0B" stroke-width="2.5"/>
                </svg>
            </article>
        </section>

        <!-- CONTENT GRID (Charts) -->
        <section class="content-grid" id="analytics">
            <!-- Left: 유입 채널 비중 추이 차트 -->
            <article class="card chart-card">
                <div class="cardtitle" id="chart-visits-title">📊 마케팅 유입 채널 분석</div>
                <div class="subtitle" id="chart-visits-desc">Google Ads 광고 유입 대 오가닉 검색 및 직접 유입 비중 추이</div>
                <div class="chart-container">
                    <canvas id="sourceChart"></canvas>
                </div>
            </article>

            <!-- Right: 요청 품목별 선호도 차트 -->
            <article class="card chart-card">
                <div class="cardtitle" id="chart-product-title">🎯 가공 요청 품목 선호도</div>
                <div class="subtitle" id="chart-product-desc">견적 요청이 접수된 서비스별(확관, 축관, 밴딩 등) 분포 분석</div>
                <div class="chart-container">
                    <canvas id="productChart"></canvas>
                </div>
            </article>
        </section>

        <!-- LEADS TABLE CARD -->
        <section class="card table-card" id="quotes">
            <div class="tablehead">
                <div>
                    <h3 class="cardtitle" id="table-mode-title" style="margin-bottom:2px;">✉️ 최근 견적 문의 접수 목록</h3>
                    <p class="subtitle" id="table-mode-desc" style="margin-bottom:0;">구글 스프레드시트와 실시간 연동된 최신 견적 접수 데이터입니다.</p>
                </div>
                
                <div class="table-controls">
                    <!-- Search Input -->
                    <div class="search-box">
                        <span>🔍</span>
                        <input type="text" id="table-search-input" placeholder="검색 (회사명, 이메일, 담당자...)" oninput="onSearchInputChanged()">
                    </div>

                    <!-- Status Filter -->
                    <select id="status-filter-select" class="pillselect" onchange="onStatusFilterChanged()">
                        <option value="all" selected>전체 상태</option>
                        <option value="성공">✅ 성공만</option>
                        <option value="실패">❌ 실패만</option>
                    </select>

                    <!-- Items per page -->
                    <select id="items-per-page-select" class="pillselect" onchange="onPageSizeChanged()">
                        <option value="10" selected>10개씩</option>
                        <option value="25">25개씩</option>
                        <option value="50">50개씩</option>
                        <option value="all">전체</option>
                    </select>

                    <span id="table-count-info" style="font-size:12px; font-weight:700; color:var(--muted);">전체 0건</span>
                </div>
            </div>

            <!-- Table Body -->
            <div class="table-scroll">
                <table id="leads-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>접수 일시</th>
                            <th>회사 / 현장명</th>
                            <th>담당자</th>
                            <th>연락처</th>
                            <th>가공 서비스</th>
                            <th>유입 경로</th>
                            <th>상태</th>
                            <th>액션</th>
                        </tr>
                    </thead>
                    <tbody id="leads-body">
                        <!-- Real-time dynamic items rendered here -->
                    </tbody>
                </table>

                <div id="table-empty" style="display:none; padding:40px; text-align:center; color:var(--muted);">
                    <div style="font-size:32px; margin-bottom:10px;">📥</div>
                    <p id="empty-state-text">접수된 견적 요청이 없습니다.</p>
                </div>
            </div>

            <!-- Pagination Bar -->
            <div id="pagination-controls" style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; padding-top:12px; border-top:1px solid #E8EDF5;">
                <div id="pagination-summary" style="font-size:12px; color:var(--muted);">
                    Showing 1 to 10 of 0 entries
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <button id="btn-prev-page" class="detail" onclick="changePage(-1)">◀ 이전</button>
                    <span id="page-num-display" style="font-size:12px; font-weight:800; color:var(--navy); min-width:50px; text-align:center;">1 / 1</span>
                    <button id="btn-next-page" class="detail" onclick="changePage(1)">다음 ▶</button>
                </div>
            </div>
        </section>

        <!-- BOTTOM GRID (Simulator & Quick Actions) -->
        <section class="bottomgrid" id="sim">
            <!-- Google Ads Simulator -->
            <article class="card simcard">
                <div class="cardtitle">▦ Google Ads 효율 시뮬레이터</div>
                <div class="subtitle">일일 광고비 설정에 따른 예상 클릭수와 문의 건수, 전환비용(CPA)을 예측합니다.</div>
                
                <div class="sim-layout">
                    <div>
                        <div class="control">
                            <label>
                                <span>일일 설정 광고 예산</span>
                                <span class="amount" id="label-budget">150,000 원</span>
                            </label>
                            <input type="range" id="input-budget" min="50000" max="1000000" step="50000" value="150000">
                        </div>
                        <div class="control" style="margin-top:18px;">
                            <label>
                                <span>평균 클릭 단가 (CPC)</span>
                                <span class="amount" id="label-cpc">450 원</span>
                            </label>
                            <input type="range" id="input-cpc" min="200" max="1500" step="50" value="450">
                        </div>
                        <button class="pillbtn primary" style="width:100%; margin-top:16px; justify-content:center; padding:11px;" onclick="calculateSimulator()">
                            시뮬레이션 재계산 ▶
                        </button>
                        <button id="btn-mock-generate" class="pillbtn" style="margin-top:8px; width:100%; justify-content:center;" onclick="generateMockQuote()">
                            ⚡ 시뮬레이션: 가상 견적 접수 테스트
                        </button>
                    </div>

                    <div>
                        <div class="simtable">
                            <div>
                                <span>구분</span>
                                <span>설정 지표</span>
                                <span>예상 성과</span>
                            </div>
                            <div>
                                <span>예상 클릭수</span>
                                <span>클릭당 CPC</span>
                                <strong id="result-clicks" style="color:var(--navy); font-size:13px;">- 회</strong>
                            </div>
                            <div>
                                <span>예상 견적 문의</span>
                                <span>전환율 기준</span>
                                <strong id="result-leads" style="color:var(--blue); font-size:13px;">- 건</strong>
                            </div>
                            <div>
                                <span>예상 전환비용(CPA)</span>
                                <span>리드당 원가</span>
                                <strong id="result-cpa" style="color:#10B981; font-size:13px;">- 원</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </article>

            <!-- Quick Actions & Notices -->
            <div>
                <article class="card quick-card">
                    <div class="cardtitle">⚡ 업무 도구 빠른 실행</div>
                    <div class="quickgrid">
                        <a href="catalog/index_catalog.html" target="_blank" class="quick">
                            <div class="qico">📱</div>카탈로그 보기
                        </a>
                        <a href="catalog/대흥정밀 B2B 파이프 임가공 제안서_미리보기.html" target="_blank" class="quick">
                            <div class="qico">📄</div>브로슈어 시안
                        </a>
                        <a href="https://dhsteel.pages.dev/" target="_blank" class="quick">
                            <div class="qico">🌐</div>B2B 협력제안서
                        </a>
                        <a href="https://docs.google.com/spreadsheets/d/1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic/edit?pli=1&gid=1031257647#gid=1031257647" target="_blank" class="quick">
                            <div class="qico" style="color:#10B981;">📊</div>Company 시트
                        </a>
                        <a href="plan/dhsteel_plan_2026.html" target="_blank" class="quick">
                            <div class="qico">📋</div>2026 마스터플랜
                        </a>
                        <a href="https://www.sendlabs.co.kr/main.do" target="_blank" class="quick">
                            <div class="qico" style="color:#2563EB;">📠</div>SendLabs 팩스
                        </a>
                    </div>
                </article>

                <article class="card notice">
                    <div class="cardtitle">📣 공지사항 &amp; 시스템 알림</div>
                    <ul>
                        <li>
                            <span>Cloudflare Pages 배포 인프라 통합 완료</span>
                            <span class="notice-date">11.20</span>
                        </li>
                        <li>
                            <span>3차 정기 B2B 이메일 발송 68건 성공</span>
                            <span class="notice-date">11.23</span>
                        </li>
                        <li>
                            <span>반송 메일 1시간 주기 자동 스캔 트리거 가동</span>
                            <span class="notice-date">11.23</span>
                        </li>
                    </ul>
                </article>
            </div>
        </section>

        <!-- SENDLABS ACCOUNT SECTION -->
        <section class="card" id="sales-tools-section" style="padding:20px; margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #E8EDF5; padding-bottom:10px;">
                <h3 class="cardtitle" style="margin-bottom:0;">📠 대량 팩스 발송 계정 정보 (SendLabs)</h3>
                <span class="badge" style="background:#DCF7EB; color:#166534;">● 정상 사용 중</span>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; font-size:12px;">
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px;">
                    <div style="color:#64748B; font-size:10.5px;">서비스 ID</div>
                    <strong style="color:#1E293B;">dhsteel</strong>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px;">
                    <div style="color:#64748B; font-size:10.5px;">공통 발신번호</div>
                    <strong style="color:#005F56;">02-2076-8203</strong>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px;">
                    <div style="color:#64748B; font-size:10.5px;">요금 방식</div>
                    <strong style="color:#1E293B;">충전식 · 25 Cash/장</strong>
                </div>
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:10px 12px;">
                    <div style="color:#64748B; font-size:10.5px;">발송 규격</div>
                    <strong style="color:#1E293B;">A4 1장 흑백 최적화</strong>
                </div>
            </div>
        </section>

    </main>

    <!-- ============================================================== -->
    <!-- MODAL: QUOTE DETAILS                                           -->
    <!-- ============================================================== -->
    <div class="modal-overlay" id="quoteModal">
        <div class="modal-card">
            <div class="modal-header">
                <h3 class="modal-title">견적 요청 상세 정보</h3>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="info-grid">
                    <div class="info-item">
                        <label>회사 / 현장명</label>
                        <p id="modal-company">-</p>
                    </div>
                    <div class="info-item">
                        <label>담당자명</label>
                        <p id="modal-name">-</p>
                    </div>
                    <div class="info-item">
                        <label>연락처</label>
                        <p id="modal-phone">-</p>
                    </div>
                    <div class="info-item">
                        <label>이메일 주소</label>
                        <p id="modal-email">-</p>
                    </div>
                    <div class="info-item">
                        <label>가공 서비스</label>
                        <p><span class="badge-product" id="modal-product">-</span></p>
                    </div>
                    <div class="info-item">
                        <label>유입 경로</label>
                        <p id="modal-source">-</p>
                    </div>
                    <div class="info-item info-item-full">
                        <label>희망 규격 및 요청 수량</label>
                        <div class="specs-display-box" id="modal-specs">-</div>
                    </div>
                    <div class="info-item info-item-full" id="modal-file-box" style="display:none;">
                        <label>첨부 도면 / 파일</label>
                        <div style="margin-top:4px;">
                            <a id="modal-file-link" href="#" target="_blank" class="pillbtn primary" style="font-size:12px;">
                                📎 첨부파일 다운로드 / 열람 ↗
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- MODAL: ERROR REPORT (BOUNCE EMAILS)                            -->
    <!-- ============================================================== -->
    <div class="modal-overlay" id="errModal" onclick="closeErrModalOutside(event)">
        <div class="modal-card" style="max-width:720px;">
            <div class="modal-header">
                <div>
                    <h3 class="modal-title" style="color:var(--navy);">📧 이메일 발송 반송/에러 상세 리포트</h3>
                    <div style="font-size:11px; color:#64748B; margin-top:2px;" id="errModalMeta">데이터 로딩 중...</div>
                </div>
                <button class="modal-close" onclick="closeErrModal()">&times;</button>
            </div>
            <div class="modal-body">
                <!-- Summary stat badges -->
                <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; margin-bottom:14px; text-align:center;">
                    <div style="background:#FEE2E2; border:1px solid #FCA5A5; border-radius:8px; padding:10px;">
                        <div style="font-size:11px; color:#991B1B; font-weight:700;">전체 실패 건수</div>
                        <strong style="font-size:18px; color:#DC2626;" id="sc-total">0건</strong>
                    </div>
                    <div style="background:#FEF3C7; border:1px solid #FCD34D; border-radius:8px; padding:10px;">
                        <div style="font-size:11px; color:#92400E; font-weight:700;">수신자 없음 (550)</div>
                        <strong style="font-size:18px; color:#D97706;" id="sc-550">0건</strong>
                    </div>
                    <div style="background:#F1F5F9; border:1px solid #CBD5E1; border-radius:8px; padding:10px;">
                        <div style="font-size:11px; color:#475569; font-weight:700;">도메인 오류 (DNS)</div>
                        <strong style="font-size:18px; color:#1E293B;" id="sc-dns">0건</strong>
                    </div>
                </div>

                <!-- Tabs: 날짜별 / 히스토리 -->
                <div style="display:flex; gap:8px; margin-bottom:12px; border-bottom:1px solid #E2E8F0; padding-bottom:8px;">
                    <button class="pillbtn primary" id="btn-tab-errlist" onclick="switchErrTab('list')">📅 일자별 반송 목록 (<span id="errListCnt">0</span>건)</button>
                    <button class="pillbtn" id="btn-tab-errhistory" onclick="switchErrTab('history')">📜 누적 히스토리 (<span id="errHistoryCnt">0</span>건)</button>
                </div>

                <!-- Date selector pills -->
                <div id="errDateSelector" style="margin-bottom:12px; display:flex; gap:6px; flex-wrap:wrap;">
                    <div id="errDateSelectorList" style="display:flex; gap:6px; flex-wrap:wrap;"></div>
                </div>

                <!-- Table for Errors -->
                <div class="table-scroll" style="max-height:300px; overflow-y:auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>회사명</th>
                                <th>이메일 주소</th>
                                <th>실패 원인</th>
                                <th>조치 상태</th>
                            </tr>
                        </thead>
                        <tbody id="errTableBody">
                            <!-- Dynamic error logs -->
                        </tbody>
                        <tbody id="errHistoryBody" style="display:none;">
                            <!-- Dynamic history logs -->
                        </tbody>
                    </table>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; padding-top:12px; border-top:1px solid #E2E8F0;">
                    <button class="detail" onclick="copyErrList()">📋 실패 목록 복사</button>
                    <button class="pillbtn primary" onclick="closeErrModal()">확인 및 닫기</button>
                </div>
            </div>
        </div>
    </div>

    <!-- ============================================================== -->
    <!-- PRESERVED SCRIPTS (UNTOUCHED LOGIC & APIS)                     -->
    <!-- ============================================================== -->
    <script>
{main_js}
    </script>

    <script>
{err_js}
    </script>
</body>
</html>
"""

with open('index_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(renewed_html)

print('[성공] index_dashboard.html 리뉴얼 v2 빌드 완료! (크기:', len(renewed_html), 'bytes)')
