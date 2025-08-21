# Thực hiện giải mã:
username = "cultiris"
password = ""
idx_target = None
with open('usernames.txt', 'r') as file:
    users_lst = file.readlines()
for idx, line in enumerate(users_lst):
    if line.strip() == username:
        idx_target = idx
        break

if idx_target is not None:
    with open('passwords.txt', 'r') as file:
        pass_lst = file.readlines()
        assert idx_target < len(pass_lst)
        password = pass_lst[idx_target].strip()
print(username, password)

def caesar_encrypt(plaintext, shift):
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():  # Kiểm tra nếu ký tự là chữ cái
            shift_base = ord('A') if char.isupper() else ord('a')  # Xác định bảng chữ cái A-Z (65) hoặc a-z (97)
            
            encrypted_text += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted_text += char  # Giữ nguyên các ký tự không phải chữ cái
    return encrypted_text

def caesar_decrypt(ciphertext, shift):
    decrypted_text = ""
    
    for char in ciphertext:
        if char.isalpha():  
            shift_base = ord('A') if char.isupper() else ord('a')  
            
            decrypted_text += chr((ord(char) - shift_base - shift) % 26 + shift_base)
        else:
            decrypted_text += char
    return decrypted_text

plaintext = caesar_decrypt(password, ord('n')-ord('a'))
print(plaintext)