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

## 5. Pilot đã chạy (2026-10-13)

- `notebooks/02_lightglue_pilot.ipynb` chạy 2 cấu hình LightGlue ở **độ phân giải gốc 1920×1080, không resize**: 3 cặp đầu (`metrics.json` + ảnh nối điểm) và **mosaic 20 frame ở độ phân giải gốc** (`mosaic_sift/`, `mosaic_superpoint/`). Dùng để đối chiếu ảnh hưởng của độ phân giải với notebook 03 (chạy 640 px).
- `notebooks/03_all_models.ipynb` chạy cả 7 cấu hình, **toàn bộ code nằm trong notebook** (adapter, pipeline, sinh báo cáo, kiểm tra) — không cần file `.py`; chưa chuyển thành package `src/matcher/`.
- Notebook 03 có **hai tầng**: `pairs/` đo chất lượng khớp cặp frame (3 cặp đầu/sequence), `mosaic/` nối chuỗi 20 frame đầu rồi warp/blend ra bảng đồ hoàn chỉnh cho từng cấu hình. Blend dùng cùng cách với notebook 01 để so sánh được.
- **Phát hiện đáng chú ý (mosaic tầng 2, village + grass):** cả 7 cấu hình đều báo ghép đủ 20/20 frame, nhưng **EfficientLoFTR cho mosaic hỏng** — canvas bị kéo giãn chéo (1465×626 so với ~650×600 của các cấu hình khác) và chỉ phủ 55,6% canvas (village), 73,4% (grass). Ảnh mosaic xác nhận bị trượt/kéo xiên. Đây là **ca lỗi thật đầu tiên**: từng cặp đều có H "hợp lệ" (2.655–3.040 matches, 2.096+ inliers, RMSE inlier thấp) mà bản đồ vẫn vỡ ⇒ bằng chứng trực tiếp rằng **inlier count/ratio và RMSE inlier không đủ để kết luận ghép đúng**, và sai số tích luỹ mới là vấn đề (đúng tiền đề RQ1/RQ3).
- **Xác nhận định lượng bằng metric drift (`RDR-0007`, Notebook 04 mục 8–10):** sai số vòng chain-vs-direct cho `efficientloftr` **1311,5 px** ở `village` (gấp **28 lần** mức nền SIFT 46,7 px) và **62,9 px** ở `grass` (gấp **37 lần** mức nền 1,7 px). 6 mô hình còn lại nằm sát mức nền (39,7–73,2 px ở `village`) nên **chưa đủ cơ sở xếp hạng** chúng.
- Mosaic của 6 cấu hình còn lại đều phủ 95,9–99,6% canvas và nhìn liền mạch khi kiểm tra bằng mắt (sift_bf, orb_bf, xfeat_lighterglue đã xem trực tiếp).
- Cùng ảnh xử lý 640 × 352, CPU 4 threads, sparse tối đa 2.000 keypoints, RANSAC 3 px; EfficientLoFTR semi-dense không giới hạn 2.000 điểm.
- EfficientLoFTR dùng bản Transformers `zju-community/efficientloftr`, được README chính thức giới thiệu. Revision model và nguồn XFeat/LightGlue ghi trong manifest.
- Cài: `uv pip install -r requirements_learned.txt`. Chọn kernel `.venv` rồi Run All notebook 03.
- `notebooks/outputs/` (gitignore) có một trang vào duy nhất `index.html`, phẳng một cấp, mỗi notebook một thư mục cùng tên: `01_classical_baseline/<sequence>/`, `02_lightglue_pilot/<sequence>/`, `03_all_models/<UTC>/…` (trong đó có `pairs/` và `mosaic/`). Không lồng `outputs/notebooks/notebooks/`, không còn thư mục trung gian tên `runs/`. Ghi đè tên file phải sửa writer, không xoá thư mục.
- Mở `notebooks/outputs/index.html`; từng run có `index.html`, `summary.csv` (tầng cặp), `mosaic_summary.csv` (tầng mosaic), `manifest.json`, `pairs/<sequence>/<model>/` và `mosaic/<sequence>/<model>/{mosaic.png,metrics.json}`.
- Sinh lại trang báo cáo mà không chạy lại inference: gọi `rebuild("<thư-mục-run>")` trong cell báo cáo của notebook 03.
- JSON tầng cặp ghi H từ ảnh sau sang ảnh trước ở hệ pixel đã resize; NPZ giữ correspondences/inlier mask. JSON tầng mosaic ghi `H_to_mosaic` (đã gồm scale + tịnh tiến canvas), kích thước canvas, `canvas_covered_fraction`, chuỗi cặp và lý do dừng nếu có.
- **Chưa đo drift**: chưa đối chiếu `trajectory.txt`. `canvas_covered_fraction` là tỷ lệ pixel canvas có ảnh, không phải diện tích mặt đất.
- Timing sau warmup gồm preprocessing/extraction/matching/chuyển điểm về CPU; không gồm tải model, đọc file, RANSAC, vẽ ảnh. Lặp lại cùng cấu hình cho kết quả khác nhau (ví dụ EfficientLoFTR 1,4–2,1 s tuỳ lần chạy), nên không được so trực tiếp với timing notebook 01/02 ở độ phân giải khác.
- Chưa đo peak RAM/VRAM, chưa đánh giá bằng ground truth và chưa kết luận chất lượng/routing. Trên 3 cặp grass này classical cũng thành công; không được suy diễn LightGlue đã “cứu” classical.
- Kiểm tra hình học tối thiểu nay nằm ở cell cuối notebook 03 (hướng H, ca thiếu correspondence, đủ 7 cấu hình, JSON nghiêm ngặt); chạy tự động khi Run All.
