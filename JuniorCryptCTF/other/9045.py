from pwn import *
from untwister import Untwister
import time

# Khởi tạo Untwister
ut = Untwister()

# Kết nối tới server
#io = remote("ctf.mf.grsu.by", 9045)
io = process(["python3", "server_9045.py"])
# Bỏ qua intro
while True:
    line = io.recvline(timeout=2).decode(errors="ignore").strip()
    print("[Intro]", line)
    if "2. Угадать следующее число" in line:
        break

# Gửi lệnh lấy 624 số
for i in range(624):
    io.sendline(b"1")
    line = io.recvline(timeout=2).decode(errors="ignore").strip()
    print(f"[{i}] Line: {line}")

    if "Следующее число:" in line:
        num = int(line.split(":")[-1].strip())
        bits = bin(num)[2:].zfill(31) + '?'  # Thêm bit cao nhất chưa biết
        ut.submit(bits)
    else:
        print("[!] Dòng không hợp lệ")
        continue
   # time.sleep(0.2)

# Đoán số tiếp theo
io.sendline(b"2")
io.recvuntil("Ваше число: ".encode("utf-8"))

r = ut.get_random()
guess = r.getrandbits(31)
print("[+] Dự đoán:", guess)
io.sendline(str(guess).encode())

# In kết quả
print(io.recvall(timeout=2).decode(errors="ignore"))
