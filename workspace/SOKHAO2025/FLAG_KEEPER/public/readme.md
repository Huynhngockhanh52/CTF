# 1) Giải thích chi tiết từng dòng / từng khối

```python
from os import urandom  
from Crypto.Cipher import AES
from ecdsa import SigningKey, NIST384p
from hashlib import sha256
```

-   `from os import urandom`: nhập hàm `urandom(n)` để tạo `n` byte ngẫu nhiên an toàn (crypto-safe).
    
-   `from Crypto.Cipher import AES`: import module AES của PyCryptodome (AES implementation).
    
-   `from ecdsa import SigningKey, NIST384p`: import lớp tạo chữ ký ECDSA (SigningKey) và đường cong NIST P-384. `SigningKey.generate(curve=NIST384p)` tạo private key ECDSA trên đường cong P-384.
    
-   `from hashlib import sha256`: dùng hàm băm SHA-256 khi ký/verify (được truyền vào `sign`/`verify`).
    

---

```python
sk = SigningKey.generate(curve=NIST384p)
vk = sk.verifying_key
idx = 0
```

-   `sk`: private signing key (ECDSA) được tạo một lần khi script khởi động.
    
-   `vk`: verifying key (public key) tương ứng, dùng để kiểm tra chữ ký.
    
-   `idx = 0`: biến toàn cục (global) dùng như **offset** trong các kiểm tra chuỗi `admin = False` / `admin = True`. Giá trị `idx` sẽ được thay đổi bởi hai hàm `key_rotation()` trong hai lớp khác nhau.
    

> Ghi chú: `idx` được sử dụng như vị trí (offset) để kiểm tra substring trong các thông điệp đã giải mã; thay đổi `idx` thay đổi nơi chương trình tìm chuỗi `admin = False` hoặc `admin = True`.

---

### Class `Server`

```python
class Server:
    def __init__(self):
        self.key = urandom(16)
        pass
```

-   Lớp `Server` giữ một `self.key` — một khóa AES 16 byte (AES-128) được tạo ngẫu nhiên khi khởi tạo.
    
-   `pass` không làm gì (thừa).
    

```python
def key_rotation(self):
        global idx
        idx = (idx + 16) % 256
        self.key = urandom(16)
        print("current Server key: ", self.key.hex())
```

-   `global idx`: hàm thao tác biến toàn cục `idx`.
    
-   `idx = (idx + 16) % 256`: tăng `idx` lên 16 (mod 256). Tức mỗi lần quay khóa của `Server` thì `idx` tiến 16.
    
-   `self.key = urandom(16)`: sinh key AES mới cho server.
    
-   In ra key hiện tại (hex) — trong môi trường thật, in ra key như vậy là lộ secret, nhưng đây là challenge/CTF style.
    

```python
def decrypt(self, enc_msg):
        key = self.key
        nonce = enc_msg[:12]
        ct = enc_msg[12:-16]
        tag = enc_msg[-16:]

        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        msg = cipher.decrypt_and_verify(ct, tag)
        return msg
```

-   `decrypt(enc_msg)`: giải mã AES-GCM từ `enc_msg` theo format:
    
    -   `nonce = enc_msg[:12]` — lấy 12 byte nonce ở đầu. (AES-GCM thường dùng nonce/IV 12 byte).
        
    -   `ct = enc_msg[12:-16]` — ciphertext nằm sau nonce tới trước tag.
        
    -   `tag = enc_msg[-16:]` — 16-byte authentication tag ở cuối (AES-GCM tag thường 16 byte).
        
-   Tạo cipher AES GCM với `key` và `nonce`. `decrypt_and_verify(ct, tag)` thực hiện giải mã và verify tag; nếu tag sai, sẽ raise exception (`ValueError`/`KeyError` tùy lib).
    
-   Trả về `msg` (plaintext) nếu hợp lệ.
    

```python
def sign(self, enc_msg):
        msg = self.decrypt(enc_msg)
        if b'admin = True' in msg:
            raise ValueError("You are not allowed to sign admin messages!")
        
        if b'admin = False' not in msg[idx:idx+16]:
            raise ValueError("Invalid message format!")
        
        return sk.sign(enc_msg, hashfunc=sha256)
```

