# Giải thích Detector, Matcher và vai trò trong nghiên cứu Failure-Aware Mosaicking

Tài liệu giải thích cốt lõi hai thành phần **Detector** (bộ dò điểm), **Matcher** (bộ so khớp) và vai trò trung tâm của chúng trong bài toán ghép ảnh UAV 2D theo định hướng nghiên cứu Failure-Aware (RDR-0003).

---

## 1. Bản chất cốt lõi: Detector và Matcher làm gì?

Để ghép 2 khung hình liên tiếp ($I_{t-1}$ và $I_t$) từ drone thành một bức ảnh panorama, máy tính phải giải quyết bài toán: **"Điểm này ở ảnh trước tương ứng với điểm nào ở ảnh sau?"**

Quy trình giải quyết gồm 2 bước tách bạch:

```
[ Ảnh thô ] ──> 1. DETECTOR  ──> Tìm toạ độ các điểm đặc biệt (Where?)
                     │
            [ Descriptor ]   ──> Mã hoá hoa văn quanh điểm thành vector số (What?)
                     │
            ──> 2. MATCHER   ──> Nối điểm ảnh 1 với điểm ảnh 2 (Which pair matches?)
                     │
            ──> [ RANSAC ]   ──> Lọc match sai & tính ma trận Homography (H)
```

### 1.1. Detector (Bộ dò tìm điểm đặc trưng)

- **Nhiệm vụ:** Quét toàn bộ ảnh để tìm toạ độ $(x, y)$ của các điểm "dễ nhận biết" (góc nhà, ngã tư, ngọn cây, ranh giới thửa đất) và bền vững khi góc bay, tỷ lệ hoặc độ sáng thay đổi.
- **Ví dụ trong dự án:**
  - _FAST (trong ORB):_ So sánh độ sáng vòng tròn 16 pixel quanh tâm. Cực nhẹ, chạy nhanh trên CPU.
  - _DoG - Difference of Gaussians (trong SIFT):_ Tìm cực trị trong không gian đa tỷ lệ (scale-space). Bền vững cao khi drone đổi độ cao.
  - _SuperPoint Detector:_ Mạng CNN được huấn luyện để phát hiện góc chuẩn xác ngay cả khi ảnh bị mờ chuyển động hoặc ít vân.

### 1.2. Matcher (Bộ so khớp đặc trưng)

- **Nhiệm vụ:** Nhận tập điểm đặc trưng từ 2 ảnh, so sánh độ tương đồng và quyết định cặp điểm nào thuộc về nhau.
- **Ví dụ trong dự án:**
  - _Classical Matcher (BFMatcher, FLANN):_ So khớp véc-tơ cục bộ độc lập dựa trên khoảng cách (Hamming cho ORB, L2 Euclidean cho SIFT) kèm bộ lọc Lowe's Ratio Test ($d_1 / d_2 < 0.75$).
  - _Learned Matcher (LightGlue, SuperGlue):_ Dùng Transformer / GNN để "nhìn" toàn bộ cụm điểm trên cả 2 ảnh, hiểu ngữ cảnh hình học toàn cục để loại trừ match giả ở địa hình khó (đồng ruộng, tán rừng lặp vân).

---

## 2. Vai trò sống còn của Detector & Matcher trong 3 RQ của dự án

Đề tài nghiên cứu là **Failure-Aware Mosaicking**: thay vì ghép mù quáng, hệ thống chủ động dự báo rủi ro lỗi ghép, phân luồng matcher và kích hoạt phục hồi để chặn trôi sai số (drift).

Detector và Matcher đóng vai trò mấu chốt trong cả 3 câu hỏi nghiên cứu:

```
                       ┌─────────────────────────┐
                       │  Khung hình UAV mới (t) │
                       └────────────┬────────────┘
                                    │
                              [ DETECTOR ] ──> Kiểm tra độ phủ không gian (RQ1)
                                    │
                         ┌──────────┴──────────┐
                         │  RISK GATE (RQ2)    │
                         └─────┬─────────┬─────┘
                     Ít rủi ro │         │ Rủi ro cao
                               ▼         ▼
                    Classical Matcher   Learned Matcher
                     (ORB / SIFT BF)     (LightGlue)
                               │         │
                         ┌─────┴─────────┴─────┐
                         │  Đánh giá kết quả   │ ──> Inliers, Reproj Error (RQ1)
                         └──────────┬──────────┘
                                    │
                     Đạt độ tin cậy │ Không đạt (Thất bại)
                                    ▼
                                  Ghép H ──(Fail)──> RECOVERY (RQ3)
                                                     - Bỏ frame
                                                     - Rematch keyframe
                                                     - Tách submosaic
```

### 2.1. Đối với RQ1 (Failure Prediction — Dự báo lỗi đăng ký)

Hệ thống dùng các chỉ báo rẻ (cheap indicators) sinh ra trực tiếp từ Detector và Matcher để biết ma trận $H$ sắp tính có tin cậy không:

- **Tín hiệu từ Detector:**
  - _Độ bao phủ không gian (Spatial Distribution / Bounding Box Area):_ Nếu Detector tìm được 1000 điểm nhưng tất cả dồn vào 1 góc nhỏ (do góc kia là mặt hồ phẳng lì), phép tính $H$ chắc chắn bị xoay méo cực đoan.
