# Tổng hợp kết quả thực nghiệm phục vụ viết paper

## 1. Material Passport và kết luận chính

- Ngày tổng hợp: 2026-11-04; chế độ `experiment-agent / validate`; trạng thái **ANALYZED**, không phải tái lập thực nghiệm.
- Nguồn là artifact cloud đã lưu; tính lại thống kê CSV/JSON trên local, không chạy notebook/model. Không thay đổi artifact, paper hoặc quyết định phương pháp.
- Bằng chứng hiện tại ủng hộ **đánh giá failure-aware có điều kiện**, chưa chứng minh một pipeline vừa nhanh hơn vừa chính xác hơn mọi baseline.
- RQ1: chỉ báo có tín hiệu nhưng khác nhau theo sequence; NCC không phải chỉ báo mạnh nhất. RQ2: routing giảm bất đồng cấp bước trong một số cảnh, nhưng chậm hơn learned-only ở run này. RQ3: split giữ frame bằng cách đánh đổi tính liên tục; không đồng nghĩa cứu được bản đồ toàn cục.
- [RDR-0011](../logs/decisions/RDR-0011_loso_and_technical_readiness.md) chốt LOSO; [RDR-0008](../logs/decisions/RDR-0008_step_level_metric_and_risk_trigger.md) vẫn **Proposed**. Mọi ngưỡng và kết quả dưới đây mang tính khám phá.

## 2. Nguồn số liệu và khả năng so sánh

Mọi đường dẫn run trong bảng nằm dưới [`notebooks/outputs/`](../../notebooks/outputs/); dùng `completed.json` thành công, không lấy số liệu từ tên thư mục mới nhất một cách máy móc.

| Ký hiệu | Thư mục / run chính | Artifact dùng |
|---|---|---|
| B | `classical_mosaicking_baseline/20261101T153341_784110Z` | `metrics_{sift,orb}_406frames.json`, mosaic PNG |
| P | `deep_matching_pilot/20261101T161621_999565Z` | `mosaic_{sift,superpoint}/metrics.json` |
| M | `feature_matcher_benchmark/20261101T163603_779942Z` | `manifest.json`, `summary.csv`, `mosaic_summary.csv` |
| D | `accumulated_drift_evaluation/20261103T165349_596427Z` | `drift_selfconsistent.json`, `trajectory_check.json` |
| F | `failure_aware_pipeline/20261101T183829_171190Z` | `report.json`, 8 `scan_*.json`, `summary.png` |

- Các run pilot/lịch sử được giữ riêng, không gộp vào trung bình full. F/`20261101T173552_053013Z` không có marker hoàn tất nên bị loại.
- D trỏ đúng M; SHA-256 của byte `manifest.json` đã tính lại và khớp `1e609ab397ce2e06fa9d4f72e7c47aadfb958d3d85bc8afdfa9ded8f58aae202`.
- M có **3.898 ảnh / 3.890 cặp liên tiếp**; F có **3.899 ảnh / 3.891 bước**. 3.898 đường dẫn chung khớp hash và kích thước xử lý.
- Sai khác xác định được: F giữ thêm `phantom3-centralPark-kfs/rgb/1454510665.360000 (1).jpg`, có cùng hash với bản không có `(1)`; M đã loại bản trùng. Không coi M và F là cùng tập đầu vào tuyệt đối; không âm thầm xoá dòng rồi coi đó là kết quả chạy lại.
- M/F xử lý cạnh dài 640 px, kích thước theo bội 32, tối đa 2.000 keypoint; ví dụ ảnh 1920×1080 thành 640×352. F: RANSAC 3 px, ratio 0,75, seed 0, gate tham chiếu 100 inlier.
- M ghi CPU 4 threads cho SIFT/ORB-BF, CUDA cho các matcher learned; F ghi `device=cuda`, Torch 2.11.0+cu130, OpenCV 4.14.0, NumPy 2.1.3. Không suy ra mọi công đoạn đều chạy GPU hay tự gán GPU T4 khi artifact chưa chứng minh model GPU cụ thể.
- RQ3 dùng matcher cố định, **không phải kết quả routing RQ2 nối tiếp recovery**: SIFT-BF cho 7 sequence, EfficientLoFTR cho grass. LOSO không biến thí nghiệm thành pipeline tích hợp end-to-end.

## 3. Đọc metric đúng trước khi so sánh

