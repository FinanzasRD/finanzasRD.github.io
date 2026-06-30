import os

filepath = os.path.join("blog", "como-ahorrar-en-rd.html")
with open(filepath, "rb") as f:
    raw = f.read()

lines = raw.split(b"\n")
for i in [39, 40, 41, 42]:
    if i <= len(lines):
        line = lines[i-1]
        print(f"Line {i} ({len(line)} bytes): {line[:200]}")

corrupt = b"\xc3\xb0\xc5\xb8\xe2\x80\x99\xc2\xb0"
correct = bytes([0xf0, 0x9f, 0x92, 0xb0])
print(f"\nCorrupt emoji still present: {corrupt in raw}")
print(f"Correct emoji present: {correct in raw}")
print(f"Correct emoji in line 39: {correct in lines[38]}")
print(f"Correct emoji in line 40: {correct in lines[39]}")

apple = lines[39]
print(f"Apple icon has clean ending: {apple.rstrip(b'\r').endswith(b'</svg>\">')}")
print(f"Apple icon has no extra text tags: {apple.count(b'<text') == 1}")
