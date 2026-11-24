# -*- coding: utf-8 -*-
import json
import os
import glob
import re

claude_dir = r'C:\Users\fix\.claude\projects\E--Antigravity-builder-dhsteel-sales'
antigravity_log = r'C:\Users\fix\.gemini\antigravity\brain\a8b9ce34-a5a8-4628-ac92-d67ec7909777\.system_generated\logs\transcript.jsonl'

out_plan_dir = r'E:\Antigravity\builder-dhsteel-sales\plan'
os.makedirs(out_plan_dir, exist_ok=True)

# ==============================================================================
# 1. Claude Code Chat History Export
# ==============================================================================
claude_files = glob.glob(os.path.join(claude_dir, '*.jsonl'))
claude_dialogs = []

for cp in claude_files:
    with open(cp, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
                t = d.get('type')
                ts = d.get('timestamp', '')[:19].replace('T', ' ')
                
                if t == 'user':
                    msg = d.get('message', {})
                    content = msg.get('content', '')
                    if isinstance(content, list):
                        texts = []
                        for c in content:
                            if isinstance(c, dict) and c.get('type') == 'text':
                                texts.append(c.get('text', ''))
                            elif isinstance(c, str):
                                texts.append(c)
                        content = '\n'.join(texts)
                    if content and content.strip():
                        # filter internal command if needed
                        claude_dialogs.append(('User (사용자)', ts, content.strip()))
                        
                elif t == 'assistant':
                    msg = d.get('message', {})
                    content = msg.get('content', '')
                    if isinstance(content, list):
                        texts = []
                        for c in content:
                            if isinstance(c, dict):
                                if c.get('type') == 'text':
                                    texts.append(c.get('text', ''))
                            elif isinstance(c, str):
                                texts.append(c)
                        content = '\n\n'.join(texts)
                    if content and content.strip():
                        claude_dialogs.append(('Claude Code (Sonnet 3.7)', ts, content.strip()))
            except Exception as e:
                pass

# Sort by timestamp
claude_dialogs.sort(key=lambda x: x[1])

# Remove consecutive duplicates if any
dedup_claude = []
for item in claude_dialogs:
    if not dedup_claude or dedup_claude[-1][0] != item[0] or dedup_claude[-1][2] != item[2]:
        dedup_claude.append(item)

print(f"Extracted {len(dedup_claude)} messages from Claude Code sessions.")

# Write Claude Code Markdown
claude_md_path = os.path.join(out_plan_dir, 'claude_chat_history_20261124.md')
with open(claude_md_path, 'w', encoding='utf-8') as f:
    f.write("# 💬 Claude Code 대화 내역 (2026-11-24)\n\n")
    f.write("> **프로젝트:** `E:\\Antigravity\\builder-dhsteel-sales`  \n")
    f.write("> **환경:** Claude Code CLI (Pro)  \n")
    f.write(f"> **총 대화 턴 수:** {len(dedup_claude)}회  \n\n")
    f.write("---\n\n")
    for speaker, ts, content in dedup_claude:
        icon = '👤' if 'User' in speaker else '🤖'
        f.write(f"### {icon} {speaker} `[{ts}]`\n\n")
        f.write(f"{content}\n\n")
        f.write("---\n\n")

# Write Claude Code HTML
def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

claude_html_path = os.path.join(out_plan_dir, 'claude_chat_history_20261124.html')
claude_body = []
for speaker, ts, content in dedup_claude:
    is_user = 'User' in speaker
    msg_class = 'msg-user' if is_user else 'msg-claude'
    author_color = '#0058be' if is_user else '#b45309'
    icon = '👤' if is_user else '🤖'
    esc_content = escape_html(content)
    
    claude_body.append(f"""  <div class="msg {msg_class}">
    <div class="author" style="color: {author_color};">
      <span>{icon} {speaker}</span>
      <span class="time">{ts}</span>
    </div>
    <div class="content">{esc_content}</div>
  </div>""")

claude_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>Claude Code 대화 기록 (2026-11-24) - 대흥정밀</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', 'Malgun Gothic', sans-serif;
      line-height: 1.65;
      color: #1e293b;
      max-width: 900px;
      margin: 40px auto;
      padding: 0 20px;
      background: #f8fafc;
    }}
    .header {{
      background: #ffffff;
      padding: 24px 30px;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
      margin-bottom: 24px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    .msg {{
      margin-bottom: 20px;
      padding: 20px 24px;
      border-radius: 12px;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }}
    .msg-user {{
      background: #f0f7ff;
      border-left: 5px solid #0058be;
    }}
    .msg-claude {{
      background: #ffffff;
      border-left: 5px solid #d97706;
    }}
    .author {{
      font-weight: 700;
      font-size: 15px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .time {{
      font-size: 12px;
      color: #94a3b8;
      font-weight: 400;
    }}
    .content {{
      font-size: 14.5px;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    pre, code {{
      background: #0f172a;
      color: #f8fafc;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: Consolas, monospace;
      font-size: 13px;
    }}
    pre {{
      padding: 12px 16px;
      overflow-x: auto;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1 style="margin: 0 0 10px; font-size: 22px;">💬 Claude Code 대화 내역 (2026-11-24)</h1>
    <div style="font-size: 13.5px; color: #64748b;">
      프로젝트: <code>E:\\Antigravity\\builder-dhsteel-sales</code> | 대화 수: {len(dedup_claude)}개
    </div>
    <p style="margin: 12px 0 0; font-size: 13px; color: #0058be; font-weight: 600;">
      💡 이 페이지를 브라우저에서 열고 <code>Ctrl+A</code>(전체 선택) ➔ <code>Ctrl+C</code>(복사) 후 구글 독스에 <code>Ctrl+V</code>(붙여넣기)하시면 서식이 깔끔하게 그대로 들어갑니다.
    </p>
  </div>

{chr(10).join(claude_body)}

</body>
</html>
"""

with open(claude_html_path, 'w', encoding='utf-8') as f:
    f.write(claude_html)

print(f"Generated Claude Code files: {claude_md_path}, {claude_html_path}")


# ==============================================================================
# 2. Antigravity Chat History Export
# ==============================================================================
antigravity_dialogs = []

with open(antigravity_log, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            d = json.loads(line)
            source = d.get('source', '')
            msg_type = d.get('type', '')
            ts = d.get('created_at', '')[:19].replace('T', ' ')
            
            # User messages
            if source == 'USER' or msg_type == 'USER_REQUEST':
                content = d.get('content', '')
                if content:
                    # Clean out injected system blocks if present
                    if content.startswith('<CONTEXT_SUMMARY>'):
                        # find user actual message after context summary
                        parts = content.split('</CONTEXT_SUMMARY>')
                        if len(parts) > 1:
                            content = parts[-1].strip()
                        else:
                            continue
                    if content.startswith('<USER_REQUEST>'):
                        parts = content.split('</USER_REQUEST>')
                        content = parts[0].replace('<USER_REQUEST>', '').strip()
                    if content and not content.startswith('<SYSTEM_MESSAGE>'):
                        antigravity_dialogs.append(('User (사용자)', ts, content.strip()))
            
            # Assistant turns
            elif source == 'MODEL' and msg_type in ['PLANNER_RESPONSE', 'TURN_COMPLETE']:
                content = d.get('content', '')
                if not content and 'tool_calls' in d:
                    continue
                if content and content.strip():
                    if not antigravity_dialogs or antigravity_dialogs[-1][2] != content.strip():
                        antigravity_dialogs.append(('Antigravity (Gemini)', ts, content.strip()))
        except Exception as e:
            pass

# Deduplicate
dedup_anti = []
for item in antigravity_dialogs:
    if not dedup_anti or dedup_anti[-1][0] != item[0] or dedup_anti[-1][2] != item[2]:
        dedup_anti.append(item)

print(f"Extracted {len(dedup_anti)} chat turns from Antigravity session.")

# Write Antigravity Markdown
anti_md_path = os.path.join(out_plan_dir, 'antigravity_chat_history_20261124.md')
with open(anti_md_path, 'w', encoding='utf-8') as f:
    f.write("# 🌐 Antigravity 대화 내역 (2026-11-24)\n\n")
    f.write("> **프로젝트:** `E:\\Antigravity\\builder-dhsteel-sales`  \n")
    f.write("> **플랫폼:** Google DeepMind Antigravity  \n")
    f.write(f"> **세션 ID:** `a8b9ce34-a5a8-4628-ac92-d67ec7909777`  \n")
    f.write(f"> **총 대화 턴 수:** {len(dedup_anti)}회  \n\n")
    f.write("---\n\n")
    for speaker, ts, content in dedup_anti:
        icon = '👤' if 'User' in speaker else '🌐'
        f.write(f"### {icon} {speaker} `[{ts}]`\n\n")
        f.write(f"{content}\n\n")
        f.write("---\n\n")

# Write Antigravity HTML
anti_html_path = os.path.join(out_plan_dir, 'antigravity_chat_history_20261124.html')
anti_body = []
for speaker, ts, content in dedup_anti:
    is_user = 'User' in speaker
    msg_class = 'msg-user' if is_user else 'msg-ai'
    author_color = '#0058be' if is_user else '#16a34a'
    icon = '👤' if is_user else '🌐'
    esc_content = escape_html(content)
    
    anti_body.append(f"""  <div class="msg {msg_class}">
    <div class="author" style="color: {author_color};">
      <span>{icon} {speaker}</span>
      <span class="time">{ts}</span>
    </div>
    <div class="content">{esc_content}</div>
  </div>""")

anti_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>Antigravity 대화 기록 (2026-11-24) - 대흥정밀</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', 'Malgun Gothic', sans-serif;
      line-height: 1.65;
      color: #1e293b;
      max-width: 900px;
      margin: 40px auto;
      padding: 0 20px;
      background: #f8fafc;
    }}
    .header {{
      background: #ffffff;
      padding: 24px 30px;
      border-radius: 12px;
      border: 1px solid #e2e8f0;
      margin-bottom: 24px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    .msg {{
      margin-bottom: 20px;
      padding: 20px 24px;
      border-radius: 12px;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }}
    .msg-user {{
      background: #f0f7ff;
      border-left: 5px solid #0058be;
    }}
    .msg-ai {{
      background: #ffffff;
      border-left: 5px solid #16a34a;
    }}
    .author {{
      font-weight: 700;
      font-size: 15px;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .time {{
      font-size: 12px;
      color: #94a3b8;
      font-weight: 400;
    }}
    .content {{
      font-size: 14.5px;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    pre, code {{
      background: #0f172a;
      color: #f8fafc;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: Consolas, monospace;
      font-size: 13px;
    }}
    pre {{
      padding: 12px 16px;
      overflow-x: auto;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1 style="margin: 0 0 10px; font-size: 22px;">🌐 Antigravity 대화 내역 (2026-11-24)</h1>
    <div style="font-size: 13.5px; color: #64748b;">
      프로젝트: <code>E:\\Antigravity\\builder-dhsteel-sales</code> | 대화 수: {len(dedup_anti)}개
    </div>
    <p style="margin: 12px 0 0; font-size: 13.5px; color: #0058be; font-weight: 600;">
      💡 이 페이지를 브라우저에서 열고 <code>Ctrl+A</code>(전체 선택) ➔ <code>Ctrl+C</code>(복사) 후 구글 독스에 <code>Ctrl+V</code>(붙여넣기)하시면 표와 색상 서식이 깨지지 않고 완벽하게 들어갑니다!
    </p>
  </div>

{chr(10).join(anti_body)}

</body>
</html>
"""

with open(anti_html_path, 'w', encoding='utf-8') as f:
    f.write(anti_html)

print(f"Generated Antigravity files: {anti_md_path}, {anti_html_path}")
