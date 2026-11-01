# RDR-0001: Điểm dừng khảo sát literature

## Status

Accepted

## Date

2026-09-18

## Decision

Khảo sát literature dừng khi **tất cả** điều kiện sau được đáp ứng.

### 1. Đủ bằng chứng để đánh giá từng RQ

Mỗi RQ ứng viên có:

- Ít nhất ba công trình gần nhất để đối chiếu.
- Một chuỗi lập luận có nguồn: `existing work → limitation → proposed difference`.
- Baseline, dataset và metric khả dụng để kiểm tra claim.

Ba công trình là mức tối thiểu để đối chiếu, không phải quota tự động kết thúc khảo sát.

### 2. Đạt information saturation

Hai vòng tìm kiếm liên tiếp — bằng tinh chỉnh keyword hoặc citation chaining — không phát hiện công trình trực tiếp liên quan làm thay đổi đánh giá của bất kỳ RQ nào.

Paper chỉ lặp lại phương pháp, dataset hoặc kết luận đã biết không được tính là thông tin mới.

### 3. Mỗi RQ đã có quyết định

Mỗi RQ nhận đúng một trạng thái:

- **Keep:** còn khoảng trống cụ thể và kiểm chứng được.
- **Narrow:** ý tưởng đã tồn tại nhưng còn boundary condition hoặc evaluation gap cụ thể.
- **Kill:** đã có nghiên cứu gần tương đương hoặc không thể đánh giá bằng nguồn lực hiện có.

### 4. Có kết quả đóng khảo sát

Một trong hai kết quả sau phải đạt:

- Có ba RQ `keep` hoặc `narrow` tạo thành một bundle dùng chung pipeline và evaluation harness.
- Không còn đủ ba RQ hợp lệ sau khi đạt information saturation; ghi nhận cần pivot thay vì tiếp tục broad search.

## Chưa được dừng khi

- Mới tìm thấy một paper ủng hộ hoặc phản bác ý tưởng.
- Một truy vấn không trả về kết quả.
- Chỉ đạt một số lượng paper tùy ý.
- Novelty mới ở mức “có vẻ chưa ai làm”.
- Chưa xác định được baseline, dataset hoặc metric cho RQ.

## Mở lại khảo sát khi

- Xuất hiện công trình trực tiếp mâu thuẫn với novelty claim đã chốt.
- Dataset hoặc baseline cốt lõi không còn sử dụng được.
- Phạm vi hoặc RQ nghiên cứu thay đổi.