-   `sign(enc_msg)`:
    
    1.  **Giải mã** `enc_msg` bằng `self.decrypt` -> `msg`.
        
    2.  Nếu **bất kỳ** vị trí nào trong `msg` chứa substring `b'admin = True'` thì từ chối ký (raise ValueError).
        
    3.  Kiểm tra **đặc biệt**: substring `b'admin = False'` **phải nằm** chính xác trong đoạn `msg[idx:idx+16]` (đoạn 16 byte bắt đầu từ `idx`). Nếu không, raise `Invalid message format!`.
        
        -   Chú ý: `msg[idx:idx+16]` là slicing theo offset `idx` — tức mã giả định rằng trong plaintext, vùng bytes tại offset `idx` sẽ chứa `admin = False`.
            
        -   Vì `idx` được điều chỉnh bởi `Server.key_rotation()` và `FlagKeeper.key_rotation()`, nên hành vi kiểm tra này thay đổi theo các lần rotate.
            
    4.  Nếu qua cả hai kiểm tra, hàm trả về `sk.sign(enc_msg, hashfunc=sha256)` — tức **ký lên toàn bộ `enc_msg` (không phải plaintext)** bằng private key `sk`, với hash function SHA-256. Điều quan trọng: **ký dữ liệu đã mã hóa** (ciphertext + nonce + tag format) chứ không phải plaintext.
        

> Nhận xét: server ký `enc_msg` (ciphertext) chứ không ký plaintext. Kiểm tra nội dung (admin...) được thực hiện sau khi giải mã.

---

### Class `FlagKeeper`

```python
class FlagKeeper:
    def __init__(self, flag):
        self.flag = flag
        self.key = urandom(16)
```

-   `FlagKeeper` giữ `self.flag` (nội dung flag) và `self.key` — key AES 16 byte riêng biệt (không giống `Server.key`). Key này dùng để giải mã khi người dùng submit yêu cầu lấy flag.
    

```python
def key_rotation(self):
        global idx
        idx = (idx-16) % 256
        self.key = urandom(16)
        print("current FlagKeeper key: ", self.key.hex())
```

-   Khi FlagKeeper quay key, `idx` giảm 16 (mod 256). Vì vậy `Server.key_rotation()` tăng idx lên 16; `FlagKeeper.key_rotation()` giảm idx 16. Việc này cho thấy mỗi lần quay một trong hai, idx thay đổi — có thể dùng trong attack/logic để đồng bộ hóa vị trí kiểm tra `admin = False`/`admin = True`.
    

```python
def get_flag(self, enc_msg, signature):
        try:
            vk.verify(signature, enc_msg, hashfunc=sha256)
        except:
            raise ValueError("Invalid signature!")

        key = self.key
        nonce = enc_msg[:12]
        ct = enc_msg[12:-16]
        tag = enc_msg[-16:]
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        msg = cipher.decrypt_and_verify(ct, tag)
        if b'admin = True' in msg[:idx] and b'admin = False' not in msg:
            return self.flag
        else:
            return b'No flag for you!'
```

-   `get_flag(enc_msg, signature)` thực hiện:
    
    1.  **Verify chữ ký** `signature` trên `enc_msg` bằng public key `vk`. Nếu verify thất bại -> raise `Invalid signature!`.
        
    2.  Dùng **FlagKeeper.key** để giải mã `enc_msg` — chú ý: flagkeeper dùng key khác so với server.
        
    3.  Sau khi có plaintext `msg`, kiểm tra: **(A)** có `b'admin = True'` nằm trong `msg[:idx]` (tức trong phần từ đầu tới offset `idx`), **và** **(B)** toàn message không chứa `b'admin = False'`. Nếu cả hai đúng, trả `self.flag`. Ngược lại trả `"No flag for you!"`.
        
