# RDR-0006: Chốt danh sách cấu hình và mô hình đưa vào chạy thử nghiệm

## Status

Accepted

## Date

2026-10-13

## Context

- Tại `RDR-0003`, nhóm đã xác định hướng nghiên cứu Failure-Aware Mosaicking với RQ2 (Matcher Routing: mặc định dùng classical, chỉ gọi learned matcher khi rủi ro cao), nhưng chưa đặc tả danh sách cụ thể các model cần thử nghiệm.
- Tại `RDR-0004`, giảng viên hướng dẫn yêu cầu tinh gọn khối lượng công việc cho sinh viên năm 2, khảo sát các model có sẵn phù hợp mang về chạy thử và hiểu rõ cơ chế.
- Khảo sát kỹ thuật đối chiếu các bài báo và kho mã nguồn chính thức (Kim & Kim 2025, LightGlue, XFeat, Efficient LoFTR) cho thấy cần một shortlist có kiểm chứng thực nghiệm thay vì khẳng định cảm tính về hiệu năng mô hình.

## Decision

1. **Chốt danh sách các cấu hình và mô hình đưa vào chạy thử nghiệm:**
   - **Nhóm Baseline truyền thống (CPU):**
     - SIFT + BF/FLANN (mốc chuẩn độ chính xác hình học cổ điển).
     - ORB + BF Hamming (mốc chuẩn tốc độ cao nhất trên CPU).
   - **Nhóm Learned Matcher dự phòng (Trọng tâm RQ2):**
     - **SIFT + LightGlue:** Ưu tiên hàng đầu cho nhánh fallback dựa trên thực nghiệm UAV của Kim & Kim (2025); bắt buộc dùng chuẩn RootSIFT kèm scale/orientation từ wrapper chính thức của LightGlue.
     - **SuperPoint + LightGlue:** Đối chứng sparse learned toàn diện (thay cả detector lẫn matcher) để so sánh với nhánh lai SIFT + LightGlue.
   - **Nhóm Learned Baseline siêu nhẹ (Kiểm chứng giả thuyết RQ2):**
     - **XFeat + MNN:** Sparse matching siêu nhẹ trên CPU/GPU.
     - **XFeat + LighterGlue:** Đối chứng cốt lõi để trả lời câu hỏi: *liệu chính sách phân luồng classical-first có thắng được một mô hình learned siêu nhẹ chạy mọi lúc (always-lightweight) hay không?*
   - **Nhóm Thử nghiệm thăm dò có giới hạn (Detector-free / Semi-dense):**
     - **Efficient LoFTR:** Chỉ chạy thử nghiệm thăm dò trên tập nhỏ các cặp frame khó/ít texture mà detector điểm cục bộ thất bại, nhằm xác định điểm nghẽn nằm ở khâu tìm điểm hay khâu khớp điểm. Không đưa vào pipeline chính nếu chi phí vượt ngưỡng tài nguyên.

2. **Ràng buộc kỹ thuật khi triển khai:**
   - **100% Pretrained Weights:** Chỉ sử dụng checkpoint công khai chính thức, đóng băng trọng số (frozen), tuyệt đối không tổ chức huấn luyện hay fine-tune matcher.
   - **Quy tắc đo lường công bằng:** Toàn bộ cấu hình phải được đo trên cùng phần cứng cố định (Google Colab GPU T4 hoặc CPU laptop), cùng kích thước ảnh và cùng phương pháp ước lượng Homography.
   - **Tính đúng chi phí phân luồng (Routing Latency):** Khi kích hoạt fallback, tổng thời gian xử lý phải cộng dồn cả lượt chạy classical ban đầu, tránh việc chỉ đo riêng lượt learned.
   - **Tuân thủ bản quyền:** Ghi nhận rõ điều khoản sử dụng nghiên cứu phi thương mại của SuperPoint (Magic Leap).

## Consequence

- Thiết lập cơ sở kỹ thuật rõ ràng để xây dựng module `matcher` linh hoạt trong mã nguồn.
- Giữ vững phạm vi đề tài, tập trung tài nguyên vào thực nghiệm đo đạc thay vì phân tán vào việc khảo sát thêm mô hình.
