# RDR-0009: Không áp đặt hạn mức cứng tối thiểu 30 tài liệu tham khảo

## Status

Accepted

## Date

2026-10-14

## Context

- Hướng dẫn học phần (`reports/templates/presen_research_based_learning_requirements.txt`) có dòng gợi ý: *"chỉ những trích dẫn nào có nhắc đến trong bài thì mới có trong mục Tài liệu tham khảo(Ít nhất 30 bài)"*.
- Bài báo mục tiêu của nhóm là định dạng hội nghị IEEE (tối thiểu 4 trang) cho sinh viên năm 2, tập trung sâu vào bài toán kỹ thuật hẹp: **Failure-Aware Mosaicking (RQ1–RQ3)** trên video UAV.
- Nếu ép số lượng $\ge 30$ bài sẽ dẫn đến hiện tượng trích dẫn hình thức, chèn bài báo không thực đọc hoặc không liên quan trực tiếp để đối phó con số.
- Thư mục `refs/` hiện có **18 bài báo chất lượng cao** (CVPR, ICCV, NeurIPS, ISPRS, Remote Sensing, Nature SciRep) bao phủ toàn diện 4 mảng: UAV Mosaicking, Failure Prediction (RQ1), Matcher Routing (RQ2), và Recovery (RQ3). Tất cả đều đã được nhóm đọc, phân loại và bóc tách cụ thể trong `refs/INDEX.md`.

## Decision

1. **Không áp đặt hạn mức cứng tối thiểu 30 tài liệu tham khảo** cho báo cáo / bài báo IEEE của nhóm.
2. **Nguyên tắc trích dẫn:**
   - Ưu tiên chất lượng và độ khớp thực tế: **chỉ trích dẫn những bài thực sự được đọc, đối chiếu số liệu hoặc kế thừa phương pháp** trong văn bản bài báo.
   - Giữ quy mô danh mục tham khảo tinh gọn, thực chất trong khoảng **15–22 bài** phù hợp với dung lượng bài báo 4–6 trang chuẩn IEEE.
3. Bộ 18 bài báo hiện có trong `refs/INDEX.md` là nguồn nòng cốt đầy đủ cho các chương Introduction, Related Works, và Methodology. Nếu trong quá trình viết cần trích dẫn thêm phương pháp phụ trợ (ví dụ OpenCV, RANSAC gốc), chỉ bổ sung khi thực sự có nhắc đến trong bài.

## Consequence

- Tránh lãng phí thời gian tìm kiếm và nhồi nhét tài liệu tham khảo rác.
- Giữ vững tính trung thực học thuật và chất lượng danh mục trích dẫn theo chuẩn IEEE.
- Đảm bảo tính khả thi cho nhóm sinh viên năm 2 tập trung hoàn thiện bài viết và kết quả thực nghiệm.
