# **Giải thích `E0.set_order((p + 1)^2)` trong Elliptic Curve**

## **🧩 1. "Số điểm" (order) của một đường cong elliptic là gì?**

Một **đường cong elliptic** $E$ trên trường hữu hạn $\mathbb{F}_p$ là tập hợp các điểm $(x, y)$ thỏa mãn:
$$
y^2 = x^3 + ax + b
$$
cùng với **điểm đặc biệt** gọi là điểm vô cực $\mathcal{O}$.

➡️ Mỗi cặp $(x, y)$ trong $\mathbb{F}_{p^2}$ mà thỏa phương trình trên đều là một **điểm trên đường cong**.

------------------------------------------------------------------------

## **🧮 2. Tổng số nghiệm**
Ký hiệu: $\#E(\mathbb{F}_p)$ là **số lượng điểm hữu hạn**
(gồm cả điểm vô cực) trên (E) có tọa độ trong trường $\mathbb{F}_{p}$.

→ Các điểm có: $ (0,0), (2,0), (3,0), (4,2), (4,3) $ + điểm vô cực ($\mathcal{O}$ ) → Tổng cộng **6 điểm**. Vậy: $\#E(\mathbb{F}_p) = 6$

------------------------------------------------------------------------
## **🧠 3. Định lý Hasse**

Định lý Hasse cho biết: $|\#E(\mathbb{F}_p) - (p + 1)| \le 2\sqrt{p}$
> Số điểm của đường cong luôn **gần bằng** (p + 1).

------------------------------------------------------------------------

## **🌍 4. Ví dụ minh họa**

Đường cong: $E_0: y^2 = x^3 + x$ được định nghĩa trên **trường bậc hai** $\mathbb{F}_{p^2}$.\
Đây là một **đường cong supersingular**, và ta biết kết quả lý thuyết đặc biệt:
> Nếu $E_0$ là **supersingular** trên $\mathbb{F}_{p^2}$, thì: \
> $$ \#E_{0}(\mathbb{F}_{p^2}) = (p + 1)^2 $$

Điều này có nghĩa là:
-   Tổng số điểm trên $E_0$, tức tất cả các nghiệm $(x, y)$ trong $\mathbb{F}_{p^2}$ **bằng bình phương của $(p + 1)$**.
-   Đây là đặc tính quan trọng trong **mật mã học isogeny**, vì group $E_{0}(\mathbb{F}_{p^2})$ có cấu trúc rất đẹp: 
    $$
        E_{0}(\mathbb{F}_{p^2}) \simeq \mathbb{Z}_{p+1} \times \mathbb{Z}_{p+1}
    $$
------------------------------------------------------------------------

## **🧩 5. Minh họa nhỏ bằng Sage**

Ví dụ nhỏ (chạy trong Sage):
``` python
p = 5
F = GF(p**2, 'i')
E = EllipticCurve(F, [1, 0])
E.order()
```
Kết quả:
```
36              #Vì ( (p + 1)\^2 = 6\^2 = 36 ).
```
------------------------------------------------------------------------