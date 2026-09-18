# Đợt quét 2 — targeted novelty audit cho RQ1–RQ3

**Ngày:** 2026-09-19. **Mục đích:** bằng chứng để đánh giá điều kiện dừng RDR-0001 cho ba cụm RQ. **Cập nhật giữa đợt:** RDR-0002 (dataset phải opensource + dữ liệu drone thật) — đã áp dụng vào mục hệ quả dataset bên dưới.

## Phương pháp

- Mỗi cụm RQ: hai lượt — (1) keyword retrieval, (2) citation/related-term chaining từ các paper trực tiếp mạnh nhất.
- Ba nhánh chạy song song; phiên chính kiểm chứng chéo metadata trên trang nhà xuất bản/CVF/Copernicus/PMC/AAAI/NeurIPS, Crossref và arXiv API.
- Cửa sổ 2022–2026 cộng seminal khi cần. Không phải PRISMA; số hit ghi nhận = top-N trả về của provider, không phải tổng database.
- Sự cố công cụ 2026-09-19: một đợt truy vấn gặp rate-limit đồng loạt (parallel 429, codex timeout, các provider khác chặn bot); đã chạy lại bằng từ khóa tương đương và bù bằng citation chaining — ghi nhận để tái lập.
- Bản ghi đầy đủ từng truy vấn: transcript ba nhánh (`history://AuditFailureSignals`, `history://AuditMatcherRouting`, `history://AuditRecoveryActions`).

## RQ1 — Failure prediction (dự báo lỗi đăng ký và drift từ chỉ báo rẻ)

**Trạng thái tạm: NARROW.** Ý tưởng "dùng tín hiệu cặp-frame giá rẻ phát hiện khớp sai" đã tồn tại (VPR: Zaffar 2024, Sferrazza 2025; homography: HEB 2023, VSAC 2021; classical quy mô lớn: Yuan 2024). Khoảng trống sống sót nằm ở miền UAV + nhãn homography/drift + calibration tiền cứu.

### Bằng chứng chính

| Paper | Năm / Venue | Độ trực tiếp | Tác động lên novelty | Kiểm chứng |
|---|---|---|---|---|
| Zaffar et al., On the Estimation of Image-matching Uncertainty in VPR | 2024, CVPR | trực tiếp với bài toán so sánh chỉ báo | THREATENING: so sánh L2/ratio/inlier count vs learned uncertainty đã có; nhãn = VPR match correctness, không phải lỗi homography | CVF + arXiv + Crossref |
| Sferrazza et al., To Match or Not to Match (VPR) | 2025, CVPRW/IMW | trực tiếp | THREATENING: 18 pipeline; inlier count ≈ mạnh nhất (AUPRC ~94.8–94.9); có false positive high-inlier | CVF + DOI |
| Barath et al., A Large-Scale Homography Benchmark (HEB) | 2023, CVPR | trực tiếp (GT homography pairwise) | BOUNDARY/CONTRARY: inlier count và reproj error không phải proxy hoàn hảo; benchmark public dùng được | CVF + arXiv |
| Yuan et al., Comparative Analysis of Color Space… Feature-Based Image Registration | 2024, J. Imaging 10(5):105 | trực tiếp (classical pairwise) | THREATENING: 1,95M lượt đăng ký; RE có R²≈0.002 với RMSE/SSIM; feature count chỉ liên quan yếu | PMC full text |
| Li et al., Real-Time Incremental Video Mosaic (UAV) | 2023, Remote Sensing 15(8):2127 | trực tiếp UAV; chỉ báo là heuristic vận hành | BOUNDARY: dùng IoU + weighted reproj error; không đánh giá dự báo | Crossref + PDF MDPI |
| Hwang et al., Real-Time 2D Orthomosaic Mapping | 2026, Applied Sciences 16(4):2133 | trực tiếp đúng regime | SUPPORTING: ngưỡng inlier để reject update; không có nhãn drift, không kiểm dự báo | Crossref + PDF MDPI |

### Chuỗi existing → limitation → proposed difference

VSAC 2021 (reject model bằng inlier độc lập) → HEB 2023 (GT pairwise quy mô lớn; inlier/reproj không hoàn hảo) → Yuan 2024 (metric pairwise bất đồng ở quy mô rất lớn) → Zaffar 2024 / Sferrazza 2025 (inlier count phân biệt tốt ở VPR, nhưng nhãn = khoảng cách GPS, false positive tồn tại) → Li 2023 / Hwang 2026 (UAV mosaicking dùng heuristic IoU/inlier/reproj nhưng không xác nhận dự báo, không drift định lượng).

