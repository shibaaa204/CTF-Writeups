enc = [0x6e, 0x49, 0x60, 0x09, 0x78, 0x75, 0x01, 0x3f, 0x58, 0x68, 0x4f]
key = b"MYSECRETKEY"

targets = [e ^ k for e, k in zip(enc, key)]

from string import ascii_letters, digits

# Chỉ duyệt các ký tự hợp lệ: a-zA-Z- (theo format flag yêu cầu)
charset = ascii_letters + "-"

candidates = []

for t in targets:
    found = False
    for c1 in charset:
        for c2 in charset:
            if ord(c1) ^ ord(c2) == t:
                candidates.append(c1 + c2)
                found = True
                break
        if found:
            break

middle = ''.join(candidates)
flag = f"grodno{{{middle}}}"
print("Flag:", flag)
