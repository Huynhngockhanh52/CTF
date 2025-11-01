from Crypto.Cipher import AES
import requests


KEY = "null"
FLAG = "null"


# @chal.route('/block_cipher_starter/decrypt/<ciphertext>/')
def decrypt(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)

    cipher = AES.new(KEY, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


# @chal.route('/block_cipher_starter/encrypt_flag/')
def encrypt_flag():
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(FLAG.encode())

    return {"ciphertext": encrypted.hex()}

plaintext = "63727970746f7b626c30636b5f633170683372355f3472335f663435375f217d"
flag = bytes.fromhex(plaintext).decode('utf-8')
print(flag)

ciphertext = "c11949a4a2ecf929dfce48b39daedd9e6d90c67d2f550b79259bdda835348a48"
res = requests.get("https://aes.cryptohack.org/block_cipher_starter/decrypt/" + ciphertext + "/")
print(res.json())