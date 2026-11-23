with open(r'e:\Antigravity\builder-dhsteel-sales\workflow\mail_style.css', 'r', encoding='utf-8') as f:
    style = f.read()

import re
# check variables
vars_m = re.search(r':root\s*{(.*?)}', style, re.DOTALL)
if vars_m:
    print("--- mail CSS variables ---")
    print(vars_m.group(1).strip()[:400])

# check font family occurrences
fonts = re.findall(r'font-family:[^;]+;', style)
print("\nUnique fonts in mail_style:")
print(set(fonts))

# check font weight occurrences
weights = re.findall(r'font-weight:\s*([0-9]+);', style)
from collections import Counter
print("\nFont weights distribution in mail_style:")
print(Counter(weights))
