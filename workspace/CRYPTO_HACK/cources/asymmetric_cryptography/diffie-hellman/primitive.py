from Crypto.Util.number import getPrime
from sympy import factorint

def is_primitive_root(g, p):
    if g <= 1 or g >= p:
        return False

    factors = factorint(p - 1)

    # Kiểm tra điều kiện: g^((p-1)/q) != 1 (mod p) với mọi q là ước nguyên tố của (p-1)
    for q in factors.keys():
        if pow(g, (p - 1) // q, p) == 1:
            return False
    return True


p = 28151
for g in range(2, p):
    if is_primitive_root(g, p):
        print(f"{g} là phần tử sinh của Z_{p}!")
        break
