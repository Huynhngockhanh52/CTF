from pwn import *

# Tạo một conection remote:
port = 5726
r = remote('jupiter.challenges.picoctf.org', port)

get_success = r.recvuntil('Encrypted message:\n').decode()
cipher = r.recvuntil('\n\n\n').decode()
r.close()

flag_enc = "pohzCZK{m311a50_0x_a1rn3x3_h1ah3x6kp60egf}"

def vigenere_encrypt(plaintext, key):
    key = key.lower()  # Khóa được chuyển sang chữ thường
    ciphertext = []
    key_index = 0
    
    for char in plaintext:
        if char.isalpha():  
            if char.islower():
                shift = (ord(char) - ord('a') + ord(key[key_index]) - ord('a')) % 26
                ciphertext.append(chr(shift + ord('a')))
            else:
                shift = (ord(char.lower()) - ord('A') + ord(key[key_index]) - ord('a')) % 26
                ciphertext.append(chr(shift + ord('A')))
            
            key_index = (key_index + 1) % len(key)  # Dịch chuyển trong khóa
        else:
            ciphertext.append(char)  # Bỏ qua ký tự không phải chữ cái
    
    return ''.join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    key = key.lower()  # Khóa được chuyển sang chữ thường
    # ciphertext = ciphertext.lower()
    plaintext = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha(): 
            if char.islower():
                shift = (ord(char) - ord(key[key_index]) + 26) % 26
                plaintext.append(chr(shift + ord('a')))
            else:
                shift = (ord(char.lower()) - ord(key[key_index]) + 26) % 26
                plaintext.append(chr(shift + ord('A')))
            
            key_index = (key_index + 1) % len(key) 
        else:
            plaintext.append(char)  # Bỏ qua ký tự không phải chữ cái
    
    return ''.join(plaintext)

key = "agfl"
ciphertext = cipher
flag = vigenere_decrypt(flag_enc, key)

print(flag)