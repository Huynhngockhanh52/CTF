# 🧠 Giải thích dễ hiểu về Solution — BEAM & Alter Ego

## 1️⃣ Bối cảnh
Bài này xoay quanh **đường cong elliptic** và **isogeny**, một phép biến đổi đặc biệt giữa các đường cong elliptic được dùng trong mật mã học (như CSIDH, SIDH, SQISign, v.v.).

Ta có một đường cong $ E $ định nghĩa trên trường mở rộng $ \mathbb{F}_{p^2} $ (nói nôm na là "phiên bản phức" của một trường số học hữu hạn).

Mỗi điểm $ G $ trên $ E(\mathbb{F}_{p^2}) $ có thể **tách thành hai phần độc lập**:

$$
G = P + Q
$$

- $ P \in E(\mathbb{F}_p) $: phần “thật”, sống trong trường con.  
- $ Q $: phần “ảo”, nằm trên **twist** của $ E $.

### 💡 Ví dụ hình dung
Hãy tưởng tượng:
- $ P $ là **bóng của điểm G trên mặt đất**,  
- $ Q $ là **phần phản chiếu của nó qua gương**.

Khi ta di chuyển $ G $, cả hai phần $ P $ và $ Q $ cùng thay đổi, nhưng **độc lập với nhau**.  

---

## 2️⃣ l-isogeny là gì?

Một **isogeny** là **một phép biến đổi giữa hai đường cong elliptic**:

$$
\phi: E \to E'
$$

- Đây là **hàm nhân học** (group homomorphism), nghĩa là nó bảo toàn phép cộng điểm.  
- **l-isogeny** (đọc là “ell-isogeny”) là isogeny có **nhân (kernel)** là nhóm gồm **l điểm**.  
  ⇒ Hiểu đơn giản: nó "chia" đường cong theo một **nhân tử nguyên tố $ l $**.

Khi ta áp dụng một $ l $-isogeny, ta đang:
- “nén” một phần của đường cong lại (giảm bậc của nhóm con tương ứng).  
- “bẻ hướng” sang một đường cong khác $ E' $.  

---

## 3️⃣ Giảm bậc của P hoặc Q

Vì $ G = P + Q $, nên khi ta áp dụng một **l-isogeny**:

$$
\phi_l(G) = \phi_l(P) + \phi_l(Q)
$$

Nhưng tùy vào **hướng của isogeny**, nó sẽ ảnh hưởng đến **P hoặc Q**:

| Dấu trong `alice_priv` | Ảnh hưởng | Giải thích |
|--------------------------|------------|-------------|
| `+l` (dương) | giảm bậc của **P** | isogeny "hướng về" phần thật $ E(\mathbb{F}_p) $ |
| `-l` (âm) | giảm bậc của **Q** | isogeny "hướng về" phần twist |

👉 Vì vậy, “giảm bậc” nghĩa là **chia nhỏ nhóm chứa P hoặc Q**.  
Ví dụ:
- Nếu $ P $ có bậc $ 33 $ và ta áp dụng $ 3 $-isogeny vào phần $ P $,  
  thì bậc mới của $ P' $ chỉ còn $ 11 $.

---

## 4️⃣ Khai thác: Cách đoán dấu của `alice_priv`

Attacker có thể **quan sát hiệu ứng** của phép biến đổi để đoán xem bước đó làm giảm $ P $ hay $ Q $.

Quy trình:

1. Gửi thử các giá trị **-1, -1, -1, …** (nghĩa là chọn hướng âm).  
2. Sau mỗi bước, kiểm tra xem phần nào của $ G $ (tức $ P $ hay $ Q $) bị thay đổi mạnh.  
   - Nếu **P** giảm bậc → hướng thật là **dương**.  
   - Nếu **Q** giảm bậc → hướng thật là **âm**.

Lặp lại quá trình này cho từng phần tử trong `alice_priv`,  
ta **suy ra toàn bộ dấu hiệu chính xác** của private key.

> 🔍 Giống như đi trong mê cung, mỗi “bước” (l-isogeny) có thể đi sang trái hoặc sang phải,  
> và ta chỉ cần nhìn xem “lối nào nhỏ đi” để biết hướng đúng.

---

## 5️⃣ Bước cuối: tạo alter ego

Khi chương trình hỏi:

```python
alter_ego = list(map(int, input('ready?! here is the "alter ego" >').split(", ")))
```

thì ta phải nhập một private key khác (`alter_ego`) sao cho nó **dẫn đến cùng đường cong** như Alice.  

Do isogeny có **cấu trúc đối xứng**, nên nếu ta đi theo đường cong đó nhưng **đảo hướng hoặc dịch bước**,  
ta vẫn đến **cùng điểm cuối** trong cây isogeny.

### 💡 Cụ thể:
Nếu ta có
```python
alice_priv = [a1, a2, a3, ..., an]
```
thì ta có thể chọn
```python
alter_ego = [a1 - 36, a2 - 36, a3 - 36, ..., an - 36]
```

Vì việc trừ đi một hằng số chỉ làm **dịch vị trí trên cây isogeny**,  
mà **không thay đổi đường cong kết quả cuối cùng**.  

Khi kiểm tra:
```python
if _alter_ego_E1.curve().a2() == _alice_E1.curve().a2():
```
nó khớp → FLAG hiện ra 🎉

---

## 6️⃣ Minh họa logic (bằng sơ đồ ASCII)

```
E0 ---+--> E1 ---+--> E2 ---+--> E3
       |           |           |
      +l          -l          +l
      |           |           |
      V           V           V
  giảm P      giảm Q      giảm P
```

Mỗi bước `+l` hoặc `-l` sẽ dẫn đến một nhánh khác trong cây.  
Nếu ta chọn cùng đường đi (hoặc đối xứng tương ứng),  
ta đến **cùng một E cuối** → FLAG xuất hiện.

---

## 7️⃣ Tóm tắt toàn bộ

| Thành phần | Ý nghĩa |
|-------------|----------|
| $ G = P + Q $ | Mỗi điểm là tổng của phần thật (E) và phần phản chiếu (twist). |
| $ l $-isogeny | Phép biến đổi giảm bậc một trong hai phần $ P $ hoặc $ Q $. |
| Dấu trong `alice_priv` | Cho biết hướng biến đổi (về P hay về Q). |
| Cách khai thác | Thử nhiều hướng (-1), xem phần nào thay đổi để đoán dấu. |
| Alter ego | Một private khác nhưng sinh cùng đường cong cuối. |
| Cách tạo | Trừ đi hằng số hoặc đảo dấu tất cả phần tử trong `alice_priv`. |

---

## 🎯 Kết luận

Ý tưởng chính là:  
> Bằng cách quan sát xem **phần nào của điểm bị chia nhỏ (P hay Q)** sau mỗi bước isogeny,  
> ta có thể khôi phục **hướng đi (dấu)** trong private key của Alice.  
> Sau đó chỉ cần tạo một “bản sao đối xứng” (alter ego) để đi đến cùng đích.
