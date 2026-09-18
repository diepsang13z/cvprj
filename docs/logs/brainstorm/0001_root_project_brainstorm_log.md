# Log trao đổi: Đề tài CPV / AIL303m và hướng drone

## 1. Chọn đề tài cho AIL303m

**Người dùng:** Nên chọn đề tài nào để làm cho môn này?

**Trợ lý:** Sau khi xem đề cương AIL303m, đề xuất ban đầu là dự đoán nguy cơ sinh viên bỏ học/kết quả học tập vì có thể bao phủ EDA, feature engineering, các mô hình phân loại, cross-validation, xử lý mất cân bằng lớp, giải thích mô hình, K-Means và PCA. Một lựa chọn thay thế là customer churn.

## 2. Liên kết với môn CPV301

**Người dùng:** Thầy nói có thể lấy đề tài môn CPV làm cho môn AIL nên muốn chốt đề tài CPV trước.

**Trợ lý:** Sau khi xem đề cương CPV301, đề xuất ban đầu là nhận diện và phân loại biển báo giao thông từ ảnh bằng CV cổ điển và ML. Phạm vi gọn: 5 loại biển báo; CPV dùng tiền xử lý, đặc trưng hình dạng/màu/HOG; AIL dùng Logistic Regression, KNN, SVM, Decision Tree/Random Forest, PCA và K-Means.

## 3. Định hướng kế thừa cho drone

**Người dùng:** Muốn một đề tài có thể kế thừa cho dự án drone trinh sát sau này.

**Trợ lý:** Đề xuất chuyển trọng tâm sang thị giác từ góc nhìn UAV, không làm cơ chế bay ngay trong học kỳ này. Một hướng ban đầu là phát hiện, phân loại và theo dõi phương tiện giao thông trong video UAV phục vụ giám sát giao thông:

- CPV: phát hiện đối tượng, tracking, đếm xe.
- AIL: phân loại phương tiện bằng đặc trưng ảnh và so sánh các mô hình ML cổ điển.
- Dataset tham khảo: VisDrone.

**Người dùng:** Có ý tưởng dài hạn về drone phỏng sinh học, lấy cảm hứng từ hải âu/cú mèo, với các ứng dụng như cứu hộ, trinh sát, thám hiểm.

**Trợ lý:** Làm rõ rằng đây là một nền tảng rộng, cần tách cơ chế bay và mô-đun thị giác. Câu hỏi định hướng là: làm sao chứng minh một đặc tính lấy cảm hứng từ sinh học mang lợi thế đo được cho một nhiệm vụ quan sát dân sự cụ thể? Trong học kỳ này nên làm “mắt nhìn” của drone, không làm cánh vỗ hay cơ chế bay.

**Người dùng:** Đây là đề tài CPV của học kỳ hiện tại; đội có 4 người, nhưng người dùng dẫn dắt chính. Phần phỏng sinh học và mục tiêu demo sẽ tính sau.

**Trợ lý:** Chốt nguyên tắc: xây mô-đun thị giác nhận video UAV để có thể tích hợp vào drone tương lai. Cần chọn một tiêu chí demo ưu tiên: phát hiện đối tượng, theo dõi/đếm, tìm kiếm, hoặc đánh giá vùng hạ cánh.

## 4. Các hướng CV từ video UAV

**Người dùng:** Hỏi sơ qua các lựa chọn phát hiện đối tượng, theo dõi/đếm, tìm kiếm người/vật thể, và đánh giá vùng hạ cánh.

**Trợ lý:**

| Hướng | Demo | Độ khó | Khả năng kế thừa |
|---|---|---:|---|
| Phát hiện đối tượng | Bounding box và nhãn | Thấp | Drone biết “thấy gì, ở đâu” |
| Theo dõi/đếm | ID, quỹ đạo, vạch đếm | Trung bình | Giám sát giao thông/khu vực |
| Tìm kiếm người/vật thể | Đánh dấu mục tiêu trong vùng | Trung bình-cao | Kịch bản cứu hộ |
| Đánh giá vùng hạ cánh | Vùng an toàn/nguy hiểm | Cao | Tự chọn điểm đáp |

Khuyến nghị ban đầu là theo dõi/đếm phương tiện vì cân bằng giữa phạm vi môn học và độ khó.

## 5. Chuyển sang ý tưởng quét video để dựng bản đồ

**Người dùng:** Quét rồi vẽ bản đồ thì sao?

