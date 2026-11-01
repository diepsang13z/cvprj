# Bảng thuật ngữ cốt lõi của dự án (Project Glossary)

Tài liệu giải thích các thuật ngữ chuyên ngành thị giác máy tính, xử lý ảnh viễn thám UAV và các khái niệm thiết kế đặc thù đang sử dụng trong dự án.

---

## 1. Thị giác máy tính & Xử lý ảnh UAV cơ bản

| Thuật ngữ (English) | Thuật ngữ (Tiếng Việt) | Giải thích & Ý nghĩa trong dự án |
|---|---|---|
| **2D Aerial Mosaicking / Image Stitching** | Ghép ảnh toàn cảnh trên không 2D | Kỹ thuật ghép chuỗi các khung hình (frames) từ camera drone thành một ảnh toàn cảnh phẳng duy nhất (orthomosaic cục bộ). |
| **Homography ($H$)** | Ma trận đồng biến phối cảnh (Phép chiếu phẳng) | Ma trận $3 \times 3$ ánh xạ toạ độ pixel từ ảnh này sang ảnh khác khi cảnh quan sát là **mặt phẳng** hoặc camera **chỉ quay quanh tâm**. |
| **Accumulated Homography ($H_{0 \to t}$)** | Ma trận Homography tích luỹ | Ma trận tích luỹ qua chuỗi phép nhân: $H_{0 \to t} = H_{0 \to 1} \times H_{1 \to 2} \times \dots \times H_{t-1 \to t}$, dùng để biến đổi trực tiếp frame $t$ về hệ toạ độ của toàn bộ bản đồ mosaic. |
| **Planar Scene Assumption** | Giả định cảnh phẳng | Giả định địa hình bên dưới tương đối bằng phẳng so với độ cao bay của drone, cho phép dùng ma trận Homography 2D thay vì phải tái tạo mô hình 3D phức tạp. |
| **Nadir / Near-nadir View** | Góc nhìn thẳng đứng (hoặc gần thẳng đứng) | Camera drone hướng thẳng góc $90^\circ$ xuống mặt đất (nadir). Góc nhìn này tối thiểu hoá hiệu ứng thị sai (parallax) và che khuất vật thể. |
| **Parallax (Thị sai)** | Sai lệch góc nhìn do độ cao địa hình | Hiện tượng các vật thể có độ cao khác nhau (nhà cửa, cây cối, khe núi) bị dịch chuyển vị trí tương đối khi drone đổi góc bay. Parallax phá vỡ giả định cảnh phẳng và gây bóng mờ/lỗi ghép. |
| **Motion Blur** | Mờ do chuyển động | Hiện tượng ảnh bị nhoè do drone bay quá nhanh, rung lắc hoặc màn trập phơi sáng lâu, làm giảm mạnh số lượng điểm đặc trưng có thể trích xuất. |
| **Warping & Blending** | Biến dạng hình học & Hoà trộn ảnh | **Warping:** Dùng $H$ uốn/chiếu ảnh vào canvas chung. **Blending:** Xử lý làm mờ đường ranh giới giáp ranh giữa 2 ảnh (đường seam) để màu sắc mượt mà (Seamline cut, Laplacian pyramid, Feathering). |

---

## 2. Đặc trưng cục bộ & Khớp ảnh (Feature Extraction & Matching)

