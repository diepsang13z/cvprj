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
- [`RDR-0007_drift_metric_choice.md`](decisions/RDR-0007_drift_metric_choice.md) — Chốt metric đo drift là **chain vs direct** (tự nhất quán, đơn vị pixel), không phụ thuộc `trajectory.txt`; kèm ngưỡng hợp lệ 100 inlier và mức nền của matcher tham chiếu.
- [`RDR-0008_step_level_metric_and_risk_trigger.md`](decisions/RDR-0008_step_level_metric_and_risk_trigger.md) — **Proposed**: thước đo sai số **cấp bước** (mở rộng `RDR-0007`), 4 chỉ báo rủi ro chính thức, ngưỡng kích hoạt τ_ncc = 0,93 theo ngân sách leo thang 25%, chiến lược phục hồi mặc định là tách submosaic.
- [`RDR-0009_reference_list_scope.md`](decisions/RDR-0009_reference_list_scope.md) — Không áp đặt hạn mức cứng $\ge 30$ tài liệu tham khảo; ưu tiên trích dẫn thực chất, tinh gọn 15–22 bài nòng cốt đã đọc và phân loại trong `refs/INDEX.md`.
- [`RDR-0010_presentation_feedback_actions.md`](decisions/RDR-0010_presentation_feedback_actions.md) — Tiếp thu góp ý sau buổi thuyết trình: cấm chạy CPU máy cá nhân (chuyển 100% sang Colab/Kaggle + lưu log), làm lại Related Work chi tiết (hiện trạng / thiếu sót / chứng minh ưu việt), chuẩn hóa format paper & ref theo chuẩn IEEE qua Google Scholar, vẽ baseline vào paper, bổ sung phần phương pháp đo lường (metrics).

## 3. Logs & Working Notes (Cấp thư mục)

Khu vực ghi nhật ký tiến trình, khảo sát văn hiến và brainstorm (không áp dụng giới hạn 200 dòng):

- [`notes/glossary.md`](../notes/glossary.md) — Từ điển thuật ngữ thị giác máy tính, xử lý ảnh UAV và khái niệm 3 RQ.
- [`notes/project_overview.md`](../notes/project_overview.md) — Bức tranh toàn cảnh dự án: bài toán, nguồn lực, RQ và kế hoạch triển khai.
- [`notes/datasets.md`](../notes/datasets.md) — Dataset của dự án: 14 gói NPU Drone-Map, nội dung ảnh/metadata, thứ tự tải trong ngân sách 10 GB; phân loại toàn bộ mục còn lại trên adv-ci và lý do không dùng.
- [`notes/orb_sift.md`](../notes/orb_sift.md) — Cơ chế hoạt động và so sánh trực diện hai thuật toán đặc trưng cổ điển (SIFT và ORB).
- [`notes/models.md`](../notes/models.md) — Danh sách các mô hình và cấu hình chạy thử nghiệm (SIFT/ORB, LightGlue, XFeat, Efficient LoFTR), vai trò trong RQ2 và lưu ý kỹ thuật.
- [`notes/notebook_01_classical_baseline.md`](../notes/notebook_01_classical_baseline.md) — Giải thích và audit baseline SIFT/ORB: luồng ghép, timing, lỗi RMSE bằng 0 khi không có phép đo, thiếu provenance.
- [`notes/notebook_02_lightglue_pilot.md`](../notes/notebook_02_lightglue_pilot.md) — Giải thích và audit LightGlue: 3 cặp và mosaic 20 frame ảnh gốc; giới hạn timing, độ phủ canvas và kết luận tài nguyên.
- [`notes/notebook_03_all_models.md`](../notes/notebook_03_all_models.md) — Giải thích và audit pilot 7 cấu hình: run/manifest/hash, kết quả canvas, giới hạn adapter và benchmark.
- [`notes/notebook_04_drift_evaluation.md`](../notes/notebook_04_drift_evaluation.md) — Giải thích và audit pose + chain-vs-direct: không phải ground truth độc lập, thang đo chưa được ảnh tự xác nhận, đoạn đo `village` tới frame 19 / `grass` tới frame 6.
- [`notes/notebook_05_failure_aware_pipeline.md`](../notes/notebook_05_failure_aware_pipeline.md) — Giải thích và audit RQ1/RQ2/RQ3 (mục 9: đính chính sau khi sửa lỗi tính toán và chạy lại toàn notebook): gate tham chiếu 100 inlier đã áp thật, AUC một chiều khai báo trước, drift kiểm bằng replay; còn lại: assertion nghiên cứu, ngân sách τ khi không ngưỡng nào hợp lệ, latency chỉ tính matcher.
- [`notes/detector_matcher.md`](../notes/detector_matcher.md) — Giải thích khái niệm Detector, Matcher và vai trò trung tâm trong 3 RQ của nghiên cứu Failure-Aware Mosaicking.
- [`notes/related_work_analysis.md`](../notes/related_work_analysis.md) — Phân tích chuyên sâu các công trình liên quan: công nghệ sử dụng, thiếu sót (research gaps) và luận điểm/bằng chứng chứng minh giải pháp của nhóm vượt trội theo 4 mảng (Ghép ảnh tích luỹ, RQ1, RQ2, RQ3).
- [`docs/logs/progress/`](logs/progress/) — Nhật ký tiến độ theo người: mỗi người một file theo ngày, append-only.
  - [`2026_09_20_diepsang13z.md`](logs/progress/2026_09_20_diepsang13z.md) — Đóng proposal, giảm scope, việc tiếp theo (baseline pipeline).
  - [`2026_10_14_diepsang13z.md`](logs/progress/2026_10_14_diepsang13z.md) — Quét 160 bước chọn cửa sổ có lỗi thật, viết Notebook 05 (RQ1/RQ2/RQ3), đề xuất `RDR-0008`, sửa lỗi tính toán và chạy lại Notebook 05.
  - [`2026_10_15_diepsang13z.md`](logs/progress/2026_10_15_diepsang13z.md) — Cập nhật paper; bổ sung tách notebook theo model/RQ, bàn giao artifact và quy định chỉ chạy trên cloud; ghi rõ kiểm tra tĩnh và giới hạn chưa chạy cloud.
