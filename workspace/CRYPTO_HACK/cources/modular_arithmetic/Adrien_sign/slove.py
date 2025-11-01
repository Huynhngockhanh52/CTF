from sympy import isprime, legendre_symbol

a = 288260533169915
p = 1007621497415251

num_lst = None
with open("output.txt") as f:
    num_lst = f.readline().strip().lstrip('[').rstrip(']').split(', ')

if not isprime(p):
    print("p is not prime!")

else:
    print(f"p is prime!, p mod 4 = {p % 4}")
    bit_lst = []
    for n in num_lst:
        n = int(n)
        bit_lst.append(1 if legendre_symbol(n, p) == 1 else 0)
    bit_str = ''.join(map(str, bit_lst))
    
    flag = ""
    for i in range(0, len(bit_str), 8):
        byte = bit_str[i:i+8]
        flag += chr(int(byte, 2))
    print("FLAG:", flag)
    
        
    

    
