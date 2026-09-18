# INDEX — context management

Chỉ liệt kê tài liệu context cần để định hướng quyết định và công việc. Cấu trúc dự án, báo cáo và template nằm trong `README.md`.
Cột "~Dòng" làm tròn, không cần sửa khi lệch vài dòng.

| Context file | Mục đích | Đọc khi nào | ~Dòng |
|---|---|---|---|
| `AGENTS.md` | Entry point: tổng quan dự án, quy tắc đọc tài liệu | Luôn (auto-load) | 30 |
| `RULES.md` | Ràng buộc cứng (200 dòng/file, không tự commit) | Luôn (auto-load) | 25 |
| `STATUS.md` | Ảnh chụp trạng thái: giai đoạn, RQ, tài liệu, việc tiếp theo | Cần biết đang ở đâu | 50 |
| `docs/INDEX.md` | Router này | Luôn | 30 |
| `docs/decisions/0001_stopping_point_for_literature_survey.md` | RDR-0001 (Accepted): điều kiện dừng, không chứa scope hay kế hoạch khảo sát | Cần quyết định tiếp tục, dừng hoặc mở lại khảo sát | 60 |
| `docs/decisions/0002_choise_dataset.md` | RDR-0002: dataset phải opensource và là dữ liệu drone (UAV) thật | Chọn/thay dataset cho mọi thí nghiệm | 10 |
| `docs/decisions/0003_confirm_rq_dataset.md` | RDR-0003: Chốt bộ 3 RQ cốt lõi (RQ1-3, hoãn RQ5) và dataset (NPU #1, DroneZaic dự phòng) | Xem định hướng RQs và dataset chính thức | 40 |
| `docs/logs/literature-survey/0002_novelty_audit_wave_2.md` | Đợt quét targeted novelty 2: evidence matrix, query log, chuỗi existing→gap, trạng thái tạm RQ1–RQ3 | Đánh giá keep/narrow/kill, chuẩn bị đợt quét 3 | 170 |
| `docs/logs/literature-survey/0003_novelty_audit_wave_3.md` | Đợt quét novelty 3: nhánh rủi ro, sự cố kênh, verdict saturation còn thiếu một vòng | Đánh giá điều kiện dừng RDR-0001 | 50 |
| `docs/logs/brainstorm/0001_root_project_brainstorm_log.md` | Brainstorm gốc: chọn đề tài, phạm vi MVP, dataset, chuyển sang NCKH | Truy lý do gốc của phạm vi và đề tài | 230 |
| `docs/logs/brainstorm/0002_project_picture_rq_dataset.md` | Bức tranh tổng thể để chốt: dự án, RQ tạm narrow, dataset ứng viên, 3 quyết định chờ | Chốt RQ và dataset | 110 |
| `docs/logs/literature-survey/0001_literature_survey_wave_1.md` | Khảo sát literature 2022–2026: kết luận, shortlist RQ1–RQ4, contract sơ bộ | Làm về RQ, baseline, dataset, metric | 100 |
| `docs/logs/datasets/0001_dataset_scan.md` | Quét dataset theo RDR-0002: shortlist, license, truy cập, telemetry/GT, khuyến nghị | Quyết định dataset cho thí nghiệm | 110 |
| `refs/README.md` | Danh mục 18 tài liệu tham khảo PDF toàn văn (2021–2026) theo từng RQ | Tra cứu nguồn gốc, tác giả, venue, vai trò | 60 |

## Đường đọc nhanh

- Đang ở đâu, làm gì tiếp: `STATUS.md`.
- Trạng thái tạm keep/narrow/kill và chuỗi bằng chứng: `docs/logs/literature-survey/0002_novelty_audit_wave_2.md`.
- Ràng buộc dataset (mở + drone thật): `docs/decisions/0002_choise_dataset.md`.
- Shortlist dataset và bằng chứng: `docs/logs/datasets/0001_dataset_scan.md`.
- Đã chốt gì: `docs/decisions/` — file số lớn nhất.
- Bắt tay vào RQ / baseline / metric: `docs/logs/literature-survey/0001_literature_survey_wave_1.md`.
- Điều kiện dừng của đợt novelty audit đang chạy: RDR-0001.
- Vì sao phạm vi bị giới hạn (GPS/IMU, 3D, realtime ngoài học kỳ): `docs/logs/brainstorm/0001_root_project_brainstorm_log.md` mục 8 và 10.

## Ghi chú

- `docs/logs/**` là nhật ký thô, miễn giới hạn 200 dòng; mọi file còn lại trong bảng phải ≤ 200 dòng.
- `docs/decisions/**` append-only: sửa sai bằng file mới, không sửa file cũ.
- `STATUS.md` ngược lại: ghi đè, chỉ giữ hiện tại.
- Cấu trúc log: `docs/logs/<topic>/<NNNN>_<slug>.md` (<topic>: kebab-case; <NNNN>: 4 số tăng dần theo topic; <slug>: snake_case).
