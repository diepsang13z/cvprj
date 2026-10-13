# Giải thích Notebook 02: Dùng AI hiện đại (LightGlue) ở độ phân giải gốc

Tài liệu giải thích file `notebooks/02_lightglue_pilot.ipynb` theo ngôn ngữ bình dân, trực quan cho sinh viên.

---

## 1. File này sinh ra để làm gì?

Ở Notebook 01, chúng ta dùng thuật toán cổ điển. Nhưng nếu drone bay nhanh, bị nghiêng camera, hoặc mặt đất ít chi tiết (mặt cỏ, mặt nước) thì thuật toán cổ điển rất dễ bị nối nhầm điểm.
Notebook 02 mang **mô hình AI hiện đại nhất hiện nay (LightGlue)** về để thử nghiệm:

- **Giữ nguyên kích thước ảnh gốc cực nét** ($1920 \times 1080$ pixel, không nén, không thu nhỏ).
- Xem thử AI có nối điểm thông minh hơn thuật toán cổ điển hay không và đo xem AI chạy nặng/chậm hơn bao nhiêu lần.

---

## 2. Các mô hình AI được mang vào thử nghiệm

Notebook kết hợp 2 cặp công nghệ:

1. **Cặp 1: SIFT + LightGlue (Kiểu con lai)**
   - Dùng SIFT của OpenCV để tìm điểm (nhẹ).
   - Nhưng khâu nối điểm thì giao cho AI **LightGlue** (mô hình Transformer) phán đoán xem điểm nào thuộc về điểm nào.
2. **Cặp 2: SuperPoint + LightGlue (Kiểu AI toàn phần)**
   - Giao toàn bộ cho AI: mạng nơ-ron **SuperPoint** tự soi ảnh tìm điểm $\rightarrow$ mạng nơ-ron **LightGlue** tự nối điểm.

---

## 3. Các bước chạy trong code (Từng bước làm gì?)

Notebook chia thành 2 phần rõ rệt:

### Phần 1: So găng trên từng cặp ảnh lẻ (Pair-matching)

- Lấy 3 cặp ảnh đầu tiên đem ra đối đầu.
- So sánh xem trên cùng 1 cặp ảnh chụp từ drone:
  - AI tìm được bao nhiêu điểm khớp?
  - Mất bao nhiêu giây để AI tính toán xong?
- Vẽ ra bức ảnh có các đường nối xanh lá cây để mắt người nhìn vào thấy ngay AI đang nối điểm chuẩn cỡ nào.

### Phần 2: Dựng bản đồ lớn ở độ phân giải gốc (Full Mosaic)

- Không chỉ dừng lại ở việc nối 2 ảnh lẻ, code tiếp tục lấy chuỗi 20 bức ảnh gốc siêu nét ($1920 \times 1080$) nối liên hoàn từ ảnh 1 đến ảnh 20.
- Tự động tính toán khung tranh khổng lồ (~$1940 \times 1850$ pixel) và dán đè các frame lên nhau.
- Vẽ ngay bức ảnh bản đồ hoàn chỉnh lên màn hình notebook để sinh viên nhìn thấy trực tiếp.

---

## 4. Kết luận quan sát được từ Notebook này

- **Độ chính xác:** Cả 2 bản đồ ghép ra đều cực kỳ thẳng hàng, không bị méo mó hay nhân đôi nhà cửa ruộng đồng. Tỷ lệ phủ kín đạt tận 98.7% - 98.8%.
- **Về tốc độ (Cái giá phải trả cho AI):**
  - Cặp con lai (`SIFT + LightGlue`): Chạy 20 frame mất **~17 giây** trên CPU. Tương đối ổn.
  - Cặp AI toàn phần (`SuperPoint + LightGlue`): Chạy 20 frame mất tận **~134 giây (hơn 2 phút)** trên CPU!
    $\rightarrow$ Điều này chứng minh nhận định của nhóm trong đề tài là hoàn toàn đúng: **Nếu bắt drone chạy AI toàn phần mọi lúc mọi nơi thì máy tính sẽ bị quá tải ngay lập tức.**

---

## 5. Kết quả đầu ra nằm ở đâu?

Kết quả được lưu tại `notebooks/outputs/02_lightglue_pilot/phantom3-village-kfs/`:

- `sift_lightglue_matches.png` & `superpoint_lightglue_matches.png`: Ảnh nối điểm màu sắc trực quan của 2 ảnh đầu.
- `mosaic_sift/mosaic.png`: Bản đồ toàn cảnh 20 frame ghép bằng SIFT + LightGlue ở độ phân giải gốc.
- `mosaic_superpoint/mosaic.png`: Bản đồ toàn cảnh 20 frame ghép bằng SuperPoint + LightGlue ở độ phân giải gốc.
- `metrics.json`: Nhật ký đo đạc thời gian và số điểm inlier.

---

## 6. Tóm tắt 1 câu

> **Notebook 02 là thí nghiệm mang AI xịn (LightGlue) vào chạy trên ảnh drone nét gốc ($1920 \times 1080$), chứng minh AI ghép cực chuẩn nhưng ngốn tài nguyên khủng khiếp (chậm hơn cả chục lần so với thuật toán thường).**
