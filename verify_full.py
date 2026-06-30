import re

with open("blog/ley-quita-espera-rd.html", "rb") as f:
    raw = f.read()
text = raw.decode("utf-8")

checks = {
    "DOCTYPE present": text.startswith("<!DOCTYPE"),
    "html lang": '<html lang="es-DO"' in text,
    "has head": "<head>" in text,
    "author meta (proper name)": "Carlos Miguel Echavarr\u00eda Rodr\u00edguez" in text[:200],
    "canonical (no typo)": "canonical" in text and "cano\u00fanical" not in text,
    "icon OK (no corrupted bytes)": b"\xc3\xb0\xc5\xb8" not in raw,
    "apple icon OK": b'<link rel="apple-touch-icon"' in raw,
    "wordCount in JSON": '"wordCount"' in text,
    "table styles updated": "font-size:.95rem" in text and "#e9ecef" in text,
    "has main": "<main>" in text,
    "has section wrapper": '<section style="padding:6rem 0 2rem"' in text,
    "has article div": '<div class="container article">' in text,
    "has breadcrumb": 'nav class="breadcrumb"' in text,
    "has back link": 'class="back-link"' in text,
    "has h1": bool(re.search(r"<h1>", text)),
    "h1 matches title": "Ley de quita y espera en Rep\u00fablica Dominicana: gu\u00eda 2026" in text.split("<h1>")[1].split("</h1>")[0] if "<h1>" in text else False,
    "has meta-bar": "article-meta-bar" in text,
    "author in meta-bar": "Por <strong>" in text and "carlos-mendez.html" in text,
    "published date in meta-bar": "Publicado: <strong>20 de mayo de 2026</strong>" in text,
    "updated date in meta-bar": "Actualizado: <strong>" in text,
    "reading time in meta-bar": "min de lectura" in text,
    "has sources block": "article-sources" in text,
    "has author bio card": "author-carlos.jpg" in text,
    "author bio has correct name": "Carlos Miguel Echavarr\u00eda Rodr\u00edguez" in text[text.find("author-bio"):text.find("author-bio")+500],
    "author bio has role": "Fundador & Editor Principal de FinanzasRD" in text,
    "author bio has bio text": "Ingeniero en Sistemas Computacionales" in text,
    "has related posts": "related-posts" in text,
    "has footer": "<footer" in text,
    "body closes": "</body>" in text,
    "html closes": "</html>" in text,
}

all_ok = True
for k, v in checks.items():
    status = "OK" if v else "FAIL"
    if not v:
        all_ok = False
    print(f"  {status}: {k}")

print(f"\n{'ALL CHECKS PASSED' if all_ok else 'SOME CHECKS FAILED'}")