**Trợ lý:** Đây là hướng rất phù hợp CPV vì đề cương có feature matching, RANSAC, feature-based alignment và image stitching.

Đề tài được đề xuất:

> **Xây dựng bản đồ ảnh 2D từ chuỗi ảnh/video UAV bằng kỹ thuật ghép ảnh.**

Các mức phạm vi:

1. Core học kỳ: ghép ảnh 2D để tạo aerial mosaic/panorama nhìn từ trên xuống.
2. Mở rộng AIL: chia mosaic thành ô và phân loại đường/cỏ/nước/công trình.
3. Để tương lai: GPS/IMU, bản đồ 3D, định vị thời gian thực.

Giới hạn quan trọng: khi chưa có GPS, hiệu chuẩn camera và sửa méo phối cảnh/địa hình, đầu ra là **bản đồ ảnh 2D (aerial mosaic)**, không phải bản đồ địa lý hay orthomosaic chính xác.

## 6. Tên đề tài

**Người dùng:** Đặt tên đề tài này là gì?

**Trợ lý:** Đề xuất ban đầu:

> **Xây dựng bản đồ ảnh 2D từ chuỗi ảnh UAV bằng kỹ thuật ghép ảnh dựa trên đặc trưng**
>
> *2D Aerial Map Construction from UAV Image Sequences Using Feature-Based Image Stitching*

**Người dùng:** Muốn người nghe hiểu rõ đang xử lý frame video rồi dựng map.

**Trợ lý:** Tên nên chốt:

> **Xây dựng bản đồ ảnh 2D từ video UAV bằng trích xuất khung hình và ghép ảnh dựa trên đặc trưng**
>
> *2D Aerial Map Construction from UAV Video via Frame Extraction and Feature-Based Image Stitching*

Thông điệp trình bày:

```text
Video UAV thô → chọn các frame chồng lấn → căn chỉnh/ghép ảnh → bản đồ ảnh 2D
```

## 7. Dataset đã tìm được

**Người dùng:** Có sẵn dataset chưa? Muốn xử lý video thô từ UAV, còn option nào khác không?

**Trợ lý:** Dataset được phân loại theo mức phù hợp với bài toán dựng mosaic từ video UAV:

