# -*- coding: utf-8 -*-
"""
fix_logo_and_plan_width.py
1. index_dashboard.html: 사이드바 로고를 공식 심볼 로고(assets/logo_dhsteel.png)로 교체
2. plan/dhsteel_plan_2026.html: tab-manual을 .container 안으로 이동시켜 가로 폭(1280px) 일치
"""

import sys, re

sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────────────────────────────────────────
# 1. index_dashboard.html 로고 교체
# ─────────────────────────────────────────────────────────────
dash_path = 'index_dashboard.html'
with open(dash_path, 'r', encoding='utf-8') as f:
    dash_html = f.read()

old_logo_pattern = """        <div class="logo">
            <div class="logo-mark">DH</div>
            <div class="logo-name">대흥정밀</div>
            <div class="logo-sub">DAEHEUNG PRECISION</div>
        </div>"""

new_logo_markup = """        <div class="logo">
            <div style="width:48px; height:48px; margin:0 auto 8px; border-radius:10px; overflow:hidden; background:#FFFFFF; padding:4px; display:flex; align-items:center; justify-content:center; box-shadow:0 3px 8px rgba(0,0,0,0.18);">
                <img src="assets/logo_dhsteel.png" alt="대흥정밀" style="width:100%; height:100%; object-fit:contain;">
            </div>
            <div class="logo-name">대흥정밀</div>
            <div class="logo-sub">DAEHEUNG PRECISION</div>
        </div>"""

if old_logo_pattern in dash_html:
    dash_html = dash_html.replace(old_logo_pattern, new_logo_markup)
    with open(dash_path, 'w', encoding='utf-8') as f:
        f.write(dash_html)
    print('[성공] index_dashboard.html 로고 이미지 교체 완료.')
else:
    print('[경고] index_dashboard.html에서 old_logo_pattern을 찾지 못했습니다.')

# ─────────────────────────────────────────────────────────────
# 2. plan/dhsteel_plan_2026.html 가로 폭 수정 (.container 안으로 tab-manual 이동)
# ─────────────────────────────────────────────────────────────
plan_path = 'plan/dhsteel_plan_2026.html'
with open(plan_path, 'r', encoding='utf-8') as f:
    plan_html = f.read()

# 현재 구조:
# </div>\n\n</div>\n\n<!-- Tab Switching Script -->\n\n  <!-- ===...\n  <!-- TAB 6: ...\n  <div id="tab-manual" ... </div>
# 이를 tab-manual이 </div> (container 닫기) 바로 앞에 오도록 수정

pattern_to_fix = """    </div>

  </div>

</div>

<!-- Tab Switching Script -->

  <!-- ============================================================== -->
  <!-- TAB 6: B2B 주간 발송 실무 매뉴얼 (메일·반송스캔·팩스) -->
  <!-- ============================================================== -->
  <div id="tab-manual" class="plan-tab-pane">"""

corrected_structure = """    </div>

  </div>

  <!-- ============================================================== -->
  <!-- TAB 6: B2B 주간 발송 실무 매뉴얼 (메일·반송스캔·팩스) -->
  <!-- ============================================================== -->
  <div id="tab-manual" class="plan-tab-pane">"""

# tab-manual의 닫는 </div> 뒤에 .container 닫는 </div>가 오도록 정리
# tab-manual의 끝 부분을 찾아서 </div> 추가
if pattern_to_fix in plan_html:
    plan_html = plan_html.replace(pattern_to_fix, corrected_structure)
    # 이제 tab-manual 끝난 뒤에 </script> 앞에 container 닫는 </div>가 필요
    # Find end of tab-manual: </div>\n\n<script> 또는 </div>\n<script>
    # tab-manual contains </div> at the end. We need container closing </div> after it!
    # Let's inspect where <script> starts
    idx_script = plan_html.rfind('<script>')
    # Before <script>, let's ensure there is </div> (for container)
    # Let's see what's right before <script>
    text_before_script = plan_html[:idx_script].rstrip()
    if not text_before_script.endswith('</div>'):
        # add </div>
        plan_html = text_before_script + '\n\n</div>\n\n' + plan_html[idx_script:]
    else:
        # Check if there are 2 </div>s: one for tab-manual, one for container
        # Since pattern_to_fix removed one </div> from before tab-manual, we must add one </div> after tab-manual!
        plan_html = text_before_script + '\n\n</div>\n\n' + plan_html[idx_script:]
        
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(plan_html)
    print('[성공] plan/dhsteel_plan_2026.html tab-manual을 .container 내부로 이동 완료.')
else:
    print('[경고] plan/dhsteel_plan_2026.html에서 pattern_to_fix를 찾지 못했습니다.')


