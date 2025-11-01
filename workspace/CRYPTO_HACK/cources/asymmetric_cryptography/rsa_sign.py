import hashlib
from Crypto.Util.number import bytes_to_long

with open("private.key", "r") as f:
    N = int(f.readline().strip().split("N = ")[1])
    d = int(f.readline().strip().split("d = ")[1])

# Ký
flag = b"crypto{Immut4ble_m3ssag1ng}"
hash_flag = hashlib.sha256(flag).digest()
num_flag = bytes_to_long(hash_flag)
signature = pow(num_flag, d, N)
print(signature)