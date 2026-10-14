# Giải thích và audit Notebook 02: Pilot LightGlue ở ảnh gốc

Đọc cùng [notebook](../notebooks/02_lightglue_pilot.ipynb).
Audit 2026-10-14: `ANALYZED` — đối chiếu code/artifact và kiểm tra hình học cô lập, chưa chạy lại model.

## 1. Notebook thử điều gì?

Tích hợp hai cấu hình pretrained, không train/fine-tune:

- **SIFT + LightGlue:** wrapper SIFT dùng OpenCV và RootSIFT; LightGlue tìm correspondence.
- **SuperPoint + LightGlue:** SuperPoint tìm keypoint/descriptor; LightGlue tìm correspondence.

Cả hai dùng tối đa 2.000 keypoint, ảnh gốc 1920×1080 và RANSAC 3 px.
`resize=None` nghĩa là không resize trong extractor, không có nghĩa JPEG nguồn chưa bị nén.
Đây là pilot trên máy hiện tại; không kiểm chứng khả năng chạy realtime hoặc mức tiêu thụ pin của drone.

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

## 3. Kết quả đã lưu

Nguồn: `notebooks/outputs/02_lightglue_pilot/phantom3-village-kfs/mosaic_*/metrics.json`.
Notebook hiện lưu output cho 6/6 code cell, không lưu exception.

| Cấu hình | Frame thực ghép / yêu cầu | `chain_total_seconds` | Phủ canvas |
|---|---|---|---|
| SIFT + LightGlue | 20/20 | 16,657 s | 98,82% |
| SuperPoint + LightGlue | 20/20 | 136,250 s | 98,71% |

`chain_total_seconds` bao gồm matching, RANSAC và warp/blend; không gồm đọc ảnh trước đó, setup,
warmup, ghi file hay hiển thị sau đó. Không cùng phạm vi với `match_seconds`.
Phủ canvas chỉ là tỷ lệ pixel có ảnh, **không phải độ chính xác đăng ký hoặc diện tích mặt đất**.
Chưa có metric drift/ground truth trong notebook này; không đủ để gọi mosaic “không méo” hoặc “cực chuẩn”.

## 4. Audit và giới hạn

| Vị trí | Phát hiện | Cách diễn giải / việc cần làm |
|---|---|---|
| Markdown đầu notebook | Vẫn nói “chưa ghép mosaic” dù phần sau đã có mosaic | Mô tả notebook chưa đồng bộ; note này phản ánh cả hai phần |
| Phần đo cặp | Warmup, setup và phạm vi đồng hồ được ghi rõ | Điểm tốt; vẫn chỉ là 3 cặp trên một sequence |
| Phần mosaic | JSON có H và số frame thực ghép | Thiếu hash ảnh/run ID; môi trường không được gói đầy đủ cùng tầng mosaic |
| Đường dẫn output | Cố định theo sequence | Run mới có thể ghi đè artifact cũ |
| Đối chiếu Notebook 03 | Khác độ phân giải và điều kiện chạy | Chưa cô lập tác động của riêng độ phân giải |
| Diễn giải tài nguyên | Không đo pin, peak RAM/VRAM hay throughput trên drone | Không được suy từ thời gian CPU rằng drone sẽ “quá tải ngay” |

Kiểm tra cô lập đã chạy: H khôi phục đúng phép tịnh tiến, 3 điểm bị từ chối.
Blend ba ảnh hằng 0/100/200 cho giá trị 125, đúng trộn tuần tự và khác trung bình đều 100.
Không chạy lại inference hoặc kiểm chứng tất cả cảnh khó; audit không xác nhận chất lượng chung của LightGlue.
Notebook chưa được sửa trong lần audit này.

## 5. Đọc output

- `metrics.json`: tầng cặp, môi trường và định nghĩa timing.
- `*_lightglue_matches.png`: inlier mẫu của cặp đầu.
- `mosaic_sift/`, `mosaic_superpoint/`: mỗi thư mục có `mosaic.png` và `metrics.json`.
- Khi so cấu hình, giữ riêng số frame đã ghép, phạm vi timing và hệ pixel của phép đo.

**Kết luận:** đạt vai trò pilot tích hợp và minh họa mosaic ảnh gốc.
Chưa chứng minh learned matcher tốt hơn classical nói chung; cũng chưa kiểm chứng routing hoặc recovery.
