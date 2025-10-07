from pwn import *
from Crypto.Util.number import inverse

context.log_level = 'info'

def extract_params(io):
    io.recvuntil(b"p = ")
    p = int(io.recvline().strip())
    io.recvuntil(b"g = ")
    g = int(io.recvline().strip())
    io.recvuntil(b"y = ")
    y = int(io.recvline().strip())
    io.recvuntil(b"r = ")
    r = int(io.recvline().strip())
    return p, g, y, r

def collect_round(io):
    io.recvuntil(b"Challenge e = ")
    e = int(io.recvline().strip())

    io.sendlineafter(b":", b"0")  # Gửi sai s

    io.recvuntil(b"s = ")
    line = io.recvline().strip()
    try:
        s = int(line)
    except:
        print(f"[!] Không đọc được s: {line}")
        raise
    return e, s

def main():
    #io = remote("ctf.mf.grsu.by", 9050)
    io = process(["python3", "zkp9050.py"])  # hoặc thay bằng remote server thật
    io.recvuntil(b"Parameters:")
    p, g, y, r = extract_params(io)
    mod = p - 1

    # Thu thập 2 round đầu để khôi phục x
    for round_num in range(1, 3):
        io.recvuntil(f"=== Round {round_num} ===".encode())
        e, s = collect_round(io)
        if round_num == 1:
            e1, s1 = e, s
        else:
            e2, s2 = e, s

    # Tính x
    x1 = ((s1 - r) * inverse(e1, mod)) % mod
    x2 = ((s2 - r) * inverse(e2, mod)) % mod
    assert x1 == x2, "Lỗi: x không khớp"
    x = x1
    log.success(f"[+] Recovered x = {x}")

    # Gửi đúng s trong các round còn lại
    for round_num in range(3, 6):
        io.recvuntil(f"=== Round {round_num} ===".encode())
        io.recvuntil(b"Challenge e = ")
        e = int(io.recvline().strip())
        s = (r + e * x) % mod
        io.sendlineafter(b":", str(s).encode())
        io.recvuntil(b"Round passed")

    # Gửi x thật
    io.recvuntil(b"x:")
    io.sendline(str(x).encode())

    print(io.recvall(timeout=3).decode(errors="ignore"))

if __name__ == "__main__":
    main()
