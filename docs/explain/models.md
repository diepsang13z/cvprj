# Danh sách các mô hình và cấu hình chạy thử nghiệm

Tài liệu đặc tả các mô hình học sâu và cấu hình được đưa vào chạy thử nghiệm theo `RDR-0006`, phục vụ nghiên cứu **Failure-Aware UAV Mosaicking** (trọng tâm RQ2).

---

## 1. Nguyên tắc sử dụng mô hình

Bám sát chỉ đạo tại `RDR-0004` và `RDR-0006`:

- **100% Pretrained Weights:** Chỉ kéo checkpoint chính thức có sẵn, đóng băng trọng số (frozen), **không train lại hay fine-tune**.
- **Không suy diễn trước kết quả:** Các thông số tốc độ/FPS trong paper là trên phần cứng của tác giả; toàn bộ phải được đo lại thực tế trên NPU Drone-Map.
- **Môi trường chạy:** Google Colab / Kaggle (GPU T4/A100) hosted cloud runtimes (`RULES.md §8`, `RDR-0010`). Tuyệt đối cấm chạy inference hoặc pipeline thực nghiệm trên CPU laptop cá nhân.
---

## 2. Chi tiết các cấu hình chạy thử

### 2.1. Nhóm Baseline truyền thống (Tầng 1)

- **SIFT + BF/FLANN:** Mốc đối chứng chuẩn về độ chính xác hình học cổ điển (OpenCV).
- **ORB + BF (Hamming):** Mốc đối chứng tốc độ nhanh nhất trên CPU.

### 2.2. Nhóm Learned Matcher dự phòng (Tầng 2 — Trọng tâm RQ2)

- **SIFT + LightGlue (ICCV 2023 — CVG ETH Zurich):**
  - _Căn cứ:_ Được Kim & Kim (2025) đánh giá là phương án ổn định nhất trên tập UAV thử nghiệm (đặc biệt trong cảnh xoay lớn và ít chi tiết).
  - _Lưu ý kỹ thuật:_ Dùng wrapper `lightglue.SIFT` chính thức (mặc định chuyển sang RootSIFT, nạp kèm scale và orientation cho positional encoding của LightGlue).
- **SuperPoint + LightGlue:**
  - _Đặc điểm:_ Thay thế toàn diện cả khâu trích xuất (CNN SuperPoint) lẫn so khớp (LightGlue Transformer). Dùng làm đối chứng xem việc đổi detector có vượt trội hơn SIFT + LightGlue trên video drone hay không.
  - _Bản quyền:_ SuperPoint tuân thủ giấy phép nghiên cứu phi thương mại của Magic Leap.

### 2.3. Nhóm Learned Baseline siêu nhẹ (Kiểm chứng giả thuyết RQ2)

- **XFeat + MNN (CVPR 2024 — Potje et al., VeRLab / UFMG):**
  - Mạng CNN nhẹ trích xuất đặc trưng 64 chiều và match sparse bằng Mutual Nearest Neighbors (MNN). Chạy được CPU thực tế.
- **XFeat + LighterGlue:**
  - Phiên bản LightGlue thu nhỏ do nhóm tác giả XFeat huấn luyện riêng cho đặc trưng XFeat.
  - _Vai trò:_ Cấu hình then chốt để đối chứng: nếu chạy một model learned siêu nhẹ mọi lúc (always-lightweight) có chi phí và chất lượng tốt hơn cơ chế phân luồng classical-first hay không.

### 2.4. Nhóm Thử nghiệm thăm dò có giới hạn (Detector-free)

- **Efficient LoFTR (CVPR 2024 — ZJU3DV):**
  - Mô hình semi-dense không dùng detector cục bộ (detector-free), trích xuất liên kết trực tiếp từ tương quan ngữ cảnh.
  - _Phạm vi:_ Chỉ dùng thử nghiệm trên số ít cặp frame khó mà các detector sparse thất bại hoàn toàn, nhằm phân biệt lỗi do mất keypoint hay lỗi do khâu matching.

---

## 3. Bảng tổng hợp cấu hình chạy thử

| Cấu hình                   | Nhóm phương pháp | Detector              | Matcher                  | Vai trò trong RQ2                  | Môi trường mục tiêu |
| -------------------------- | ---------------- | --------------------- | ------------------------ | ---------------------------------- | ------------------- |
| **ORB + BF**               | Cổ điển          | ORB (OpenCV)          | BFMatcher Hamming        | Tầng 1: Tốc độ tối đa              | Colab/Kaggle (CPU)  |
| **SIFT + BF/FLANN**        | Cổ điển          | SIFT (OpenCV)         | BF / FLANN L2            | Tầng 1: Chuẩn hình học cổ điển     | Colab/Kaggle (CPU)  |
| **SIFT + LightGlue**       | Lai (Hybrid)     | RootSIFT              | LightGlue (`sift`)       | Tầng 2: Fallback chính             | Colab/Kaggle (GPU)  |
| **SuperPoint + LightGlue** | Deep Learning    | SuperPoint            | LightGlue (`superpoint`) | Tầng 2: Đối chứng sparse toàn diện | Colab/Kaggle (GPU)  |
| **XFeat + MNN**            | Deep Learning    | XFeat sparse          | MNN                      | Đối chứng: Always-learned nhẹ      | Colab/Kaggle (GPU/CPU)|
| **XFeat + LighterGlue**    | Deep Learning    | XFeat sparse          | LighterGlue              | Đối chứng: Learned nhẹ + matcher   | Colab/Kaggle (GPU)  |
| **Efficient LoFTR**        | Deep Learning    | Không (Detector-free) | Linear Transformer       | Thăm dò cặp frame mất điểm cục bộ  | Colab/Kaggle (GPU)  |
---

