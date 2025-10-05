def caesar_encrypt(plaintext, key):
    ciphertext = ""
    for char in plaintext:
        # Kiểm tra nếu ký tự là chữ cái
        if char.isalpha():
            shift = key % 26
            ascii_offset = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            ciphertext += new_char
        else:
            ciphertext += char  # Giữ nguyên ký tự không phải chữ cái
    return ciphertext

def caesar_decrypt(ciphertext, key):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            shift = key % 26 
            ascii_offset = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            plaintext += new_char
        else:
            plaintext += char 
    return plaintext

plaintext = "picoCTF{}"
key = 4

# Ciphertext
# ciphertext = "xqkwKBN{z0bib1wv_l3kzgxb3l_429in00n}"
ciphertext = ""
with open('encrypted.txt', 'r') as file:
    lines = file.readlines()
for line in lines:
    ciphertext += str(line)

# Giải mã và in ra plaintext
for i in range(0,26):
    decrypted_text = caesar_decrypt(ciphertext, i)
    if "picoCTF" in decrypted_text:
        print(f"Giải mã k = {i}: {decrypted_text}")
