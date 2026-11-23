# -*- coding: utf-8 -*-
import os, sys

sys.stdout.reconfigure(encoding='utf-8')

plan_file = r'E:\Antigravity\builder-dhsteel-sales\plan\dhsteel_plan_2026.html'
with open(plan_file, 'r', encoding='utf-8') as f:
    text = f.read()

phase19_card = '''    <!-- PHASE 19 (2026-11-23) -->
    <div class="card" style="border: 2px solid #10B981;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0;"><span class="badge badge-success">PHASE 19</span> 검증 우량 68개사 3차 정기 이메일 발송 준비 완료</h2>
        <span style="font-size:12px; color:#10B981; font-weight:700;">2026-11-23 발송 대기</span>
      </div>
      <div class="tip-box green" style="margin-top:12px;">
        • <strong>3차 정기 메일 타겟 확정</strong>: 11/09 성공 67개사 + 코베아(오타 정제) 총 68개사 선별 완료<br>
        • <strong>구글 시트 연동</strong>: '2026-11-23' 전용 워크시트 생성 및 'company' 시트 68개사 A열 TRUE / M열 '3차 정기(11/23)' 세팅 완료<br>
        • <strong>인프라 연동</strong>: 11/20 구축된 Cloudflare Pages(dhsteel.pages.dev) CDN 템플릿(dhsteel_proposal_v2.html) 기반 첫 정기 발송<br>
        • <strong>보고서 발행</strong>: workflow/2026-11-23_dhsteel_mail_plan_batch3.docx 표준 워드 보고서 발행 완료
      </div>
      <ul class="checklist">
        <li class="task-item"><input type="checkbox" id="ph19-target-68" checked><span class="task-text"><strong>[타겟 선별]</strong> 11/09 성공군 + 코베아 오타 정제 68개사 확정</span><input type="date" class="task-date-input" id="ph19-target-68-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-target-68-memo" value="검증 성공군 67건 + 코베아 복구"></li>
        <li class="task-item"><input type="checkbox" id="ph19-sheet-20261123" checked><span class="task-text"><strong>[시트 연동]</strong> '2026-11-23' 워크시트 생성 및 68개사 A열 TRUE / M열 회차 세팅</span><input type="date" class="task-date-input" id="ph19-sheet-20261123-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-sheet-20261123-memo" value="company 시트 68개사 동기화 완료"></li>
        <li class="task-item"><input type="checkbox" id="ph19-report-docx" checked><span class="task-text"><strong>[보고서 발행]</strong> 2026-11-23_dhsteel_mail_plan_batch3.docx 워드 보고서 생성</span><input type="date" class="task-date-input" id="ph19-report-docx-date" value="2026-11-23"><input type="text" class="task-memo-input" id="ph19-report-docx-memo" value="맑은 고딕 10pt 표준 서식 발행"></li>
        <li class="task-item"><input type="checkbox" id="ph19-mail-trigger"><span class="task-text"><strong>[발송 집행]</strong> 구글 시트 상단 메뉴 [대흥 아웃바운드] 원클릭 일괄 발송 집행</span><input type="date" class="task-date-input" id="ph19-mail-trigger-date"><input type="text" class="task-memo-input" id="ph19-mail-trigger-memo" value="Gmail API 3초 간격 일괄 전송 대기"></li>
      </ul>
    </div>
'''

target_marker = '    <!-- PHASE 18 (NEW - 2026-11-20) -->'
if target_marker in text:
    text = text.replace(target_marker, phase19_card + '\n' + target_marker)
    with open(plan_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print('[Success] Phase 19 inserted successfully.')
else:
    print('[Error] Target marker not found.')

