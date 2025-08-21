Trong một hệ thống khóa công khai, tấn công bản rõ được chọn **(Chosen plaintext attack - CPA)** gần như là một phần của thiết kế, các bản rõ tùy ý có thể được mã hóa để tạo ra các bản mã theo ý muốn. Tuy nhiên, theo thiết kế, những điều này không nên cung cấp bất kỳ thông tin nào giúp suy ra khóa riêng tư.

Một cuộc tấn công bản mã được chọn có thể được thực hiện bằng cách lựa chọn cẩn thận bản rõ. Tuy nhiên, để thực hiện một cuộc tấn công, điều này khá đơn giản đối với RSA. Trước hết, chúng ta có một bản mã mà ta ký hiệu là:
$$C \equiv t^e \mod n$$

Đây là RSA mà chúng ta đã biết. Giờ đây, Eve có C, điều này hoàn toàn bình thường vì Eve được cho phép thấy C. Bây giờ Eve có thể chọn một bản rõ, chọn 2 làm bản rõ của mình và tính toán:
$$C_a \equiv 2^e \mod n$$

Tuy nhiên, cô ta gửi cho nạn nhân không nghi ngờ của mình: 
$$C_b \equiv C_a \cdot C \equiv t^e \cdot 2^e \mod n$$

Tất cả đều ổn. Vì đây là một cuộc tấn công bản rõ được chọn, ta sẽ dựa vào việc có quyền truy cập vào quá trình giải mã của giá trị thay thế của mình, nên bây giờ nạn nhân không nghi ngờ sẽ tính toán:
$$(C_b)^d \equiv [t^e \cdot 2^e]^d \equiv (t^e)^d \cdot (2^e)^d \mod n$$

Tuy nhiên, với bất kỳ văn bản rõ $x$ nào, chúng ta biết rằng $C ≡ x^e$ và $x ≡ C^d$. Do đó:
$$(x^e)^d ≡ x \mod n$$

Do đó, từ kết quả trên, ta có:
$$(C_b)^d \equiv t \cdot 2 \mod n$$

Khi nhận lại giá trị đó, chúng ta có thể dễ dàng tính toán $t$. Chúng ta chỉ cần chia đôi nó.

Điều này thực sự có thể áp dụng cho bất kỳ bản rõ nào mà ta muốn chọn, tôi chọn số $2$ vì nó đơn giản. Bài báo này đề cập đến kỹ thuật chung và nhiều thứ khác nữa.

Điều này chỉ áp dụng cho RSA đơn giản (theo sách giáo khoa). Ứng dụng đúng đắn của RSA ngoài thực tế đòi hỏi phải sử dụng các sơ đồ đệm (padding schemes) để đánh bại cuộc tấn công này bằng cách đảm bảo rằng bản mã không thể bị thay đổi theo cách này.