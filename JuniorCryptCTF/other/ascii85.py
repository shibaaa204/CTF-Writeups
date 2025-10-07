import base64

data = ";Ibge=6Sb+;_TAM9sZoF>P'Vo9s[Bn=Le:4=5L7];wD_89s:NZ:]OHr:]p.j9Dj!D=c>7%;wD_V"

for shift in range(1, 95):
    try:
        caesar_reversed = ''.join(
            chr((ord(c) - shift) % 256) for c in data
        )

        decoded = base64.a85decode(caesar_reversed.encode())

        # Nếu decode thành công, in ra luôn
        print(f"[✓] Shift = {shift} -> decoded = {decoded[:50]}...")

        if b'flag{' in decoded or b'ctf{' in decoded:
            print(f"\n[!] FOUND (shift = {shift}):")
            print("Ascii85 input:", caesar_reversed)
            print("Decoded flag:", decoded.decode(errors='ignore'))
            break
    except Exception as e:
        print(f"[✗] Shift = {shift} failed: {type(e).__name__}")

