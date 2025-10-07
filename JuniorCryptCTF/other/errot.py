def hamming74_decode(block):
    # Chuyển block string -> list int
    bits = [int(b) for b in block]
    
    # Parity check matrix H (3x7)
    H = [
        [1, 0, 1, 0, 1, 0, 1],  # P1 kiểm tra bit 0,2,4,6
        [0, 1, 1, 0, 0, 1, 1],  # P2 kiểm tra bit 1,2,5,6
        [0, 0, 0, 1, 1, 1, 1],  # P3 kiểm tra bit 3,4,5,6
    ]
    
    # Tính syndrome
    syndrome = [sum(hb & bb for hb, bb in zip(row, bits)) % 2 for row in H]
    syndrome_value = int("".join(map(str, syndrome)), 2)

    # Nếu syndrome ≠ 0 => sửa lỗi tại bit đó (vị trí từ 1 đến 7)
    if syndrome_value != 0 and 1 <= syndrome_value <= 7:
        bits[syndrome_value - 1] ^= 1  # Lật bit sai

    # Trích xuất 4 bit dữ liệu gốc (theo thứ tự chuẩn: d1 d2 d3 d4)
    # bit index: [p1 p2 d1 p3 d2 d3 d4]
    data_bits = [bits[2], bits[4], bits[5], bits[6]]
    return data_bits

# Đọc toàn bộ input
with open("hamming_input.txt") as f:
    lines = f.read().strip().splitlines()

all_bits = []

for line in lines:
    if len(line.strip()) != 7:
        continue
    decoded = hamming74_decode(line.strip())
    all_bits.extend(decoded)

# Gom thành byte (8 bits)
bytes_out = bytearray()
for i in range(0, len(all_bits), 8):
    byte_bits = all_bits[i:i+8]
    if len(byte_bits) < 8:
        break
    value = int("".join(map(str, byte_bits)), 2)
    bytes_out.append(value)

# In ra
print("Decoded (bytes):", bytes_out)
try:
    print("Decoded (string):", bytes_out.decode())
except:
    print("Cannot decode as string")
