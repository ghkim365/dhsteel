# -*- coding: utf-8 -*-
import base64, os, re

logo_path = r'e:\Antigravity\builder-dhsteel-sales\assets\logo_dhsteel_removebg.png'
with open(logo_path, 'rb') as f:
    b64_logo = base64.b64encode(f.read()).decode('utf-8')
data_uri = f'data:image/png;base64,{b64_logo}'

print(f"Base64 data URI length: {len(data_uri)}")

# 1. Fix mailling/mail_report.html
mail_path = r'e:\Antigravity\builder-dhsteel-sales\mailling\mail_report.html'
with open(mail_path, 'r', encoding='utf-8') as f:
    mail_html = f.read()

# Replace ../assets/logo_dhsteel.png with data_uri
mail_html = mail_html.replace('src="../assets/logo_dhsteel.png"', f'src="{data_uri}"')

with open(mail_path, 'w', encoding='utf-8') as f:
    f.write(mail_html)
print("Updated mailling/mail_report.html with inline base64 logo!")

# 2. Fix fax/fax_report.html
fax_path = r'e:\Antigravity\builder-dhsteel-sales\fax\fax_report.html'
with open(fax_path, 'r', encoding='utf-8') as f:
    fax_html = f.read()

# Add CDN scripts if missing
cdn_scripts = '''    <!-- html2canvas for image export -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <!-- jsPDF for PDF export -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>'''

if 'html2canvas.min.js' not in fax_html:
    fax_html = fax_html.replace('<style>', f'{cdn_scripts}\n    <style>')
    print("Added CDN scripts to fax/fax_report.html!")

# Replace ../assets/logo_dhsteel.png with data_uri
fax_html = fax_html.replace('src="../assets/logo_dhsteel.png"', f'src="{data_uri}"')

with open(fax_path, 'w', encoding='utf-8') as f:
    f.write(fax_html)
print("Updated fax/fax_report.html with inline base64 logo and CDN scripts!")

