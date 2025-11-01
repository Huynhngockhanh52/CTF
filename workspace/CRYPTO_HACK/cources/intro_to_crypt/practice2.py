str_hex = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"

string = bytes.fromhex(str_hex).decode()

key = "myXORkey"*6

flag = "".join(chr(ord(string[i]) ^ ord(key[i])) for i in range(len(str_hex)//2))
print(flag)