| Metric | Ý nghĩa và giới hạn |
|---|---|
| Pair success, RMSE inlier | Có H theo kiểm tra của matcher; residual trên inlier. Không chứng minh H đúng toàn cảnh hoặc chuỗi ổn định. |
| Step error (F) | Bất đồng H với SIFT ảnh gốc tham chiếu, trên 4 góc + tâm; pixel ảnh gốc. Nhãn bad là >2 px, chưa là lỗi trắc địa. |
| Common ATE (D) | Căn trung bình bình phương độ lệch chain-vs-direct trên cùng tập frame hợp lệ của cả 7 matcher, bỏ frame 0. Không phải ATE trajectory theo mét. |
| Drift (F) | So với **chuỗi** H tham chiếu; khác tham chiếu trực tiếp về frame 0 của D. Sau split đổi gốc đo. |
| Final drift | Có thể là frame cuối **còn đo được**, không phải frame cuối sequence; phải kèm chỉ số frame và availability. |
| Retained / coverage | Frame đã đặt gồm cả root của mảnh; độ phủ canvas là tỷ lệ pixel canvas, không phải diện tích thực địa. |
| Macro / pooled | Macro là trung bình các giá trị theo sequence, mỗi sequence cùng trọng số; pooled là cộng tử/mẫu hoặc trung bình mọi cặp. Không đổi lẫn hai cách. |

## 4. Baseline ảnh gốc và deep pilot

B/P full đều chạy trên village, 406 frame, ảnh gốc. Đây là kiểm chứng ghép ảnh và so sánh minh hoạ, không phải bảng tốc độ chuẩn hoá trên 8 sequence.

| Cấu hình | Frame ghép | Thời gian đã lưu (s) | Phạm vi đồng hồ |
|---|---:|---:|---|
| SIFT-BF (B) | 406/406 | 858,88 | `pipeline_total_seconds` |
| ORB-BF (B) | 406/406 | 231,72 | `pipeline_total_seconds` |
| SIFT-LightGlue (P) | 406/406 | 1.292,46 | `chain_total_seconds`, không cộng thử cặp riêng |
| SuperPoint-LightGlue (P) | 406/406 | 512,40 | `chain_total_seconds`, không cộng thử cặp riêng |

Đã xem mosaic B: ORB có biến dạng kéo dài rõ; SIFT vẫn có đường nối/mảng màu. Cả hai giữ đủ frame nên **406/406 không phải tiêu chí hình học đủ**. Quan sát ảnh thu nhỏ không thay cho kiểm định định lượng. Mosaic P có chiều rộng canvas 5.000 px, coverage lần lượt 82,45% và 75,15%; không diễn giải thành phần trăm đất được lập bản đồ.

## 5. Benchmark 7 matcher: pair thành công không bảo đảm mosaic

Tính lại từ M/`summary.csv`: mỗi matcher có 3.890 cặp. Match time là trung bình pooled trên mọi cặp (kể cả failed); RMSE là trung bình trên cặp `status=success`. Frame ghép lấy từ `mosaic_summary.csv`, mẫu số mỗi matcher là 3.898.

| Matcher | Cặp success | Match s/cặp | RMSE px | Frame ghép | Sequence ghép đủ /8 | Macro common ATE D (px) |
|---|---:|---:|---:|---:|---:|---:|
| SIFT-BF | 3.875 | 0,220 | 0,559 | 3.740 | 6 | 49,15 |
| ORB-BF | 3.889 | 0,054 | 1,096 | 3.535 | 6 | 170,51 |
| SIFT-LightGlue | 3.889 | 0,329 | 0,628 | 3.766 | 7 | 45,08 |
| SuperPoint-LightGlue | 3.889 | 0,067 | 1,282 | 3.694 | 6 | 83,13 |
| XFeat-MNN | 3.888 | 0,019 | 1,353 | 3.071 | 5 | 138,29 |
| XFeat-LighterGlue | 3.888 | 0,044 | 1,311 | 3.391 | 4 | 59,12 |
| EfficientLoFTR | 3.884 | 0,184 | 0,917 | 1.062 | 0 | 3.143,64 |

