# KỊCH BẢN THUYẾT TRÌNH ĐỀ CƯƠNG NGHIÊN CỨU (RESEARCH PROPOSAL SCRIPT)
## Đề tài: Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking for UAV Video
**Khóa học:** AI2002 | **Nhóm:** 09 | **Thời lượng chuẩn:** 10 – 12 phút  
**Giảng viên hướng dẫn:** TS. Nguyễn Hồng Hải (HaiNH51)

---

### PHÂN CÔNG VAI TRÒ & TIẾN TRÌNH THUYẾT TRÌNH

| STT | Thành viên | Slide phụ trách | Nội dung chính | Thời lượng dự kiến |
| :-: | :--- | :---: | :--- | :---: |
| **1** | **Diệp Quang Sáng** | Slide 1 – 3 | Mở đầu, Đặt vấn đề, Bối cảnh thực tế & Sự cần thiết | ~2.5 phút |
| **2** | **Đào Đặng Nguyên Khôi** | Slide 4 – 5 | Hạn chế của nghiên cứu hiện hành & 3 Câu hỏi cốt lõi (RQ1–3) | ~2.5 phút |
| **3** | **Trương Quang Đăng Khoa** | Slide 6 – 7 | Phạm vi, Tính khả thi & Kiến trúc hệ thống (Pipeline 2 tầng) | ~3.0 phút |
| **4** | **Nguyễn Đức Nam** | Slide 8 – 11 | Thiết lập thực nghiệm, Kế hoạch 6 tuần, Đầu ra & Kết luận | ~3.0 phút |

---

## PHẦN 1: MỞ ĐẦU & TÍNH CẤP THIẾT CỦA ĐỀ TÀI
**Người trình bày:** **Diệp Quang Sáng (SE200655)**  
*Thời lượng: ~2.5 phút (Slide 1 $\to$ Slide 3)*

---

### 🎙️ Slide 1: Giới thiệu đề tài & Nhóm thực hiện
*(Bật Slide 1 — Nền tối, phong thái tự tin, rõ ràng)*

> "Kính chào Thầy và các bạn trong Hội đồng.  
> Em là **Diệp Quang Sáng**, đại diện cho **Nhóm 09** gồm 4 thành viên: em, bạn **Nguyễn Đức Nam**, bạn **Đào Đặng Nguyên Khôi** và bạn **Trương Quang Đăng Khoa**.  
> 
> Dưới sự hướng dẫn của **TS. Nguyễn Hồng Hải**, hôm nay nhóm 09 xin phép được báo cáo đề cương nghiên cứu với đề tài:  
> **'Failure-Aware and Resource-Adaptive 2D Aerial Mosaicking for UAV Video'** — tức: *Xây dựng bản đồ ảnh 2D từ video UAV với cơ chế cảnh báo lỗi và tự thích ứng tài nguyên.*"

---

### 🎙️ Slide 2: Bối cảnh thực tế & Đề xuất giải pháp cốt lõi
*(Chuyển sang Slide 2 — Bấm chỉ vào 3 cột trụ)*

> "Thưa Thầy và Hội đồng, nhu cầu bay UAV để lập bản đồ hiện trạng nhanh trong cứu hộ bão lũ, sạt lở đất hay nông nghiệp chính xác là rất lớn. Tuy nhiên, các giải pháp ghép ảnh tuần tự hiện nay đối mặt với một nghịch lý nan giải:
> 
> - Nếu chỉ dùng **thuật toán cổ điển nhẹ**, hệ thống rất dễ bị mất dấu (*catastrophic failure*) hoặc trôi dạt hình học tích lũy (*drift*) khi bay qua vùng ít vân đặc trưng như mặt nước, đồng ruộng.
> - Ngược lại, nếu lạm dụng **mô hình học sâu (deep matchers)** cho mọi khung hình, máy tính tại hiện trường sẽ bị quá tải ngay lập tức.
> 
> Để giải quyết nghịch lý này, nhóm đề xuất một khung làm việc 2D tích hợp **3 cơ chế trọng tâm**:
> 1. **Dự báo sớm rủi ro (RQ1):** Nhận diện nguy cơ lỗi ngay ở cấp độ từng cặp frame bằng các chỉ báo chi phí thấp.
> 2. **Phân luồng tài nguyên thích ứng (RQ2):** Mặc định chạy giải thuật nhẹ, chỉ tự động kích hoạt mô hình học sâu khi phát hiện nguy cơ cao.
> 3. **Phục hồi có kiểm soát (RQ3):** Hạn chế trôi dạt bằng bộ 3 hành động: loại frame xấu, đối sánh lại với keyframe, hoặc tách cụm ảnh con (*submosaic*)."

