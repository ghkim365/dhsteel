# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('workflow/extracted_body_old.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if any(k in line for k in ['<header', '<nav', '<main', '<aside', '<section', 'kpi-card', 'class="card', 'id="quoteModal', 'id="errModal', 'id="dashboard-wrapper', 'leads-body', 'class="modal']):
        print(f"Line {idx+1}: {line.strip()[:100]}")

