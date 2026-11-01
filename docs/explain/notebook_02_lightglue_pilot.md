# Giải thích và audit Notebook 02: Pilot LightGlue ở ảnh gốc

Đọc cùng notebook [`notebooks/deep_matching_pilot.ipynb`](../../notebooks/deep_matching_pilot.ipynb).
Cập nhật kỹ thuật: **2026-11-01** — Đã hoàn thành toàn bộ sửa đổi kỹ thuật theo `RDR-0010`, `RDR-0011` và `RULES.md §8`.
## 1. Notebook thử điều gì?

Tích hợp hai cấu hình pretrained, không train/fine-tune:

- **SIFT + LightGlue:** wrapper SIFT dùng OpenCV và RootSIFT; LightGlue tìm correspondence.
- **SuperPoint + LightGlue:** SuperPoint tìm keypoint/descriptor; LightGlue tìm correspondence.

Cả hai dùng tối đa 2.000 keypoint, ảnh gốc 1920×1080 và RANSAC 3 px.
Chạy trên Google Colab / Kaggle (GPU T4/A100); nghiêm cấm chạy máy cá nhân (`RULES.md §8`).

## 2. Hai phần thực nghiệm

### Cặp-frame

Chạy 3 cặp liên tiếp đầu `phantom3-village-kfs`, lưu match, inlier, RMSE, H và ảnh minh họa.
Warmup được loại khỏi thời gian đo, setup được ghi riêng; có synchronization khi dùng CUDA.
`match_seconds` gồm extraction, matching và chuyển điểm về CPU;
không gồm đọc ảnh, setup, warmup, RANSAC hoặc vẽ ảnh.
Đường nối inlier cho biết RANSAC giữ cặp điểm đó, chưa chứng minh chúng đúng theo thực địa.

### Mosaic

`build_mosaic()` nối tối đa 20 frame, dừng ở cặp lỗi đầu tiên và lưu `H_to_mosaic`.
`canvas_and_mosaic()` warp và blend 50/50 như Notebook 01.
Đầu vào matching là ảnh gốc; canvas kết quả vẫn có cơ chế giảm kích thước nếu vượt giới hạn 5.000 px.

## 3. Kết quả và trạng thái kỹ thuật

Nguồn: `outputs/02_lightglue_pilot/<stamp>/mosaic_*/metrics.json`.
Các code cell trong notebook đều ở trạng thái sạch (`outputs: []`, `execution_count: null`) sẵn sàng chạy cloud.

| Cấu hình | Frame thực ghép / yêu cầu | `chain_total_seconds` | Phủ canvas |
|---|---|---|---|
| SIFT + LightGlue | 20/20 | 16,657 s | 98,82% |
| SuperPoint + LightGlue | 20/20 | 136,250 s | 98,71% |

`chain_total_seconds` bao gồm matching, RANSAC và warp/blend; không gồm đọc ảnh trước đó, setup,
warmup, ghi file hay hiển thị sau đó. Không cùng phạm vi với `match_seconds`.
Phủ canvas chỉ là tỷ lệ pixel có ảnh, **không phải độ chính xác đăng ký hoặc diện tích mặt đất**.
Chưa có metric drift/ground truth trong notebook này; không đủ để gọi mosaic “không méo” hoặc “cực chuẩn”.

## 4. Audit và giới hạn

| Hạng mục | Hiện trạng kỹ thuật mới nhất |
|---|---|
| **Cloud Guard & Storage** | Kiểm tra môi trường Colab/Kaggle; fail-closed nếu không mount được `/content/drive/MyDrive`. |
| **Thư mục chạy UTC độc bản** | Xuất vào `OUTPUT_ROOT / "02_lightglue_pilot" / <RUN_STAMP>`, từ chối ghi nếu đã có `completed.json`. |
| **Kiểm tra frame tối thiểu** | Xác thực $\ge 2$ frame cho warmup và $\ge 4$ frame cho pilot trước khi load model, chống crash trên sequence ngắn. |
| **Provenance chính xác** | Đọc revision thực tế của LightGlue qua Git/metadata thay vì gán cứng commit string. |
| **Bảo vệ toàn vẹn** | Lưu manifest chi tiết kèm ordered frame SHA-256, backend thiết bị, và marker hoàn tất `completed.json`. |
| **Cấu hình linh hoạt** | Đọc `UAV_SEQUENCE` và `UAV_EXECUTION_MODE` (`pilot` hoặc `full`). |
## 5. Đọc output

- `metrics.json`: tầng cặp, môi trường và định nghĩa timing.
- `*_lightglue_matches.png`: inlier mẫu của cặp đầu.
- `mosaic_sift/`, `mosaic_superpoint/`: mỗi thư mục có `mosaic.png` và `metrics.json`.
- Khi so cấu hình, giữ riêng số frame đã ghép, phạm vi timing và hệ pixel của phép đo.

**Kết luận:** đạt vai trò pilot tích hợp và minh họa mosaic ảnh gốc.
Chưa chứng minh learned matcher tốt hơn classical nói chung; cũng chưa kiểm chứng routing hoặc recovery.
