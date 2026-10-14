# Giải thích và audit Notebook 05: Thử nghiệm phát hiện rủi ro và phục hồi

Đọc cùng [notebook](../notebooks/05_failure_aware_pipeline.ipynb).
Tài liệu phân biệt ý tưởng, số liệu đã lưu và kết luận còn thiếu bằng chứng; không chốt phương pháp thay nhóm.

## Material Passport

| Trường | Giá trị |
|---|---|
| Origin Skill / Mode | `experiment-agent` / `validate` |
| Origin Date / Version Label | 2026-10-14 / `validation_v2` → `validation_v3` (mục 9) |
| Verification Status | `VERIFIED` — notebook chạy lại trọn từ trên xuống sau khi sửa lỗi (mục 9) |
| Overall Confidence | `AMBER` — lỗi tính toán đã sửa và có self-check; giới hạn phương pháp ở mục 7 vẫn nguyên |
| Report đối chiếu | `notebooks/outputs/05_failure_aware/report.json`, stamp `20261014T070805_406984Z` |
| Quyết định phương pháp | [RDR-0008](../docs/decisions/RDR-0008_step_level_metric_and_risk_trigger.md), **Proposed** |

## 1. Notebook làm gì và chưa làm gì?

| RQ | Cách thực hiện trong code | Giới hạn |
|---|---|---|
| RQ1 | So 8 chỉ báo với độ lệch H từng bước so với SIFT tham chiếu | Chỉ phân tích các bước trả H thành công trên cửa sổ chọn sẵn |
| RQ2 | Mô phỏng routing bằng kết quả matcher đã đo, quét ngưỡng | Chi phí cộng gộp matcher, không phải latency toàn pipeline |
| RQ3 | Thử không cứu / bỏ frame / rematch / tách submosaic | Chạy từng matcher cố định, chưa nối sau routing |

Không có pipeline end-to-end “SIFT → LightGlue → kiểm tra lại → split” trong thí nghiệm hiện tại.
RQ3 dùng SIFT cho `village`, EfficientLoFTR cho `grass`, không dùng kết quả leo thang RQ2.
Dự án xử lý hậu kỳ; chưa thử bay realtime, mức pin hay tải máy trên drone.

NCC là **tương quan chéo chuẩn hóa** giữa hai ảnh sau căn chỉnh, không phải độ tương phản.
Nó được tính sau khi có H: phát hiện rủi ro hậu đăng ký, không dự báo trước matching.
Điều kiện `risk()` còn gồm `inlier_ratio < 0,30` hoặc không có H; không chỉ có ngưỡng NCC.

## 2. “Sai” ở đây nghĩa là gì?

SIFT ảnh gốc với 4000 đặc trưng tạo H tham chiếu cho cùng cặp.
`step_error_px` là trung bình độ lệch trên 4 góc và tâm ảnh giữa H được chấm và H tham chiếu.
Đây là **độ bất đồng với matcher tham chiếu**, không phải sai số ngoài thực địa.
Ngưỡng `> 2 px` là quy ước hiện tại, chưa được RDR-0007 hiệu chuẩn trực tiếp cho cấp bước.

Drift Notebook 05 so với **chuỗi H tham chiếu**, khác chain-vs-direct của Notebook 04.
Chuỗi tham chiếu cũng tích lũy sai số; không được đồng nhất hai metric chỉ vì cùng đơn vị pixel.

**Điều kiện tham chiếu chưa được thực thi đúng:** khai báo `MIN_INLIERS=100` nhưng assertion chỉ kiểm tra 30.
Scan `grass` có 7/45 bước dưới 100: bước cục bộ 19–25 có 95, 75, 99, 77, 77, 60, 68 inlier.
`village` có tối thiểu 849. Các điểm và chuỗi phụ thuộc tham chiếu dưới ngưỡng cần xử lý rõ trước khi kết luận.
Các cặp tham chiếu dùng khi rematch cũng chưa được áp gate 100 inlier.

## 3. Vì sao chọn các cửa sổ này?

`village` frame 80–125 và `grass` frame 0–45: mỗi cửa sổ 46 frame, 45 bước.
Chúng được chọn sau lần quét 160 bước để tìm ca khó
([nhật ký quét](../docs/logs/experiments/0001_failure_scan_windows.md)).
Đây là chọn mẫu có chủ đích cho khám phá; chưa đại diện toàn bộ dataset và chưa có tập đánh giá giữ riêng.
Ghép đủ 20/20 frame không chứng minh 20 frame đầu không có lỗi hình học.
Các bước liền nhau phụ thuộc thời gian, không phải 45 quan sát độc lập.

