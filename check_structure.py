import glob, os, re

files = glob.glob("blog/*.html") + [f for f in glob.glob("*.html")
    if os.path.basename(f) not in ("template.html",)]

issues = []

for f in sorted(files):
    with open(f, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8", errors="replace")
    tn = os.path.basename(f)
    lines = text.split("\n")
    
    # Check 1: head properly before body
    head_close = text.find("</head>")
    body_open = text.find("<body", head_close if head_close >= 0 else 0)
    
    if head_close < 0:
        issues.append(f"{tn}: MISSING </head>")
        continue
    if body_open < 0:
        issues.append(f"{tn}: MISSING <body>")
        continue
    
    # Check for content between </head> and <body>
    gap = text[head_close + 7:body_open]
    gap_stripped = gap.strip()
    if gap_stripped and gap_stripped != "</html>":
        issues.append(f"{tn}: Content between </head> and <body>: {repr(gap_stripped[:80])}")
    
    # Check 2: duplicate <body>
    body_count = len(re.findall(r'<body[\s>]', text))
    if body_count != 1:
        issues.append(f"{tn}: <body> appears {body_count} times")
    
    # Check 3: duplicate </head>
    head_close_count = text.count("</head>")
    if head_close_count != 1:
        issues.append(f"{tn}: </head> appears {head_close_count} times")
    
    # Check 4: Are there <link> tags in the body that should be in head?
    body_content = text[body_open:].split("</body>")[0] if "</body>" in text[body_open:] else text[body_open:]
    body_lines = body_content.split("\n")
    for li, l in enumerate(body_lines, 1):
        stripped = l.strip()
        if stripped.startswith("<link") and "stylesheet" not in stripped and "preconnect" not in stripped:
            issues.append(f"{tn}:{li}: <link> tag in body: {stripped[:100]}")
            break  # one per file is enough

print(f"Files checked: {len(files)}")
print(f"Issues found: {len(issues)}")
for i in issues:
    print(f"  {i}")
