from pwn import *
from Crypto.Util.number import *

# Mảng chữ cái và mã Morse tương ứng
letters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
]

morse_letters = [
    '.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---',
    '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-',
    '..-', '...-', '.--', '-..-', '-.--', '--..'
]

# Mảng chứa các chữ số và mảng mã Morse tương ứng
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

morse_digits = [
    '-----',  # 0
    '.----',  # 1
    '..---',  # 2
    '...--',  # 3
    '....-',  # 4
    '.....',  # 5
    '-....',  # 6
    '--...',  # 7
    '---..',  # 8
    '----.'   # 9
]

char_lst = letters + digits
morse_lst = morse_letters + morse_digits

char_mapping = {morse_lst[i]: char_lst[i] for i in range(len(morse_lst))}

# Tạo một conection remote:
port = 48247
r = remote('jupiter.challenges.picoctf.org', port)

# Lấy flag được mã hóa
flag_enc = r.recvline(keepends=False).strip().decode()

flag_enc_lst = flag_enc.split()
flag = []
for block in flag_enc_lst:
    if block in char_mapping:
        flag.append(char_mapping[block])
    else:
        flag.append(block)
        
print("\n\n")
print("".join(flag))
print("\n\n")

r.close()