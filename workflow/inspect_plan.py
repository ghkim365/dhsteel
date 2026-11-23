import re

with open('plan/dhsteel_plan_2026.html', 'r', encoding='utf-8') as f:
    plan = f.read()

print('Plan size:', len(plan), 'bytes')
tabs = re.findall(r'<button class="tab-btn[^"]*"[^>]*>([^<]+)</button>', plan)
print('Tabs found:', tabs)

# Search for November or 2026-11-23 entries
idx = plan.find('2026-11-23')
print('2026-11-23 found at index:', idx)
if idx != -1:
    print(plan[idx:idx+400])