- [`docs/logs/literature-survey/`](logs/literature-survey/) — Nhật ký quét novelty (Wave 1–3) và query logs.
- [`docs/logs/experiments/`](logs/experiments/) — Nhật ký thực nghiệm dài (quét trước khi thiết kế thí nghiệm).
  - [`0001_failure_scan_windows.md`](logs/experiments/0001_failure_scan_windows.md) — Nhật ký quét 160 bước × 2 sequence và chọn cửa sổ `village` 80–125 / `grass` 0–45. Đọc kèm audit 05: ghép đủ frame không chứng minh không có lỗi hình học.
- [`docs/logs/datasets/`](logs/datasets/) — Quét và phân tích dataset UAV mở.
  - [`0001_dataset_scan.md`](logs/datasets/0001_dataset_scan.md) — Shortlist dataset ứng viên theo tiêu chí `RDR-0002`.
  - [`0002_npu_dronemap_intro.md`](logs/datasets/0002_npu_dronemap_intro.md) — Hồ sơ dataset đã chốt (NPU Drone-Map): xuất xứ, nội dung, metadata, giới hạn.
  - [`0003_trajectory_pose_verification.md`](logs/datasets/0003_trajectory_pose_verification.md) — Kiểm chứng quy ước `trajectory.txt`/`Plane=` + mã nguồn tác giả: quaternion theo thứ tự (x, y, z, w); sau khi sửa, cầu nối `village` đạt residual 0,88 px (cả chuỗi 1 → 21 px ≈ 3 m) và `grass` vẫn suy biến. Có mục ĐÍNH CHÍNH các kết luận sai ban đầu.
- [`docs/logs/brainstorm/`](logs/brainstorm/) — Brainstorm gốc: chọn đề tài, hình dung RQ và dataset.

## 4. Reports & Deliverables (Cấp thư mục)

- `reports/md/` — Bản markdown (thuyết minh đề cương).
- `reports/templates/` — Mẫu và hướng dẫn học phần.
- [`reports/paper/`](../reports/paper/) — **Bản nháp bài báo IEEE**, hai bản cùng số liệu: `main.tex` → `main.pdf` (tiếng Anh) và `main_vi.tex` → `main_vi.pdf` (tiếng Việt, cần font Times New Roman). `make_figures.py` và `make_mosaics.py` đọc artifact lịch sử; không tự chuyển sang run cloud mới. `check_tables.py` đối chiếu bảng với `report.json`, đọc `INDICATOR_SUSPICION` từ `notebooks/shared/failure_core.py` bằng text (không import model), và chặn em dash. `RDR-0008` còn Proposed; đọc kèm Limitations.
  - [`reports/paper/presentation_script.md`](../reports/paper/presentation_script.md) — Kịch bản thuyết trình paper 3–5 phút cho nhóm báo cáo với GVHD kèm bảng tra cứu số liệu nhanh.
- [`reports/present_02/`](../reports/present_02/) — Slide Present 2, hai bản: `open_slide/` (deck open-slide 12 trang, có speaker notes + export PDF/PPTX, chạy `pnpm dev`) và `index.html` (bản offline mở bằng trình duyệt). Chi tiết ở `README.md` trong thư mục.
- [`notebooks/README.md`](../notebooks/README.md) — Điểm vào thực nghiệm: notebook riêng theo model/RQ, thứ tự phụ thuộc, phân công và hợp đồng bàn giao. **Chỉ chạy Colab/Kaggle hosted runtime**, theo `RULES.md` §8.
- [`notebooks/classical/`](../notebooks/classical/) và [`notebooks/lightglue/`](../notebooks/lightglue/) — Pilot ảnh gốc tách SIFT/ORB và từng extractor LightGlue; không trộn với benchmark 640 px.
- [`notebooks/models/`](../notebooks/models/) — Bảy notebook 640 px, một cấu hình mỗi notebook; độc lập output và log.
- [`notebooks/drift/`](../notebooks/drift/) — Một job trajectory và bảy job chain-vs-direct, nhận đường dẫn run model cụ thể.
- [`notebooks/research/`](../notebooks/research/) — Ba scan theo matcher → RQ1/RQ2 → bốn recovery độc lập → tổng hợp report. Các notebook 01–05 cũ chỉ còn mục lục; output lịch sử không thay đổi.

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
