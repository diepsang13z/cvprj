# Kịch Bản Thuyết Trình Paper Với Giảng Viên Hướng Dẫn

- **Đề tài:** Ghép ảnh 2D từ video UAV biết rủi ro và thích ứng tài nguyên: một nghiên cứu thực nghiệm
- **Nhóm thực hiện:** Nhóm 09 (AI2002) — Diệp Quang Sáng, Nguyễn Đức Nam, Đào Đặng Nguyên Khôi, Trương Quang Đăng Khoa
- **Thời lượng dự kiến:** 3 – 5 phút

---

## 1. Phân vai gợi ý

- **Phần 1: Bài toán & Động lực** (Sáng)
- **Phần 2: Ba câu hỏi nghiên cứu & Kết quả thực nghiệm (RQ1 & RQ2)** (Nam & Khôi)
- **Phần 3: Chiến lược phục hồi (RQ3), Giới hạn & Kế hoạch tiếp theo** (Khoa)

*(Nếu nhóm phân công 1 bạn thuyết trình toàn bộ, đọc tuần tự từ Phần 1 đến Phần 3).*

---

## 2. Lời thoại thuyết trình (Script)

### PHẦN 1: BÀI TOÁN & ĐỘNG LỰC NGHIÊN CỨU (~1 phút)

> "Kính thưa Thầy/Cô, hôm nay nhóm 09 xin báo cáo kết quả nghiên cứu: **Ghép ảnh 2D từ video UAV biết rủi ro và thích ứng tài nguyên**.
>
> 1. **Bài toán đặt ra:**
> Ghép ảnh tuần tự (sequential mosaicking) dựa trên homography tích luỹ là phương án tính toán rẻ nhất để tạo ảnh hiện trạng 2D từ video UAV mà không cần hệ thống photogrammetry hay GPS/IMU đắt tiền. Tuy nhiên, nó có điểm yếu chí mạng: **hỏng một cách âm thầm**. Chỉ cần 1 frame ghép sai tích luỹ vào bản đồ, toàn bộ các frame tiếp theo đều thừa hưởng sai số đó và làm bản đồ bị trôi dạt (drift) vĩnh viễn.
>
> 2. **Đánh đổi hiện tại trong văn liệu:**
> - Matcher cổ điển (SIFT/ORB) chạy rất nhanh trên CPU nhưng dễ vỡ ở địa hình thiếu vân hoặc lặp vân.
> - Matcher học sâu (như LightGlue/LoFTR) bền vững hơn nhưng chi phí tính toán cao hơn từ 1 đến 2 bậc độ lớn, không khả thi khi phải xử lý toàn bộ frame trên thiết bị thực tế hoặc laptop cá nhân.
>
> Thay vì chọn cứng nhắc một mô hình, hướng nghiên cứu của nhóm là: **Chỉ tiêu tốn tài nguyên cho mô hình nặng khi phát hiện frame có rủi ro cao**, đồng thời đo kiểm thực nghiệm trên bộ dữ liệu chuẩn NPU Drone-Map."

---

### PHẦN 2: KẾT QUẢ THỰC NGHIỆM TRẢ LỜI CÁC RQ (~2 phút)

> "Nghiên cứu của nhóm tập trung trả lời 3 câu hỏi cốt lõi:
>
> #### RQ1: Dùng chỉ báo rẻ nào để phát hiện sớm bước ghép hỏng?
> Các luật nhận/loại truyền thống thường nhìn vào số lượng `matches` hoặc `inliers`. Tuy nhiên kết quả thực nghiệm đo trên 45 bước cho thấy một phát hiện phản trực giác:
> - **Chỉ báo đếm điểm hoàn toàn thất bại ở cấp bước:** AUC chỉ đạt **0.40** cho matches và **0.41** cho inliers (thấp hơn cả đoán ngẫu nhiên 0.50). Lý do là ở các vùng ruộng lúa hay cây cối lặp vân, thuật toán tìm được rất nhiều điểm khớp nhưng toàn bộ là khớp sai.
> - Ngược lại, **bằng chứng sau khi ghép** (post-registration evidence) như hệ số tương quan chuẩn hoá NCC (AUC **0.86**) và diện tích phủ chéo (overlap) mới thực sự phân tách chính xác bước ghép sai.
>
> #### RQ2: Phân luồng thích ứng (Matcher Routing) đem lại lợi ích gì?
> Nhóm xây dựng cơ chế phân luồng 2 tầng: mặc định chạy SIFT CPU, chỉ khi độ rủi ro vượt ngưỡng ($\tau_{\text{ncc}} = 0.93$) mới leo thang gọi matcher học sâu:
> - **Phát hiện quan trọng:** Chạy matcher học sâu cho **100% frame** vừa chậm vừa cho drift cao hơn cả SIFT thuần (**82.4 px / 60.4 s** so với **75.3 px / 3.2 s**).
> - Trong khi đó, phân luồng có chọn lọc chỉ cần leo thang **16% số bước**, đưa drift tích luỹ cuối cùng về **28.5 px** (giảm 62% sai số trôi dạt) trong khi thời gian chỉ tốn 13.3 s.
> - Kết quả này chứng minh điểm làm việc tối ưu nằm trong một khoảng hẹp, không phải cứ dùng mô hình mạnh cho mọi frame là đem lại kết quả tốt."