## 4. RQ1 — có tín hiệu phân biệt, chưa có bộ phát hiện đã kiểm chứng

Report hiện tại: `village` / SIFT có 21/45 bước vượt ngưỡng 2 px.

| Chỉ báo | AUC đã lưu |
|---|---|
| `photo_bad_frac` | 0,855 |
| `rmse_px` | 0,839 |
| `overlap_ratio` | 0,788 |
| `photo_ncc` | 0,770 |
| `inlier_ratio` | 0,726 |
| `matches` / `inliers` | 0,598 / 0,591 |
| `hull_area_ratio` | 0,571 |

Code lấy `max(AUC, 1−AUC)` trên chính mẫu đánh giá, tức chọn chiều có lợi sau khi nhìn nhãn.
AUC không phải tỷ lệ dự đoán đúng tại ngưỡng 0,93; chưa có khoảng bất định hoặc kiểm chứng ngoài mẫu.
Không đủ cơ sở gọi chỉ báo 0,57–0,59 “vô dụng”, hoặc khẳng định chỉ NCC mới phát hiện được lỗi.
`photo_bad_frac` đo tỷ lệ pixel lệch >25 mức xám sau warp và trừ trung bình; khác công thức NCC.

**Spearman đang sai trong code và report mới:** rank 1..n bị trừ `(n−1)/2` thay vì trung bình rank.
Kiểm tra cô lập trước đó: hai dãy đảo thứ tự cho 0,2 thay vì −1; biến hằng không được trả không xác định.
Audit lần này tính lại NCC/SIFT bằng tương quan Pearson của rank:

| Sequence | Spearman trong report hiện tại | Tính đúng trên cùng dữ liệu |
|---|---|---|
| `village` | −0,626195 | −0,635837 |
| `grass` | −0,192141 | −0,199209 |

Report cũ từng có giá trị đúng; không dùng kết quả audit report cũ để chứng nhận report mới.
AUC được tính bằng hàm riêng, không trực tiếp chịu lỗi công thức Spearman.

## 5. RQ2 — đọc chi phí và chất lượng cùng phạm vi

Các giá trị dưới đây thuộc stamp ở đầu tài liệu, chỉ cho cửa sổ `village`.

| Chính sách | Bước dùng matcher mạnh | Thời gian matcher cộng gộp | Drift cuối so với chuỗi tham chiếu |
|---|---|---|---|
| Chỉ SIFT | 0/45 | 3,374 s | 75,27 px |
| Chỉ SuperPoint+LightGlue | 45/45 | 55,822 s | 82,42 px |
| Routing τ = 0,93 | 7/45 | 12,432 s | 28,52 px |
| Routing + ảnh gốc | 7/45 | 69,234 s | 35,84 px |

Routing giảm độ lệch cuối khoảng 62% so với chỉ-SIFT **trong cửa sổ này**,
nhưng chậm hơn SIFT; không phải “nhanh và chính xác nhất” theo mọi tiêu chí.
Đồng hồ dừng trước RANSAC, warp/NCC và quyết định risk nên chưa chứng minh lợi ích latency toàn hệ thống.
Chính sách chỉ-learned ghi `escalations=0` vì không leo thang từ SIFT; không có nghĩa không gọi learned matcher.

Ở 7 bước bị gắn cờ, ảnh gốc có độ lệch trung bình 1,49 px so với 4,51 px ở 640 px,
nhưng drift cuối vẫn lớn hơn routing 640 px. Cải thiện cấp bước không bảo đảm cải thiện cả chuỗi.
Chưa có ablation để quy nguyên nhân riêng cho độ thô đặc trưng hay nội suy.

RQ2 chọn ngưỡng riêng: `village` 0,93, `grass` 0,96; RQ3 mới lấy ngưỡng chung từ sweep.
Ngân sách 25% và ngưỡng còn Proposed; fallback `TAU_NCC` khi không có ngưỡng hợp lệ không bảo đảm ngân sách.

## 6. RQ3 — bảo toàn frame khác bảo toàn bản đồ liên tục

| Sequence / matcher | Chính sách | Frame giữ | Mảnh | Bước ghép được ghi | Drift nội bộ lớn nhất |
|---|---|---|---|---|---|
| `village` / SIFT | Không cứu | 46/46 | 1 | 45 | 84,6 px |
| `village` / SIFT | Drop / rematch | 14/46 | 1 | 13 | 21,7 px |
| `village` / SIFT | Split | 46/46 | 8 | 38 | 21,7 px |
| `grass` / EfficientLoFTR | Không cứu | 46/46 | 1 | 45 | 671,3 px |
| `grass` / EfficientLoFTR | Drop / rematch | 1/46 | 1 | 0 | Không đo được |
| `grass` / EfficientLoFTR | Split | 46/46 | 45 | 1 | 2,7 px |

