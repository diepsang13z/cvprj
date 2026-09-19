# KỊCH BẢN THUYẾT TRÌNH ĐỀ CƯƠNG NGHIÊN CỨU (RESEARCH PROPOSAL SCRIPT)
## Đề tài: Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking for UAV Video
**Khóa học:** AI2002 | **Nhóm:** 09 | **Thời lượng chuẩn:** 10 – 12 phút  
**Giảng viên hướng dẫn:** TS. Nguyễn Hồng Hải (HaiNH51)  
**Cấu trúc chuẩn theo Hội đồng:**
1. Giới thiệu đề tài
2. Input/Output $\to$ Dataset
3. Phương pháp đánh giá
4. Đề xuất hướng giải quyết
5. Đề xuất đóng góp của nhóm cho bài toán

---

### PHÂN CÔNG VAI TRÒ & TIẾN TRÌNH THUYẾT TRÌNH (8 SLIDES)

| STT | Thành viên | Slide phụ trách | Nội dung chính | Thời lượng dự kiến |
| :-: | :--- | :---: | :--- | :---: |
| **1** | **Diệp Quang Sáng** | Slide 1 – 2 | **1. Giới thiệu đề tài:** Bối cảnh thực tế, Điểm nghẽn & Mục tiêu | ~2.5 phút |
| **2** | **Đào Đặng Nguyên Khôi** | Slide 3 – 4 | **2. Input/Output $\to$ Dataset:** Quy cách vào/ra & Dữ liệu NPU / DroneZaic | ~2.5 phút |
| **3** | **Trương Quang Đăng Khoa** | Slide 5 – 6 | **3. Đánh giá & 4. Hướng giải quyết:** Chỉ số định lượng & Pipeline 2 tầng | ~3.0 phút |
| **4** | **Nguyễn Đức Nam** | Slide 7 – 8 | **5. Đóng góp của nhóm:** 3 Đóng góp, Kế hoạch 6 tuần, Kết luận & Q&A | ~2.5 phút |

---

## PHẦN 1: GIỚI THIỆU ĐỀ TÀI
**Người trình bày:** **Diệp Quang Sáng (SE200655)**  
*Thời lượng: ~2.5 phút (Slide 1 $\to$ Slide 2)*

---

### 🎙️ Slide 1: Bìa đề tài & Nhóm thực hiện
*(Bật Slide 1 — Phong thái tự tin, đứng thẳng, giọng nói rõ ràng)*

> "Kính chào Thầy và các bạn trong Hội đồng thẩm định.  
> Em là **Diệp Quang Sáng**, đại diện cho **Nhóm 09** gồm 4 thành viên: em, bạn **Nguyễn Đức Nam**, bạn **Đào Đặng Nguyên Khôi** và bạn **Trương Quang Đăng Khoa**.  
> 
> Dưới sự hướng dẫn của **TS. Nguyễn Hồng Hải**, hôm nay nhóm xin phép được báo cáo đề cương nghiên cứu với đề tài:  
> **'Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking for UAV Video'** — tức: *Xây dựng bản đồ ảnh 2D từ video UAV với cơ chế cảnh báo lỗi và tự thích ứng tài nguyên.*"

---

### 🎙️ Slide 2: Bối cảnh thực tế, Bài toán & Mục tiêu nghiên cứu
*(Chuyển sang Slide 2 — Hướng tay chỉ vào 3 khối thẻ: Nhu cầu, Điểm nghẽn, Mục tiêu)*

> "Kính thưa Thầy và Hội đồng, UAV hỗ trợ lập mosaic hiện trạng nhanh cho cứu hộ, giám sát môi trường và nông nghiệp. Tuy nhiên, các giải pháp hiện hữu vẫn có hai điểm nghẽn:
> 
> - **Điểm nghẽn công nghệ:** Các quy trình SfM/3D thương mại thường cần xử lý ngoại tuyến trong thời gian dài. Ghép ảnh 2D tuần tự cổ điển (SIFT/ORB) nhẹ hơn nhưng có thể mất dấu (*catastrophic failure*) hoặc trôi dạt (*drift*) khi camera rung lắc hay cảnh ít vân đặc trưng.
> 
> - **Mục tiêu cốt lõi của nhóm:** Xây dựng pipeline ghép ảnh 2D trên máy tính cá nhân, không bắt buộc GPS/IMU, tự nhận biết rủi ro để điều phối learned matcher khi cần và hạn chế drift tích lũy.
> 
> Sau đây, xin mời bạn **Đào Đặng Nguyên Khôi** sẽ trình bày về quy cách Input/Output và hai tập dữ liệu thực nghiệm của đề tài."

---

## PHẦN 2: INPUT / OUTPUT ➔ DATASET
**Người trình bày:** **Đào Đặng Nguyên Khôi (SE200450)**  
*Thời lượng: ~2.5 phút (Slide 3 $\to$ Slide 4)*

---