---

### 🎙️ Slide 3: Tính cấp thiết & Thực trạng tại Việt Nam
*(Chuyển sang Slide 3 — Chỉ vào 2 cột so sánh)*

> "Nhìn vào thực tế tại Việt Nam hiện nay, hầu hết các đơn vị đều phụ thuộc vào các phần mềm thương mại ngoại tuyến như **Pix4D** hay **Agisoft Metashape**. 
> 
> Quy trình tái tạo 3D/SfM của các phần mềm này rất nặng, đòi hỏi máy trạm đắt tiền, mất từ vài giờ đến cả ngày để xử lý, và bắt buộc phải có GPS RTK độ chính xác cao. Điều này hoàn toàn bất khả thi cho các nhiệm vụ khẩn cấp tại hiện trường.
> 
> Mục tiêu của nhóm **không phải cạnh tranh với phần mềm trắc địa 3D**, mà là: **Tạo ra bản đồ hiện trạng 2D cục bộ nhanh chóng, chạy trực tiếp trên laptop thông thường ngay tại thực địa mà không phụ thuộc GPS đắt tiền.**
> 
> Sau đây, xin mời bạn **Đào Đặng Nguyên Khôi** sẽ phân tích sâu hơn về các điểm nghẽn kỹ thuật và 3 câu hỏi nghiên cứu cốt lõi."

---

## PHẦN 2: HẠN CHẾ CÔNG NGHỆ & 3 CÂU HỎI NGHIÊN CỨU
**Người trình bày:** **Đào Đặng Nguyên Khôi (SE200450)**  
*Thời lượng: ~2.5 phút (Slide 4 $\to$ Slide 5)*

---

### 🎙️ Slide 4: Ba điểm nghẽn kỹ thuật trong các nghiên cứu quốc tế
*(Chuyển sang Slide 4 — Nhấn giọng vào 3 thẻ số 01, 02, 03)*

> "Em xin cảm ơn bạn Sáng. Kính thưa Thầy, qua khảo sát các công bố quốc tế giai đoạn 2023–2026, nhóm nhận thấy 3 điểm nghẽn lớn:
> 
> - **Thứ nhất — Thiếu cơ chế dự báo lỗi sớm:** Các pipeline tuần tự như của Hwang et al. (2026) hay Li et al. (2023) thường chỉ lọc bằng số lượng inlier cố định. Nhưng các nghiên cứu ở CVPR 2024 đã chỉ ra: số inlier cục bộ có tương quan rất yếu với sai số toàn cục và rất dễ bị lừa bởi các vân lặp lại.
> - **Thứ hai — Sự đánh đổi gay gắt về tài nguyên:** Thuật toán cổ điển SIFT/ORB chạy nhanh nhưng mong manh; trong khi learned matcher như LightGlue tuy rất bền bỉ ở cảnh khó nhưng tốn tài nguyên gấp 5–10 lần. Hiện chưa có chính sách định tuyến tự động giữa 2 trường phái này.
> - **Thứ ba — Các cơ chế phục hồi chưa được đối chuẩn thống nhất:** Các hành vi xử lý khi mất dấu như bỏ qua frame, rematch keyframe, hay tách submosaic mới chỉ xuất hiện phân tán, chưa từng được so sánh thực nghiệm dưới cùng một điều kiện kích hoạt."

---

### 🎙️ Slide 5: Mục tiêu & 3 Câu hỏi nghiên cứu cốt lõi (RQ1, RQ2, RQ3)
*(Chuyển sang Slide 5 — Nêu bật từng RQ theo RDR-0003)*

