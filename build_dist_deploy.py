# -*- coding: utf-8 -*-
import os, sys, shutil

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r'E:\Antigravity\builder-dhsteel-sales'
dist_dir = os.path.join(base_dir, 'dist_deploy')

# Clean existing dist_deploy if exists
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)
    print('[Cleaned] Existing dist_deploy directory.')

os.makedirs(dist_dir, exist_ok=True)

# ==========================================
# 1. Root Web Assets
# ==========================================
root_files = [
    'index.html',
    'index_dashboard.html',
    'app.js',
    'styles.css',
    'manifest.json',
    'google_apps_script_outbound.js'
]

for f in root_files:
    src = os.path.join(base_dir, f)
    dst = os.path.join(dist_dir, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f'[Copied Root] {f}')

# Create Cloudflare Pages _redirects file
redirects_content = """# Cloudflare Pages Redirects / Rewrites
/    /index_dashboard.html    200
/gallery/*    /catalog/gallery/:splat    200
/images/*     /catalog/images/:splat     200
"""
with open(os.path.join(dist_dir, '_redirects'), 'w', encoding='utf-8') as f:
    f.write(redirects_content)
print('[Created] _redirects (/ -> /index_dashboard.html, /gallery/*, /images/* 200)')

# ==========================================
# 2. Catalog Assets
# ==========================================
dist_catalog = os.path.join(dist_dir, 'catalog')
os.makedirs(dist_catalog, exist_ok=True)

catalog_src = os.path.join(base_dir, 'catalog')

catalog_files = [
    'index_catalog.html',
    'index_brochure.html',
    'index_proposal.html',
    'app.js',
    'styles.css',
    'manifest.json',
    'google_apps_script_outbound.js',
    '대흥정밀 B2B 파이프 임가공 제안서_미리보기.html'
]

for f in catalog_files:
    src = os.path.join(catalog_src, f)
    dst = os.path.join(dist_catalog, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f'[Copied Catalog File] {f}')

# Copy media folders in catalog (gallery, images, products, templates)
for folder in ['gallery', 'images', 'products', 'templates']:
    src_f = os.path.join(catalog_src, folder)
    dst_f = os.path.join(dist_catalog, folder)
    if os.path.exists(src_f):
        shutil.copytree(src_f, dst_f)
        print(f'[Copied Catalog Folder] {folder}/')
        # Also mirror gallery and images to root for legacy email template compatibility
        if folder in ['gallery', 'images']:
            dst_root_f = os.path.join(dist_dir, folder)
            shutil.copytree(src_f, dst_root_f)
            print(f'[Mirrored to Root] {folder}/')

# ==========================================
# 2-1. Root Assets (Logos & Fonts)
# ==========================================
dist_assets = os.path.join(dist_dir, 'assets')
os.makedirs(dist_assets, exist_ok=True)
assets_src = os.path.join(base_dir, 'assets')
if os.path.exists(assets_src):
    for f in os.listdir(assets_src):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.webp', '.txt')):
            shutil.copy2(os.path.join(assets_src, f), os.path.join(dist_assets, f))
            print(f'[Copied Root Asset] assets/{f}')

# ==========================================
# 3. Plan & Reports Web Pages
# ==========================================
# plan
dist_plan = os.path.join(dist_dir, 'plan')
os.makedirs(dist_plan, exist_ok=True)
shutil.copy2(os.path.join(base_dir, 'plan', 'dhsteel_plan_2026.html'), os.path.join(dist_plan, 'dhsteel_plan_2026.html'))
print('[Copied Plan] dhsteel_plan_2026.html')

# fax
dist_fax = os.path.join(dist_dir, 'fax')
os.makedirs(dist_fax, exist_ok=True)
shutil.copy2(os.path.join(base_dir, 'fax', 'fax_report.html'), os.path.join(dist_fax, 'fax_report.html'))
print('[Copied Fax Report] fax_report.html')

# mailling
dist_mail = os.path.join(dist_dir, 'mailling')
os.makedirs(dist_mail, exist_ok=True)
shutil.copy2(os.path.join(base_dir, 'mailling', 'mail_report.html'), os.path.join(dist_mail, 'mail_report.html'))
print('[Copied Mail Report] mail_report.html')

# workflow (작업 요약 HTML 보고서만 복사: docx/pptx/pdf/스크립트 등 내부 파일은 제외)
import glob
src_workflow = os.path.join(base_dir, 'workflow')
dist_workflow = os.path.join(dist_dir, 'workflow')
workflow_reports = sorted(glob.glob(os.path.join(src_workflow, '*_claude_dashboard_work_summary.html')))
if workflow_reports:
    os.makedirs(dist_workflow, exist_ok=True)
    for rp in workflow_reports:
        shutil.copy2(rp, os.path.join(dist_workflow, os.path.basename(rp)))
        print(f'[Copied Workflow Report] {os.path.basename(rp)}')
else:
    print('[Skipped] workflow reports not found')

# ==========================================
# 4. Measure Size
# ==========================================
total_size = 0
file_count = 0
for root, dirs, files in os.walk(dist_dir):
    for f in files:
        fp = os.path.join(root, f)
        total_size += os.path.getsize(fp)
        file_count += 1

print(f'\n==========================================')
print(f'✅ dist_deploy Build Complete!')
print(f'Total Files: {file_count}')
print(f'Total Size: {total_size / (1024*1024):.2f} MB')
print(f'==========================================')

