# Bức tranh dự án (Project Overview)

Tài liệu tóm lược dự án theo cách trực quan, dễ hiểu nhất cho sinh viên thực hiện.

---

## 1. Problem Statement (Bài toán thực tế)

- **Đầu vào:** Video flycam quay từ trên cao nhìn xuống (camera gần như vuông góc với mặt đất).
- **Đầu ra:** Một bức ảnh toàn cảnh duy nhất (aerial mosaic) ghép từ các khung hình trong video.
- **Vấn đề gặp phải:** Khi drone bay, camera bị rung lắc, đổi hướng, hoặc bay qua vùng ít vân bề mặt (mặt cỏ, mặt nước, sân xi măng). Khi đó, các thuật toán ghép ảnh rất dễ bị tính sai toạ độ ghép. Sai một frame sẽ kéo theo cả chuỗi frame sau lệch theo, làm bản đồ bị méo mó, nhân đôi vật thể, hoặc rách nát hoàn toàn (drift tích luỹ).

---

## 2. Nguồn lực & Ràng buộc (Resources & Constraints)

Nhóm không ảo tưởng về tài nguyên, bám sát chỉ đạo tại `RDR-0004`:

- **Nhân lực:** Sinh viên năm 2.
- **Thiết bị:** Laptop cá nhân, không có dàn máy GPU khủng.
- **Môi trường chạy:** Google Colab / Kaggle miễn phí (chấp nhận giới hạn RAM/GPU theo phiên).
- **Dữ liệu:** Cắt 1 phần mẫu khoảng 10 GB (~vài nghìn frame) từ dataset chuẩn **NPU Drone-Map**. Hiện có 8 sequence `-kfs` giải nén tại `data/` (~2,6 GB); chạy thử bằng `data/phantom3-village-kfs/`.
- **Nguyên tắc công nghệ:** Không tự train AI từ đầu. Tận dụng tối đa thuật toán cổ điển (OpenCV) và các mô hình AI mã nguồn mở đã train sẵn tốt nhất hiện nay (SuperPoint, LightGlue).

---

## 3. Research Gap (Khoảng trống nghiên cứu)

Hiện nay trên thế giới:
- **Cách truyền thống (SIFT / ORB):** Chạy rất nhanh, máy yếu cũng chạy được, nhưng gặp cảnh khó (ít chi tiết, đổi góc quay) là ghép hỏng ngay.
- **Cách dùng AI hiện đại (SuperPoint + LightGlue / LoFTR):** Ghép cực chuẩn, chấp mọi cảnh khó, nhưng rất nặng và chạy chậm. Nếu bắt cả video hàng nghìn frame đều chạy qua AI thì máy Colab sẽ sập hoặc chạy mất nhiều tiếng đồng hồ.
- **Khoảng trống:** Chưa có một hệ thống thông minh biết **"liệu cơm gắp mắm"** — cảnh dễ thì chạy cách nhẹ, cảnh khó mới kích hoạt AI; đồng thời khi ghép hỏng thì biết tự phát hiện và tự cứu để không hỏng cả bản đồ.

---

## 4. RQs & Tính đóng góp (Research Questions & Contributions)

Đề tài giải quyết 3 câu hỏi nghiên cứu cốt lõi (`RDR-0003`):

### RQ1: Bắt bệnh sớm (Failure Prediction)
- **Câu hỏi:** Làm sao để biết 2 frame sắp ghép vào nhau có nguy cơ bị lệch/vỡ map mà không cần tốn nhiều công tính toán?
- **Cách làm:** Rút ra các chỉ số đo cực nhanh (số lượng điểm khớp, tỉ lệ điểm chuẩn inlier, độ phân tán của điểm trên ảnh, sai số chiếu lại reprojection error).
- **Đóng góp:** Tìm ra "công thức báo động đỏ" giá rẻ giúp phát hiện rủi ro ghép sai trước khi lỗi lan ra toàn bản đồ.

