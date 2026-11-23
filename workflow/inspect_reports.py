import re

with open(r'e:\Antigravity\builder-dhsteel-sales\mailling\mail_report.html', 'r', encoding='utf-8') as f:
    mail_html = f.read()

m_scripts = re.findall(r'<script>(.*?)</script>', mail_html, re.DOTALL)
m_funcs = []
for s in m_scripts:
    m_funcs.extend(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', s))
print(f"mail_report functions ({len(m_funcs)}):", m_funcs)

with open(r'e:\Antigravity\builder-dhsteel-sales\fax\fax_report.html', 'r', encoding='utf-8') as f:
    fax_html = f.read()

f_scripts = re.findall(r'<script>(.*?)</script>', fax_html, re.DOTALL)
f_funcs = []
for s in f_scripts:
    f_funcs.extend(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', s))
print(f"\nfax_report functions ({len(f_funcs)}):", f_funcs)
