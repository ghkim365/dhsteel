with open('mailling/mail_report.html', 'r', encoding='utf-8') as f:
    m = f.read()
with open('fax/fax_report.html', 'r', encoding='utf-8') as f:
    x = f.read()

print('Mail has 10px td:', 'font-size:10px;' in m)
print('Mail has 12px td:', 'font-size:12px;' in m)
print('Mail has 13.5px company:', 'font-size:13.5px; color:var(--navy);' in m)
print('Fax has 10.5px td:', 'font-size:10.5px;' in x)
print('Fax has 12.5px td:', 'font-size:12.5px;' in x)
print('Fax has 13.5px company:', 'font-size:13.5px; color:var(--navy);' in x)

