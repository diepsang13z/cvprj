# RDR-0010: Tiếp thu góp ý sau buổi thuyết trình và các quyết định điều chỉnh dự án

## Status

Accepted

## Date

2026-10-14

## Context

Sau khi nhóm thuyết trình kết quả và phương pháp nghiên cứu (Present 2), hội đồng / giảng viên hướng dẫn đã đóng góp ý kiến phản biện. Để đảm bảo an toàn thiết bị, nâng cao chất lượng học thuật và đạt chuẩn bài báo khoa học IEEE, nhóm thống nhất ghi nhận và ban hành 5 quyết định điều chỉnh sau buổi báo cáo.

## Decision

Nhóm thống nhất 5 quyết định hành động cụ thể:

### 1. Môi trường thực nghiệm: Chạy trên Google Colab / Kaggle và lưu log đầy đủ
- **Tuyệt đối không chạy thực nghiệm / benchmark nặng trên CPU laptop cá nhân**, do tải tính toán liên tục ở nhiệt độ cao gây nguy cơ nghiêm trọng làm hỏng hoặc thoái hóa phần cứng cá nhân.
- Toàn bộ pipeline ghép ảnh, trích xuất đặc trưng và benchmark đánh giá phải chuyển 100% sang chạy trên nền tảng đám mây (Google Colab hoặc Kaggle) có GPU/CPU chuyên dụng.
- Mọi lượt chạy (run) trên Colab phải tự động lưu lại đầy đủ nhật ký (log), thông số cấu hình và artifact (`report.json`, biểu đồ, ảnh mosaic) để bảo đảm tính tái lập.

### 2. Làm lại phần Related Work chi tiết và chặt chẽ
- Rà soát và viết lại toàn diện phần Related Work theo cấu trúc 3 câu hỏi cốt lõi:
  1. **Hiện trạng:** Các nghiên cứu hiện tại giải quyết bài toán UAV mosaicking, matching và kiểm soát drift như thế nào?
  2. **Thiếu sót (Research Gap):** Các phương pháp hiện hành đang thiếu sót gì? (Ví dụ: pipeline cổ điển ghép "mù" không biết rủi ro; mô hình learned quá nặng để chạy toàn bộ; thiếu cơ chế phát hiện sớm sai số trước khi trôi dạt tích lũy vỡ bản đồ; xử lý lỗi thụ động sau khi hỏng).
  3. **Chứng minh tính ưu việt của nhóm:** Làm rõ luận điểm và thiết kế thực nghiệm chứng minh giải pháp của nhóm tốt hơn (dùng chỉ báo rẻ dự báo lỗi sớm, phân luồng matcher linh hoạt tiết kiệm tài nguyên mà giữ độ chính xác, cơ chế phục hồi phân mảnh giới hạn drift).

### 3. Chuẩn hóa bài báo và danh mục tài liệu tham khảo theo định dạng IEEE
- Bài báo hiện tại chưa đạt chuẩn định dạng IEEE. Cần rà soát toàn bộ cấu trúc bài theo đúng IEEE template (layout, tiêu đề, bảng biểu, hình vẽ).
- Đối chiếu từng tài liệu tham khảo trên Google Scholar để chuẩn hóa citation theo format IEEE (họ tên tác giả, tên bài viết chuẩn, tên hội nghị/tạp chí in nghiêng, tập, số, trang, năm xuất bản, DOI).

### 4. Bổ sung trực quan hóa Baseline vào bài báo
- Đưa hình ảnh và biểu đồ trực quan của đường cơ sở (Baseline) vào paper.
- Thể hiện rõ sự so sánh đối đầu giữa: baseline cổ điển (SIFT/ORB ghép tuần tự không có cơ chế rủi ro) hoặc baseline mô hình mạnh chạy đơn lẻ so với pipeline Failure-Aware đề xuất của nhóm.

### 5. Viết thêm phần phương pháp đo lường (Metrics / Measurement) vào bài báo
- Bổ sung mục chi tiết giải thích rõ ràng các thước đo và cơ chế đánh giá mà nhóm áp dụng:
  - Metric sai số cấp bước (step-level error / residual).
  - Metric đo drift tự nhất quán (chain vs direct theo `RDR-0007`).
  - Các chỉ báo rủi ro (NCC patch overlap, inlier ratio, reprojection error).
  - Các chỉ số đánh giá trade-off: thời gian thực thi (latency), tỷ lệ khung hình giữ lại (coverage / retained frames), số lượng submosaic.

## Consequence

- **Phần cứng:** Loại bỏ triệt để rủi ro hỏng máy cá nhân của các thành viên.
- **Học thuật:** Phần Related Work và Methodology trong paper đạt độ chặt chẽ, thuyết phục người đọc về tính mới và giá trị thực nghiệm.
- **Hình thức:** Paper tuân thủ nghiêm ngặt quy chuẩn xuất bản IEEE.
