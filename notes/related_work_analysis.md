# Phân tích chuyên sâu các công trình liên quan (Related Work Analysis)

Tài liệu này hệ thống hoá toàn diện các nghiên cứu liên quan đến đề tài **Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking**, làm rõ công nghệ cốt lõi của từng bên, chỉ rõ khoảng trống nghiên cứu (research gap) và đưa ra luận điểm cùng bằng chứng thực nghiệm chứng minh giải pháp của nhóm vượt trội.

---

## 1. Bức tranh tổng quan và 4 mảng bài toán

Nghiên cứu của nhóm giải quyết bài toán ghép ảnh 2D từ video UAV không có ground truth định vị tuyệt đối (GNSS/IMU chính xác cao) qua 4 mảng kỹ thuật:
1. **Ghép ảnh UAV gia tăng (Incremental UAV Mosaicking):** Luồng ghép tuần tự từ frame sang frame.
2. **Dự báo lỗi đăng ký (Failure Prediction & Uncertainty - RQ1):** Dự báo sớm bước ghép hỏng bằng chỉ báo rẻ.
3. **Phân luồng đối sánh đặc trưng (Matcher Routing & Resource Trade-off - RQ2):** Cân bằng chất lượng bản đồ và độ trễ tính toán.
4. **Cơ chế phục hồi sau suy biến (Error Recovery Policies - RQ3):** Khống chế lan truyền lỗi (drift cascade) khi phát hiện bước ghép hỏng.

---

## 2. Phân tích chi tiết từng mảng

### Mảng 1: Ghép ảnh UAV gia tăng (Incremental UAV Mosaicking & Baselines)

#### A. Người khác đang làm thế nào & Công nghệ sử dụng
- **Hwang et al. (2026) [Applied Sciences]:**
  - *Công nghệ:* Pipeline tuần tự trên CPU dùng ORB/SIFT kết hợp bộ đối sánh FLANN/Brute-Force Matcher và thuật toán RANSAC để ước lượng homography $3 \times 3$. Dùng ngưỡng số lượng inlier cố định (fixed inlier threshold) để chấp nhận hoặc bác bỏ một frame mới.
- **Li et al. (2023) [Remote Sensing]:**
  - *Công nghệ:* Ghép video gia tăng dựa trên tối ưu hoá sai số chiếu lại có trọng số (weighted reprojection error optimization). Sử dụng thuật toán chọn keyframe dựa trên độ đè phủ quang học và cơ chế kết nối lại (rematch) với keyframe lịch sử trong quá khứ khi quỹ đạo bị trôi dạt.
- **Kim & Kim (2025) [ISPRS Archives]:**
  - *Công nghệ:* Kết hợp trích xuất đặc trưng cổ điển (SIFT) với mạng nơ-ron đồ thị Transformer (LightGlue) để giải quyết các cặp ảnh UAV có góc xoay lớn và vùng nghèo vân bề mặt.
- **Chen et al. (2022) [Remote Sensing]:**
  - *Công nghệ:* Tối ưu hoá đường nối ghép (optimal seamline) bằng quy hoạch động kết hợp phép biến đổi nửa xạ ảnh (half-projective warp) nhằm giảm biến dạng hình học khi cảnh có độ cao thay đổi.
- **Kharismawati & Kazic (2025) [DroneZaic, Plant Phenome J.]:**
  - *Công nghệ:* Ghép video UAV nông nghiệp sử dụng trường dòng quang học dày đặc (Farneback Dense Optical Flow) và thuật toán phân cụm không gian để gom frame thành các mảnh con (submosaics).
- **Bu et al. (2016) [Map2DFusion, IEEE/RSJ IROS]:**
  - *Công nghệ:* Kết hợp direct tracking mức pixel (Lucas-Kanade) với đồ thị keyframe và tối ưu hoá bundle adjustment 2D cục bộ.

