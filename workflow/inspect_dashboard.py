# -*- coding: utf-8 -*-
import os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

backup = 'index_dashboard - 20161120_0112pm.html'
print(f'Backup exists: {os.path.exists(backup)}, Size: {os.path.getsize(backup) if os.path.exists(backup) else 0}')

with open('index_dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
print(f'Functions defined in index_dashboard: {len(funcs)}')
print('Functions:', funcs)

get_ids = re.findall(r'getElementById\([\'"]([^\'"]+)[\'"]\)', text)
print(f'Unique getElementById targets: {len(set(get_ids))}')
print('IDs:', sorted(list(set(get_ids))))

# Find all script tags content
scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', text, re.DOTALL)
print(f'Total script tags: {len(scripts)}')

# Let's inspect CSS style tag
styles = re.findall(r'<style\b[^>]*>(.*?)</style>', text, re.DOTALL)
print(f'Total style tags: {len(styles)}')

