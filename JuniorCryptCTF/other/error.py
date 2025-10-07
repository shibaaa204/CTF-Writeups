from pwn import *
from math import isqrt

def hamming_decode_7_4(code):
    if len(code) != 7 or any(c not in '01' for c in code):
        raise ValueError("Chuỗi phải có đúng 7 bit (0 hoặc 1)")

    bits = list(map(int, code))
    # Vị trí các bit: [p1, p2, d1, p3, d2, d3, d4]
    p1, p2, d1, p3, d2, d3, d4 = bits

    # Tính lại parity từ data
    c1 = d1 ^ d2 ^ d4
    c2 = d1 ^ d3 ^ d4
    c3 = d2 ^ d3 ^ d4

    # Syndrome để xác định lỗi
    s1 = p1 ^ c1
    s2 = p2 ^ c2
    s3 = p3 ^ c3
    error_pos = s1 * 1 + s2 * 2 + s3 * 4  # vị trí lỗi (1-indexed)

    # Nếu có lỗi, sửa nó
    if error_pos != 0:
        bits[error_pos - 1] ^= 1

    # Lấy lại d1 d2 d3 d4 sau khi sửa
    corrected_data = [bits[2], bits[4], bits[5], bits[6]]
    return error_pos, ''.join(map(str, corrected_data))


# Kết nối tới server
p = remote("ctf.mf.grsu.by", 9057)

for i in range(20):
    a = p.recvuntil(b'>>').decode().split()
    code = a[-3][:7]  # lấy chuỗi 7 bit
    err_pos, data = hamming_decode_7_4(code)
    answer = f'{err_pos}:{data}'
    print(f"[{i+1}/20] {code} => {answer}")
    p.sendline(answer.encode())

p.interactive()
