# RESEARCH PROPOSAL

| Hạng mục           | Chi tiết                                                                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Research title** | **Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking for UAV Video**<br />(Xây dựng bản đồ ảnh 2D từ video UAV với cơ chế cảnh báo lỗi và tự thích ứng tài nguyên) |
| **Lecturer**       | Nguyễn Hồng Hải - HaiNH51                                                                                                                                                |
| **Members**        | 1. Diệp Quang Sáng - SE200655<br />2. Nguyễn Đức Nam - SE200991<br />3. Đào Đặng Nguyên Khôi - SE200450<br />4. Trương Quang Đăng Khoa - SE201463                        |

---

## Abstract

Việc ghép ảnh 2D từ video máy bay không người lái (UAV) cho phép tạo mosaic hiện trạng cục bộ phục vụ nông nghiệp, xây dựng, cứu hộ và giám sát môi trường. Tuy nhiên, pipeline tuần tự có thể thất bại nghiêm trọng (_catastrophic failure_) hoặc tích lũy sai số trôi dạt (_cumulative drift_) khi cảnh có ít đặc trưng, như mặt nước và đồng lúa, hoặc khi camera quay đột ngột. Nghiên cứu này đề xuất khung ghép ảnh **Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking** gồm ba cơ chế: (1) dự báo sớm rủi ro đăng ký từ các chỉ báo chi phí thấp ở cấp cặp frame; (2) phân luồng tài nguyên hai tầng (_matcher routing_), dùng SIFT/ORB mặc định và chỉ kích hoạt learned matcher SIFT+LightGlue khi rủi ro cao; (3) phục hồi có kiểm soát bằng cách loại frame, ghép lại với keyframe trước đó hoặc tách submosaic. Đề tài sẽ đánh giá khung trên các bộ dữ liệu UAV thực tế (NPU Drone-Map, DroneZaic) theo sai số hình học, tỷ lệ ghép thành công và độ trễ thực thi trong điều kiện giới hạn tài nguyên.

**Keywords:** UAV Video Mosaicking, Failure Prediction, Feature Matching, Matcher Routing, Homography Estimation, Cumulative Drift.

---

## 1. Introduction / Giới thiệu

### 1.1. Literature review / Tình hình nghiên cứu trong và ngoài nước

- **Ghép ảnh UAV tuần tự:** Hwang et al. (2026) trình bày pipeline chạy hoàn toàn trên CPU với ngân sách keypoint cố định và bước lọc inlier đơn giản. Li et al. (2023) tối ưu sai số chiếu lại có trọng số kết hợp với chọn keyframe. Hai công trình này dùng heuristic vận hành, nhưng chưa liên hệ các tín hiệu ở cấp cặp frame với drift tích lũy trên toàn mosaic. Kharismawati & Kazic (DroneZaic, 2025) sử dụng optical flow và tách submosaic cho ảnh nông nghiệp có đặc trưng lặp lại.
- **Chỉ báo lỗi và độ bất định (Failure Indicators):** Trong Visual Place Recognition (VPR), Zaffar et al. (CVPR 2024) và Sferrazza et al. (CVPRW 2024/2025) cho thấy số inlier có thể phân biệt các trường hợp matching thất bại, nhưng vẫn có false positive ở cảnh lặp vân. Barath et al. (HEB, CVPR 2023) và Yuan et al. (J. Imaging 2024) ghi nhận tương quan yếu giữa sai số chiếu lại, số lượng đặc trưng và sai số toàn cục (RMSE).
- **Feature matcher thích ứng tài nguyên:** LightGlue (ICCV 2023) dùng cơ chế early-exit thích ứng. XFeat (CVPR 2024) đạt khoảng 27 FPS trên CPU. Kim & Kim (ISPRS 2025) báo cáo SIFT+LightGlue cho kết quả tốt hơn ở địa hình UAV ít đặc trưng, với chi phí tính toán cao hơn.
- **Bối cảnh ứng dụng tại Việt Nam:** Nhiều quy trình viễn thám trong nước sử dụng phần mềm thương mại như Pix4D và Agisoft theo hướng SfM/3D, thường cần xử lý ngoại tuyến trong thời gian dài. Đề tài tập trung vào việc tạo mosaic 2D cục bộ nhanh cho các tình huống trinh sát hiện trường, đánh giá lũ lụt và nông nghiệp chính xác.

### 1.2. Limitations of current work / Những hạn chế của các nghiên cứu hiện tại

1. **Thiếu dự báo lỗi sớm:** Pipeline UAV hiện hành thường dùng ngưỡng inlier tối thiểu để nhận hoặc loại frame cục bộ, nhưng chưa liên hệ các tín hiệu ở cấp cặp frame với drift tích lũy của toàn mosaic.
2. **Đánh đổi tài nguyên:** Việc chỉ dùng thuật toán cổ điển có thể thất bại ở cảnh khó, trong khi chạy learned matcher cho mọi frame làm tăng chi phí tính toán trên thiết bị biên.
3. **Phục hồi chưa được đánh giá thống nhất:** Các cơ chế loại frame, ghép lại với keyframe hoặc tách submosaic đã xuất hiện trong các công trình khác nhau, nhưng chưa được so sánh trực tiếp dưới cùng một ngưỡng kích hoạt (_confidence trigger_).

