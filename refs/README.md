# Danh mục tài liệu tham khảo (References)

Thư mục lưu trữ các bài báo khoa học toàn văn (PDF) phục vụ nghiên cứu đề tài **Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking**.

---

## 1. UAV Mosaicking & Incremental Homography (Nền tảng & Prior Art)

| File | Tác giả & Năm | Nguồn / Venue | Vai trò trong nghiên cứu |
|---|---|---|---|
| `2026_Hwang_RealTime_2D_Orthomosaic_AppliedSciences.pdf` | Hwang et al. (2026) | Applied Sciences (MDPI) | Baseline CPU-based tuần tự; dùng inlier threshold để reject update. |
| `2023_Li_RealTime_Incremental_Video_Mosaic_RS.pdf` | Li et al. (2023) | Remote Sensing (MDPI) | Baseline tối ưu: weighted reprojection error + rematch keyframe lịch sử. |
| `2025_Kim_Robust_UAV_Mosaicking_SIFT_LightGlue_ISPRS.pdf` | Kim & Kim (2025) | ISPRS Archives | Bằng chứng thực nghiệm: SIFT+LightGlue cứu vùng ít vân và góc xoay lớn trên UAV. |
| `2022_Chen_UAV_Video_Stitching_Optimal_Seamline_RS.pdf` | Chen et al. (2022) | Remote Sensing (MDPI) | Tham chiếu xử lý seamline tối ưu và half-projective warp trong ghép video UAV. |
| `2025_Gaisbauer_Classical_Learned_Matching_UAV_ISPRS.pdf` | Gaisbauer et al. (2025) | ISPRS Annals | Benchmark so sánh classical và learned feature matching trên camera drone. |

---

## 2. RQ1 — Failure Prediction & Uncertainty Estimation (Dự báo lỗi đăng ký)

| File | Tác giả & Năm | Nguồn / Venue | Đóng góp & Khoảng trống đối chiếu |
|---|---|---|---|
| `2024_Zaffar_Image_Matching_Uncertainty_VPR_CVPR.pdf` | Zaffar et al. (2024) | CVPR 2024 | So sánh chỉ báo rẻ (inlier count/ratio) vs learned uncertainty; nhãn VPR, chưa có nhãn drift UAV. |
| `2024_Sferrazza_Keypoint_Matching_Confidence_VPR_CVPRW.pdf` | Sferrazza et al. (2024/2025) | CVPRW / IMW | Đánh giá 18 pipeline: inlier count phân loại tốt nhưng tồn tại false-positive khi vân lặp. |
| `2023_Barath_Homography_Benchmark_HEB_CVPR.pdf` | Barath et al. (2023) | CVPR 2023 | Homography Evaluation Benchmark (HEB) quy mô lớn với ground truth. |
| `2024_Yuan_Comparative_Analysis_Color_Space_Registration.pdf` | Yuan et al. (2024) | J. Imaging (MDPI) | Thực nghiệm 1.95M lượt đăng ký: reprojection error và feature count tương quan yếu với RMSE. |

---

## 3. RQ2 — Matcher Routing & Lightweight Matching (Phân luồng & Tối ưu tài nguyên)

| File | Tác giả & Năm | Nguồn / Venue | Ý nghĩa với cơ chế phân luồng |
|---|---|---|---|
| `2023_Lindenberger_LightGlue_ICCV.pdf` | Lindenberger et al. (2023) | ICCV 2023 | Learned matcher chính khi kích hoạt fallback; cơ chế early-exit và adaptive depth. |
| `2024_Potlapalli_XFeat_CVPR.pdf` | Potlapalli et al. (2024) | CVPR 2024 | Matcher learned siêu nhẹ (~27 FPS trên CPU); dùng làm baseline đối chứng Pareto. |
| `2024_Wang_Efficient_LoFTR_CVPR.pdf` | Wang et al. (2024) | CVPR 2024 | Semi-dense learned matching hiệu năng cao với token selection. |
| `2025_DALGlue_Nature_SciReports.pdf` | Nature Sci. Rep. (2025) | Nature SciReports | Deformable attention learned matching cho ảnh viễn thám / UAV. |
| `2024_ETO_Equivariant_Transform_Optimization_NeurIPS.pdf` | NeurIPS (2024) | NeurIPS 2024 | Ước lượng giả thuyết homography tốc độ cao (~21 ms). |
| `2022_Chen_OETR_Overlap_Estimation_AAAI.pdf` | Chen et al. (2022) | AAAI 2022 | Mô hình dự báo diện tích chồng lấn (overlap) phục vụ tiền xử lý trước khi match. |

---

## 4. RQ3 & Nhóm bổ trợ: Recovery, Uncertainty & Blending

| File | Tác giả & Năm | Nguồn / Venue | Ứng dụng |
|---|---|---|---|
| `2021_Ivashechkin_VSAC_ICCV.pdf` | Ivashechkin et al. (2021) | ICCV 2021 | Thuật toán VSAC độc lập đánh giá chất lượng inlier và loại bỏ model sai. |
| `2025_UASTHN_Deep_Homography_UAV_Geolocalization.pdf` | Preprint (2025) | arXiv (2025) | Ước lượng độ bất định (uncertainty) trong bài toán homography định vị UAV. |
| `2024_Implicit_Neural_Image_Stitching_WACV.pdf` | Kim et al. (2024) | WACV 2024 | Kỹ thuật tái tạo và hòa trộn vùng biên ghép bằng biểu diễn neural ngầm định. |
