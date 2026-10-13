# Agent Guidance & Project Context

Tài liệu định vị phạm vi và hướng dẫn cách tiếp cận context cho các Agent làm việc trên dự án **UAV 2D Aerial Mosaicking**.

---

## 1. Bài toán & Đề tài

Xây dựng bản đồ ảnh 2D (aerial mosaic) từ video UAV: trích frame → ghép ảnh dựa trên đặc trưng (ORB/SIFT → matching → RANSAC/homography → warp/blend). Đầu vào là video UAV (hoặc thư mục frame); đầu ra là ảnh mosaic + metadata.

- Kết quả **không georeference** — là ảnh hiện trạng cục bộ, không phải bản đồ địa lý chính xác.
- Pipeline cổ điển kèm evaluation harness.
- Hướng nghiên cứu đã chốt (RDR-0003): **Failure-Aware Mosaicking** — dùng chỉ báo rẻ dự báo lỗi đăng ký, phân luồng matcher theo rủi ro, và cơ chế phục hồi để giới hạn drift.

### Ba câu hỏi nghiên cứu (RDR-0003)

- **RQ1 (Failure Prediction):** chỉ báo rẻ cấp cặp-frame (inlier count/ratio, reprojection error, overlap, spatial distribution) dự báo lỗi đăng ký và drift tích luỹ.
- **RQ2 (Matcher Routing):** phân luồng 2 tầng (classical nhẹ mặc định; chỉ kích hoạt learned matcher khi rủi ro cao) trên trade-off chất lượng–độ trễ.
- **RQ3 (Recovery):** so sánh 3 cơ chế phục hồi (loại frame / rematch keyframe / tách submosaic) dưới cùng ngưỡng kích hoạt.

## 2. Phạm vi (Scope)

### Trong phạm vi

- Video UAV ngắn, camera gần nadir, cảnh tương đối phẳng.
- Pipeline cổ điển (ORB/SIFT → matching → RANSAC/homography → warp/blend) kèm eval harness.
- Ràng buộc thiết kế giữ từ đầu (phục vụ kế thừa drone):
  - Module interface cố định, **không hardcode** dataset/path.
  - Lưu **ma trận homography tích luỹ** frame → hệ toạ độ mosaic, không chỉ ảnh kết quả.
  - Log metric mỗi lần chạy ra CSV/JSON (số frame, inlier, RMSE, thời gian, % phủ).

### Ngoài phạm vi

- GPS/IMU bắt buộc, 3D/SLAM, realtime.
- Khảo sát độ chính xác cao, cơ chế bay.

## 3. Quy tắc đọc tài liệu & tiếp nhận context (Navigation Protocol)

Mỗi Agent khi bắt đầu phiên mới đọc lướt theo thứ tự tối giản:

1. **Bước 1 — `docs/INDEX.md`:** router tài liệu; định vị cấu trúc.
2. **Bước 2 — `RULES.md`:** nắm giới hạn 200 dòng, kỷ luật Git, nơi ghi quyết định/việc mở/nhật ký.
3. **Bước 3 — RDR liên quan trong `docs/decisions/`:** đọc theo chủ đề đang làm; file số lớn nhất là quyết định mới nhất.
4. **Bước 4 — GitHub Issues và `docs/logs/`:** Issues là việc đang mở; log ghi việc đã xảy ra, không thay cho Issues.
5. **Bước 5 — Không đọc tràn lan `docs/logs/`:** chỉ mở log cụ thể khi nhiệm vụ hiện tại yêu cầu.

## 4. Dữ liệu (Dataset)

- Dataset UAV **opensource, dữ liệu drone thật** (RDR-0002).
- Ưu tiên 1: **NPU Drone-Map** (video RGB, ảnh undistorted, `.SRT`, log GPS, GCP); dự phòng: **DroneZaic (Dryad)**.
- GVHD cho phép chạy **một phần** dataset (~10 GB) trên Colab/Kaggle do nhóm chỉ có laptop cá nhân (RDR-0004).
- Thư mục `data/` là dữ liệu mẫu để thử nghiệm; không hardcode đường dẫn vào code.

## 5. Khi thêm tài liệu

- File context mới → thêm một dòng vào `docs/INDEX.md`. Không có dòng trong INDEX = file vô hình với agent sau.
- Quyết định mới → `docs/decisions/RDR-NNNN_<slug>.md`, số kế tiếp, không sửa/không xoá file cũ.
- Nhật ký/trao đổi dài → `docs/logs/<chủ-đề>/<NNNN>_<slug>.md`, chỉ liệt kê ở INDEX.
- File context ≤ 200 dòng (trừ `docs/logs/`).
