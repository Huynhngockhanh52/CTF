## **1. Lý thuyết**
### ***1.1. Phép cộng trong trường $\mathbb{F}_{256}$***

Mỗi phần tử 8-bit trong $\mathbb{F}_{256}$ được xem như **một đa thức bậc ≤ 7** với hệ số trong $\mathbb{F}_2 = \{0,1\}$:
$$
a(x) = a_0 + a_1x + a_2x^2 + \dots + a_7x^7 = \sum_{i=1}^{7}{a_i.x^i}
$$
trong đó mỗi $a_i$ là một bit của số.

Phép cộng trong $\mathbb{F}_{256}$ chính là **cộng từng hệ số modulo 2** — tức là **XOR** từng bit:
$$
(a + b)(x) = (a_0 \oplus b_0) + (a_1 \oplus b_1)x + \dots + (a_7 \oplus b_7)x^7
$$
Nói cách khác, cộng hai byte trong $\mathbb{F}_{256}$ chính là thực hiện phép XOR bitwise của chúng.

**Ví dụ:**
$$24 = 00011000_2 = x^4 + x^3,\quad 8 = 00001000_2 = x^3$$
$$\Rightarrow (x^4 + x^3) + x^3 = x^4 \Rightarrow 00010000_2 = 16$$
→ Như vậy, phép $\text{XOR}$ có thể được xem như một phép cộng trên trường mở rộng của $\mathbb{F_2}$.

---

### ***1.2. Phần tử sinh***
Một **trường hữu hạn** (finite field), ký hiệu là $\mathbb{F}_{p^n}$, là tập hợp hữu hạn các phần tử có:
-   Phép **cộng**, **nhân**, **trừ**, **chia** (trừ chia cho 0),
-   Và thỏa mãn các tính chất đại số của một **trường** (giống như $\mathbb{R}$ hay $\mathbb{Q}$).\
Ví dụ:
    -   $\mathbb{F}_2 = \{0, 1\}$
    -   $\mathbb{F}_3 = \{0, 1, 2\}$
    -   $\mathbb{F}_{2^8}$: có 256 phần tử.

Trong một trường $\mathbb{F}_{p^n}$, nếu bỏ phần tử 0 đi, tập các phần tử còn lại $\mathbb{F}_{p^n}^\times = \mathbb{F}_{p^n} \setminus \{0\}$  
**tạo thành một nhóm Abel** theo phép nhân. Nhóm này có đúng $p^n - 1$ phần tử.

Ví dụ: $\mathbb{F}_{2^8}^\times$ có $256 - 1 = 255$ phần tử.

Một **phần tử sinh (generator)**, hay còn gọi là **phần tử nguyên thủy (primitive element)** — là **một phần tử $g$** sao cho:
$$
\{ g^1, g^2, g^3, \ldots, g^{p^n - 1} \} = \mathbb{F}_{p^n}^\times
$$

Tức là, **mọi phần tử khác 0 trong trường đều có thể được biểu diễn dưới dạng một lũy thừa của $g$**.\
✅ Nói cách khác: Nhóm nhân $\mathbb{F}_{p^n}^\times$ là *nhóm cyclic*, và $g$ là phần tử sinh của nhóm đó.

**Ví dụ đơn giản**: Với $\mathbb{F}_7$:\
Tập phần tử khác 0 là: $\{1, 2, 3, 4, 5, 6\}$\
Ta kiểm tra lũy thừa của 3:
$$3^1 = 3,\; 3^2 = 2,\; 3^3 = 6,\; 3^4 = 4,\; 3^5 = 5,\; 3^6 = 1 \pmod{7}$$
→ Tất cả 6 phần tử xuất hiện!  
→ $3$ là **phần tử sinh** của $\mathbb{F}_7^\times$.

---
**Với $\mathbb{F}_{2^8}$**, ta định nghĩa:
$$
\mathbb{F}_{2^8} = \mathbb{F}_2[x] / (x^8 + x^4 + x^3 + x + 1)
$$
Gọi $a$ là nghiệm của đa thức này, thì:
$$
a^8 = a^4 + a^3 + a + 1
$$

Khi đó, $a$ **thường được chọn làm phần tử sinh**,  
tức là mọi phần tử khác 0 của trường đều có thể viết thành $a^k$ với $0 \le k < 255$.
## **2. Lời giải cho bài toán**
### ***2.1. Mục đích bài toán***
Chương trình cho phép ta gửi một hoán vị `plainperm` (một bảng thay thế 8-bit), rồi chương trình tạo một **khóa ngẫu nhiên 64 byte** và xây hàm mã hóa `f(i)` bằng cách lặp: với mỗi byte khóa (ngoại trừ byte cuối) thực hiện `i = plainperm[i ^ k]`, cuối cùng trả `i ^ key[-1]`. Kết quả là `cipherperm`, hoán vị của 0..255 sau toàn bộ vòng.
    
Thách thức: Biết `plainperm` và biết `cipherperm` thu được, làm sao tìm **key** dài 64 byte?
    
