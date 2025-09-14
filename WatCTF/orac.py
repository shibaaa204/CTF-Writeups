#!/usr/bin/env python3
import sys
import re
import json
from typing import List
from pwn import process

BLOCK = 16

# ---------------- Oracle giao tiếp ----------------
class LocalOracle:
    def __init__(self, cmd: List[str]):
        self.io = process(cmd)

    def _readline(self) -> str:
        line = self.io.recvline(timeout=5).decode(errors="ignore").strip()
        return line

    def get_initial_ciphertext(self) -> bytes:
        hex_line = None
        for _ in range(50):
            line = self._readline()
            if re.fullmatch(r"[0-9a-fA-F]+", line or "") and len(line) >= 32:
                hex_line = line
                break
        if not hex_line:
            raise RuntimeError("Không nhận được ciphertext hex ban đầu.")
        return bytes.fromhex(hex_line)

    def query(self, iv_ct_hex: str) -> str:
        self.io.sendline(iv_ct_hex.encode())
        return self._readline()

# ---------------- Padding Oracle Attack ----------------
def split_blocks(b: bytes, n: int = BLOCK) -> List[bytes]:
    return [b[i:i+n] for i in range(0, len(b), n)]

def join_blocks(blocks: List[bytes]) -> bytes:
    return b"".join(blocks)

def oracle_valid_padding(resp: str) -> bool:
    return "Valid padding" in resp
def decrypt_block(oracle: LocalOracle, target: bytes, full_ct: bytes) -> bytes:
    inter = bytearray(BLOCK)
    fake = bytearray(BLOCK)

    for pad in range(1, BLOCK+1):
        idx = BLOCK - pad
        found = False
        for guess in range(256):
            X = bytearray(fake)

            # set các byte đã biết
            for j in range(1, pad):
                k = BLOCK - j
                X[k] = fake[k] ^ inter[k] ^ pad

            # brute byte hiện tại
            X[idx] = guess

            # Đặt X làm block trước target
            forged = join_blocks([bytes(X), target])  

            # prepend thêm phần còn lại để đủ format
            forged = join_blocks([forged, full_ct])

            resp = oracle.query(forged.hex())
            if oracle_valid_padding(resp):
                inter[idx] = guess ^ pad
                found = True
                break
        if not found:
            raise RuntimeError(f"Không tìm được byte ở pad={pad}")

    return bytes(inter)


def cbc_po_decrypt(oracle: LocalOracle, iv: bytes, ct_blocks: List[bytes]) -> bytes:
    plaintext = b""
    for bi, C in enumerate(ct_blocks):
        inter = decrypt_block(oracle, C)

        # XOR với block trước (hoặc IV nếu là block 0)
        prev = iv if bi == 0 else ct_blocks[bi-1]
        P = bytes([inter[i] ^ prev[i] for i in range(BLOCK)])
        plaintext += P
    return plaintext

def pkcs7_unpad(data: bytes, block: int = BLOCK) -> bytes:
    pad = data[-1]
    if pad < 1 or pad > block:
        raise ValueError("bad pad")
    if data[-pad:] != bytes([pad]) * pad:
        raise ValueError("bad pad bytes")
    return data[:-pad]

# ---------------- Main ----------------
def main():
    o = LocalOracle([sys.executable, "challenge.py"])
    orig = o.get_initial_ciphertext()
    iv, ct = orig[:BLOCK], orig[BLOCK:]
    ct_blocks = split_blocks(ct, BLOCK)

    print(f"[+] Số block ciphertext: {len(ct_blocks)}")

    padded_plain = cbc_po_decrypt(o, iv, ct_blocks)
    plain = pkcs7_unpad(padded_plain, BLOCK)

    print("[+] Plaintext JSON:\n", plain.decode(errors="ignore"))

    try:
        obj = json.loads(plain.decode())
        print("[+] Flag:", obj.get("access_code"))
    except Exception:
        print("[!] Không parse được JSON")

if __name__ == "__main__":
    main()
