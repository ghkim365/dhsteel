# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('workflow/extracted_body_old.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Lines 40 - 150 (Header & Mode switch) ===')
for l in lines[39:150]:
    print(l, end='')

