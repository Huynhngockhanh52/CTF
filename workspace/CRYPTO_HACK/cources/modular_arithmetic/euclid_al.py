p = 26513
q = 32321

def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q_ = old_r // r
        old_r, r = r, old_r - q_ * r
        old_s, s = s, old_s - q_ * s
        old_t, t = t, old_t - q_ * t
    return old_r, old_s, old_t

g, u, v = extended_gcd(p, q)

print("p =", p)
print("q =", q)
print("gcd =", g)
print("u =", u)
print("v =", v)
print("Check: p*u + q*v =", p*u + q*v)

flag_value = min(u, v)
flag = f"crypto{{{flag_value}}}"
print("\nFlag (lower of u and v):", flag)