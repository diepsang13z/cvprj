# Bức tranh dự án (Project Overview)

Tài liệu tóm lược dự án theo cách trực quan, dễ hiểu nhất cho sinh viên thực hiện.

---

## 1. Problem Statement (Bài toán thực tế)

- **Đầu vào:** Video flycam quay từ trên cao nhìn xuống (camera gần như vuông góc với mặt đất).
- **Đầu ra:** Một bức ảnh toàn cảnh duy nhất (aerial mosaic) ghép từ các khung hình trong video.
- **Vấn đề gặp phải:** Khi drone bay, camera bị rung lắc, đổi hướng, hoặc bay qua vùng ít vân bề mặt (mặt cỏ, mặt nước, sân xi măng). Khi đó, các thuật toán ghép ảnh rất dễ bị tính sai toạ độ ghép. Sai một frame sẽ kéo theo cả chuỗi frame sau lệch theo, làm bản đồ bị méo mó, nhân đôi vật thể, hoặc rách nát hoàn toàn (drift tích luỹ).

---

## 2. Nguồn lực & Ràng buộc (Resources & Constraints)

Nhóm không ảo tưởng về tài nguyên, bám sát chỉ đạo tại `RDR-0004`, `RDR-0010` và `RULES.md §8`:

- **Nhân lực:** Sinh viên năm 2.
- **Thiết bị:** Laptop cá nhân; **tuyệt đối không chạy mô hình hoặc pipeline thực nghiệm trên CPU laptop cá nhân** (`RULES.md §8`, `RDR-0010`). Máy cá nhân chỉ dùng để kiểm tra tĩnh, review code và quản lý repo.
- **Môi trường chạy:** Google Colab / Kaggle (GPU T4/A100) hosted runtimes. Kết quả bắt buộc lưu trữ bền vững trên Google Drive đã mount.
- **Dữ liệu:** Dataset mở từ drone thật **NPU Drone-Map** (`RDR-0005`), lưu trên Google Drive theo cấu trúc `MyDrive/mosaicking_from_uav_video_research/dataset/<sequence>/rgb/*.jpg`.
- **Nguyên tắc công nghệ:** Không tự train AI từ đầu. Tận dụng thuật toán cổ điển (OpenCV SIFT/ORB) và các mô hình AI mã nguồn mở đã train sẵn tốt nhất (SuperPoint, LightGlue, XFeat, Efficient LoFTR) theo `RDR-0006`.

---

## 3. Research Gap (Khoảng trống nghiên cứu)

Hiện nay trên thế giới:
- **Cách truyền thống (SIFT / ORB):** Chạy rất nhanh, máy yếu cũng chạy được, nhưng gặp cảnh khó (ít chi tiết, đổi góc quay) là ghép hỏng ngay.
- **Cách dùng AI hiện đại (SuperPoint + LightGlue / LoFTR):** Ghép cực chuẩn, chấp mọi cảnh khó, nhưng rất nặng và chạy chậm. Nếu bắt cả video hàng nghìn frame đều chạy qua AI thì máy Colab sẽ sập hoặc chạy mất nhiều tiếng đồng hồ.
- **Khoảng trống:** Chưa có một hệ thống thông minh biết **"liệu cơm gắp mắm"** — cảnh dễ thì chạy cách nhẹ, cảnh khó mới kích hoạt AI; đồng thời khi ghép hỏng thì biết tự phát hiện và tự cứu để không hỏng cả bản đồ.

---

## 4. RQs & Tính đóng góp (Research Questions & Contributions)

Đề tài giải quyết 3 câu hỏi nghiên cứu cốt lõi (`RDR-0003`) theo giao thức đánh giá **Leave-One-Sequence-Out (LOSO)** (`RDR-0011`):

### RQ1: Bắt bệnh sớm (Failure Prediction)
- **Câu hỏi:** Làm sao để biết 2 frame sắp ghép vào nhau có nguy cơ bị lệch/vỡ map mà không cần tốn nhiều công tính toán?
- **Cách làm:** Rút ra các chỉ báo rẻ (số inlier, tỷ lệ inlier, độ phân tán điểm, sai số chiếu lại, tương quan ảnh sau biến đổi Patch NCC).
- **Đóng góp:** Phát hiện số lượng match/inlier có thể gây ngộ nhận ở địa hình lặp; Patch NCC phản ánh tốt hơn độ bất đồng cấp bước so với matcher tham chiếu chất lượng cao.

