# **CSIDH (Lý thuyết tóm tắt)**

## **1. Ý tưởng tổng quát**
***CSIDH (Commutative Supersingular Isogeny Diffie–Hellman)*** là một giao thức mật mã dựa trên isogeny giữa đường cong elliptic supersingular trên trường hữu hạn. Mục tiêu là xây dựng một cơ chế tương đương Diffie–Hellman nhưng dùng cấu trúc lớp (class group) của một order trong một trường đại số nghiệm tưởng tượng, kết quả là một hành động nhóm giao hoán (commutative group action) lên tập các đường cong supersingular được định danh bởi j-invariant. 

Điểm quan trọng:
- **Group action:** Secret tác động lên đường cong công khai bằng một chuỗi isogenies có các bậc nhỏ,  kết quả là đường cong mới (public key của người sở hữu secret). Tương tự như Diffie-Hellman: nNu Alice có `a` và Bob có `b`, thì `a·(b·E0) = b·(a·E0)`.
- **Public key**: Một đường cong (thường thể hiện bằng j-invariant).
- **Secret key**: Một phần tử của một nhóm abelian (thường biểu diễn bằng vector các chỉ số nguyên nhỏ).
---

## **2. Nền tảng toán học**
### *2.1 Đường cong elliptic và isogenies*
- **Đường cong elliptic** $E$ qua trường hữu hạn $\mathbb{F}_p$ có tập điểm $E(\mathbb{F}_{p^2})$.
- Một **isogeny** $\phi : E \to E'$ là một morphism nhóm (hàm đồng cấu nhóm) có **kernel** (một subgroup hữu hạn). Độ (**degree**) của isogeny thường là kích thước của kernel.
- Composition các isogenies tương đương với phép nhân các lý tưởng tương ứng; các isogenies tạo thành một **đồ thị isogeny (isogeny graph)** giữa các đường cong.

---

### *2.2. Supersingular curves*
- **Supersingular elliptic curves** có cấu trúc *endomorphism ring* phức tạp hơn so với *ordinary curves*;  tuy nhiên khi xét trên $\mathbb{F}_p$, tập các *j-invariant* supersingular là hữu hạn và có các isogenies giữa chúng.
- Trong **CSIDH**, thường chọn các đường cong supersingular định nghĩa trên $\mathbb{F}_p$ (để không cần mở rộng trường lớn) sao cho **group action** có thể định nghĩa trên cùng một tập *isomorphism classes*.

---

### *2.3. Class group action (ý tưởng chính)*
- Có một **order** $\mathcal{O}$ (ví dụ một order trong một trường tưởng tượng) có **ideal class group** $Cl(\mathcal{O})$.
- Thành phần của $Cl(\mathcal{O})$ tác động lên các *isomorphism class* của các đường cong với cấu trúc $\mathcal{O}$-module (về mặt trực quan: “lấy đường cong và áp ideal” để sinh ra đường cong mới).
- Hành động này là **giao hoán (commutative)**, nên có thể dùng cho Diffie–Hellman.

---

### *2.4. Biểu diễn secret keys*
- Thực tế, class group được sinh bởi các lớp tương ứng với các prime nhỏ $l_1, \ldots, l_k$. Một **secret key** được biểu diễn bằng vector:   
   $$
   a = (a_1, \ldots, a_k)
   $$
   trong một khoảng nhỏ (ví dụ $a_i \in [-B, B]$ hoặc $[12, 27]$ tùy triển khai).

- Tương ứng với vector $ a $ là phần tử của nhóm bằng tích  
   $$
   \prod_i [l_i]^{a_i}
   $$
   (lũy thừa lớp lý tưởng).

- Áp action này lên đường cong cơ sở $ E_0 $, ta nhận được đường cong
   $$
   E = a \cdot E_0
   $$
   —> Đó chính là **public key**.

---

### *2.5. Tại sao chọn $p$ sao cho $p+1$ chia hết bởi các prime nhỏ?*

- Nếu $ p $ được chọn sao cho $ p+1 $ có nhiều thành phần nguyên tố nhỏ $ l_i $,thì điểm của $ E(\mathbb{F}_p) $ hoặc $ E(\mathbb{F}_{p^2}) $ có cấu trúc chứa các chuỗi cyclic tương ứng, cho phép dễ dàng xây dựng **isogenies bậc $l_i$** (kernel là subgroup bậc $ l_i $).
- Điều này cho phép triển khai action bằng cách thực hiện **nhiều isogenies bậc nhỏ nối tiếp** thay vì một isogeny lớn một lần, đây là điểm **thực tiễn quan trọng của CSIDH (hiệu năng)**.
---