| Dataset | Phù hợp | Lưu ý |
|---|---|---|
| [UMCD](https://www.umcd-dataset.net/) | Lựa chọn chính | Thiết kế riêng cho UAV mosaicking và change detection; khoảng 3.5 GB; gồm video mosaic và cặp video có georeference. Cần email xin mật khẩu tải. |
| [DroneZaic](https://datadryad.org/dataset/doi:10.5061/dryad.r4xgxd2q7) | Dự phòng | Video UAV thật trên nông trại, có metadata GPS `.SRT`; bộ video thô đầy đủ khoảng 38.21 GB nên cần giới hạn một mission/đoạn video. |
| [Mid-Air](https://midair.ulg.ac.be/) | Kiểm thử | Dữ liệu chuyến bay drone mô phỏng, có RGB, GPS, IMU, depth và semantic map; phù hợp thử thuật toán, không nên là demo chính. |
| [UAVDT](https://sites.google.com/view/grli-uavdt/) | Stress-test | Có video UAV thật, nhưng được thiết kế cho detection/tracking chứ không phải mosaic. |
| [Aerial234](https://huggingface.co/datasets/RussRobin/Aerial234) | Fallback ảnh rời | 234 ảnh drone quét liên tục, phù hợp kiểm tra pipeline ghép ảnh nhưng không phải video thô. |

Khuyến nghị hiện tại:

1. Dataset chính: UMCD.
2. Nếu vướng quyền tải: DroneZaic.
3. Dataset phụ kiểm thử: Mid-Air hoặc Aerial234.

Pipeline lõi:

```text
Video thô → trích/chọn frame đủ chồng lấn → ORB/SIFT matching
→ RANSAC + homography → warp + blending → aerial mosaic
```

## 8. Độ khó và phạm vi an toàn

**Người dùng:** Chủ đề có quá khó với sinh viên AI cuối năm 2 không?

**Trợ lý:** Không quá khó nếu giữ phạm vi ở mức MVP. Độ khó khoảng 6/10.

MVP hợp lý:

- Một video ngắn, camera gần hướng thẳng xuống và cảnh tương đối phẳng.
- Chọn 15–30 frame rõ, có vùng chồng lấn.
- ORB, matching, RANSAC/homography, `warpPerspective`, blending đơn giản.
- Xuất một aerial mosaic.

Không làm trong học kỳ:

- Bản đồ diện tích lớn hay độ chính xác khảo sát.
- GPS/IMU, 3D reconstruction, SLAM, realtime.
- Xử lý mọi góc bay/video UAV.
- Cơ chế bay phỏng sinh học.

Gợi ý chia nhóm:

1. Trích frame, kiểm tra độ mờ và độ chồng lấn.
2. Feature detection, matching và RANSAC.
3. Warp, blending, xuất mosaic.
4. Đánh giá, dataset, demo, báo cáo.

## 9. Giá trị thực tế của đề tài

**Người dùng:** Map đã quá chính xác rồi thì project này giải quyết được gì?

**Trợ lý:** Nhận định: nếu chỉ tạo “một cái map” thì giá trị thực tế yếu; không nên định vị dự án như thay thế Google Maps.

Giá trị đúng là tạo **ảnh toàn cảnh hiện trạng cục bộ, mới nhất** từ chuyến bay vừa thực hiện, khi ảnh nền hiện có cũ, thiếu chi tiết hoặc hiện trường đã thay đổi. Bối cảnh phù hợp:

- Khảo sát công trường/khuôn viên sau thi công.
- Theo dõi hiện trạng đồng ruộng.
- Đánh giá hiện trường sau thiên tai.
- Hỗ trợ drone thám hiểm tạo “bộ nhớ không gian” của khu vực vừa bay qua.

Hướng định vị vấn đề nên là:

> **Xây dựng bản đồ ảnh hiện trạng cục bộ từ video UAV phục vụ khảo sát khu vực.**

Mosaic là năng lực CV lõi; “khảo sát hiện trạng” là bài toán mang lại lý do tồn tại cho dự án.

## 10. Hình thức thực hiện: project môn học hay nghiên cứu khoa học

**Người dùng:** Nên làm dự án môn này dạng project hay nghiên cứu khoa học?

**Trợ lý:** Khác biệt cốt lõi không nằm ở độ khó mà ở thứ phải chứng minh:

| | Project môn học | Nghiên cứu khoa học |
|---|---|---|
| Phải chứng minh | Hệ thống chạy, demo được, hiểu pipeline | Câu hỏi nghiên cứu + so với baseline + kết luận dùng lại được |
| Sản phẩm | Demo + báo cáo môn | Bài báo/hội thảo, có phần "đóng góp" |
| Rủi ro | Thấp | Cao: không có gì mới thì thành báo cáo kỹ thuật |

Phần lõi của đề tài (ORB/SIFT → matching → RANSAC → homography → warp/blend) là kiến thức đã có sẵn, làm theo tutorial ra được kết quả — về bản chất là project. Muốn thành NCKH cần increment thật: chiến lược chọn frame chồng lấn, đánh giá định lượng (số inlier, RMSE control point, PSNR/SSIM vùng chồng lấn, độ phủ), so sánh ORB/SIFT/AKAZE, ablation.

Lưu ý thực tế: NCKH thường chỉ 1–2 tác giả, nhóm hiện có 4 người cho 2 môn.

**Người dùng:** Chọn giữ mở, ưu tiên kế thừa drone.

**Trợ lý:** Chốt **nộp dạng project môn học**, không cam kết NCKH. Giữ đường kế thừa drone bằng 3 ràng buộc thiết kế — cũng chính là "lớp nghiên cứu" miễn phí nếu sau này nâng lên NCKH:

1. Đóng gói thành module có interface cố định. Vào: đường dẫn video (hoặc thư mục frame). Ra: ảnh mosaic + metadata. Không hardcode dataset/path.
2. Lưu **ma trận homography tích luỹ** (frame → hệ toạ độ mosaic), không chỉ lưu ảnh kết quả. Đây là thứ drone cần để trả lời "vật này nằm ở đâu trong bản đồ". Chi phí gần bằng 0 nếu làm ngay, phải làm lại từ đầu nếu bỏ qua.
3. Log metric mỗi lần chạy ra CSV/JSON: số frame dùng, số inlier, RMSE, thời gian, % diện tích phủ. Đây chính là số liệu NCKH.

Không làm ở giai đoạn này: related work, so sánh baseline, tuyên bố đóng góp — đó là chi phí riêng của NCKH.

Ranh giới cần giữ: đừng để "kế thừa cho drone" biến thành lý do mở rộng phạm vi. Kế thừa thật chỉ cần đúng 3 điểm trên; GPS/IMU, 3D, realtime vẫn nằm ngoài học kỳ này.

## Trạng thái hiện tại

**Đề tài CPV đề xuất để chốt:**

> **Xây dựng bản đồ ảnh 2D từ video UAV bằng trích xuất khung hình và ghép ảnh dựa trên đặc trưng.**

**Phạm vi MVP:** Video UAV ngắn → chọn frame chồng lấn → ORB/SIFT → matching → RANSAC/homography → blending → aerial mosaic.

**Định vị ứng dụng:** Tạo ảnh bản đồ hiện trạng cục bộ phục vụ khảo sát/thám hiểm dân sự; không thay thế bản đồ địa lý chính xác.

**Hình thức:** Nghiên cứu khoa học + 1 MVP demo. RQ chưa chốt.

**Ràng buộc thiết kế để kế thừa drone:** module có interface cố định (video → mosaic + metadata); lưu homography tích luỹ frame → mosaic; log metric mỗi lần chạy ra CSV/JSON.

## 11. Pivot sang nghiên cứu khoa học + MVP demo

**Người dùng:** Muốn thay đổi hướng project thành nghiên cứu khoa học + 1 MVP demo.

**Trợ lý:** Chốt nguyên tắc: NCKH + MVP không phải "làm thêm" mà là **đổi câu hỏi phải trả lời** — project chứng minh "hệ thống chạy", NCKH chứng minh "một tuyên bố có thể bác bỏ, bằng số". MVP demo và nghiên cứu dùng **chung một codebase**: pipeline = demo, eval harness = số liệu bài báo.

Ba ràng buộc thiết kế ở mục 10 (interface cố định, homography tích luỹ, log metric CSV/JSON) không bỏ đi mà trở thành chính hạ tầng nghiên cứu.

Các RQ đề xuất (**chưa chốt**, tối thiểu 3, chia chung một harness + một dataset):

| RQ | Câu hỏi | Baseline | Đề xuất | Metric | Đóng góp |
|---|---|---|---|---|---|
| RQ1 — Chọn frame (chính, kế thừa drone) | Không GPS/IMU, chọn frame *tối thiểu* nào để mosaic đạt độ phủ + chất lượng? | Chọn frame cách đều | Chọn thích ứng: blur (Laplacian variance) + overlap (homography/inlier) | Tỉ lệ ghép thành công, #frame dùng vs thô, % độ phủ, RMSE | Ít frame hơn, chất lượng tương đương/cao hơn |
| RQ2 — Bộ mô tả đặc trưng | Detector–descriptor nào bền nhất với ảnh aerial (xoay/co giãn/độ sáng/mờ)? | ORB (mặc định) | So sánh ORB vs SIFT vs AKAZE | Tỉ lệ ghép thành công, inlier, RMSE reprojection, thời gian | Bảng khuyến nghị detector theo loại cảnh |
| RQ3 — Blending | Blending nào giảm seam/ghost tốt nhất? | Weighted average | Multi-band / Laplacian pyramid | PSNR/SSIM vùng chồng lấn + no-reference | Khuyến nghị blending cho mosaic UAV |

RQ dự phòng (nếu muốn 4): **ngưỡng overlap tối thiểu** giữa frame liền kề để đăng ký không thất bại (quét 20%→70%, tìm ngưỡng an toàn).

Thứ tự triển khai đề xuất: RQ2 (nhanh, xác định detector) → RQ1 (đóng góp chính) → RQ3 (polish). Nếu bí thời gian cắt RQ3 — đây là "làm đẹp", không phải đóng góp cốt lõi. RQ1 + RQ2 đã đủ thành một NCKH sinh viên chặt chẽ.

Lưu ý thực tế:
- 3 RQ = 3 lần phải bảo vệ; đừng chạy song song từ đầu.
- Bẫy novelty: nếu chọn-frame không thắng rõ baseline → thành báo cáo kỹ thuật. Đặt tuyên bố khiêm tốn: "ít frame hơn mà không giảm chất lượng" đã là đóng góp hợp lệ.
- NCKH thường 1–2 tác giả, nhóm 4 người cho 2 môn → tách rõ ai đứng NCKH, ai làm demo/báo cáo môn.

**MVP demo (đúng 1 cái):** đưa 1 video UAV ngắn (UMCD/DroneZaic) → xuất mosaic + hiển thị trực quan số frame được chọn so với tổng frame thô. Một demo này chứng minh đồng thời hệ thống chạy và đóng góp nghiên cứu.

