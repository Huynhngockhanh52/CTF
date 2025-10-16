# **🌀 Alter-Ego — Writeups**

## **1. Hiểu đề bài**

Bài này thuộc dạng **isogeny-based cryptography** (giống như CSIDH). Nhiệm vụ là **tìm ra một khóa bí mật "âm"** tương đương với khóa "dương" mà server giữ.\
Cụ thể:
- Server có một **secret key** `sk`, một vector gồm các hệ số trong khoảng `[12, 27]`.  
  → Ví dụ: `sk = [13, 15, 18, 26, ...]`

- Ta cần tìm một khóa khác `sk'` có **hệ số trong [-30, -1]**, sao cho hai khóa này **tạo ra cùng một đường cong elliptic** sau khi thực hiện phép “group action” (phương thức `group_action`).

Ta chỉ có thể tương tác với server qua **oracle**, theo đó, phương thức `BEAM()` cho phép:
- Mỗi lần gọi, nó sẽ:
  1. Lấy một đường cong hiện tại (hoặc `E0` ban đầu).
  2. Áp dụng phép biến đổi theo khóa bí mật `sk'`.
  3. Trả về đường cong kết quả (nhưng không nói ta đã áp dụng cái gì).

Và ta chỉ được **gọi oracle 39 lần** (ứng với 39 primes trong `ells`).

---

## **2. Ý tưởng phân tích và đơn giản hóa**

### *🧩 2.a. Nếu biết `sk` sẵn*

Nếu ta đã biết khóa bí mật `sk = [12, 27, ...]`, thì có thể **chuyển nó thành khóa "âm" tương đương** bằng cách trừ cho một vector có tất cả phần tử bằng 30:
```text
sk' = sk - [30, 30, 30, ...]
```
Do trong CSIDH, cộng/trừ cùng một hằng cho tất cả hệ số (theo hướng đồng nhất) sẽ không thay đổi kết quả phép nhóm.

---

### *🧠 2.b. Nếu có 2 điểm ngẫu nhiên*

Giả sử oracle cho ta **hình ảnh của 2 điểm ngẫu nhiên** thay vì 1 điểm, thì ta có thể “tách riêng” ảnh hưởng của từng prime $\mathbb{ℓ}_i$: `ℓ_i`.

Vì mỗi prime `ℓ_i` trong danh sách `ells` tương ứng với một **bậc isogeny**,  
nên việc quan sát cách mà mỗi điểm biến đổi có thể giúp ta phát hiện **khi nào hệ số cho `ℓ_i` = 0**.

Cách làm (giả lập tư duy):
- Ban đầu, `sk` có các hệ số dương (ví dụ `[15, 20, ...]`).
- Sau mỗi lần gọi oracle, ta được phép “thêm” một vector nhỏ `[-1, 0, 1]` vào `sk`.
- Nếu ta liên tục **trừ 1 vào tất cả hệ số sau mỗi lần**, thì sau một số lần nhất định, từng hệ số sẽ lần lượt đạt 0 → Tại thời điểm đó, ta có thể **phát hiện ra vị trí và giá trị gốc** của hệ số đó.

Như vậy, chỉ cần quan sát **tại lần nào hệ số = 0**, ta suy ra giá trị gốc của hệ số `sk[i]`.

---

### *3. Giải thực tế*

Vấn đề là oracle **chỉ cho 1 điểm duy nhất**, vì vậy ta không thể dùng cách “so sánh hai điểm”. Nhưng có một quan sát cực kỳ quan trọng (được phát hiện khi thử nghiệm bằng Sage):

> Nếu hệ số `ℓ_i ≥ 1`, thì ảnh của điểm ngẫu nhiên sau khi biến đổi **luôn có dạng `(x, i·y)`**, với `x, y ∈ 𝔽_p`.

Ngược lại, nếu hệ số ≤ 0, thì ảnh này **không có dạng đó**.

---

### *4. Cách khai thác thực tế*

Ta có thể dựa vào quan sát này để phát hiện khi nào hệ số chuyển từ dương → 0:

1. **Khởi đầu:**  
   - Lấy khóa `sk` chưa biết (ẩn).  
   - Bắt đầu từ `E0`.

2. **Lặp 39 lần:**  
   - Gửi yêu cầu đến oracle.  
     Mỗi lần oracle chạy, nó biến đổi theo `sk'` hiện tại.  
   - Sau đó, **cập nhật `sk' = sk' + [-1, -1, ..., -1]`**.  
   - Quan sát xem đầu ra (điểm ảnh) có dạng `(x, i·y)` không.  
     - Nếu **có dạng đó**, hệ số vẫn ≥ 1.  
     - Nếu **mất dạng đó**, tức là đã giảm đến 0.

3. **Ghi lại** lần đầu mà dạng `(x, i·y)` biến mất đối với từng `ℓ_i`.  
   Con số đó chính là giá trị ban đầu của hệ số `sk[i]`.

4. Khi đã có toàn bộ `sk`,  
   ta chỉ việc trừ `[30, ..., 30]` để có `sk'` thỏa mãn điều kiện nằm trong `[-30, -1]`.

---

### *5. Kết luận*

Toàn bộ quá trình tóm gọn lại như sau:

| Bước | Hành động | Ý nghĩa |
|------|------------|---------|
| 1 | Gọi oracle lần 1 với `sk` | Nhận ảnh đầu tiên |
| 2 | Mỗi lần tiếp theo trừ 1 vào mọi hệ số | Giảm dần giá trị `sk` |
| 3 | Quan sát khi nào điểm đầu ra không còn dạng `(x, i·y)` | Phát hiện hệ số = 0 |
| 4 | Ghi lại số lần đó | Chính là hệ số ban đầu |
| 5 | Tạo `sk' = sk - [30, ..., 30]` | Sinh ra “alter ego” âm |
| 6 | So sánh kết quả đường cong của `sk'` và `sk` | Nếu trùng → lấy cờ (`FLAG`) |