from pwn import *
import json, ast, re
from decrypt import *

host = "socket.cryptohack.org"
port = 13379
r = remote(host, port)

r.recvuntil('Send to Bob: ').decode()
r.sendline(b'{"supported":["DH64"]}')    # Chọn nhỏ nhất

r.recvuntil('Intercepted from Bob: ').decode()
text_b = r.recvline(keepends=False).strip().decode()

r.recvuntil('Send to Alice: ').decode()
r.sendline(text_b.encode())

r.recvuntil('Intercepted from Alice: ').decode()
p_g_A = r.recvline(keepends=False).strip().decode()
p_g_A = json.loads(p_g_A)

r.recvuntil('Intercepted from Bob: ').decode()
B = r.recvline(keepends=False).strip().decode()
B = json.loads(B)

r.recvuntil('Intercepted from Alice: ').decode()
iv_cipher = r.recvline(keepends=False).strip().decode()
iv_cipher = json.loads(iv_cipher)

p = int(p_g_A['p'], 16)
g = int(p_g_A['g'], 16)
A = int(p_g_A['A'], 16)
B = int(B['B'], 16)

from sympy.ntheory.residue_ntheory import *  #help to calculate 'a' from diff Helman alg
'''
From
A = pow(g,a,p) - we have everything except 'a'
B = pow(g,b,p) - we have  no b,

calculating a
a =discrete_log(p,A,g)
b =discrete_log(p,B,g)

Then 
shared_secret(alice) = shared_secret(bob)
shared_secret = pow(B,a,p)
'''
a = discrete_log(p, A, g)
b = discrete_log(p, B, g)
print("The value of a and b", {a,b})
#print(sharedSecretAlice = pow(A,b,p))
#SharedSecretBob = pow(B,a,p)
#print("Alice & Bob shared secret: ", {SharedSecretAlice,SharedSecretBob})
shared_secret = pow(B,a,p)
print("Shared_secret is: ", shared_secret)
print(decrypt_flag(shared_secret, iv_cipher['iv'], iv_cipher["encrypted_flag"]))