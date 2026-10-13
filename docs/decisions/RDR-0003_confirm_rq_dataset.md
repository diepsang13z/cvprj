# RDR-0003: Chốt RQs và Dataset

## Status

Accepted

## Date

2026-09-19

## Decision

### 1. Bộ câu hỏi nghiên cứu (RQs)

Chốt chính thức bộ 3 RQ cốt lõi theo hướng **Failure-Aware Mosaicking** (dùng chung một pipeline và một evaluation harness):

- **RQ1 (Failure Prediction):** Xác định các chỉ báo rẻ ở cấp cặp-frame (inlier count/ratio, reprojection error, overlap, spatial distribution) để dự báo lỗi đăng ký và drift tích luỹ trên toàn mosaic.
- **RQ2 (Matcher Routing):** Đánh giá hiệu quả của chính sách phân luồng 2 tầng (mặc định dùng classical matcher nhẹ, chỉ kích hoạt learned matcher như SIFT+LightGlue khi rủi ro cao) trên trade-off giữa chất lượng ghép và độ trễ ở cấp độ mosaic.
- **RQ3 (Recovery):** So sánh có kiểm soát 3 cơ chế phục hồi (loại bỏ frame / rematch keyframe / tách submosaic) dưới cùng một ngưỡng kích hoạt (confidence trigger) để giới hạn drift.

**Kế hoạch mở rộng (RQ5):**
- **RQ5 (Edge/Hardware Optimization):** Tối ưu độ trễ/RAM trên phần cứng nhúng (Raspberry Pi/Jetson). RQ này **tạm hoãn** và chỉ được xem xét thực hiện nếu còn thời gian sau khi đã hoàn thành trọn vẹn 3 RQs cốt lõi.

### 2. Lựa chọn Dataset

Căn cứ theo RDR-0002 (mở và dữ liệu drone thật), lựa chọn bộ dữ liệu theo thứ tự ưu tiên:

1. **Ưu tiên số 1 (Dataset chính): NPU Drone-Map**
   - Cung cấp đầy đủ video drone RGB thực tế, ảnh undistorted, file phụ đề `.SRT`, log GPS và các điểm kiểm soát mặt đất (GCP) phục vụ đo lường sai số.
   - Dùng để chạy thử nghiệm chính cho toàn bộ 3 RQ.

2. **Phương án dự phòng & Stress-test: DroneZaic (Dryad)**
   - Đóng vai trò phương án dự phòng chính thức nếu việc truy cập hoặc tải NPU Drone-Map gặp sự cố.
   - Được dùng làm tập dữ liệu thử thách (stress-test) cho các cảnh địa hình khó (đặc trưng lặp vân nông nghiệp).

### 3. Nguyên tắc thực thi kế tiếp

- Tiến hành xây dựng bản MVP hoàn chỉnh (1 video $\to$ 1 mosaic 2D) trước khi dựng evaluation harness cho 3 RQ.
- Thiết kế pipeline và module interface đảm bảo không gắn cứng (hardcode) với bất kỳ dataset cụ thể nào.
