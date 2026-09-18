# RESEARCH PROPOSAL

| Hạng mục | Chi tiết |
| --- | --- |
| **Research title** | **Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking for UAV Video**<br />*(Xây dựng bản đồ ảnh 2D từ video UAV với cơ chế cảnh báo lỗi và tự thích ứng tài nguyên)* |
| **Lecturer** | Nguyễn Hồng Hải - HaiNH51 |
| **Members** | 1. Diệp Quang Sáng - SE200655<br />2. Nguyễn Đức Nam - SE200991<br />3. Đào Đặng Nguyên Khôi - SE200450<br />4. Trương Quang Đăng Khoa - SE201463 |

---

## Abstract

Ghép ảnh trực giao 2D (*aerial mosaicking*) từ chuỗi video máy bay không người lái (UAV) là giải pháp thiết thực để thiết lập nhanh bản đồ hiện trạng cục bộ phục vụ giám sát nông nghiệp, khảo sát công trình, cứu hộ thiên tai và quản lý môi trường. Tuy nhiên, các quy trình ghép ảnh tuần tự truyền thống rất dễ rơi vào tình trạng mất dấu hoàn toàn (*catastrophic tracking failure*) hoặc tích lũy sai số trôi dạt hình học (*cumulative drift*) nghiêm trọng khi bay qua các địa hình đồng nhất, nghèo đặc trưng thị giác (như mặt nước, đồng ruộng) hoặc khi góc quay camera biến động đột ngột. Ngược lại, việc áp dụng toàn bộ các mô hình đối sánh học sâu (*learned matchers*) cho mọi khung hình lại đòi hỏi năng lực tính toán vượt quá khả năng của các thiết bị biên.

Nghiên cứu này đề xuất khung ghép ảnh 2D thích ứng tài nguyên và nhận biết rủi ro (**Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking**), tích hợp ba cơ chế trọng tâm: (1) Cảnh báo sớm nguy cơ lỗi đăng ký ảnh dựa trên tổ hợp chỉ báo hình học chi phí thấp ở cấp độ từng cặp khung hình liên tiếp; (2) Chiến lược phân luồng tài nguyên hai tầng (*matcher routing*), ưu tiên giải thuật cổ điển nhẹ (SIFT/ORB) trong điều kiện thuận lợi và chỉ kích hoạt bộ đối sánh học sâu (SIFT+LightGlue) khi phát hiện nguy cơ sai số cao; (3) Cơ chế phục hồi có kiểm soát nhằm ngăn chặn đứt gãy mô hình và khống chế sai số trôi dạt thông qua loại bỏ khung hình nhiễu, tái đối sánh với khung hình khóa (*keyframe*) hoặc phân tách miền ảnh con (*submosaic*). Đề tài kiểm chứng giải pháp trên các tập dữ liệu UAV thực tế (NPU Drone-Map, DroneZaic) nhằm xác lập một quy trình ghép ảnh tin cậy, cân bằng tối ưu giữa độ chính xác hình học và hiệu năng tính toán thời gian thực.

**Keywords:** UAV Video Mosaicking, Failure Prediction, Feature Matching, Matcher Routing, Homography Estimation, Cumulative Drift.

---

## 1. Introduction

### 1.1. Literature review

Ghép ảnh từ video UAV là bài toán kinh điển trong thị giác máy tính nhưng đang đứng trước nhiều thách thức mới khi mở rộng sang các kịch bản thực địa phức tạp:

- **Quy trình ghép ảnh tuần tự từ video UAV:** Các nghiên cứu gần đây tập trung tối ưu hóa quy trình ghép ảnh trực tiếp trên CPU nhằm đáp ứng tính sẵn sàng tại hiện trường. Tiêu biểu, Hwang et al. (2026) đề xuất quy trình tính toán hoàn toàn trên CPU thông qua việc giới hạn số lượng điểm đặc trưng và áp dụng bộ lọc inlier nhẹ. Li et al. (2023) kết hợp kỹ thuật chọn khung hình khóa (*keyframe selection*) với việc tối ưu sai số chiếu lại có trọng số nhằm hạn chế trôi dạt. Trong điều kiện nông nghiệp có vân bề mặt lặp lại, Kharismawati & Kazic (DroneZaic, 2025) ứng dụng dòng quang học (*optical flow*) kết hợp phân cụm ảnh con (*submosaic*). Dù đạt tốc độ xử lý khả quan, các giải pháp này phần lớn vận hành dựa trên các ngưỡng kinh nghiệm cục bộ (*heuristic*), chưa xây dựng được cơ chế định lượng mối quan hệ giữa sai số tức thời ở từng cặp khung hình với mức trôi dạt tích lũy trên toàn bộ bản đồ mosaic.
- **Đánh giá rủi ro và độ bất định trong đối sánh ảnh:** Trong lĩnh vực nhận diện vị trí bằng thị giác (VPR), Zaffar et al. (CVPR 2024) và Sferrazza et al. (CVPRW 2024/2025) chứng minh rằng số lượng và tỷ lệ điểm tương đồng nội lai (*inlier ratio*) có thể phân tách các trường hợp đối sánh thành công và thất bại; tuy nhiên, tín hiệu này vẫn dễ phát sinh dương tính giả (*false positive*) tại các vùng vân lặp. Ở bài toán ước lượng ma trận biến đổi đồng dạng (*homography*), Barath et al. (HEB, CVPR 2023) và Yuan et al. (J. Imaging 2024) chỉ ra rằng sai số chiếu lại (*reprojection error*) hay mật độ đặc trưng đơn thuần có tương quan rất yếu với sai số toàn cục (RMSE), khẳng định sự cần thiết của một tổ hợp chỉ báo đa diện chi phí thấp.
- **Đối sánh đặc trưng thích ứng tài nguyên:** Sự xuất hiện của các mô hình học sâu như LightGlue (ICCV 2023) với cơ chế dừng sớm (*early-exit*), hay XFeat (CVPR 2024) tối ưu cho phần cứng nhẹ đã nâng cao rõ rệt độ bền vững trước các biến dạng phối cảnh phức tạp. Kim & Kim (ISPRS 2025) khẳng định SIFT+LightGlue mang lại độ chính xác vượt trội trên địa hình UAV nghèo đặc trưng, song chi phí tính toán cao hơn đáng kể so với thuật toán truyền thống.
- **Bối cảnh ứng dụng thực tế tại Việt Nam:** Hiện nay, việc xử lý ảnh viễn thám UAV trong nước chủ yếu phụ thuộc vào các gói phần mềm thương mại ngoại tuyến (như Pix4D, Agisoft Metashape) theo hướng SfM/3D. Quy trình này đòi hỏi cấu hình máy trạm chuyên dụng và thời gian xử lý kéo dài nhiều giờ, không đáp ứng được yêu cầu phản ứng nhanh tại hiện trường như cứu hộ lũ lụt, đánh giá sạt lở hay trinh sát nông nghiệp. Đề tài mở ra hướng tiếp cận xử lý ảnh 2D gọn nhẹ, vận hành hiệu quả ngay trên máy tính xách tay cá nhân.

### 1.2. Limitations of current work

1. **Thiếu cơ chế cảnh báo sớm rủi ro tích lũy:** Các hệ thống hiện hành chủ yếu dùng ngưỡng inlier cố định để chấp nhận hoặc loại bỏ từng khung hình đơn lẻ, chưa có khả năng liên kết các dấu hiệu bất định ở cấp cặp khung hình để dự báo sớm nguy cơ lệch trục và trôi dạt toàn cục.
2. **Sự đánh đổi nan giải giữa độ tin cậy và chi phí tính toán:** Giải thuật cổ điển chạy nhanh nhưng dễ vỡ trận ở cảnh khó; ngược lại, việc lạm dụng mô hình học sâu cho toàn bộ khung hình gây quá tải tài nguyên và không thể triển khai trên thiết bị biên. Hiện chưa có chính sách điều phối tài nguyên linh hoạt theo mức độ rủi ro thực tế của từng khung hình.
3. **Các giải pháp phục hồi chưa được đánh giá quy chuẩn:** Các hành vi xử lý khi mất dấu (loại bỏ khung hình lỗi, đối sánh lại với keyframe, tách phân đoạn mosaic) mới chỉ xuất hiện phân tán trong từng công trình riêng lẻ và chưa từng được đối chuẩn trên cùng một ngưỡng kích hoạt (*confidence trigger*).

### 1.3. Research rationale

Đề tài giải quyết bài toán cốt lõi: *Làm thế nào để xây dựng bản đồ ảnh 2D từ video UAV một cách tin cậy, khống chế được sai số tích lũy mà không phụ thuộc vào hệ thống định vị chính xác cao (RTK-GPS) hay hạ tầng tính toán đắt tiền?* Việc kết hợp hài hòa giữa thị giác máy tính cổ điển và mô hình học sâu thông qua cơ chế nhận biết lỗi và điều phối tài nguyên thích ứng là hướng đi thực tiễn, đáp ứng trực tiếp nhu cầu thành lập bản đồ nhanh phục vụ dân sinh và hiện trường.

