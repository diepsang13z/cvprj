# Thực nghiệm độc lập theo model và RQ

## Quy định bắt buộc

**Không chạy notebook hoặc script thực nghiệm trên máy cá nhân.** Chỉ dùng runtime do Google Colab/Kaggle cấp, không dùng Colab local runtime. Áp dụng cả SIFT/ORB chạy CPU và model học sâu chạy GPU. Xem [RULES.md §8](../RULES.md).

Notebook và module thực nghiệm đều có chốt kiểm tra môi trường trước khi import thư viện model. Đây là chốt chống chạy nhầm, không phải sandbox bảo mật; không giả lập biến môi trường để vượt chốt.

Năm notebook `01`–`05` ở thư mục gốc nay là **mục lục**, không còn Run All nhiều model. Các output lịch sử giữ nguyên. Code thuật toán được chuyển vào `shared/` để chỉ sửa một nơi; notebook riêng chứa cấu hình, đầu vào, lệnh chạy và vị trí bàn giao.

## Danh sách công việc

| Thư mục | Notebook | Mục đích / đầu vào | Bàn giao |
| --- | --- | --- | --- |
| `classical/` | `01_sift`, `01_orb` | Baseline ảnh gốc, độc lập từng thuật toán | Mosaic + metrics/H, log |
| `lightglue/` | `02_sift`, `02_superpoint` | Pilot LightGlue ảnh gốc, độc lập từng extractor | Pair metrics + mosaic/H, log |
| `models/` | `03_<method>` | Pilot thống nhất 640 px; 7 cấu hình bên dưới | Thư mục run chứa `manifest.json`, `pairs/`, `mosaic/`, CSV, HTML |
| `drift/` | `04_trajectory` | Kiểm chứng pose/plane; không phụ thuộc pilot model | `trajectory_check.json` |
| `drift/` | `04_<method>` | Một model; điền `INPUT_RUN` là run của `03_<method>` | `drift_selfconsistent.json` |
| `research/` | `05_scan_sift_bf`, `05_scan_superpoint_lightglue`, `05_scan_efficientloftr` | Quét cửa sổ RQ riêng từng matcher; không cần pilot 03 | Mỗi người một `scan.json` |
| `research/` | `05_rq1` | Nhận đủ ba scan; phân tích Spearman/AUC, không inference | `result.json` của RQ1 |
| `research/` | `05_rq2` | Nhận đủ ba scan; mô phỏng routing và rematch ảnh gốc | `result.json` của RQ2 + ngưỡng |
| `research/` | `05_recovery_none`, `05_recovery_drop`, `05_recovery_anchor`, `05_recovery_split` | Mỗi chính sách một notebook; nhận ba scan và cùng kết quả RQ2 | Mỗi chính sách một `result.json` |
| `research/` | `05_assemble` | Nhận ba scan, RQ1, RQ2, đủ bốn chính sách | `report.json` + `scan_<sequence>.json` |

Tên method của nhóm 03/04: `sift_bf`, `orb_bf`, `sift_lightglue`, `superpoint_lightglue`, `xfeat_mnn`, `xfeat_lighterglue`, `efficientloftr`. Tất cả tên notebook có đuôi `.ipynb`.

Không gộp pilot ảnh gốc 01/02 với pilot 640 px 03 thành cùng benchmark. Hai nhóm giữ cấu hình/thuật toán cũ để không thay đổi ý nghĩa thực nghiệm.

## Thứ tự và phân công gợi ý

- **Thành viên A:** SIFT/ORB trong `models/`, drift tương ứng, scan SIFT.
- **Thành viên B:** SIFT+LightGlue / SuperPoint+LightGlue, drift tương ứng, scan SuperPoint+LightGlue.
- **Thành viên C:** XFeat+MNN / XFeat+LighterGlue / EfficientLoFTR, drift tương ứng, scan EfficientLoFTR.
- **Thành viên D:** `04_trajectory`; nhận ba scan để chạy RQ1/RQ2 và tổng hợp.
- Khi RQ2 xong, chia bốn notebook recovery cho bốn người, sau đó D chạy `05_assemble`.
- Pilot ảnh gốc 01/02 là công việc riêng khi cần đối chiếu độ phân giải, không phải điều kiện bắt buộc cho RQ.

RQ1 và RQ2 chạy độc lập sau ba scan. RQ3 phụ thuộc RQ2 để lấy **cùng ngưỡng**, không phụ thuộc kết quả RQ1. Không yêu cầu notebook khác còn mở hoặc biến còn trong RAM.

