#!/usr/bin/env python3
"""Robustly fix icon links, author bios, and encoding in all HTML files."""
import os
import glob
import re

import sys

BLOG_DIR = r"C:\Users\winde\Desktop\finanzasrd\blog"
ROOT_DIR = r"C:\Users\winde\Desktop\finanzasrd"

CORRECT_ICON_NORMAL = '  <link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>\U0001F4B0</text></svg>">'
CORRECT_APPLE_NORMAL = '  <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>\U0001F4B0</text></svg>">'

NEW_BIO = re.compile(
    r'<a href="\.\./autores/carlos-mendez\.html" class="author-bio"[^>]*>.*?Ver perfil (completo|\u2192).*?</a>',
    re.DOTALL
)
NEW_BIO_REPLACEMENT = (
    '        <a href="../autores/carlos-mendez.html" class="author-bio" '
    'style="display:flex;text-decoration:none;cursor:pointer;gap:1rem;'
    'align-items:start;background:var(--primary-light);border-radius:'
    'var(--radius-sm);padding:1.25rem;margin:2rem 0;border:1px solid '
    'rgba(10,92,54,0.12)">\n'
    '          <div class="author-bio__avatar" style="font-size:2.5rem;'
    'flex-shrink:0;width:56px;height:56px;display:flex;align-items:center;'
    'justify-content:center;border-radius:50%;overflow:hidden;'
    'background:var(--white)">\n'
    '            <img src="../images/author-carlos.jpg" alt="" '
    'style="width:100%;height:100%;object-fit:cover" onerror='
    '"this.style.display=\'none\';this.parentElement.textContent='
    '\'\U0001F468\u200D\U0001F4BC\'">\n'
    '          </div>\n'
    '          <div class="author-bio__info" style="flex:1">\n'
    '            <strong style="display:block;color:var(--dark);'
    'font-size:.95rem">Carlos Miguel Echavarr\u00eda Rodr\u00edguez'
    '</strong>\n'
    '            <span style="display:block;color:var(--primary-dark);'
    'font-size:.8rem;font-weight:600;margin-bottom:.5rem">'
    'Fundador & Editor Principal de FinanzasRD</span>\n'
    '            <p style="font-size:.85rem;color:var(--text-light);'
    'margin:0;line-height:1.6">Ingeniero en Sistemas Computacionales '
    '(UTESA) apasionado por la educaci\u00f3n financiera. Creador de '
    'FinanzasRD. Combino mi formaci\u00f3n tecnol\u00f3gica con el '
    'an\u00e1lisis financiero para ayudarte a tomar mejores decisiones '
    'con tu dinero.</p>\n'
    '          </div>\n'
    '          <span style="color:var(--primary-dark);font-weight:600;'
    'font-size:.8rem;white-space:nowrap;align-self:center">'
    'Ver perfil \u2192</span>\n'
    '        </a>'
)

def fix_file(filepath):
    with open(filepath, 'rb') as f:
        raw = f.read()
    
    modified_raw = raw
    changed = False
    
    # --- Fix icon links using raw byte patterns ---
    # The correct emoji in UTF-8 is: \xf0\x9f\x92\xb0
    
    # Fix line 1: icon link that's truncated (no closing </text></svg>")
    # Pattern: starts with icon href, has SVG opening but is cut off
    icon_prefix = b'  <link rel="icon" href="data:image/svg+xml,<svg'
    icon_correct_bytes = (
        b'  <link rel="icon" href="data:image/svg+xml,'
        b'<svg xmlns=\'http://www.w3.org/2000/svg\' '
        b'viewBox=\'0 0 100 100\'><text y=\'.9em\' '
        b'font-size=\'90\'>\xf0\x9f\x92\xb0</text></svg>">'
    )
    
    idx = modified_raw.find(icon_prefix)
    if idx >= 0:
        # Find the end of this line
        line_end = modified_raw.find(b'\n', idx)
        if line_end >= 0:
            line_content = modified_raw[idx:line_end].rstrip(b'\r')
            # Check if this line is missing the closing </text></svg>">
            if not line_content.endswith(b'</text></svg>">'):
                # Check if there's already a correct icon line after
                rest = modified_raw[idx+len(icon_correct_bytes):idx+len(icon_correct_bytes)+50]
                # Replace just this line
                modified_raw = modified_raw[:idx] + icon_correct_bytes + modified_raw[line_end:]
                changed = True
    
    # Fix line 2: apple-touch-icon with trailing garbage
    apple_prefix = b'  <link rel="apple-touch-icon" href="data:image/svg+xml,<svg'
    apple_correct_bytes = (
        b'  <link rel="apple-touch-icon" href="data:image/svg+xml,'
        b'<svg xmlns=\'http://www.w3.org/2000/svg\' '
        b'viewBox=\'0 0 100 100\'><text y=\'.9em\' '
        b'font-size=\'90\'>\xf0\x9f\x92\xb0</text></svg>">'
    )
    
    idx2 = modified_raw.find(apple_prefix)
    if idx2 >= 0:
        line_end2 = modified_raw.find(b'\n', idx2)
        if line_end2 >= 0:
            line_content2 = modified_raw[idx2:line_end2].rstrip(b'\r')
            # Check if this line has trailing garbage (extra <text... after closing)
            if line_content2.count(b'</text>') > 1:
                modified_raw = modified_raw[:idx2] + apple_correct_bytes + modified_raw[line_end2:]
                changed = True
    
    # --- Fix author bios ---
    text = modified_raw.decode('utf-8', errors='replace')
    orig_text = text
    old_bio = re.search(
        r'<a href="\.\./autores/carlos-mendez\.html" class="author-bio"[^>]*>.*?Ver perfil completo.*?</a>',
        text
    )
    if old_bio:
        text = text.replace(old_bio.group(), NEW_BIO_REPLACEMENT)
        changed = True
    
    # --- Fix double accents ---
    if '\u00fa\u00fa' in text:
        text = text.replace('\u00fa\u00fa', '\u00fa')
        changed = True
    
    if changed:
        modified_raw = text.encode('utf-8')
        with open(filepath, 'wb') as f:
            f.write(modified_raw)
    
    return changed

def main():
    files = []
    for d in [BLOG_DIR, ROOT_DIR]:
        for f in glob.glob(os.path.join(d, '*.html')):
            name = os.path.basename(f)
            if name in ('template.html', 'check_bytes.py', 'fix_all.py', 'fix-all.py', 'fix-all.ps1', 'update-articles.ps1'):
                continue
            files.append(f)
    
    fixed = 0
    for f in sorted(files):
        try:
            if fix_file(f):
                print(f"  FIXED: {os.path.basename(f)}")
                fixed += 1
        except Exception as e:
            print(f"  ERROR: {os.path.basename(f)}: {e}")
    
    print(f"\nTotal archivos modificados: {fixed}")

if __name__ == '__main__':
    main()
