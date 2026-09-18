# Đợt quét 3 — novelty audit (2026-09-19)

**Mục đích:** kiểm điều kiện saturation của RDR-0001 (điều kiện 2: hai vòng tìm kiếm liên tiếp không làm đổi đánh giá RQ). **Nhánh rủi ro đã chốt:** photogrammetry QA / block reliability (RQ1), learned matcher CPU trong UAV mosaicking (RQ2), shot detection / keyframe selection (RQ3), nguồn non-English.

## Kênh tra cứu và sự cố (ghi thật để tái lập)

- **web_search:** 3/4 truy vấn lỗi 429 đồng loạt mọi provider (parallel MCP rate limit, codex usage_limit, google/mojeek/ecosia/duckduckgo chặn bot). 1 truy vấn thành công ("shot detection" aerial mosaic) — kết quả toàn paper đã biết (radiometric calibration, seamline, SIFT+LightGlue, IMU stitching).
- **Semantic Scholar API:** 1/8 truy vấn thành công (photogrammetry reliability — chỉ kết quả cũ/đã biết: optical-flow dense matching UAV 2024, line-feature fusion triangulation 2024, survey 2022, 1993–2018); 7 truy vấn còn lại 429 kể cả khi backoff 9 giây.
- **arXiv API (http và https):** trả 0 entry cho mọi truy vấn, kể cả `all:submosaic` → coi như kênh hỏng tại thời điểm chạy.
- **Crossref query:** hoạt động bình thường — dùng làm kênh chính (6 truy vấn quét nhánh rủi ro).

## Kết quả đối chiếu — không công trình nào đổi trạng thái RQ

- **RQ2:** AAPMatcher (Neural Networks 2025 — adaptive attention pruning, adaptive *bên trong* một learned matcher, cùng họ LightGlue/CasP); Ada-Matcher (Knowledge-Based Systems 2025 — adaptive weight sharing, nội bộ); CHAMELEON-SLAM (TechRxiv 2026 preprint — uncertainty-aware matching + adaptive feature selection trong SLAM, không phải classical-first → learned-fallback cho mosaicking). Không cái nào là routing cross-matcher classical→learned có đánh giá mosaic-level.
- **RQ1:** Image Matching by Bare Homography (IEEE TIP 2024 — phương pháp matcher dựa homography, không dự báo lỗi/drift); "Solving photogrammetric cold cases using AI-based image matching" (ISPRS JPRS 2023 — khớp ảnh lưu trữ lịch sử, không phải QA/dự báo); STN-Homography (2019), adaptive homography transform (CCC 2021) — cũ/khác mục tiêu. Không thấy nghiên cứu chỉ báo rẻ → drift tiền cứu nào mới ở miền UAV.
- **RQ3:** MaiZaic preprint (2024) = tiền thân DroneZaic (đã biết); shot/keyframe trả về toàn paper đã biết hoặc ngoài cửa sổ 2022–2026. Không có so sánh có kiểm soát 3 hành động dưới một confidence trigger.
- **Non-English:** truy vấn tiếng Trung không chạy được (kênh chết) → chuyển sang đợt 4.

## Verdict saturation

Đợt 3 **không phát hiện công trình làm đổi keep/narrow/kill của RQ nào**. Nhưng đọc chặt RDR-0001: cần **hai vòng liên tiếp** không đổi. Đợt 2 có đổi (narrow cả ba) → đếm lại; đợt 3 = vòng yên tĩnh thứ nhất. Còn thiếu **một vòng nữa** (đợt 4 nhỏ):

1. Retry các truy vấn chết khi quota hồi phục (web_search, S2, arXiv).
2. Citation chaining theo 4 tên mới: AAPMatcher, Ada-Matcher, Bare Homography, CHAMELEON-SLAM.
3. Nguồn tiếng Trung/Hàn cho aerial mosaicking (无人机 图像拼接; 드론 영상 모자이크).

Nếu đợt 4 cũng không đổi đánh giá → đủ điều kiện 2 → ghi RDR khóa bộ RQ. Team hoàn toàn có quyền quyết khóa luôn (ghi đè đọc chặt bằng quyết định mới) — không khuyến nghị vì kênh đợt 3 bị hạn chế.

## Điểm bất định

- Phân loại 4 tên mới ở mức tiêu đề + venue (Crossref không trả abstract cho các DOI này); không ảnh hưởng verdict vì cả 4 đều rõ thuộc họ adaptive-nội-bộ / phương pháp matcher.
- Kênh tra cứu hạn chế ngày 2026-09-19; kết luận "không đổi" là search-bounded như mọi vòng trước.
