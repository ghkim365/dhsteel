import sys

with open('mailling/mail_report.html', 'r', encoding='utf-8') as f:
    mail_content = f.read()

with open('fax/fax_report.html', 'r', encoding='utf-8') as f:
    fax_content = f.read()

# Mail report adjustments
replacements_mail = [
    ("        .control-panel h2 {\n            width: 100%;\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 17px;",
     "        .control-panel h2 {\n            width: 100%;\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 18px;"),
    ("        .control-panel p {\n            width: 100%;\n            font-size: 12.5px;",
     "        .control-panel p {\n            width: 100%;\n            font-size: 13.5px;"),
    ("        .ctrl-group label {\n            font-size: 11.5px;",
     "        .ctrl-group label {\n            font-size: 12.5px;"),
    ("        .ctrl-group input,\n        .ctrl-group select {\n            border: 1px solid var(--border);\n            border-radius: 6px;\n            padding: 8px 12px;\n            font-size: 12.5px;",
     "        .ctrl-group input,\n        .ctrl-group select {\n            border: 1px solid var(--border);\n            border-radius: 6px;\n            padding: 8px 12px;\n            font-size: 13.5px;"),
    ("        .btn {\n            padding: 8px 16px;\n            border-radius: 6px;\n            font-size: 12.5px;",
     "        .btn {\n            padding: 8px 16px;\n            border-radius: 6px;\n            font-size: 13.5px;"),
    ("            font-size: 11.5px;\n            line-height: 1.55;\n            color: var(--text);\n        }",
     "            font-size: 13px;\n            line-height: 1.6;\n            color: var(--text);\n        }"),
    ("        .report-logo-text h1 {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 17px;",
     "        .report-logo-text h1 {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 18px;"),
    ("        .report-logo-text p {\n            font-size: 10.5px;",
     "        .report-logo-text p {\n            font-size: 12px;"),
    ("        .report-doc-type {\n            font-size: 10px;",
     "        .report-doc-type {\n            font-size: 11px;"),
    ("        .report-main-title {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 20px;",
     "        .report-main-title {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 21px;"),
    ("        .report-period {\n            font-size: 11.5px;",
     "        .report-period {\n            font-size: 12.5px;"),
    ("        .meta-item label {\n            display: block;\n            font-size: 9.5px;",
     "        .meta-item label {\n            display: block;\n            font-size: 11px;"),
    ("        .meta-item .meta-val {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 16px;",
     "        .meta-item .meta-val {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 17px;"),
    ("        .meta-item .meta-sub {\n            font-size: 9.5px;",
     "        .meta-item .meta-sub {\n            font-size: 11px;"),
    ("        .section-title {\n            font-size: 10.5px;",
     "        .section-title {\n            font-size: 12.5px;"),
    ("        .kpi-card-label {\n            font-size: 9.5px;",
     "        .kpi-card-label {\n            font-size: 11.5px;"),
    ("        .kpi-card-value {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 24px;",
     "        .kpi-card-value {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 25px;"),
    ("        .kpi-card-sub {\n            font-size: 9.5px;",
     "        .kpi-card-sub {\n            font-size: 11px;"),
    ("        .round-pill {\n            display: flex;\n            align-items: center;\n            gap: 7px;\n            background: var(--bg-soft);\n            border: 1px solid var(--border);\n            border-radius: 4px;\n            padding: 5px 12px;\n            font-size: 11.5px;",
     "        .round-pill {\n            display: flex;\n            align-items: center;\n            gap: 7px;\n            background: var(--bg-soft);\n            border: 1px solid var(--border);\n            border-radius: 4px;\n            padding: 5px 12px;\n            font-size: 12.5px;"),
    ("        .round-pill .round-count {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 13px;",
     "        .round-pill .round-count {\n            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif;\n            font-size: 14px;"),
    ("        .log-table {\n            width: 100%;\n            border-collapse: collapse;\n            font-size: 10.5px;\n        }",
     "        .log-table {\n            width: 100%;\n            border-collapse: collapse;\n            font-size: 12.5px;\n        }"),
    ("        .log-table thead th {\n            padding: 8px 9px;\n            font-weight: 600;\n            text-align: left;\n            font-size: 10px;\n            white-space: nowrap;\n        }",
     "        .log-table thead th {\n            padding: 9px 10px;\n            font-weight: 600;\n            text-align: left;\n            font-size: 12px;\n            white-space: nowrap;\n        }"),
    ("        .log-table tbody td {\n            padding: 7px 9px;\n            color: var(--text);\n            vertical-align: middle;\n        }",
     "        .log-table tbody td {\n            padding: 8px 10px;\n            color: var(--text);\n            vertical-align: middle;\n        }"),
    ("        .status-badge {\n            display: inline-block;\n            padding: 1px 7px;\n            border-radius: 3px;\n            font-size: 9.5px;",
     "        .status-badge {\n            display: inline-block;\n            padding: 2px 8px;\n            border-radius: 3px;\n            font-size: 11px;"),
    ("        .round-badge {\n            display: inline-block;\n            background: var(--gold-light);\n            color: #7A5C00;\n            border: 1px solid #DEC97A;\n            padding: 1px 6px;\n            border-radius: 3px;\n            font-size: 9.5px;",
     "        .round-badge {\n            display: inline-block;\n            background: var(--gold-light);\n            color: #7A5C00;\n            border: 1px solid #DEC97A;\n            padding: 2px 7px;\n            border-radius: 3px;\n            font-size: 11px;"),
    ("        .info-chip {\n            display: inline-flex;\n            align-items: center;\n            gap: 4px;\n            padding: 1px 8px;\n            border-radius: 3px;\n            font-size: 9.5px;",
     "        .info-chip {\n            display: inline-flex;\n            align-items: center;\n            gap: 4px;\n            padding: 2px 8px;\n            border-radius: 3px;\n            font-size: 11px;"),
    ("        .info-chip .chip-icon {\n            font-size: 9px;",
     "        .info-chip .chip-icon {\n            font-size: 10.5px;"),
    ("        .report-footer-left {\n            font-size: 9.5px;",
     "        .report-footer-left {\n            font-size: 11px;"),
    ("        .report-footer-left strong {\n            display: block;\n            font-size: 10.5px;",
     "        .report-footer-left strong {\n            display: block;\n            font-size: 12px;"),
    ("        .report-footer-right {\n            text-align: right;\n            font-size: 9.5px;",
     "        .report-footer-right {\n            text-align: right;\n            font-size: 11px;"),
    ("        .confidential-badge {\n            display: inline-block;\n            border: 1px solid var(--text-light);\n            color: var(--text-light);\n            border-radius: 3px;\n            padding: 1px 7px;\n            font-size: 8.5px;",
     "        .confidential-badge {\n            display: inline-block;\n            border: 1px solid var(--text-light);\n            color: var(--text-light);\n            border-radius: 3px;\n            padding: 2px 8px;\n            font-size: 10px;"),
    ("        .tab-btn {\n            flex: 1;\n            padding: 14px 20px;\n            font-size: 13px;",
     "        .tab-btn {\n            flex: 1;\n            padding: 14px 20px;\n            font-size: 14px;")
]

