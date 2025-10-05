import base64

# Chuỗi cần giải mã
with open('enc_flag', 'rb') as file:
    flag_enc = file.readline().strip()

# print(flag_enc)

b64decode1 = base64.b64decode(flag_enc).decode()
b64decode1 = b64decode1.replace("b'", "").replace("'", "")
b64decode2 = base64.b64decode(b64decode1).decode()

flag_base_decode = "wpjvJAM{jhlzhy_k3jy9wa3k_890k2379}"
flag             = "picoCTF{.........................}"

original_chars = "abcdefghijklmnopqrstuvwxyz"
encrypts_chars = "**j**m**p*****vw***a******"
# ==> Caeser cipher

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

flag = caesar_decrypt(b64decode2, 26 - ord('t') + ord('a'))
print(flag)