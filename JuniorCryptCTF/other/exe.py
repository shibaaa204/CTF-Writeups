import hashlib

password = "Filitoni2"
local_a8 = bytearray()

for i, ch in enumerate(password):
    ch_bytes = ch.encode()  # 1 byte
    md5_ch = hashlib.md5(ch_bytes).digest()
    byte_from_md5 = md5_ch[0]
    
    val = i ^ (byte_from_md5 & 0x7b)
    local_a8.append(val)

# Bây giờ tính sha256 của local_a8
flag_hash = hashlib.sha256(local_a8).hexdigest()

flag = f"grodno{{{flag_hash}}}"
print("Decrypted flag:", flag)