SIFT-LightGlue có macro common ATE thấp nhất trong run này và giữ nhiều frame nhất, nhưng không thắng từng sequence và không ghép đủ toàn dataset. XFeat-MNN nhanh nhất theo đồng hồ matching, không phải chất lượng tốt nhất. EfficientLoFTR có residual inlier nhỏ nhưng chuỗi rất kém: cần phân biệt residual nội bộ với độ đúng toàn cục; chưa đủ bằng chứng quy nguyên nhân cho domain shift hoặc trọng số pretrained.

## 6. Drift chain-vs-direct: tập đánh giá nhỏ và có thiên lệch tham chiếu

D dùng H đã ghép được từ M. **Trong D, `frames_requested` bằng số frame đã ghép của M, không phải số ảnh dataset ban đầu**; chia `frames_stitched/frames_requested` của D sẽ cho 100% giả tạo về coverage đầu vào. Dùng mẫu số 3.898 từ M khi báo retention; riêng grass đầu vào là 648, dù chuỗi SIFT-LightGlue truyền sang D chỉ có 516 frame.

| Sequence (bỏ tiền tố camera và `-kfs`) | Ảnh M | Frame common D | Common ATE SIFT-BF | Common ATE SIFT-LG | Bước F | Tham chiếu bước F invalid |
|---|---:|---:|---:|---:|---:|---:|
| monticules | 395 | 11 | 11,32 | 13,29 | 394 | 0 |
| npu | 337 | 16 | 3,27 | 3,14 | 336 | 0 |
| saplings | 482 | 12 | 5,97 | 6,61 | 481 | 0 |
| centralPark | 835 | 35 | 166,67 | 78,82 | 835 | 1 |
| factory | 402 | 7 | 32,49 | 36,59 | 401 | 4 |
| grass | 648 | 6 | 1,84 | 1,89 | 647 | 84 |
| huangqi | 393 | 27 | 54,59 | 89,09 | 392 | 0 |
| village | 406 | 24 | 117,09 | 131,18 | 405 | 0 |

Chỉ **138 frame common** trên 8 sequence; không gọi đây là đánh giá drift trên mọi frame. Những đoạn quay lại gần frame gốc có thể được đo lại; common không nhất thiết là prefix liên tục. SIFT-BF vừa là đối tượng chấm vừa cùng họ với tham chiếu SIFT: giá trị của nó là mức nền tự nhất quán, không phải sàn sai số ground truth. `trajectory_check.json` ghi `disabled_or_unavailable`; không có căn cứ đổi pixel thành mét.

## 7. RQ1: chỉ báo nào phát hiện bất đồng cấp bước?

F có 89 bước tham chiếu invalid; SIFT có 11 bước không trả H. Sau các điều kiện lọc, NCC/SIFT còn **3.794 bước**, trong đó **1.075 (28,33%)** có step error >2 px. Không cộng 89 và 11 một cách máy móc vì hai tập có giao nhau. AUC dùng chiều nghi ngờ khai báo trước, không lấy `max(AUC,1−AUC)`.

| Chỉ báo SIFT | Macro Spearman với step error | Macro AUC (8 sequence) |
|---|---:|---:|
| RMSE inlier | 0,728 | 0,882 |
| Photo bad fraction | 0,613 | 0,834 |
| NCC | −0,484 | 0,762 |
| Hull area ratio | −0,449 | 0,731 |
| Overlap ratio | −0,452 | 0,720 |
| Inlier ratio | −0,356 | 0,716 |
| Inlier count | −0,127 | 0,557 |
| Match count | −0,091 | 0,535 |

NCC AUC theo thứ tự sequence ở mục 6: **0,636; 0,803; 0,672; 0,871; 0,754; 0,721; 0,803; 0,838**. Đây là phân tích mô tả mỗi sequence, không phải accuracy của một classifier LOSO đã chọn tối ưu. NCC được tính **sau đăng ký**, vì vậy gọi là phát hiện rủi ro hậu đăng ký, không phải dự báo trước matching.

SuperPoint-LightGlue: 2.097/3.802 bước hợp lệ vượt 2 px, macro NCC AUC 0,743. EfficientLoFTR: 3.796/3.802 vượt ngưỡng; 7 sequence chỉ có một lớp nên AUC không xác định. AUC 0,996 của centralPark chỉ có 6 bước lớp tốt, **không được quảng bá là AUC 0,996 trên 8 sequence**. Sự bất đồng với SIFT chưa tự nó chứng minh nguyên nhân mô hình lỗi.

## 8. RQ2: LOSO routing và chi phí thực đo

