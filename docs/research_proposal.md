# RESEARCH PROPOSAL

| Hạng mục           | Chi tiết                                                                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Research title** | **Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking for UAV Video**<br />(Xây dựng bản đồ ảnh 2D từ video UAV với cơ chế cảnh báo lỗi và tự thích ứng tài nguyên) |
| **Lecturer**       | Nguyễn Hồng Hải - HaiNH51                                                                                                                                                |
| **Members**        | 1. Diệp Quang Sáng - SE200655<br />2. Nguyễn Đức Nam - SE200991<br />3. Đào Đặng Nguyên Khôi - SE200450<br />4. Trương Quang Đăng Khoa - SE201463                        |

---

## Abstract

Ghép ảnh 2D từ video máy bay không người lái (UAV) là phương pháp hiệu quả để tạo bản đồ hiện trạng phục vụ nông nghiệp, xây dựng, cứu hộ và giám sát môi trường. Tuy nhiên, các pipeline tuần tự truyền thống dễ gãy đổ (_catastrophic failure_) hoặc tích lũy sai số trôi dạt (_cumulative drift_) khi bay qua địa hình ít vân (mặt nước, đồng lúa) hoặc camera xoay đột ngột. Nghiên cứu này đề xuất khung ghép ảnh **Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking**, tích hợp 3 cơ chế: (1) Dự báo sớm rủi ro đăng ký bằng các chỉ báo tính toán rẻ ở cấp cặp-frame; (2) Phân luồng tài nguyên 2 tầng (_matcher routing_), ưu tiên thuật toán truyền thống nhẹ (SIFT/ORB) và chỉ kích hoạt deep matcher (SIFT+LightGlue) khi rủi ro cao; (3) Tự phục hồi có kiểm soát (loại bỏ frame, ghép lại keyframe cũ, tách submosaic) khi xảy ra lỗi. Đề tài kiểm chứng thực nghiệm trên các bộ dữ liệu drone thực tế (NPU Drone-Map, DroneZaic), hướng tới cân bằng tối ưu giữa độ chính xác hình học, tính bền vững và thời gian thực thi trên phần cứng giới hạn.

**Keywords:** UAV Video Mosaicking, Failure Prediction, Feature Matching, Matcher Routing, Homography Estimation, Cumulative Drift.

---

## 1. Introduction / Giới thiệu

### 1.1. Literature review / Tình hình nghiên cứu trong và ngoài nước

- **Ghép ảnh UAV tuần tự:** Hwang et al. (2026) đề xuất pipeline CPU thuần túy với ngân sách keypoint cố định và lọc inlier đơn giản; Li et al. (2023) tối ưu sai số chiếu lại có trọng số kết hợp chọn keyframe. Tuy nhiên, cả hai đều chỉ dùng heuristic vận hành, chưa có nhãn đo drift định lượng và không có cơ chế dự báo lỗi. Kharismawati & Kazic (DroneZaic, 2025) xử lý chuyển động bằng optical flow và tách submosaic trên ảnh nông nghiệp lặp vân.
- **Chỉ báo lỗi và độ bất định (Failure Indicators):** Trong bài toán Visual Place Recognition (VPR), Zaffar et al. (CVPR 2024) và Sferrazza et al. (CVPRW 2024/2025) chứng minh số lượng inlier phân biệt tốt matching thất bại nhưng dễ sinh false-positive ở cảnh lặp vân. Barath et al. (HEB, CVPR 2023) và Yuan et al. (J. Imaging 2024) khẳng định sai số chiếu lại (reprojection error) và số lượng đặc trưng tương quan rất yếu với sai số toàn cục (RMSE).
- **Feature Matcher thích ứng tài nguyên:** LightGlue (ICCV 2023) giới thiệu cơ chế early-exit thích ứng; XFeat (CVPR 2024) đạt tốc độ ~27 FPS trên CPU; Kim & Kim (ISPRS 2025) chứng minh SIFT+LightGlue vượt trội ở địa hình UAV ít vân nhưng chi phí tính toán cao.
- **Tại Việt Nam & Ứng dụng:** Các nghiên cứu viễn thám trong nước chủ yếu dùng phần mềm thương mại (Pix4D, Agisoft) với quy trình SfM/3D nặng, đòi hỏi nhiều giờ xử lý offline. Nhu cầu bản đồ 2D nhanh phục vụ trinh sát hiện trường, đánh giá lũ lụt và nông nghiệp chính xác là rất lớn.

### 1.2. The limitation of current works / Những hạn chế của các nghiên cứu hiện tại