## **3. Thuật toán cơ bản**

### *3.1. Chọn tham số:*

- Một prime $p$ đặc biệt (thỏa điều kiện về phân tích $p+1$ thành tích các prime nhỏ).
- Tập các prime $L = \{l_1, \dots, l_k\}$ chia hết $p+1$.
- Một đường cong cơ sở supersingular $E_0$ trên $\mathbb{F}_p$.

### *3.2. Secret key generation:*

- Chọn vector $a = (a_1, \dots, a_k)$ với mỗi $a_i$ trong một đoạn giới hạn (ví dụ $[-B, B]$ hoặc $[12,27]$ trong bài toán).
- Secret là $a$.

### *3.3. Action / Public key computation:*

- Để tính $E = a \cdot E_0$, thực hiện với mỗi prime $l_i$ lặp lại $a_i$ lần một isogeny bậc $l_i$ (cách hiện thực thực tế có nhiều tối ưu).
- Trả về j-invariant của $E$ (hoặc một biểu diễn chuẩn hoá khác) làm public key.

### *3.4. Diffie–Hellman style:*

- Alice chọn $a$, Bob chọn $b$. Alice gửi $E_A = a\cdot E_0$, Bob gửi $E_B = b\cdot E_0$.
- Alice computes $a\cdot E_B = a\cdot(b\cdot E_0)$.
- Bob computes $b\cdot E_A = b\cdot(a\cdot E_0)$.
- Vì action giao hoán, $a\cdot(b\cdot E_0) = b\cdot(a\cdot E_0)$ là cùng một đường cong — đó là secret chung.

---

## **4. Biểu diễn thực thi (ghi chú kỹ thuật)**

- **Thực hiện isogenies bậc nhỏ:** dùng Vélu formulas hoặc các công thức x-only để tính isogenies degree = small prime.
- **Chuẩn hoá public key:** thường chỉ gửi j-invariant (một phần tử trong $\mathbb{F}_p$) — đơn giản, không cần điểm cụ thể.
- **Giới hạn range của $a_i$:** nhỏ để việc tính toán hiệu quả; nhưng phải đủ lớn để đảm bảo an ninh (khó bị brute-force từng hệ số).

---

## **5. Bảo mật — giả định và tấn công**

### *5.1. Bài toán lõi (hard problem):*

- Từ $E_0$ và $E = a\cdot E_0$, tìm $a$ (hoặc một phần tử nhóm tương đương) là bài toán khó: tương đương với tìm một đường đi (isogeny path) trong đồ thị isogeny giữa hai nút (đường cong). Trong CSIDH, vì action là class group action, bài toán tương đương với “discrete logarithm” trong không gian lớp — nhiều dạng tấn công nhưng không có thuật toán polynomial được biết.

### *5.2. Các tấn công thực tiễn:*

- **Meet-in-the-middle / baby-step giant-step:** có chi phí bộ nhớ/hàm phức tạp ~ $O(N)$ với $N$ kích thước không gian keys.
- **Tấn công dựa trên cấu trúc:** khai thác properties của class group, hoặc các phương pháp tìm đường trong đồ thị isogeny (claw finding).
- **Các tấn công phân tích thời gian/side-channel:** triển khai cần cẩn thận.

### *5.3. So sánh với SIDH (và các biến thể):*

- SIDH/SIKE dùng đường cong supersingular nhưng action **không giao hoán** (non-commutative structure), và có thêm điểm công khai (points of known order) — điều này dẫn tới những tấn công khác (ví dụ tấn công của Castryck–Decru vào SIKE).
- CSIDH dùng class group action (commutative), tránh các lỗ hổng liên quan tới điểm công khai, nhưng có các thách thức riêng về lựa chọn tham số và tấn công dựa trên decomposition của secret vector.

---

## **6. Ưu và nhược điểm của CSIDH**

**Ưu:**

- Giao hoán → thích hợp cho Diffie–Hellman.
- Public key nhỏ (j-invariant).
- Cấu trúc phù hợp cho một số ứng dụng như key exchange không tương tác.

**Nhược:**

- Hiệu năng chậm hơn nhiều so với ECC truyền thống, mặc dù nhanh hơn SIDH ở một số phép tính.
- Biểu diễn secret phải cân nhắc để đảm bảo an toàn.
- Bảo mật dựa trên các giả định khó tính toán; nghiên cứu về tấn công liên tục tiến triển.
