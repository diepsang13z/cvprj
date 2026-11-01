# RDR-0005: Chốt chính thức dataset NPU Drone-Map

## Status

Accepted

## Date

2026-10-13

## Context

Theo `RDR-0003`, nhóm từng đặt NPU Drone-Map là ưu tiên 1 và giữ DroneZaic (Dryad) làm phương án dự phòng. Tuy nhiên:
- Tại `RDR-0004`, giảng viên hướng dẫn đã yêu cầu nhóm tinh gọn phạm vi, chỉ chọn đúng 1 dataset duy nhất và ưu tiên bộ mới nhất để tối ưu nguồn lực cho sinh viên năm 2.
- Đối chiếu hai tập dữ liệu: DroneZaic đã khá cũ, trong khi NPU Drone-Map mới hơn, cung cấp dữ liệu drone RGB thực tế phong phú, ảnh undistorted chuẩn, kèm file `.SRT`, GPS log và tọa độ điểm kiểm soát mặt đất (GCP) rõ ràng.

## Decision

1. **Chốt NPU Drone-Map là dataset duy nhất** của đề tài cho toàn bộ quá trình phát triển pipeline và thử nghiệm 3 RQ.
2. **Loại bỏ DroneZaic (Dryad):** Không tiếp tục duy trì phương án dự phòng này để tránh phân tán tài nguyên và không phải viết các bộ loader chuyển đổi dữ liệu thừa thãi.
3. **Phạm vi dữ liệu thực thi:**
   - Giai đoạn lập trình khung (baseline): Chạy trên các frame trích xuất mẫu tại `data/sample/` (`rgb01`, `rgb02`).
   - Giai đoạn đánh giá & benchmark diện rộng: Trích xuất một phần đại diện (~10 GB) của NPU Drone-Map để chạy trên Google Colab / Kaggle theo hướng dẫn tại `RDR-0004`.

## Consequence

- Toàn bộ module tiền xử lý dữ liệu (data loader, reader) chỉ cần chuẩn hóa theo cấu trúc của NPU Drone-Map.
- Loại bỏ hoàn toàn khối lượng công việc liên quan đến việc hỗ trợ và stress-test đa dataset.
