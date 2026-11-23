# -*- coding: utf-8 -*-
import os, re

mail_path = r'e:\Antigravity\builder-dhsteel-sales\mailling\mail_report.html'
with open(mail_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace Google Fonts link with Pretendard
old_font_link = r'<link\s+href="https://fonts\.googleapis\.com[^"]+"\s+rel="stylesheet">'
new_font_link = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">'
content = re.sub(old_font_link, new_font_link, content)

# 2. Extract CSS and update
style_match = re.search(r'(<style>)(.*?)(</style>)', content, re.DOTALL)
if style_match:
    style_inner = style_match.group(2)
    
    # Update :root tokens
    old_root = re.search(r':root\s*{.*?--accent:\s*var\(--gold\);\s*}', style_inner, re.DOTALL)
    if old_root:
        new_root = ''':root {
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

            /* aliases for backward compat */
            --brand: var(--navy);
            --brand-light: #1E3A70;
            --accent: var(--brand-blue);
        }'''
        style_inner = style_inner[:old_root.start()] + new_root + style_inner[old_root.end():]
        
    # Replace font families
    style_inner = re.sub(r"font-family:\s*'Noto Sans KR',\s*sans-serif;", "font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;", style_inner)
    style_inner = re.sub(r"font-family:\s*'Outfit',\s*sans-serif;", "font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;", style_inner)

    # Replace bold weights: 700, 800, 900 -> 600 (semi-bold)
    style_inner = re.sub(r'font-weight:\s*(?:700|800|900);', 'font-weight: 600;', style_inner)

    # Enhance body font size and smoothness
    style_inner = re.sub(r'font-size:\s*12px;', 'font-size: 12.5px;', style_inner)
    style_inner = re.sub(r'font-size:\s*11px;', 'font-size: 11.5px;', style_inner)

    # Style .report-logo-badge for external img
    logo_badge_css = '''.report-logo-badge {
            height: 42px;
            width: auto;
            object-fit: contain;
            background: transparent;
            border: none;
            box-shadow: none;
            display: inline-flex;
            align-items: center;
        }
        .report-logo-badge img {
            height: 42px;
            width: auto;
            object-fit: contain;
        }'''
    style_inner = re.sub(r'\.report-logo-badge\s*{[^}]*}', logo_badge_css, style_inner)

    # Modernize control panel & tabs
    style_inner = re.sub(r'\.control-panel\s*{[^}]*}', '''.control-panel {
            max-width: 900px;
            margin: 0 auto 20px;
            background: #fff;
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: var(--card-shadow);
            display: flex;
            flex-wrap: wrap;
            align-items: flex-end;
            gap: 14px;
            border: 1px solid var(--border);
        }''', style_inner)

    style_inner = re.sub(r'\.tab-nav\s*{[^}]*}', '''.tab-nav {
            max-width: 900px;
            margin: 0 auto 16px;
            display: flex;
            gap: 8px;
            background: #fff;
            padding: 6px;
            border-radius: 10px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }''', style_inner)

    content = content[:style_match.start(2)] + style_inner + content[style_match.end(2):]

# 3. Replace the massive 650KB base64 logo in HTML
old_logo_pattern = r'<div class="report-logo-badge"><img\s+src="data:image/png;base64,[^"]+"\s*></div>\s*<div class="report-logo-text">\s*<h1>대흥정밀</h1>\s*<p>[^<]*</p>\s*</div>'
new_logo = '''<div class="report-logo-badge"><img src="../assets/logo_dhsteel.png" alt="DHSTEEL"></div>
                        <div class="report-logo-text">
                            <h1>대흥정밀 (DHSTEEL)</h1>
                            <p>소구경 파이프 2차 정밀 임가공 전문 기업 | B2B 마케팅 본부</p>
                        </div>'''

content = re.sub(old_logo_pattern, new_logo, content, flags=re.DOTALL)

with open(mail_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated mail_report.html successfully! New size: {len(content)} bytes")

