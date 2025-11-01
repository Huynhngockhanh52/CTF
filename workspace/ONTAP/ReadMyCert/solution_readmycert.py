import subprocess
command = [
        # Thêm -noout và -text để hiển thị nội dung
        'openssl', 'req', '-in', 'readmycert.csr', '-noout', '-text'  
    ]

try:
    # Mở tệp decrypt.txt để ghi đầu ra
    with open('decrypt.txt', 'w') as output_file:
        # Chạy câu lệnh OpenSSL bằng subprocess và chuyển hướng stdout đến tệp
        result = subprocess.run(command, check=True, stdout=output_file, stderr=subprocess.PIPE)

    print("Giải mã thành công, dữ liệu đã được lưu vào decrypt.txt!")

    # Đọc và in nội dung từ tệp decrypt.txt
    with open('decrypt.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            print(line.strip())  # Sử dụng strip() để loại bỏ ký tự xuống dòng

except subprocess.CalledProcessError as e:
    # In ra lỗi nếu có vấn đề trong quá trình giải mã
    print(f"Lỗi khi giải mã file: {e.stderr.decode('utf-8')}")