## Chuẩn bị trên cloud

1. Mở Colab hosted runtime hoặc Kaggle Notebook. Clone cùng commit của repo cho mọi thành viên; đặt working directory vào root repo (nơi có `requirements_learned.txt`). Mở/chạy notebook con trong môi trường đó.
2. Cài dependency **trong cloud**, trước các cell thực nghiệm:
   ```python
   %pip install -r requirements_learned.txt
   ```
   Khởi động lại kernel nếu pip yêu cầu. Không dùng hướng dẫn này để cài/chạy thử model ở máy cá nhân.
3. Đặt/mount dữ liệu theo `data/<sequence>/.../rgb`. Các job trajectory còn cần `config.cfg`, `trajectory.txt` theo cấu trúc cũ. Không notebook nào tự tải toàn bộ dataset.
4. Colab: mount Google Drive trước. Mặc định output là `/content/drive/MyDrive/uav_runs`. Có thể đặt biến môi trường `UAV_OUTPUT_ROOT` sang thư mục lưu bền vững khác.
5. Kaggle: mặc định `/kaggle/working/uav_runs`. Khi xong phải **Save Version kèm outputs** hoặc tải/copy artifact ra kho nhóm; filesystem phiên chạy không phải nơi lưu lâu dài.
6. Chọn `DEVICE` trong cell đầu (`cpu` nghĩa là CPU trên cloud). Đổi sang `cuda` nếu cần, nhưng các job của **cùng benchmark** phải dùng môi trường nhất quán. Không âm thầm fallback khi CUDA không có.
7. Điền các path bàn giao trong cell cấu hình. Path rỗng cố ý chặn thực thi; không chọn run mới nhất tự động. Có thể copy artifact sang runtime mới rồi dùng đường dẫn mới.
8. Run All **trên cloud**. Cell cuối in thư mục/file cần bàn giao. Thư mục session chứa `run.log`, kể cả traceback nếu job lỗi; thư mục con chứa kết quả. Không nộp job lỗi như một run hoàn tất.

## Hợp đồng artifact và tổng hợp

- Mỗi job dùng thư mục theo tên công việc và UTC microseconds; không ghi đè output thành viên khác hoặc `notebooks/outputs/` lịch sử.
- Scan lưu hash ảnh, kích thước, cửa sổ, tham số, phiên bản thư viện, thiết bị và hash code; không lưu đường dẫn tuyệt đối của máy nguồn hay ảnh trong JSON.
- `SCAN_PATHS` cần đúng một scan mỗi matcher. Tổng hợp từ chối khác dữ liệu, môi trường, cấu hình hoặc hình học tham chiếu. Thời gian matcher tham chiếu có thể khác giữa các worker, không dùng nó làm thời gian matcher ứng viên.
- RQ2/RQ3 nạp lại ảnh khi thực sự cần inference; xác minh hash và nạp cache các cặp đã đo. RQ1/tổng hợp chỉ dùng JSON.
- Bốn recovery phải dùng cùng `result.json` RQ2; assembler kiểm tra hash, đủ policy/sequence, không nhận trùng hoặc thiếu kết quả.
- `report.json` cuối giữ các trường RQ1/RQ2/RQ3 mà paper sử dụng; kèm provenance của scan. Đây vẫn là **các thí nghiệm RQ riêng**, chưa phải pipeline routing + recovery end-to-end.
- Không tự thay dữ liệu của paper. `reports/paper/*` vẫn đọc snapshot lịch sử trong `notebooks/outputs/05_failure_aware/`. Khi nhóm chốt run cloud mới, cập nhật nguồn dữ liệu và số liệu paper cùng nhau; không trộn bảng của run cũ với hình của run mới.
- Thời gian vẫn theo phạm vi đo cũ, không phải latency end-to-end. Chạy trên các GPU/CPU khác nhau không chứng minh speedup; đối chiếu cấu hình phần cứng trước khi diễn giải, kể cả khi tên môi trường giống nhau.

## Giới hạn kiểm tra của lần tách

Chỉ kiểm tra JSON/cú pháp, tính nhất quán code được chuyển và hợp đồng đường dẫn tại máy phát triển. **Không thực thi bất kỳ notebook, matcher, RANSAC hay mosaic nào trên máy cá nhân.** Cần chạy các job thật trên cloud để xác nhận dependency, dữ liệu và kết quả số; không coi kiểm tra tĩnh là bằng chứng thí nghiệm đã chạy.
