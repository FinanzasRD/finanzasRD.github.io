import re

filepath = r"blog/ley-quita-espera-rd.html"

with open(filepath, "rb") as f:
    raw = f.read()

text = raw.decode("utf-8")

# Split into head and body
head_end = text.find("</head>")
head = text[:head_end + 7]
# Split body at header end
header_end = text.find("</header>")
header_section = text[head_end + 7:header_end + 9]  # includes <body> tag + header

# Content between </header> and the first <div class="article-sources"> or old author-bio
# Find the old author-bio start (marker for where bottom sections begin)
old_bio_start = text.find('<a href="../autores/carlos-mendez.html" class="author-bio"', header_end)

# Content to preserve is from after header to old_bio_start
article_content = text[header_end + 9:old_bio_start].strip()

# Find sources section
sources_start = text.find('<div class="article-sources">', old_bio_start)
sources_end = text.find("</div>", text.find('<span class="sources-note">', sources_start))
sources_section = text[sources_start:sources_end + 6].strip()

# Find related posts section
related_start = text.find('<section class="related-posts">', sources_end)
related_end = text.find("</section>", related_start)
related_section = text[related_start:related_end + 10].strip()

# Find footer
footer_start = text.find("<footer", related_end)
footer_end = text.find("</html>", footer_start)
footer_section = text[footer_start:footer_end + 7].strip()

# Find adsense
adsense_start = text.find('<div class="adsense">', related_end)
if adsense_start < 0 or adsense_start > footer_start:
    adsense_start = text.find('<ins class="adsense"', related_end)
adsense_end = text.find("</div>", adsense_start)
if adsense_end < 0 or adsense_end > footer_start:
    adsense_end = text.find("</ins>", adsense_start)
    adsense_end = text.find("</div>", adsense_end) + 6
else:
    adsense_end += 6
adsense_section = text[adsense_start:adsense_end].strip() if adsense_start >= 0 else ""

# Extract reading time from content
word_count_estimate = len(article_content.split())
reading_time = max(1, round(word_count_estimate / 200))

# Extract date from JSON-LD
date_match = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', text)
pub_date = date_match.group(1) if date_match else "2026-05-20"
mod_match = re.search(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})"', text)
mod_date = mod_match.group(1) if mod_match else pub_date

# Format dates in Spanish
months = {"01": "enero", "02": "febrero", "03": "marzo", "04": "abril",
          "05": "mayo", "06": "junio", "07": "julio", "08": "agosto",
          "09": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"}
pub_parts = pub_date.split("-")
pub_human = f"{int(pub_parts[2])} de {months.get(pub_parts[1], pub_parts[1])} de {pub_parts[0]}"
mod_parts = mod_date.split("-")
mod_human = f"{int(mod_parts[2])} de {months.get(mod_parts[1], mod_parts[1])} de {mod_parts[0]}"

# Title from h1 or title tag
title_match = re.search(r'<title>(.*?) - FinanzasRD</title>', head)
title = title_match.group(1).strip() if title_match else ""

new_body = f"""<body>
  <header class="header" id="header">
    <div class="container header__container">
      <a href="../index.html" class="header__logo" aria-label="FinanzasRD - Inicio">FinanzasRD</a>
      <button class="header__toggle" id="menuToggle" aria-label="Abrir menú" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <nav class="header__nav" id="mainNav" role="navigation" aria-label="Navegación principal">
        <ul class="header__menu">
          <li><a href="../index.html#inicio" class="header__link">Inicio</a></li>
          <li><a href="../index.html#calculadoras" class="header__link">Calculadoras</a></li>
          <li><a href="../index.html#conversor" class="header__link">Conversor</a></li>
          <li><a href="../index.html#blog" class="header__link">Blog</a></li>
          <li><a href="../index.html#comparador" class="header__link">Comparador</a></li>
          <li><a href="../index.html#contacto" class="header__link">Contacto</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>
    <section style="padding:6rem 0 2rem">
      <div class="container article">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <a href="../index.html">Inicio</a>
          <span class="breadcrumb__sep">/</span>
          <a href="../index.html#blog">Blog</a>
          <span class="breadcrumb__sep">/</span>
          <span class="breadcrumb__current">{title}</span>
        </nav>
        <a href="../index.html#blog" class="back-link">← Volver al blog</a>
        <h1>{title}</h1>

        <div class="article-meta-bar">
          <span>Por <strong><a href="../autores/carlos-mendez.html" style="color:var(--primary-dark)">Carlos Miguel Echavarría Rodríguez</a></strong></span>
          <span class="dot">•</span>
          <span>Publicado: <strong>{pub_human}</strong></span>
          <span class="dot">•</span>
          <span>Actualizado: <strong>{mod_human}</strong></span>
          <span class="dot">•</span>
          <span>{reading_time} min de lectura</span>
        </div>

{article_content}

        {sources_section}

        <a href="../autores/carlos-mendez.html" class="author-bio" style="display:flex;text-decoration:none;cursor:pointer;gap:1rem;align-items:start;background:var(--primary-light);border-radius:var(--radius-sm);padding:1.25rem;margin:2rem 0;border:1px solid rgba(10,92,54,0.12)">
          <div class="author-bio__avatar" style="font-size:2.5rem;flex-shrink:0;width:56px;height:56px;display:flex;align-items:center;justify-content:center;border-radius:50%;overflow:hidden;background:var(--white)">
            <img src="../images/author-carlos.jpg" alt="" style="width:100%;height:100%;object-fit:cover" onerror="this.style.display='none';this.parentElement.textContent='👨‍💼'">
          </div>
          <div class="author-bio__info" style="flex:1">
            <strong style="display:block;color:var(--dark);font-size:.95rem">Carlos Miguel Echavarría Rodríguez</strong>
            <span style="display:block;color:var(--primary-dark);font-size:.8rem;font-weight:600;margin-bottom:.5rem">Fundador & Editor Principal de FinanzasRD</span>
            <p style="font-size:.85rem;color:var(--text-light);margin:0;line-height:1.6">Ingeniero en Sistemas Computacionales (UTESA) apasionado por la educación financiera. Creador de FinanzasRD. Combino mi formación tecnológica con el análisis financiero para ayudarte a tomar mejores decisiones con tu dinero.</p>
          </div>
          <span style="color:var(--primary-dark);font-weight:600;font-size:.8rem;white-space:nowrap;align-self:center">Ver perfil →</span>
        </a>

        {related_section}
      </div>
    </section>

    {adsense_section}

  </main>

{footer_section}
"""

# Write back - head + new body
with open(filepath, "wb") as f:
    f.write((head + "\n" + new_body).encode("utf-8"))

print(f"Fixed: {filepath}")
print(f"  Title: {title}")
print(f"  Published: {pub_human}")
print(f"  Reading time: {reading_time} min")
print(f"  Content length: {len(article_content)} chars")
