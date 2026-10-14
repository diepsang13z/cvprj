# Giải thích và audit Notebook 04: Đo độ lệch hình học bằng tham chiếu

Đọc cùng [notebook](../notebooks/04_drift_evaluation.ipynb).
Audit 2026-10-14: `ANALYZED` — kiểm tra code, artifact và phép chiếu cô lập; chưa chạy lại matching toàn bộ.
Notebook hiện có output cho 12/12 code cell, không lưu exception; điều này không chứng nhận mọi kết luận.

## 1. Hai câu hỏi khác nhau

1. **Chẩn đoán pose:** hiểu `trajectory.txt`, quaternion và `Plane=` để đối chiếu chuyển động suy từ ảnh.
2. **Đo tự nhất quán:** so H ghép tuần tự với H ghép thẳng bằng SIFT, theo
   [RDR-0007](../docs/decisions/RDR-0007_drift_metric_choice.md).

Phần 2 không phụ thuộc trajectory, nhưng **không độc lập với ảnh hoặc matcher tham chiếu**.
Câu hỏi đúng là “hai cách đăng ký bất đồng bao nhiêu pixel?”, không phải “lệch bao nhiêu so với thực địa?”.
Notebook đã có cả hai phần; mô tả cũ rằng nó chỉ chẩn đoán và không xuất drift không còn đúng.

## 2. Phần pose cho biết gì?

`quat_to_R()` đọc quaternion theo `(x, y, z, w)`, đối chiếu với nguồn tác giả được ghi trong
[nhật ký kiểm chứng](../docs/logs/datasets/0003_trajectory_pose_verification.md).
Sửa cách đọc quaternion làm residual cặp tham chiếu `village` trong kết quả đã lưu giảm còn khoảng 0,88 px.
Đó là bằng chứng hữu ích về quy ước, không phải bảo đảm độ chính xác cho mọi cặp.

Trajectory do hệ SLAM của tác giả tái dựng, không nên gọi là GPS đo độc lập.
Với `grass`, cấu hình mặt phẳng/pose đang xét bị suy biến; không suy ra drone thật sự bay sát mặt đất 0 m.
Đổi gốc tọa độ tự nó không làm mô hình sai nếu mặt phẳng và pose được biến đổi nhất quán.

### Tỷ lệ ảnh/pose gần 1 chưa xác nhận đơn vị mét

Notebook quét khoảng cách mặt phẳng rồi chọn giá trị làm tỷ lệ gần 1.
Kiểm lại tỷ lệ tại chính giá trị đã chọn không phải một phép kiểm chứng ngoài mẫu.
Sự gần nhau với `Plane=` là bằng chứng nhất quán bổ sung, nhưng pose và plane không nhất thiết độc lập.

**Kiểm tra đã chạy trên hàm `H_gt()` với pose `village`:**
nhân toàn bộ tịnh tiến camera lên 10 lần và khoảng cách 194 lên 1940,
H thay đổi tối đa khoảng `2,3e-13` — chỉ ở mức sai số số học.
Lý do: phép chiếu phụ thuộc tỷ số dịch chuyển/khoảng cách.
Vì vậy ảnh và tỷ lệ này không tự phân biệt mét với một thang độ dài khác.
Quy đổi pixel sang mét cần nguồn hiệu chuẩn thang đo bên ngoài và các giả định mặt phẳng.

## 3. Chain vs direct hoạt động thế nào?

- **Chain:** tích lũy các H từ frame hiện tại về frame 0.
- **Direct:** SIFT ảnh gốc ghép thẳng frame hiện tại về frame 0.
- Bỏ biến đổi canvas từ `H_to_mosaic`, rồi đổi hệ pixel resize về ảnh gốc bằng `D @ H @ D⁻¹`.
- Chiếu 4 góc và tâm ảnh qua hai H, lấy trung bình khoảng cách Euclidean.
- `direct_to_first()` chỉ nhận điểm đo có ít nhất 100 inlier; dưới ngưỡng ghi không đo được.

Phép direct không tích lũy qua chuỗi, nhưng vẫn có sai số matching, RANSAC và mô hình mặt phẳng.
Dòng SIFT cũng gồm sai số của **cả chuỗi lẫn direct**, không tách được “độ rung riêng của thước”.
Không được lấy mức SIFT làm ngưỡng sai số cho phép hoặc tự động trừ nó khỏi các mô hình khác.

## 4. Số liệu và phạm vi đo thực tế

