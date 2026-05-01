#!/usr/bin/env python3
"""Build jafner.com static site by injecting partials into source pages."""

import re
import shutil
from pathlib import Path

ROOT    = Path(__file__).parent
SRC     = ROOT / 'src'
COMMON  = ROOT / 'common'
PUBLIC  = ROOT / 'public'

# Partials
nav    = (COMMON / 'nav.html').read_text()
footer = (COMMON / 'footer.html').read_text()

# Clean and recreate public/
if PUBLIC.exists():
    shutil.rmtree(PUBLIC)
PUBLIC.mkdir()

# Static assets that should be copied as-is (not processed)
for asset_dir in ['assets', 'css', 'js', 'images']:
    src_assets = ROOT / asset_dir
    if src_assets.exists():
        shutil.copytree(src_assets, PUBLIC / asset_dir)

# Also copy style.css from root if it lives there
for top_file in ['style.css', 'favicon.ico', 'robots.txt']:
    f = ROOT / top_file
    if f.exists():
        shutil.copy(f, PUBLIC / top_file)

# Build each HTML page
pages_built = 0
for page in SRC.glob('*.html'):
    page_name = page.name

    # Mark the active nav link based on this page's filename
    nav_with_active = re.sub(
        rf'href="/{page_name}"',
        rf'href="/{page_name}" aria-current="page"',
        nav,
    )

    html = (page.read_text()
        .replace('<!--NAV-->', nav_with_active)
        .replace('<!--FOOTER-->', footer))

    (PUBLIC / page_name).write_text(html)
    pages_built += 1
    print(f'  built {page_name}')

print(f'\n✓ {pages_built} pages built into {PUBLIC}/')