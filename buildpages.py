# build.py
from pathlib import Path
import re

nav = Path('common/nav.html').read_text()
footer = Path('common/footer.html').read_text()

src, out = Path('src'), Path('public')
out.mkdir(exist_ok=True)

for page in src.glob('*.html'):
    page_name = page.name
    nav_with_active = re.sub(
        rf'href="/{page_name}"',
        rf'href="/{page_name}" aria-current="page"',
        nav
    )
    
    html = (page.read_text()
        .replace('<!--NAV-->', nav_with_active)
        .replace('<!--FOOTER-->', footer))
    (out / page.name).write_text(html)
    print(f'built {page.name}')