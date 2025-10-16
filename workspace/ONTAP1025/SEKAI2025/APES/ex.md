# 1. Giải thích từng phần của chương trình

```python
import os
FLAG = os.getenv("FLAG", "SEKAI{TESTFLAG}")

def play():
    plainperm = bytes.fromhex(input('Plainperm: '))
    assert sorted(plainperm) == list(range(256)), "Invalid permutation"

    key = os.urandom(64)
    def f(i):
        for k in key[:-1]:
            i = plainperm[i ^ k]
        return i ^ key[-1]

    cipherperm = bytes(map(f, range(256)))
    print(f'Cipherperm: {cipherperm.hex()}')
    print('Do you know my key?')
    return bytes.fromhex(input()) == key
```

-   `plainperm = bytes.fromhex(input(...))` — chương trình chờ bạn nhập một **permutation** (một hoán vị của 0..255) ở dạng hex; `assert sorted(plainperm) == list(range(256))` kiểm tra rằng đó đúng là hoán vị (mỗi giá trị 0..255 xuất hiện đúng một lần).
    
-   `key = os.urandom(64)` — chương trình sinh một `key` ngẫu nhiên 64 byte, chỉ server biết.
    
-   Hàm `f(i)` được định nghĩa bằng vòng lặp:
    
    -   Với mỗi byte `k` trong `key[:-1]` (tức là 63 byte đầu), làm `i = plainperm[i ^ k]`.
        
    -   Sau vòng lặp, trả `i ^ key[-1]` (xử lý XOR với byte cuối cùng).
        
    -   Kết quả là `f` là một hoán vị trên không gian 0..255 (tổ hợp các XOR và tra hoán vị vẫn là hoán vị).
        
-   `cipherperm = bytes(map(f, range(256)))` — chương trình áp dụng `f` cho từng giá trị 0..255, tạo ra một "cipher permutation" (hiển thị cho bạn ở dạng hex). Nói cách khác, chương trình tiết lộ hoán vị `f` (kết quả của việc kết hợp plainperm và key).
    
-   Cuối cùng chương trình hỏi: "Do you know my key?" — chờ bạn nhập key (hex). Nếu bạn nhập đúng key (bytes), chương trình in FLAG; nếu sai thì vòng lặp cho chạy lại.
    

Tóm tắt ngắn: bạn đưa vào một hoán vị `plainperm` (bạn có thể chọn), chương trình sinh `key` bí mật, tạo `cipherperm = f` (một hoán vị mới được in ra), rồi hỏi bạn có biết `key` hay không — nhiệm vụ của người tấn công là từ `plainperm` và `cipherperm` suy ra `key`.

# 2. Diễn giải toán học / cấu trúc hoán vị

Ta có không gian $X=\{0,\dots,255\}$. Với mỗi byte $k$ định nghĩa phép toán trên $X$:

-   $XOR_k(x) = x \oplus k$ (một hoán vị vì phép XOR là đảo được),
    
-   $S(x) = \text{plainperm}[x]$ (hoán vị cố định do bạn nhập).
    

Trong hàm `f`, mỗi bước `i = plainperm[i ^ k]` thực chất là áp dụng $S \circ XOR_k$. Với key là $[k_1,k_2,\dots,k_{64}]$ (một chuỗi 64 byte), ta có

$$
f = XOR_{k_{64}} \circ S \circ XOR_{k_{63}} \circ S \circ \cdots \circ XOR_{k_{1}}.
$$

(Chú ý thứ tự vì cách code làm: vòng lặp áp nhiều `S \circ XOR` rồi cuối cùng XOR với `k_last`.)

Vì các phép toán này đều là hoán vị, $f$ là một hoán vị biết được (vì chương trình in ra `cipherperm`). Người tấn công có hai hoán vị biết: $S$ (plainperm) và $f$ (cipherperm), còn bí mật là dãy các `XOR_k` xen kẽ với các $S$.

# 3. Tính khó / ý tưởng tấn công (mức cao)

-   Không có công thức tuyến tính đơn giản để tách các phép XOR và S vì chúng xen kẽ và XOR phụ thuộc vào byte $k$ khác nhau ở mỗi vòng. Với không gian 256 và khóa 64 byte, không thể brute-force toàn bộ không gian $256^{64}$.
    
