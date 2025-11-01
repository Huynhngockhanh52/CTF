from pwn import *
import json, ast, re
from decrypt import *

def str2dict(s):
    for loader in (json.loads, ast.literal_eval):
        try:
            obj = loader(s)
            break
        except Exception:
            obj = None
    if not isinstance(obj, dict):
        pairs = re.findall(r'["\']?([A-Za-z0-9_+-]+)["\']?\s*:\s*["\']?([^,"\'}\]]+)["\']?', s)
        obj = {k: v for k, v in pairs}
    def conv(v):
        if isinstance(v, int):
            return v
        v = v.strip()
        if re.fullmatch(r'[+-]?0[xX][0-9a-fA-F]+', v):
            return int(v, 16)
        if re.fullmatch(r'[0-9]+', v):
            return int(v, 10)
        return v
    return {k: conv(v) for k, v in obj.items()}

def dec2hex(n):
    if n == 0:
        return "0x00"
    num_bytes = (n.bit_length() + 7) // 8  # số byte cần thiết
    return "0x" + n.to_bytes(num_bytes, "big").hex()

host = "socket.cryptohack.org"
port = 13371
r = remote(host, port)

get_success = r.recvuntil('from Alice: ').decode()
alice = r.recvline(keepends=False).strip().decode()
alice = str2dict(alice)

get_success = r.recvuntil('Send to Bob: ').decode()

mitm_json = {
    "p": dec2hex(alice["p"]),
    "g": dec2hex(alice["g"]),   # hoặc "0x02" nếu bạn muốn cố định
    "A": dec2hex(1)
}
payload = json.dumps(mitm_json)   # đây là string JSON hợp lệ
r.sendline(payload)
# r.sendline(b'{"p":"0x01","g":"0x02","A":"0x03"}')
get_success = r.recvuntil('from Bob: ', timeout=10).decode()

gb = r.recvline(keepends=False).strip().decode()
gb = str2dict(gb)

r.sendline(b'{"B":"0x01"}') # ==> key = 0x01
r.recvuntil(b"Intercepted from Alice:")

data = r.recvline(keepends=False).strip().decode()
data = json.loads(data)
print(data)

print(decrypt_flag(1, data['iv'], data['encrypted_flag']))