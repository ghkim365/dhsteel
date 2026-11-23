import re

with open('mailling/mail_report.html', 'r', encoding='utf-8') as f:
    mail = f.read()

lines = mail.splitlines()
print('=== Inline font-size in mail_report.html ===')
for i, line in enumerate(lines):
    if 'font-size' in line and i > 800: # inside JS
        print(f'{i+1}: {line.strip()[:100]}')

with open('fax/fax_report.html', 'r', encoding='utf-8') as f:
    fax = f.read()

lines_fax = fax.splitlines()
print('\n=== Inline font-size in fax_report.html ===')
for i, line in enumerate(lines_fax):
    if 'font-size' in line and i > 400: # inside JS
        print(f'{i+1}: {line.strip()[:100]}')