-   Tuy nhiên, trong một số trường hợp đặc biệt (ví dụ key ngắn, hoặc plainperm có cấu trúc đặc biệt), có thể khai thác cấu trúc hoán vị / chu kỳ để rút ra thông tin về key. Trong thực tế CTF, người ta thường tìm:
    
    -   Các điểm cố định / chu kỳ của hoán vị,
        
    -   Dạng đồng hợp (conjugacy) giữa hoán vị: $f = X \circ S \circ X^{-1}$ dạng đơn giản là khi key chỉ có 1 byte hoặc khi có thể gom các bước lại.
        
    -   Các tấn công dựa trên group theory (nhóm các hoán vị) hoặc giải hệ phương trình rời rạc.
        
-   Nhưng **điều quan trọng**: chương trình in toàn bộ `cipherperm` — đó là một lượng dữ liệu lớn (256 giá trị). Tùy plainperm, đôi khi có thể suy ra từng byte key bằng cách phân tích ánh xạ các chu kỳ. Phân tích này có thể phức tạp và tùy thuộc vào plainperm.
    
-   Trong thực tế, nếu plainperm do bạn kiểm soát (người tấn công được phép chọn plainperm), thì có thể chọn plainperm để làm lộ key dễ hơn — đó là lỗ hổng: chương trình cho phép attacker đưa `plainperm` tùy ý. Vì thế thiết kế này có thể gặp lỗ hổng nếu attacker có thể chọn plainperm đặc biệt.
    

# 4) Ví dụ minh họa (thu nhỏ) — chạy thử và brute-force

Để minh họa cách hoạt động và cho thấy nguyên lý phục hồi key khi không gian nhỏ, mình đã làm một bản demo thu nhỏ:

-   Thu nhỏ "alphabet" từ 256 xuống N = 16 (phải để brute-force khả thi).
    
-   Dùng key có độ dài 3 (thay vì 64).
    
-   Sinh plainperm ngẫu nhiên, sinh key bí mật, in cipherperm = f(0..N-1).
    
-   Brute-force tất cả $N^{KEY\_LEN}$ khả năng để tìm key(s) phù hợp với cipherperm quan sát được.
    

Kết quả demo (đã chạy trong môi trường notebook và in ra) — ví dụ thực tế từ lần chạy:

-   `N = 16`
    
-   `plainperm` (một hoán vị ngẫu nhiên 0..15):  
    `[10, 14, 5, 1, 9, 2, 3, 11, 13, 7, 8, 4, 0, 6, 15, 12]`
    
-   `Secret key` (unknown): `[9, 4, 3]`
    
-   `Cipherperm` (f(i) với i = 0..15):  
    `[2, 4, 9, 3, 6, 10, 14, 7, 11, 12, 1, 13, 0, 5, 15, 8]`
    
-   Brute-force toàn bộ 4096 khả năng và tìm đúng 1 key khớp: `[[9, 4, 3]]` — tức là **khóa gốc đã được phục hồi** trong demo này.
    

(Đoạn code minh họa mà mình chạy đã hiển thị toàn bộ thông tin trên — bạn có thể thay đổi `N` và `KEY_LEN` để thử nghiệm.)

# 5) Kết luận và lời khuyên bảo mật / giải CTF

-   **Về bảo mật**: với 256 và key 64 byte, brute-force toàn bộ là không khả thi. Nhưng chương trình để attacker chọn `plainperm` là một điểm yếu: nếu attacker có thể lựa chọn plainperm, họ có thể chọn hoán vị có cấu trúc để giảm độ khó phục hồi key (ở các biến thể CTF, đó thường là điểm tấn công). Vì vậy, cho nhập trực tiếp plainperm từ attacker là không an toàn nếu bạn dùng cơ chế tương tự trong thực hệ thống.
    
-   **Về giải CTF**: cách tiếp cận thường là:
    
    -   Phân tích cấu trúc hoán vị (chu kỳ, điểm cố định).
        
    -   Tìm cách giảm chiều không gian: ví dụ nhóm hoán vị sinh bởi $S$ và các XOR có dạng cụ thể, hoặc khai thác việc key lặp lại, key ngắn, hay plainperm có dạng cho phép "triệt tiêu" một vài vòng.
        
    -   Thử các plainperm “đặc biệt” (nếu bạn có thể chọn plainperm) để tiết lộ key từng phần.
        
    -   Tìm yêu cầu phụ: chương trình cho biết `cipherperm` khi bạn nhập `plainperm` do bạn chọn — điều này cho phép bạn dùng nhiều lần với nhiều plainperm khác nhau để thu thập dữ liệu (nếu phiên bản thật cho ta làm nhiều lần), từ đó suy ra key.
        

