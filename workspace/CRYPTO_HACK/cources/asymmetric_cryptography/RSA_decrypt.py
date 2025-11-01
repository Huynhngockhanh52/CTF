from sympy import factorint

N = 882564595536224140639625987659416029426239230804614613279163
e = 65537

cipher = 77578995801157823671636298847186723593814843845525223303932

# factors = factorint(N)
# Sử dụng db factor: https://www.alpertron.com.ar/ECM.HTM
p = 857504083339712752489993810777
q = 1029224947942998075080348647219

phiN = (p - 1) * (q - 1)

# for key, val in factors:
#     if val == 1:
#         phiN *= key

d = pow(e, -1, phiN)

plaintext = pow(cipher, d, N)
print(plaintext)