# UAV video 2D aerial mosaicking

Dự án xây dựng mosaic ảnh 2D từ video UAV bằng pipeline đặc trưng cổ điển (ORB/SIFT → matching → RANSAC/homography → warp/blend). Kết quả là ảnh hiện trạng cục bộ, không phải bản đồ georeference.

Môn AI2002 — nhóm 09.

## Bắt đầu từ đâu

| Bạn là | Đọc theo thứ tự |
| --- | --- |
| **Agent** | [`AGENTS.md`](AGENTS.md) — tự nạp, chứa protocol đọc 5 bước |
| **Người mới vào dự án** | [`docs/INDEX.md`](docs/INDEX.md) → [`RULES.md`](RULES.md) → RDR liên quan trong `docs/decisions/` |
| **Chỉ muốn biết đề tài** | Mục dưới + [`docs/decisions/RDR-0003_confirm_rq_dataset.md`](docs/decisions/RDR-0003_confirm_rq_dataset.md) |
| **Thuật ngữ** | [`notes/glossary.md`](notes/glossary.md) |
| **Tra cứu văn hiến** | [`refs/INDEX.md`](refs/INDEX.md) |

## Kiến trúc repository

| Tầng | Thư mục chính | Trách nhiệm |
| --- | --- | --- |
| **1. Project Governance** | `README.md`, `AGENTS.md`, `RULES.md`, `docs/INDEX.md` | Quy tắc vận hành, protocol Agent, kỷ luật Git, router tài liệu |
| **2. Research Theory & Notes** | `notes/` | Thuật ngữ, ghi chú lý thuyết |
| **3. Literature Reference** | `refs/` | Thư viện 18 bài báo toàn văn (PDF), danh mục ở `refs/INDEX.md` |
| **4. Research Records** | `docs/decisions/`, `docs/logs/` | Quyết định `RDR-NNNN` append-only và nhật ký tiến độ |
| **5. Deliverables** | `reports/`, `templates/` | Đề cương (Word/PDF/slide) và mẫu môn học |

## Cấu trúc thư mục

| Thư mục | Nội dung |
| --- | --- |
| `docs/` | Router (`INDEX.md`), quyết định (`decisions/`), nhật ký (`logs/`) |
| `notes/` | Thuật ngữ dự án (`glossary.md`) |
| `refs/` | Thư viện PDF tham khảo, danh mục ở `refs/INDEX.md` |
| `reports/` | Deliverables: `proposal/` (Word/PDF/slide), `md/` (bản markdown) |
| `templates/` | Mẫu Word gốc của đề cương |
| `data/` | Sample frame thử nghiệm (không hardcode vào code) |
