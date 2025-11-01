# **Xem luồng bài toán đi:**

Bài toán này có tối đa 5 vòng. Đầu tiên, ta có các kỹ thuật được sử dụng như:
- AES_GCM, 
- ECDSA_256

### **1. Phân tích trò chơi**

#### ***1.1. Lựa chọn 1:***
- Xoay khóa $S_k$, dịch $idx \rightarrow idx + 16 $

#### ***1.2. Lựa chọn 2:***
- Xoay khóa $F_k$, dịch $idx \rightarrow idx - 16 $

#### ***1.3. Lựa chọn 3:***
- Yêu cầu nhập một cipher dạng hex $enc^{(1)}_{msg}$
- Server sẽ kiểm tra tính toàn vẹn và giải mã thành $msg^{(1)}$, kiểm tra:
    + `admin = True` (12 byte) **không được** trong $msg$ 
    + `admin = False` **phải nằm** trong khoảng $msg[idx, idx+16]$
- Server ký $enc^{(1)}_{msg}$: 
$$
Sign(enc^{(1)}_{msg}) = sk.sign(enc^{(1)}_{msg}) = SIGN
$$

#### ***1.4. Lựa chọn 4:***
- Yêu cầu nhập một cipher dạng hex $enc^{(2)}_{msg}$
- Yêu cầu nhập chữ ký đã ký của server từ $enc^{(2)}_{msg}$
- FK sẽ kiểm tra tính toàn vẹn và giải mã thành $msg^{(2)}$, kiểm tra:
    + `admin = False` (13 byte) **không được** trong $msg$ 
    + `admin = True` **phải nằm** trong khoảng $msg[0, idx]$
- Nếu đúng in ra `flag`