Nguồn: `notebooks/outputs/04_drift_evaluation/drift_selfconsistent.json`;
run Notebook 03 được chấm: `20261013T164937_145955Z`.
Frame đánh số từ 0, đơn vị là pixel ảnh gốc.

| Cấu hình | `village`: đo cuối tại frame 19 | `grass`: đo cuối tại frame 6 |
|---|---|---|
| SIFT+BF | 46,69 | 1,72 |
| ORB+BF | 73,23 | 2,78 |
| SIFT+LightGlue | 47,05 | 1,82 |
| SuperPoint+LightGlue | 61,11 | 1,83 |
| XFeat+MNN | 39,69 | 8,66 |
| XFeat+LighterGlue | 47,63 | 3,37 |
| EfficientLoFTR | 1311,51 | 62,86 |

`village` có 20 điểm được báo đo, **kể cả mốc 0**; `grass` có 7 điểm, kể cả mốc 0.
`grass` frame 7–19 không đạt điều kiện tham chiếu; không được gọi 62,86 px là drift cuối chuỗi 20 frame.
Không đạt 100 inlier không đồng nghĩa không tìm được H hoặc mất hoàn toàn vùng chồng.

Tỷ số khoảng 28×/37× là so EfficientLoFTR với **giá trị SIFT của từng sequence**,
không phải vượt “giới hạn cho phép” 28–37 lần.
Các con số không chứng minh 6 cấu hình còn lại tương đương; chưa có kiểm định tương đương/khoảng bất định.
Khác độ dài đoạn đo cũng không cho phép suy `grass` chính xác hơn hoặc khó hơn chỉ từ hai cột.

## 5. Audit code và khả năng tái lập

| Vị trí | Bằng chứng / rủi ro | Việc cần làm |
|---|---|---|
| `latest_run_dir()` | Tự lấy thư mục mới nhất có `index.html` | Cố định run đánh giá; có HTML không tự bảo đảm mọi artifact đầy đủ |
| `chain_to_original()` | Đọc H/size từ run cũ, ghép direct từ ảnh hiện tại | Kiểm hash trước khi chấm, không chỉ ghi tên run |
| Audit hash lần này | 40/40 hash ảnh hiện tại khớp manifest run trên | Chưa thấy trộn ảnh sai ở run hiện tại; đây vẫn là kiểm tra còn thiếu trong notebook |
| `direct_to_first()` | Có áp ngưỡng 100, khác Notebook 05 hiện tại | Giữ cơ chế không đo được và báo rõ đoạn đánh giá |
| Tổng hợp `measured` / `ate_px` | Tính cả mốc 0 luôn bằng 0 | Nếu chỉ còn mốc, không được báo như có đánh giá drift hữu ích |
| Assertions chẩn đoán | Ép residual tăng >10× | Kết quả nghiên cứu không phải bất biến code |
| Assertions metric | Ép SIFT <60 px và EfficientLoFTR >5× SIFT | Có thể loại một thí nghiệm hợp lệ chỉ vì khác kỳ vọng |
| Kiểm `drift(i=0)==0` | Identity so với identity | Không đủ để chứng minh hướng H ở các frame khác |
| Docstring / phần mở đầu | `read_trajectory()` vẫn ghi `qw qx qy qz`; trạng thái nguồn pose chưa đồng bộ | Sửa tài liệu trong notebook trước khi dùng làm hướng dẫn |

`ate_px` ở đây là RMS của dãy độ lệch 5 điểm, không phải Absolute Trajectory Error theo ground truth.
Kiểm tra cô lập `drift_px()` với tịnh tiến (3,4) cho đúng 5 px;
quaternion identity cho đúng ma trận identity. Không thay thế kiểm chứng pipeline đầy đủ.

## 6. Đọc output và kết luận

- `trajectory_check.json`: chẩn đoán quy ước và các giả định pose/plane, không phải chứng nhận GPS.
- `drift_selfconsistent.json`: sai số vòng, run nguồn, `last_index`, `skipped_steps`, chuỗi metric.
- Writer dùng đường dẫn cố định; cần giữ run nguồn và artifact tương ứng khi so các lần chạy.

**Kết luận:** có giá trị đo tự nhất quán và chẩn đoán, nhưng chưa đo sai số ngoài thực địa.
Cần sửa lập luận về thang đo, assertions ép kết quả và ràng buộc provenance.
Notebook/RDR chưa được sửa trong lần audit này.
