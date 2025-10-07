from time import time
from tqdm import trange

# Known constants
a = 2**15 - 1
b = 2**51 - 1

# Given outputs
x0 = 1751416129730664
x1 = 500383683954583
x2 = 1566165415030040

# Approximate time of generation
approx_m = int(time() * 1_000_000)

# Brute-force for m in ±5 million range
for m in trange(approx_m - 5_000_000, approx_m + 5_000_000):
    check1 = (a * x0 + b) % m == x1
    check2 = (a * x1 + b) % m == x2
    if check1 and check2:
        print(f"✅ Found modulus m = {m}")
        x3 = (a * x2 + b) % m
        print(f"🔮 Predicted next number: {x3}")
        break
else:
    print("❌ Failed to find a valid modulus.")