---

## 2. Research objectives

- **Mục tiêu tổng quát:** Xây dựng khung phần mềm ghép ảnh 2D hoàn chỉnh từ video UAV, tích hợp cơ chế nhận biết rủi ro đăng ký ảnh, tự động điều phối tài nguyên tính toán và thực thi chiến lược phục hồi nhằm kiểm soát tối đa sai số trôi dạt tích lũy.
- **Mục tiêu cụ thể (3 câu hỏi nghiên cứu cốt lõi - RDR-0003):**
  - **RQ1 (Failure Prediction):** Xác định và đánh giá tổ hợp các chỉ báo hình học chi phí thấp ở cấp độ cặp khung hình (tỷ lệ inlier, sai số chiếu lại, mức độ chồng lấn diện tích, độ phân tán không gian) trong việc dự báo nguy cơ lỗi đăng ký và độ trôi dạt tích lũy của toàn mosaic.
  - **RQ2 (Matcher Routing):** Thiết kế và đánh giá chính sách phân luồng hai tầng—mặc định sử dụng thuật toán cổ điển nhanh và chỉ kích hoạt bộ đối sánh học sâu khi rủi ro cao—nhằm tối ưu hóa sự đánh đổi giữa độ chính xác ghép nối và độ trễ xử lý.
  - **RQ3 (Confidence Recovery):** So sánh định lượng hiệu quả của ba chiến lược phục hồi (loại bỏ khung hình, tái đối sánh với keyframe, phân tách cụm submosaic) dưới cùng một điều kiện kích hoạt nhằm ngăn chặn đứt gãy chuỗi mosaic.

---

## 3. Research scope

- **Phạm vi nghiên cứu:** 
  - Dữ liệu đầu vào: Chuỗi video UAV quang học (RGB) độ dài ngắn đến trung bình (100–1000 khung hình), góc quay camera hướng thẳng đứng hoặc gần thẳng đứng (*near-nadir*), cảnh quan tương đối bằng phẳng (khu đô thị, đường giao thông, đồng ruộng).
  - Phương pháp: Tiếp cận hình học 2D dựa trên ma trận biến đổi đồng dạng tích lũy (*incremental homography estimation*), kết hợp bộ công cụ đánh giá định lượng độc lập (*evaluation harness*).
- **Giới hạn đề tài (Ngoài phạm vi):** Không bắt buộc dữ liệu GPS/IMU (chỉ sử dụng telemetry để đối chuẩn nếu có sẵn); không thực hiện tái tạo hình học 3D, SfM phức tạp hay thuật toán SLAM thời gian thực; không hướng đến bản đồ trắc địa có hệ quy chiếu tuyệt đối (*georeferencing*).

---

## 4. Feasibility of research

- **Tính khả thi về dữ liệu (RDR-0002, RDR-0003):** Sử dụng tập dữ liệu nguồn mở từ drone thực tế **NPU Drone-Map** (chứa video RGB, ảnh đã khử méo quang học, log GPS và các điểm kiểm soát mặt đất GCP chuẩn xác) làm dữ liệu thử nghiệm chính. Đồng thời sử dụng **DroneZaic (Dryad)** làm tập dữ liệu dự phòng và thử thách (*stress-test*) trong các kịch bản lặp vân nông nghiệp phức tạp.
- **Tính khả thi về thuật toán và công nghệ:** Sử dụng hệ sinh thái Python chuẩn mực (OpenCV, PyTorch, NumPy) kết hợp các mô hình đối sánh hiện đại đã được tiền huấn luyện vững chắc (LightGlue, XFeat, SIFT).
- **Tính khả thi về phần cứng:** Toàn bộ thử nghiệm được thực thi và tối ưu trên máy trạm cá nhân tiêu chuẩn (CPU đa nhân kết hợp GPU thương mại phổ thông có hỗ trợ CUDA), bảo đảm tính tái lập cao mà không cần máy chủ chuyên dụng.

---

## 5. Approach and Method

### 5.1. Kiến trúc hệ thống đề xuất (Proposed Pipeline)

Hệ thống vận hành theo quy trình tuần tự khép kín, được bảo vệ bởi các cơ chế kiểm soát rủi ro và điều phối tài nguyên:

```text
Video UAV (near-nadir) ──► Trích xuất khung hình ──► Đối sánh cổ điển (SIFT/ORB)
                                                            │
                                                     [RQ1: Cổng rủi ro]
                                                     ┌──────┴──────┐
                                      (Rủi ro thấp)  │             │ (Rủi ro cao)
                                                     ▼             ▼
                                              Tích lũy H     Đối sánh học sâu (SIFT+LightGlue)
                                                     │             │
                                                     │      [Đánh giá độ tin cậy]
                                                     │       ┌─────┴─────┐
                                                     │       │ Đạt       │ Không đạt
                                                     ▼       ▼           ▼
                                               Tích lũy H         [RQ3: Phục hồi]
                                                     │              ├── Loại khung hình
                                                     │              ├── Tái đối sánh keyframe
                                                     ▼              └── Tách submosaic
                                              Warp & Hòa trộn ảnh
                                                     │
                                                     ▼
                                        Mosaic 2D + Báo cáo chỉ số
```

### 5.2. Phương pháp thực nghiệm và tiêu chí đánh giá

- **Phương pháp đối chứng (Baselines):**
  1. *Always-Classical:* Pipeline thuần cổ điển, sử dụng SIFT/ORB kết hợp RANSAC cho toàn bộ chuỗi video.
  2. *Always-Learned:* Luôn kích hoạt bộ đối sánh học sâu (SIFT + LightGlue) cho mọi khung hình.
  3. *Sequential Baseline:* Khung xử lý tuần tự trên CPU theo công bố của Hwang et al. (2026).
- **Hệ thống chỉ số đánh giá định lượng:**
  - *Sai số hình học:* Sai số trung bình bình phương tại các điểm kiểm soát mặt đất (GCP RMSE) và sai số trôi dạt vòng khép kín (*loop closure drift*).
  - *Độ tin cậy và tính ổn định:* Tỷ lệ khung hình đăng ký thành công trên toàn chuỗi (*tracking success rate*) và tần suất xuất hiện lỗi vỡ ảnh (*failure rate*).
  - *Hiệu năng tính toán:* Độ trễ xử lý trung bình và phân vị cao (P50/P95 latency, tính bằng ms/frame), cùng tỷ lệ phần trăm khung hình phải kích hoạt bộ đối sánh học sâu.

---

## 6. Research plan

| No. | Date | Task | Output | Person in charge |
| :-: | :------------: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | :-------------------------------------------: |
|  1  | 21-9 -> 27/9   | **Chuẩn hóa dữ liệu & Thiết lập môi trường đánh giá:** Tiền xử lý dữ liệu UAV thực tế (chuỗi khung hình, metadata, GCP) và thiết lập giao thức đo lường sai số. | Bộ dữ liệu UAV chuẩn hóa; Khung công cụ đo lường định lượng (*Evaluation Harness*). | Nguyễn Đức Nam |
|  2  | 28-9 -> 4/10   | **Xây dựng pipeline ghép ảnh cơ sở (Baseline Framework):** Hiện thực quy trình ghép ảnh tuần tự 2D dựa trên homography tích lũy và kiểm chứng độ ổn định ban đầu. | Khung phần mềm ghép ảnh 2D cơ sở; Kết quả mosaic đối chứng sơ bộ. | Diệp Quang Sáng |
|  3  | 5-10 -> 11/10  | **Nghiên cứu cơ chế dự báo rủi ro & Phân luồng tài nguyên (RQ1, RQ2):** Mô hình hóa chỉ báo lỗi cấp cặp khung hình và xây dựng bộ điều phối đối sánh hai tầng. | Module nhận biết rủi ro đăng ký (*Risk Gate*); Chính sách phân luồng tài nguyên (*Matcher Router*). | Đào Đặng Nguyên Khôi |
|  4  | 12-10 -> 18/10 | **Phát triển chiến lược phục hồi & Tích hợp hệ thống (RQ3):** Hiện thực các hành vi phục hồi có kiểm soát (loại khung hình, tái đối sánh, tách cụm ảnh con) và hoàn thiện hệ thống. | Module phục hồi theo độ tin cậy; Pipeline ghép ảnh hoàn chỉnh (*Integrated Pipeline*). | Trương Quang Đăng Khoa |
|  5  | 19-10 -> 25/10 | **Thực nghiệm diện rộng & Đánh giá định lượng:** Thực thi kiểm chứng trên tập dữ liệu chuẩn và kịch bản thử thách; đối chuẩn toàn diện sai số hình học và độ trễ. | Tập dữ liệu kết quả thực nghiệm định lượng (RMSE, drift, latency profile); Báo cáo thực nghiệm đối chuẩn. | Nguyễn Đức Nam, Trương Quang Đăng Khoa |
|  6  | 26-10 -> 31/10 | **Tổng hợp kết quả nghiên cứu & Hoàn thiện tài liệu đề tài:** Phân tích phát hiện khoa học từ 3 câu hỏi nghiên cứu; đóng gói mã nguồn và hoàn chỉnh báo cáo tổng kết. | Báo cáo nghiên cứu khoa học hoàn chỉnh (*Research Report*); Kho mã nguồn và tài liệu kỹ thuật đóng gói. | Cả nhóm |

