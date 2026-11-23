# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect everything between <body> and the first <script>
body_start = text.find('<body>')
first_script = text.find('<script', body_start)
body_html = text[body_start:first_script]

print('Body HTML length before script:', len(body_html))

# Let's find major containers inside body
containers = re.findall(r'<div\b[^>]*\bid=[\'"]([^\'"]+)[\'"][^>]*>', body_html)
print('Major container IDs:', containers)

# Let's see the main script block
scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', text, re.DOTALL)
for i, s in enumerate(scripts):
    print(f'Script {i} length: {len(s)}')
    # print first 200 chars
    print(f'Script {i} preview: {s.strip()[:150]}...')

