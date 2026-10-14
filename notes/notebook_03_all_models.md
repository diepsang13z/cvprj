# Giải thích và audit Notebook 03: Pilot chung cho 7 cấu hình

Đọc cùng [notebook](../notebooks/03_all_models.ipynb).
Audit 2026-10-14: `ANALYZED` — đọc code/artifact, kiểm tra hình học và hash; chưa chạy lại inference.

## 1. Mục đích

Đặt các cấu hình vào cùng điều kiện xử lý để quan sát matching và mosaic:
`sift_bf`, `orb_bf`, `sift_lightglue`, `superpoint_lightglue`,
`xfeat_mnn`, `xfeat_lighterglue`, `efficientloftr`.
Đây là khảo sát cấu hình pretrained, chưa phải benchmark đủ rộng hoặc xếp hạng mô hình tổng quát.

- Hai sequence: `phantom3-village-kfs`, `phantom3-grass-kfs`.
- Tầng cặp: 3 cặp đầu mỗi sequence, tổng cộng 42 lần đo cho 7 cấu hình.
- Tầng mosaic: 20 frame đầu mỗi sequence, tổng cộng 14 mosaic.
- CPU 4 threads, cạnh dài tối đa 640 px, kích thước làm tròn xuống bội 32.
- Sparse đặt tối đa 2.000 keypoint; EfficientLoFTR semi-dense không bị ép cùng số correspondence.

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

## 4. Audit: đã kiểm gì, còn thiếu gì?

| Hạng mục | Kết quả audit | Giới hạn |
|---|---|---|
| Hình học | Phép tịnh tiến được khôi phục đúng; 3 correspondence bị từ chối | Chưa bao phủ mọi cấu hình suy biến/projective |
| Blend | Ba ảnh hằng 0/100/200 cho pixel 125 | Đúng blend tuần tự, không phải trung bình đều |
| Hash đầu vào | 40/40 ảnh hiện tại khớp manifest của run trên | Không tự xác nhận code/checkpoint/môi trường hoàn toàn giống run cũ |
| Tái lập | Run riêng, manifest, JSON nghiêm ngặt, NPZ giữ điểm | Chưa chạy lặp lại toàn bộ để kiểm tra độ ổn định |
| Resize | 1920×1080 được đưa về 640×352 | Hai trục có tỷ lệ khác nhau; cần giữ đúng biến đổi tọa độ khi so ảnh gốc |
| Tiêu chí thành công | H hợp lệ về số học | Không kiểm tra độc lập rằng đăng ký đúng |
| Thống kê | Mỗi cặp đo một lượt sau warmup | Chưa có khoảng bất định hay benchmark nhiều sequence/cửa sổ |
| Assertions cuối | Có kiểm tra hình học hữu ích, nhưng ép `frames_stitched >= 2` | Ca thất bại ngay cặp đầu vẫn là kết quả thí nghiệm hợp lệ, không nhất thiết lỗi code |

`match_seconds` chỉ đo matcher/preprocessing/chuyển điểm về CPU, không gồm RANSAC.
`chain_total_seconds` gồm matching, RANSAC và dựng mosaic, không gồm đọc ảnh trước đó hoặc ghi kết quả.
Không so trực tiếp với timing Notebook 01/02 mà bỏ qua khác biệt phạm vi, độ phân giải và điều kiện máy.
Chưa đo peak RAM/VRAM, điện năng hoặc throughput trên drone.

Kiểm tra adapter learned với nguồn upstream/checkpoint độc lập **chưa được thực hiện trong audit này**.
Vì thế không thể dùng các kiểm tra geometry đã pass để chứng nhận cả 7 adapter đều đúng.

## 5. Đọc artifact

- `manifest.json`: cấu hình run, revision và hash ảnh nguồn.
- `summary.csv`, `mosaic_summary.csv`: bảng CSV, không phải workbook Excel.
- `pairs/<sequence>/<method>/`: `metrics.json`, ảnh nối điểm và `.npz` correspondence/inlier mask.
- `mosaic/<sequence>/<method>/`: ảnh mosaic và metrics có `H_to_mosaic`, số frame, lý do dừng.
- `index.html`: báo cáo; sự tồn tại của trang không thay thế kiểm tra tính đầy đủ của run.

**Kết luận:** tốt làm nền thực nghiệm chung. Cần mở rộng mẫu, đo lặp lại và audit adapter
trước khi xếp hạng mô hình; notebook chưa được sửa trong lần audit này.