---

## 7. Computational Resource Requirements

- **Phần cứng thực nghiệm:** 01 Máy trạm cá nhân: CPU 8 nhân / 16 luồng, RAM 16–32 GB, GPU hỗ trợ CUDA $\ge 6$ GB VRAM (đáp ứng tốt nhu cầu chạy suy luận cho LightGlue/XFeat).
- **Lưu trữ dữ liệu:** Khoảng 100 GB dung lượng ổ cứng để lưu trữ và xử lý các tập dữ liệu NPU Drone-Map và DroneZaic.

---

## 8. Expected results

1. **Sản phẩm mã nguồn:** Khung phần mềm hoàn chỉnh cho bài toán ghép ảnh 2D từ video UAV tích hợp cơ chế phân luồng tài nguyên và phục hồi lỗi, đi kèm bộ công cụ đánh giá tự động, sẵn sàng công bố mã nguồn mở.
2. **Dữ liệu thực nghiệm khoa học:** Báo cáo phân tích định lượng chi tiết cung cấp lời giải rõ ràng cho 3 câu hỏi nghiên cứu RQ1, RQ2 và RQ3.
3. **Ấn phẩm khoa học:** Một bài báo khoa học hoàn chỉnh trình bày phương pháp luận, kiến trúc đề xuất và kết quả thực nghiệm để công bố tại hội nghị hoặc tạp chí chuyên ngành.

---

## References

1. D. Hwang et al., "Real-Time 2D Orthomosaic Mapping Using CPU-Based Incremental Homography Matrix Estimation with UAV Video," *Appl. Sci.*, vol. 16, no. 4, p. 2133, 2026.
2. X. Li et al., "A Real-Time Incremental Video Mosaic Framework for UAV Remote Sensing," *Remote Sens.*, vol. 15, no. 8, p. 2127, 2023.
3. M. Kharismawati and D. Kazic, "DroneZaic: A robust end-to-end pipeline for mosaicking freely flown aerial video of agricultural fields," *Plant Phenome J.*, vol. 8, no. 1, p. e70033, 2025.
4. M. Zaffar et al., "On the Estimation of Image-Matching Uncertainty in Visual Place Recognition," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2024, pp. 17873–17883.
5. C. Sferrazza et al., "To Match or Not to Match: Evaluating Keypoint Matching Confidence for Visual Place Recognition," in *CVPRW*, 2024.
6. D. Barath et al., "A Large-Scale Homography Benchmark," in *Proc. CVPR*, 2023, pp. 9272–9281.
7. P. Lindenberger, P.-E. Sarlin, and M. Pollefeys, "LightGlue: Local Feature Matching at Light Speed," in *Proc. ICCV*, 2023, pp. 10853–10863.
8. P. Potlapalli et al., "XFeat: Accelerated Features for Lightweight Image Matching," in *Proc. CVPR*, 2024, pp. 20045–20054.
9. J. Kim and S. Kim, "Robust UAV Image Mosaicking Using SIFT and LightGlue," *Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci.*, vol. XLVIII-2-W11-2025, pp. 169–173, 2025.
10. J. Chen et al., "UAV Video Stitching Based on Optimal Seamline and Half-Projective Warp," *Remote Sens.*, vol. 14, no. 5, p. 1068, 2022.
11. H. Yuan, D. Peng, and M. Dong, "Comparative Analysis of Color Space Transformations on Feature-Based Image Registration," *J. Imaging*, vol. 10, no. 5, p. 105, 2024.
12. Q. Wang et al., "Efficient LoFTR: Semi-Dense Local Feature Matching with Sparse-Like Speed," in *Proc. CVPR*, 2024, pp. 19994–20003.