Solution mô tả một chiến lược tấn công: *Thiết kế `plainperm` có cấu trúc đặc biệt để cho phép suy ra một phần lớn phép biến đổi là tuyến tính (trong trường $\mathbb{F}_{256}$), rồi chỉ cần dò các trường hợp nhỏ còn lại (vì vài vị trí bị “xáo” bởi các 3-cycle) để thu được khóa thực.*

### **Chú ý rằng bài toán đang tính toán trên trường mở rộng, không phải là trường hữu hạn. Tức là, chúng ta đang làm việc với toán đa thức, không phải là toán mod.**

### ***2.2. Ý tưởng mô hình hóa toán học***

## 1) Mô hình toán học — xem hoán vị như ánh xạ trên $\mathbb{F}_{256}$

-   Ta tưởng tượng 8-bit là trường hữu hạn $\mathbb{F}_{256}$ với phép cộng chính là XOR (điều này đúng: phép cộng trong trường biểu diễn bitwise tương đương xor). Có phép nhân trường chuẩn với một phần tử sinh $a$.
    
-   Xét ánh xạ tuyến tính dạng $f(x)=a x$ (hoặc tổng quát hơn $f(x)=a x + b$). Khi bạn **xét chuỗi nhiều lần** các thao tác loại này cộng với thao tác XOR với các byte khóa, các ánh xạ tuyến tính sẽ cộng dồn theo cách rất có thể biểu diễn đóng gói bằng công thức lũy thừa.
    

## 2) Nếu mọi thứ đều tuyến tính → thông tin mất mát

-   Giả sử thay thế `plainperm` là chính ánh xạ $x \mapsto f(x)=a x$ (hoặc `f(x)=a x + b`) — tức là mỗi lần qua hàng substitution thực ra là nhân cho $a$ (và có thể cộng thêm một hằng).
    
-   Khi kết hợp 63 vòng substitution + các phép XOR byte khóa giữa các vòng, sau cùng ta thu được một công thức dạng:
    
    $$
    \text{enc}(x) = a^{63} x + \sum_{i=0}^{63} a^{63-i} k_i
    $$
    
    (đây là kết quả của việc hợp thành các ánh xạ tuyến tính và addition).
    
-   **Quan trọng:** kết quả chỉ phụ thuộc vào $a^{63} x$ và một **tổng cố định** $S=\sum a^{63-i} k_i$. Khi biết `cipherperm` ta có thể đo được $a^{63}$ (nếu biết cách tương ứng) và **S**, nhưng *không đủ* để tách từng byte $k_i$. Nói cách khác có một tập hợp vô số khóa cho cùng một $S$ — tức là không thể phục hồi khóa duy nhất nếu toàn bộ hệ thống là tuyến tính.
    

## 3) Thêm nhiễu cục bộ (3-cycle) — làm lộ thêm thông tin

-   Ý tưởng: làm cho `plainperm` không hoàn toàn tuyến tính; chỉ thay đổi rất ít điểm (chẳng hạn bằng cách ghép thêm vài 3-cycles như $g=(0,1,255)$). Một 3-cycle chỉ đổi chỗ 3 giá trị — tức là ảnh hưởng rất ít đầu vào.
    
-   Nếu ta viết `plainperm = f \circ g` với `f` tuyến tính và `g` là vài 3-cycle (chỉ thay đổi trên một số lượng nhỏ điểm), khi hợp thành 64 lần tương tự, ta thu được:
    
    $$
    f_1\circ g_1 \circ f_2\circ \dots \circ g_{63}\circ f_{64} = g_1' \circ g_2' \circ \dots \circ g_{63}' \circ F
    $$
    
    với $F$ là ánh xạ tuyến tính lớn (ví dụ $F(x)=a^{63} x + b$) và mỗi $g_i'$ là các 3-cycle tương ứng nhưng số lượng điểm bị “thay đổi” bởi tất cả các $g_i'$ là nhỏ (ở ví dụ là tối đa 192 điểm, vì 63 \* 3 ≤ 192 — ý nghĩa: chỉ ~192 giá trị đầu vào bị ảnh hưởng khác biệt so với ánh xạ tuyến tính F).
    
-   Kết quả: trên **phần lớn** (ở đây là 64 điểm còn lại) giá trị `cipherperm` chính là ảnh của $F$ tại x. Ta có thể dùng những đầu vào không bị ảnh hưởng (những “điểm sạch”) để suy ra $F$ hoàn chỉnh (hai tham số $a^{63}$ và $b$).
    

## 4) Từ $F$ tới khóa: thu hẹp không gian tìm kiếm

-   Khi biết $F(x) = a^{63} x + b$ (tức ta biết một ánh xạ tuyến tính đại diện phần lớn quá trình), ta có một phương trình liên hệ giữa các byte khóa $k_i$: chính công thức tổng $S=\sum a^{63-i} k_i$ xuất hiện trong biểu thức.
    
