# STATUS — trạng thái hiện tại

Ảnh chụp, **không phải nhật ký**. Trạng thái đổi → ghi đè file này.
Lịch sử và lý do gốc nằm ở `docs/decisions/` và `docs/logs/`, không chép lại vào đây.

Cập nhật lần cuối: 2026-09-18

## Giai đoạn

Đang chạy targeted novelty audit cho ba cụm RQ (theo RDR-0001). Chưa có mã nguồn, chưa có experiment contract thành văn.

## Hướng nghiên cứu

*Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking* — chưa khóa; chỉ khóa khi có ba RQ `keep`/`narrow`.

| RQ | Câu hỏi | Trạng thái |
|---|---|---|
| RQ1 | Chỉ báo rẻ nào ở cấp cặp-frame dự báo được lỗi đăng ký về sau và drift tích luỹ của mosaic? | shortlist — chờ audit |
| RQ2 | Chính sách hai tầng (classical mặc định, gọi learned matcher khi rủi ro cao) có trade-off chất lượng–độ trễ tốt hơn always-classical và always-learned? | shortlist — chờ audit |
| RQ3 | Khi đăng ký vẫn không đáng tin, hành động phục hồi nào (loại frame / rematch keyframe trước / tách submosaic) giới hạn drift tốt nhất mà không cần SLAM hay bundle adjustment? | shortlist — chờ audit |
| RQ4 | Ở mức nhiễu và dropout GPS/yaw nào thì telemetry tối thiểu còn cải thiện pipeline, và từ khi nào thành có hại? | mở — chỉ kích hoạt nếu cả ba cụm cốt lõi bị `kill` hoặc metadata công khai đủ tốt |

Nguồn: `docs/logs/literature-survey/0001_literature_survey_wave_1.md`.

## Đã chốt chính thức

- **RDR-0001 (Accepted, 2026-09-18)** — Điểm dừng khảo sát literature:
  - Mỗi RQ có ít nhất ba công trình gần nhất, novelty chain có nguồn, baseline, dataset và metric khả dụng.
  - Hai vòng tìm kiếm liên tiếp không có công trình mới làm đổi trạng thái `keep`/`narrow`/`kill`.
  - Đóng khảo sát khi có ba RQ hợp lệ dùng chung harness, hoặc ghi nhận cần pivot nếu saturation còn ít hơn ba.

Chưa có RDR nào khác.

## Chốt tạm (chỉ nằm trong log)

- Hình thức: NCKH + 1 MVP demo, dùng chung một codebase (pipeline = demo, eval harness = số liệu).
- Dataset chính UMCD; dự phòng DroneZaic; Mid-Air và Aerial234 để kiểm thử; video nhóm tự quay chỉ dùng external validation.
- MVP: một video ngắn gần nadir, cảnh phẳng, 15–30 frame chồng lấn → một aerial mosaic.

## Tài liệu

| Hạng mục | Trạng thái |
|---|---|
| Brainstorm gốc | có |
| Khảo sát literature đợt 1 | có |
| RDR-0001 | Accepted |
| Evidence matrix + query/citation log của audit | chưa — cần để đánh giá điều kiện dừng |
| Experiment contract (baseline, dataset, metric) | chưa |
| README, `refs/` | chưa có gì |

## Việc tiếp theo

1. Chạy targeted novelty audit ba cụm, ghi evidence matrix và query log.
2. Quyết định `keep`/`narrow`/`kill` cho từng RQ; nếu còn dưới ba RQ hợp lệ thì ghi RDR pivot.
3. Chốt RQ và chuyển experiment contract sơ bộ thành bản thành văn.