#### B. Họ đang thiếu sót gì? (Research Gaps)
1. **Hoạt động "mù" rủi ro (Risk-Blind Execution):** Các hệ thống hoặc chọn hoàn toàn thuật toán cổ điển nhẹ (dễ chết khi gặp địa hình lặp như đồng cỏ, ruộng lúa, mặt nước hoặc khi drone quay đổi hướng đột ngột), hoặc chạy toàn bộ bằng mạng nơ-ron sâu (quá nặng, tiêu tốn bộ nhớ và thời gian, không thể chạy trọn chuyến bay trên laptop/máy bay không người lái).
2. **Cổng lọc kiểm duyệt thô sơ và tĩnh:** Hwang et al. và Li et al. dựa vào các ngưỡng cố định như $N_{\mathrm{inliers}} > K$ hoặc sai số chiếu lại trung bình $\mathrm{RMSE} < \epsilon$. Họ ngầm giả định rằng "nhiều inlier là homography đúng", bỏ qua việc RANSAC dễ dàng hội tụ vào các cấu trúc lặp sai lệch (vân cỏ, ngói nhà).
3. **Thiếu sự so sánh công bằng giữa các chiến lược phục hồi:** Mỗi bài báo chỉ đưa ra một giải pháp riêng lẻ (bỏ frame, rematch keyframe, hay tách submosaic) mà không đo lường định lượng trên cùng một chuẩn kích hoạt xem chiến lược nào bảo toàn được bản đồ tốt nhất.

#### C. Nhóm chứng minh tốt hơn thế nào?
- **Giải pháp:** Xây dựng pipeline 2 tầng nhận biết rủi ro (Failure-Aware): tầng nhẹ (SIFT-640) chạy mặc định; chỉ leo thang (escalate) lên tầng sâu (SuperPoint + LightGlue) hoặc tăng độ phân giải khi chỉ báo rủi ro vượt ngưỡng.
- **Bằng chứng thực nghiệm:**
  - Tiết kiệm **75,8%** thời gian tính toán so với việc chạy toàn bộ bằng mô hình học sâu (13,3 giây so với 54,9 giây ở chuỗi `village`).
  - Đạt độ trôi dạt tích luỹ cuối cùng là **28,5 px**, vượt trội hơn cả việc chạy thuần cổ điển (75,3 px) và chạy thuần learned matcher (82,4 px).

---

### Mảng 2: RQ1 — Dự báo lỗi đăng ký & Ước lượng độ bất định (Failure Prediction)

#### A. Người khác đang làm thế nào & Công nghệ sử dụng
- **Zaffar et al. (2024) [CVPR] & Sferrazza et al. (2024) [CVPRW]:**
  - *Công nghệ:* Đánh giá độ tin cậy đối sánh trên 18 pipeline thị giác máy tính cho bài toán nhận diện vị trí (Visual Place Recognition - VPR). Sử dụng số lượng inlier ($N_{\mathrm{inlier}}$), tỉ lệ inlier ($R_{\mathrm{inlier}}$) từ RANSAC/MAGSAC++ để phân loại cặp ảnh thành công hay thất bại.
- **Barath et al. (2023) [CVPR] & Yuan et al. (2024) [J. Imaging]:**
  - *Công nghệ:* Khảo sát quy mô lớn (benchmark HEB và 1,95 triệu lượt đăng ký), đánh giá mối tương quan giữa sai số chiếu lại (Reprojection Error), mật độ điểm đặc trưng và sai số hình học ground truth.
- **Xiao & Loianno (2025) [UASTHN, arXiv]:**
  - *Công nghệ:* Mạng Deep Homography kết hợp ước lượng độ bất định (aleatoric/epistemic uncertainty) cho nhiệm vụ định vị UAV qua ảnh nhiệt và ảnh vệ tinh.
- **Ivashechkin et al. (2021) [VSAC, ICCV]:**
  - *Công nghệ:* Thuật toán ước lượng độc lập VSAC, áp dụng thống kê phân bố mẫu để kiểm tra tính độc lập và chấm điểm chất lượng inliers.