---

Nếu bạn muốn, mình có thể:

-   (A) Chạy thêm ví dụ (tùy bạn chọn N, độ dài key) để bạn nhìn thêm các trường hợp.
    
-   (B) Giúp bạn phân tích một chiến lược cụ thể để tấn công biến thể 256/64 (theo hướng lý thuyết — ví dụ phân tích chu kỳ, phép đồng hợp), hoặc
    
-   (C) Nếu bạn đang làm bài CTF, gửi cho mình `plainperm` (hex) và `cipherperm` (hex) thực tế — mình sẽ cố gắng phân tích xem có cách rút ra một phần key nào hay không.
    

Bạn muốn mình thực hiện bước nào tiếp theo? (ví dụ: chạy thêm 1-2 demo, hoặc phân tích tấn công cho trường hợp bạn có thể chọn nhiều lần `plainperm`...)


### Mục đích tổng quát

Đoạn code tạo ra, cho mỗi vòng `i` (0..62), **tập các ánh xạ (nhỏ) có thể** mà vòng đó gây ra lên ba điểm kiểm tra `[0,1,255]` khi ta thử mọi `k0` khả dĩ. Mỗi phần tử của `possible_maps[i]` là một cặp `(k0, perm3)`:

-   `k0` — một ứng viên byte khóa cho vòng `i`
    
-   `perm3` — một hoán vị nhỏ (được tạo từ ba ảnh của `[0,1,255]` sau khi chia `a^i` và cộng `k0`), biểu diễn “cách vòng i dịch ba điểm kiểm tra”
    

Ý tưởng: sau khi thu được `possible_maps` cho mọi `i`, ta có thể thử kết hợp (compose) các hoán vị nhỏ này theo thứ tự để xem có tái tạo được `cipherperm` hay không — tức là dùng không gian các perm khả thi để dựng lại hoán vị tổng thể.

---

### Giải thích từng dòng (chú ý conversion kiểu trong Sage)

```python
possible_maps = [[] for _ in range(63)]
for i in range(63):
    a0 = a ** i
    ts = [F.from_integer(t)/a0 for t in [0, 1, 255]]
```

-   `a0 = a**i` : tách yếu tố nhân tuyến tính của vòng `i`.
    
-   `ts = [...]` : `ts` là 3 điểm tham chiếu **đã “chuẩn hoá”** (chia cho `a^i`) — tức là giá trị nguyên thủy trước khi nhân bởi `a^i`.
    
    -   (Lưu ý: với Givaro bạn sẽ dùng `F.fetch_int(t)` hoặc `F(t)` thay vì `from_integer`.)
        

```python
for k0 in possible_k0[i]:
        us = [u + k0 for u in ts]
```

-   Với mỗi `k0` khả thi cho vòng `i`, ta cộng `k0` vào từng `u` trong `ts`. `us` là ba giá trị trong field sau phép cộng — đây là **vị trí ảnh** của ba điểm kiểm tra nếu khóa vòng là `k0`.
    

```python
us = [x.to_integer() + 1 for x in us]
```

-   Chuyển mỗi phần tử field `x` thành số nguyên 0..255 rồi +1 để trở thành **index 1-based** (Sage `Permutation` mặc định dùng 1..n). Kết quả là một tuple 3 số trong 1..256.
    

```python
perm3 = Permutation([tuple(us)])
```

-   Tạo một **Permutation** từ **danh sách các cycle**; ở đây truyền `[(u1,u2,u3)]` nghĩa là hoán vị gồm **một cycle** `(u1 u2 u3)`.
    
    -   Kết quả `perm3` là hoán vị chỉ thay đổi 3 vị trí tương ứng với `us` theo cycle order.
        

```python
possible_maps[i].append((k0, perm3))
```

-   Lưu cặp `(k0, perm3)` vào danh sách ứng viên cho vòng `i`.
    

---

### Minh hoạ bằng ví dụ nhỏ (dễ theo dõi)

Giả sử dùng trường nhỏ GF(7) để minh họa ý tưởng (tính bằng tay):

-   Chọn `a = 2`, vòng `i = 1` ⇒ `a0 = 2`.
    
-   Điểm kiểm tra: `[0,1,6]` (tương ứng với `[0,1,255]` trong ví dụ thật).
    
-   Chuẩn hoá: `ts = [0/2, 1/2, 6/2]` trong GF(7) → `[0, 4, 3]` (vì 1/2 ≡ 4 mod7).
    
