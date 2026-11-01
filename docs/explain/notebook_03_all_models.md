# Giải thích và audit Notebook 03: Benchmark chuẩn hoá 7 mô hình

Đọc cùng notebook [`notebooks/feature_matcher_benchmark.ipynb`](../../notebooks/feature_matcher_benchmark.ipynb).
Cập nhật kỹ thuật: **2026-11-01** — Đã hoàn thành toàn bộ sửa đổi kỹ thuật theo `RDR-0010`, `RDR-0011` và `RULES.md §8`.
## 1. Mục đích

Đặt các cấu hình vào cùng điều kiện xử lý để quan sát matching và mosaic:
`sift_bf`, `orb_bf`, `sift_lightglue`, `superpoint_lightglue`,
`xfeat_mnn`, `xfeat_lighterglue`, `efficientloftr`.
Đây là khảo sát cấu hình pretrained, chưa phải benchmark đủ rộng hoặc xếp hạng mô hình tổng quát.

- Chế độ benchmark: `pilot` (2 sequence: `village`, `grass`; 3 cặp đầu; 20 frame mosaic) hoặc `full` (tự động quét toàn bộ sequence trong `dataset/`, toàn bộ cặp và toàn bộ frame).
- Độ phân giải chuẩn hoá: cạnh dài tối đa 640 px (làm tròn xuống bội 32).
- Sparse đặt tối đa 2.000 keypoint; EfficientLoFTR semi-dense không bị ép cùng số correspondence.
- Môi trường thực thi: Google Colab / Kaggle (GPU T4/A100); nghiêm cấm chạy máy cá nhân (`RULES.md §8`).

Không nên gán một sequence luôn “dễ” hoặc “khó”: mức khó phụ thuộc matcher, cửa sổ và phép đo.

## 2. Luồng code và điểm mạnh

1. Adapter `load_matcher()` nhận RGB và trả hai mảng điểm trong hệ pixel đầu vào.
2. `geometry()` dùng RANSAC 3 px, kiểm tra H hữu hạn/hạng 3, đủ inlier và RMSE hữu hạn.
3. `build_mosaic()` tích lũy H, dừng ở cặp thất bại; `canvas_and_mosaic()` warp/blend 50/50.
4. `run()` ghi cấu hình, hash ảnh, correspondence, metric, H và ảnh theo từng run UTC riêng.
5. `write_reports()` xuất HTML/CSV; `rebuild()` dựng lại HTML từ artifact, không chạy model.

Warmup tách khỏi timing, revision mô hình ghi trong manifest, không âm thầm fallback CPU khi yêu cầu CUDA.
Đây là các điểm tốt để kế thừa cho thực nghiệm tiếp theo.

## 3. Số liệu phải gắn với run

Run đối chiếu: `notebooks/outputs/03_all_models/20261013T164937_145955Z/`.
Notebook hiện lưu output cho 9/9 code cell, không lưu exception.
`mosaic_summary.csv` cho thấy cả 14 trường hợp giữ đủ 20/20 frame.

| Cấu hình / sequence | Canvas | Phủ canvas |
|---|---|---|
| SIFT+BF / `village` | 647×604 | 98,59% |
| EfficientLoFTR / `village` | 1465×626 | 55,59% |
| EfficientLoFTR / `grass` | 946×1073 | 73,40% |

Canvas khác thường là tín hiệu cần kiểm tra, không phải metric độ chính xác độc lập.
Ghép đủ frame không chứng minh đúng hình học; phủ canvas cao cũng không chứng minh mosaic không méo.
Notebook 04 bổ sung phép đo chain-vs-direct trên run này, nhưng không phải ground truth ngoài thực địa.

Chưa đủ bằng chứng quy nguyên nhân riêng cho “sai số góc quay nhỏ tích lũy” hoặc kết luận mô hình
EfficientLoFTR nói chung không phù hợp: cần tách ảnh hưởng adapter, preprocessing, checkpoint và dữ liệu.
Quan sát hiện tại hỗ trợ nhu cầu kiểm tra lỗi đăng ký; chưa chứng minh chỉ báo/routing/recovery của RQ1–RQ3.

## 4. Audit kỹ thuật và các điểm hoàn thiện mới nhất

| Hạng mục | Hiện trạng kỹ thuật mới nhất |
|---|---|
| **Cloud Guard & Bền vững** | Nghiêm cấm chạy local; fail-closed nếu không mount được `/content/drive/MyDrive`. Chặn ghi đè run cũ khi có `completed.json`. |
| **Bộ nhớ $O(1)$ (Lazy Streaming)** | Đọc ảnh lười theo cặp on-demand khi matching và render mosaic thay vì giữ toàn bộ mảng ảnh trong RAM, bảo đảm chạy an toàn trên full dataset. |
| **Subpixel Precision cho ELoFTR** | Trích xuất toạ độ qua `process_eloftr_matches()` giữ nguyên độ chính xác `float32`, kèm unit self-check tự động xác thực. |
| **Kiểm tra và Xuất marker sau cùng** | `completed.json` chỉ được xuất SAU CÙNG sau khi kiểm tra hình học, tính hợp lệ JSON và số lượng pair khớp chuẩn. Trang navigation chỉ nhận run có `completed.json`. |
| **Provenance thiết bị chuẩn xác** | Ghi nhận backend minh bạch cho từng phương pháp: `"cpu"` cho OpenCV SIFT/ORB, `"cuda"` cho các mô hình học sâu. |
| **Xử lý ca thất bại hợp lệ** | Cho phép chấp nhận kết quả 1 frame khi matcher thất bại mà không crash hay ép `frames_stitched >= 2`. |
## 5. Đọc artifact

- `manifest.json`: cấu hình run, revision và hash ảnh nguồn.
- `summary.csv`, `mosaic_summary.csv`: bảng CSV, không phải workbook Excel.
- `pairs/<sequence>/<method>/`: `metrics.json`, ảnh nối điểm và `.npz` correspondence/inlier mask.
- `mosaic/<sequence>/<method>/`: ảnh mosaic và metrics có `H_to_mosaic`, số frame, lý do dừng.
- `index.html`: báo cáo; sự tồn tại của trang không thay thế kiểm tra tính đầy đủ của run.

**Kết luận:** tốt làm nền thực nghiệm chung. Cần mở rộng mẫu, đo lặp lại và audit adapter
trước khi xếp hạng mô hình; notebook chưa được sửa trong lần audit này.
