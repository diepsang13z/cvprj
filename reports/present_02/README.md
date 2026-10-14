# Slide Thuyết Trình Present 2 (DAP391m)

Tài nguyên cho cột mốc **Present 2: Khảo sát đánh giá & Kết quả sơ bộ phương pháp đề xuất**.

Thư mục có **hai bản trình chiếu** phục vụ hai mục đích khác nhau.

---

## Bản A: Deck open-slide (bản chính, có presenter view)

Đường dẫn: `open_slide/`

```bash
cd open_slide
pnpm dev          # mở http://localhost:5173 → chọn slide "Failure-Aware ..."
```

- Slide nằm ở `open_slide/slides/failure-aware-mosaicking/index.tsx`: 12 trang.
- **Speaker notes**: export `notes` trong `index.tsx`, hiện ở present mode `F` cùng đồng hồ đếm.
- Sửa nội dung trực tiếp trong `index.tsx`; trình duyệt tự cập nhật (hot reload).
- Xuất PDF / PPTX / static HTML qua nút Export trong giao diện dev.
- `pnpm build` tạo bản tĩnh ở `open_slide/dist/`.

Lần đầu clone về cần `pnpm install` trong `open_slide/` (`node_modules` không được version hoá).

## Bản B: HTML độc lập (bản offline)

Đường dẫn: `index.html`

- Click đúp là mở, không cần Node, không cần mạng, không cần cài gì.
- Dùng khi máy chiếu không có sẵn toolchain, hoặc để gửi kèm cho người khác xem nhanh.
- Phím tắt: `←` `→` `Space` `PageDown` chuyển trang, `F` toàn màn hình, `Home`/`End` đầu/cuối.
- Nội dung và ảnh giống Bản A; bản này không có speaker notes.

## Ảnh thực nghiệm

Thư mục `assets/` (được cả hai bản dùng, Bản A import qua `open_slide/slides/failure-aware-mosaicking/assets/`):

| File | Nguồn | Dùng ở |
|---|---|---|
| `sample_village.jpg` | `data/phantom3-village-kfs/rgb/` | Trang 4: EDA |
| `sample_grass.jpg` | `data/phantom3-grass-kfs/rgb/` | Trang 4: EDA |
| `mosaic_loftr_broken.png` | Notebook 03, run `20261013T164937_145955Z` | Trang 5: ca vỡ bản đồ |
| `mosaic_sift.png` | Notebook 03, cùng run | Trang 5: đối chứng |
| `mosaic_superpoint.png` | Notebook 03, cùng run | Dự phòng |
| `matches_loftr.jpg` | Notebook 03, cùng run | Dự phòng |
| `summary_rq1_rq3.png` | Notebook 05 | Dự phòng |

## Cấu trúc 12 trang

| # | Trang | Barem đề cương |
|---|---|---|
| 1 | Bìa |: |
| 2 | Bài toán & 3 RQ | Introduction |
| 3 | Nghiên cứu liên quan & khoảng trống | Related works |
| 4 | Dữ liệu & EDA | Experimental (EDA) |
| 5 | Nghịch lý inlier: ca vỡ bản đồ | Experimental |
| 6 | Thước đo chain vs direct | Methodology |
| 7 | Kiến trúc 3 tầng | Methodology |
| 8 | Kết quả RQ1 | Results |
| 9 | Kết quả RQ2 + ablation | Results |
| 10 | Kết quả RQ3 + giới hạn | Results, Discussion |
| 11 | Nhật ký học kỳ & kế hoạch | Training log |
| 12 | Kết luận | Conclusion |

## Ghi chú kỹ thuật

- `open_slide/.agents/`, `open_slide/.claude/`, `AGENTS.md`, `CLAUDE.md` là scaffolding của framework,
  trùng lặp với skill đã cài toàn cục. Có thể xoá nếu muốn repo gọn hơn.
- `open_slide/slides/getting-started/` là slide mẫu của scaffolder; xoá được nếu không cần.
- Mọi số liệu trên slide lấy từ `notebooks/outputs/05_failure_aware/report.json`
  (stamp `20261014T070805_406984Z`) và `notebooks/outputs/04_drift_evaluation/drift_selfconsistent.json`.
  Các hạn chế khoa học được nêu thẳng ở trang 10 thay vì bỏ qua.