- **Tín hiệu từ Matcher:**
  - _Số lượng inliers & Inlier Ratio:_ Số cặp điểm khớp hợp lệ sau RANSAC. Dưới ngưỡng tối thiểu (ví dụ $< 20\text{--}30$ inliers) $\to$ cờ báo động đỏ.
  - _Sai số chiếu lại trung bình (Reprojection Error):_ Đo độ lệch hình học pixel giữa 2 ảnh sau khi áp ma trận $H$.

### 2.2. Đối với RQ2 (Matcher Routing — Phân luồng bộ khớp theo rủi ro)

Đây là nơi Matcher đóng vai trò **trọng tâm thiết kế**:

- **Nghịch lý thực tế:**
  - Classical Matcher (ORB/SIFT): Siêu nhanh (vài chục ms, chạy tốt trên CPU drone), nhưng dễ gãy khi bay qua vùng ít chi tiết, tán cây lặp vân, hoặc đổi góc gắt.
  - Learned Matcher (LightGlue): Ghép cực kỳ chính xác và kiên cường, nhưng rất nặng (chậm hơn 10–20 lần, đòi hỏi GPU, ngốn pin).
- **Giải pháp Routing (RQ2):**
  - **Tầng 1 (Mặc định):** Chạy Classical Matcher nhẹ. Với 80% thời gian drone bay thẳng qua cảnh nhà cửa bình thường, tầng này hoàn thành tốt nhiệm vụ ở độ trễ cực thấp.
  - **Tầng 2 (Dự phòng rủi ro):** Khi chỉ số rủi ro (RQ1) cảnh báo nguy cơ trôi lỗi hoặc match thấp $\to$ Risk Gate mới kích hoạt Learned Matcher (SuperPoint + LightGlue) để giải cứu.
  - Nhờ đó, hệ thống đạt điểm tối ưu Pareto: chất lượng tương đương toàn bộ AI nhưng tốc độ tiệm cận thuật toán cổ điển.

### 2.3. Đối với RQ3 (Recovery — Cơ chế phục hồi khi Matcher bế tắc)

Khi cả Classical Matcher lẫn Learned Matcher đều không tìm đủ số lượng match tin cậy (ví dụ drone xoay $90^\circ$ đột ngột làm mất dấu hoàn toàn):

- Tín hiệu fail từ Matcher kích hoạt 1 trong 3 cơ chế ứng phó:
  1. **Frame Rejection:** Huỷ frame hiện tại, không ghép vào canvas để tránh làm "nhiễm độc" ma trận tích luỹ $H_{0 \to t}$.
  2. **Keyframe Rematching:** Yêu cầu Matcher thử so khớp ngược về một Keyframe lịch sử trong bộ nhớ thay vì frame $t-1$.
  3. **Submosaic Splitting:** Đóng cụm bản đồ con hiện tại, mở cụm mosaic mới để ngắt đứt chuỗi tích luỹ lỗi.

---

## 3. Bảng so sánh các Detector và Matcher trong thực nghiệm dự án

| Thành phần                | Đại diện tiêu biểu          | Ưu điểm                                           | Nhược điểm                                      | Vai trò trong dự án                             |
| ------------------------- | --------------------------- | ------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- |
| **Detector cổ điển**      | FAST (ORB), DoG (SIFT)      | Chạy CPU cực nhanh, không cần GPU                 | Kém ở cảnh thiếu sáng, mờ chuyển động           | Khai thác ở baseline và tầng phân luồng nhẹ     |
| **Detector học sâu**      | SuperPoint                  | Bắt điểm ổn định ở ảnh mờ, bề mặt lặp             | Cần mạng nơ-ron inference                       | Phục vụ tầng khớp khó của Learned Matcher       |
| **Matcher cổ điển**       | BFMatcher, FLANN            | Rất nhẹ, thuật toán tất định                      | Dễ nối nhầm khi hoa văn lặp lại                 | Bộ khớp mặc định Tầng 1 (RQ2)                   |
| **Learned Matcher**       | LightGlue (SIFT/SuperPoint) | Hiểu ngữ cảnh toàn ảnh, lọc rác thông minh        | Tốn tài nguyên tính toán                        | Bộ khớp cứu nguy Tầng 2 khi cảnh báo rủi ro cao |
| **Detector-free Matcher** | EfficientLoFTR              | Khớp trực tiếp từ lưới pixel, không cần keypoints | Dễ nối điểm "ma" ở rìa ngoài, sai lệch tích luỹ | Thử nghiệm đối chứng tìm điểm gãy bản đồ        |

---

## 4. Tóm gọn ghi nhớ

- **Detector** trả lời câu hỏi: _"Điểm đặc trưng nằm ở đâu trên ảnh?"_ $\to$ Cung cấp tín hiệu độ bao phủ không gian cho **RQ1**.
- **Matcher** trả lời câu hỏi: _"Điểm nào ở ảnh 1 ứng với điểm nào ở ảnh 2?"_ $\to$ Là hạt nhân phân luồng chất lượng/tốc độ của **RQ2** và kích hoạt phục hồi cho **RQ3**.