> "Từ 3 điểm nghẽn trên, nhóm đã chính thức xác lập **Mục tiêu tổng quát** và cụ thể hóa thành **3 câu hỏi nghiên cứu cốt lõi**:
> 
> - **RQ1 (Failure Prediction):** *Tổ hợp chỉ báo hình học rẻ nào ở cấp cặp frame—như tỷ lệ inlier, sai số chiếu lại, độ phân tán đặc trưng—có thể dự báo chính xác nguy cơ lỗi đăng ký và drift tích lũy?* Trọng tâm là tìm ra mối tương quan định lượng giữa sai số tức thời và độ méo toàn cục.
> - **RQ2 (Matcher Routing):** *Chính sách phân luồng 2 tầng—mặc định dùng matcher cổ điển, chỉ gọi learned matcher khi rủi ro cao—tối ưu hóa sự đánh đổi giữa chất lượng ghép và độ trễ ra sao so với việc luôn dùng cố định một loại matcher?*
> - **RQ3 (Confidence Recovery):** *Dưới cùng một ngưỡng kích hoạt tin cậy, hành động nào trong 3 lựa chọn: loại frame, rematch keyframe, hay tách submosaic giúp khống chế drift tích lũy hiệu quả nhất?*
> 
> Tiếp theo, xin mời bạn **Trương Quang Đăng Khoa** trình bày về phạm vi thực hiện và kiến trúc hệ thống đề xuất."

---

## PHẦN 3: PHẠM VI, TÍNH KHẢ THI & KIẾN TRÚC HỆ THỐNG
**Người trình bày:** **Trương Quang Đăng Khoa (SE201463)**  
*Thời lượng: ~3.0 phút (Slide 6 $\to$ Slide 7)*

---

### 🎙️ Slide 6: Ranh giới phạm vi & Tính khả thi đề tài
*(Chuyển sang Slide 6 — Đi nhanh qua Scope và nhấn mạnh Feasibility)*

> "Cảm ơn bạn Khôi. Kính thưa Thầy và Hội đồng, để đảm bảo tính tập trung và hoàn thành đúng hạn, nhóm xác lập rõ ranh giới nghiên cứu:
> 
> - **Về phạm vi:** Nhóm tập trung vào chuỗi video UAV quang học góc quay gần thẳng đứng (near-nadir), độ dài 100–1000 frame trên các địa hình tương đối bằng phẳng. Đề tài áp dụng biến đổi đồng dạng 2D tích lũy (Incremental Homography). Nhóm **không** làm tái tạo 3D/SLAM phức tạp và **không** yêu cầu hệ quy chiếu trắc địa tuyệt đối.
> - **Về tính khả thi:** 
>   - *Dữ liệu:* Nhóm sử dụng tập dữ liệu UAV thực tế nguồn mở **NPU Drone-Map** có đầy đủ video, ảnh undistorted, log GPS và các điểm kiểm soát mặt đất GCP để đo sai số. Đồng thời dùng **DroneZaic (Dryad)** làm tập dữ liệu thử thách cho cảnh nông nghiệp lặp vân.
>   - *Hạ tầng:* Toàn bộ pipeline được phát triển trên Python, OpenCV, PyTorch với các model pre-trained sẵn như LightGlue, SIFT, chạy hoàn toàn trên PC cá nhân có GPU thương mại thông thường."

---

### 🎙️ Slide 7: Kiến trúc hệ thống Failure-Aware & Resource-Adaptive Pipeline
*(Chuyển sang Slide 7 — Đi từng bước theo sơ đồ khối từ trái sang phải, trên xuống dưới)*

