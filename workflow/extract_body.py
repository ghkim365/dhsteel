# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open('index_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

body_start = text.find('<body>')
first_script = text.find('<script', body_start)
body_html = text[body_start:first_script]

# Let's save body_html to a temporary file in workflow for inspection
with open('workflow/extracted_body_old.html', 'w', encoding='utf-8') as f:
    f.write(body_html)

print('Saved workflow/extracted_body_old.html, length:', len(body_html))