Split đặt lại hệ gốc/chuỗi tham chiếu ở từng mảnh, không tính lỗi qua cạnh đã cắt.
Ở `grass`, 46 frame thành 45 mảnh là 44 mảnh một frame và một mảnh hai frame.
Drift thấp như vậy không chứng minh đã cứu được bản đồ có ích.
Frame gốc mỗi mảnh vẫn được tính là giữ lại dù chưa có bước ghép.

Trong report, drop/rematch `village` có 32 trigger thay vì 7 của none/split; không có rematch thành công.
Đó là kết quả của cửa sổ/chính sách này, không chứng minh drop luôn hỏng hoặc split là cách duy nhất.
Cần đánh giá kích thước mảnh, số cạnh liên thông và ảnh mosaic; notebook chưa xuất mosaic cho từng recovery.

## 7. Trạng thái code và kiểm chứng

Notebook hiện lưu 14/14 code cell đã chạy, không lưu exception.
Lỗi `chosen_strong` đã được sửa trước audit này; routing đã qua smoke 9 ngưỡng × 2 scan ở lần sửa đó.
Các kiểm tra cô lập trước đây xác nhận thêm:

| Vị trí | Phát hiện chưa sửa |
|---|---|
| `chain_from_steps()` | Row `status="failed"` thiếu H gây `KeyError` thay vì được xử lý thành kết quả thất bại |
| `try_anchor()` | Với `placed=[0,2]` có thể chọn frame 1, chưa có H về gốc |
| Assertion chặn trên drift | Scale 10× rồi lệch 1 px cho drift 10 px, vượt chặn 2 px của hai bước; bất đẳng thức không đúng tổng quát |
| Assertions nghiên cứu | Ép mô hình phải sai/NCC phải tách được/drop phải giữ ít frame; không phải bất biến code |
| Output cố định | Scan ghi trước RQ2, report ở cuối; chạy lỗi có thể để artifact khác run cạnh nhau |

Audit lần này đối chiếu report hiện tại và tính lại Spearman, không chạy lại model hay ghi đè artifact.
**Verdict tái lập toàn notebook: `CANNOT_VERIFY`**, khác với việc đã thấy một lần chạy được lưu.
Chưa sửa các lỗi còn lại hoặc phê chuẩn ngưỡng trong RDR-0008.

## 8. Rà soát sai lệch phương pháp — 11/11 nhóm

| Nhóm | Kết quả trong phạm vi audit |
|---|---|
| Simpson | Chưa thấy bằng chứng đảo chiều do gộp nhóm; RQ1 tách sequence/matcher |
| Ecological fallacy | Tránh suy chất lượng cả bản đồ chỉ từ chỉ báo cấp bước |
| Berkson | Có chọn cửa sổ theo lỗi, chưa xác nhận nghịch lý cụ thể |
| Collider | Lọc bước thành công tạo điều kiện chọn mẫu; chưa xác lập quan hệ nhân quả collider |
| Base-rate neglect | Tỷ lệ bước sai ở cửa sổ chọn lọc không đại diện triển khai |
| Regression to the mean | Không có thiết kế trước–sau đủ để xác nhận vấn đề này |
| Survivorship | RQ1 chỉ chấm H thành công; recovery chỉ đo phần giữ/ghép được |
| Look-elsewhere | Quét chỉ báo/chiều AUC/ngưỡng trên cùng dữ liệu gây nguy cơ lạc quan |
| Forking paths | Nhiều lựa chọn khám phá, chưa phải đánh giá xác nhận ngoài mẫu |
| Correlation ≠ causation | Chỉ báo tương quan không giải thích nguyên nhân lỗi |
| Reverse causality | NCC sau đăng ký không chứng minh dự báo trước matching |

**Ưu tiên:** sửa tính đúng và gate tham chiếu → chạy lại có provenance nhất quán →
đánh giá sequence giữ riêng → đo latency đầy đủ và routing nối recovery.
Notebook là thực nghiệm khám phá ba RQ, chưa phải lời giải hoàn chỉnh cho UAV thực tế.

## 9. ĐÍNH CHÍNH sau khi sửa lỗi tính toán (2026-10-14, `validation_v3`)

