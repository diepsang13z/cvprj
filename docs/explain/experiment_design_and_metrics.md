# Thiết kế Thực nghiệm và Đo lường (Experiment Design & Metrics)

Tài liệu hệ thống hoá quy chuẩn thiết kế thực nghiệm, giao thức kiểm định và các thước đo (metrics) áp dụng xuyên suốt dự án Failure-Aware Aerial Mosaicking.

---

## 1. Mục tiêu Nghiên cứu và 3 Câu hỏi Cốt lõi (RQs)

Dự án giải quyết bài toán ghép ảnh UAV 2D trong điều kiện cảnh khó (đồng nhất, trôi dạt tích luỹ) theo RDR-0003:
- **RQ1 (Failure Prediction):** Các chỉ báo rẻ cấp cặp ảnh (photo NCC, inlier ratio, inlier count, spatial spread...) có dự báo tin cậy lỗi đăng ký homography không?
- **RQ2 (Matcher Routing):** Phân luồng 2 tầng (mặc định matcher cổ điển rẻ; chỉ kích hoạt learned matcher khi chỉ báo vượt ngưỡng rủi ro) tối ưu trade-off giữa độ trễ và chất lượng thế nào?
- **RQ3 (Recovery Mechanisms):** Dưới cùng ngưỡng rủi ro kích hoạt, cơ chế phục hồi nào (bỏ qua frame / neo lại keyframe cũ / tách submosaic) hạn chế vỡ hình tốt nhất?

---

## 2. Thiết kế Thực nghiệm (Experimental Design)

### 2.1. Giao thức Đánh giá LOSO (Leave-One-Sequence-Out)
Theo RDR-0011, để đánh giá khả năng tổng quát hoá mà không bị rò rỉ dữ liệu (data leakage) do tương quan thời gian giữa các frame liên tiếp:
- **Chia theo sequence:** Với $N$ chuỗi video UAV, thực hiện $N$ fold. Mỗi fold giữ lại 1 sequence làm tập kiểm thử (test sequence), dùng $N-1$ sequence còn lại để hiệu chỉnh ngưỡng ($\tau$).
- **Không chọn lại ngưỡng trên test sequence:** Ngưỡng tối ưu từ tập train được áp nguyên sang test fold.
- **Tính minh bạch lịch sử:** Hai cửa sổ `village` (frame 80-125) và `grass` (frame 0-45) từng được dùng khám phá chỉ báo phải được nêu rõ giới hạn, không coi là hoàn toàn mù với thiết kế phương pháp.

### 2.2. Phân định Chế độ Thực thi (Execution Modes)
- **Pilot Mode:** Chạy trên cửa sổ nhỏ (3 cặp ảnh / 20 frame) để kiểm tra khói (smoke test), xác thực môi trường và luồng dữ liệu trong vài phút.
- **Full Mode:** Chạy toàn bộ frame của toàn bộ sequence có trong dataset để thu thập số liệu khoa học đầy đủ.

### 2.3. Quy chuẩn Môi trường Cloud
Tuân thủ RULES.md §8: 100% thực nghiệm chạy trên Google Colab / Kaggle hosted runtime (ưu tiên T4 GPU cho deep models). Máy cá nhân chỉ phục vụ kiểm tra tĩnh AST, cú pháp và đường dẫn.

---

## 3. Hệ thống Thước đo (Measurement Metrics)

### 3.1. Thước đo Cấp Cặp ảnh (Pair-level Matching)
- **Số lượng Inliers ($N_{in}$):** Số cặp điểm tương đồng thoả mãn mô hình hình học sau RANSAC.
- **Inlier Ratio ($R_{in}$):** Tỷ lệ $N_{in} / N_{raw\_matches}$.
- **RMSE Inlier:** Căn bậc hai trung bình bình phương sai số tái chiếu của các điểm inlier (đơn vị pixel). *Lưu ý:* RMSE inlier thấp không đồng nghĩa homography đúng trên toàn cảnh nếu điểm phân bố hẹp.

