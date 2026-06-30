import glob, os, sys

files = glob.glob("blog/*.html")
files += [f for f in glob.glob("*.html") if os.path.basename(f) not in ("index.html", "template.html")]

bad_icon = []
bad_structure = []

for f in sorted(files):
    with open(f, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8", errors="replace")
    tn = os.path.basename(f)
    
    # Check for trailing garbage in icon line
    lines = text.split("\n")
    for i, l in enumerate(lines, 1):
        stripped = l.strip()
        if stripped.startswith('<link rel="icon"') or stripped.startswith('<link rel="apple-touch-icon"'):
            # Count closing tags - if more than one </text> in the line, there's trailing garbage
            if l.count("</text>") > 1:
                bad_icon.append((tn, i, l[:150]))
                break
    
    # Check for head leak into body (link tags after head)
    head_end = text.find("</head>")
    body_start = text.find("<body", head_end if head_end >= 0 else 0)
    
    if head_end >= 0 and body_start >= 0:
        # Check if there are <link> tags between head end and body start (or anywhere)
        between = text[head_end + 7:body_start]
        if "<link " in between:
            bad_structure.append((tn, "link_tags_between_head_and_body"))
        
        # Check for link tags outside head
        head_content = text[:head_end]
        body_content = text[body_start:]
        link_in_body = [l for l in body_content.split("\n") 
                       if l.strip().startswith("<link") and "stylesheet" not in l and "preconnect" not in l]
        if link_in_body:
            bad_structure.append((tn, f"{len(link_in_body)} link tags in body"))

print(f"Articles with trailing garbage in icon: {len(bad_icon)}")
for tn, line, snippet in bad_icon:
    print(f"  {tn}:{line} - {snippet}")

print(f"\nArticles with head/body structure issues: {len(bad_structure)}")
for tn, issue in bad_structure:
    print(f"  {tn}: {issue}")
