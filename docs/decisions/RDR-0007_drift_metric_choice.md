# RDR-0007: Chốt công thức đo drift không phụ thuộc `trajectory.txt`

## Status

Accepted

## Date

2026-10-13

## Context

- `RDR-0003` đặt trọng tâm vào drift tích luỹ, nhưng chưa chốt **cách đo**.
- `notebooks/04_drift_evaluation.ipynb` kiểm chứng cầu nối giữa `trajectory.txt` và ma trận $H$: quy ước pose đã xác minh được (quaternion camera→world, tâm camera $C = t$, mặt phẳng `Plane=` cách camera ~190 m) và tỷ lệ mét khớp ảnh (tỷ lệ 0,9999 trên 6 cặp của `village`).
- Tuy nhiên cầu nối **chưa đủ chuẩn để công bố drift**: residual một bước 6–16 px tăng tuyến tính tới ~92 px sau 19 bước; quy ước phần xoay chưa xác minh; sequence `grass` ở hệ quy chiếu khác và mô hình mặt phẳng suy biến; và **nguồn gốc pose chưa xác minh** (thiết bị đo hay hệ tái dựng).
- Chi tiết bằng chứng: `docs/logs/datasets/0003_trajectory_pose_verification.md` và `notes/notebook_04_drift_evaluation.md` mục 7.
- Theo `RULES.md` mục 4, chọn công thức metric là quyết định phương pháp → nhóm phải chốt.

## Decision

1. **Chốt metric đo drift là "chain vs direct" (tự nhất quán), không dùng `trajectory.txt` làm tham chiếu.**

   Với mỗi mô hình và mỗi sequence, trên cùng chuỗi frame đã ghép:
   - $H^{\\text{chain}}_{i \\to 0}$: homography tích luỹ tuần tự qua $i$ bước (lấy từ `H_to_mosaic` của run, đưa về hệ pixel ảnh gốc).
   - $H^{\\text{direct}}_{i \\to 0}$: homography ghép **thẳng** frame $i$ về frame $0$ bằng một matcher tham chiếu cố định (SIFT + RANSAC 3 px, ảnh gốc).
   - Sai số vòng: $\\text{drift}_i = \\frac{1}{|P|}\\sum_{p \\in P} \\lVert H^{\\text{chain}}_i p - H^{\\text{direct}}_i p \\rVert_2$ với $P$ = 4 góc + tâm ảnh.
   - Báo cáo: `drift_px` theo từng $i$, `final_drift_px` tại $i$ lớn nhất đo được, `ate_px` = RMS trên các $i$ đo được.

2. **Đơn vị chính là pixel**, không phải mét. Quy đổi mét chỉ được nêu kèm cảnh báo vì nó kế thừa giả định của cầu nối (khoảng cách mặt phẳng ~190 m, mặt đất phẳng).

3. **Matcher tham chiếu cố định cho mọi mô hình là SIFT.** Vì vậy **dòng `sift_bf` chính là mức nền của phương pháp** (chain và direct cùng dùng SIFT); mọi so sánh giữa các mô hình phải đọc kèm mức nền này.

4. **Điều kiện hợp lệ:** chỉ nhận một điểm đo khi cặp ghép trực tiếp đạt tối thiểu **100 inlier**; dưới ngưỡng đó ghi `không đo được`, không suy diễn. Ngưỡng và lý do ghi trong manifest của kết quả.

5. **Ghi kết quả** vào `notebooks/outputs/04_drift_evaluation/drift_selfconsistent.json` kèm hash dữ liệu, tên run, tham số matcher và phiên bản thư viện.

## Consequence

- Drift đo được **không phụ thuộc** file pose của dataset ⇒ không kế thừa các sai số đã nêu ở mục Context, và không cần chờ phản hồi tác giả để bắt đầu RQ1/RQ2.
- **Có thể chạy ngay**: không cần tải thêm model, chỉ dùng homography đã lưu của run 7 mô hình + một matcher tham chiếu.
- **Giới hạn phải nêu khi báo cáo:** (a) chỉ đo được trong phạm vi hai frame còn đủ vùng chồng (đã kiểm: tới frame 19 của `village` vẫn còn 114 inlier); (b) mức nền của phương pháp là sai số của matcher tham chiếu, không tách được khỏi sai số chuỗi; (c) metric này đo **sai số hình học tương đối**, không phải sai số vị trí tuyệt đối ngoài thực địa.
- Việc hỏi tác giả dataset về quy ước và nguồn gốc pose **vẫn nên làm** (đã ghi ở `notes/datasets.md` mục 5) để có phương án đối chiếu thứ hai, nhưng **không còn là điều kiện chặn**.

---

## Addendum 2026-10-13 (không thay đổi Decision)

Sau khi ra quyết định, nhóm đối chiếu **mã nguồn tác giả dataset** (clone `github.com/bushuhui/Map2DFusion`) và phát hiện hai chỗ trong phần Context ở trên đã lỗi thời:

1. **Thứ tự quaternion.** `PIL/src/base/types/SE3.h` định nghĩa `operator>>` là `x y z rx ry rz w` ⇒ quaternion là **$(x,y,z,w)$**, không phải $(w,x,y,z)$ như parser dùng lúc đó. `src/main.cpp` cũng xác nhận `trajectory.txt` mỗi dòng là `<tên ảnh> <SE3>` và `Plane=` là một **SE3**.
2. **Vì vậy các số trong Context bị sai, cần đọc lại như sau:**

| Chỉ số | Ghi lúc ra quyết định | Sau khi sửa parser |
|---|---|---|
| Residual cặp tham chiếu | ~10 px | **0,88 px** |
| Vai trò phần xoay | tắt xoay tốt hơn (9,97 vs 11,83 px) | **bật xoay tốt hơn hẳn** (0,88 vs 9,96 px) |
| Khoảng cách mặt phẳng | 190 m | 194 m (khớp `Plane=` 193,9 m) |
| Residual theo baseline | 6 px → 92 px | **1,0 px → 21,2 px (≈3 m)** |

**Decision giữ nguyên** (metric `chain vs direct` là thước đo chính) vì: (a) trajectory của dataset là quỹ đạo **do SLAM tác giả tái dựng**, không độc lập hoàn toàn với ảnh; (b) metric hiện tại đã chạy và tự bắt được lỗi. Cầu nối pose nay đủ tốt để dùng làm **phép đối chiếu thứ hai cho `phantom3-village-kfs`** (không dùng được cho `phantom3-grass-kfs`).

Hồ sơ chi tiết: `docs/logs/datasets/0003_trajectory_pose_verification.md` (mục ĐÍNH CHÍNH) và `notes/notebook_04_drift_evaluation.md` mục 4–5.