1. **Thiếu khả năng dự báo lỗi sớm:** Các pipeline UAV hiện tại chỉ kiểm tra ngưỡng inlier tối thiểu để nhận/loại frame một cách cục bộ, chưa có mô hình liên kết tín hiệu cặp-frame với drift tích luỹ toàn cục.
2. **Tiến thoái lưỡng nan về tài nguyên:** Sử dụng 100% thuật toán cổ điển sẽ gãy ở cảnh khó; lạm dụng 100% deep matcher gây lãng phí năng lượng/tài nguyên trên thiết bị biên.
3. **Cơ chế phục hồi phân mảnh:** Các kỹ thuật loại frame, quay lại mốc cũ hoặc chia nhỏ bản đồ tồn tại rời rạc, chưa từng được so sánh đối đầu dưới một ngưỡng kích hoạt (_confidence trigger_) thống nhất.

### 1.3. The necessity of the research / Sự cần thiết tiến hành nghiên cứu

Xây dựng một pipeline có nhận thức về rủi ro (_failure-aware_) và tự thích ứng tài nguyên giúp drone dã chiến có thể tự xử lý video và tạo bản đồ hiện trạng tin cậy mà không phụ thuộc GPS độ chính xác cao (RTK) hay trạm máy chủ GPU cồng kềnh.

---

## 2. Research objectives / Mục tiêu của đề tài

- **Mục tiêu tổng quát:** Xây dựng pipeline phần mềm ghép video UAV thành ảnh trực giao 2D (mosaic) có cơ chế tự thích ứng phân luồng tài nguyên và phục hồi chống trôi dạt sai số.
- **Mục tiêu cụ thể (3 Research Questions - RDR-0003):**
  - **RQ1 (Failure Prediction):** Xác định tổ hợp chỉ báo chi phí thấp ở cấp cặp-frame (inlier ratio, reprojection error, overlap, spatial spread) có năng lực dự báo chính xác lỗi đăng ký và drift tích luỹ.
  - **RQ2 (Matcher Routing):** Thiết kế chính sách phân luồng 2 tầng (classical mặc định $\to$ learned fallback khi rủi ro cao) đạt biên tối ưu chất lượng–độ trễ (_Pareto front_) vượt trội so với always-classical và always-learned.
  - **RQ3 (Confidence Recovery):** Đánh giá thực nghiệm 3 hành động phục hồi (reject / rematch keyframe / split submosaic) dưới cùng một trigger để hạn chế tối đa drift tích lũy.

---

## 3. Research scope / Phạm vi nghiên cứu

- **Trong phạm vi:** Video UAV ngắn (100–1000 frames), camera góc gần thẳng đứng (near-nadir), cảnh tương đối phẳng (đồng ruộng, đô thị, giao thông); pipeline homography tích lũy 2D kết hợp eval harness đo đếm định lượng.
- **Ngoài phạm vi:** Không bắt buộc GPS/IMU (dữ liệu telemetry chỉ dùng đối chứng nếu có); không tái tạo 3D/SfM/SLAM; không khảo sát trắc địa địa chính có georeference tuyệt đối.

---

## 4. Feasibility of research / Tính khả thi của đề tài

- **Dữ liệu khả dụng (RDR-0002):** Tập chính **NPU Drone-Map** (video RGB drone thật, ảnh hiệu chỉnh méo, GPS log, GCP đo sai số); tập dự phòng & stress-test **DroneZaic (Dryad)** (ảnh nông nghiệp lặp vân cao).
- **Công nghệ & Công cụ:** Triển khai trên Python, OpenCV, PyTorch; mô hình tiền huấn luyện sẵn có (LightGlue, XFeat, SIFT).
- **Hạ tầng tính toán:** Khả thi trên máy tính cá nhân tiêu chuẩn (CPU đa nhân, GPU phổ thông phục vụ suy luận learned matcher).

---

## 5. Approach and Method / Cách tiếp cận và phương pháp nghiên cứu

### 5.1. Kiến trúc hệ thống đề xuất (Proposed Pipeline)

```text
Video UAV (Nadir) ──► Trích xuất Frame ──► Classical Matcher (SIFT/ORB)
                                                   │
                                            [RQ1: Risk Gate]
                                            ┌──────┴──────┐
                               (Rủi ro thấp)│             │(Rủi ro cao)
                                            ▼             ▼
                                     Tích luỹ H     Learned Matcher (SIFT+LightGlue)
                                            │             │
                                            │     [Kiểm tra độ tin cậy]
                                            │      ┌──────┴──────┐
                                            │      │Đạt          │Vẫn hỏng
                                            ▼      ▼             ▼
                                        Tích luỹ H       [RQ3: Phục hồi]
                                            │            ├── Reject frame
                                            ▼            ├── Rematch keyframe
                                        Warp & Blend     └── Split submosaic
                                            │
                                            ▼
                                  Mosaic 2D + Log Metric
```

