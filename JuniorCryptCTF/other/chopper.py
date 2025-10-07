import reedsolo
import base64

cd_b64 = b'TXkgZmF2b3JpdGUgcmVpbmQE/v9NMC7EPgT+fVKtYX1uAP1zYW1iaQT+ZXNpjl6WWlMZ+F06cKpDoSF7cIQ2Ug9OxlQ2VQ58otSA6jm+xjhwUFcr02pIxVfyY85y84/QFG8T94M='
corrupted_data1 = base64.b64decode(cd_b64)

for n1 in range(4, 40, 2):
    try:
        rs1 = reedsolo.RSCodec(n1)
        corrupted_data0 = rs1.decode(corrupted_data1)
    except:
        continue

    for n0 in range(4, 40, 2):
        try:
            rs0 = reedsolo.RSCodec(n0)
            original = rs0.decode(corrupted_data0)
            print(f"[+] Success with n1={n1}, n0={n0}")
            print("Recovered original text:", original.decode(errors="replace"))
            exit()
        except:
            continue

print("❌ Failed to decode with all tested n0/n1 combinations.")
