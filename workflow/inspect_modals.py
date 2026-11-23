# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('workflow/extracted_body_old.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Lines 360 - 520 (SendLabs card & Modals) ===')
for l in lines[360:520]:
    print(l, end='')