### RQ2: Phân luồng thông minh (Matcher Routing)
- **Câu hỏi:** Khi nào dùng thuật toán nhẹ (ORB/SIFT), khi nào phải gọi AI (LightGlue / SuperPoint)?
- **Cách làm:** Cặp frame an toàn $\rightarrow$ chạy matcher nhẹ để lấy tốc độ. Cặp frame bị chỉ báo rủi ro gắn cờ $\rightarrow$ leo thang sang learned matcher hoặc ảnh gốc.
- **Đóng góp:** Tìm kiếm điểm cân bằng Pareto: chất lượng tương đương mô hình học sâu toàn phần nhưng độ trễ tiệm cận thuật toán cổ điển. Ngưỡng phân luồng được hiệu chỉnh theo giao thức LOSO (`RDR-0011`).

### RQ3: Cơ chế tự cứu (Recovery Mechanisms)
- **Câu hỏi:** Khi rủi ro vượt ngưỡng hoặc matcher bế tắc, làm sao để hạn chế trôi dạt sai số mà vẫn giữ được dữ liệu?
- **Cách làm:** Đặt 4 chính sách lên cùng một bàn cân dưới cùng ngưỡng rủi ro của fold LOSO:
  1. *Không cứu (None):* Tiếp tục ghép chuỗi liên tục dù có rủi ro.
  2. *Bỏ qua frame lỗi (Drop):* Bỏ frame hiện tại, nhảy cóc sang frame kế tiếp.
  3. *Rematch với Keyframe (Anchor):* Thử ghép ngược về các frame mốc tin cậy đã đặt trong lịch sử.
  4. *Tách cụm (Submosaic Split):* Đóng cụm bản đồ con hiện tại, mở cụm mosaic mới để ngắt chuỗi tích luỹ lỗi.
- **Đóng góp:** So sánh định lượng công bằng giữa các cơ chế phục hồi trên cùng tập dữ liệu chuẩn. Các giá trị ngưỡng và chính sách tối ưu hiện tại ở trạng thái khám phá (`RDR-0008` Proposed), chờ kiểm chứng trên toàn bộ dataset qua LOSO.

---

## 5. Project Planning (Kế hoạch hành động)

Kế hoạch chia thành 4 bước tuần tự, mỗi bước có sản phẩm cụ thể:

```
[Bước 1: Baseline cổ điển] ──> [Bước 2: Pilot học sâu] ──> [Bước 3: Benchmark 7 mô hình] ──> [Bước 4: Đánh giá Drift & Failure-Aware]
```

### Bước 1: Dựng khung ghép ảnh cổ điển (Classical Baseline)
- Code pipeline cơ bản bằng Python + OpenCV trong `notebooks/classical_mosaicking_baseline.ipynb`: đọc ảnh $\rightarrow$ trích đặc trưng (ORB/SIFT) $\rightarrow$ RANSAC tính Homography $\rightarrow$ warp & blend.
- Lưu ma trận toạ độ tích luỹ `H_to_mosaic`, chạy trên Colab/Kaggle với thư mục output độc bản UTC và manifest kèm hash SHA-256. Chi tiết tại [audit baseline](classical_mosaicking_baseline.md).

### Bước 2: Tích hợp Learned Matcher có sẵn (AI Baseline)
- Khảo sát mô hình pretrained (SIFT/SuperPoint + LightGlue) trên ảnh gốc 1920×1080 trong `notebooks/deep_matching_pilot.ipynb`.
- Đo đạc thời gian sau warmup, số inliers, RMSE và xuất mosaic 20 frame. Chi tiết tại [audit deep matching](deep_matching_pilot.md).

### Bước 3: Benchmark chuẩn hoá 7 mô hình
- So sánh có hệ thống 7 cấu hình ở cùng độ phân giải 640 px trong `notebooks/feature_matcher_benchmark.ipynb`.
- Tối ưu bộ nhớ $O(1)$ qua nạp ảnh lười theo cặp (lazy streaming), hỗ trợ chế độ pilot và full, xuất `completed.json` sau cùng. Chi tiết tại [audit benchmark](feature_matcher_benchmark.md).

### Bước 4: Đánh giá Drift Tự nhất quán & Pipeline Failure-Aware
- Đo sai số trôi tích luỹ Chain-vs-Direct (`RDR-0007`) và so sánh trên tập đối chiếu chung (common eligible frames) trong `notebooks/accumulated_drift_evaluation.ipynb`. Chi tiết tại [audit drift](accumulated_drift_evaluation.md).
- Hiện thực hoá 3 RQ theo giao thức LOSO (`RDR-0011`) trong `notebooks/failure_aware_mosaicking_pipeline.ipynb`: kiểm định chỉ báo RQ1, mô phỏng routing RQ2 và đánh giá 4 chính sách phục hồi RQ3. Chi tiết tại [audit failure-aware](failure_aware_mosaicking_pipeline.md).
