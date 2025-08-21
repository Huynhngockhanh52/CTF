def rail_fence_encrypt(text, key):
    # Tạo danh sách chứa các hàng kích thước (len(text), key)
    rail = [['' for _ in range(len(text))] for _ in range(key)]
    
    direction_down = False
    row = 0
    
    for i in range(len(text)):
        # Đặt ký tự vào hàng hiện tại
        rail[row][i] = text[i]
        
        # Nếu ở hàng trên cùng hoặc dưới cùng, thay đổi hướng
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        
        # Dịch chuyển lên hoặc xuống
        row += 1 if direction_down else -1
    
    encrypted_text = []
    for r in rail:
        encrypted_text.append(''.join(r))
    
    return ''.join(encrypted_text)

def rail_fence_decrypt(cipher, key):
    cols = len(cipher)
    rail = [['' for _ in range(cols)] for __ in range(key)]
    direction_down = False
    row = 0
    
    # Đánh dấu các vị trí zigzag
    for i in range(cols):
        rail[row][i] = '*'
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1
    
    # Điền các ký tự từ cipher vào các vị trí đã đánh dấu
    index = 0
    for i in range(key):
        for j in range(cols):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1
    
    # Giải mã bằng cách đọc lại theo zigzag
    result = []
    row = 0
    direction_down = False
    for i in range(len(cipher)):
        result.append(rail[row][i])
        
        if row == 0 or row == key - 1:
            direction_down = not direction_down
        
        row += 1 if direction_down else -1
    
    return ''.join(result)

# Thực hiện giải mã:
cipher = ""
with open('message.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    cipher += line.strip()
    
print(cipher)

for key in range(2, 11):
    plaintext = rail_fence_decrypt(cipher, key)
    print(f"Key k = {key}: {plaintext}")