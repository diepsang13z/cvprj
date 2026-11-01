# Giải thích và audit: Baseline SIFT & ORB (Classical Mosaicking Baseline)

Đọc cùng notebook [`notebooks/classical_mosaicking_baseline.ipynb`](../../notebooks/classical_mosaicking_baseline.ipynb).
Cập nhật kỹ thuật: **2026-11-01** — Đã hoàn thành toàn bộ sửa đổi kỹ thuật theo `RDR-0010`, `RDR-0011` và `RULES.md §8`.
## 1. Mục tiêu và phạm vi

Ghép tối đa 20 ảnh UAV (hoặc toàn bộ chuỗi ở chế độ full) thành mosaic cục bộ,
so sánh SIFT+BF với ORB+BF. Đây là baseline xử lý hậu kỳ, chạy trên Colab/Kaggle hosted runtime;
tuyệt đối cấm chạy trên CPU laptop cá nhân (`RULES.md §8`). Ảnh không georeference.

## 2. Code làm gì?

1. `load_sequence()` đọc ảnh theo timestamp cùng metadata.
2. `extract_and_match()` tìm keypoint/descriptor, so khoảng cách L2 cho SIFT hoặc Hamming cho ORB,
   rồi lọc bằng ratio test. Inlier không có nghĩa là điểm đúng theo thực địa.
3. `estimate_homography()` dùng RANSAC để tìm H ánh xạ **frame hiện tại về frame trước**.
4. `run_mosaic_pipeline()` tích lũy H; nếu một cặp thất bại thì dừng, không giả vờ ghép đủ.
5. `compute_canvas()` tìm khung chứa các ảnh; warp/blend và lưu H ánh xạ vào chính ảnh mosaic xuất ra.

Blend là trộn kết quả cũ và ảnh mới theo tỷ lệ 50/50 ở vùng chồng.
Ảnh đến sau có trọng số lớn hơn; không phải trung bình đều theo số ảnh, cũng chưa phải xử lý đường nối tối ưu.

## 3. Kết quả đã lưu nói được gì?

Nguồn: `outputs/classical_mosaicking_baseline/<stamp>/metrics_*_20frames.json`.
Các code cell trong notebook đều ở trạng thái sạch (`outputs: []`, `execution_count: null`) sẵn sàng chạy cloud.
| Cấu hình | Frame đã ghép / yêu cầu | `pipeline_total_seconds` |
|---|---|---|
| SIFT+BF | 20/20 | 7,48 s |
| ORB+BF | 20/20 | 3,96 s |

Thời gian này bao gồm đọc ảnh trong pipeline, matching, RANSAC và dựng mosaic;
không gồm ghi PNG/JSON và hiển thị sau khi hàm trả về. Là một lần chạy, không phải kết quả benchmark lặp lại.
Chưa có số đo drift hay kiểm chứng thực địa trong notebook này.
RMSE trên các inlier dùng fit H không đủ để kết luận SIFT ghép đúng hơn ORB trong mọi cảnh.

## 4. Audit: phần đúng và phần còn thiếu

| Hạng mục | Hiện trạng kỹ thuật mới nhất |
|---|---|
| **Cloud Guard & Storage** | Kiểm tra nghiêm ngặt `COLAB_RELEASE_TAG` / `KAGGLE_KERNEL_RUN_TYPE`; fail-closed nếu không mount được `/content/drive/MyDrive`. |
| **Thư mục chạy UTC độc bản** | Xuất vào `OUTPUT_ROOT / "01_classical_baseline" / <RUN_STAMP>`. Từ chối ghi nếu thư mục đã có `completed.json`, bảo vệ artifact lịch sử. |
| **Giải nén an toàn** | `ensure_sequence()` giải nén tự động qua `tarfile.data_filter` chống path traversal, hỗ trợ cả `.tar.gz`, `.tgz`, `.zip`. |
| **Cấu hình linh hoạt** | Đọc `UAV_SEQUENCE` (mặc định `phantom3-village-kfs`) và `UAV_EXECUTION_MODE` (`pilot` hoặc `full`). |
| **Báo cáo trung thực** | Đã sửa: trường hợp không có phép đo hợp lệ báo `None`/`N/A`, không báo nhầm `avg_rmse = 0.0`. |
| **Độ phủ thực tế** | Tiêu đề và metadata hiển thị số frame thực ghép `frames_stitched` thay vì số frame yêu cầu danh định. |
| **Provenance đầy đủ** | Lưu manifest chi tiết gồm ordered frame SHA-256, byte sizes, cấu hình trích xuất, backend `"cpu"`, và marker hoàn tất `completed.json`. |
## 5. Đọc output và dùng lại

- `mosaic_sift_20frames.png`, `mosaic_orb_20frames.png`: ảnh kết quả.
- `metrics_*.json`: `H_to_mosaic`, bản ghi cặp thành công/thất bại, `frames_stitched`, `frames_requested`.
- `manifest.json`: hash SHA-256 từng frame, cấu hình matcher và môi trường run.
- `completed.json`: marker hoàn tất xác nhận toàn bộ cell và artifact đã sinh thành công.

**Kết luận:** Đã hoàn thiện toàn bộ tiêu chuẩn kỹ thuật làm baseline đối chứng cổ điển cho RQ2.