#### B. Họ đang thiếu sót gì? (Research Gaps)
1. **Thiếu nhãn sai số cấp bước trong chuỗi tích luỹ UAV:** Các công trình trên đánh giá lỗi trên từng cặp ảnh độc lập (pair-wise) trong bối cảnh nhận diện địa điểm (VPR) với nhãn 3D/GPS, chưa từng nghiên cứu tác động của sai số cấp bước ($e_i$) dẫn đến hiện tượng trôi dạt tích luỹ (cumulative drift) trong chuỗi video ghép ảnh liên tục.
2. **Ảo tưởng về số inlier (Inlier Count Illusion):** Các nghiên cứu prior art mặc định xem số inlier là thước đo độ tin cậy. Tuy nhiên, trên ảnh UAV có địa hình đồng nhất (đồng cỏ, ruộng lúa), RANSAC thường xuyên tìm thấy hàng trăm inlier khớp giả giữa các gợn cỏ ngẫu nhiên; sai số chiếu lại nội tại vẫn rất nhỏ ($< 1$ px) nhưng ma trận homography bị xoay lệch hoàn toàn (lỗi hình học thực tế lên đến 5 - 313 px/bước).

#### C. Nhóm chứng minh tốt hơn thế nào?
- **Phương pháp đo đạc:** Thiết lập thước đo sai số cấp bước độc lập ($e_i$) đối chiếu với matcher tham chiếu chất lượng cao ($H_i^{\mathrm{ref}}$ có cổng lọc tối thiểu 100 inliers). Đánh giá 8 chỉ báo chi phí thấp bằng hệ số tương quan hạng Spearman ($\rho$) và diện tích dưới đường cong ROC (AUC).
- **Phát hiện thực nghiệm và chứng minh:**
  - **Kết quả phủ định quan trọng (Negative Result):** Chỉ ra số lượng matches ($N_{\mathrm{match}}$) và số inliers ($N_{\mathrm{inlier}}$) hoàn toàn phản tác dụng trong việc dự báo sai số cấp bước (AUC thực tế $< 0,5$, lần lượt là 0,402 và 0,409).
  - **Chỉ báo vượt trội:** Nhóm chứng minh chỉ báo độ tương quan tương đồng chuẩn hoá vùng đè phủ sau khi biến đổi (Overlap Patch NCC - $\tau_{\mathrm{ncc}}$) đạt AUC vượt trội (**0,770** trên `village` và **0,855** trên `grass`). Bằng chứng định lượng này chỉ ra rằng kiểm tra tính nhất quán quang học sau biến đổi hình học đáng tin cậy hơn nhiều so với việc đếm số điểm đặc trưng.

---

### Mảng 3: RQ2 — Phân luồng đối sánh & Tối ưu tài nguyên (Matcher Routing)

#### A. Người khác đang làm thế nào & Công nghệ sử dụng
- **DeTone et al. (2018) [SuperPoint, CVPRW]:** CNN trích xuất điểm đặc trưng và vector mô tả tự giám sát.
- **Lindenberger et al. (2023) [LightGlue, ICCV]:** Mạng nơ-ron đồ thị (GNN) với cơ chế chú ý Transformer (Self/Cross-Attention), tích hợp cơ chế thoát sớm (early-exit) và độ sâu tương thích (adaptive depth) để giảm tính toán ở các cặp ảnh dễ.
- **Sun et al. (2021) [LoFTR, CVPR] & Wang et al. (2024) [Efficient LoFTR, CVPR]:** Transformer đối sánh không cần detector (detector-free), kết hợp kim tự tháp đặc trưng CNN và cơ chế lọc token QuadTree để giảm độ phức tạp tính toán.
- **Potlapalli et al. (2024) [XFeat, CVPR]:** Mạng học sâu trích xuất và đối sánh siêu nhẹ tối ưu riêng cho CPU (~27 FPS).
- **Zhang et al. (2025) [DALGlue, Nature SciReports]:** Cơ chế Deformable Attention chuyên biệt cho biến dạng địa hình phức tạp trên ảnh viễn thám / UAV.
- **Gaisbauer et al. (2025) [ISPRS Annals]:** Thực nghiệm đo lường so sánh có hệ thống giữa phương pháp cổ điển và học sâu trên dữ liệu máy bay không người lái.

