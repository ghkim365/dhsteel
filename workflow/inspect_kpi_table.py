# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('workflow/extracted_body_old.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Lines 150 - 360 (KPIs, Charts, Leads Table) ===')
for l in lines[150:360]:
    print(l, end='')