### 1.3. Research rationale / Sự cần thiết tiến hành nghiên cứu

Đề tài xem xét một pipeline có cơ chế nhận biết rủi ro và điều phối tài nguyên để đánh giá khả năng tạo mosaic 2D cục bộ từ video UAV mà không yêu cầu GPS độ chính xác cao (RTK) hoặc máy chủ GPU. Điều này phù hợp với các nhiệm vụ hiện trường có hạ tầng tính toán hạn chế.

---

## 2. Research objectives / Mục tiêu của đề tài

- **Mục tiêu tổng quát:** Xây dựng pipeline phần mềm tạo mosaic 2D từ video UAV, có cơ chế phân luồng tài nguyên và phục hồi nhằm hạn chế drift tích lũy.
- **Mục tiêu cụ thể (3 Research Questions - RDR-0003):**
  - **RQ1 (Failure Prediction):** Xác định tổ hợp chỉ báo chi phí thấp ở cấp cặp frame (inlier ratio, reprojection error, overlap, spatial spread) và đánh giá khả năng dự báo lỗi đăng ký cùng drift tích lũy.
  - **RQ2 (Matcher Routing):** Đánh giá chính sách phân luồng hai tầng, dùng classical matcher mặc định và learned matcher khi rủi ro cao, theo đánh đổi giữa chất lượng ghép và độ trễ so với các baseline luôn dùng một loại matcher.
  - **RQ3 (Confidence Recovery):** So sánh ba hành động phục hồi (loại frame, ghép lại với keyframe, tách submosaic) dưới cùng một trigger để giới hạn drift tích lũy.

---

## 3. Research scope / Phạm vi nghiên cứu

- **Trong phạm vi:** Video UAV ngắn (100–1000 frame), camera gần thẳng đứng (near-nadir), cảnh tương đối phẳng (đồng ruộng, đô thị, giao thông); pipeline tích lũy homography 2D kết hợp bộ đánh giá định lượng.
- **Ngoài phạm vi:** Không bắt buộc GPS/IMU (dữ liệu telemetry chỉ dùng đối chứng nếu có); không tái tạo 3D/SfM/SLAM; không khảo sát trắc địa địa chính có georeference tuyệt đối.

---

## 4. Feasibility of research / Tính khả thi của đề tài

- **Dữ liệu khả dụng (RDR-0002):** NPU Drone-Map là tập dữ liệu chính, gồm video UAV RGB, ảnh đã hiệu chỉnh méo, log GPS và điểm kiểm soát mặt đất (GCP) để đo sai số. DroneZaic (Dryad) là phương án dự phòng và tập stress-test cho cảnh nông nghiệp có đặc trưng lặp lại.
- **Công nghệ và công cụ:** Python, OpenCV, PyTorch cùng các mô hình tiền huấn luyện sẵn có như LightGlue, XFeat và SIFT.
- **Hạ tầng tính toán:** Máy tính cá nhân với CPU đa nhân và GPU phổ thông đủ để thực hiện suy luận learned matcher.

---

## 5. Approach and Method / Cách tiếp cận và phương pháp nghiên cứu

### 5.1. Kiến trúc hệ thống đề xuất (Proposed Pipeline)

```text
Video UAV (near-nadir) ──► Trích xuất frame ──► Classical matcher (SIFT/ORB)
                                                      │
                                               [RQ1: Risk gate]
                                               ┌──────┴──────┐
                                (Rủi ro thấp) │             │ (Rủi ro cao)
                                               ▼             ▼
                                        Tích lũy H     Learned matcher (SIFT+LightGlue)
                                               │             │
                                               │      [Đánh giá độ tin cậy]
                                               │       ┌─────┴─────┐
                                               │       │ Đạt       │ Không đạt
                                               ▼       ▼            ▼
                                         Tích lũy H         [RQ3: Phục hồi]
                                               │              ├── Loại frame
                                               │              ├── Ghép lại keyframe
                                               ▼              └── Tách submosaic
                                        Warp và blend
                                               │
                                               ▼
                                  Mosaic 2D + nhật ký chỉ số
```

### 5.2. Phương pháp thực nghiệm và chỉ số đánh giá

- **Phương pháp đối chứng:** (1) Always-Classical (SIFT/ORB + RANSAC); (2) Always-Learned (SIFT + LightGlue cho toàn bộ frame); (3) pipeline tuần tự baseline của Hwang et al. (2026).
- **Chỉ số đánh giá:** (a) sai số hình học: RMSE tại các điểm kiểm soát mặt đất (GCP) và loop drift; (b) độ ổn định: tỷ lệ ghép thành công theo chuỗi và tỷ lệ thất bại; (c) hiệu năng: độ trễ P50/P95 (ms/frame) và tỷ lệ frame gọi learned matcher.

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

1. **Mã nguồn:** Pipeline hoàn chỉnh cùng bộ công cụ đánh giá định lượng, dự kiến công bố mã nguồn mở.
2. **Dữ liệu thực nghiệm:** Báo cáo kết quả định lượng cho ba câu hỏi nghiên cứu RQ1, RQ2 và RQ3.
3. **Ấn phẩm khoa học:** Một bài báo trình bày giải pháp và kết quả thực nghiệm.

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