| Thuật ngữ (English) | Thuật ngữ (Tiếng Việt) | Giải thích & Ý nghĩa trong dự án |
|---|---|---|
| **Keypoints & Descriptors** | Điểm đặc trưng & Vector mô tả | **Keypoint:** Vị trí toạ độ $(x, y)$ của góc/cạnh nổi bật. **Descriptor:** Vector số (128-d với SIFT, 256-bit với ORB) mã hoá thông tin vân bề mặt xung quanh keypoint để so khớp. |
| **Classical Features** (SIFT, ORB, BRISK, AKAZE) | Đặc trưng cổ điển (Thủ công) | Các giải thuật trích xuất đặc trưng toán học truyền thống. Chạy nhanh, tốn ít RAM/CPU, nhưng dễ gãy khi ảnh ít vân (low-texture), mờ, hoặc xoay góc quá lớn. |
| **Learned Matchers** (LightGlue, SuperGlue, LoFTR, XFeat) | Bộ khớp đặc trưng bằng AI/Deep Learning | Sử dụng mạng nơ-ron (GNN, Transformer) để hiểu ngữ cảnh toàn ảnh và ghép điểm đặc trưng. Cực kỳ bền bỉ ở vùng khó (đồng ruộng lặp lại, ánh sáng gắt, xoay gắt) nhưng tốn tài nguyên GPU/CPU. |
| **Ratio Test (Lowe's Ratio)** | Phép lọc tỷ số khoảng cách | Kỹ thuật loại bỏ match rác: chỉ giữ match nếu khoảng cách đến láng giềng gần nhất nhỏ hơn đáng kể (ví dụ $< 0.75$) so với láng giềng gần thứ nhì. |
| **RANSAC** (Random Sample Consensus) | Giải thuật loại trừ ngoại lai ngẫu nhiên | Thuật toán lặp chọn 4 cặp điểm ngẫu nhiên để thử tính $H$, đếm số điểm khớp tuân theo $H$ đó, nhằm loại bỏ các cặp match sai (outliers) trước khi chốt $H$ chuẩn. |
| **Inliers & Inlier Ratio** | Điểm khớp hợp lệ & Tỷ lệ inlier | **Inliers:** Các cặp điểm thực sự khớp đúng hình học sau RANSAC. **Inlier Ratio:** Số inlier chia cho tổng số match ban đầu; chỉ số thô phản ánh độ tin cậy của phép ghép. |

---

## 3. Khái niệm cốt lõi trong 3 RQ của dự án (Failure-Aware Engine)

| Thuật ngữ (English) | Thuật ngữ (Tiếng Việt) | Giải thích & Ý nghĩa trong dự án |
|---|---|---|
| **Failure Prediction (RQ1)** | Dự báo lỗi đăng ký hình học | Khả năng tính toán các **chỉ báo rẻ** (blur score, số inliers, độ bao phủ không gian, sai số chiếu lại) ngay sau khi khớp frame để dự đoán xem ma trận $H$ này có làm hỏng bản đồ tích luỹ về sau không. |
| **Reprojection Error (RE)** | Sai số chiếu lại | Khoảng cách Euclidean (tính bằng pixel) giữa toạ độ điểm thực tế trên ảnh 2 và toạ độ điểm từ ảnh 1 được chiếu qua ma trận $H$. |
| **Cumulative Drift** | Sai số trôi tích luỹ (Drift) | Hiện tượng sai số nhỏ ở từng cặp frame nhân dồn qua thời gian ($H_{0 \to t}$), khiến các frame sau cùng bị bóp méo, lệch vị trí hàng chục mét hoặc biến dạng hình thang cực độ. |
| **Matcher Routing / Risk Gate (RQ2)** | Cơ chế phân luồng bộ khớp theo rủi ro | Chạy matcher cổ điển trước, chỉ kích hoạt learned matcher hoặc ảnh gốc khi chỉ báo vượt ngưỡng rủi ro của fold LOSO (`RDR-0011`). |
| **Pareto Frontier** | Biên tối ưu Pareto | Đường cong thể hiện sự đánh đổi tối ưu: không thể tăng thêm chất lượng mosaic mà không chấp nhận độ trễ (latency) cao hơn. |
| **Confidence-Triggered Recovery (RQ3)** | Phục hồi theo mức tin cậy | Cơ chế xử lý bước ghép khi rủi ro vượt ngưỡng $\tau$, thử nghiệm 4 chính sách: không cứu, bỏ frame, rematch anchor, tách submosaic. |
| ↳ **Frame Rejection (Drop)** | Loại bỏ khung hình | Bỏ hẳn frame hiện tại, nhảy cóc sang frame kế tiếp để tránh làm nhiễm độc ma trận tích luỹ $H_{0 \to t}$. |
| ↳ **Keyframe Rematching (Anchor)** | Khớp lại với Keyframe lịch sử | Thay vì ghép với frame $t-1$, hệ thống tìm trong bộ nhớ các frame mốc tin cậy đã đặt trước đó để ghép trực tiếp. |
| ↳ **Submosaic Splitting (Split)** | Tách cụm bản đồ con | Đóng cụm hiện tại và mở cụm mới với hệ toạ độ riêng; ngắt đứt chuỗi tích luỹ lỗi và giữ trọn vẹn số frame. |

---

## 4. Dữ liệu & Đánh giá thực nghiệm (Datasets & Metrics)

| Thuật ngữ (English) | Thuật ngữ (Tiếng Việt) | Giải thích & Ý nghĩa trong dự án |
|---|---|---|
| **GCP (Ground Control Point)** | Điểm khống chế mặt đất | Điểm mốc cố định trên thực địa được đo toạ độ GPS chính xác cỡ milimet/centimet, dùng làm chuẩn tuyệt đối để đánh giá sai số hình học của bản đồ mosaic. |
| **RTK (Real-Time Kinematic)** | Định vị vi sai thời gian thực | Công nghệ GPS độ chính xác cao (sai số $1\text{--}3\text{ cm}$) gắn trên drone chuyên dụng, giúp biết chính xác toạ độ tâm chụp của từng frame. |
| **Telemetry (.SRT / EXIF log)** | Dữ liệu đo xa / Nhật ký bay | File phụ đề/metadata đi kèm video drone chứa toạ độ GPS, độ cao (altitude), vận tốc, và các góc quay camera (yaw, pitch, roll) theo từng mili-giây. |
| **Georeferencing** | Định vị địa lý (Gắn toạ độ) | Quá trình gán hệ toạ độ thực (WGS84, UTM, VN-2000) vào từng pixel của ảnh mosaic. *(Dự án hiện tại là bản đồ cục bộ, không bắt buộc georeference).* |
| **RMSE (Root Mean Square Error)** | Sai số căn bậc hai trung bình | Căn của trung bình bình phương sai số; RMSE inlier trong các notebook là reprojection error trên chính điểm fit $H$, không phải sai số so với ground truth mặt đất. |
| **Self-Consistent Drift (Chain-vs-Direct)** | Độ lệch tự nhất quán chuỗi vs trực tiếp | Thước đo drift theo `RDR-0007`: so sánh ma trận chuỗi $H^{\text{chain}}_{i \to 0}$ với ma trận ghép thẳng $H^{\text{direct}}_{i \to 0}$ bằng SIFT ảnh gốc trên 5 điểm mốc (đơn vị pixel ảnh gốc). |
| **Reference Gate ($\ge 100$ inliers)** | Cổng nghiệm thu tham chiếu | Điều kiện tiên quyết của `RDR-0007`: chỉ công nhận điểm đo drift thực nghiệm khi cặp ghép trực tiếp có $\ge 100$ inliers. Mất vùng chồng được ghi nhận trung thực là `None`/`N/A`. |
| **Common Eligible Frame Set** | Tập khung hình đối chiếu chung | Tập hợp các bước $i \ge 1$ mà tất cả các mô hình đem so sánh đều có tham chiếu SIFT hợp lệ, bảo đảm so sánh cross-method công bằng. |
| **Step-Level Error ($e_i$)** | Sai số cấp bước | Sai số hình học của từng bước ghép so với matcher tham chiếu chất lượng cao (theo `RDR-0008` Proposed). |
| **Leave-One-Sequence-Out (LOSO)** | Kiểm chứng chéo giữ lại một chuỗi | Giao thức kiểm chứng chéo theo `RDR-0011`: mỗi fold giữ 1 sequence làm tập test, hiệu chỉnh toàn bộ ngưỡng rủi ro $\tau$ trên các sequence còn lại. |
