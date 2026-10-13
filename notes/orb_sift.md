# Giải thích thuật toán SIFT và ORB

Tài liệu so sánh và giải thích cơ chế của hai thuật toán trích xuất đặc trưng cổ điển (**SIFT** và **ORB**) dùng trong pipeline ghép ảnh UAV 2D.

---

## 1. Bản chất chung của bài toán Feature Matching

Để ghép 2 bức ảnh chụp từ drone, thuật toán cần làm 2 bước:
1. **Detector (Bộ tìm điểm):** Tìm các vị trí "đặc biệt" trên ảnh (góc nhà, ngã tư, hoa văn rõ nét) không bị mất đi khi đổi góc quay hay zoom.
2. **Descriptor (Bộ mô tả):** Biến vùng ảnh xung quanh mỗi điểm thành một chuỗi số (vector đặc trưng) để thuật toán so sánh xem điểm ở ảnh A là điểm nào ở ảnh B.

---

## 2. SIFT (Scale-Invariant Feature Transform)

Được đề xuất bởi David Lowe (1999, hoàn thiện 2004). Là tượng đài về độ chính xác trong thị giác máy tính cổ điển.

### Cách hoạt động
- **Tìm điểm (Scale-Space Extrema):** Làm mờ ảnh bằng bộ lọc Gaussian ở nhiều kích thước khác nhau rồi lấy hiệu hai ảnh làm mờ (Difference of Gaussians - DoG). Các cực trị cục bộ trong không gian này chính là điểm đặc trưng không đổi khi drone bay lên cao hoặc hạ thấp (bất biến tỷ lệ - scale invariance).
- **Gán hướng chủ đạo:** Tính gradient của các pixel xung quanh để xác định hướng chính của điểm. Khi drone xoay ngang/dọc, vector đặc trưng cũng xoay theo (bất biến góc quay - rotation invariance).
- **Tạo vector mô tả:** Cắt vùng $16 \times 16$ pixel quanh điểm, chia thành 16 ô nhỏ ($4 \times 4$), mỗi ô tính histogram gradient theo 8 hướng $\to 16 \times 8 = \mathbf{128}$ **số thực (`float32`)**.

### Đánh giá
- **Ưu điểm:** Cực kỳ chính xác, chịu được drone bay đổi độ cao lớn, xoay góc mạnh, thay đổi ánh sáng tốt.
- **Nhược điểm:** Tính toán phức tạp, tốn CPU/RAM. Khoảng cách so khớp dùng Euclidean (L2-norm) trên vector 128 số thực nên tốc độ match chậm.

---

## 3. ORB (Oriented FAST and Rotated BRIEF)

Được đề xuất bởi Rublee et al. (2011, OpenCV Labs) nhằm thay thế SIFT/SURF với tốc độ cao và miễn phí bản quyền.

### Cách hoạt động
- **Tìm điểm (FAST):** Kiểm tra vòng tròn 16 pixel xung quanh một điểm ảnh. Nếu có chuỗi liên tiếp $\ge 9$ pixel sáng hơn hoặc tối hơn hẳn điểm tâm $\to$ công nhận là điểm góc. Để có hướng, ORB tính trọng tâm cường độ sáng (intensity centroid) quanh điểm đó (gọi là **oFAST**).
- **Tạo vector mô tả (BRIEF):** So sánh độ sáng của từng cặp pixel định sẵn quanh điểm: pixel $A > B \to 1$, ngược lại $\to 0$. ORB xoay ma trận các cặp này theo góc định hướng vừa tìm được để giữ bất biến góc quay (gọi là **rBRIEF**).
- **Kết quả:** Chuỗi **256 bit nhị phân (32 bytes)** (`uint8`).

### Đánh giá
- **Ưu điểm:** Siêu nhanh (nhanh gấp $10 - 20$ lần SIFT). So khớp 2 điểm chỉ cần phép toán XOR bit (khoảng cách Hamming) được tăng tốc phần cứng trực tiếp trên CPU.
- **Nhược điểm:** Nhạy cảm với nhiễu, kém bền vững khi drone thay đổi tỷ lệ quá lớn (zoom/độ cao thay đổi đột ngột) hoặc góc chụp nghiêng phối cảnh mạnh (perspective distortion).

---

## 4. Bảng so sánh trực diện

| Tiêu chí | SIFT | ORB |
|---|---|---|
| **Dạng descriptor** | 128 số thực (`float32`) | 256 bits nhị phân (`uint8`) |
| **Hàm khoảng cách** | Euclidean (L2 Norm) | Hamming Distance (phép XOR bit) |
| **Tốc độ trích xuất & match** | Chậm (~150–300 ms/cặp ảnh 1080p) | Rất nhanh (~15–40 ms/cặp ảnh 1080p) |
| **Bất biến góc xoay (Rotation)** | Rất tốt ($360^\circ$) | Tốt ($360^\circ$) |
| **Bất biến tỷ lệ (Scale/Zoom)** | Xuất sắc (Scale-space DoG) | Khá (dùng Image Pyramid bậc thang) |
| **Cảnh ít vân / lặp vân** | Chịu đựng khá | Dễ bị match sai / mất inliers |
| **Bộ nhớ tiêu hao** | Cao | Rất thấp (32 bytes/descriptor) |

---

## 5. Vai trò trong dự án UAV Mosaicking (AI2002)

1. **Giai đoạn Baseline (Bước 1):**
   - Dùng **SIFT** làm mốc tham chiếu độ chính xác chuẩn (do camera UAV Phantom 3 bay tương đối ổn định).
   - Dùng **ORB** làm mốc tham chiếu về tốc độ tối đa trên CPU.

2. **Giai đoạn Matcher Routing (RQ2):**
   - **Tầng 1 (Mặc định):** Dùng thuật toán nhẹ (ORB hoặc SIFT) để xử lý nhanh các frame bay thẳng, nhiều chi tiết, địa hình phẳng.
   - **Tầng 2 (Dự phòng):** Khi chỉ số rủi ro (RQ1) cảnh báo inlier tụt dốc hoặc cảnh mất chi tiết $\to$ mới kích hoạt Learned Matcher (SuperPoint + LightGlue).
