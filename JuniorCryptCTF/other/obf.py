import numpy as np
from sympy import Matrix

MOD = 257
BLOCK_SIZE = 3  # Kích thước khối: 3 byte → ma trận 3x3

def modinv_matrix(A, mod):
    """
    Tính nghịch đảo ma trận modulo `mod` bằng sympy
    (chính xác hơn so với float)
    """
    M = Matrix(A.tolist())
    if M.det() % mod == 0:
        raise ValueError("Matrix not invertible under mod {}".format(mod))
    M_inv = M.inv_mod(mod)
    return np.array(M_inv.tolist(), dtype=int)

def pad(data: bytes, block_size: int) -> bytes:
    pad_len = (block_size - len(data) % block_size) % block_size
    return data + bytes([0] * pad_len)

def encrypt(data: bytes, key_matrix: np.ndarray) -> np.ndarray:
    padded = pad(data, key_matrix.shape[0])
    reshaped = np.frombuffer(padded, dtype=np.uint8).reshape(-1, key_matrix.shape[0])
    return (reshaped @ key_matrix.T) % MOD

def decrypt(cipher: np.ndarray, key_matrix: np.ndarray) -> bytes:
    A_inv_T = modinv_matrix(key_matrix, MOD).T
    decrypted = (cipher @ A_inv_T) % MOD
    flat = decrypted.flatten()
    flat = np.array(flat, dtype=np.uint8)
    return bytes(flat).rstrip(b"\x00")

if __name__ == "__main__":
    flag = b"VERYSECRETFLAG"  # 👈 bạn có thể thay bằng flag thật tại đây

    # Sinh ma trận ngẫu nhiên A khả nghịch
    while True:
        A = np.random.randint(1, MOD, (BLOCK_SIZE, BLOCK_SIZE))
        try:
            _ = modinv_matrix(A, MOD)
            break
        except:
            continue

    # Mã hóa flag
    encrypted = encrypt(flag, A)

    # In kết quả
    print("A =")
    print(np.array2string(A, separator=', '))
    print("\nEncrypted =")
    print(np.array2string(encrypted, separator=', '))
    A=[[193, 243, 218], [240, 186, 172], [62, 118, 70]]
    A = np.array(A)
    
    encrypted=[[76, 252, 109], [67, 73, 222], [227, 49, 104], [199, 230, 167], [118, 74, 4], [253, 70, 40], [78, 123, 230], [16, 240, 85], [62, 184, 34], [87, 50, 233], [224, 188, 40]]
    # Giải mã lại kiểm tra
    decrypted_flag = decrypt(encrypted, A)
    print("\nDecrypted flag:", decrypted_flag)
