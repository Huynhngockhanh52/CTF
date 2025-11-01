# factor_prime.py
# ----------------------------
# Lightweight prime factorization module (like Sage's factor())
# Returns a dictionary {prime: exponent}
# ----------------------------

import random
import math
from collections import Counter


def is_probable_prime(n, k=8):
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    # Small primes fast check
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n % p == 0:
            return n == p

    # Write n-1 = d * 2^s
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    def try_composite(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return False
        return True  # definitely composite

    # Deterministic bases for 64-bit range
    if n < 2**64:
        bases = [2, 325, 9375, 28178, 450775, 9780504, 1795265022]
        for a in bases:
            if a % n == 0:
                return True
            if try_composite(a):
                return False
        return True

    # Probabilistic for larger n
    for _ in range(k):
        a = random.randrange(2, n - 1)
        if try_composite(a):
            return False
    return True


def pollards_rho(n):
    """Pollard's Rho algorithm for factorization."""
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        x = random.randrange(2, n - 1)
        y = x
        c = random.randrange(1, n - 1)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
            if d == n:
                break
        if 1 < d < n:
            return d


def factor(n):
    """Return dict {prime: exponent} similar to Sage's factor()."""
    if n == 0:
        return {0: 1}
    if n < 0:
        n = -n

    factors = []

    def _factor_rec(m):
        if m == 1:
            return
        if is_probable_prime(m):
            factors.append(m)
            return
        d = pollards_rho(m)
        if d is None or d == m:
            # fallback to trial division
            for i in range(2, int(math.isqrt(m)) + 1):
                if m % i == 0:
                    _factor_rec(i)
                    _factor_rec(m // i)
                    return
            factors.append(m)
            return
        _factor_rec(d)
        _factor_rec(m // d)

    _factor_rec(n)
    return dict(Counter(factors))


# --- Optional quick test ---
if __name__ == "__main__":
    test_numbers = [
        2 * 3 * 3 * 97,
        600851475143,
        857504083339712752489993810777 * 1029224947942998075080348647219,
    ]
    for n in test_numbers:
        print(f"n = {n}")
        print("factors:", factor(n))
        print()