---

### PHẦN 3: PHỤC HỒI (RQ3) & TỰ PHẢN BIỆN GIỚI HẠN (~1.5 phút)

> #### RQ3: Khi phát hiện bước gãy, cơ chế phục hồi nào hiệu quả nhất?
> Dưới cùng một ngưỡng kích hoạt rủi ro, nhóm so sánh 3 cơ chế phục hồi:
> 1. Bỏ frame (Frame dropping)
> 2. Ghép lại với keyframe cũ đã chốt (Keyframe re-matching)
> 3. Tách mảnh bản đồ con (Frame-preserving submosaic splitting)
>
> **Kết quả:**
> - Bỏ frame và rematch keyframe bị **hiệu ứng kích hoạt dây chuyền (cascading triggers)**: một khi đã gãy, các frame sau tiếp tục gãy liên hoàn, khiến bản đồ cuối cùng chỉ giữ lại được **14 trên tổng số 46 frame** (mất 70% dữ liệu).
> - Chiến lược tách mảnh con giữ trọn vẹn **46/46 frame** vào các cụm bản đồ độc lập có độ tin cậy cao, bảo toàn toàn bộ dữ liệu quan sát của chuyến bay.
>
> #### Giới hạn nghiên cứu & Công việc tiếp theo:
> Nhóm nhìn nhận thẳng thắn các giới hạn của bản nháp v0.1:
> 1. Số liệu hiện mới đo trên 2 cửa sổ chọn lọc (45 bước) của NPU Drone-Map; cần mở rộng trên các sequence dài hơn.
> 2. Thời gian đo hiện tại mới tính ở tầng matcher, chưa tính trọn gói RANSAC và warp.
> 3. **Bước kế tiếp:** Nhóm sẽ nối mạch End-to-End từ **Đánh giá rủi ro $\to$ Phân luồng thích ứng $\to$ Tách mảnh phục hồi** thành một pipeline thống nhất và kết xuất ảnh mosaic trực quan để nghiệm thu.
>
> Nhóm xin lắng nghe nhận xét và góp ý của Thầy/Cô để hoàn thiện bài báo. Xin cảm ơn Thầy/Cô."

---

## 3. Bảng tra cứu số liệu nhanh (Dành cho Q&A phản biện)

| Câu hỏi / Chủ đề | Đại lượng | Con số thực nghiệm | Ý nghĩa trả lời GV |
| :--- | :--- | :--- | :--- |
| **RQ1: Chỉ báo đếm điểm** | AUC `matches` / `inliers` | **0.40 / 0.41** | Đếm điểm cấp bước thua đoán mò vì dương tính giả ở vùng lặp vân. |
| **RQ1: Chỉ báo đo sau ghép** | AUC NCC sau warp | **0.86** | Đo độ tương quan ảnh sau biến đổi hình học mới là chỉ báo tin cậy. |
| **RQ2: Chạy Deep Learning 100%** | Drift cuối / Thời gian | **82.4 px / 60.4 s** | Chậm hơn ~19 lần và drift tệ hơn SIFT (75.3 px / 3.2 s). |
| **RQ2: Phân luồng thích ứng** | Ngưỡng $\tau_{\text{ncc}} = 0.93$ | **28.5 px / 13.3 s** | Chỉ leo thang 16% frame, giảm 62% drift tích luỹ. |
| **RQ3: Hiệu quả giữ frame** | Số frame giữ lại | **46/46** (Tách mảnh)<br>**14/46** (Bỏ frame / Rematch) | Bỏ frame kích hoạt dây chuyền làm mất 70% ảnh; tách mảnh bảo toàn 100%. |