-   Tóm tắt logic kiểm tra:
    
    -   `Server.sign` từ chối ký nếu plaintext chứa `admin = True` ở bất kỳ đâu; đồng thời `Server.sign` chỉ ký nếu `admin = False` xuất hiện chính xác tại `msg[idx:idx+16]`.
        
    -   `FlagKeeper.get_flag` chỉ trả flag nếu:
        
        -   chữ ký hợp lệ (tức `enc_msg` phải được ký bởi `sk`),
            
        -   sau khi giải mã với key của FlagKeeper, `admin = True` nằm trong prefix `msg[:idx]`,
            
        -   và `admin = False` **không** xuất hiện ở bất cứ nơi nào trong `msg`.
            
-   Đặc biệt: Server dùng key A để giải mã trước khi ký; FlagKeeper dùng key B để giải mã khi kiểm tra để trả flag. Vì A != B, cùng `enc_msg` sẽ giải mã ra hai plaintext khác nhau nếu keys khác nhau. Đây là cốt lõi của challenge: **cùng một ciphertext** khi giải bằng hai key khác nhau cho hai plaintext khác nhau; server chỉ ký nếu plaintext thỏa điều kiện, và flagkeeper trả flag nếu plaintext khác (được giải bằng key của flagkeeper) thỏa điều kiện flag.
    

---

### Hàm `main()` — giao diện tương tác

```python
def main():
    flag = open("flag.txt", "rb").read().strip()
    fk = FlagKeeper(flag)
    server = Server()

    print("Welcome to the secure server!")
    print("You can use the following services:")
    print("1. Rotate Server's keys ")
    print("2. Rotate FlagKeeper's keys ")
    print("3. Sign a message (except admin = True)")
    print("4. Get the flag (only if your message contains admin = True)")
    print("5. Exit")
```

-   Mở file `flag.txt`, đọc flag; khởi tạo `FlagKeeper` và `Server`. In menu.
    

```python
for _ in range(5):
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                server.key_rotation()

            elif choice == 2:
                fk.key_rotation()

            elif choice == 3:
                enc_msg = bytes.fromhex(input("Enter the encrypted message (in hex): "))
                signature = server.sign(enc_msg)
                print("Signature (in hex):", signature.hex())

            elif choice == 4:
                enc_msg = bytes.fromhex(input("Enter the encrypted message (in hex): "))
                signature = bytes.fromhex(input("Enter the signature (in hex): "))
                flag = fk.get_flag(enc_msg, signature)
                print("Flag:", flag.decode())

            elif choice == 5:
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")
        except Exception as e:
            print("Error:", str(e))
```

-   Server cho phép tối đa **5 lượt** nhập (vòng for \_ in range(5)). Mỗi lượt có thể:
    
    1.  Quay key server (tăng idx +16).
        
    2.  Quay key FlagKeeper (giảm idx -16).
        
    3.  Gửi một **ciphertext** (hex) để server giải mã và ký — server trả về chữ ký của `enc_msg`.
        
    4.  Gửi một **ciphertext** (hex) và một chữ ký (hex) để FlagKeeper verify & trả flag nếu điều kiện thỏa.
        
    5.  Thoát.
        
-   Mọi ngoại lệ (ví dụ verify thất bại, decrypt lỗi, checks thất bại) được bắt và in `Error: ...`.
    

---

# 2) Tóm tắt / bản chất của challenge (nhìn từ góc độ an ninh)

-   Server và FlagKeeper dùng **khóa AES khác nhau**; cùng một `enc_msg` có thể giải ra hai plaintext khác nhau (vì decrypt với key khác).
    
-   Server chỉ ký ciphertext nếu khi giải bằng `Server.key`, plaintext có `admin = False` **tại vị trí idx** và **không có** `admin = True` ở bất kỳ đâu.
    
-   FlagKeeper trả flag nếu khi giải bằng `FlagKeeper.key`, plaintext có `admin = True` trong prefix `msg[:idx]` và **không có** `admin = False` ở bất kỳ đâu.
    
-   `idx` thay đổi theo các lần quay khóa: Server tăng idx +16, FlagKeeper giảm idx -16. Việc thay đổi này cho phép thay đổi vị trí nơi code kiểm tra chuỗi `admin = False` trong server và vị trí prefix nơi FlagKeeper tìm `admin = True`.
    
