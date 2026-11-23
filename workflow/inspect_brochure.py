import re

with open(r'E:/Antigravity/builder-samhyup-sales/catalog/index_brochure.html', 'r', encoding='utf-8') as f:
    text = f.read()

pages = re.findall(r'<main[^>]*id="([^"]+)"', text)
print('Page IDs:', pages)

# Print headings
h1_tags = re.findall(r'<h[1-3][^>]*>(.*?)</h[1-3]>', text, re.DOTALL)
print('\nSample headings:')
for h in h1_tags[:15]:
    cleaned = re.sub(r'<[^>]+>', '', h).strip()
    if cleaned:
        print(' -', cleaned[:60])

