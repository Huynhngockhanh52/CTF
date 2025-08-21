import itertools

def generate_permutations(n):
    '''
    Phương thức này trả về hoán vị của các phần tử từ 0 -> (n-1). Trả về mảng 3D  
    '''
    # Tạo mảng chứa các phần tử từ 1 đến n
    origin_arr = list(range(0, n))
    
    # Sử dụng permutations để lấy tất cả các hoán vị
    permutations_list = list(itertools.permutations(origin_arr))
    
    # Chuyển đổi các hoán vị từ tuple thành list
    permutations_list = [list(permutation) for permutation in permutations_list]
    
    return permutations_list

def split_into_blocks(text, block_size=3):
    '''
    Phương thức phân tách chuỗi thành các khối nhỏ dựa trên kích thước `block_size` đã cho. Trả về một list(): 2D
    '''
    # Duyệt chuỗi theo từng khối có độ dài `block_size`
    blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]
    return blocks

def decrypt_block(cipher_blocks, change_arr):
    '''
    Giải mã từng khối bản mã dựa trên một mảng vị trí chỉ định.
    '''
    res = ""
    for block in cipher_blocks:
        # Chuyển đổi vị trí của khối lại ban đầu và cộng vào res
        for idx in change_arr:
            res += block[idx]
    print(res)

# Thực hiện:
cipher = ""
with open('message.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    cipher += line.strip()

# Chia chuỗi thành các khối nhỏ
cipher_blocks = split_into_blocks(cipher, 3)

# Lấy tất cả hoán vị với n = 3
n3 = generate_permutations(3)

# Thực hiện giải mã:
for arr in n3:
    decrypt_block(cipher_blocks, arr)