#### B. Họ đang thiếu sót gì? (Research Gaps)
1. **Tư duy "Được ăn cả, ngã về không" (All-or-Nothing Deployment):** Các nghiên cứu mô hình sâu chỉ đo lường thời gian xử lý trên từng cặp ảnh riêng biệt. Khi triển khai vào hệ thống thực tế, họ ép toàn bộ luồng xử lý phải chạy qua mô hình nặng, khiến việc xử lý trên thiết bị bay hoặc máy tính cá nhân bị nghẽn cổ chai nghiêm trọng.
2. **Ảo giác sai số của mô hình bán dày (Semi-dense Degeneration):** Các mô hình như LoFTR hay Efficient LoFTR dù có sai số chiếu lại nội tại rất nhỏ trên tập dữ liệu chuẩn, nhưng khi gặp địa hình UAV đồng nhất lặp (như chuỗi `grass`), chúng sinh ra hàng loạt tương ứng sai lệch trên toàn khung hình, làm vỡ hoàn toàn quỹ đạo ghép (sai số lên đến 313 px/bước).
3. **Chạy mô hình mạnh mọi nơi làm bản đồ tệ hơn:** Chưa có công trình nào phát hiện và định lượng hiện tượng: việc ép buộc chạy mô hình sâu mạnh trên mọi bước có thể tích luỹ drift lớn hơn cả mô hình cổ điển trên chuỗi bay UAV thực tế.

#### C. Nhóm chứng minh tốt hơn thế nào?
- **Phương pháp phân luồng:** Bộ định tuyến rủi ro (Risk-based Router) kích hoạt 2 tầng theo ngân sách leo thang định trước ($\le 25\%$ số bước).
- **Bằng chứng định lượng trực tiếp:**
  - Chạy toàn bộ bằng SIFT: Tốn 3,0 giây tính toán, drift cuối chuỗi là **75,3 px**.
  - Chạy toàn bộ bằng mô hình mạnh (SuperPoint + LightGlue): Tốn tới 54,9 giây tính toán, nhưng drift cuối chuỗi lên tới **82,4 px** (vừa chậm gấp 18 lần, vừa làm méo bản đồ nặng hơn).
  - Phân luồng rủi ro của nhóm ($\tau_{\mathrm{ncc}} = 0,93$): Chỉ leo thang **16%** số bước khó, thời gian xử lý chỉ **13,3 giây**, nhưng drift cuối chuỗi giảm ngoạn mục xuống còn **28,5 px** (giảm 62,1% sai số so với SIFT thuần và giảm 65,4% so với mô hình mạnh thuần).

---

### Mảng 4: RQ3 — Cơ chế phục hồi sau suy biến (Recovery Policies)

#### A. Người khác đang làm thế nào & Công nghệ sử dụng
- **Hwang et al. (2026):** Cơ chế loại bỏ frame (Frame Dropping) — nếu frame $i$ không khớp được với $i-1$, frame đó bị vứt bỏ hoàn toàn.
- **Li et al. (2023):** Cơ chế đối sánh lại với keyframe (Keyframe Rematching) — khi khớp với frame liền trước thất bại, tìm kiếm ngược dòng thời gian để ghép nối với một keyframe đã đặt trước đó.
- **Kharismawati & Kazic (2025):** Cơ chế phân cụm và tách mảnh (Submosaic Splitting) — chia video thành các cụm độc lập khi phát hiện đứt gãy.

#### B. Họ đang thiếu sót gì? (Research Gaps)
1. **Hiện tượng sụp đổ dây chuyền (Cascade Failure):** Khi loại bỏ một frame hoặc cố gắng nhảy cóc để rematch với keyframe cũ, khoảng cách không gian và góc nhìn giữa frame hiện tại và frame tham chiếu bị kéo giãn ra. Hậu quả là frame tiếp theo càng khó khớp hơn, dẫn đến phản ứng dây chuyền: một vài bước lỗi ban đầu làm vứt bỏ phần lớn video (cascade).
2. **Thiếu đánh giá định lượng so sánh:** Chưa có công trình nào đặt 3 cơ chế này lên cùng một bàn cân, dưới cùng một ngưỡng phát hiện lỗi rủi ro để đo lường tỷ lệ giữ frame và độ trôi dạt bản đồ.

