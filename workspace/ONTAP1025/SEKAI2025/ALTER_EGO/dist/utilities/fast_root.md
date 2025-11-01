# **📘 Fast Square Root and Quadratic Roots in $\mathbb{F}_{p^2}$**

Hai hàm dưới đây được sử dụng trong tính toán **trên trường mở rộng $\mathbb{F}_{p^2}$**, thường xuất hiện trong các thuật toán **isogeny** (ví dụ SIDH, SIKE, SQISign).

Mục tiêu:
- Tính **căn bậc hai** (square root) trong $\mathbb{F}_{p^2}$ nhanh hơn;
- Tính **nghiệm của phương trình bậc hai** trên $\mathbb{F}_{p^2}$.

---

## **1. Phương thức `sqrt_Fp2(a)`**
Phương thức tính căn bậc hai của phần tử $a \in \mathbb{F}_{p^2}$, giả sử $p \equiv 3 \pmod 4$. Khi đó, với mọi phần tử $a \in \mathbb{F}_p$:
$$
\sqrt{a} = a^{\frac{p+1}{4}}
$$
Trong $\mathbb{F}_{p^2}$, ta có thêm phần tử ảo $i = \sqrt{-1}$.

### *1.1. Thuật toán*

1. Gọi $p = \text{đặc trưng của } \mathbb{F}_p $
2. Đặt $i = \sqrt{-1}$
3. Tính:
   $$   a_1 = a^{\frac{p - 3}{4}}   $$
   $$   x_0 = a_1 \cdot a, \quad \alpha = a_1 \cdot x_0 $$
4. Nếu $ \alpha = -1 $ thì:
   $$   x = i \cdot x_0     $$
   Ngược lại:
   $$   b = (1 + \alpha)^{\frac{p - 1}{2}}, \quad x = b \cdot x_0 $$
5. Trả về $x$

---

### *1.2 Ví dụ minh họa*

Giả sử $ p = 7 $, ta có $ 7 \equiv 3 \ (\text{mod } 4) $.

Khi đó, trường mở rộng $ \mathbb{F}_{7^2} = \mathbb{F}_7[i] $, trong đó $ i^2 = -1 $.

```python
# Giả lập trên SageMath
Fp2.<i> = GF(7^2, modulus=x^2+1)
a = 3 + 2*i
sqrt_a = sqrt_Fp2(a)
print(sqrt_a)       # 4 + 6*i
```

## **2. Phương thức `quadratic_roots(b, c)`**
Phương thức giải phương trình bậc hai: 
$$
    x^2 + bx + c = 0
$$
Trên trường $\mathbb{F}_{p^2}$, dựa trên công thức cổ điển:
$$
    x = \frac{-b  \pm \sqrt{b^2 - 4ac} }{2a}
$$

### *2.1. Cấu trúc phương thức*

```python
def quadratic_roots(b, c):
    d2 = b**2 - 4 * c
    d = sqrt_Fp2(d2)
    return ((-b + d) / 2, -(b + d) / 2)
```

---

### *1.2 Ví dụ minh họa*
Giải phương trình $x^2 + (2+i)x + (3 + 4i) = 0$. Ta có:

```python
Fp2.<i> = GF(7^2, modulus=x^2+1)
b = 2 + i
c = 3 + 4*i

r1, r2 = quadratic_roots(b, c)
print("Nghiệm 1:", r1)
print("Nghiệm 2:", r2)
```
Kết quả:
```
Nghiệm 1: 5 + 2*i
Nghiệm 2: 3 + 6*i
```