# Đợt khảo sát literature 2022–2026 để tái định hình RQ

**Người dùng:** Muốn mở một đợt khảo sát rộng các paper mới nhất liên quan đến đề tài để tìm RQ phù hợp. Phạm vi thời gian là 2022–2026 cộng các paper nền; ưu tiên cân bằng novelty–khả thi. Có thể xét sensor fusion nếu tồn tại public dataset; nếu không thì giữ RGB-first và chỉ dùng metadata tùy chọn. Nguồn lực giới hạn ở public dataset và GPU miễn phí; video nhóm tự quay chỉ dùng để external test.

**Trợ lý:** Thực hiện rapid scoping review, không phải systematic review/PRISMA. Các nhánh được quét gồm frame/keyframe selection, feature matching, homography, drift, blending, SLAM/SfM, metadata fusion và public datasets.

## 1. Kết luận chính từ literature

1. Pipeline MVP hiện tại gần như đã được công bố nguyên dạng:
   - [Hwang et al. (2026)](https://doi.org/10.3390/app16042133) dùng sparse video frames, fixed keypoint budget, RANSAC, accumulated homography và lightweight blending trên CPU.
   - Paper vẫn nêu các giới hạn quan trọng: drift dài hạn, weak texture, motion blur, parallax và thiếu ground truth.

2. Adaptive frame/keyframe selection không còn là khoảng trống độc lập:
   - [Li et al. (2023)](https://doi.org/10.3390/rs15082127) đã có keyframe selection, weighted reprojection optimization và Laplacian-pyramid fusion.
   - [DroneZaic (2025)](https://doi.org/10.1002/ppj2.70033) đã có dynamic sampling, optical flow, calibration, deep homography và mini-mosaics.
   - [OrthoTrack (ECCV 2026)](https://orthotrack.ethz.ch/) đánh giá adaptive keyframe triggers trong hệ thống map-anchored tracking.

3. So sánh detector–descriptor cổ điển không còn đủ novelty:
   - [Kim và Kim (2025)](https://isprs-archives.copernicus.org/articles/XLVIII-2-W11-2025/169/2025/) cho thấy SIFT+LightGlue đáng tin cậy trong UAV scenes có low texture và rotation lớn.
   - [Gaisbauer et al. (2025)](https://isprs-annals.copernicus.org/articles/X-1-W2-2025/35/2025/) đã so sánh classical và learned matching trên dữ liệu có camera drone.
   - [DALGlue (2025)](https://www.nature.com/articles/s41598-025-21602-5), [LightGlue (ICCV 2023)](https://openaccess.thecvf.com/content/ICCV2023/html/Lindenberger_LightGlue_Local_Feature_Matching_at_Light_Speed_ICCV_2023_paper.html) và [Efficient LoFTR (CVPR 2024)](https://openaccess.thecvf.com/content/CVPR2024/html/Wang_Efficient_LoFTR_Semi-Dense_Local_Feature_Matching_with_Sparse-Like_Speed_CVPR_2024_paper.html) đã đẩy mạnh accuracy–latency của learned matching.

4. Blending không nên là đóng góp chính:
   - [Chen et al. (2022)](https://doi.org/10.3390/rs14051068) đã kết hợp optimal seam với half-projective warp.
   - [Implicit Neural Image Stitching (WACV 2024)](https://openaccess.thecvf.com/content/WACV2024/html/Kim_Implicit_Neural_Image_Stitching_With_Enhanced_and_Blended_Feature_Reconstruction_WACV_2024_paper.html) đã nghiên cứu learned blending.

5. Sensor fusion là hướng mở nhưng có rủi ro triển khai:
   - [Aerial Image Stitching Using IMU Data (2025, preprint)](https://arxiv.org/abs/2511.06841) đã kết hợp IMU với computer vision.
   - [UASTHN (2025, preprint)](https://arxiv.org/abs/2502.01035) đã nghiên cứu uncertainty cho deep homography trong cross-modal UAV geolocalization.
   - Vì vậy, “thêm GPS/IMU” không đủ mới; câu hỏi phải xét noise, dropout và graceful degradation.

6. Khoảng trống khả thi nhất sau đợt quét:
   - Dự báo một phép ghép có làm hỏng mosaic về sau hay không.
   - Phân bổ compute ở cấp pipeline: dùng classical matcher cho cặp dễ và learned matcher cho cặp khó.
   - Recovery khi homography không đáng tin cậy, thay vì tiếp tục tích lũy lỗi.
   - Đánh giá end-to-end trên final mosaic thay vì chỉ báo pairwise matching accuracy.

## 2. Tác động lên các RQ cũ

| RQ cũ | Trạng thái sau khảo sát |
|---|---|
| Adaptive frame selection | Không giữ làm đóng góp chính; literature 2023–2026 đã có nhiều chiến lược tương tự |
| ORB vs SIFT vs AKAZE | Chỉ giữ làm classical baseline/ablation |
| Weighted vs multi-band blending | Chỉ giữ làm thành phần hoàn thiện demo |
| Ngưỡng overlap tối thiểu | Có thể dùng làm phân tích phụ, không đủ làm RQ trung tâm |

## 3. Hướng nghiên cứu đề xuất — chưa khóa

> **Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking from UAV Video**

### RQ1 — Failure prediction

> Which low-cost frame-pair indicators best predict downstream registration failure and cumulative mosaic drift across different UAV scene domains?

Tín hiệu ứng viên: blur score, số match, RANSAC inlier ratio, spatial inlier coverage, median symmetric transfer error và tính hợp lệ của projected frame quadrilateral.

### RQ2 — Adaptive matcher routing

> Can a resource-aware two-stage policy—using a classical matcher by default and invoking SIFT+LightGlue only on high-risk frame pairs—achieve a better mosaic quality–latency trade-off than always-classical and always-learned pipelines?

### RQ3 — Confidence-triggered recovery

> When registration remains unreliable, which confidence-triggered recovery action—frame rejection, previous-keyframe rematching, or submosaic splitting—most effectively limits cumulative drift without full SLAM or bundle adjustment?

### RQ4 — Tùy chọn nếu metadata đủ tốt

> Under what GPS/yaw noise and dropout levels does minimal UAV telemetry improve a failure-aware RGB mosaicking pipeline, and when does it become harmful?

## 4. Experiment contract sơ bộ

### Baselines tối thiểu

1. ORB + BF + RANSAC.
2. SIFT + FLANN + RANSAC.
3. Luôn dùng SIFT + LightGlue.
4. Đề xuất: classical-first → risk gate → learned fallback → reject/rematch/split nếu vẫn thất bại.

### Dataset

- [UMCD](https://www.umcd-dataset.net/): lựa chọn chính; 3.5 GB, thiết kế cho mosaicking, có telemetry và một số geo-referenced sequences; cần xin mật khẩu.
- [DroneZaic](https://datadryad.org/dataset/doi:10.5061/dryad.r4xgxd2q7): chọn một mission để kiểm tra repetitive agricultural texture.
- Video nhóm tự quay gần nadir: chỉ dùng external validation, không dùng để tuning.
- MovingDrone của OrthoTrack: tùy chọn nếu cần dense pose/orthophoto ground truth.

### Metrics chính

- Geometry: control-point/reference RMSE hoặc endpoint/loop drift.
- Robustness: stitching success rate, catastrophic failure rate, longest coherent segment.
- Coverage: vùng mosaic hợp lệ và số frame thực dùng.
- Efficiency: median/p95 latency mỗi frame, peak VRAM và tỷ lệ frame gọi learned fallback.
- PSNR/SSIM chỉ dùng khi có reference đã căn chỉnh; không dùng làm metric geometry chính.

## 5. Trạng thái quyết định

- Bộ RQ1–RQ3 là shortlist được khuyến nghị vì dùng chung một pipeline, một eval harness và không yêu cầu phần cứng đặc biệt.
- RQ4 là nhánh mở rộng, chỉ kích hoạt khi public dataset có metadata đồng bộ và calibration phù hợp.
- Novelty hiện mới ở mức sơ bộ; chưa tuyên bố khoảng trống cuối cùng.
- Bước kế tiếp trước khi khóa RQ: targeted review riêng cho ba cụm **failure prediction**, **matcher routing** và **recovery/mini-mosaic**.