### 🎙️ Slide 3: Quy cách dữ liệu đầu vào & Kết quả đầu ra
*(Chuyển sang Slide 3 — So sánh trực quan giữa 2 cột Đầu vào và Đầu ra)*

> "Em xin cảm ơn bạn Sáng. Kính thưa Thầy và Hội đồng, nhóm xác lập quy cách dữ liệu vào và ra như sau:
> 
> - **Về đầu vào (Input):**
>   + Video quang học RGB từ camera UAV góc quay gần thẳng đứng (*near-nadir*), độ dài 100 – 1000 frames.
>   + Khảo sát trên các địa hình tương đối bằng phẳng như đồng ruộng, đô thị và giao thông.
>   + Nhóm **không** bắt buộc phải có GPS/IMU, chỉ dùng telemetry để đối chứng nếu có sẵn.
> 
> - **Về đầu ra (Output):**
>   + Một bản đồ ảnh hiện trạng 2D toàn cảnh ghép liền mạch (*2D mosaic*).
>   + **Ma trận Homography tích lũy:** Lưu biến đổi $H$ từ mỗi frame về hệ tọa độ mosaic để tái lập quá trình ghép và phân tích drift.
>   + Nhật ký chất lượng (số frame, inlier, sai số chiếu lại) và các *submosaic* nếu chuỗi bay không thể khôi phục."

---

### 🎙️ Slide 4: Tập dữ liệu thực nghiệm NPU Drone-Map & DroneZaic
*(Chuyển sang Slide 4 — Chỉ vào 2 khối thẻ kèm hình ảnh minh họa thực địa)*

> "Căn cứ nguyên tắc **RDR-0002**, dữ liệu nghiên cứu phải là nguồn mở và từ drone thật. Nhóm chọn NPU Drone-Map làm tập chính, còn DroneZaic là tập dự phòng và stress-test:
> 
> - **Tập dữ liệu chính — NPU Drone-Map:**
>   + Cung cấp video drone RGB thực tế, ảnh undistorted, file `.SRT`, log GPS và các điểm kiểm soát mặt đất (GCP).
>   + GCP được dùng để đo **GCP RMSE**; **Loop Closure Drift** được dùng riêng để đo độ lệch tích lũy khi quỹ đạo khép vòng.
> 
> - **Tập dữ liệu thử thách & dự phòng — DroneZaic (Dryad):**
>   + Là phương án dự phòng nếu việc truy cập hoặc tải NPU Drone-Map gặp sự cố.
>   + Cảnh nông nghiệp có đặc trưng lặp vân cao, phù hợp để stress-test cơ chế kích hoạt mô hình học sâu và phục hồi vỡ chuỗi.
> 
> Tiếp theo, xin mời bạn **Trương Quang Đăng Khoa** trình bày về phương pháp đánh giá và kiến trúc giải pháp đề xuất."

---

## PHẦN 3: PHƯƠNG PHÁP ĐÁNH GIÁ & ĐỀ XUẤT HƯỚNG GIẢI QUYẾT
**Người trình bày:** **Trương Quang Đăng Khoa (SE201463)**  
*Thời lượng: ~3.0 phút (Slide 5 $\to$ Slide 6)*

---

### 🎙️ Slide 5: Hệ thống chỉ số định lượng, Ground Truth & Baseline đối chứng
*(Chuyển sang Slide 5 — Trình bày mạch lạc 3 nhóm chỉ số và các phương pháp so sánh)*

> "Em xin cảm ơn bạn Khôi. Kính thưa Thầy, nhóm đánh giá khách quan bằng 3 nhóm chỉ số:
> 
> 1. **Sai số hình học:** **GCP RMSE** đo sai số tại GCP; **Loop Closure Drift** đo độ lệch khi quỹ đạo khép vòng.
> 2. **Độ ổn định:** **Tracking Success Rate (%)** và số lần vỡ chuỗi cần phục hồi.
> 3. **Hiệu năng:** Độ trễ **P50 / P95 (ms/frame)** và tỷ lệ frame gọi learned matcher.
> 
> Kết quả được đối chuẩn với *Always-Classical* (SIFT/ORB), *Always-Learned* (SIFT+LightGlue) và pipeline tuần tự của *Hwang et al. (2026)*."

---

### 🎙️ Slide 6: Đề xuất hướng giải quyết — Pipeline 2 tầng thích ứng
*(Chuyển sang Slide 6 — Trình bày 3 trụ cột kỹ thuật của giải pháp)*

