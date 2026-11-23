# -*- coding: utf-8 -*-
with open(r'e:\Antigravity\builder-dhsteel-sales\mailling\mail_report.html', 'r', encoding='utf-8') as f:
    text = f.read()

badge_start = text.find('<div class="report-logo-badge">')
if badge_start != -1:
    # Find the end of report-logo-text
    text_end_str = '</p>\n                        </div>'
    text_end = text.find(text_end_str, badge_start)
    if text_end == -1:
        text_end_str = '</p>'
        p_end = text.find(text_end_str, badge_start)
        div_end = text.find('</div>', p_end)
        text_end = div_end + len('</div>')
    else:
        text_end += len(text_end_str)
        
    print(f"Replacing from {badge_start} to {text_end} ({text_end - badge_start} chars)")
    
    new_logo_block = '''<div class="report-logo-badge"><img src="../assets/logo_dhsteel.png" alt="DHSTEEL"></div>
                        <div class="report-logo-text">
                            <h1>대흥정밀 (DHSTEEL)</h1>
                            <p>소구경 파이프 2차 정밀 임가공 전문 기업 | B2B 마케팅 본부</p>
                        </div>'''
                        
    text = text[:badge_start] + new_logo_block + text[text_end:]
    
    with open(r'e:\Antigravity\builder-dhsteel-sales\mailling\mail_report.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced base64 logo with ../assets/logo_dhsteel.png! New file length:", len(text))
else:
    print("report-logo-badge not found")

