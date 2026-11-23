# -*- coding: utf-8 -*-
import re

# 1. Update mailling/mail_report.html
mail_path = r'e:\Antigravity\builder-dhsteel-sales\mailling\mail_report.html'
with open(mail_path, 'r', encoding='utf-8') as f:
    mail_html = f.read()

# Update .a4-page width from 794px to 900px with max-width: 100%
mail_html = re.sub(
    r'\.a4-page\s*{\s*width:\s*794px;',
    '.a4-page {\n            width: 900px;\n            max-width: 100%;',
    mail_html
)

with open(mail_path, 'w', encoding='utf-8') as f:
    f.write(mail_html)
print("Updated mailling/mail_report.html width to 900px!")

# 2. Update fax/fax_report.html
fax_path = r'e:\Antigravity\builder-dhsteel-sales\fax\fax_report.html'
with open(fax_path, 'r', encoding='utf-8') as f:
    fax_html = f.read()

fax_html = re.sub(
    r'\.a4-page\s*{\s*width:\s*794px;',
    '.a4-page {\n            width: 900px;\n            max-width: 100%;',
    fax_html
)

with open(fax_path, 'w', encoding='utf-8') as f:
    f.write(fax_html)
print("Updated fax/fax_report.html width to 900px!")

