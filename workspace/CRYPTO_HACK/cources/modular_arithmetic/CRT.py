from sympy.ntheory.modular import crt

remainders = [2, 3, 5]
moduli = [5, 11, 17]

x, m = crt(moduli, remainders)
print(f"x = {int(x)} mod {int(m)}")