**Gap sống sót:** nghiên cứu tiền cứu, đa miền UAV, so sánh các chỉ báo classical giá rẻ — đơn lẻ và kết hợp — đối chiếu với CẢ lỗi homography tức thời LẪN drift tích luỹ mức mosaic, calibration domain-disjoint, public data + free compute. Đóng góp = benchmark + calibration + liên kết pairwise→sequence; không claim chỉ báo mới.

## RQ2 — Adaptive matcher routing (classical-first → learned fallback)

**Trạng thái tạm: NARROW.** Không tìm thấy công trình làm đúng policy cross-matcher classical-first + risk gate + learned fallback có đánh giá mosaic-level quality/latency. Nhưng: adaptive compute bên trong matcher (LightGlue), cascade nội bộ (CasP), gate tiền xử lý (OETR), chọn descriptor (Hu & Lin 2016) đều đã có; cheap always-learned (XFeat, ELoFTR, ETO) đe dọa trực tiếp lợi ích latency của routing.

| Paper | Năm / Venue | Độ trực tiếp | Tác động |
|---|---|---|---|
| LightGlue | 2023, ICCV | gần-trực tiếp | THREATENING: adaptive depth/width + early exit bên trong một learned matcher; không chọn classical/learned |
| Hu & Lin, Progressive Feature Matching w/ Alternate Descriptor Selection | 2016, CVPR (seminal) | trực tiếp cho adaptive selection | THREATENING: chọn descriptor theo keypoint đã có; không phải fallback cặp-frame |
| OETR (Guide Local Feature Matching by Overlap Estimation) | 2022, AAAI | gián tiếp (gate signal) | SUPPORTING/BOUNDARY: học overlap/scale trước khi match; pipeline luôn cố định; tự thêm cost (train 2×V100×48h) |
| XFeat | 2024, CVPR | gián tiếp (baseline learned giá rẻ) | CONTRARY: sparse ~27 FPS trên CPU i5 → có thể xóa lợi thế latency của classical-first |
| Efficient LoFTR | 2024, CVPR | gián tiếp | CONTRARY: ~27–35 ms GPU; token selection nội bộ; tác giả ghi nhận chưa có early stop |
| ETO | 2024, NeurIPS | gián tiếp | CONTRARY/BOUNDARY: 21–22 ms; homography hypotheses nội bộ; train 3×RTX3090×80h |
| CasP | 2025, ICCV | gián tiếp | BOUNDARY: cascade nội bộ cố định; ~2.2× nhanh hơn ELoFTR ở 1152 px; train 8×V100×30 epochs |
| Kim & Kim, Robust UAV Image Mosaicking Using SIFT and LightGlue | 2025, ISPRS Archives (UAV-g) | trực tiếp ứng dụng UAV | THREATENING cho "SIFT+LightGlue là mới"; SUPPORTING cho complementarity: classical giữ epipolar/reproj error thấp hơn, SIFT+LightGlue cứu low-texture; KHÔNG đo latency; dataset không public |

**Gap sống sót:** chạy classical homography trước; tính risk score calibrated từ output classical; gọi learned matcher (pretrained frozen) chỉ khi rủi ro cao; đánh giá quality + latency mức mosaic cuối so với always-classical, always-learned và budget-matched (XFeat sparse, LightGlue depth giới hạn). Không claim adaptive compute/cascade/confidence gate là mới.

**Kill-switch trong contract:** nếu budget-matched always-learned thắng mọi điểm trên biên Pareto ở dữ liệu UAV → hạ RQ2 xuống ablation. Chỉ train/calibrate gate (free-GPU); không retrain matcher.

## RQ3 — Confidence-triggered recovery (reject / rematch / split)

**Trạng thái tạm: NARROW.** Cả ba hành động đã tồn tại riêng lẻ; khoảng trống = so sánh có kiểm soát dưới một trigger thống nhất + policy chọn hành động.

| Paper | Năm / Venue | Hành động | Tác động |
|---|---|---|---|
| Hwang et al. | 2026, Applied Sciences | reject update khi thiếu inlier | THREATENING: reject tồn tại; không ablation, không công bố tỷ lệ reject; data on-request |
| Li et al. | 2023, Remote Sensing | rematch keyframe lịch sử (luôn bật cho keyframe được nhận, chọn min weighted reproj) | THREATENING: rematch tồn tại; không phải failure-triggered |
| Yuan et al., Real-Time Mosaic Method … Two-Stage Key Frame Selection | 2024, Open J. Applied Sciences 14 (SCIRP — chất lượng venue chưa đánh giá độc lập) | trigger 4 px remapping error → backoff frame trước | THREATENING: backoff có trigger; không rematch keyframe lịch sử; 1 video 500×255, không public |
| Aktar et al. (VMZ), Robust mosaicking of maize fields | 2020, Applications in Plant Sciences (seminal) | group/mini-mosaic (≤40 frames hoặc displacement >1/3) | THREATENING: split tồn tại; trigger = heuristic, không phải confidence |
| Kharismawati & Kazic, DroneZaic | 2025, Plant Phenome Journal | shot detection (optical-flow angular change) → mini-mosaics | THREATENING: split hiện đại; trigger = motion/shot; dataset Dryad public |