### 3.2. Sai số Đăng ký Cấp bước (Step-level Registration Error)
Đo sai lệch giữa ma trận homography bước $H_{i \rightarrow i-1}$ do mô hình dự đoán so với ma trận tham chiếu $H_{ref}$:
- **Cổng Hợp lệ Tham chiếu (RDR-0007):** $H_{ref}$ chỉ được công nhận khi matcher tham chiếu mạnh đạt $\ge 100$ inliers. Nếu không đạt cổng, phép đo ghi nhận `None` / `N/A`, tuyệt đối không ghi bằng 0.
- **Sai số bước ($E_{step}$):** Khoảng cách Euclid trung bình giữa 4 góc ảnh (hoặc lưới điểm) khi nhân qua $H$ so với $H_{ref}$ (đơn vị pixel ảnh gốc).

### 3.3. Độ trôi Tích luỹ (Accumulated Drift - Chain vs Direct)
Theo RDR-0007, không dùng `trajectory.txt` làm ground truth tuyệt đối do chưa độc lập và có thể suy biến mặt phẳng:
- **Nguyên lý Chain-vs-Direct:** So sánh phép biến đổi tích luỹ tuần tự (chain: $H_{0 \rightarrow k} = H_{k-1 \rightarrow k} \dots H_{0 \rightarrow 1}$) với phép đăng ký trực tiếp từ frame $k$ về frame 0 (direct: $H_{0 \rightarrow k}^{direct}$).
- **Tập đối chiếu chung (Common Eligible Frames):** Chỉ tính drift trên các frame mà matcher tham chiếu ghép trực tiếp về frame 0 đạt đủ cổng $\ge 100$ inliers và có diện tích giao nhau hợp lệ.
- **Đơn vị:** Pixel trên toạ độ ảnh gốc.

### 3.4. Thước đo Đánh giá Chỉ báo Rủi ro (RQ1 Metrics)
- **Hệ số Tương quan Hạng Spearman ($\rho$):** Đo mức độ tương quan đơn điệu giữa giá trị chỉ báo và sai số thực tế từng bước.
- **AUC-ROC:** Diện tích dưới đường cong ROC khi dùng chỉ báo để phân loại nhị phân bước ghép lỗi ($E_{step} > 2.0$ px). Hướng dự báo tuân thủ nghiêm ngặt bảng định hướng khai báo trước (`INDICATOR_SUSPICION`).

### 3.5. Thước đo Phân luồng và Đánh đổi (RQ2 Metrics)
- **Độ trễ trung bình mỗi bước (Latency / Step Runtime):** Thời gian tính toán đặc trưng và so khớp (tính bằng giây).
- **Tỷ lệ Leo thang (% Escalated Steps):** Tỷ lệ phần trăm số bước phải kích hoạt matcher tầng 2 (deep model).
- **Đường cong Đánh đổi Pareto:** Biểu đồ tương quan giữa độ trôi tích luỹ (Drift) và độ trễ (Latency) qua các ngưỡng kích hoạt $\tau$.

### 3.6. Thước đo Phục hồi Bản đồ (RQ3 Metrics)
- **Tỷ lệ Giữ Frame (% Retained Frames):** Tỷ lệ frame đưa vào canvas thành công trên tổng số frame đầu vào.
- **Số Mảnh ghép (Number of Submosaics):** Số phân vùng bản đồ độc lập khi kích hoạt chính sách tách (split).
- **Chất lượng Mảnh lớn nhất:** Độ phủ diện tích canvas và độ trôi đo trên mảnh ghép có kích thước lớn nhất.

---

## 4. Nguyên tắc Toàn vẹn Dữ liệu Thực nghiệm (Provenance)

1. **Không suy diễn số liệu thiếu:** Trường hợp mất dấu, thiếu overlap hoặc matcher thất bại phải đánh dấu `null` / `failed`, không được thay thế bằng sai số 0.
2. **Thư mục chạy độc bản UTC:** Mỗi run lưu trữ trong thư mục timestamp riêng (ví dụ `outputs/<experiment>/<UTC_STAMP>/`), chứa đầy đủ `manifest.json`, hash SHA-256 ảnh đầu vào, tham số đo và phiên bản thư viện.
3. **Marker hoàn tất (`completed.json`):** File `completed.json` chỉ được ghi ở cell cuối cùng sau khi toàn bộ artifact và self-check đã vượt qua. Tuyệt đối không đọc output từ run chưa có `completed.json`.
