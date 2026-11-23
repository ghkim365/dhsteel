import re

# 1. Update mail_report.html
with open('mailling/mail_report.html', 'r', encoding='utf-8') as f:
    mail = f.read()

# Update mainRow template literals in mail_report.html
old_main_row = """                // 메인 행
                const mainRow = `<tr>
                <td style="color: var(--text-light); font-size:10px;">${idx + 1}</td>
                <td style="font-weight:600;">${log.id || idx + 1}</td>
                <td style="font-size:10px; color: var(--text-light);">${dateStr}</td>
                <td style="font-weight:600; font-size:11px;">${escHtml(log.company || '—')}</td>
                <td style="font-size:10px; color: var(--text-light);">${escHtml(log.region || '—')}</td>
                <td style="font-size:10px; color: var(--text-light);">${escHtml(log.email || '—')}</td>
                <td><span class="round-badge">${escHtml(log.round || '—')}</span></td>
                <td>${badge}</td>
                <td style="font-size:10px; color: var(--text-light);">${detail}</td>
            </tr>`;"""

new_main_row = """                // 메인 행
                const mainRow = `<tr>
                <td style="color: var(--text-light); font-size:12px;">${idx + 1}</td>
                <td style="font-weight:600; font-size:12.5px;">${log.id || idx + 1}</td>
                <td style="font-size:12px; color: var(--text-light);">${dateStr}</td>
                <td style="font-weight:600; font-size:13.5px; color:var(--navy);">${escHtml(log.company || '—')}</td>
                <td style="font-size:12px; color: var(--text-mid);">${escHtml(log.region || '—')}</td>
                <td style="font-size:12.5px; color: var(--text);">${escHtml(log.email || '—')}</td>
                <td><span class="round-badge">${escHtml(log.round || '—')}</span></td>
                <td>${badge}</td>
                <td style="font-size:12.5px; color: var(--text);">${detail}</td>
            </tr>`;"""

if old_main_row in mail:
    mail = mail.replace(old_main_row, new_main_row)
    print("mail_report mainRow replaced successfully!")
else:
    print("Warning: old_main_row not found in mail_report.html!")

# Update chip styles in CSS if needed
mail = mail.replace('padding: 2px 8px;\n            border-radius: 3px;\n            font-size: 11px;',
                    'padding: 3px 9px;\n            border-radius: 4px;\n            font-size: 11.5px;')

# Update table thead widths in mail_report.html
old_thead = """                        <tr>
                            <th style="width:26px;">#</th>
                            <th style="width:38px;">연번</th>
                            <th style="width:112px;">발송 일시</th>
                            <th style="width:95px;">회사명</th>
                            <th style="width:60px;">지역</th>
                            <th style="width:130px;">이메일 주소</th>
                            <th style="width:52px;">발송 회차</th>
                            <th style="width:56px;">상태</th>
                            <th>세부 결과 · 연락처 · 사이트</th>
                        </tr>"""

new_thead = """                        <tr>
                            <th style="width:32px;">#</th>
                            <th style="width:44px;">연번</th>
                            <th style="width:116px;">발송 일시</th>
                            <th style="width:110px;">회사명</th>
                            <th style="width:60px;">지역</th>
                            <th style="width:150px;">이메일 주소</th>
                            <th style="width:64px;">발송 회차</th>
                            <th style="width:58px;">상태</th>
                            <th>세부 결과 · 연락처 · 사이트</th>
                        </tr>"""

if old_thead in mail:
    mail = mail.replace(old_thead, new_thead)
    print("mail_report thead replaced successfully!")

with open('mailling/mail_report.html', 'w', encoding='utf-8') as f:
    f.write(mail)

# 2. Update fax_report.html
with open('fax/fax_report.html', 'r', encoding='utf-8') as f:
    fax = f.read()

old_fax_tr = """                tr.innerHTML = `
                    <td style="text-align:center; font-family:'Outfit'; font-weight:600; color:#555;">#${item.id || (idx + 1)}</td>
                    <td style="font-size:10.5px; color:#555;">${item.date || '-'}</td>
                    <td style="font-weight:700; color:var(--navy);">${item.company || '-'}</td>
                    <td style="font-family:'Outfit'; font-size:11px;">${item.fax || '-'}</td>
                    <td style="text-align:center;"><span class="badge-round">${item.round || '-'}</span></td>
                    <td style="text-align:center;">${statusBadge}</td>
                    <td style="font-size:10.5px; color:#444;">${item.detail || '-'}${noteInfo}</td>
                `;"""

new_fax_tr = """                tr.innerHTML = `
                    <td style="text-align:center; font-family:'Outfit'; font-weight:600; font-size:12.5px; color:#555;">#${item.id || (idx + 1)}</td>
                    <td style="font-size:12.5px; color:#555;">${item.date || '-'}</td>
                    <td style="font-weight:600; font-size:13.5px; color:var(--navy);">${item.company || '-'}</td>
                    <td style="font-family:'Outfit'; font-size:12.5px; color:#444;">${item.fax || '-'}</td>
                    <td style="text-align:center;"><span class="badge-round">${item.round || '-'}</span></td>
                    <td style="text-align:center;">${statusBadge}</td>
                    <td style="font-size:12.5px; color:#444;">${item.detail || '-'}${noteInfo}</td>
                `;"""

if old_fax_tr in fax:
    fax = fax.replace(old_fax_tr, new_fax_tr)
    print("fax_report tr replaced successfully!")
else:
    print("Warning: old_fax_tr not found in fax_report.html!")

with open('fax/fax_report.html', 'w', encoding='utf-8') as f:
    f.write(fax)

print("Both report JS templates updated successfully!")

