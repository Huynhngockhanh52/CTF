from pwn import *
from Crypto.Util.number import *
import subprocess
from IPython.display import clear_output

def hex2dec_ascii(hex_str):
    '''
    Phương thức chuyển chuỗi HEX theo đề bài về 2 mảng là thập phân và ký tự
    '''
    hexs_lst = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
    
    decs_lst = []
    ascs_lst = []
    
    for hexa in hexs_lst:
        dec_value = int(hexa, 16)  # Chuyển đổi từ hex sang dec
        decs_lst.append(dec_value)
        ascs_lst.append(chr(dec_value))  # Chuyển đổi từ dec sang ký tự ASCII
    return decs_lst, ascs_lst

# Tạo một conection remote:
port = 58913
r = remote('mercury.picoctf.net', port)

# Lấy flag được mã hóa
get_success = r.recvuntil('This is the encrypted flag!\n').decode()
flag_enc = r.recvline(keepends=False).strip().decode()
print(flag_enc)
print(len(flag_enc)//2)         # 32

# Chuyển đổi flag về 2 mảng decimal và character
_, ascii_flag = hex2dec_ascii(flag_enc)
ascii_flag = "".join(ascii_flag)

# Tạo một chuỗi bất kỳ với độ dài bằng LEN_KEY - len(flag)
temp_enc = 'a'* (50000 - len(flag_enc)//2)

# Đưa vào để chạy hết chiều dài của key
get_success = r.recvuntil('like to encrypt?').decode()
r.sendline(temp_enc)                # r.send('pi\n`)
get_success = r.recvuntil('Here ya go!\n').decode()
char2_enc = r.recvline(keepends=False).strip().decode()


# 2 lần mã hóa = 1 lần giải mã
get_success = r.recvuntil('like to encrypt?').decode()
r.sendline(ascii_flag)               
get_success = r.recvuntil('Here ya go!\n').decode()
char2_enc = r.recvline(keepends=False).strip().decode()
print(char2_enc)

_, flags = hex2dec_ascii(char2_enc) 

# Xóa stdout
clear_output(wait=True)

# in ra Flag 
flag = 'picoCTF{' + "".join(flags)+ '}'
print("\n\n")
print(flag)