> "Đây là kiến trúc tổng thể của hệ thống mà nhóm đề xuất. Luồng xử lý được vận hành khép kín theo 4 khối:
> 
> 1. **Đầu vào:** Video UAV được trích xuất frame và hiệu chỉnh méo quang học.
> 2. **Đối sánh cổ điển:** Sử dụng SIFT hoặc ORB trích xuất đặc trưng và tính toán nhanh các chỉ báo bất định ở cấp cặp frame.
> 3. **Cổng rủi ro (Risk Gate — RQ1 & RQ2):** Đây là trái tim của hệ thống. 
>    - Nếu rủi ro thấp, khung hình được tính ma trận Homography $H$ và cập nhật ngay vào mosaic.
>    - Nếu phát hiện rủi ro cao, hệ thống tự động định tuyến sang mô hình học sâu **SIFT + LightGlue** để tìm đối sánh chính xác hơn.
> 4. **Khối phục hồi (Confidence Recovery — RQ3):** Nếu sau khi chạy LightGlue mà chất lượng đối sánh vẫn không đạt độ tin cậy, hệ thống sẽ kích hoạt 1 trong 3 hành vi phục hồi:
>    - *Chiến lược 1:* Bỏ qua frame lỗi nếu camera bị rung lắc tức thời.
>    - *Chiến lược 2:* Đối sánh ngược với Keyframe chuẩn gần nhất.
>    - *Chiến lược 3:* Đóng gói cụm ảnh hiện tại và tách submosaic độc lập nếu chuỗi bị đứt gãy hoàn toàn.
> 
> Nhờ đó, 90% các khung hình thuận lợi chạy trên nhánh cổ điển siêu nhẹ, và chỉ các frame khó mới kích hoạt tài nguyên học sâu và bộ phục hồi.
> 
> Sau đây, xin mời bạn **Nguyễn Đức Nam** trình bày về phương pháp thực nghiệm, kế hoạch 6 tuần và sản phẩm đầu ra."

---

## PHẦN 4: THỰC NGHIỆM, TIẾN ĐỘ 6 TUẦN & KẾT LUẬN
**Người trình bày:** **Nguyễn Đức Nam (SE200991)**  
*Thời lượng: ~3.0 phút (Slide 8 $\to$ Slide 11)*

---

### 🎙️ Slide 8: Thiết lập thực nghiệm & Hệ thống chỉ số đối chuẩn
*(Chuyển sang Slide 8 — Trình bày mạch lạc giữa Baselines và Metrics)*

> "Em xin cảm ơn bạn Khoa. Kính thưa Thầy, để đánh giá khách quan giải pháp đề xuất, nhóm thiết lập một quy trình đối chuẩn định lượng độc lập:
> 
> - **Các phương pháp đối chứng:** Nhóm so sánh hệ thống với 3 baseline:
>   1. *Always-Classical:* Thuần SIFT/ORB cho toàn bộ frame (nhanh nhất nhưng dễ vỡ nhất).
>   2. *Always-Learned:* Chạy SIFT+LightGlue cho 100% frame (chính xác nhất nhưng nặng nhất).
>   3. *Baseline tuần tự của Hwang et al. (2026)* chạy thuần CPU.
> - **3 nhóm chỉ số đánh giá:**
>   - *Sai số hình học:* Đo bằng **GCP RMSE** tại các điểm kiểm soát mặt đất thực tế và **Loop Closure Drift** khi khép vòng bay.
>   - *Độ ổn định:* Đo bằng **Tracking Success Rate (%)** và số lần vỡ chuỗi mosaic.
>   - *Hiệu năng tính toán:* Đo bằng **độ trễ P50/P95 (ms/frame)** và tỷ lệ % khung hình phải gọi learned matcher."

---

### 🎙️ Slide 9: Kế hoạch thực hiện nghiên cứu 6 tuần
*(Chuyển sang Slide 9 — Trình bày dứt khoát từng tuần và phân công)*

> "Kế hoạch nghiên cứu của nhóm kéo dài trong **6 tuần, từ ngày 21/09 đến ngày 31/10**, được phân công rõ ràng cho 4 thành viên:
> 
> - **Tuần 1 (21/9 -> 27/9):** Em (*Đức Nam*) phụ trách chuẩn hóa dữ liệu NPU Drone-Map và dựng khung đo lường tự động (*Evaluation Harness*).
> - **Tuần 2 (28/9 -> 4/10):** Bạn *Quang Sáng* xây dựng pipeline cơ sở ghép ảnh tuần tự 2D dựa trên ma trận homography tích lũy.
> - **Tuần 3 (5/10 -> 11/10):** Bạn *Nguyên Khôi* nghiên cứu mô hình hóa Risk Gate và bộ định tuyến Matcher Router cho RQ1 và RQ2.
> - **Tuần 4 (12/10 -> 18/10):** Bạn *Đăng Khoa* phát triển module phục hồi cho RQ3 và tích hợp hệ thống hoàn chỉnh.
> - **Tuần 5 (19/10 -> 25/10):** Em và bạn *Khoa* phối hợp chạy thực nghiệm diện rộng trên toàn bộ dữ liệu NPU và tập stress-test DroneZaic.
> - **Tuần 6 (26/10 -> 31/10):** Cả nhóm tổng hợp phân tích kết quả, đóng gói mã nguồn mở và hoàn thiện Báo cáo nghiên cứu tổng kết."

