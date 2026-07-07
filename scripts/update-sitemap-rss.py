#!/usr/bin/env python3
"""Update sitemap.xml and rss.xml from blog articles."""
import os, re, glob, html
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT, 'blog')
SITEMAP = os.path.join(ROOT, 'sitemap.xml')
RSS = os.path.join(ROOT, 'rss.xml')
SITE = 'https://finanzasrd.github.io'

MONTHS_ES = {
    '01':'enero','02':'febrero','03':'marzo','04':'abril','05':'mayo','06':'junio',
    '07':'julio','08':'agosto','09':'septiembre','10':'octubre','11':'noviembre','12':'diciembre'
}

MONTHS_EN = {
    '01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
    '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'
}

def extract_meta(html_text, pattern):
    m = re.search(pattern, html_text)
    return m.group(1).strip() if m else ''

def extract_title(html_text):
    m = re.search(r'<title>(.*?)\s*-\s*FinanzasRD</title>', html_text)
    return m.group(1).strip() if m else ''

def extract_description(html_text):
    return extract_meta(html_text, r'<meta\s+name="description"\s+content="([^"]*)"')

def extract_date(html_text):
    raw = extract_meta(html_text, r'<meta\s+property="article:published_time"\s+content="([^"]*)"')
    if raw:
        return raw[:10]
    return '2026-01-01'

def extract_category(html_text):
    return extract_meta(html_text, r'<meta\s+property="article:tag"\s+content="([^"]*)"')

def format_rss_date(date_str):
    if len(date_str) == 10:
        y, m, d = date_str.split('-')
        return f"{MONTHS_EN.get(m, 'Jan')} {int(d):02d} {y} 10:00:00 GMT"
    return 'Mon, 01 Jan 2026 10:00:00 GMT'

def format_date_human(date_str):
    if len(date_str) == 10:
        y, m, d = date_str.split('-')
        return f"{int(d)} de {MONTHS_ES.get(m, 'mes')} de {y}"
    return date_str

def get_read_time(html_text):
    content = re.sub(r'<[^>]+>', '', html_text)
    words = len(content.split())
    minutes = max(1, round(words / 200))
    return str(minutes)

def collect_articles():
    articles = []
    for fpath in sorted(glob.glob(os.path.join(BLOG_DIR, '*.html'))):
        name = os.path.basename(fpath)
        if name == 'template.html':
            continue
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        filename = name.replace('.html', '')
        url = f"{SITE}/blog/{name}"
        title = extract_title(content) or filename.replace('-', ' ').title()
        desc = extract_description(content) or title
        date = extract_date(content)
        cat = extract_category(content) or 'General'
        read_time = get_read_time(content)
        date_human = format_date_human(date)
        rss_date = format_rss_date(date)
        articles.append({
            'filename': filename,
            'url': url,
            'title': title,
            'description': desc,
            'date': date,
            'date_human': date_human,
            'rss_date': rss_date,
            'category': cat,
            'read_time': read_time,
            'content': content,
        })
    return articles

def generate_sitemap(articles, static_pages):
    static = [
        ('/', 'weekly', '1.0', '2026-05-20'),
        ('/about.html', 'monthly', '0.7', '2026-05-20'),
        ('/privacidad.html', 'yearly', '0.3', '2026-05-18'),
        ('/terminos.html', 'yearly', '0.3', '2026-05-18'),
        ('/cookies.html', 'yearly', '0.3', '2026-05-18'),
        ('/descargo.html', 'yearly', '0.3', '2026-05-18'),
        ('/nuestra-metodologia.html', 'monthly', '0.7', '2026-05-20'),
    ]
    for a in ['carlos-mendez', 'maria-rodriguez', 'roberto-pena']:
        static.append((f'/autores/{a}.html', 'monthly', '0.5', '2026-05-20'))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    for path, freq, priority, lastmod in static:
        lines.append(f'  <url><loc>{SITE}{path}</loc><lastmod>{lastmod}</lastmod><changefreq>{freq}</changefreq><priority>{priority}</priority></url>')
    for art in articles:
        lines.append(f'  <url><loc>{art["url"]}</loc><lastmod>{art["date"]}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>')
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'

def generate_rss(articles):
    items = []
    for art in articles:
        items.append(f'    <item><title>{html.escape(art["title"])}</title><link>{art["url"]}</link><guid isPermaLink="true">{art["url"]}</guid><description>{html.escape(art["description"])}</description><pubDate>{art["rss_date"]}</pubDate><category>{html.escape(art["category"])}</category></item>')

    now_str = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>FinanzasRD - Blog Financiero para República Dominicana</title>
    <link>{SITE}/</link>
    <description>Las mejores herramientas financieras y educación financiera para República Dominicana. Calcula préstamos, ahorro e inversiones. Blog con consejos prácticos.</description>
    <language>es-do</language>
    <lastBuildDate>{now_str}</lastBuildDate>
    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml"/>
    <managingEditor>info@finanzasrd.com (FinanzasRD)</managingEditor>
    <webMaster>info@finanzasrd.com (FinanzasRD)</webMaster>
{chr(10).join(items)}
  </channel>
</rss>
'''
    return rss

def main():
    print("Actualizando sitemap.xml y rss.xml...")
    articles = collect_articles()
    print(f"  Artículos encontrados: {len(articles)}")

    sitemap_content = generate_sitemap(articles, [])
    with open(SITEMAP, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print(f"  sitemap.xml escrito ({len(sitemap_content)} bytes)")

    rss_content = generate_rss(articles)
    with open(RSS, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    print(f"  rss.xml escrito ({len(rss_content)} bytes)")

    print("¡Listo!")

if __name__ == '__main__':
    main()
