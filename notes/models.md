# Danh sách các mô hình và cấu hình chạy thử nghiệm

Tài liệu đặc tả các mô hình học sâu và cấu hình được đưa vào chạy thử nghiệm theo `RDR-0006`, phục vụ nghiên cứu **Failure-Aware UAV Mosaicking** (trọng tâm RQ2).

---

## 1. Nguyên tắc sử dụng mô hình

Bám sát chỉ đạo tại `RDR-0004` và `RDR-0006`:
- **100% Pretrained Weights:** Chỉ kéo checkpoint chính thức có sẵn, đóng băng trọng số (frozen), **không train lại hay fine-tune**.
- **Không suy diễn trước kết quả:** Các thông số tốc độ/FPS trong paper là trên phần cứng của tác giả; toàn bộ phải được đo lại thực tế trên NPU Drone-Map.
- **Môi trường chạy:** Google Colab / Kaggle (GPU T4) và kiểm tra khả năng chạy CPU trên laptop.

---

## 2. Chi tiết các cấu hình chạy thử

### 2.1. Nhóm Baseline truyền thống (Tầng 1)
- **SIFT + BF/FLANN:** Mốc đối chứng chuẩn về độ chính xác hình học cổ điển (OpenCV).
- **ORB + BF (Hamming):** Mốc đối chứng tốc độ nhanh nhất trên CPU.

### 2.2. Nhóm Learned Matcher dự phòng (Tầng 2 — Trọng tâm RQ2)
- **SIFT + LightGlue (ICCV 2023 — CVG ETH Zurich):**
  - *Căn cứ:* Được Kim & Kim (2025) đánh giá là phương án ổn định nhất trên tập UAV thử nghiệm (đặc biệt trong cảnh xoay lớn và ít chi tiết).
  - *Lưu ý kỹ thuật:* Dùng wrapper `lightglue.SIFT` chính thức (mặc định chuyển sang RootSIFT, nạp kèm scale và orientation cho positional encoding của LightGlue).
- **SuperPoint + LightGlue:**
  - *Đặc điểm:* Thay thế toàn diện cả khâu trích xuất (CNN SuperPoint) lẫn so khớp (LightGlue Transformer). Dùng làm đối chứng xem việc đổi detector có vượt trội hơn SIFT + LightGlue trên video drone hay không.
  - *Bản quyền:* SuperPoint tuân thủ giấy phép nghiên cứu phi thương mại của Magic Leap.

### 2.3. Nhóm Learned Baseline siêu nhẹ (Kiểm chứng giả thuyết RQ2)
- **XFeat + MNN (CVPR 2024 — Potje et al., VeRLab / UFMG):**
  - Mạng CNN nhẹ trích xuất đặc trưng 64 chiều và match sparse bằng Mutual Nearest Neighbors (MNN). Chạy được CPU thực tế.
- **XFeat + LighterGlue:**
  - Phiên bản LightGlue thu nhỏ do nhóm tác giả XFeat huấn luyện riêng cho đặc trưng XFeat.
  - *Vai trò:* Cấu hình then chốt để đối chứng: nếu chạy một model learned siêu nhẹ mọi lúc (always-lightweight) có chi phí và chất lượng tốt hơn cơ chế phân luồng classical-first hay không.

### 2.4. Nhóm Thử nghiệm thăm dò có giới hạn (Detector-free)
- **Efficient LoFTR (CVPR 2024 — ZJU3DV):**
  - Mô hình semi-dense không dùng detector cục bộ (detector-free), trích xuất liên kết trực tiếp từ tương quan ngữ cảnh.
  - *Phạm vi:* Chỉ dùng thử nghiệm trên số ít cặp frame khó mà các detector sparse thất bại hoàn toàn, nhằm phân biệt lỗi do mất keypoint hay lỗi do khâu matching.

---

## 3. Bảng tổng hợp cấu hình chạy thử

| Cấu hình | Nhóm phương pháp | Detector | Matcher | Vai trò trong RQ2 | Môi trường mục tiêu |
|---|---|---|---|---|---|
| **ORB + BF** | Cổ điển | ORB (OpenCV) | BFMatcher Hamming | Tầng 1: Tốc độ tối đa | CPU laptop |
| **SIFT + BF/FLANN** | Cổ điển | SIFT (OpenCV) | BF / FLANN L2 | Tầng 1: Chuẩn hình học cổ điển | CPU laptop |
| **SIFT + LightGlue** | Lai (Hybrid) | RootSIFT | LightGlue (`sift`) | Tầng 2: Fallback chính | Colab GPU / CPU |
| **SuperPoint + LightGlue** | Deep Learning | SuperPoint | LightGlue (`superpoint`) | Tầng 2: Đối chứng sparse toàn diện | Colab GPU |
| **XFeat + MNN** | Deep Learning | XFeat sparse | MNN | Đối chứng: Always-learned nhẹ | Colab GPU / CPU |
| **XFeat + LighterGlue** | Deep Learning | XFeat sparse | LighterGlue | Đối chứng: Learned nhẹ + matcher | Colab GPU |
| **Efficient LoFTR** | Deep Learning | Không (Detector-free) | Linear Transformer | Thăm dò cặp frame mất điểm cục bộ | Colab GPU |

---

## 4. Kế hoạch triển khai mã nguồn

1. **Bước 1 (Mô-đun hoá):** Xây dựng interface chuẩn `match_pair(img0, img1, method, **cfg)` trong `src/matcher/`.
2. **Bước 2 (Pilot test):** Chạy thử từng cấu hình trên tập mẫu nhỏ (~100–200 cặp frame) trích từ các sequence đa dạng của NPU Drone-Map.
3. **Bước 3 (Ghi nhận số liệu):** Đo đạc đồng thời tỷ lệ inliers, RMSE reprojection, thời gian (tính cả chi phí gate nếu dùng routing) và bộ nhớ tiêu thụ trên cùng một máy để đưa ra kết luận công bằng.
