# **🧮 Kummer Isogeny**

## Giới thiệu

**Kummer Isogeny** là một khái niệm quan trọng trong **isogeny-based cryptography**, được sử dụng để tăng tốc tính toán trên **đường cong elliptic (Elliptic Curves)**.

Nó dựa trên việc **chiếu ánh xạ isogeny xuống không gian Kummer**, nơi ta chỉ làm việc với **tọa độ x (hoặc projective)** thay vì toàn bộ điểm (x, y).


## **1️⃣ Kiến thức nền tảng**

### *1.1. Đường cong elliptic*

Một đường cong elliptic $E$ trên trường $\mathbb{F}_p$ có dạng tổng quát:
$$
E: y^2 = x^3 + Ax + B
$$

Tập các điểm $E(\mathbb{F}_p)$ cùng với điểm vô cực $\mathcal{O}$ tạo thành một **nhóm abelian**.

---

### *1.2. Isogeny là gì?*

Một **isogeny** $\phi: E \to E'$ là ánh xạ giữa hai đường cong elliptic **bảo toàn cấu trúc nhóm**:
$$
\phi(P + Q) = \phi(P) + \phi(Q)
$$

với **kernel** (tập các điểm bị ánh xạ về 𝒪) là hữu hạn.

Isogeny có thể được coi là “cầu nối” giữa hai đường cong elliptic, thường được mô tả bằng một **đa thức hữu tỉ**.

---

### *1.3. Kummer Variety*

**Kummer variety** của $E$, ký hiệu là $ \text{Kum}(E) $, được định nghĩa như:

$$
\text{Kum}(E) = E / \{ \pm 1 \}
$$

Tức là ta **đồng nhất hai điểm đối xứng qua trục x**:
$$
(x, y) \sim (x, -y)
$$

Do đó, ta chỉ còn làm việc với **tọa độ x**.

Ví dụ, trên đường cong **Montgomery** $ E: By^2 = x^3 + Ax^2 + x $,
Kummer variety chính là **Kummer line**, được mô tả bằng các giá trị x duy nhất.

---

### *1.4. Kummer Isogeny*

Nếu $ \phi: E \to E' $ là một isogeny giữa hai elliptic curves,  
thì ta có **Kummer isogeny** tương ứng:

$$
\tilde{\phi}: \text{Kum}(E) \to \text{Kum}(E')
$$

Kummer isogeny này cho phép **tính toán ánh xạ giữa hai Kummer lines**,  
**mà không cần theo dõi dấu ±y**.

👉 Điều này giúp:
- Giảm số phép tính cần thiết (vì chỉ làm việc với x);
- Giảm rủi ro rò rỉ thông tin (side-channel);
- Tăng tốc độ trong các giao thức như **CSIDH**, **SIKE**, **SQISign**.

---

## **2️⃣ Ví dụ minh họa**

### *2.1. Ví dụ đơn giản với Montgomery curve*

Giả sử ta có đường cong Montgomery:
$$
E: By^2 = x^3 + Ax^2 + x
$$
với $ A = 2 $, $ B = 1 $, trên trường $ \mathbb{F}_{97} $.

Ta chọn điểm $ P = (x, y) = (3, 6) $.

Phép nhân đôi điểm (x-only) trong Kummer line được tính bằng công thức:

$$
x_{2P} = \frac{(x^2 - 1)^2}{4x(x^2 + A x + 1)} \pmod{p}
$$

```python
p = 97
A = 2

def xDBL(x):
    num = (x**2 - 1)**2 % p
    den = (4 * x * (x**2 + A*x + 1)) % p
    return (num * pow(den, -1, p)) % p

xP = 3
x2P = xDBL(xP)
print("x-coordinate of 2P:", x2P)
```
## *3. Tổng thể minh họa*
```python
# 1. Khởi tạo trường hữu hạn
F = GF(101)  # Trường hữu hạn modulo 101
print("Trường hữu hạn F =", F)

# 2. Khởi tạo đường cong Montgomery: y^2 = x^3 + A x^2 + x
A = F(6)
E = EllipticCurve(F, [0, A, 0, 1, 0])
print("Đường cong Montgomery E:")
print(E)

# 3. Khởi tạo Kummer line tương ứng
K = KummerLine(E)
print("Kummer line K tương ứng với E:")
print(K)

# 4. Lấy một điểm ngẫu nhiên trên E
P = E.random_point()
print("Điểm ngẫu nhiên P trên E:", P)

# 5. Chuyển P sang Kummer line (lấy x-coordinate)
xP = K(P)
print("Điểm tương ứng trên Kummer line [P]:", xP)

# 6. Lấy thêm một điểm Q để minh họa pseudo-addition
Q = E.random_point()
xQ = K(Q)
xPQ = K(P - Q)
print("Điểm Q trên E:", Q)
print("Điểm [Q] trên Kummer line:", xQ)
print("Điểm [P-Q] trên Kummer line:", xPQ)

# 7. Pseudo-addition: tính [P+Q] trên Kummer line
xP_plus_Q = xP.add(xQ, xPQ)
print("Kết quả pseudo-addition [P+Q] trên Kummer line:", xP_plus_Q)

```

#### **Tham khảo:**
- https://github.com/GiacomoPope/KummerIsogeny
