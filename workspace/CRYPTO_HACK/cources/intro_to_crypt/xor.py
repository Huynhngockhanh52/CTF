label = "label" 

decoded = "".join(chr(ord(ch) ^ 13) for ch in label)

flag = f"crypto{{{decoded}}}"
print(flag)