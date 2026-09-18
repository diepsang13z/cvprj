# STATUS — trạng thái hiện tại

Ảnh chụp, **không phải nhật ký**. Trạng thái đổi → ghi đè file này.
Lịch sử và lý do gốc nằm ở `docs/decisions/` và `docs/logs/`, không chép lại vào đây.

Cập nhật lần cuối: 2026-09-19

## Giai đoạn

Đã xong đợt quét targeted novelty thứ hai cho ba cụm RQ. Evidence matrix, query log và chuỗi existing→gap nằm ở `docs/logs/literature-survey/0002_novelty_audit_wave_2.md`. Ba RQ cốt lõi có trạng thái tạm **narrow**; chưa đạt information saturation (RDR-0001 điều kiện 2) vì đợt 2 phát hiện công trình làm thu hẹp cả ba RQ. Đã quét xong dataset theo RDR-0002; shortlist và bằng chứng tại `docs/logs/datasets/0001_dataset_scan.md` — đang chờ team quyết định dataset. Chưa có mã nguồn, chưa có experiment contract thành văn.

## Hướng nghiên cứu

*Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking* — chưa khóa; chỉ khóa khi đạt đủ điều kiện RDR-0001. Công thức từng RQ đã thu hẹp sau đợt 2.

| RQ | Câu hỏi | Trạng thái tạm |
|---|---|---|
| RQ1 | Chỉ báo rẻ nào ở cấp cặp-frame dự báo được lỗi đăng ký và drift tích luỹ của mosaic? | narrow — giữ benchmark/calibration chỉ báo ở miền UAV + liên kết pairwise→drift; so sánh chỉ báo ở VPR đã có (Zaffar 2024, Sferrazza 2025) |
| RQ2 | Chính sách hai tầng classical mặc định, learned matcher khi rủi ro cao có tốt hơn always-X? | narrow — chỉ policy cross-matcher routing + quality/latency mức mosaic; adaptive bên trong matcher đã có (LightGlue 2023, CasP 2025) |
| RQ3 | Hành động phục hồi nào (loại frame / rematch keyframe / tách submosaic) giới hạn drift tốt nhất? | narrow — so sánh có kiểm soát dưới một confidence trigger; từng hành động đã tồn tại (Hwang 2026, Li 2023, DroneZaic 2025) |
| RQ4 | GPS/yaw nhiễu và dropout ở mức nào còn giúp, từ khi nào có hại? | mở — không đổi; chỉ kích hoạt nếu ba cụm cốt lõi bị kill |

## Đã chốt chính thức

- **RDR-0001 (Accepted, 2026-09-18)** — điều kiện dừng khảo sát literature: đủ bằng chứng/RQ, hai vòng liên tiếp không đổi đánh giá, mỗi RQ một trạng thái keep/narrow/kill, và có ba RQ hợp lệ dùng chung harness (hoặc ghi nhận pivot).
- **RDR-0002 (2026-09-19)** — dataset cho mọi thí nghiệm phải opensource và là dữ liệu từ drone (UAV) thật. File: `docs/decisions/0002_choise_dataset.md`.

## Chốt tạm (chỉ nằm trong log)

- Hình thức: NCKH + 1 MVP demo, dùng chung một codebase (pipeline = demo, eval harness = số liệu).
- Dataset theo RDR-0002 (mở + drone thật): đang chờ team quyết định — shortlist và bằng chứng tại `docs/logs/datasets/0001_dataset_scan.md`. Ứng viên: NPU Drone-Map (video + .SRT + GPS + GCP), DroneZaic Dryad (nông nghiệp repetitive), Aerial234 (cc-by-4.0), WHU Aerial Video (RTK + GCP + GT pose), UMCD (mosaicking-specific, cần mật khẩu). Mid-Air và MovingDrone đã loại vì mô phỏng. Video nhóm tự quay chỉ dùng external validation.
- MVP: video ngắn gần nadir, cảnh phẳng, 15–30 frame chồng lấn → một aerial mosaic.
- Trạng thái tạm đợt 2 (2026-09-19): RQ1–RQ3 đều `narrow`; RQ4 mở.

## Tài liệu

| Hạng mục | Trạng thái |
|---|---|
| Brainstorm gốc | có |
| Khảo sát literature đợt 1 | có |
| RDR-0001 | Accepted |
| RDR-0002 (dataset mở + drone thật) | có |
| Evidence matrix + query/citation log (đợt 2) | có — `docs/logs/literature-survey/0002_novelty_audit_wave_2.md` |
| Quét dataset theo RDR-0002 | có — `docs/logs/datasets/0001_dataset_scan.md` |
| Experiment contract (baseline, dataset, metric) | chưa — cần khi khóa RQ |
| README, `refs/` | chưa có gì |

## Việc tiếp theo

1. Team quyết định dataset từ shortlist trong `docs/logs/datasets/0001_dataset_scan.md` (kèm quyết định về cách đọc "opensource": license chuẩn hay chỉ cần tải được) → ghi RDR-0003.
2. Chạy đợt quét novelty 3 theo các nhánh rủi ro đã liệt kê trong log đợt 2 (photogrammetric block reliability, learned matcher CPU trong UAV mosaicking, shot detection/keyframe selection, nguồn non-English).
3. Nếu đợt 3 không đổi đánh giá → đạt saturation → ghi RDR-0004 khóa bộ RQ (3 × narrow + RQ4 mở).
4. Khóa xong RQ + dataset → chuyển experiment contract sơ bộ thành bản thành văn.
