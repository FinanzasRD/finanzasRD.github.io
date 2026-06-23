#!/usr/bin/env python3
"""Add search bar to all blog articles and key pages."""
import os
import glob

BLOG_DIR = r"C:\Users\winde\Desktop\finanzasrd\blog"
ROOT_DIR = r"C:\Users\winde\Desktop\finanzasrd"

SEARCH_FORM = '''        <form class="header__search" role="search" action="https://www.google.com/search" method="GET" target="_blank">
          <input type="hidden" name="as_sitesearch" value="finanzasrd.github.io">
          <input type="search" name="q" class="header__search-input" placeholder="Buscar en FinanzasRD..." aria-label="Buscar en el sitio">
        </form>
      </nav>'''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'header__search' in content:
        return False
    old = '</ul>\n      </nav>'
    new = '</ul>\n' + SEARCH_FORM
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

count = 0
for html in glob.glob(os.path.join(BLOG_DIR, '*.html')):
    if fix_file(html):
        print(f"  + {os.path.basename(html)}")
        count += 1

key_pages = ['about.html', 'privacidad.html', 'terminos.html', 'cookies.html',
             'descargo.html', 'nuestra-metodologia.html', '404.html',
             'autores/carlos-mendez.html', 'autores/maria-rodriguez.html', 'autores/roberto-pena.html']
for page in key_pages:
    path = os.path.join(ROOT_DIR, page)
    if os.path.exists(path):
        if fix_file(path):
            print(f"  + {page}")
            count += 1

print(f"\nUpdated {count} files with search bar.")
