# Documentation Router (docs/INDEX.md)

Router đơn điều hướng toàn bộ tài liệu context. Mọi Agent bắt đầu tra cứu từ file này.

---

## 1. Core Context Files (Cấp file)

- [`README.md`](../README.md) — Điểm vào cho người đọc: đề tài, kiến trúc repo, cấu trúc thư mục.
- [`RULES.md`](../RULES.md) — Quy tắc vận hành: ngân sách 200 dòng, kỷ luật Git, Single Source of Truth, quy ước đặt tên, luật nhật ký.
- [`AGENTS.md`](../AGENTS.md) — Định vị đề tài, phạm vi in/out-scope, protocol đọc 5 bước, dataset.
- [GitHub Issues](https://github.com/diepsang13z/cvprj/issues) — Việc đang mở, người phụ trách, blocker; không chép danh sách việc vào repo.
- [`refs/INDEX.md`](../refs/INDEX.md) — Danh mục tài liệu tham khảo và thư viện bài báo.

## 2. Decisions (Cấp file)

Thư mục `docs/decisions/` hoạt động append-only (`RDR-NNNN`). Đọc theo chủ đề; quyết định mới chỉ thay quyết định cũ khi ghi rõ phạm vi thay thế.

- [`RDR-0001_stopping_point_for_literature_survey.md`](decisions/RDR-0001_stopping_point_for_literature_survey.md) — Điều kiện dừng khảo sát literature.
- [`RDR-0002_choise_dataset.md`](decisions/RDR-0002_choise_dataset.md) — Dataset phải opensource và là dữ liệu từ drone (UAV) thật.
- [`RDR-0003_confirm_rq_dataset.md`](decisions/RDR-0003_confirm_rq_dataset.md) — Chốt 3 RQ cốt lõi và dataset (NPU Drone-Map ưu tiên 1, DroneZaic dự phòng).
- [`RDR-0004_lecturer_review_after_persen_proposal.md`](decisions/RDR-0004_lecturer_review_after_persen_proposal.md) — Giảm scope SV năm 2: dùng model có sẵn, sample ~10 GB, chạy Colab/Kaggle.
- [`RDR-0005_finalize_npu_dronemap_dataset.md`](decisions/RDR-0005_finalize_npu_dronemap_dataset.md) — Chốt NPU Drone-Map là dataset duy nhất (loại bỏ DroneZaic do đã cũ).
- [`RDR-0006_shortlist_models_for_experimentation.md`](decisions/RDR-0006_shortlist_models_for_experimentation.md) — Chốt danh sách cấu hình và mô hình (SIFT/ORB, SIFT/SP+LightGlue, XFeat, Efficient LoFTR) đưa vào chạy thử nghiệm.

## 3. Logs & Working Notes (Cấp thư mục)

Khu vực ghi nhật ký tiến trình, khảo sát văn hiến và brainstorm (không áp dụng giới hạn 200 dòng):

- [`notes/glossary.md`](../notes/glossary.md) — Từ điển thuật ngữ thị giác máy tính, xử lý ảnh UAV và khái niệm 3 RQ.
- [`notes/project_overview.md`](../notes/project_overview.md) — Bức tranh toàn cảnh dự án: bài toán, nguồn lực, RQ và kế hoạch triển khai.
- [`notes/datasets.md`](../notes/datasets.md) — Dataset của dự án: 14 gói NPU Drone-Map, nội dung ảnh/metadata, thứ tự tải trong ngân sách 10 GB; phân loại toàn bộ mục còn lại trên adv-ci và lý do không dùng.
- [`notes/orb_sift.md`](../notes/orb_sift.md) — Cơ chế hoạt động và so sánh trực diện hai thuật toán đặc trưng cổ điển (SIFT và ORB).
- [`notes/models.md`](../notes/models.md) — Danh sách các mô hình và cấu hình chạy thử nghiệm (SIFT/ORB, LightGlue, XFeat, Efficient LoFTR), vai trò trong RQ2 và lưu ý kỹ thuật.
- [`notes/notebook_01_classical_baseline.md`](../notes/notebook_01_classical_baseline.md) — Hướng dẫn dễ hiểu cho sinh viên về Notebook 01: Quy trình ghép ảnh cổ điển bằng SIFT và ORB.
- [`notes/notebook_02_lightglue_pilot.md`](../notes/notebook_02_lightglue_pilot.md) — Hướng dẫn dễ hiểu cho sinh viên về Notebook 02: Dùng AI LightGlue ghép ảnh ở độ phân giải gốc 1080p.
- [`notes/notebook_03_all_models.md`](../notes/notebook_03_all_models.md) — Hướng dẫn dễ hiểu cho sinh viên về Notebook 03: Đấu trường 7 mô hình và phát hiện ca vỡ bản đồ thực tế của EfficientLoFTR.
- [`notes/detector_matcher.md`](../notes/detector_matcher.md) — Giải thích khái niệm Detector, Matcher và vai trò trung tâm trong 3 RQ của nghiên cứu Failure-Aware Mosaicking.
- [`docs/logs/progress/`](logs/progress/) — Nhật ký tiến độ theo người: mỗi người một file theo ngày, append-only.
  - [`2026_09_20_diepsang13z.md`](logs/progress/2026_09_20_diepsang13z.md) — Đóng proposal, giảm scope, việc tiếp theo (baseline pipeline).
- [`docs/logs/literature-survey/`](logs/literature-survey/) — Nhật ký quét novelty (Wave 1–3) và query logs.
- [`docs/logs/datasets/`](logs/datasets/) — Quét và phân tích dataset UAV mở.
  - [`0001_dataset_scan.md`](logs/datasets/0001_dataset_scan.md) — Shortlist dataset ứng viên theo tiêu chí `RDR-0002`.
  - [`0002_npu_dronemap_intro.md`](logs/datasets/0002_npu_dronemap_intro.md) — Hồ sơ dataset đã chốt (NPU Drone-Map): xuất xứ, nội dung, metadata, giới hạn.
- [`docs/logs/brainstorm/`](logs/brainstorm/) — Brainstorm gốc: chọn đề tài, hình dung RQ và dataset.

## 4. Reports & Deliverables (Cấp thư mục)

- `reports/md/` — Bản markdown (thuyết minh đề cương).
- `reports/templates/` — Mẫu và hướng dẫn học phần.
- `notebooks/` — Thực nghiệm ghép ảnh: `01_classical_baseline.ipynb` (Classical Baseline ORB/SIFT, tích lũy Homography, log metric).
- [`02_lightglue_pilot.ipynb`](../notebooks/02_lightglue_pilot.ipynb) — Pilot pretrained SIFT/SuperPoint + LightGlue; cài `requirements_learned.txt`, chọn kernel `.venv`, Run All. Đã kiểm tra CPU trên 3 cặp village mỗi cấu hình; chưa đánh giá drift/routing.
- [`03_all_models.ipynb`](../notebooks/03_all_models.ipynb) — Chạy đủ 7 cấu hình RDR-0006 trên cùng cặp-frame; tự chứa toàn bộ code (adapter, pipeline, báo cáo, kiểm tra), không cần `.py`. Mở `notebooks/outputs/index.html` để vào kết quả.
---

## Đường đọc nhanh

- Đang ở đâu, làm gì tiếp: [`docs/logs/progress/2026_09_20_diepsang13z.md`](logs/progress/2026_09_20_diepsang13z.md) (hoặc Issues).
- Đã chốt gì: `docs/decisions/` — file số lớn nhất là mới nhất.
- Hướng nghiên cứu & RQs: [`RDR-0003_confirm_rq_dataset.md`](decisions/RDR-0003_confirm_rq_dataset.md).
- Dataset đã chốt: [`RDR-0005_finalize_npu_dronemap_dataset.md`](decisions/RDR-0005_finalize_npu_dronemap_dataset.md) (NPU Drone-Map là dataset duy nhất).
- Điều kiện dừng novelty audit: [`RDR-0001_stopping_point_for_literature_survey.md`](decisions/RDR-0001_stopping_point_for_literature_survey.md).
- Vì sao phạm vi bị giới hạn: [`RDR-0004_lecturer_review_after_persen_proposal.md`](decisions/RDR-0004_lecturer_review_after_persen_proposal.md).
- Trạng thái keep/narrow/kill và chuỗi bằng chứng: `docs/logs/literature-survey/0002_novelty_audit_wave_2.md`.

## Ghi chú

- `docs/logs/**` là nhật ký thô, miễn giới hạn 200 dòng; mọi file còn lại trong router phải ≤ 200 dòng.
- `docs/decisions/**` append-only: sửa sai bằng file mới, không sửa file cũ.
- Cấu trúc log: `docs/logs/<chủ-đề>/<NNNN>_<slug>.md` (chủ đề snake_case cho file mới; `<NNNN>` 4 số tăng dần theo chủ đề).
