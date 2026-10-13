# Giải thích Notebook 03: Đấu trường 7 mô hình và phát hiện ca vỡ bản đồ thật

Tài liệu giải thích file `notebooks/03_all_models.ipynb` theo ngôn ngữ bình dân, trực quan cho sinh viên.

---

## 1. File này sinh ra để làm gì?

Đây là **file thực nghiệm lớn nhất và quan trọng nhất** của giai đoạn khảo sát mô hình.
Thay vì thử lắt nhắt từng cái, notebook này đưa **tất cả 7 cấu hình thuật toán và AI** vào cùng một "đấu trường", ép chúng chạy trên cùng tập dữ liệu, cùng độ phân giải (nén về cạnh 640 pixel để chạy nhanh trên máy cá nhân) và xuất ra báo cáo web HTML đối chiếu toàn diện.

---

## 2. Danh sách 7 "đối thủ" tham gia đấu trường

1. **`sift_bf`:** SIFT cổ điển của OpenCV (Chuẩn mực truyền thống).
2. **`orb_bf`:** ORB cổ điển của OpenCV (Tốc độ ánh sáng, siêu nhẹ).
3. **`sift_lightglue`:** Con lai giữa SIFT truyền thống và AI LightGlue.
4. **`superpoint_lightglue`:** Bộ đôi AI nổi tiếng của giới thị giác máy tính.
5. **`xfeat_mnn`:** Mô hình AI siêu nhẹ (CVPR 2024), thiết kế riêng để chạy thời gian thực trên robot/drone.
6. **`xfeat_lighterglue`:** XFeat kết hợp với phiên bản thu nhỏ của LightGlue (vừa nhanh vừa chính xác).
7. **`efficientloftr`:** Mô hình AI không cần tìm điểm góc (detector-free, CVPR 2024), chuyên trị các cảnh trơn nhẵn mất chi tiết.

---

## 3. Hai tầng thực nghiệm trong Code

Code chia làm 2 tầng rõ rệt:

### Tầng 1: So khớp cặp frame lẻ (`pairs/`)

- Cho từng mô hình chạy thử trên 3 cặp ảnh đầu tiên của cả 2 cảnh: cảnh dễ (`village` - ruộng đồng) và cảnh khó (`grass` - bãi cỏ trơn nhẵn).
- Đo đạc: Số điểm nối được, số điểm chuẩn (inliers), sai số RMSE và thời gian tính toán của 1 cặp ảnh.

### Tầng 2: Nối liên hoàn 20 frame để tạo Full bản đồ (`mosaic/`)

- Lấy 20 bức ảnh liên tiếp, ép từng mô hình phải nối dồn từ ảnh 1 đến ảnh 20 để tạo ra bức ảnh panorama to đùng.
- Kiểm tra xem ma trận toạ độ cộng dồn có bị "lệch lạc" làm rách bản đồ hay không.
- Vẽ toàn bộ 7 bức ảnh bản đồ của từng sequence lên màn hình notebook để mắt người so sánh trực quan.

---

## 4. Phát hiện "đắt giá" nhất cho bài nghiên cứu (Research Finding)

Khi chạy xong tầng 2, một phát hiện cực kỳ thú vị đã xuất hiện:

- **6 mô hình đầu tiên (SIFT, ORB, LightGlue, XFeat):** Đều ghép ra bản đồ **rất đẹp, liền mạch**, ruộng đồng thẳng thớm, độ phủ đạt 96% - 99%. Trong đó `orb_bf` và `xfeat_mnn` chạy siêu nhanh (~0.5 - 2 giây cho cả 20 frame).
- **Riêng `efficientloftr` bị VỠ NÁT BẢN ĐỒ:**
  - Khung ảnh bị kéo giãn xiên xẹo thành một vệt chéo dị dạng, diện tích phủ tụt xuống chỉ còn **55.6%**.
  - **Điểm nghịch lý:** Ở Tầng 1, `efficientloftr` báo cáo số liệu **đẹp như mơ** (hơn 2.600 điểm nối, hơn 2.000 điểm inlier, sai số RMSE cực nhỏ). Nhưng khi tích lũy dồn qua 20 frame, sai số góc quay nhỏ tích tụ dần khiến cả bản đồ bị vặn xoắn hoàn toàn!

> 💡 **Ý nghĩa khoa học:** Đây chính là **bằng chứng thực tế đầu tiên** chứng minh cho câu hỏi nghiên cứu **RQ1** của nhóm: _Chỉ nhìn vào số lượng điểm inlier của từng cặp frame là KHÔNG ĐỦ để kết luận bản đồ có ghép thành công hay không. Phải có cơ chế dự báo rủi ro trôi dạt (drift) tích luỹ._

---

## 5. Kết quả đầu ra nằm ở đâu?

Toàn bộ kết quả được tự động lưu theo từng mốc thời gian tại:
`notebooks/outputs/03_all_models/<ngày_giờ>/`

- `index.html`: **Trang web báo cáo tổng hợp** hiển thị đầy đủ bảng biểu so sánh và 28 bức ảnh đối chiếu trực tiếp.
- `summary.csv`: File Excel số liệu của Tầng 1 (cặp frame).
- `mosaic_summary.csv`: File Excel số liệu của Tầng 2 (toàn cảnh bản đồ: diện tích, độ phủ, thời gian).
- `pairs/`: Chứa ảnh nối điểm và file toạ độ `.npz` của từng cặp.
- `mosaic/`: Chứa file ảnh bản đồ to `mosaic.png` của từng mô hình.

---

## 6. Tóm tắt 1 câu

> **Notebook 03 là bài test tổng lực đem cả 7 mô hình ra chạy đua để vừa đo đạc tốc độ/độ chính xác, vừa xuất ra bản đồ toàn cảnh và phát hiện ra ca ghép hỏng thực tế làm bằng chứng cho đề tài.**
