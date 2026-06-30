with open(r'C:\Users\winde\Desktop\finanzasrd\blog\mejores-cooperativas-en-rd.html', 'rb') as f:
    data = f.read()
idx = data.find(b'rel="icon"')
if idx >= 0:
    chunk = data[idx:idx+250]
    print('Icon link raw bytes:')
    print(chunk)
    print()
    print('Hex:', chunk.hex())
else:
    print('icon not found')
idx2 = data.find(b'rel="apple-touch-icon"')
if idx2 >= 0:
    chunk2 = data[idx2:idx2+250]
    print()
    print('Apple icon raw bytes:')
    print(chunk2)
