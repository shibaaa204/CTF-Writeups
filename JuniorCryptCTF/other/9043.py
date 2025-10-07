from randcrack import RandCrack
from pwn import *
import time

rc = RandCrack()

# Kết nối tới server
io = remote("ctf.mf.grsu.by", 9043)
#io = process(["python3", "server_9043.py"])
# Bỏ qua phần intro cho đến khi thấy menu
while True:
    line = io.recvline(timeout=1).decode(errors="ignore").strip()
    print("[Intro]", line)
    if "2. Угадать следующее число" in line:
        break

# Thu thập đúng 624 số ngẫu nhiên
i = 0
while i < 624:
    io.sendline(b'1')
    time.sleep(0.3)  # tránh gửi quá nhanh

    try:
        line = io.recvline(timeout=1).decode(errors="ignore").strip()
    except EOFError:
        print("[!] Mất kết nối.")
        break

    print(f"[{i}] Line nhận được:", line)

    if "Следующее число:" in line:
        try:
            num = int(line.split(":")[-1].strip())
            rc.submit(num)
            i += 1
        except Exception as e:
            print(f"[!] Lỗi parse: {e}")
    else:
        print("[!] Không đúng định dạng hoặc bị rỗng, thử lại...")
        time.sleep(0.1)

# Đoán số tiếp theo
io.sendline(b'2')
io.recvuntil('Ваше число: '.encode('utf-8'))

guess = rc.predict_getrandbits(32)
print(f"[+] Dự đoán số tiếp theo: {guess}")
io.sendline(str(guess).encode())

# Nhận kết quả
print(io.recvall(timeout=2).decode(errors="ignore"))
