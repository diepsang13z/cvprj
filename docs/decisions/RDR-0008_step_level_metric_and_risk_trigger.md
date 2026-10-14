# RDR-0008: Thước đo cấp bước, bộ chỉ báo rủi ro và ngưỡng kích hoạt

## Status

**Proposed** — chờ nhóm chốt. Theo `RULES.md` §4, chọn ngưỡng/chỉ báo là quyết định phương pháp nên
agent chỉ được đề xuất kèm bằng chứng, không tự chốt.

## Date

2026-10-14

## Context

`RDR-0003` định hình ba RQ (dự báo lỗi – phân luồng – phục hồi) và `RDR-0007` đã chốt metric drift
`chain vs direct` ở mức **cả chuỗi**. Ba thứ sau vẫn chưa ai chốt, mà không có chúng thì RQ1/RQ2/RQ3
không chạy được:

1. **Cách đo sai số của MỘT bước ghép** (mức cặp frame liền kề). Metric của `RDR-0007` cần frame 0
   và chỉ đo được tới frame ~19 vì hết vùng chồng — không đủ để đánh giá chỉ báo theo từng bước.
2. **Bộ chỉ báo rủi ro chính thức** cho RQ1 (đề cương liệt kê inlier count/ratio, reprojection error,
   overlap, spatial distribution — nhưng chưa có bằng chứng chỉ báo nào thực sự báo được lỗi).
3. **Ngưỡng kích hoạt** và **chiến lược phục hồi mặc định** — `RULES.md` §4 nêu đích danh "ngưỡng kích hoạt".

Bằng chứng để ra quyết định: `notebooks/05_failure_aware_pipeline.ipynb` chạy trên hai cửa sổ 45 bước
(`phantom3-village-kfs` frame 80–125, `phantom3-grass-kfs` frame 0–45) — cửa sổ được chọn bằng lần quét
160 bước ở `docs/logs/experiments/0001_failure_scan_windows.md` vì 20 frame đầu không có lỗi nào để học.

## Decision (đề xuất)

1. **Thước đo cấp bước — mở rộng `RDR-0007`, không thay thế.**
   Với mỗi bước `i`: ghép chính cặp `(i-1, i)` bằng **matcher tham chiếu** (SIFT ảnh gốc 4000 đặc trưng,
   đúng định nghĩa `RDR-0007`), rồi
   `step_error_px(i) = khoảng cách trung bình trên 5 điểm mốc (4 góc + tâm, hệ ảnh gốc)`
   giữa homography của pipeline và homography tham chiếu. Bước bị coi là **sai khi `step_error_px > 2`**
   (mức nền nhiễu của chính SIFT). Drift cả chuỗi vẫn báo cáo thêm dưới dạng
   `drift vs chuỗi tham chiếu` (tổng các bước), dùng cho so sánh dài hơn 19 bước.

2. **Bộ chỉ báo chính thức = 4 chỉ báo, có bằng chứng tách được bước sai.**
   `photo_bad_frac` (tỉ lệ điểm ảnh lệch > 25 mức xám sau khi ghép), `rmse_px` (RMSE nội tại của RANSAC),
   `overlap_ratio` (giao khung ảnh sau khi chiếu), `photo_ncc` (tương phản sau khi ghép).
   Xếp hạng trên `village`/SIFT (21/45 bước sai): AUC 0,855 / 0,839 / 0,788 / 0,770.
   **Loại khỏi vai trò chỉ báo:** `matches`, `inliers` (AUC 0,598 / 0,591 — gần như đoán mò) và
   `hull_area_ratio` (0,571). `inlier_ratio` giữ ở mức dự phòng (0,726).

3. **Ngưỡng kích hoạt `τ_ncc = 0,93`** (kèm `inlier_ratio < 0,30` là điều kiện phụ), chọn theo luật
   "ngưỡng cao nhất mà **mọi** sequence vẫn nằm trong **ngân sách leo thang 25%**". Hệ quả đo được:
   `village` leo thang 16% số bước, `grass` 0%. Biến thể **leo thang ở ảnh gốc** dùng khi cần độ chính xác:
   tại 7 bước bị gắn cờ ở `village`, sai số bước là **1,49 px** (ảnh gốc) so với **4,51 px** (640 px).

4. **Chiến lược phục hồi mặc định = tách submosaic (`split`)** khi bước vẫn rủi ro sau khi leo thang.
   Trên `village` với 7 trigger: `split` giữ **46/46 frame** chia thành 8 mảnh, drift lớn nhất 21,7 px;
   `drop`/`anchor` chỉ giữ **14/46 frame** (cascade) với cùng mức drift 21,7 px.
   **`drop` và `anchor` không được coi là mặc định** vì chúng hy sinh ~70% frame; `anchor` trong thí nghiệm
   này trùng kết quả `drop` (không tìm được keyframe nào không rủi ro).

## Consequence

- **Có thể chạy được cả ba RQ** ngay trên CPU trong ~9 phút (một lần chạy notebook 05), không cần GPU.
- **Kết quả định lượng đã có:**
  - RQ1: chỉ báo đếm điểm **không** báo được lỗi (AUC ≈ 0,59), trong khi EfficientLoFTR vỡ 5–190 px vẫn
    có RMSE nội tại **tốt hơn** SIFT (trung vị thấp hơn) — tức "chỉ số đẹp" không suy ra "ghép đúng".
  - RQ2: gọi matcher mạnh cho **mọi** bước tốn 55 s và drift 82,4 px — **tệ hơn** matcher nhẹ (3 s, 75,3 px);
    phân luồng ở `τ = 0,93` tốn 12 s và drift 28,5 px.
  - RQ3: khi matcher hỏng gần như mọi bước (`grass` + EfficientLoFTR, 44 trigger), **không chiến lược nào
    cứu được bản đồ**: `drop`/`anchor` không đặt nổi frame nào, `split` vỡ thành 45 mảnh một frame.
- **Giới hạn phải nêu khi báo cáo:** drift là số tổng hợp **đơn điệu không đều theo τ** (28,5 px ở 0,93 nhưng
  56,2 px ở 0,95), nên không thể chọn ngưỡng chỉ bằng một cửa sổ; và mọi số ở đây là *đồng thuận với matcher
  tham chiếu*, không phải sai số ngoài thực địa (kế thừa giới hạn `RDR-0007`).
- **Việc còn để nhóm chốt:** ngân sách leo thang (25% đang là giả định), có dùng biến thể leo thang ảnh gốc
  hay không, và có thêm luật "buộc nhận sau N lần bỏ" để chặn cascade của `drop` hay không.

## Liên hệ với quyết định cũ

- **Mở rộng** `RDR-0007` (thêm mức cấp bước + chuỗi tham chiếu), **không phủ định**: metric `chain vs direct`
  ở mức cả chuỗi vẫn là thước đo chính khi chỉ cần 20 frame đầu.
- Không thay đổi `RDR-0005` (dataset) hay `RDR-0006` (danh sách mô hình); `superpoint_lightglue` được dùng
  làm tầng mạnh, `sift_bf` làm tầng nhẹ, `efficientloftr` giữ vai trò **ca chẩn đoán đã biết là vỡ**.
