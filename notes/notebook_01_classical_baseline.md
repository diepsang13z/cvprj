# Giải thích Notebook 01: Ghép ảnh bằng thuật toán cổ điển (SIFT & ORB)

Tài liệu giải thích file `notebooks/01_classical_baseline.ipynb` theo ngôn ngữ bình dân, trực quan cho sinh viên.

---

## 1. File này sinh ra để làm gì?
Mục tiêu là làm ra **một bức ảnh bản đồ lớn (mosaic)** bằng cách lấy 20 bức ảnh chụp liên tiếp từ flycam rồi dán nối chúng lại với nhau.
Ở file này, nhóm chỉ dùng **thuật toán toán học thuần túy của OpenCV (SIFT và ORB)**, hoàn toàn không đụng đến Trí tuệ nhân tạo (AI/Deep Learning).

---

## 2. Các bước chạy trong code (Từng bước làm gì?)

Quy trình ghép ảnh trong notebook trải qua 5 bước chính:

```
[Ảnh 1, Ảnh 2...] 
   ↓ (Bước 1: Tìm điểm đặc trưng)
[Góc nhà, ngã tư, bụi cây]
   ↓ (Bước 2: Nối các điểm giống nhau giữa 2 ảnh)
[Các cặp điểm khớp nhau]
   ↓ (Bước 3: RANSAC - Tìm phép biến đổi toạ độ H)
[Biết Ảnh 2 dịch/xoay bao nhiêu so với Ảnh 1]
   ↓ (Bước 4: Trải tấm vải to (Canvas) & Dán ảnh đè lên)
[Bức ảnh toàn cảnh hoàn chỉnh]
```

### Bước 1 & 2: Tìm điểm và Nối điểm (`extract_and_match`)
- Thuật toán soi vào 2 bức ảnh liền kề để tìm các góc cạnh nổi bật (keypoints).
- Sau đó, nó so sánh xem điểm ở bức ảnh trước tương ứng với điểm nào ở bức ảnh sau.
- Dùng mẹo **Lowe's ratio test** để gạt bỏ các cặp nối "nhìn nhang nhác giống nhau nhưng thực ra là sai".

### Bước 3: Lọc điểm chuẩn và Đo độ lệch (`estimate_homography`)
- Khi nối điểm, thể nào cũng có điểm bị nối nhầm. Thuật toán **RANSAC** như một vị trọng tài: chọn ngẫu nhiên các điểm để tính thử góc quay/độ dịch chuyển, điểm nào đi ngược lại số đông thì bị loại bỏ (outliers), chỉ giữ lại điểm chuẩn (inliers).
- Tính ra ma trận $H$ (Homography $3 \times 3$): đây là "công thức dịch chuyển" giúp bẻ cong và dán bức ảnh này khớp khít vào bức ảnh kia.

### Bước 4: Trải vải to và Dán ảnh (`compute_canvas` & Blending)
- Vì drone bay tiến lên phía trước, bức ảnh sau sẽ bị lệch ra ngoài khung của bức ảnh đầu.
- Code sẽ tính toán diện tích tổng thể của cả 20 bức ảnh để tạo ra một "khung tranh khổng lồ" màu đen (Canvas).
- Dán bức ảnh đầu tiên vào góc, sau đó dùng ma trận $H$ tích lũy để dán tiếp các bức ảnh sau vào đúng toạ độ. Vùng nào 2 ảnh đè lên nhau thì pha trộn 50/50 để viền đỡ bị lộ.

### Bước 5: Chạy đối đầu giữa SIFT và ORB
Notebook chạy thử cả chuỗi 20 frame lần lượt bằng 2 thuật toán:
1. **SIFT:** Chạy kỹ, điểm nối rất chuẩn, đường ghép đẹp nhưng chạy hơi lâu (~8 giây).
2. **ORB:** Chạy lướt, dùng phép toán nhị phân cực nhanh (~3.8 giây), nhưng điểm nối không chuẩn bằng SIFT, ảnh ghép dễ bị méo nhẹ ở viền.

---

## 3. Kết quả đầu ra nằm ở đâu?
Sau khi bấm Run All, file sẽ lưu kết quả vào `notebooks/outputs/01_classical_baseline/phantom3-village-kfs/`:
- `mosaic_sift_20frames.png`: Bức ảnh toàn cảnh ghép bằng SIFT.
- `mosaic_orb_20frames.png`: Bức ảnh toàn cảnh ghép bằng ORB.
- `metrics_*.json`: File nhật ký ghi lại chi tiết từng frame mất bao nhiêu mini-giây, tìm được bao nhiêu điểm chuẩn và sai số bao nhiêu pixel.

---

## 4. Tóm tắt 1 câu
> **Notebook 01 là bài kiểm tra cơ bản nhất: dùng toán hình học thuần túy của OpenCV để ghép 20 ảnh drone thành 1 bản đồ lớn và so sánh xem giữa SIFT (chính xác) và ORB (nhanh) cái nào tối ưu hơn.**
