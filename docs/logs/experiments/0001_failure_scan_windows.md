# 0001 — Quét 160 bước để tìm cửa sổ có lỗi đăng ký thật

Phiên: 2026-10-14 · Người: diepsang13z (agent hỗ trợ) · Loại: nhật ký thực nghiệm

---

## 1. Vì sao phải quét trước khi làm RQ1/RQ2/RQ3

20 frame đầu của `phantom3-village-kfs` và `phantom3-grass-kfs` **không có lỗi đăng ký nào**:
cả 7 mô hình của notebook 03 ghép đủ 20/20 frame (`stopped_at_pair = null`), kể cả mô hình
sau đó bị kết luận là vỡ bản đồ. Nếu đo RQ1/RQ2/RQ3 trên đoạn đó thì:

- chỉ báo rủi ro không bao giờ kích hoạt → RQ2 (phân luồng) và RQ3 (phục hồi) không có ca nào để so;
- ngưỡng chọn được sẽ là ngưỡng "chưa từng gặp lỗi" — vô nghĩa khi đem đi báo cáo.

Vì vậy phải quét dài trước để **chọn cửa sổ có lỗi thật**, rồi mới đo.

## 2. Cách quét

- Matcher đo: SIFT ở độ phân giải làm việc 640 px, 2000 đặc trưng, ratio 0,75, RANSAC 3 px — đúng
  cấu hình tầng nhẹ của pipeline.
- Matcher tham chiếu: SIFT ảnh gốc 1920×1080, 4000 đặc trưng (định nghĩa `RDR-0007`).
- Sai số mỗi bước = khoảng cách trung bình trên 5 điểm mốc (4 góc + tâm, hệ ảnh gốc) giữa
  homography của SIFT-640 và homography tham chiếu của **đúng cặp ảnh đó**.
- Phạm vi: 160 bước liên tiếp cho mỗi sequence (dùng ~1,8 phút/sequence, CPU).

## 3. Kết quả

| Sequence | step_err trung vị | p90 | lớn nhất | inlier tham chiếu (min / trung vị) |
|---|---|---|---|---|
| `phantom3-village-kfs` | 1,37 px | 4,71 px | 11,03 px | 713 / 1613 |
| `phantom3-grass-kfs` | 0,71 px | 1,89 px | 8,75 px | 34 / 452 |

Các bước có sai số > 5 px:

- `village`: 86, 88, 90, 94, 98, 116, 125, 126, 127, 128, 129, 137 — tập trung ở hai cụm 86–98 và 116–137.
- `grass`: 67 (23 inlier), 120 (15 inlier) — cả hai đều là bước có **rất ít đặc trưng**.

## 4. Ba kết luận dùng để thiết kế notebook 05

1. **SIFT-640 không hề "hỏng" trên phần lớn chuỗi.** Trung vị sai số 0,7–1,4 px, tức là ngang mức
   nhiễu của chính nó. Vì vậy "ít đặc trưng" ≠ "ghép sai": trên `grass`, bước 7 chỉ có 34 inlier nhưng
   sai số 0,43 px, trong khi bước 67 có 23 inlier và sai số 5,3 px. Quan hệ **không đơn điệu**, nên
   chỉ báo kiểu `inliers`/`matches` không thể là căn cứ duy nhất.
2. **Lỗi thật có thật, nhưng nằm ở cửa sổ cụ thể.** `village` 80–125 chứa các bước sai 5–11 px;
   `grass` 0–45 chứa các bước mà mô hình học sâu (EfficientLoFTR) sai 5–190 px. Notebook 05 đo
   trên hai cửa sổ này thay vì 20 frame đầu.
3. **Chỉ báo quang học bắt được lỗi, chỉ báo đếm điểm thì không.** Ở `village`, các bước sai 5–11 px
   đi kèm `photo_ncc` (tương phản sau khi ghép) tụt xuống 0,905–0,945 trong khi các bước tốt ở mức
   0,96–0,99. Ở `grass`, EfficientLoFTR vừa báo 2812/2812 điểm khớp với RMSE 0,03 px nhưng sai 5,5 px,
   vừa có bước sai **189 px** — trong khi đó `photo_ncc` của nó tụt còn 0,51–0,69.

## 5. Giới hạn của lần quét này

- Mới có một matcher nhẹ (SIFT) và hai sequence; ORB chưa quét dài.
- "Sai số" ở đây là **đồng thuận với matcher tham chiếu**, không phải sai số so với thực địa
  (kế thừa giới hạn của `RDR-0007`: matcher tham chiếu có sai số riêng, chưa tách được).
- `grass` có bước mà ngay cả tham chiếu cũng chỉ đạt 34 inlier — sát ngưỡng hợp lệ 100 của `RDR-0007`,
  nên các số ở sequence này phải đọc kèm cảnh báo.
