import re

# ==========================================
# 1. Update fax/fax_report.html
# ==========================================
with open('fax/fax_report.html', 'r', encoding='utf-8') as f:
    fax = f.read()

# Replace width 900px -> 1020px
fax = fax.replace('max-width: 900px;', 'max-width: 1020px;')
fax = fax.replace('width: 900px;', 'width: 1020px;')

# Remove redundant note "(샌드랩스 대량 팩스)" in table rendering
old_fax_tr = """                tr.innerHTML = `
                    <td style="text-align:center; font-family:'Outfit'; font-weight:600; font-size:12.5px; color:#555;">#${item.id || (idx + 1)}</td>
                    <td style="font-size:12.5px; color:#555;">${item.date || '-'}</td>
                    <td style="font-weight:600; font-size:13.5px; color:var(--navy);">${item.company || '-'}</td>
                    <td style="font-family:'Outfit'; font-size:12.5px; color:#444;">${item.fax || '-'}</td>
                    <td style="text-align:center;"><span class="badge-round">${item.round || '-'}</span></td>
                    <td style="text-align:center;">${statusBadge}</td>
                    <td style="font-size:12.5px; color:#444;">${item.detail || '-'}${noteInfo}</td>
                `;"""

new_fax_tr = """                const cleanNote = (item.note && item.note !== '샌드랩스 대량 팩스') ? ` <span style="color:#888;">(${item.note})</span>` : '';
                tr.innerHTML = `
                    <td style="text-align:center; font-family:'Outfit'; font-weight:600; font-size:12.5px; color:#555; white-space:nowrap;">#${item.id || (idx + 1)}</td>
                    <td style="font-size:12.5px; color:#555; white-space:nowrap;">${item.date || '-'}</td>
                    <td style="font-weight:600; font-size:13.5px; color:var(--navy); white-space:nowrap;">${item.company || '-'}</td>
                    <td style="font-family:'Outfit'; font-size:12.5px; color:#444; white-space:nowrap;">${item.fax || '-'}</td>
                    <td style="text-align:center; white-space:nowrap;"><span class="badge-round">${item.round || '-'}</span></td>
                    <td style="text-align:center; white-space:nowrap;">${statusBadge}</td>
                    <td style="font-size:12.5px; color:#444; white-space:nowrap;">${item.detail || '-'}${cleanNote}</td>
                `;"""

if old_fax_tr in fax:
    fax = fax.replace(old_fax_tr, new_fax_tr)
    print("fax_report tr updated with cleanNote and nowrap!")
else:
    print("Warning: old_fax_tr not found in fax_report.html!")

# Update table header widths in fax_report.html
old_fax_thead = """                <thead>
                    <tr>
                        <th style="width: 50px; text-align:center;">연번</th>
                        <th style="width: 90px;">발송일자</th>
                        <th style="width: 140px;">수신 업체명</th>
                        <th style="width: 110px;">팩스 번호</th>
                        <th style="width: 95px; text-align:center;">발송회차</th>
                        <th style="width: 70px; text-align:center;">발송상태</th>
                        <th>세부결과 및 비고</th>
                    </tr>
                </thead>"""

new_fax_thead = """                <thead>
                    <tr>
                        <th style="width: 55px; text-align:center; white-space:nowrap;">연번</th>
                        <th style="width: 105px; white-space:nowrap;">발송일자</th>
                        <th style="width: 160px; white-space:nowrap;">수신 업체명</th>
                        <th style="width: 120px; white-space:nowrap;">팩스 번호</th>
                        <th style="width: 125px; text-align:center; white-space:nowrap;">발송회차</th>
                        <th style="width: 75px; text-align:center; white-space:nowrap;">발송상태</th>
                        <th style="white-space:nowrap;">세부결과 및 비고</th>
                    </tr>
                </thead>"""

if old_fax_thead in fax:
    fax = fax.replace(old_fax_thead, new_fax_thead)
    print("fax_report thead updated successfully!")
else:
    # Try searching for thead if widths slightly differ
    print("Notice: old_fax_thead exact match not found, checking with regex")
    fax = re.sub(r'<thead>\s*<tr>\s*<th style="width:\s*50px;.*?</tr>\s*</thead>', new_fax_thead, fax, flags=re.DOTALL)

with open('fax/fax_report.html', 'w', encoding='utf-8') as f:
    f.write(fax)


# ==========================================
# 2. Update mailling/mail_report.html
# ==========================================
with open('mailling/mail_report.html', 'r', encoding='utf-8') as f:
    mail = f.read()

# Replace width 900px -> 1020px
mail = mail.replace('max-width: 900px;', 'max-width: 1020px;')
mail = mail.replace('width: 900px;', 'width: 1020px;')

