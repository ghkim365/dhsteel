import re
from collections import Counter

with open('mailling/mail_report.html', 'r', encoding='utf-8') as f:
    mail = f.read()

with open('fax/fax_report.html', 'r', encoding='utf-8') as f:
    fax = f.read()

print('=== MAIL REPORT FONT SIZES ===')
for k, v in Counter(re.findall(r'font-size:\s*[^;\"\'\}]+', mail)).most_common():
    print(f'{k}: {v}')

print('\n=== FAX REPORT FONT SIZES ===')
for k, v in Counter(re.findall(r'font-size:\s*[^;\"\'\}]+', fax)).most_common():
    print(f'{k}: {v}')

