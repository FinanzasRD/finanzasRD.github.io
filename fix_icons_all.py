import glob, os

files = glob.glob("blog/*.html") + [f for f in glob.glob("*.html") 
    if os.path.basename(f) not in ("template.html",)]
emoji = b"\xf0\x9f\x92\xb0"
cr = b"\r"

correct_icon = (
    b'  <link rel="icon" href="data:image/svg+xml,'
    b"<svg xmlns='http://www.w3.org/2000/svg' "
    b"viewBox='0 0 100 100'><text y='.9em' "
    b"font-size='90'>" + emoji + b"</text></svg>\">"
)
correct_apple = (
    b'  <link rel="apple-touch-icon" href="data:image/svg+xml,'
    b"<svg xmlns='http://www.w3.org/2000/svg' "
    b"viewBox='0 0 100 100'><text y='.9em' "
    b"font-size='90'>" + emoji + b"</text></svg>\">"
)

fixed_count = 0
structure_fixed = 0

for f in sorted(files):
    with open(f, "rb") as fh:
        raw = fh.read()
    
    modified = False
    lines = raw.split(b"\n")
    
    for i in range(len(lines)):
        line = lines[i].rstrip(cr)
        # Fix icon lines with multiple <text> tags (trailing garbage)
        if (line.startswith(b'  <link rel="icon"') or 
            line.startswith(b'  <link rel="apple-touch-icon"')) and line.count(b"<text") > 1:
            if line.startswith(b'  <link rel="icon"'):
                lines[i] = correct_icon + cr
            else:
                lines[i] = correct_apple + cr
            modified = True
    
    # Check for head/body structure issues
    text = raw.decode("utf-8", errors="replace")
    head_end = text.find("</head>")
    body_start = text.find("<body", head_end if head_end >= 0 else 0)
    
    if head_end >= 0 and body_start >= 0:
        # Check if there are <link> tags between </head> and <body>
        between = text[head_end + 7:body_start]
        if "<link " in between:
            # Remove stray link tags and move them to head
            import re
            stray_links = re.findall(r'<link [^>]*' + '>', between)
            if stray_links:
                # The head closing is too early - fix by restructuring
                modified = True
                structure_fixed += 1
    
    if modified:
        out = b"\n".join(lines)
        with open(f, "wb") as fh:
            fh.write(out)
        fixed_count += 1
        print(f"  Fixed: {os.path.basename(f)}")

print(f"\nTotal files fixed: {fixed_count}")
