def atbash_encode(text):
    encoded = ""
    for char in text:
        if char.isalpha():
            # Chuyển đổi chữ hoa và chữ thường
            if char.islower():
                encoded += chr(219 - ord(char))  # ord('a') = 97, ord('z') = 122
            else:
                encoded += chr(155 - ord(char))  # ord('A') = 65, ord('Z') = 90
        else:
            encoded += char  # Giữ nguyên ký tự không phải chữ cái
    return encoded


def atbash_decode(text):
    # Vì Atbash là đối xứng, hàm decode giống hàm encode
    return atbash_encode(text)


# Đầu tiên ta sử dụng `steghide extract -sf atbash.jpg` để trích xuất file mã hóa giấu trong ảnh. Tiếp theo, ta giải mã đoạn bản mã bằng thuật toán Atbash
cipher = ""
with open('encrypted.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    cipher += line.strip()
plaintext = atbash_decode(cipher)
print(plaintext)