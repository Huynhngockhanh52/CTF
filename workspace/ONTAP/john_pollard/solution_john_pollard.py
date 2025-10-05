from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import base64
import sympy
from itertools import permutations
from pprint import pprint

# Đọc chứng chỉ từ file
with open("cert", "rb") as cert_file:
    certificate_pem = cert_file.read()

# Giải mã chứng chỉ
certificate = x509.load_pem_x509_certificate(certificate_pem, default_backend())

# Lấy khóa công khai từ chứng chỉ
public_key = certificate.public_key()

# Kiểm tra nếu là khóa RSA
if isinstance(public_key, rsa.RSAPublicKey):
    # Trích xuất modulus và số mũ công khai
    public_numbers = public_key.public_numbers()
    modulus = public_numbers.n
    exponent = public_numbers.e
    
    # Hiển thị modulus và số mũ
    print("N:", modulus)
    print("e:", exponent)
    
    # Trích xuất ra p, q:
    factors = sympy.factorint(modulus)
    pq_lst = list(factors.keys())
    
    # Lấy tất cả hoán vị của mảng
    permutations_list = list(permutations(pq_lst))
    
    flag = "picoCTF{"
    for pq in permutations_list:
        temp = flag + ",".join(map(str, pq)) + "}"
        print(temp)
else:
    print("Không phải là khóa RSA.")

# Flag: picoCTF{73176001,67867967}