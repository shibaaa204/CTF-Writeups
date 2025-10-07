import numpy as np

MOD = 257

A = np.array([
    [193, 243, 218],
    [240, 186, 172],
    [62,  118, 70]
])

encrypted = np.array([
    [76, 252, 109],
    [67, 73, 222],
    [227, 49, 104],
    [199, 230, 167],
    [118, 74, 4],
    [253, 70, 40],
    [78, 123, 230],
    [16, 240, 85],
    [62, 184, 34],
    [87, 50, 233],
    [224, 188, 40]
])

def matrix_modular_inverse(A, mod):
    det = int(round(np.linalg.det(A))) % mod
    det_inv = pow(det, -1, mod)
    A_inv = np.round(det * np.linalg.inv(A)).astype(int)
    return (det_inv * A_inv) % mod

# Tính A⁻¹ mod 257
A_inv = matrix_modular_inverse(A, MOD)

# Giải mã
decrypted = (encrypted @ A_inv.T) % MOD
flat = decrypted.flatten()

# Cắt byte về đúng 0–255
flag_bytes = bytes([b if b < 256 else 0 for b in flat])  # mod 257, nên 256 phải xử lý
flag = flag_bytes.rstrip(b"\x00")  # remove padding

#print("Flag:", flag.decode())

print("Flag:", flag.decode('latin1'))
