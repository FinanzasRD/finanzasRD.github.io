import glob, os

for f in sorted(glob.glob("*.html")):
    with open(f, "rb") as fh:
        raw = fh.read()
    lines = raw.split(b"\n")
    name = os.path.basename(f)
    print(f"{name}: {len(lines)} lines")
