str_hex = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

string = bytes.fromhex(str_hex).decode()

for xored in range(256):
    flag = "".join(chr(ord(c) ^ xored) for c in string)
    if "crypto{" in flag:
        print(flag, xored)