-   Vì server ký ciphertext (không ký plaintext) và flagkeeper xác thực chữ ký trên ciphertext, nên attack kiểu “tạo ciphertext được server ký nhưng khi FlagKeeper giải lại sinh ra plaintext có `admin = True`” là mục tiêu — phần challenge: tạo ciphertext mà giải với key A cho plaintext chứa `admin = False` đúng offset để server ký, nhưng giải với key B yield plaintext chứa `admin = True` ở vị trí trước idx (và không chứa `admin = False`).
    

---

# 3) Ví dụ minh hoạ: script mẫu (chạy local) — mô phỏng vòng đời encrypt/sign/get-flag

Dưới đây là một **ví dụ minh họa** bạn có thể chạy để thấy cách chương trình hoạt động (mã độc lập, mô phỏng client side và server/flagkeeper cùng chạy trong file đó để demo). **Lưu ý:** trong thực tế, `Server.key` và `FlagKeeper.key` khác nhau và bí mật; ví dụ này chỉ để minh họa hành vi.

```python
# demo_simulation.py
from os import urandom
from Crypto.Cipher import AES
from ecdsa import SigningKey, NIST384p
from hashlib import sha256

# Tạo keys giống như chương trình gốc
sk = SigningKey.generate(curve=NIST384p)
vk = sk.verifying_key

def aes_gcm_encrypt(key, plaintext):
    nonce = urandom(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(plaintext)
    return nonce + ct + tag

def aes_gcm_decrypt(key, enc_msg):
    nonce = enc_msg[:12]
    ct = enc_msg[12:-16]
    tag = enc_msg[-16:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ct, tag)

# Giả sử idx = 0 ban đầu
idx = 0

# Tạo 2 key khác nhau cho server và flagkeeper
server_key = urandom(16)
flag_key = urandom(16)

# Plaintexts mẫu:
# Khi server giải bằng server_key => plaintext phải chứa b'admin = False' bắt đầu tại offset idx (0)
# Khi flagkeeper giải bằng flag_key => plaintext phải có b'admin = True' trong prefix msg[:idx] (như idx>0)
#
# Ở ví dụ đơn giản này mình sẽ cho idx = 0, để thấy behavior: server sẽ reject admin=True anywhere.
# Nhưng để minh họa sự khác nhau, ta tạo hai plaintext khác nhau và tương ứng hai enc_msg khác nhau.

# plaintext_for_server: chứa '...admin = False...' at offset 0
plaintext_for_server = b"admin = False; user = guest;"
enc_msg_for_server = aes_gcm_encrypt(server_key, plaintext_for_server)

# Server decrypt & sign
try:
    msg = aes_gcm_decrypt(server_key, enc_msg_for_server)
    assert b'admin = True' not in msg
    assert b'admin = False' in msg[idx:idx+16]  # idx=0
    signature = sk.sign(enc_msg_for_server, hashfunc=sha256)
    print("Server signed enc_msg_for_server (signature hex):", signature.hex()[:80], "...")
except Exception as e:
    print("Server sign failed:", e)

# Now flagkeeper: simulate verifying signature then decrypting with flag_key
try:
    vk.verify(signature, enc_msg_for_server, hashfunc=sha256)  # verify passes since same signature
    # But decrypt with different key -> will raise (wrong tag) because different key -> invalid plaintext
    pt = aes_gcm_decrypt(flag_key, enc_msg_for_server)
    print("FlagKeeper decrypted:", pt)
except Exception as e:
    print("FlagKeeper decryption or verify failed:", e)
```

-   Kết quả: server ký thành công vì plaintext giải bằng `server_key` thỏa điều kiện. Nhưng flagkeeper dùng `flag_key` khác sẽ không thể giải được cùng ciphertext (thường sẽ raise authentication error) — điều này minh hoạ vì khóa khác, cùng `enc_msg` không có nghĩa là `FlagKeeper` sẽ giải được ra một plaintext hợp lệ.
    

---

# 4) Cách craft message (mô tả ý tưởng, không exploit chi tiết)