Đã kiểm tra 8 fold, mỗi test sequence không xuất hiện trong 7 train sequence. Chọn τ lớn nhất trong grid 0,90–0,99 sao cho **mọi sequence train** có escalation ≤25%; τ=0,92 khi giữ saplings, 0,90 ở 7 fold còn lại. Risk gồm NCC thấp, inlier ratio <0,30 hoặc thiếu H; không chỉ NCC.

| Policy | Failed H /3.891 | Escalation | Tổng seconds | Macro mean step error (px) |
|---|---:|---:|---:|---:|
| Classical SIFT | 11 | 0 | 792,03 | 6,676 |
| Learned-only SP-LG | 0 | Không áp dụng | 261,55 | 3,338 |
| Routed | 0 | 315 (8,10%) | 813,70 | 2,940 |
| Routed full-resolution | 0 | 315 (8,10%) | 974,95 | 2,843 |

`seconds` cộng matching + geometry + chỉ báo từ các kết quả đã đo; routed cộng cả cheap và strong khi leo thang. GPU được đồng bộ khi đo; I/O tách riêng. Đây **không phải wall-clock end-to-end**, không gồm toàn bộ warp/blend, nạp model và điều phối. “Cheap” là vai trò thiết kế, không đúng về tốc độ đo lần này: routed chậm gấp **3,11 lần** learned-only, dù chỉ gọi strong cho 8,10% bước.

| Sequence | Routed escalation | Drift classical → routed (px) | Frame cuối còn đo / bước yêu cầu |
|---|---:|---:|---:|
| monticules | 2/394 | 3.904,57 → 2.490,70 | 394/394 |
| npu | 26/336 | 458,72 → 458,88 | 336/336 |
| saplings | 126/481 | 5.992,82 → 8.066,21 | 481/481 |
| centralPark | 32/835 | 270,43 → 107,40 | 834/835 |
| factory | 58/401 | 2.227,57 → 1.630,50 | 375/401 |
| grass | 49/647 | 3,46 → 3,46 | 18/647 |
| huangqi | 2/392 | 65,25 → 87,13 | 392/392 |
| village | 20/405 | 565,68 → 494,11 | 405/405 |

Saplings test leo thang **26,20%**, vượt ngân sách 25% dù fold ghi `budget_compliant`: nhãn đó chỉ nói train. Step error macro giảm không đảm bảo drift cuối giảm; saplings/npu/huangqi là phản ví dụ. Grass chỉ đo drift đến bước 18: 3,46 px không chứng minh chuỗi 647 bước tốt. Không gộp các giá trị cuối bị kiểm duyệt này thành một bảng xếp hạng drift toàn sequence.

## 9. RQ3: giữ frame, khả năng nối và phân mảnh

Các policy được chấm trên cùng sequence/ngưỡng LOSO nhưng matcher khác giữa grass và các cảnh khác. Drop bỏ frame rủi ro; anchor thử neo vào frame đã đặt; split mở gốc mới. Root được tính là retained nhưng không phải cạnh đăng ký thành công.

| Policy | Frame giữ /3.899 | Retention | Frame có bước nối | Tổng mảnh | Anchor thành công | Phép đo drift hợp lệ, bỏ root |
|---|---:|---:|---:|---:|---:|---:|
| None | 3.872 | 99,31% | 3.864 | 8 | 0 | 3.235 |
| Drop | 1.693 | 43,42% | 1.685 | 8 | 0 | 1.685 |
| Anchor | 1.706 | 43,75% | 1.698 | 8 | 3 | 1.698 |
| Split | 3.899 | 100% | 3.104 | 795 | 0 | 3.092 |

| Sequence | Split: số mảnh | Mảnh lớn nhất (frame) | Mảnh một frame | Max drift none → split (px) |
|---|---:|---:|---:|---:|
| monticules | 3 | 326 | 0 | 18.693.670 → 18.693.670 |
| npu | 27 | 308 | 23 | 533,85 → 533,85 |
| saplings | 127 | 110 | 95 | 12.205,12 → 948,17 |
| centralPark | 33 | 293 | 7 | 4.485,93 → 788,50 |
| factory | 59 | 157 | 44 | 13.018,44 → 4.486,89 |
| grass | 522 | 15 | 485 | 499,23 → 85,44 |
| huangqi | 3 | 328 | 0 | 238,08 → 170,53 |
| village | 21 | 188 | 8 | 694,53 → 330,37 |

