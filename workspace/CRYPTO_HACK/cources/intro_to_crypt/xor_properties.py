KEY1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
KEY21 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
KEY23 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
FLAG_KEY123 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

key1 = bytes.fromhex(KEY1)
key21 = bytes.fromhex(KEY21)
key23 = bytes.fromhex(KEY23)
flag_key123 = bytes.fromhex(FLAG_KEY123)

key13 = bytes(a ^ b for a, b in zip(key1, key23))

key2 = bytes(a ^ b for a, b in zip(key21, key1))
key3 = bytes(a ^ b for a, b in zip(key23, key2))

flag = bytes(a ^ b ^ c ^ d for a, b, c, d in zip(flag_key123, key2, key3, key1))

print(flag.decode())