**Gap sống sót:** một confidence interface hiệu chỉnh dùng chung; giữ compute/state budget cố định; so sánh reject vs rematch-keyframe-lịch-sử vs split-submosaic trên cùng sequences và metric drift/coverage/latency. Chưa có nghiên cứu head-to-head; chưa có policy chọn hành động theo loại/bản chất failure.

## Hệ quả dataset — RDR-0002

RDR-0002 (2026-09-19): dataset phải **opensource** và là **dữ liệu drone (UAV) thật**.

- Đủ điều kiện (mở + drone thật): DroneZaic Dryad (70 GB, nông nghiệp repetitive texture), NPU Drone-Map (Li 2023, 3 sequences public), UMCD (real UAV, public nhưng cần xin mật khẩu — giữ làm chính nếu xin được).
- Loại khỏi tập eval: Mid-Air (mô phỏng) và MovingDrone của OrthoTrack (photorealistic → tổng hợp) — vi phạm "drone thật".
- Chỉ dùng làm prior art, không làm eval dataset: Hwang 2026 (data on-request), Kim & Kim 2025 (không public), Yuan OJAppS 2024 (không public).
- Cần kiểm lại trước khi dùng: Aerial234 (nguồn thật + license); license từng bản Dryad/NPU Drone-Map.

## Đánh giá điều kiện dừng (RDR-0001)

- Điều kiện 1 (≥3 công trình/RQ + chuỗi nguồn + baseline/dataset/metric khả dụng): **đạt** cho RQ1–RQ3.
- Điều kiện 2 (saturation — hai vòng liên tiếp không đổi đánh giá): **chưa đạt**. Đợt 2 phát hiện công trình làm thu hẹp cả ba RQ → đánh giá đổi so với đợt 1.
- Điều kiện 3 (mỗi RQ một trạng thái): trạng thái tạm đã có (bảng dưới).
- Điều kiện 4 (ba RQ hợp lệ dùng chung harness): tạm đạt dạng bundle 3 × narrow.

| RQ | Trạng thái tạm | Lý do một dòng |
|---|---|---|
| RQ1 | narrow | so sánh chỉ báo đã có ở VPR; mới ở miền UAV + nhãn homography/drift + calibration tiền cứu |
| RQ2 | narrow | mọi adaptive đều bên trong matcher; chưa có cross-matcher routing policy với đánh giá mosaic-level |
| RQ3 | narrow | ba hành động đều tồn tại; chưa có so sánh dưới một trigger thống nhất |

## Việc còn lại trước khi khóa (đợt 3)

1. Keyword tinh chỉnh + chaining trên nhánh rủi ro: (a) thuật ngữ photogrammetry "block reliability"/registration QA/statistical testing; (b) learned matcher CPU (XFeat-class) trong UAV mosaicking; (c) shot detection/keyframe selection cho RQ3; (d) nguồn non-English (tiếng Trung, tiếng Hàn) cho aerial mosaicking.
2. Nếu đợt 3 không đổi trạng thái nào → điều kiện 2 đạt → ghi RDR-0003 khóa bộ RQ (3 × narrow + RQ4 mở).
3. Song song: kiểm tra dataset theo RDR-0002 (UMCD mật khẩu, tải NPU Drone-Map, license DroneZaic Dryad, Aerial234 nguồn thật) và chuyển experiment contract sơ bộ thành bản thành văn.

## Điểm bất định chính

- VPR→UAV là câu hỏi thực nghiệm; transfer chưa được chứng minh.
- HEB GT từ COLMAP kiểm thủ công; UDIS-D (Yuan 2024) không có GT transform.
- Li 2023 / Hwang 2026 không có drift định lượng → chưa có "drift ground truth" công khai cho video UAV dạng này; phải tự xây quy trình gắn nhãn (control points/loop).
- Bằng chứng vắng mặt là search-bounded, không phải proof of absence (patent, non-English, cửa sổ 2026 còn chạy).
- Latency giữa các paper không so sánh được (hardware/resolution khác nhau) → contract phải đo trên một stack cố định.