### RQ2: Phân luồng thông minh (Matcher Routing)
- **Câu hỏi:** Khi nào dùng thuật toán nhẹ (ORB/SIFT), khi nào phải gọi AI xịn (LightGlue)?
- **Cách làm:** Cặp frame an toàn $\rightarrow$ cho thuật toán nhẹ xử lý để lấy tốc độ. Cặp frame bị RQ1 cảnh báo nguy hiểm $\rightarrow$ chuyển sang AI xử lý để lấy độ chính xác.
- **Đóng góp:** Tạo ra pipeline kết hợp đạt được cả 2 mục tiêu: **nhanh gần như thuật toán truyền thống** nhưng **chuẩn gần như AI toàn phần**.

### RQ3: Cơ chế tự cứu (Recovery Mechanisms)
- **Câu hỏi:** Nếu AI cũng bó tay hoặc frame đó quá tệ, làm sao để bản đồ không bị vỡ nát?
- **Cách làm:** Thử nghiệm và so sánh định lượng 3 phương án:
  1. *Bỏ qua frame lỗi:* Không ghép frame đó nữa, đợi frame tiếp theo tốt hơn.
  2. *Rematch với Keyframe:* Không ghép với frame vừa trước nó, mà tìm lại frame mốc chuẩn trước đó để ghép.
  3. *Tách cụm (Submosaic):* Đóng cụm bản đồ cũ lại, tạo cụm bản đồ mới rồi nối 2 cụm sau.
- **Đóng góp:** Đưa ra kết luận thực nghiệm rõ ràng: trong tình huống nào của video drone thì phương án tự cứu nào là tối ưu nhất.

---

## 5. Project Planning (Kế hoạch hành động)

Kế hoạch chia thành 4 bước tuần tự, mỗi bước có sản phẩm cụ thể:

```
[Bước 1: Baseline cổ điển] ──> [Bước 2: Tích hợp AI có sẵn] ──> [Bước 3: Lắp ráp 3 RQ] ──> [Bước 4: Đo đạc & Viết bài]
```

### Bước 1: Dựng khung ghép ảnh cổ điển (Classical Baseline)
- Code pipeline cơ bản bằng Python + OpenCV: Đọc ảnh $\rightarrow$ Trích đặc trưng (ORB/SIFT) $\rightarrow$ Khớp điểm $\rightarrow$ RANSAC tính Homography $\rightarrow$ Warp & Blend.
- Baseline đã chạy trên 20 frame đầu của `data/phantom3-village-kfs/rgb/` trong `notebooks/01_classical_baseline.ipynb`; chất lượng/giới hạn được ghi ở [note audit 01](notebook_01_classical_baseline.md).
- Kết quả cần đạt: Xuất ra được ảnh ghép đầu tiên và file log lưu ma trận toạ độ tích luỹ.

### Bước 2: Tích hợp Learned Matcher có sẵn (AI Baseline)
- Kéo model đã train sẵn (SuperPoint + LightGlue) về chạy thử trên cùng tập frame mẫu.
- Đo đạc thông số: Thời gian chạy mỗi frame, số điểm khớp chuẩn, bộ nhớ tiêu hao.

### Bước 3: Hiện thực hóa 3 RQ
- Lắp module tính chỉ số rủi ro (RQ1).
- Lắp bộ rẽ nhánh Router tự động chọn matcher (RQ2).
- Thử nghiệm 3 nhánh cứu hộ khi gặp cảnh vỡ map (RQ3).

### Bước 4: Chạy Benchmark diện rộng & Viết báo cáo
- Chạy toàn bộ pipeline trên tập dữ liệu ~10 GB của NPU Drone-Map trên Colab/Kaggle.
- Xuất biểu đồ chi phí–chất lượng với phạm vi timing rõ ràng; tách RMSE/inlier nội tại khỏi sai số tham chiếu, và tỷ lệ phủ canvas khỏi diện tích mặt đất. Xem audit [03](notebook_03_all_models.md), [04](notebook_04_drift_evaluation.md), [05](notebook_05_failure_aware_pipeline.md) trước khi dùng số liệu.
- Đưa số liệu thực nghiệm vào báo cáo nghiệm thu cuối kỳ.
