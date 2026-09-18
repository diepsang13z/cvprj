# AGENTS

## Dự án
Xây dựng bản đồ ảnh 2D (aerial mosaic) từ video UAV: trích frame → ghép ảnh dựa trên đặc trưng.
Đầu vào: video UAV (hoặc thư mục frame). Đầu ra: ảnh mosaic + metadata.
Kết quả không georeference — đây là ảnh hiện trạng cục bộ, không phải bản đồ địa lý chính xác.

Trong phạm vi: video UAV ngắn, camera gần nadir, cảnh tương đối phẳng; pipeline cổ điển (ORB/SIFT → matching → RANSAC/homography → warp/blend) kèm eval harness.
Ngoài phạm vi: GPS/IMU bắt buộc, 3D/SLAM, realtime, khảo sát độ chính xác cao, cơ chế bay.

Ràng buộc thiết kế giữ từ đầu (phục vụ kế thừa drone, không phải yêu cầu học kỳ):
- Module interface cố định, không hardcode dataset/path.
- Lưu **ma trận homography tích luỹ** frame → hệ toạ độ mosaic, không chỉ ảnh kết quả.
- Log metric mỗi lần chạy ra CSV/JSON (số frame, inlier, RMSE, thời gian, % phủ).

## Quy tắc đọc tài liệu (bắt buộc)
1. Đọc `docs/INDEX.md` trước. Đó là router: file | mục đích | đọc khi nào | ~số dòng.
2. Trạng thái hiện tại: `STATUS.md` — ảnh chụp, ghi đè khi đổi; không chép lịch sử vào đó.
3. Chỉ mở file theo cột "Đọc khi nào". Không đọc cả `docs/` để "nắm bối cảnh".
4. `docs/logs/` là nhật ký trao đổi, chưa chắt lọc, dài — chỉ đọc khi cần truy lý do gốc.
5. `docs/decisions/` là nguồn sự thật cho việc đã chốt. Đọc file số lớn nhất trước; append-only, không sửa file cũ.
6. Mâu thuẫn giữa `AGENTS.md` / `STATUS.md` / `INDEX.md` với `docs/decisions/` → decisions thắng.
7. `RULES.md` là ràng buộc cứng, đọc khi chuẩn bị tạo/sửa file.

## Khi thêm tài liệu
- File context mới → thêm một dòng vào `docs/INDEX.md`. Không có dòng trong INDEX = file vô hình với agent sau.
- Trạng thái đổi → sửa `STATUS.md`, không tạo file mới.
- Quyết định mới → `docs/decisions/NNNN_<slug>.md`, số kế tiếp, không sửa/không xóa file cũ.
- Nhật ký/trao đổi dài → `docs/logs/<chủ-đề>/NNNN_<slug>.md`, chỉ liệt kê ở INDEX, không cần tóm tắt.
- File context ≤ 200 dòng (trừ `docs/logs/`).
