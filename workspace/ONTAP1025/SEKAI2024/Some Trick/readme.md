## 🧩 1. Tổng quan

Đây là chương trình Python mô phỏng **một hệ mã dựa trên hoán vị (permutation)**.  
Tất cả được điều khiển bởi một hạt giống (`CIPHER_SUITE`) dùng để sinh ra các hoán vị ngẫu nhiên.

```python
CIPHER_SUITE = randbelow(2**256)
random.seed(CIPHER_SUITE)
```

Do `random.seed()` được đặt bằng giá trị in ra (`oPUN_SASS_SASS_l version 4.0.{CIPHER_SUITE}`), ta có thể **reproduce chính xác toàn bộ phép mã hóa** nếu ta biết được `CIPHER_SUITE`.

---

## ⚙️ 2. Cấu trúc dữ liệu chính

### 2.1. Các tham số

```python
GSIZE = 8209
GNUM = 79
LIM = GSIZE**GNUM
```

-   `GSIZE` = 8209: độ dài của mỗi hoán vị.
    
-   `GNUM` = 79: số lượng tầng hoán vị.
    
-   `LIM = 8209^79`: cực kỳ lớn → không thể brute-force trực tiếp.
    

### 2.2. Hàm `gen(n)`

Sinh ra **một hoán vị (permutation)** trên `n` phần tử.

```python
def gen(n):
    p, i = [0]*n, 0
    for j in random.sample(range(1, n), n - 1):
        p[i], i = j, j
    return tuple(p)
```

👉 Kết quả là một tuple `p` sao cho `p[i] = j` mô tả ánh xạ của `i → j`.  
Nó tạo ra 79 hoán vị khác nhau, mỗi hoán vị kích thước 8209.

```python
G = [gen(GSIZE) for i in range(GNUM)]
```

---

## 🔢 3. Hàm `gexp(g, e)`

Đây là **phép lũy thừa hoán vị** (composition exponentiation).

```python
def gexp(g, e):
    res = tuple(g)
    while e:
        if e & 1:
            res = tuple(res[i] for i in g)
        e >>= 1
        g = tuple(g[i] for i in g)
    return res
```

Nó tính $g^e$, nghĩa là **áp dụng hoán vị `g` lặp lại `e` lần**.  
Cách viết này tương tự **exponentiation by squaring** (bình phương & nhân nhanh), giúp tính nhanh $g^e \mod n!$.

---

## 🧮 4. Hàm `enc(k, m, G)`

Hàm mã hóa chính — đây là “trick” thú vị nhất.

```python
def enc(k, m, G):
    if not G:
        return m
    mod = len(G[0])
    return gexp(G[0], k % mod)[m % mod] + enc(k // mod, m // mod, G[1:]) * mod
```

Hiểu logic:

-   `G` là danh sách các hoán vị.
    
-   Mỗi tầng hoạt động **theo từng “chữ số cơ sở GSIZE”** của `k` và `m`.
    
-   Ta tách `k` và `m` thành dạng cơ số `mod` = 8209, rồi mã hóa từng tầng:
    

$$
\text{enc}(k, m, [G_0, G_1, \dots]) = G_0^{k_0}[m_0] + \text{enc}(k_1, m_1, G[1:]) \times 8209
$$

→ tức là **mã hóa chữ số m\_i bằng phép hoán vị G\_i^k\_i**, rồi ghép lại thành số lớn ở dạng cơ số 8209.

---

## 🔁 5. Hàm `inverse(perm)`

Trả về hoán vị nghịch đảo để giải mã.

```python
def inverse(perm):
    res = list(perm)
    for i, v in enumerate(perm):
        res[v] = i
    return res
```

---

## 🔐 6. Quy trình “mã hóa hội thoại”

1.  Sinh `G` (79 hoán vị).
    
2.  Mã hóa FLAG (đã được padding ngẫu nhiên hai lần).
    
3.  Bob chọn `bob_key`, mã hóa `bob_encr = enc(FLAG, bob_key, G)`
    
4.  Alice chọn `alice_key`, mã hóa tiếp: `alice_encr = enc(bob_encr, alice_key, G)`
    
5.  Bob giải mã lại bằng `inverse(G)`.
    

---

## 🧨 7. Trick chính — Tính chất nhóm hoán vị

Hàm `enc` là phép **ánh xạ kết hợp khóa & thông điệp theo tầng**.  
Nếu ta gọi `E_k(m) = enc(k, m, G)` thì:

$$
E_{k_1}(E_{k_2}(m)) = E_{k_1 + k_2}(m)
$$

→ Đây là **homomorphism cộng khóa modulo LIM**.  
Do đó, việc `bob` và `alice` lần lượt mã hóa tương đương với **cộng khóa** như trong Diffie–Hellman nhưng diễn ra trên nhóm hoán vị.

👉 Khi Bob giải mã bằng khóa nghịch đảo, ta có:

$$
E_{bob}^{-1}(E_{alice}(E_{bob}(m))) = E_{alice}(m)
$$

nên cuối cùng Bob sẽ nhận lại **Alice’s encryption của FLAG**.

---

## 📉 8. Điểm yếu / Khả năng tấn công

-   `random.seed(CIPHER_SUITE)` ⇒ nếu ta có thể đọc giá trị `{CIPHER_SUITE}` in ra → **ta có thể hoàn toàn tái tạo lại `G`**, từ đó giải ngược `enc`.
    
-   `FLAG` được pad bằng `randbits`, không bảo mật nếu ta biết seed.
    
-   Tất cả đều dùng **Python `random`** → không phải cryptographically secure.
    
-   Hàm `enc` là **deterministic** và invertible nếu biết `G`.
    

Do đó:  
➡️ Challenge “Some Trick” chỉ “trick” người đọc bằng cấu trúc phức tạp, nhưng thực ra:  
nếu ta biết `CIPHER_SUITE`, ta có thể **tái tạo toàn bộ G** và **viết `dec(k, c, G)` = `enc(k, c, [inverse(g) for g in G])`** để khôi phục lại FLAG.

---
## ✅ Tóm tắt ý tưởng cốt lõi

| Thành phần | Vai trò | Ghi chú |
| --- | --- | --- |
| `G[i]` | hoán vị thứ i | dựa trên seed |
| `gexp(g, e)` | tính g^e | lũy thừa hoán vị |
| `enc(k, m, G)` | mã hóa | dùng hệ cơ số 8209 |
| `inverse(G)` | giải mã | nghịch đảo từng hoán vị |
| `CIPHER_SUITE` | seed duy nhất | in ra, có thể khôi phục |
| Trick | ẩn phép cộng trong nhóm hoán vị | Diffie–Hellman kiểu hoán vị |