## 4. Kế hoạch triển khai mã nguồn

1. **Bước 1 (Mô-đun hoá):** Xây dựng interface chuẩn `match_pair(img0, img1, method, **cfg)` trong `src/matcher/`.
2. **Bước 2 (Pilot test):** Chạy thử từng cấu hình trên tập mẫu nhỏ (~100–200 cặp frame) trích từ các sequence đa dạng của NPU Drone-Map.
3. **Bước 3 (Ghi nhận số liệu):** Đo đạc đồng thời tỷ lệ inliers, RMSE reprojection, thời gian (tính cả chi phí gate nếu dùng routing) và bộ nhớ tiêu thụ trên cùng một máy để đưa ra kết luận công bằng.

## 5. Pilot đã chạy (2026-10-13)

- `notebooks/deep_matching_pilot.ipynb` chạy 2 cấu hình LightGlue ở **độ phân giải gốc 1920×1080, không resize**: 3 cặp đầu (`metrics.json` + ảnh nối điểm) và **mosaic 20 frame** (`mosaic_sift/`, `mosaic_superpoint/`). Đã bổ sung kiểm tra số frame tối thiểu ($\ge 2$ cho warmup, $\ge 4$ cho pilot) và ghi nhận revision thực tế từ môi trường.
- `notebooks/feature_matcher_benchmark.ipynb` chạy cả 7 cấu hình ở độ phân giải 640 px với 2 chế độ `pilot` (2 sequence, 3 pairs, 20 frame) và `full` (tự động phát hiện toàn bộ sequence trong dataset, all pairs/frames).
- **Tối ưu bộ nhớ $O(1)$:** Thay thế việc nạp sẵn danh sách mảng ảnh vào RAM bằng cơ chế đọc lười theo cặp (on-demand lazy streaming) cho cả khâu match lẫn render canvas, khống chế bộ nhớ thường trực dưới ngưỡng OOM trên Google Colab.
- **Xử lý subpixel float32:** Trích xuất toạ độ ELoFTR qua `process_eloftr_matches` bảo toàn độ chính xác số thực subpixel, kèm unit self-check tự động.
- **Quan sát từ run `20261013T164937_145955Z`:** Cả 7 cấu hình ghép đủ 20/20 frame, nhưng EfficientLoFTR có canvas khác thường (1465×626 ở `village`) và phủ 55,6% / 73,4% ở `village` / `grass`. H hợp lệ và nhiều inlier không chứng minh đúng hình học; cần tách lỗi mô hình khỏi adapter/preprocessing/checkpoint trước khi quy nguyên nhân.
- **Metric từ Notebook Drift (`accumulated_drift_evaluation.ipynb`):** EfficientLoFTR có sai số vòng 1311,5 px ở `village` **frame 19**, 62,9 px ở `grass` **frame 6**; SIFT lần lượt 46,7 và 1,7 px. Tỷ số 28×/37× là so với SIFT, không phải giới hạn cho phép hoặc nhiễu độc lập.
- Sáu cấu hình còn lại phủ 95,9–99,6% canvas; tỷ lệ phủ cao không chứng minh đăng ký chính xác hoặc bản đồ không méo.
- Cùng ảnh xử lý 640 × 352, sparse tối đa 2.000 keypoints, RANSAC 3 px; EfficientLoFTR semi-dense không giới hạn 2.000 điểm. Backend ghi nhận minh bạch: `"cpu"` cho OpenCV SIFT/ORB, `"cuda"` cho deep models.
- **Cấu trúc lưu trữ độc bản UTC:** `OUTPUT_ROOT / "03_all_models" / <stamp>/` chứa `manifest.json`, `pairs/`, `mosaic/` và bảng tổng hợp CSV. Marker hoàn tất `completed.json` chỉ được xuất SAU CÙNG sau khi toàn bộ kiểm tra hình học, tính hợp lệ JSON và số lượng pair khớp tuyệt đối. Nghiêm cấm ghi đè lên thư mục run đã có marker `completed.json`.
- JSON tầng cặp ghi H từ ảnh sau sang ảnh trước ở hệ pixel đã resize; NPZ giữ correspondences/inlier mask. JSON tầng mosaic ghi `H_to_mosaic`, kích thước canvas, `canvas_covered_fraction`, `frames_stitched`, `stopped_at_pair`.
- Sai số drift được chuyển sang `notebooks/accumulated_drift_evaluation.ipynb` đo bằng phương pháp chain-vs-direct (`RDR-0007`) trên tập đối chiếu chung (common eligible frames).
