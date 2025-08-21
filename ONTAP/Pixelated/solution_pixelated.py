from PIL import Image
import numpy as np
import glob
import os

def sum_images(img_file_lst):
    
    # Mở và chuyển đổi tất cả ảnh sang định dạng RGB và NumPy array
    img_RGB_lst = [np.array(Image.open(img).convert('RGB')) for img in img_file_lst]
    
    # Cộng tất cả các ảnh với nhau, đảm bảo giá trị không vượt quá 255
    result = np.zeros_like(img_RGB_lst[0], dtype=np.int32)  # Mảng để chứa kết quả
    
    # Đảm bảo rằng tất cả các ảnh đều có cùng kích thước
    width, height = img_RGB_lst[0].shape[1], img_RGB_lst[0].shape[0]
    for img in img_RGB_lst:
        if img.shape[1] != width or img.shape[0] != height:
            raise ValueError("All images must have the same dimensions")
        result += img
    
    # Đảm bảo các giá trị nằm trong khoảng từ 0 đến 255
    result = result % 256

    # Chuyển đổi kết quả về dạng ảnh
    result_image = Image.fromarray(result.astype(np.uint8))
    return result_image

# Đường dẫn tới thư mục chứa ảnh
image_folder = "."

# Tìm tất cả các file ảnh có dạng scrambled*.png
image_files = glob.glob(os.path.join(image_folder, "scrambled*.png"))

res = sum_images(image_files)
res.show()

# picoCTF{7188864c}