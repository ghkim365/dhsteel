# -*- coding: utf-8 -*-
import os, re

fax_path = r'e:\Antigravity\builder-dhsteel-sales\fax\fax_report.html'
with open(fax_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update font and styles
new_css = '''
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
    <style>
        :root {
            --navy: #15284D;
            --navy-deep: #0F172A;
            --brand-blue: #2563EB;
            --blue-light: #EFF6FF;
            --accent-blue: #3B82F6;
            --gold: #D97706;
            --gold-light: #FEF3C7;
            --success: #16A34A;
            --success-bg: #DCFCE7;
            --fail: #DC2626;
            --fail-bg: #FEE2E2;
            --text: #1E293B;
            --text-mid: #475569;
            --text-light: #64748B;
            --border: #E2E8F0;
            --border-light: #F1F5F9;
            --bg-screen: #F8FAFC;
            --bg-soft: #F8FAFC;
            --card-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans KR", sans-serif;
            background: var(--bg-screen);
            min-height: 100vh;
            padding: 30px 20px 60px;
            color: var(--text);
            font-size: 13px;
            -webkit-font-smoothing: antialiased;
        }

        /* 컨트롤 패널 */
        .control-panel {
            max-width: 900px;
            margin: 0 auto 16px;
            background: #fff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 22px;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            box-shadow: var(--card-shadow);
        }

        .cp-label {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-mid);
            white-space: nowrap;
        }

        .cp-input, .cp-select {
            padding: 7px 12px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 12.5px;
            font-family: inherit;
            color: var(--text);
            background: #fff;
            outline: none;
            transition: all 0.2s ease;
        }

        .cp-input:focus, .cp-select:focus {
            border-color: var(--brand-blue);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }

        .btn-group {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-left: auto;
        }

        .btn {
            padding: 7.5px 15px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid transparent;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.15s ease;
            font-family: inherit;
            white-space: nowrap;
        }

        .btn-primary {
            background: var(--navy);
            color: #fff;
            border-color: var(--navy);
            box-shadow: 0 2px 6px rgba(21, 40, 77, 0.15);
        }
        .btn-primary:hover {
            background: #1E3A70;
        }

        .btn-export-pdf {
            background: #fff;
            color: #991B1B;
            border-color: #F87171;
        }
        .btn-export-pdf:hover {
            background: #FEF2F2;
        }

        .btn-export-img {
            background: #fff;
            color: var(--brand-blue);
            border-color: #93C5FD;
        }
        .btn-export-img:hover {
            background: var(--blue-light);
        }

        .btn-print {
            background: #fff;
            color: var(--text-mid);
            border-color: var(--border);
        }
        .btn-print:hover {
            background: var(--border-light);
        }

        #status-bar {
            max-width: 900px;
            margin: -6px auto 14px;
            padding: 10px 18px;
            background: var(--blue-light);
            border-left: 3px solid var(--brand-blue);
            border-radius: 0 8px 8px 0;
            font-size: 12.5px;
            color: var(--navy);
            font-weight: 500;
            display: none;
        }

        /* A4 보고서 */
        #report-wrapper {
            max-width: 900px;
            margin: 0 auto;
        }

        .a4-page {
            width: 794px;
            min-height: 1123px;
            background: #fff;
            margin: 0 auto;
            padding: 44px 48px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.07);
            border-radius: 8px;
            border: 1px solid var(--border);
            position: relative;
            font-size: 12px;
            line-height: 1.6;
            color: var(--text);
        }

        .report-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            padding-bottom: 18px;
            border-bottom: 2px solid var(--navy);
            margin-bottom: 22px;
        }

        .report-logo-area {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .report-logo-img {
            height: 42px;
            width: auto;
            object-fit: contain;
        }

        .report-logo-text h1 {
            font-size: 18px;
            font-weight: 600;
            color: var(--navy);
            letter-spacing: -0.3px;
        }

        .report-logo-text p {
            font-size: 11px;
            color: var(--text-light);
            margin-top: 2px;
            font-weight: 500;
        }

        .report-title-area {
            text-align: right;
        }

        .report-doc-type {
            font-size: 10px;
            font-weight: 600;
            color: var(--brand-blue);
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .report-main-title {
            font-size: 19px;
            font-weight: 600;
            color: var(--navy-deep);
            margin-top: 3px;
            letter-spacing: -0.4px;
        }

        .meta-strip {
            display: flex;
            justify-content: space-between;
            background: var(--bg-soft);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 18px;
            margin-bottom: 20px;
            font-size: 11.5px;
        }

        .meta-item {
            display: flex;
            gap: 6px;
        }
        .meta-label {
            color: var(--text-light);
            font-weight: 500;
        }
        .meta-val {
            color: var(--navy);
            font-weight: 600;
        }

        .kpi-row {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 22px;
        }

        .kpi-card {
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 14px 16px;
            background: #fff;
            border-left: 3.5px solid var(--navy);
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }

        .kpi-card.k-success { border-left-color: var(--success); }
        .kpi-card.k-fail { border-left-color: var(--fail); }
        .kpi-card.k-rate { border-left-color: var(--brand-blue); }

        .kpi-card-label {
            font-size: 10.5px;
            font-weight: 600;
            color: var(--text-light);
            margin-bottom: 5px;
        }

        .kpi-card-value {
            font-size: 24px;
            font-weight: 600;
            color: var(--navy);
            line-height: 1.1;
        }

        .kpi-card.k-success .kpi-card-value { color: var(--success); }
        .kpi-card.k-fail .kpi-card-value { color: var(--fail); }
        .kpi-card.k-rate .kpi-card-value { color: var(--brand-blue); }

        .kpi-card-sub {
            font-size: 10px;
            color: var(--text-light);
            margin-top: 5px;
        }

        .section-heading {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 600;
            color: var(--navy);
            margin-bottom: 12px;
            margin-top: 22px;
        }

        .section-bar {
            width: 3.5px;
            height: 15px;
            background: var(--brand-blue);
            border-radius: 2px;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11.5px;
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
        }

        .data-table th {
            background: var(--bg-soft);
            color: var(--navy);
            font-weight: 600;
            padding: 8.5px 12px;
            border-bottom: 1px solid var(--border);
            text-align: left;
            white-space: nowrap;
        }

        .data-table td {
            padding: 7.5px 12px;
            border-bottom: 1px solid var(--border-light);
            color: var(--text);
            vertical-align: middle;
        }

        .data-table tr:hover {
            background-color: #F8FAFC;
        }

        .badge-status {
            display: inline-block;
            padding: 2.5px 8px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            text-align: center;
        }
        .badge-status.success {
            background: var(--success-bg);
            color: var(--success);
            border: 1px solid #BBF7D0;
        }
        .badge-status.fail {
            background: var(--fail-bg);
            color: var(--fail);
            border: 1px solid #FECACA;
        }

        .badge-round {
            background: var(--blue-light);
            color: var(--navy);
            border: 1px solid #BFDBFE;
            padding: 1.5px 7px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 600;
            white-space: nowrap;
        }

        .report-footer {
            margin-top: 28px;
            padding-top: 14px;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 10px;
            color: var(--text-light);
        }

        @media print {
            body {
                background: #fff;
                padding: 0;
            }
            .control-panel, #status-bar {
                display: none !important;
            }
            .a4-page {
                box-shadow: none;
                border: none;
                padding: 15mm 12mm;
                width: 100%;
                min-height: auto;
            }
        }
    </style>
'''

# Replace old font link and style
content = re.sub(r'<link[^>]*href="https://fonts\.googleapis\.com[^>]*>.*?<style>.*?</style>', new_css, content, flags=re.DOTALL)

# Replace SVG logo with official logo_dhsteel.png and update titles
old_logo_pattern = r'<div class="report-logo-box"[^>]*>.*?</div>\s*<div class="report-logo-text">\s*<h1>.*?</h1>'
new_logo = '''<img src="../assets/logo_dhsteel.png" class="report-logo-img" alt="DHSTEEL">
                    <div class="report-logo-text">
                        <h1>대흥정밀 (DHSTEEL)</h1>'''

content = re.sub(old_logo_pattern, new_logo, content, flags=re.DOTALL)

with open(fax_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated fax_report.html successfully!")

