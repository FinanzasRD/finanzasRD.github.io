filepath = "blog/ley-quita-espera-rd.html"
cr = bytes([0x0d])
lf = bytes([0x0a])
em = bytes([0xf0, 0x9f, 0x92, 0xb0])

corr_icon = b'  <link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>' + em + b'</text></svg>">' + cr
corr_apple = b'  <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>' + em + b'</text></svg>">' + cr

with open(filepath, "rb") as f:
    raw = f.read()

fixed = False
lines = raw.split(lf)
for i, line in enumerate(lines):
    stripped = line.rstrip(cr)
    if stripped.startswith(b'  <link rel="icon"') and stripped.count(b"<text") > 1:
        lines[i] = corr_icon
        fixed = True
    elif stripped.startswith(b'  <link rel="apple-touch-icon"') and stripped.count(b"<text") > 1:
        lines[i] = corr_apple
        fixed = True

if fixed:
    out = lf.join(lines)
    with open(filepath, "wb") as f:
        f.write(out)
    print("Fixed icon lines")
else:
    print("No fix needed")
