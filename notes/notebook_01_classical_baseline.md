# Giải thích và audit Notebook 01: Baseline SIFT & ORB

Tài liệu cho sinh viên đọc cùng [notebook](../notebooks/01_classical_baseline.ipynb).
Audit 2026-10-14: `ANALYZED` — đọc code/artifact và chạy kiểm tra cô lập, không chạy lại toàn thí nghiệm.

## 1. Mục tiêu và phạm vi

Ghép tối đa 20 ảnh UAV đầu sequence `phantom3-village-kfs` thành mosaic cục bộ,
so sánh SIFT+BF với ORB+BF. Đây là baseline xử lý hậu kỳ, không điều khiển drone hay chạy realtime.
Ảnh không georeference; không được coi là bản đồ địa lý chính xác.

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

Nguồn: `notebooks/outputs/01_classical_baseline/phantom3-village-kfs/metrics_*_20frames.json`.
Output notebook hiện có 7/7 code cell đã thực thi, không lưu exception; không tương đương tái lập độc lập.

| Cấu hình | Frame đã ghép / yêu cầu | `pipeline_total_seconds` |
|---|---|---|
| SIFT+BF | 20/20 | 7,48 s |
| ORB+BF | 20/20 | 3,96 s |

Thời gian này bao gồm đọc ảnh trong pipeline, matching, RANSAC và dựng mosaic;
không gồm ghi PNG/JSON và hiển thị sau khi hàm trả về. Là một lần chạy, không phải kết quả benchmark lặp lại.
Chưa có số đo drift hay kiểm chứng thực địa trong notebook này.
RMSE trên các inlier dùng fit H không đủ để kết luận SIFT ghép đúng hơn ORB trong mọi cảnh.

## 4. Audit: phần đúng và phần còn thiếu

| Vị trí | Bằng chứng | Ảnh hưởng / việc cần sửa |
|---|---|---|
| `extract_and_match()` + `estimate_homography()` | Chạy SIFT/ORB trên ảnh đen 64×64: H bị từ chối | Xử lý không có đặc trưng đúng; thời gian helper trả 0,0 dù đã tính toán |
| Bộ tổng hợp ở cell 11 | Thực thi nhánh `valid=[]` cho `avg_rmse=0.0` | Không có phép đo bị trình bày như sai số bằng 0; cần `N/A` |
| Tiêu đề mosaic ở cell 11 | Dùng `len(selected_files)`, không dùng số H thực lưu | Nếu dừng sớm, tiêu đề vẫn có thể ghi đủ số frame yêu cầu |
| JSON kết quả | Có H, metric từng cặp và thời gian tổng | Chưa có hash ảnh, đầy đủ tham số và môi trường của run |
| `load_sequence()` | Comment/print gọi trajectory là ground truth | Không nên gọi pose SLAM tái dựng là chuẩn độc lập; xem note 04 |

Thời gian 0,0 của helper ở ca thiếu đặc trưng không làm mất latency của cặp trong pipeline:
pipeline có đồng hồ riêng bao quanh extraction và RANSAC.
Kiểm tra cô lập canvas một ảnh identity cho đúng kích thước; chưa kiểm hết các homography suy biến/projective.
Các lỗi báo cáo nêu trên **chưa được sửa trong notebook** bởi lần audit này.

## 5. Đọc output và dùng lại

- `mosaic_sift_20frames.png`, `mosaic_orb_20frames.png`: ảnh kết quả.
- `metrics_*.json`: `H_to_mosaic`, bản ghi cặp thành công/thất bại, số frame yêu cầu.
- Số frame thực ghép là số ma trận trong `H_to_mosaic`; tên file vẫn dùng số frame yêu cầu.
- Writer dùng đường dẫn cố định, lần chạy mới có thể ghi đè. Cần giữ kèm dữ liệu/cấu hình nếu muốn so các run.

**Kết luận:** đạt vai trò baseline minh họa. Ưu tiên sửa báo cáo ca thất bại và provenance;
không cần thêm learned matcher hoặc recovery vào notebook này.