Các mục dưới đây **thay thế** phát hiện tương ứng ở trên; phần audit gốc giữ nguyên để đối chiếu.
Notebook đã chạy lại trọn từ trên xuống (`report.json` stamp `20261014T070805_406984Z`), nên mọi bảng mục 4–6
phải đọc lại theo artifact mới.

| Lỗi ở bản `validation_v2` | Cách sửa trong notebook | Kết quả sau khi sửa |
|---|---|---|
| `report.json` còn số Spearman của bản cũ (`village`/SIFT/NCC = −0,6262) dù code đã đúng | sinh lại artifact bằng một lần chạy trọn, có self-check trước khi ghi | ρ = -0,6358 (đúng như audit tính lại) |
| `MIN_INLIERS = 100` chỉ khai báo, assertion kiểm 30 | cổng tham chiếu áp thật: bước dưới ngưỡng **bị loại khỏi RQ1** (`n_invalid_reference`), vẫn giữ trong chuỗi RQ2/RQ3 và đếm `reference_invalid_used`; in cảnh báo khi quét | `grass` loại 7 bước (min 60 inlier), `village` loại 0 |
| AUC lấy `max(AUC, 1−AUC)` sau khi đã nhìn nhãn | chiều từng chỉ báo khai báo trước (`INDICATOR_SUSPICION`); AUC < 0,5 = tách ngược chiều kỳ vọng | `matches` 0,402 và `inliers` 0,409 — thấp hơn 0,5, tức **ngược chiều**, không còn 0,598/0,591 |
| `chain_from_steps()` ném `KeyError` khi row lỗi thiếu H | dừng chuỗi, ghi `chained_steps`; assertion buộc chuỗi RQ2 nối hết bước | không còn đường ném lỗi; chuỗi nối đủ 45 bước |
| `try_anchor()` có thể chọn frame **chưa đặt** vào bản đồ (tra `H_to_root` -> `KeyError` hoặc drift sai gốc) | chỉ neo vào các frame **đã đặt** gần nhất, bỏ frame vừa ghép hỏng | ca `placed=[0,2]` không còn thử frame 1 |
| Assertion "drift ≤ tổng sai số các bước" sai tổng quát (H co giãn được) | thay bằng phép replay: mọi bước đặt bằng **đúng H tham chiếu** -> drift phải bằng 0, kiểm cho cả chuỗi RQ2 lẫn pipeline RQ3 | lưới bắt lỗi trộn hệ toạ độ vẫn còn, nhưng đúng về toán |
| `scan_*.json` ghi giữa chừng, `report.json` ghi cuối -> chạy lỗi để lại artifact trộn hai lần chạy | mọi artifact ghi **một lần ở cell cuối**, sau các self-check | file trên đĩa luôn cùng một lần chạy |

Số liệu sau khi sửa (cửa sổ `village`, 45 bước, cùng ngưỡng): chỉ-SIFT 3,2 s / 75,3 px; chỉ SuperPoint+LightGlue
60,4 s / 82,4 px; phân luồng τ = 0,93 leo thang 16% số bước -> 13,3 s / 28,5 px; leo thang ở ảnh gốc 73,6 s / 35,8 px.
RQ3 (matcher cố định, cùng τ = 0,93): `village`/SIFT giữ 46/46 frame khi không cứu, drop 14, anchor 14,
split 46 frame / 8 mảnh; `grass`/EfficientLoFTR: split 46 frame / 45 mảnh.

**Liên quan `RDR-0008` (Proposed) — không sửa vì RDR append-only:** AUC/thời gian RDR trích thuộc lần chạy cũ và
**chiều AUC đã bị lật** (`matches`/`inliers` nay 0,402/0,409 -> kết luận "loại khỏi vai trò chỉ báo" **mạnh hơn**);
mọi con số chất lượng giữ nguyên (0,770–0,855; drift 28,5 px; 1,49 px so với 4,51 px), chỉ thời gian lệch ~10%.

**Còn lại chưa sửa** (không phải lỗi tính toán, phải nêu khi báo cáo): assertion ở mục 7 vẫn là *kỳ vọng
nghiên cứu* nên sẽ vỡ ở sequence khác; `choose_tau()` vẫn im lặng rơi về `TAU_NCC` khi không ngưỡng nào
nằm trong ngân sách; đồng hồ RQ2 chỉ tính thời gian matcher, chưa gồm RANSAC/warp/quyết định risk;
`try_anchor` sau khi sửa vẫn chưa được thiết kế thành “buộc nhận sau N lần bỏ” nên cascade bỏ frame
vẫn chưa được chặn.