---

### 🎙️ Slide 10: Kết quả dự kiến & Đóng góp của đề tài
*(Chuyển sang Slide 10 — Nêu rõ 3 kết quả cụ thể)*

> "Đề tài cam kết mang lại **3 kết quả đầu ra cụ thể**:
> 1. **Khung phần mềm mã nguồn mở:** Toàn bộ pipeline ghép ảnh 2D tự thích ứng cùng bộ công cụ đo kiểm tự động, có tài liệu hướng dẫn tái lập thực nghiệm đầy đủ.
> 2. **Bộ dữ liệu đo chuẩn (Benchmark):** Tập số liệu định lượng chi tiết giải đáp trọn vẹn 3 câu hỏi nghiên cứu RQ1, RQ2 và RQ3.
> 3. **Báo cáo & Ấn phẩm khoa học:** Một báo cáo tổng kết đề tài hoàn chỉnh và một bản thảo bài báo khoa học sẵn sàng gửi hội nghị hoặc tạp chí chuyên ngành."

---

### 🎙️ Slide 11: Kết luận & Mời Hội đồng hỏi đáp (Q&A)
*(Chuyển sang Slide 11 — Giọng trang trọng, kết thúc tự tin)*

> "Tóm lại, đề tài của nhóm tập trung vào tính ứng dụng thực tế: **Tạo bản đồ ảnh 2D nhanh tại hiện trường, chủ động nhận biết rủi ro và điều phối tài nguyên thông minh để khống chế sai số tích lũy.**
> 
> Với sự chuẩn bị kỹ lưỡng về cơ sở lý thuyết, dữ liệu thực tế đã sẵn sàng và kế hoạch 6 tuần phân bổ chặt chẽ, nhóm 09 tự tin sẽ hoàn thành tốt đề tài.
> 
> Nhóm em xin chân thành cảm ơn Thầy và các bạn đã chú ý lắng nghe. Nhóm rất mong nhận được những câu hỏi và ý kiến đóng góp quý báu từ Thầy và Hội đồng để đề tài được hoàn thiện hơn.  
> Xin trân trọng cảm ơn!"

---

### 💡 MẸO PHỐI HỢP THUYẾT TRÌNH CHO CẢ 4 THÀNH VIÊN:
1. **Ánh mắt & Tác phong:** Khi bạn mình đang nói, 3 bạn còn lại đứng ngay ngắn, nhìn về phía slide hoặc hướng về Hội đồng, tuyệt đối không bấm điện thoại hay nói chuyện riêng.
2. **Kỹ thuật chuyển giao (Handoff Cues):** Luôn nói to câu chuyển người: *"Sau đây xin mời bạn [Tên] sẽ trình bày về..."*. Người tiếp theo bước lên nửa bước, gật đầu nhẹ: *"Em xin cảm ơn bạn [Tên]. Kính thưa Thầy và Hội đồng..."* giúp bài nói liền mạch như một dòng chảy chuyên nghiệp.
3. **Phân chia phần Q&A (Hỏi đáp):**
   - Câu hỏi về **Bối cảnh, ý nghĩa, tính cấp thiết:** $\to$ **Diệp Quang Sáng** trả lời.
   - Câu hỏi về **RQ1, RQ2, công thức chỉ báo rủi ro, LightGlue vs Classical:** $\to$ **Đào Đặng Nguyên Khôi** trả lời.
   - Câu hỏi về **Pipeline, ma trận Homography, cơ chế phục hồi RQ3:** $\to$ **Trương Quang Đăng Khoa** trả lời.
   - Câu hỏi về **Dataset NPU, GCP RMSE, đo lường độ trễ, tiến độ 6 tuần:** $\to$ **Nguyễn Đức Nam** trả lời.
