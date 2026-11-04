# Paper v2 — empirical failure-aware UAV mosaicking

## Nội dung

- `main.tex` / `main.pdf`: bản nghiên cứu tiếng Anh.
- `main_vi.tex` / `main_vi.pdf`: bản tiếng Việt cùng số liệu để nhóm rà soát; không phải template IEEE tiếng Việt được chứng nhận riêng.
- `related_work.tex`, `related_work_vi.tex`: tổng hợp nghiên cứu liên quan có nguồn.
- `references.bib`: cơ sở BibTeX dùng chung; `reference_audit.md`: URL kiểm chứng và giới hạn truy cập Google Scholar.
- `make_assets.py`: đọc artifact cloud và sinh bảng/hình, không chạy matching, RANSAC hoặc warp mosaic.
- `tables/`: bảng số liệu LaTeX dùng chung hai bản; `figures/`: sơ đồ baseline và mosaic baseline đã lưu.

## Template chính thức

Nguồn: [IEEE Manuscript Templates for Conference Proceedings](https://www.ieee.org/conferences/publishing/templates), truy cập 2026-11-04. Trang IEEE yêu cầu LaTeX ở chế độ `conference`; gói template ghi Updated 2024.

- Đã tải nguyên gói `conference-latex-template.zip` từ link trên trang IEEE, lưu `ieee_template.zip`.
- `IEEEtran.cls` được trích nguyên byte từ `IEEE-conference-template-062824/IEEEtran.cls`.
- SHA-256 ZIP: `516252d9ac6e974af3a1d9aa72f97ecc462b9a47556225019fb0adef69bba78a`.
- SHA-256 class: `c972aca108fda004c3514d63658e02816da2e54d9a1451e870b9bd970e003f55`.
- Bibliography dùng `IEEEtran.bst` nguyên bản từ gói **LaTeX Bibliography Files** trên cùng trang IEEE; SHA-256 `d83aa3c9b47fc120bb3d9d8e476216cb889c738f72ec950beeac3661c45ded24`. Đánh số theo thứ tự trích dẫn, không tự viết số Ref bằng tay.
- Chưa chọn conference/journal cụ thể. Không có một template IEEE “chuẩn nhất” cho mọi venue; cần dùng hướng dẫn venue trước khi nộp. Không tự thêm copyright, mã hội nghị, email hay funding.

## Tái tạo từ repository root

```powershell
python reports/paper/v2/make_assets.py
tectonic --keep-logs reports/paper/v2/main.tex
tectonic --keep-logs reports/paper/v2/main_vi.tex
python reports/paper/v2/check_paper.py
```

Python dùng `matplotlib` và `Pillow`; Tectonic dùng XeTeX/BibTeX và có thể tải bundle TeX khi thiếu. Cả hai bản cần Times New Roman/Courier New trên hệ thống. Đây là sinh tài liệu từ kết quả đã lưu, không phải chạy thực nghiệm local. PDF nằm cạnh file TeX.

## Nguồn dữ liệu cố định

Các đường dẫn dưới đây tương đối với `notebooks/outputs/`:

| Nhóm | Run |
|---|---|
| Baseline native-resolution | `classical_mosaicking_baseline/20261101T153341_784110Z` |
| Deep native-resolution | `deep_matching_pilot/20261101T161621_999565Z` |
| Benchmark | `feature_matcher_benchmark/20261101T163603_779942Z` |
| Chain-vs-direct | `accumulated_drift_evaluation/20261103T165349_596427Z` |
| RQ1–RQ3 / LOSO | `failure_aware_pipeline/20261101T183829_171190Z` |

Chi tiết mẫu số, phép tổng hợp và giới hạn: [tổng hợp kết quả](../../../docs/explain/experimental_results_synthesis.md).

- `summary.csv`: pair-success count, match time trung bình mọi cặp, RMSE trung bình cặp success.
- `mosaic_summary.csv`: frame giữ, mẫu số 3.898 ảnh; không lấy mẫu số đã bị cắt trong artifact drift.
- `drift_selfconsistent.json`: macro mean `common_ate_px` trên 8 sequence, cùng 138 frame common.
- `report.json`: macro indicator/step-error theo sequence, pooled cost/escalation và recovery accounting. Không trộn số liệu pilot.
- Benchmark và pipeline lệch một bản ảnh trùng centralPark; paper công bố sai khác, không sửa artifact.

## Lưu trữ v1

21 file cũ đã chuyển vào `../v1/`, SHA-256 trước/sau giống nhau. V1 giữ cả Ref và kết luận lịch sử, không phải nguồn đã kiểm chứng. Các script v1 giữ nguyên đường dẫn cũ để bảo toàn snapshot, không dùng chúng để tái tạo v2. Nhật ký cũ giữ nguyên theo quy định append-only.

## Giới hạn

Bản thảo báo kết quả khám phá, không khẳng định ưu thế tổng quát hay độ chính xác trắc địa. RQ2 và RQ3 là thí nghiệm thành phần tách biệt; thời gian cộng gộp không phải end-to-end. Không có kiểm định thống kê nhiều seed hoặc chứng nhận PDF eXpress/venue-specific. Không coi kiểm tra citation nội bộ là bảo đảm tuyệt đối không sai; đối chiếu tác giả lần cuối trước khi nộp.