> "Pipeline 2 tầng của nhóm gồm 3 cơ chế:
> 
> - **Trụ cột 1 — Phân luồng thích ứng 2 tầng (RQ2):** Mặc định dùng SIFT/ORB; khi Risk Gate báo rủi ro cao, chuyển sang **SIFT + LightGlue**. RQ2 đo đánh đổi chất lượng ghép, độ trễ và tỷ lệ frame gọi learned matcher so với baseline.
> 
> - **Trụ cột 2 — Cổng rủi ro sớm (RQ1):** Dùng tỷ lệ inlier, sai số chiếu lại, độ chồng lấn và độ phân tán không gian để dự báo lỗi đăng ký và drift.
> 
> - **Trụ cột 3 — Phục hồi có kiểm soát (RQ3):** Dưới cùng một trigger, hệ thống loại frame, rematch keyframe hoặc tách submosaic để giới hạn drift.
> 
> Sau đây, xin mời bạn **Nguyễn Đức Nam** sẽ trình bày về đóng góp, kế hoạch 6 tuần và kết luận."

---

## PHẦN 4: ĐỀ XUẤT ĐÓNG GÓP CỦA NHÓM CHO BÀI TOÁN & KẾT LUẬN
**Người trình bày:** **Nguyễn Đức Nam (SE200991)**  
*Thời lượng: ~2.5 phút (Slide 7 $\to$ Slide 8)*

---

### 🎙️ Slide 7: 3 Đóng góp cốt lõi & Kế hoạch thực hiện 6 tuần
*(Chuyển sang Slide 7 — Trình bày rõ ràng giữa 3 Đóng góp và Lộ trình 6 tuần)*

> "Em xin cảm ơn bạn Khoa. Kính thưa Thầy và Hội đồng, đề tài có 3 đóng góp:
> 
> 1. **Phương pháp:** Chính sách phân luồng 2 tầng để đánh giá đánh đổi giữa tài nguyên hạn chế và độ bền vững ở cảnh UAV khó.
> 2. **Khoa học:** Khung đối chuẩn định lượng liên hệ chỉ báo tức thời với drift tích lũy, đồng thời so sánh 3 hành vi phục hồi dưới cùng một trigger.
> 3. **Công cụ:** Pipeline, *Evaluation Harness* và tài liệu kỹ thuật; nhóm dự kiến công bố mã nguồn mở.
> 
> Kế hoạch 6 tuần, từ 21/09 đến 31/10:
> - *Tuần 1:* Đức Nam chuẩn hóa dữ liệu và thiết lập giao thức đo lường.
> - *Tuần 2:* Quang Sáng xây dựng pipeline cơ sở ghép ảnh 2D.
> - *Tuần 3:* Nguyên Khôi mô hình hóa Risk Gate và Matcher Router.
> - *Tuần 4:* Đăng Khoa hoàn thiện recovery và tích hợp hệ thống.
> - *Tuần 5:* Đức Nam và Đăng Khoa chạy thực nghiệm, phân tích số liệu.
> - *Tuần 6:* Cả nhóm tổng hợp kết quả, đóng gói mã nguồn và hoàn thiện báo cáo."

---

### 🎙️ Slide 8: Kết luận đề tài & Lời cảm ơn
*(Chuyển sang Slide 8 — Giọng trang trọng, kết thúc tự tin, hướng về Hội đồng)*

> "Tóm lại, đề tài hướng tới xây dựng mosaic 2D nhanh tại hiện trường, chủ động nhận biết rủi ro và điều phối tài nguyên để hạn chế drift tích lũy.
> 
> Dữ liệu UAV và kế hoạch 6 tuần đã sẵn sàng. Nhóm xin cảm ơn Thầy và Hội đồng, đồng thời mong nhận được câu hỏi và góp ý để hoàn thiện đề cương.
> 
> Xin trân trọng cảm ơn!"

---

### 💡 MẸO PHỐI HỢP THUYẾT TRÌNH CHO CẢ 4 THÀNH VIÊN:
1. **Tác phong sân khấu:** Khi một bạn đang nói, 3 bạn còn lại đứng thẳng, nhìn về phía slide hoặc hướng về Hội đồng, thể hiện sự đồng thuận cao của một tập thể.
2. **Kỹ thuật chuyển giao (Handoff Cues):** Luôn kết thúc bằng câu gọi tên đồng đội: *"Sau đây xin mời bạn [Tên]..."*. Người tiếp theo bước lên nửa bước, gật đầu nhẹ: *"Em xin cảm ơn bạn [Tên]. Kính thưa Thầy và Hội đồng..."*.
3. **Phân chia phần Q&A (Hỏi đáp):**
   - **Bối cảnh, ý nghĩa, tính cấp thiết, bài toán:** $\to$ **Diệp Quang Sáng** trả lời.
   - **Input, Output, đặc tả NPU Drone-Map & DroneZaic:** $\to$ **Đào Đặng Nguyên Khôi** trả lời.
   - **Chỉ số GCP RMSE, Loop Drift, Pipeline 2 tầng, Cổng rủi ro & Phục hồi:** $\to$ **Trương Quang Đăng Khoa** trả lời.
   - **Evaluation Harness, Baseline đối chứng, kế hoạch 6 tuần & đóng góp:** $\to$ **Nguyễn Đức Nam** trả lời.
