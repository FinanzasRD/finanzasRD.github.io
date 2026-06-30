#!/usr/bin/env python3
"""Fix all articles in finanzasrd project."""
import os
import re
import glob

BLOG_DIR = r"C:\Users\winde\Desktop\finanzasrd\blog"
ROOT_DIR = r"C:\Users\winde\Desktop\finanzasrd"

# Correct icon line (from index.html)
CORRECT_ICON = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>\U0001F4B0</text></svg>">'
CORRECT_APPLE = '<link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>\U0001F4B0</text></svg>">'

# New author bio (Carlos)
NEW_BIO = '''        <a href="../autores/carlos-mendez.html" class="author-bio" style="display:flex;text-decoration:none;cursor:pointer;gap:1rem;align-items:start;background:var(--primary-light);border-radius:var(--radius-sm);padding:1.25rem;margin:2rem 0;border:1px solid rgba(10,92,54,0.12)">
          <div class="author-bio__avatar" style="font-size:2.5rem;flex-shrink:0;width:56px;height:56px;display:flex;align-items:center;justify-content:center;border-radius:50%;overflow:hidden;background:var(--white)">
            <img src="../images/author-carlos.jpg" alt="" style="width:100%;height:100%;object-fit:cover" onerror="this.style.display=\'none\';this.parentElement.textContent=\'\U0001F468\u200D\U0001F4BC\'">
          </div>
          <div class="author-bio__info" style="flex:1">
            <strong style="display:block;color:var(--dark);font-size:.95rem">Carlos Miguel Echavarr\u00eda Rodr\u00edguez</strong>
            <span style="display:block;color:var(--primary-dark);font-size:.8rem;font-weight:600;margin-bottom:.5rem">Fundador & Editor Principal de FinanzasRD</span>
            <p style="font-size:.85rem;color:var(--text-light);margin:0;line-height:1.6">Ingeniero en Sistemas Computacionales (UTESA) apasionado por la educaci\u00f3n financiera. Creador de FinanzasRD. Combino mi formaci\u00f3n tecnol\u00f3gica con el an\u00e1lisis financiero para ayudarte a tomar mejores decisiones con tu dinero.</p>
          </div>
          <span style="color:var(--primary-dark);font-weight:600;font-size:.8rem;white-space:nowrap;align-self:center">Ver perfil \u2192</span>
        </a>'''

def fix_file(filepath):
    """Fix a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changed = False
    
    # 1. Fix broken icon links
    # Pattern 1: broken icon link (line missing the <text...></svg>"> part)
    broken_pat1 = re.compile(
        r'<link rel="icon" href="data:image/svg\+xml,<svg xmlns=\'http://www\.w3\.org/2000/svg\' viewBox=\'0 0 100 100\'>\s*$',
        re.MULTILINE
    )
    if broken_pat1.search(content):
        content = broken_pat1.sub(CORRECT_ICON, content)
        changed = True
    
    # Pattern 2: broken apple-touch-icon link (with duplicate trailing garbage)
    broken_pat2 = re.compile(
        r'<link rel="apple-touch-icon" href="data:image/svg\+xml,<svg xmlns=\'http://www\.w3\.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'\.9em\' font-size=\'90\'>[^<]*</text></svg>"><text y=\'\.9em\' font-size=\'90\'>[^<]*</text></svg>">',
    )
    if broken_pat2.search(content):
        content = broken_pat2.sub(CORRECT_APPLE, content)
        changed = True
    
    # Also handle correct-but-possibly-corrupted apple-touch-icon links
    # Pattern: Some articles might have the right icon but corrupted apple-touch-icon
    # with weird emoji encoding (like dY' or ??)
    corrupted_icon = re.compile(
        r'<link rel="(?:icon|apple-touch-icon)" href="data:image/svg\+xml,<svg xmlns=\'http://www\.w3\.org/2000/svg\' viewBox=\'0 0 100 100\'>[^<]*</svg>">'
    )
    # Just verify both icon links exist and are closed properly
    
    # 2. Replace old author bio
    # Old pattern matches "Ver perfil completo" style
    old_bio_pattern = re.compile(
        r'<a href="\.\./autores/carlos-mendez\.html" class="author-bio"[^>]*>.*?Ver perfil completo.*?</a>',
        re.DOTALL
    )
    if old_bio_pattern.search(content):
        content = old_bio_pattern.sub(NEW_BIO, content)
        changed = True
    
    # Also fix corrupted new bio (with mangled Unicode from bad encoding)
    # Pattern: new bio with corrupted text like Echavarr\u00c3\u00ada instead of Echavarr\u00eda
    corrupted_bio = re.compile(
        r'<a href="\.\./autores/carlos-mendez\.html" class="author-bio"[^>]*>.*?Ver perfil.*?</a>',
        re.DOTALL
    )
    if corrupted_bio.search(content):
        # If the bio has corrupted Unicode but is in new format, replace it
        match = corrupted_bio.search(content)
        if match and ('Ã' in match.group() or 'ðŸ' in match.group()):
            content = corrupted_bio.sub(NEW_BIO, content)
            changed = True
    
    # 3. Fix double-accent encoding (e.g., "úú" -> "ú")
    if '\u00fa\u00fa' in content:
        content = content.replace('\u00fa\u00fa', '\u00fa')
        changed = True
    
    # 4. Fix other encoding artifacts
    fixes = {
        '\u00c3': '\u00c3',  # Placeholder - need to check actual patterns
    }
    
    # Fix "c?mo" or similar
    content = content.replace('\ufffd', '')  # Remove replacement characters
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return changed

def main():
    # Collect all HTML files
    files = []
    for d in [BLOG_DIR, ROOT_DIR]:
        for f in glob.glob(os.path.join(d, '*.html')):
            name = os.path.basename(f)
            if name == 'template.html':
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
    
    print(f"\nArchivos modificados: {fixed}")

if __name__ == '__main__':
    main()
