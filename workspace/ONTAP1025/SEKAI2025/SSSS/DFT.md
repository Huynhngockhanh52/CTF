# 📘 Lý thuyết Fourier – Tổng quan và Ứng dụng

## 1️⃣ Giới thiệu

**Phân tích Fourier (Fourier Analysis)** là một công cụ toán học mạnh mẽ dùng để biểu diễn **một hàm hay tín hiệu phức tạp** dưới dạng **tổng của các sóng sin và cos** (hoặc các số mũ phức).

Ý tưởng cốt lõi:
> Mọi tín hiệu tuần hoàn đều có thể được biểu diễn bằng tổng vô hạn các sóng sin và cos với tần số khác nhau.

Điều này giúp chuyển từ **miền thời gian (time domain)** sang **miền tần số (frequency domain)**, từ đó dễ dàng phân tích, xử lý hoặc nén dữ liệu.

---

## 2️⃣ Biểu diễn Fourier cơ bản

### 🔹 Chuỗi Fourier (Fourier Series)

Với một hàm tuần hoàn \( f(t) \) có chu kỳ \( T \), ta có:

\[
f(t) = a_0 + \sum_{n=1}^{\infty} \left[ a_n \cos\left(\frac{2\pi n t}{T}\right) + b_n \sin\left(\frac{2\pi n t}{T}\right) \right]
\]

Trong đó:
\[
a_n = \frac{2}{T} \int_0^T f(t) \cos\left(\frac{2\pi n t}{T}\right) dt, \quad
b_n = \frac{2}{T} \int_0^T f(t) \sin\left(\frac{2\pi n t}{T}\right) dt
\]

👉 Mỗi cặp hệ số \( (a_n, b_n) \) cho biết **biên độ và pha** của sóng tại tần số thứ \( n \).

---

## 3️⃣ Biến đổi Fourier liên tục (Continuous Fourier Transform)

Với hàm không nhất thiết tuần hoàn \( f(t) \), ta dùng **biến đổi Fourier liên tục**:

\[
F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i \omega t} dt
\]
\[
f(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} F(\omega) e^{i \omega t} d\omega
\]

Ở đây:
- \( F(\omega) \): phổ tần số (frequency spectrum)
- \( \omega \): tần số góc (angular frequency)

---

## 4️⃣ Biến đổi Fourier rời rạc (DFT – Discrete Fourier Transform)

Trong máy tính, tín hiệu thường là **rời rạc**.  
DFT được định nghĩa cho dãy \( x_0, x_1, \dots, x_{N-1} \):

$$
X_k = \sum_{n=0}^{N-1} x_n \, e^{-2\pi i k n / N}, \quad k = 0, 1, \dots, N-1
$$

Phép nghịch đảo:
$$
x_n = \frac{1}{N} \sum_{k=0}^{N-1} X_k \, e^{2\pi i k n / N}
$$

### 🔸 Diễn giải trực quan

- DFT biến đổi tín hiệu trong **miền thời gian** thành **miền tần số**.  
- Mỗi giá trị \( X_k \) là biên độ phức của **thành phần tần số k** trong tín hiệu.

---

## 5️⃣ Fourier trên trường hữu hạn (Finite Field Fourier Transform)

Trong mật mã học và CTF, ta thường làm việc trong **trường hữu hạn GF(p)** thay vì số thực hoặc phức.  
Ở đó, phép biến đổi Fourier rời rạc được mô phỏng như sau:

$$
Y_k = \sum_{n=0}^{t-1} f_n \cdot g^{kn} \pmod{p}
$$

với:
- \( g \) là **căn nguyên thủy (primitive t-th root of unity)** trong \( GF(p) \)
- \( t \): số điểm ta chọn để đánh giá đa thức

### 🔹 Tính chất

Nếu \( g \) có bậc \( t \), thì các giá trị \( 1, g, g^2, \dots, g^{t-1} \) **tạo thành cơ sở** cho việc khôi phục đa thức.  
Phép đánh giá đa thức tại các điểm đó **tương tự phép DFT**, giúp ta dễ dàng suy ra các hệ số của đa thức (ngược lại chính là “
