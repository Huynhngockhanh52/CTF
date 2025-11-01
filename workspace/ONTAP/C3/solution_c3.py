import sys
from fileinput import input

lookup1 = "\n \"#()*+/1:=[]abcdefghijklmnopqrstuvwxyz"
lookup2 = "ABCDEFGHIJKLMNOPQRSTabcdefghijklmnopqrst"

# Nhận dữ liệu đầu vào
chars = ""
lines = None

with open('ciphertext', 'r') as file:
    lines = file.readlines()

for line in lines:
    chars += str(line)
# print(char)

# Đảo ngược và chuyển chuỗi thành một mảng các index trong lookup2:
chars = chars[::-1]
# print(chars)

num_chars = []
for char in chars:
    num_chars.append(lookup2.index(char))
# print(num_chars)

max_for = len(lookup1)
for m in range(max_for):
    X = m
    text_decrypt = ""
    for enc_i in num_chars:
        text_decrypt += lookup1[X]
        X = (X - enc_i) % 40
    # # Giải mã ký tự cuối cùng
    # text_decrypt += lookup1[X]

    # Đảo ngược chuỗi lại
    text_decrypt = text_decrypt[::-1]
    if X == 0:
        with open('decrypt.txt', 'w', encoding='utf-8') as file:
            file.write(text_decrypt)
        # print(f'Chuỗi với i = {X}: {repr(text_decrypt)}') # Chạy in ra \n
        print(f'Chuỗi với i = {X}: {text_decrypt}')
        
## Này là thu được mã code:
chars = ""
with open('decrypt.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    chars += str(line)

b = 1
flag = ""
for i in range(len(chars)):
    if i == b * b * b:
        print(chars[i], end="")
        flag += chars[i]
        b += 1
print()
print(f"picoCTF{{{flag}}}")