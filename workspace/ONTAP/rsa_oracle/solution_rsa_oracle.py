from pwn import *
from Crypto.Util.number import *
import subprocess
# import decimal

# Mã hóa openSSL:
def decrypt_file(input_file, password):
    command = [
        'openssl', 'enc', '-aes-256-cbc', '-d', '-in', input_file, '-k', password
    ]

    try:
        # Sử dụng subprocess để chạy câu lệnh và đọc kết quả từ stdout
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # In ra kết quả đã giải mã
        print(f"Result: {result.stdout}")

    except subprocess.CalledProcessError as e:
        # In ra lỗi nếu có vấn đề trong quá trình giải mã
        print(f"Lỗi khi giải mã file: {e.stderr}")

# Tạo một conection remote:
port = 56248
r = remote('titan.picoctf.net', port)

# Đọc file về password:
with open('password.enc', 'r') as file:
    password_enc = int(file.read().strip())

# Gửi yêu cầu mã hóa: E, sau đó gửi dữ liệu mã hóa là số 2 đi:
enc_sym = b'E' + b'\n' 
dec_sym = b'D' + b'\n' 

payload = b'\x02' + b'\n'

get_success = r.recvuntil('decrypt.').decode()
r.send(enc_sym)                 # r.sendline(b'E')
get_success = r.recvuntil('keysize):').decode()
r.send(payload)

# Vì server gửi ra quá nhiều dòng, do đó, ta sẽ thực hiện lấy dữ liệu mã hóa của 2 bằng cách lắng nghe để gọn code:
get_success = r.recvuntil('ciphertext (m ^ e mod n)').decode()
enc_2 = r.recvline(keepends=False).decode()

# Nhân 2 giá trị encode vào và thực hiện quá trình giải mã:
text_dec = int(enc_2) * password_enc
text_dec = str(text_dec).encode() + b'\n'

# Thực hiện decrypt:
get_success = r.recvuntil('decrypt.').decode()
r.send(dec_sym)      
get_success = r.recvuntil('decrypt:').decode()
r.send(text_dec)

# Lấy dữ liệu decrypt:
get_success = r.recvuntil('hex (c ^ d mod n):').decode()
num_dec = r.recvline(keepends=False).strip().decode()     
get_success = r.recvuntil('decrypted ciphertext:').decode()
text_dec = r.recvline(keepends=False).strip().decode()    

# Chuyển đổi thành số nguyên (từ 16 --> 10), sau đó chia lấy phần nguyên với 2
num_dec = int(num_dec, 16)//2
print(num_dec)

# Chuyển lại thành hexa, sau đó bỏ số 0x. Cuối cùng chuyển về lại thành byte ASCII
hex_string = hex(num_dec)[2:]
byte_array = bytes.fromhex(hex_string)
text_dec = byte_array.decode('ascii')
print(text_dec, hex_string)

# Giải mã và in ra kết quả:
decrypt_file("secret.enc", text_dec)        

# Đóng chương trình:
r.close()