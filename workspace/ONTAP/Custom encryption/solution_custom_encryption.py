from random import randint
import sys
from custom_encryption import *


# Đọc nội dung từ tệp
with open('enc_flag', 'r') as file:
    lines = file.readlines()

# Khởi tạo biến
a = None
b = None
cipher = []

# Trích xuất giá trị từ các dòng
for line in lines:
    if line.startswith('a ='):
        a = int(line.split('=')[1].strip())
    elif line.startswith('b ='):
        b = int(line.split('=')[1].strip())
    elif line.startswith('cipher is:'):
        cipher = eval(line.split(':')[1].strip())

p = 97
g = 31

key = generator(generator(g, b, p), a, p)

# Định nghĩa một phương thức decrypt():
def decrypt(cipher:list, key: int) -> str:
    s = []
    plaintext = ""
    for item in cipher:
        num = item // (key * 311)
        s.append(num)
        char = chr(num)
        plaintext += char
    # print(s)
    return plaintext, s

# Định nghĩa lại phương thức XOR:
def dynamic_xor_decrypt(plaintext_arr, text_key):
    cipher_text = ""
    key_length = len(text_key)
    for i, char in enumerate(plaintext_arr):
        key_char = text_key[i % key_length]
        encrypted_char = chr(char ^ ord(key_char))
        cipher_text += encrypted_char
    
    # Đảo ngược chuỗi lại:
    cipher_text = cipher_text[::-1]
    return cipher_text


semi_plaintext, plaintext_arr = decrypt(cipher, key)
plaintext = dynamic_xor_decrypt(plaintext_arr, "trudeau")

print(plaintext)