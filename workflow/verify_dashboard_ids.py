# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL)
js_combined = ' '.join(scripts[1:])
get_ids = set(re.findall(r'getElementById\([\'"]([^\'"]+)[\'"]\)', js_combined))

body_part = html[:html.find('<script', html.find('<body>'))]
html_ids = set(re.findall(r'id=[\'"]([^\'"]+)[\'"]', body_part))

missing = get_ids - html_ids
print(f'Total required IDs: {len(get_ids)}')
print(f'Matched IDs in HTML: {len(get_ids & html_ids)}')
print(f'Missing IDs count: {len(missing)}')
if missing:
    print('Missing IDs:', sorted(list(missing)))

