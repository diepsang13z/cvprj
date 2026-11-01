# RDR-0011: Leave-one-sequence-out và sửa kỹ thuật trước

## Status

Accepted — chỉ protocol chia sequence và phạm vi sửa kỹ thuật.

## Date

2026-11-01

## Context

Người dùng chốt hai lựa chọn: **Leave-one-sequence-out (LOSO)** và
**Chỉ sửa kỹ thuật trước**. Audit notebook phát hiện lỗi thực thi, ghi đè
artifact, tham chiếu không hợp lệ vẫn đi vào metric, assertion ép kết quả
nghiên cứu và giới hạn pilot bị mô tả nhầm là đánh giá toàn dataset.

## Decision

1. Giữ ba RQ trong RDR-0003: dự báo lỗi, phân luồng matcher và phục hồi.
2. Chọn LOSO theo **sequence**, không chia ngẫu nhiên cặp/frame gần nhau:
   mỗi fold giữ lại một sequence để đánh giá, dùng các sequence còn lại
   để hiệu chỉnh. Với tám sequence, có tám fold.
3. Dữ liệu của sequence giữ lại không được dùng chọn chỉ báo/ngưỡng hoặc
   chọn cấu hình có kết quả tốt nhất. Lưu danh sách train/test và cấu hình
   hiệu chỉnh của từng fold. Báo cáo theo sequence và kết quả tổng hợp,
   không coi các frame tương quan là các lần lặp độc lập.
4. LOSO không xoá lịch sử: village/grass đã được dùng để khám phá chỉ báo
   và chọn cửa sổ. Phải nêu giới hạn này; không gọi mọi fold là hoàn toàn
   độc lập với quá trình phát triển phương pháp.
5. Đợt hiện tại chỉ sửa kỹ thuật: runtime cloud, dữ liệu/đường dẫn,
   validity/provenance của metric, timing, xử lý thất bại, artifact và
   kiểm tra tính đúng. Không tự chốt policy thắng hay sửa code để ép giả thuyết.
6. **RDR-0008 vẫn Proposed.** Lựa chọn LOSO không phê duyệt ngưỡng sai số
   2 px, ngân sách escalation 25%, inlier ratio 0,30, ngưỡng NCC, hoặc
   split là chiến lược mặc định. Giá trị hiện có chỉ là cấu hình khám phá
   và phải được ghi rõ trong artifact.
7. Gate tham chiếu 100 inlier và giới hạn metric trong RDR-0007 vẫn giữ.
   Tham chiếu thiếu/không hợp lệ phải tạo phép đo không khả dụng, không
   biến thành 0 hay homography giả. Chain-vs-direct không được diễn giải
   thành ground truth thực địa; hết overlap không phải bằng chứng pipeline sai.
8. Chạy hết sequence/frame và có phép đo hợp lệ trên hết frame là hai
   việc khác nhau. Phải báo frame đã xử lý, ghép thành công, bị loại,
   phân mảnh và phần đánh giá không khả dụng riêng biệt.
9. Mỗi run có thư mục riêng, cấu hình/provenance và trạng thái hoàn tất.
   Không ghi đè artifact lịch sử. Thực nghiệm chỉ chạy hosted Colab/Kaggle
   theo RULES.md §8; kiểm tra tĩnh local không phải bằng chứng chạy cloud.

## Consequence

- Số liệu matching có thể dùng lại giữa các fold nếu cùng input/hash,
  cấu hình và không phụ thuộc vào việc chọn ngưỡng trên test sequence.
- Mỗi fold có thể chọn ngưỡng khác nhau; kết quả LOSO đánh giá quy trình
  hiệu chỉnh, không chứng minh một ngưỡng duy nhất tốt cho mọi sequence.
- Trước đánh giá xác nhận phải chốt các lựa chọn phương pháp còn Proposed;
  chạy LOSO với tham số khám phá vẫn là kết quả khám phá.
- Không cam kết thời gian chạy, mức tiết kiệm hay policy thắng trước khi đo.

## Liên hệ với quyết định cũ

Bổ sung protocol đánh giá cho RDR-0003; không thay metric RDR-0007,
không nâng trạng thái RDR-0008, không thay quy định cloud RDR-0010.
