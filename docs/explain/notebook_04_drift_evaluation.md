# Giải thích và audit Notebook 04: Đo độ lệch hình học bằng tham chiếu

Đọc cùng notebook [`notebooks/accumulated_drift_evaluation.ipynb`](../../notebooks/accumulated_drift_evaluation.ipynb).
Cập nhật kỹ thuật: **2026-11-01** — Đã hoàn thành toàn bộ sửa đổi kỹ thuật theo `RDR-0007`, `RDR-0010`, `RDR-0011` và `RULES.md §8`.

## 1. Hai câu hỏi khác nhau

1. **Chẩn đoán pose:** hiểu `trajectory.txt`, quaternion và `Plane=` để đối chiếu chuyển động suy từ ảnh.
2. **Đo tự nhất quán:** so H ghép tuần tự với H ghép thẳng bằng SIFT, theo
   [`RDR-0007`](../logs/decisions/RDR-0007_drift_metric_choice.md).

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

## 5. Audit kỹ thuật và các điểm hoàn thiện mới nhất

| Hạng mục | Hiện trạng kỹ thuật mới nhất |
|---|---|
| **Tách biệt chẩn đoán Pose** | Chẩn đoán trajectory mặc định tắt (`UAV_ENABLE_POSE_DIAGNOSIS=0`). Khi tắt, xuất structured `status: "disabled_or_unavailable"` và `None` cho các metric hình học, không fake số liệu. |
| **Độc lập metadata camera** | Đọc danh sách ảnh và kích thước `(w, h)` trực tiếp từ file ảnh đĩa (`images_data`), không phụ thuộc `config.cfg`. |
| **Xác thực Provenance & Hash** | `validate_benchmark_manifest()` kiểm chứng 100% tên file, thứ tự và hash SHA-256 từng ảnh so với benchmark run. |
| **Lọc Run hoàn tất chuẩn** | `latest_run_dir()` chỉ tự động nhận các run có `completed.json` và cấu trúc artifacts đầy đủ; cho phép chọn run lịch sử qua `UAV_INPUT_RUN` khi đã qua xác thực. |
| **Loại trừ mốc Identity** | Mốc $i = 0$ là reference origin ($0.0\text{ px}$ tự nhiên), loại khỏi các chỉ số thực nghiệm. Không còn điểm $i>0$ hợp lệ thì `final_drift_px = None`. |
| **So sánh công bằng (Common Eligible Sets)** | Tính toán `common_eligible_sets` trên các frame mà mọi mô hình đều có tham chiếu hợp lệ ($\ge 100$ inlier), phân tách rõ với độ phủ `frames_stitched`. |
| **Xoá Assertions thiên kiến** | Loại bỏ toàn bộ assertion ép kết quả nghiên cứu (SIFT < 60, ELoFTR > 5x, residual tăng >10x); chỉ giữ lại các unit self-check toán học. |
## 6. Đọc output và kết luận

- `trajectory_check.json`: chẩn đoán quy ước và các giả định pose/plane, không phải chứng nhận GPS.
- `drift_selfconsistent.json`: sai số vòng, run nguồn, `last_index`, `skipped_steps`, chuỗi metric.
- Writer dùng đường dẫn cố định; cần giữ run nguồn và artifact tương ứng khi so các lần chạy.
**Kết luận:** Notebook đo drift tự nhất quán chuỗi vs trực tiếp theo chuẩn khoa học `RDR-0007`, lưu vết provenance đầy đủ và bảo toàn toàn bộ nhật ký inliers phục vụ đánh giá công bằng.