Split giảm drift nội bộ ở 6/8 sequence nhưng đổi gốc và loại cạnh qua biên mảnh, nên không thể so như cùng một trajectory liên tục. Grass giữ 648 frame nhưng 485 mảnh đơn, chỉ 114 phép đo drift hợp lệ; drop/anchor chỉ giữ root, drift là N/A chứ không phải 0. Monticules còn cực trị 18,7 triệu px ở mọi policy: bằng chứng chưa giới hạn được drift, cần chẩn đoán homography/điểm chiếu trước kết luận nguyên nhân. Anchor chỉ cứu thành công 3 lần trong cả run.

## 10. Nội dung đưa vào paper và phần chưa được khẳng định

- **Experimental setup:** ghi dataset 8 sequence, resize, backend, seed, ngưỡng khám phá, LOSO train-only và lịch sử dùng village/grass để phát triển chỉ báo; công bố ảnh trùng centralPark.
- **Results:** dùng bảng benchmark mục 5, coverage/common ATE mục 6, chỉ báo mục 7, latency + error + availability mục 8, retention + fragmentation mục 9. Giữ kết quả âm; không chọn riêng village để tuyên bố routing thắng.
- **Hình:** baseline SIFT/ORB làm minh hoạ “ghép đủ vẫn méo”; drift cần panel riêng mỗi sequence và biên split. F/`summary.png` đã xem nhưng legend quá dày và cực trị monticules lấn át phần còn lại, chưa thích hợp bê nguyên vào paper.
- **Discussion:** bằng chứng mạnh là sự tách biệt giữa residual/cặp thành công và chất lượng chuỗi, cùng trade-off phục hồi. Chưa có bằng chứng “routing tiết kiệm thời gian so learned-only”, “split cứu bản đồ liên tục”, “NCC tốt nhất”, “độ chính xác địa lý”, hay “realtime UAV”.
- **Trước đánh giá xác nhận:** thống nhất lọc trùng input, chốt các lựa chọn Proposed bằng quyết định của nhóm, kiểm tra riêng sai lệch EfficientLoFTR và cực trị monticules, rồi chạy cloud nếu cần. Không sửa số liệu cũ để ép giả thuyết.
- **Chưa có trong phân tích này:** CI/p-value, lặp nhiều seed, kiểm định độ nhạy ngưỡng, ground truth độc lập, đo latency tích hợp routing→recovery, định lượng coverage thực địa và kiểm tra trực quan mọi mosaic. Chênh lệch mô tả không được gọi là có ý nghĩa thống kê.

## 11. Kiểm chứng và rà soát sai lệch

Đã tính lại bảng M từ CSV; macro common ATE D từ 56 dòng; kiểm hash manifest D→M; so hash/kích thước ảnh M↔F; đối chiếu 8 scan rời bằng nội dung scan trong report; tính độc lập lại NCC AUC/SIFT và mẫu số trên 8 sequence; kiểm 32 dòng recovery với `frames_placed = frames_with_step + submosaics`; đếm mảnh từ `records`. Không chạy lại model để chứng nhận tái lập.

Rà soát 11/11 nhóm: **Simpson** (giữ bảng từng sequence, không suy từ pooled); **ecological** (không suy chất lượng bản đồ từ AUC); **Berkson/collider** (lọc H/tham chiếu tạo selection, chưa xác lập cấu trúc nhân quả); **base rate** (công bố tỷ lệ bad và lớp suy biến); **regression to mean** (không có thiết kế lặp trước–sau để kết luận); **survivorship** (công bố frame dừng, N/A và root); **look-elsewhere/forking paths** (nhiều chỉ báo/ngưỡng, còn khám phá); **correlation≠causation** (không quy nguyên nhân lỗi từ tương quan); **reverse causality** (NCC đo sau đăng ký). Frame liền kề không độc lập; đơn vị báo cáo chính là sequence, không phải hàng nghìn phép lặp độc lập.

Tài liệu này là bản tổng hợp run mới; các audit lịch sử trong [pipeline](failure_aware_mosaicking_pipeline.md), [drift](accumulated_drift_evaluation.md) và [thiết kế metrics](experiment_design_and_metrics.md) cần đọc theo ngày/run, không trộn số liệu cũ vào bảng trên.