### 5.2. Phương pháp thực nghiệm & Đo lường

- **Baselines đối chứng:** (1) Always-Classical (SIFT/ORB + RANSAC); (2) Always-Learned (SIFT + LightGlue toàn bộ); (3) Pipeline tuần tự baseline (Hwang et al., 2026).
- **Metrics:** (a) Sai số hình học: RMSE điểm kiểm soát (GCP) và drift khép vòng (loop drift); (b) Độ bền vững: Tỷ lệ ghép thành công chuỗi, tỷ lệ gãy vỡ; (c) Hiệu năng: Độ trễ P50/P95 (ms/frame), tỷ lệ frame gọi learned matcher.

---

## 6. Research plan / Kế hoạch thực hiện nghiên cứu

| No. | Date | Task | Output | Person in charge |
| :-: | :--: | ---- | ------ | :--------------: |
|  1  |      |      |        |                  |
|  2  |      |      |        |                  |
|  3  |      |      |        |                  |
|  4  |      |      |        |                  |
|  5  |      |      |        |                  |
|  6  |      |      |        |                  |

---

## 7. Computational Resource Requirements / Yêu cầu tài nguyên tính toán

- **Phần cứng:** Máy trạm cá nhân (01 PC): CPU 8 cores/16 threads, RAM 16–32 GB, GPU hỗ trợ CUDA $\ge 6$ GB VRAM (chạy inference LightGlue).
- **Lưu trữ:** 100 GB ổ cứng cho dataset NPU Drone-Map và DroneZaic.

---

## 8. Expected results / Dự kiến kết quả đề tài

1. **Mã nguồn:** Pipeline hoàn chỉnh kèm bộ công cụ đo kiểm (Evaluation Harness) mã nguồn mở.
2. **Dữ liệu thực nghiệm:** Báo cáo đối sánh định lượng cho 3 câu hỏi nghiên cứu (RQ1, RQ2, RQ3).
3. **Ấn phẩm khoa học:** 01 bài báo khoa học trình bày giải pháp và kết quả thực nghiệm.

---

## References / Tài liệu tham khảo

1. D. Hwang et al., "Real-Time 2D Orthomosaic Mapping Using CPU-Based Incremental Homography Matrix Estimation with UAV Video," _Appl. Sci._, vol. 16, no. 4, p. 2133, 2026.
2. X. Li et al., "A Real-Time Incremental Video Mosaic Framework for UAV Remote Sensing," _Remote Sens._, vol. 15, no. 8, p. 2127, 2023.
3. M. Kharismawati and D. Kazic, "DroneZaic: A robust end-to-end pipeline for mosaicking freely flown aerial video of agricultural fields," _Plant Phenome J._, vol. 8, no. 1, p. e70033, 2025.
4. M. Zaffar et al., "On the Estimation of Image-Matching Uncertainty in Visual Place Recognition," in _Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)_, 2024, pp. 17873–17883.
5. C. Sferrazza et al., "To Match or Not to Match: Evaluating Keypoint Matching Confidence for Visual Place Recognition," in _CVPRW_, 2024.
6. D. Barath et al., "A Large-Scale Homography Benchmark," in _Proc. CVPR_, 2023, pp. 9272–9281.
7. P. Lindenberger, P.-E. Sarlin, and M. Pollefeys, "LightGlue: Local Feature Matching at Light Speed," in _Proc. ICCV_, 2023, pp. 10853–10863.
8. P. Potlapalli et al., "XFeat: Accelerated Features for Lightweight Image Matching," in _Proc. CVPR_, 2024, pp. 20045–20054.
9. J. Kim and S. Kim, "Robust UAV Image Mosaicking Using SIFT and LightGlue," _Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci._, vol. XLVIII-2-W11-2025, pp. 169–173, 2025.
10. J. Chen et al., "UAV Video Stitching Based on Optimal Seamline and Half-Projective Warp," _Remote Sens._, vol. 14, no. 5, p. 1068, 2022.
11. H. Yuan, D. Peng, and M. Dong, "Comparative Analysis of Color Space Transformations on Feature-Based Image Registration," _J. Imaging_, vol. 10, no. 5, p. 105, 2024.
12. Q. Wang et al., "Efficient LoFTR: Semi-Dense Local Feature Matching with Sparse-Like Speed," in _Proc. CVPR_, 2024, pp. 19994–20003.