-   Mục tiêu tấn công (CTF-style): tìm hoặc tạo `enc_msg` sao cho:
    
    1.  Khi `enc_msg` được giải bằng **Server.key** -> plaintext contains `admin = False` tại `msg[idx:idx+16]` và **không có** `admin = True` -> Server ký `enc_msg`.
        
    2.  Khi `enc_msg` được giải bằng **FlagKeeper.key** -> plaintext contains `admin = True` trong `msg[:idx]` và **không có** `admin = False` -> FlagKeeper trả flag.
        
-   Vì `enc_msg` dùng AES-GCM (authenticated encryption), bạn **không thể** tự do đổi ciphertext để tạo ra hai plaintext khác nếu không biết cả hai khóa hoặc không tận dụng các yếu điểm khác (ex: reusing nonce with same key, leaking key via prints, padding oracle...). Challenge thường thiết kế để có lỗ hổng logic với `idx` và key rotations để người chơi lợi dụng (ví dụ: can change idx giữa lúc ký / get\_flag, reuse nonce hoặc replay attack, hoặc leak key prints).
    
-   Trong code gốc, các hàm `key_rotation()` in key hex — nếu attacker được xem log (console) hoặc có khả năng quay và đọc key prints, họ có thể biết key hiện tại -> từ đó craft enc\_msg. (Nhưng trong production, in key là lộ secret).
    

> Mình không hướng dẫn exploit cụ thể (tránh vượt ngưỡng), nhưng đã giải thích đủ để bạn hiểu điểm yếu logic cốt lõi.

---

# 5) Một số lưu ý kỹ thuật / pitfalls

-   **Ký trên ciphertext**: server ký `enc_msg` không phải plaintext — đây là điểm quan trọng.
    
-   **AES-GCM**: dùng nonce 12 bytes + tag 16 bytes — bạn phải dựng enc\_msg theo đúng format `nonce || ct || tag`.
    
-   **Verify trước decrypt**: FlagKeeper verify chữ ký trước rồi mới giải mã với `FlagKeeper.key`.
    
-   **Slicing theo idx**: kiểm tra `msg[idx:idx+16]` có nghĩa là server đòi đúng vị trí chứa `admin = False`. Nếu idx thay đổi, vị trí cần đổi theo.
    
-   **Global idx**: được cả hai class thay đổi. Độ lệch của idx giữa thời điểm server ký và FlagKeeper kiểm tra có thể được lợi dụng nếu attacker điều khiển rotations.
    
-   **Printing keys**: `print("current Server key: ", self.key.hex())` làm lộ key nếu attacker có thể xem output — trong challenge, có thể đây là intended leak.
    

---

# 6) Kết luận ngắn

-   Code mô phỏng một challenge crypto: **hai thực thể** (Server, FlagKeeper) dùng hai key AES khác nhau để giải cùng một `enc_msg`. Server ký ciphertext nếu plaintext (giải bằng server key) có `admin = False` ở vị trí `idx`. FlagKeeper trả flag nếu plaintext (giải bằng flag key) có `admin = True` trong prefix và không chứa `admin = False`. `idx` thay đổi khi quay key.
    
-   Mấu chốt: **sự khác biệt giữa hai key** + **signature trên ciphertext** + **kiểm tra vị trí theo `idx`** tạo nên một trò chơi để tìm được ciphertext thỏa cả hai điều kiện khi được giải bằng hai key khác nhau.
    

---

Nếu bạn muốn mình:

-   **(A)** Viết một script mô phỏng tấn công/thuật toán thử-nhiều-trường-hợp (brute-force nonce? thử các vị trí idx?) — mình có thể viết ví dụ mô phỏng (không đảm bảo lấy được flag, nhưng minh hoạ các bước).
    
-   **(B)** Viết một phiên bản đã tối giản (unit tests) để bạn chạy và thử nghiệm với các rotation để quan sát `idx` thay đổi, printing keys.
    
-   **(C)** Giải thích sâu hơn về AES-GCM (nonce/tag), hoặc ECDSA (signature format) — mình sẽ giải thích và cho ví dụ hex cụ thể.
    

Bạn muốn mình tạo ví dụ bổ sung nào không? (ví dụ: script simulation hoàn chỉnh để chạy)