-   Vì các 3-cycle chỉ thay đổi một tập nhỏ các giá trị, ta có thể lọc ra những đầu vào bị thay đổi và chỉ dùng những đầu vào “không bị ảnh hưởng” để đo $F$. Sau khi biết $F$, ta liệt kê (enumerate) các tổ hợp $k_i$ có thể cho cùng $F$ và kiểm tra tương thích với những điểm bị thay đổi do 3-cycles để chọn khóa thực.
    
-   Để làm cho bài toán dễ hơn nữa, người giải chọn `plainperm` theo cách đặc biệt: mỗi 3-cycle **mở rộng** chu trình (cycle) mà không tách nhỏ chu trình. Vì thế các 3-cycle này không chồng lấn tập con những điểm mà $F$ gán — điều này giúp tách rõ điểm nào bị ảnh hưởng và điểm nào không, giúp loại bỏ nhiều khả năng khóa giả.
    

## 5) Kết luận về hiệu suất / xác suất

-   Sau khi áp dụng chiến lược này, bài toán bị thu nhỏ: ta chỉ cần tìm trong một không gian khả dĩ nhỏ hơn nhiều (vì biết $F$ hạn chế tập khóa tương thích).
    
-   Solution nói rằng xác suất trung bình thành công (với cách chọn `plainperm` theo chiến lược nói trên và dò lặp) là xấp xỉ **1 trên 60** — tức là nếu lặp vài lần (hoặc thử vài lựa chọn) sẽ có xác suất tốt tìm đúng key. (Con số 60 ở đây đến từ phân tích số lượng khả năng còn lại sau khi loại trừ bằng $F$ và bằng các điều kiện tại các điểm bị ảnh hưởng.)
    

---

# Liên hệ trực tiếp với code bạn đưa

-   `plainperm` do bạn nhập: đây chính là hoán vị thay thế mà attacker được phép tự thiết kế — điều quan trọng để xây chiến lược tấn công phía trên (attacker có thể chọn `plainperm` có dạng f∘g như mô tả).
    
-   `key = os.urandom(64)`: khóa 64 byte, mỗi byte được dùng như `k` trong vòng lặp; do đó có đúng 63 vòng gọi `plainperm[i ^ k]` (vì vòng for chạy `key[:-1]`) và byte cuối cùng `key[-1]` chỉ XOR ở cuối.
    
-   `cipherperm = bytes(map(f, range(256)))`: chương trình trả về hoán vị kết quả — đây là thông tin mà attacker quan sát được sau khi gửi `plainperm`.
    
-   Từ `cipherperm` và `plainperm`, attacker theo solution chọn/thiết kế `plainperm` sao cho hầu hết ánh xạ là tuyến tính (F) và gồm một số 3-cycle nhỏ; sau đó:
    
    1.  Tìm những x mà output khớp với dạng tuyến tính → suy ra F.
        
    2.  Dùng F để rút gọn không gian khóa khả dĩ.
        
    3.  Dò (enumerate) những khả năng còn lại và kiểm tra bằng toàn bộ `cipherperm` để xác định `key` đúng.
        
-   Vì key thực là 64 byte ngẫu nhiên, thuật toán tấn công tận dụng quyền chọn `plainperm` để giảm độ phức tạp tìm key (không phải brute-force toàn bộ 2^512).
    

---

# Ví dụ minh hoạ cực đơn giản (ý tưởng)

-   Giả sử chỉ có 3 vòng (thay vì 63) và `f(x)=a x` (tuyến tính), ta sẽ có: `enc(x)=a^3 x + a^2 k0 + a^1 k1 + a^0 k2`. Nếu `plainperm` hoàn toàn là f, ta chỉ thấy `a^3` và tổng cố định $S$ — không thể tách k0,k1,k2.
    
-   Nếu ta thay đổi `plainperm` chỉ tại các điểm {0,1,255}, nghĩa là khi input ∈ {0,1,255} thì ánh xạ khác; còn 253 giá trị khác theo đúng công thức tuyến tính. Ta dùng 253 giá trị để giải ra `a^3` và $S$. Sau đó chỉ cần thử vài khả năng cho các k\_i sao cho phù hợp với 3 xuất ra khác biệt — không còn nhiều khả năng nữa.
    

---

# Tóm tắt gọn

-   Nếu substitution hoàn toàn tuyến tính thì ta chỉ nhận được một tổng cố định của các byte khóa → không thể phục hồi key duy nhất.
    
-   Bằng cách thêm *một số rất nhỏ* các 3-cycle (chỉ thay đổi vài đầu vào), ta giữ được phần lớn ánh xạ tuyến tính $F$ có thể suy ra từ `cipherperm`.
    
-   Sau khi biết $F$, ta giảm mạnh không gian khả dĩ của khóa, rồi liệt kê các khả năng nhỏ còn lại và kiểm tra với những điểm bị thay đổi để chọn đúng key.
    
-   Chiến lược này tận dụng **quyền chọn `plainperm`** (điều mà code cho phép attacker làm) để biến bài toán tưởng chừng brute-force rất lớn trở nên khả thi — với xác suất thành công ~1/60 theo phân tích của tác giả.