#### C. Nhóm chứng minh tốt hơn thế nào?
- **Phương pháp thử nghiệm:** Đặt cả 3 chiến lược (Bỏ frame · Rematch keyframe · Tách submosaic) vào cùng pipeline online và cùng ngưỡng kích hoạt rủi ro $\tau_{\mathrm{ncc}} = 0,93$.
- **Bằng chứng định lượng:**
  - Cơ chế Bỏ frame (Drop Frame) và Rematch Keyframe: Bị sụp đổ dây chuyền, chỉ giữ được **14/46 frame** (mất tới 69,6% dữ liệu của chuyến bay do 7 bước lỗi ban đầu kích hoạt dây chuyền làm hỏng 32 bước tiếp theo).
  - Cơ chế Tách Submosaic của nhóm: **Giữ trọn vẹn 46/46 frame** (chia thành 8 mảnh con sạch không bị méo hình học), đồng thời khống chế độ trôi dạt tối đa của từng mảnh chỉ ở mức **21,7 px**.

---

## 3. Bảng tổng hợp đối đầu (Head-to-Head Comparison Matrix)

| Chiều so sánh | Các nghiên cứu hiện tại (Prior Art) | Công nghệ chính | Hạn chế cốt tử | Giải pháp của nhóm (This Work) | Bằng chứng vượt trội định lượng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Pipeline tích luỹ** | Hwang (2026), Li (2023), Kim (2025) | SIFT/ORB + RANSAC; SIFT+LightGlue | Mù rủi ro; hoặc quá yếu (dễ vỡ) hoặc quá nặng (sập thiết bị). | Phân luồng rủi ro 2 tầng (SIFT mặc định, LightGlue dự phòng). | Giảm **75,8%** thời gian so với deep model; giảm **62,1%** drift so với SIFT. |
| **Chỉ báo lỗi (RQ1)** | Zaffar (2024), Sferrazza (2024), Barath (2023) | Đếm inliers ($N_{\mathrm{inlier}}$), tỉ lệ inlier, Reprojection Error | Đánh giá cặp ảnh tĩnh VPR; inlier giả trên địa hình lặp gây ngộ nhận. | Đo sai số cấp bước thật ($e_i$); dùng Patch NCC ($\tau_{\mathrm{ncc}}$). | $N_{\mathrm{inlier}}$ phản tác dụng (AUC 0,409); Patch NCC đạt AUC cao (**0,770 – 0,855**). |
| **Phân luồng matcher (RQ2)** | Lindenberger (2023), Wang (2024), Potlapalli (2024) | LightGlue, Efficient LoFTR, XFeat | All-or-nothing; deep model chạy mọi bước gây drift cao hơn cổ điển. | Matcher Router kích hoạt theo ngưỡng $\tau_{\mathrm{ncc}}$ với ngân sách $\le 25\%$. | Drift **28,5 px** (tốt hơn chạy toàn bộ LightGlue: 82,4 px và SIFT: 75,3 px). |
| **Phục hồi suy biến (RQ3)** | Hwang (2026), Li (2023), Kharismawati (2025) | Bỏ frame đơn lẻ; Rematch keyframe lịch sử | Sụp đổ dây chuyền (cascade failure); làm mất phần lớn video. | So sánh 3 chính sách dưới cùng một ngưỡng kích hoạt $\tau$; ưu tiên tách submosaic. | Tách submosaic giữ **46/46 frame** (drift 21,7 px); bỏ frame/rematch mất **32/46 frame**. |

---

## 4. Hướng dẫn tích hợp vào bản thảo bài báo (`main.tex` / `main_vi.tex`)

Khi đưa nội dung này vào Section II của bài báo IEEE, tuân thủ các nguyên tắc:
1. **Nêu đích danh công nghệ:** Ghi rõ từng nhóm tác giả dùng thuật toán gì (ví dụ: Farneback Optical Flow, SuperPoint+LightGlue GNN, LoFTR QuadTree token selection, RANSAC inlier thresholding).
2. **Nhấn mạnh rõ 3 câu hỏi:**
   - Người khác đang làm gì với công nghệ nào?
   - Họ gặp giới hạn gì khi áp dụng vào chuỗi video UAV gia tăng?
   - Nhóm kiểm chứng và chứng minh vượt trội bằng thước đo và số liệu thực nghiệm nào?
3. **Quy tắc văn phong IEEE:** Tuyệt đối không dùng dấu gạch dài em dash; giữ câu từ kỹ thuật, trực diện, bằng chứng đi trước kết luận.