-   Giả sử `possible_k0[1]` chứa `k0` = 5 và 2.
    
    -   Với `k0=5`: `us = [0+5, 4+5, 3+5] = [5, 2, 1]`.
        
        -   Chuyển thành 1-based (nếu field mã hoá 0..6): `[6,3,2]`.
            
        -   `perm3 = (6 3 2)` — hoán vị chỉ ảnh hưởng 3 vị trí.
            
    -   Với `k0=2`: `us = [2,6,5]` → `[3,7,6]` (tuỳ mapping) → perm khác.
        

Bạn lưu hai cặp `(5, permA)`, `(2, permB)` vào `possible_maps[1]`. Sau khi làm cho mọi `i`, bạn có tập các perm nhỏ khả thi cho từng vòng — sau đó thử compose chọn một perm cho mỗi vòng để xem có khớp `cipherperm` không (hoặc dùng pruning/constraint solving).

---

### Vì sao làm như vậy — ý nghĩa thực tế

-   **Chia nhỏ không gian tìm kiếm.** Thay vì thử tất cả 256^63 khóa, ta thử các perm nhỏ chỉ trên 3 điểm, số lượng ứng viên per round đã được lọc trước (`possible_k0[i]`).
    
-   **Tách thành bài toán perm composition.** Mỗi vòng ứng viên biểu diễn như một 3-cycle cụ thể; compose các 3-cycle này (cộng với backbone tuyến tính F) sẽ tái tạo cipherperm nếu chọn đúng `k0` cho mỗi vòng.
    
-   **Cho phép pruning mạnh.** Nếu khi compose một số perm đầu tiên đã mâu thuẫn với cipherperm (vị trí nào đó), ta có thể cắt nhánh.
    

---

### Lưu ý kỹ thuật (Sage/Givaro)

-   `F.from_integer` có thể không tồn tại trong backend Givaro. Dùng thay:
    
    -   `F.fetch_int(t)` hoặc đơn giản `F(t)` để tạo phần tử từ integer.
        
-   `x.to_integer()` cũng không tồn tại cho phần tử Givaro. Thay thế bằng:
    
    -   `poly = x.polynomial(); int_value = sum(c * 2**i for i,c in enumerate(poly.list()))`
        
    -   Hoặc nếu bạn tạo field với `type='classic'`, dùng `x.integer_representation()` trực tiếp.
        
-   Khi xây `us` để feed vào `Permutation`, nhớ đảm bảo chúng là **1-based Python ints** (không phải Sage Integer gây lỗi với `Permutation`).
    

---

### Đề xuất mã an toàn hơn (gợi ý sửa)

```python
possible_maps = [[] for _ in range(63)]
for i in range(63):
    a0 = a ** i
    # dùng F(t) để tránh lỗi from_integer
    ts = [F(t)/a0 for t in (0,1,255)]
    for k0 in possible_k0[i]:
        us_field = [u + k0 for u in ts]
        # chuyển sang int 0..255 một cách an toàn (Givaro -> polynomial -> int)
        us_int = []
        for x in us_field:
            poly = x.polynomial()
            val = sum(int(c) * (1 << idx) for idx, c in enumerate(poly.list()))
            us_int.append(val + 1)   # +1 cho 1-based
        perm3 = Permutation([tuple(us_int)])
        possible_maps[i].append((k0, perm3))
```

---

### Tóm tắt

-   **Mục đích:** cho mỗi vòng i và ứng viên `k0`, xây hoán vị nhỏ `perm3` biểu diễn ảnh của 3 điểm thử; lưu vào `possible_maps[i]`.
    
-   **Sử dụng:** sau đó dùng tập `possible_maps` này để thử các phối hợp perm (compose) nhằm khôi phục hoán vị/chìa khóa toàn cục.
    
-   **Chú ý:** conversions giữa Sage Integer / Python int / field element cần xử lý thận trọng (dùng `F(t)` / `fetch_int` / `polynomial()` tùy backend).
    

Nếu bạn muốn, mình có thể:

-   Viết hàm **compose thử** dùng `possible_maps` để tìm tổ hợp phù hợp với `cipherperm`, hoặc
    
-   Viết đoạn code **chạy thật** trên Sage theo backend của bạn (mình sẽ dùng `polynomial()` conversion cho Givaro) để bạn chạy trực tiếp. Bạn muốn mình làm cái nào?