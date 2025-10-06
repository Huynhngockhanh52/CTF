# 🧩 Shamir Secret Sharing – Polynomial Reconstruction (CTF Writeup)

## 1️⃣ Ý tưởng chính

Trong bài này, ta cần khôi phục **bí mật (secret)** được ẩn bên trong một đa thức ngẫu nhiên mà server tạo ra theo cơ chế **Shamir Secret Sharing**.

Server cho phép ta **tự chọn các điểm x** để server tính giá trị của đa thức tại đó, sau đó trả về các giá trị y tương ứng.  
Từ đó, ta có thể khôi phục đa thức nếu biết đủ điểm.

---

### 🔹 Cơ sở lý thuyết

- Một đa thức bậc `t - 1` được xác định duy nhất nếu ta biết **t điểm (x, y)** khác nhau.  
- Thay vì chọn ngẫu nhiên các giá trị x, ta chọn các điểm đặc biệt:
  \[
  x = 1, g, g^2, g^3, \ldots, g^{t-1}
  \]
  trong đó `g` là **phần tử sinh (primitive root)** có **bậc t** trong trường hữu hạn `GF(p)`.

- Khi đó, việc đánh giá đa thức tại các điểm trên tương tự như **biến đổi Fourier rời rạc (DFT)** nhưng diễn ra trong **trường hữu hạn**.

=> Nhờ vậy, ta có thể khôi phục **toàn bộ các hệ số của đa thức** chỉ từ các giá trị y nhận được.

---

## 2️⃣ Điểm yếu của challenge

Server chạy hai vòng:

- Ở **vòng 1**, nó sinh một đa thức ngẫu nhiên và chèn **bí mật** làm **một hệ số** bất kỳ.  
- Ở **vòng 2**, nó sinh một đa thức mới — cũng chứa **cùng bí mật**, nhưng ở vị trí khác, và các hệ số còn lại hoàn toàn khác.

Sau khi ta khôi phục hai đa thức:

- Các hệ số bình thường đều ngẫu nhiên, nên hiếm khi trùng nhau.
- **Chỉ có bí mật** là giá trị xuất hiện trong **cả hai danh sách hệ số**.

👉 Do đó, chỉ cần lấy **giao (intersection)** của hai danh sách hệ số là tìm ra **secret**.

---

## 3️⃣ Phân tích mã nguồn solver

```python
from sage.all import *
from pwn import *

context.log_level = 'debug'

p = 2 ** 256 - 189                     # Số nguyên tố lớn (modulus)
R = PolynomialRing(GF(p), 'x')         # Vòng đa thức trên GF(p)
t = 29                                 # Bậc đa thức + 1

io = process(["python3", "chall.py"])  # Kết nối tới server local

def sample():
    io.sendline(str(t).encode())       # Gửi giá trị t cho server

    # Tìm g có bậc đúng bằng t
    while True:
        g = randint(1, p)
        g = pow(g, (p - 1)//t, p)
        if g != 1:
            break

    shares = []
    # Lấy t điểm (x_i, y_i)
    for i in range(t):
        x0 = pow(g, i, p)              # x_i = g^i mod p
        io.sendline(str(x0).encode())  # Gửi x_i
        y0 = int(io.recvline().strip())# Nhận y_i = f(x_i)
        shares.append((x0, y0))

    # Khôi phục đa thức bằng nội suy Lagrange
    return R.lagrange_polynomial(shares).coefficients()

# Lấy mẫu lần 1
s0 = sample()

# Gửi tín hiệu yêu cầu server sinh đa thức mới
io.sendline(b'1')
io.recvline()

# Lấy mẫu lần 2
s1 = sample()

# Tìm giao giữa hai tập hệ số → chính là secret
for secret in set(s0) & set(s1):
    io.sendline(str(secret).encode())
    io.interactive()
