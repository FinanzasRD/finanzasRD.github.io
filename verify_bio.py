import os
filepath = os.path.join("blog", "como-ahorrar-en-rd.html")
with open(filepath, "rb") as f:
    raw = f.read()
text = raw.decode("utf-8")
if "author-bio" in text:
    idx = text.find("author-bio")
    print(text[idx-50:idx+400])
