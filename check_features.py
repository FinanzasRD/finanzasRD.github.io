import os, glob, re

files = sorted(glob.glob("blog/*.html"))
for f in files:
    if f.endswith("template.html"):
        continue
    with open(f, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8", errors="replace")
    has_meta = "article-meta-bar" in text
    has_sources = "article-sources" in text
    if not has_meta or not has_sources:
        print(f"  {os.path.basename(f)}: meta={has_meta}, sources={has_sources}")