# Remove redundant "Gmail API 발송 완료" in table rendering
old_mail_main_row = """                // 메인 행
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

new_mail_main_row = """                // 세부 결과 문구 간소화 (Gmail API 발송 완료 등 중복 문구 제거)
                let displayDetail = detail;
                if (isSuccess && (displayDetail === 'Gmail API 발송 완료' || displayDetail === '정상 발송' || !displayDetail)) {
                    displayDetail = '<span style="color:var(--text-light); font-size:11.5px;">—</span>';
                }

                // 메인 행
                const mainRow = `<tr>
                <td style="color: var(--text-light); font-size:12px; white-space:nowrap;">${idx + 1}</td>
                <td style="font-weight:600; font-size:12.5px; white-space:nowrap;">${log.id || idx + 1}</td>
                <td style="font-size:12px; color: var(--text-light); white-space:nowrap;">${dateStr}</td>
                <td style="font-weight:600; font-size:13.5px; color:var(--navy); white-space:nowrap;">${escHtml(log.company || '—')}</td>
                <td style="font-size:12px; color: var(--text-mid); white-space:nowrap;">${escHtml(log.region || '—')}</td>
                <td style="font-size:12.5px; color: var(--text); white-space:nowrap;">${escHtml(log.email || '—')}</td>
                <td style="white-space:nowrap;"><span class="round-badge">${escHtml(log.round || '—')}</span></td>
                <td style="white-space:nowrap;">${badge}</td>
                <td style="font-size:12.5px; color: var(--text);">${displayDetail}</td>
            </tr>`;"""

if old_mail_main_row in mail:
    mail = mail.replace(old_mail_main_row, new_mail_main_row)
    print("mail_report mainRow updated with displayDetail and nowrap!")
else:
    print("Warning: old_mail_main_row not found in mail_report.html!")

# Update table thead widths in mail_report.html
old_mail_thead = """                        <tr>
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

new_mail_thead = """                        <tr>
                            <th style="width:32px; white-space:nowrap;">#</th>
                            <th style="width:44px; white-space:nowrap;">연번</th>
                            <th style="width:125px; white-space:nowrap;">발송 일시</th>
                            <th style="width:150px; white-space:nowrap;">회사명</th>
                            <th style="width:60px; white-space:nowrap;">지역</th>
                            <th style="width:180px; white-space:nowrap;">이메일 주소</th>
                            <th style="width:115px; white-space:nowrap;">발송 회차</th>
                            <th style="width:60px; white-space:nowrap;">상태</th>
                            <th style="white-space:nowrap;">세부 결과 · 연락처 · 사이트</th>
                        </tr>"""

if old_mail_thead in mail:
    mail = mail.replace(old_mail_thead, new_mail_thead)
    print("mail_report thead updated successfully!")
else:
    print("Warning: old_mail_thead not found in mail_report.html!")

# Update mail meta bar to include "Gmail API" channel clearly
old_meta_bar = """                <div class="meta-bar">
                    <div class="meta-item">
                        <label>보고서 번호</label>
                        <div class="meta-val" style="font-size:13px;" id="rpt-no">DHR-MAIL-20261123</div>
                        <div class="meta-sub" id="rpt-date">작성일: 2026.11.23</div>
                    </div>
                    <div class="meta-item">
                        <label>담당자</label>
                        <div class="meta-val" style="font-size:15px;" id="rpt-manager">—</div>
                        <div class="meta-sub">작성 책임자</div>
                    </div>
                    <div class="meta-item">
                        <label>결재자</label>
                        <div class="meta-val" style="font-size:15px;" id="rpt-approver">—</div>
                        <div class="meta-sub">최종 승인자</div>
                    </div>
                    <div class="meta-item">
                        <label>데이터 소스</label>
                        <div class="meta-val" style="font-size:11px; margin-top: 4px;">Google Sheets</div>
                        <div class="meta-sub">builder-dhsteel_data / mail_log</div>
                    </div>
                </div>"""

new_meta_bar = """                <div class="meta-bar">
                    <div class="meta-item">
                        <label>보고서 번호</label>
                        <div class="meta-val" style="font-size:13px;" id="rpt-no">DHR-MAIL-20261123</div>
                        <div class="meta-sub" id="rpt-date">작성일: 2026.11.23</div>
                    </div>
                    <div class="meta-item">
                        <label>발송 채널</label>
                        <div class="meta-val" style="font-size:14px; color:var(--brand-blue);">Gmail API</div>
                        <div class="meta-sub">구글 워크스페이스 아웃바운드</div>
                    </div>
                    <div class="meta-item">
                        <label>담당자 / 결재자</label>
                        <div class="meta-val" style="font-size:13px;" id="rpt-manager">영업마케팅팀</div>
                        <div class="meta-sub">작성 및 결재</div>
                    </div>
                    <div class="meta-item">
                        <label>데이터 소스</label>
                        <div class="meta-val" style="font-size:11px; margin-top: 4px;">Google Sheets</div>
                        <div class="meta-sub">builder-dhsteel_data / mail_log</div>
                    </div>
                </div>"""

if old_meta_bar in mail:
    mail = mail.replace(old_meta_bar, new_meta_bar)
    print("mail_report meta-bar updated with Gmail API channel!")
else:
    print("Notice: meta-bar slight difference, checking...")

with open('mailling/mail_report.html', 'w', encoding='utf-8') as f:
    f.write(mail)

print("Updates applied to both files!")

