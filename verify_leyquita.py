import re

with open("blog/ley-quita-espera-rd.html", "rb") as f:
    raw = f.read()
text = raw.decode("utf-8")

checks = {
    "has_main": "<main>" in text,
    "has_h1": bool(re.search(r"<h1>", text)),
    "has_meta_bar": "article-meta-bar" in text,
    "has_breadcrumb": "breadcrumb" in text,
    "has_back_link": "back-link" in text,
    "has_author_bio_card": "author-carlos.jpg" in text,
    "has_sources": "article-sources" in text,
    "has_related": "related-posts" in text,
    "has_adsense": "adsense" in text,
    "has_footer": "<footer" in text,
    "icon_ok": not any(b in raw for b in [b"\xef\xbf\xbd", b"\xc3\xb0"]),
    "canonical_ok": "canonical" in text and "canoúnical" not in text,
}

for k, v in checks.items():
    status = "OK" if v else "FAIL"
    print(f"  {status}: {k}")

# Show meta-bar content
if "article-meta-bar" in text:
    idx = text.index("article-meta-bar")
    end = text.index("</div>", idx)
    print(f"\nMeta-bar:\n{text[idx:end+6]}")