mail_count = 0
for src, dst in replacements_mail:
    if src in mail_content:
        mail_content = mail_content.replace(src, dst)
        mail_count += 1
    else:
        print('MAIL NOT FOUND:', repr(src[:40]))

with open('mailling/mail_report.html', 'w', encoding='utf-8') as f:
    f.write(mail_content)
print(f'Mail report updated: {mail_count}/{len(replacements_mail)} replacements.')

# Fax report adjustments
replacements_fax = [
    ("        .cp-label {\n            font-size: 12px;",
     "        .cp-label {\n            font-size: 13px;"),
    ("        .cp-input, .cp-select {\n            padding: 7px 12px;\n            border: 1px solid var(--border);\n            border-radius: 8px;\n            font-size: 12.5px;",
     "        .cp-input, .cp-select {\n            padding: 7.5px 12px;\n            border: 1px solid var(--border);\n            border-radius: 8px;\n            font-size: 13.5px;"),
    ("        .btn {\n            padding: 7.5px 15px;\n            border-radius: 8px;\n            font-size: 12.5px;",
     "        .btn {\n            padding: 8px 16px;\n            border-radius: 8px;\n            font-size: 13.5px;"),
    ("        #status-bar {\n            max-width: 900px;\n            margin: -6px auto 14px;\n            padding: 10px 18px;\n            background: var(--blue-light);\n            border-left: 3px solid var(--brand-blue);\n            border-radius: 0 8px 8px 0;\n            font-size: 12.5px;",
     "        #status-bar {\n            max-width: 900px;\n            margin: -6px auto 14px;\n            padding: 10px 18px;\n            background: var(--blue-light);\n            border-left: 3px solid var(--brand-blue);\n            border-radius: 0 8px 8px 0;\n            font-size: 13px;"),
    ("            font-size: 12px;\n            line-height: 1.6;\n            color: var(--text);\n        }",
     "            font-size: 13px;\n            line-height: 1.6;\n            color: var(--text);\n        }"),
    ("        .report-logo-text h1 {\n            font-size: 18px;",
     "        .report-logo-text h1 {\n            font-size: 19px;"),
    ("        .report-logo-text p {\n            font-size: 11px;",
     "        .report-logo-text p {\n            font-size: 12px;"),
    ("        .report-doc-type {\n            font-size: 10px;",
     "        .report-doc-type {\n            font-size: 11px;"),
    ("        .report-main-title {\n            font-size: 19px;",
     "        .report-main-title {\n            font-size: 21px;"),
    ("        .meta-strip {\n            display: flex;\n            justify-content: space-between;\n            background: var(--bg-soft);\n            border: 1px solid var(--border);\n            border-radius: 8px;\n            padding: 10px 18px;\n            margin-bottom: 20px;\n            font-size: 11.5px;\n        }",
     "        .meta-strip {\n            display: flex;\n            justify-content: space-between;\n            background: var(--bg-soft);\n            border: 1px solid var(--border);\n            border-radius: 8px;\n            padding: 10px 18px;\n            margin-bottom: 20px;\n            font-size: 12.5px;\n        }"),
    ("        .kpi-card-label {\n            font-size: 10.5px;",
     "        .kpi-card-label {\n            font-size: 11.5px;"),
    ("        .kpi-card-value {\n            font-size: 24px;",
     "        .kpi-card-value {\n            font-size: 25px;"),
    ("        .kpi-card-sub {\n            font-size: 10px;",
     "        .kpi-card-sub {\n            font-size: 11px;"),
    ("        .section-heading {\n            display: flex;\n            align-items: center;\n            gap: 8px;\n            font-size: 13px;",
     "        .section-heading {\n            display: flex;\n            align-items: center;\n            gap: 8px;\n            font-size: 14px;"),
    ("        .data-table {\n            width: 100%;\n            border-collapse: collapse;\n            font-size: 11.5px;",
     "        .data-table {\n            width: 100%;\n            border-collapse: collapse;\n            font-size: 12.5px;"),
    ("        .data-table th {\n            background: var(--bg-soft);\n            color: var(--navy);\n            font-weight: 600;\n            padding: 8.5px 12px;",
     "        .data-table th {\n            background: var(--bg-soft);\n            color: var(--navy);\n            font-weight: 600;\n            padding: 9px 12px;"),
    ("        .data-table td {\n            padding: 7.5px 12px;",
     "        .data-table td {\n            padding: 8px 12px;"),
    ("        .badge-status {\n            display: inline-block;\n            padding: 2.5px 8px;\n            border-radius: 4px;\n            font-size: 10px;",
     "        .badge-status {\n            display: inline-block;\n            padding: 2.5px 8px;\n            border-radius: 4px;\n            font-size: 11px;"),
    ("        .badge-round {\n            background: var(--blue-light);\n            color: var(--navy);\n            border: 1px solid #BFDBFE;\n            padding: 1.5px 7px;\n            border-radius: 4px;\n            font-size: 10px;",
     "        .badge-round {\n            background: var(--blue-light);\n            color: var(--navy);\n            border: 1px solid #BFDBFE;\n            padding: 2px 7px;\n            border-radius: 4px;\n            font-size: 11px;"),
    ("        .report-footer {\n            margin-top: 28px;\n            padding-top: 14px;\n            border-top: 1px solid var(--border);\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n            font-size: 10px;",
     "        .report-footer {\n            margin-top: 28px;\n            padding-top: 14px;\n            border-top: 1px solid var(--border);\n            display: flex;\n            justify-content: space-between;\n            align-items: center;\n            font-size: 11.5px;")
]

fax_count = 0
for src, dst in replacements_fax:
    if src in fax_content:
        fax_content = fax_content.replace(src, dst)
        fax_count += 1
    else:
        print('FAX NOT FOUND:', repr(src[:40]))

with open('fax/fax_report.html', 'w', encoding='utf-8') as f:
    f.write(fax_content)
print(f'Fax report updated: {fax_count}/{len(replacements_fax)} replacements.')

