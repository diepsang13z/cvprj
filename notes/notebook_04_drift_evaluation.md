# Giải thích Notebook 04: Làm sao biết mô hình nào bị "trôi" bản đồ?

Tài liệu giải thích file `notebooks/04_drift_evaluation.ipynb` theo ngôn ngữ bình dân, trực quan cho sinh viên.

| Trường | Giá trị |
|---|---|
| Ngày | 2026-10-13 |
| Trạng thái | Ghi chú nội bộ, chưa qua phản biện |
| File thực nghiệm | `notebooks/04_drift_evaluation.ipynb` |
| Kết quả sinh ra | `notebooks/outputs/04_drift_evaluation/` (2 file JSON) |
| Muốn đọc bản kỹ thuật | `docs/logs/datasets/0003_trajectory_pose_verification.md` |
| Quyết định phương pháp | `docs/decisions/RDR-0007_drift_metric_choice.md` |

---

## 1. Vấn đề cần giải (kể chuyện cho dễ hiểu)

Notebook 03 đã cho ra bản đồ của 7 mô hình. Nhưng câu hỏi thật của đề tài là:

> **"Sau khi ghép 20 tấm ảnh liên tiếp, mô hình nào bị lệch ít nhất?"**

Muốn biết "lệch bao nhiêu" thì phải có **thước đo**. Nhóm có sẵn file `trajectory.txt` (ghi vị trí drone theo từng frame, đơn vị **mét**), nhưng pipeline ghép ảnh lại làm việc bằng **pixel**.

> **Ví dụ dễ hiểu:** bạn có bản đồ giấy đo bằng pixel, còn GPS ghi bằng mét. Muốn so hai thứ với nhau, bạn phải biết **1 pixel trên bản đồ tương ứng bao nhiêu mét ngoài đời**. Công thức quy đổi đó gọi là **"cầu nối"**.
> Nếu cầu nối sai → mọi con số "lệch bao nhiêu mét" đều là **số rác**.

Notebook 04 làm hai việc:
1. **Kiểm tra cầu nối trước** (mục 1–7) — xem có tin được không.
2. **Đo độ lệch thật** (mục 8–10) — bằng cách đo không cần `trajectory.txt`.

---

## 2. Việc 1: Kiểm tra "cầu nối" có đáng tin không?

**Cách kiểm tra rất đơn giản về ý tưởng:**
- Lấy **một cặp ảnh thật**, ghép bằng SIFT (thuật toán chuẩn, sai số nhỏ) → biết được "ảnh 2 lệch ảnh 1 bao nhiêu **pixel**".
- Lấy `trajectory.txt` của đúng hai ảnh đó → suy ra "drone đã bay bao nhiêu **mét**" → quy đổi ra pixel bằng cầu nối.
- **Hai con số phải khớp nhau.** Khớp = cầu nối đúng.

### Phát hiện lớn: nhóm đọc sai thứ tự của quaternion

File `trajectory.txt` mỗi dòng có 7 số: 3 số vị trí + 4 số **quaternion** (mô tả camera đang xoay hướng nào).

> **Ví dụ dễ hiểu:** quaternion giống như mô tả "số nhà" gồm 4 phần. Nhóm đọc theo thứ tự `w, x, y, z`, nhưng tác giả dataset viết theo thứ tự `x, y, z, w` — tức là **đọc lộn ngược**. Kết quả: camera bị hiểu thành đang **chĩa lên trời** thay vì **chĩa xuống đất**.

Sửa lại thì mọi thứ khớp:

| Chỉ số | Đọc sai | Đọc đúng (như tác giả) |
|---|---|---|
| Sai số khi ghép 1 cặp ảnh | 9,97 pixel | **0,88 pixel** |
| Camera nhìn hướng nào | "lên trời" (vô lý) | **thẳng xuống đất** (đúng) |
| Khoảng cách từ camera tới mặt đất | 200 m | **194 m** (khớp với config 193,9 m) |
| Dùng phần "xoay" của pose | làm sai số tăng | **làm sai số giảm** |

**Cách tìm ra lỗi:** nhóm tải **mã nguồn C++ của chính tác giả dataset** (`Map2DFusion` trên GitHub) và đọc xem họ ghi/đọc file này thế nào. Trong code ghi rõ thứ tự đọc là `x y z` rồi mới tới `w`.

---

## 3. Việc 1 (tiếp): Cảnh nào dùng được, cảnh nào không?

| Cảnh | Kết quả | Giải thích dễ hiểu |
|---|---|---|
| `phantom3-village-kfs` (ruộng đồng) | **Dùng được** | Sai số cầu nối chỉ 0,88 pixel cho 1 cặp, và khoảng 3 mét nếu ghép liền 19 bước |
| `phantom3-grass-kfs` (bãi cỏ) | **Không dùng được** | File toạ độ của cảnh này đặt gốc ngay tại drone, mặt đất cách 0 mét → công thức chia cho ~0 nên "nổ" ra số vô nghĩa |

**Tại sao vẫn chưa dùng `trajectory.txt` để chấm điểm chính thức:** trang dự án của tác giả ghi họ dùng **SLAM** (thuật toán tự ước lượng vị trí từ ảnh) để tạo ra file này — tức nó **cũng suy ra từ ảnh**, không phải thiết bị GPS đo độc lập. Dùng nó làm "đáp án chuẩn" để chấm các phương pháp chạy bằng ảnh thì **không công bằng** (tự chấm bài mình). Nó chỉ nên dùng để **đối chiếu chéo**.

---

## 4. Việc 2: Đo độ lệch mà KHÔNG cần file toạ độ

Vì cầu nối chỉ dùng được cho 1 cảnh, nhóm chọn cách đo khác — **không cần dữ liệu bên ngoài**:

> **Ý tưởng:** tưởng tượng bạn đi từ nhà tới trường.
> - **Đi thẳng:** ghép trực tiếp ảnh số 19 về ảnh số 0 (1 lần ghép).
> - **Đi vòng:** ghép dồn 0→1→2→…→19 (19 lần ghép, mỗi lần sai một chút).
> - Nếu đi vòng mà tới đúng chỗ như đi thẳng → chuỗi ghép tốt. Lệch bao nhiêu pixel chính là **độ trôi (drift) tích luỹ**.

Cách này đo được cho cả 2 cảnh, mọi mô hình, và mỗi frame đều có một con số.

---

## 5. Kết quả đo độ trôi

Đơn vị là **pixel trên ảnh gốc** (ảnh 1920×1080). Cột "mức nền" giải thích ở mục 6.

| Cảnh | Mô hình | Đo được tới frame | Trôi cuối (px) |
|---|---|---|---|
| `village` | **efficientloftr** | 19 | **1311** |
| `village` | orb_bf | 19 | 73 |
| `village` | superpoint_lightglue | 19 | 61 |
| `village` | sift_lightglue / xfeat_lighterglue / xfeat_mnn | 19 | 47 / 48 / 40 |
| `village` | **sift_bf (mức nền)** | 19 | **47** |
| `grass` | **efficientloftr** | 6 | **63** |
| `grass` | xfeat_mnn | 6 | 8,7 |
| `grass` | 4 mô hình còn lại | 6 | 1,7 – 3,4 |
| `grass` | **sift_bf (mức nền)** | 6 | **1,7** |

---

## 6. Cách đọc bảng kết quả (phần quan trọng nhất)

**1. `efficientloftr` hỏng thật, và giờ có số chứng minh.**
Nó trôi **1311 px** ở cảnh ruộng (gấp **28 lần** mức nền) và **63 px** ở cảnh cỏ (gấp **37 lần**). Con số này khớp với việc mắt thường đã thấy bản đồ của nó bị "vỡ" ở Notebook 03.

**2. "Mức nền" là gì?**
Mọi mô hình đều được chấm bằng **cùng một thước đo là SIFT**. Nên dòng `sift_bf` chính là **độ nhiễu của chính cái thước** — nó không phải một mô hình để so thắng thua.
Ví dụ: nếu cái cân đã tự sai 47 gram thì không thể nói món A (40 g) nhẹ hơn món B (73 g) một cách chắc chắn.

**3. Vì sao KHÔNG xếp hạng 6 mô hình còn lại?**
Sáu mô hình tốt có độ trôi 40–73 px, mà **mức nền đã là 47 px** — chênh lệch giữa chúng còn nhỏ hơn sai số của thước. Muốn xếp hạng phải làm thước chính xác hơn (ghép nhiều frame hơn, hoặc chạy lặp nhiều lần).

**4. Vì sao `grass` chỉ đo được tới frame 6?**
Ghép trực tiếp ảnh 0 với ảnh thứ 7 trở đi không còn đủ điểm khớp (dưới 100 điểm). Bản thân điều này đã cho thấy **cảnh cỏ khó hơn cảnh ruộng** — đúng như nhóm dự đoán ban đầu.

---

## 7. Hai bài học đáng nhớ

**Bài học 1 — Số đẹp ở từng cặp chưa chắc đúng cho cả bản đồ.**
`efficientloftr` ghép từng cặp ảnh rất "đẹp": hơn 2.600 điểm khớp, sai số nhỏ. Nhưng sai số nhỏ đó **cộng dồn qua 19 bước** thì bản đồ vỡ hoàn toàn. Vì vậy chỉ nhìn điểm khớp của từng cặp là **không đủ** để kết luận — đây chính là lý do đề tài đặt ra câu hỏi nghiên cứu RQ1.

**Bài học 2 — Khi mọi mô hình cho cùng một con số, hãy nghi cái thước trước.**
Lần chạy đầu tiên, cả 7 mô hình đều ra "trôi 7,6 triệu pixel" — gần như giống hệt nhau. Con số đó vô lý: nếu mô hình tốt lẫn xấu đều ra một kết quả thì thước đo đang đo sai, chứ không phải các mô hình giống nhau.
Nguyên nhân: cảnh cỏ có mặt đất cách camera 0 mét → công thức nhân/chia cho ~0 nên "nổ". Nhóm **đã xoá bảng số sai đó** khỏi notebook để người đọc sau không tưởng nhầm là đã đo được kết quả.

*(Ba con số 7,6 triệu px đó là quan sát từ đoạn code cũ đã bị thay thế và không tái lập được từ repo; phần kiểm chứng lại được là **nguyên nhân gây lỗi** — mục 6 của notebook in ra đúng dòng "cảnh grass cách mặt phẳng 0,00 m".)*

---

## 8. Kết quả nằm ở đâu & tự kiểm chứng lại thế nào?

Bấm **Run All** → kết quả lưu ở `notebooks/outputs/04_drift_evaluation/`:
- `trajectory_check.json` — kết quả kiểm tra cầu nối.
- `drift_selfconsistent.json` — bảng độ trôi của 7 mô hình.

Notebook có sẵn các **assert tự kiểm tra** — chạy lại là biết đúng/sai ngay, không cần tin lời:
- Nếu đọc sai thứ tự quaternion → sai số sẽ vọt lên, assert báo lỗi.
- Nếu cái thước bị sai (ví dụ truyền sai tham số) → dòng mức nền sẽ vọt lên, assert báo lỗi.

*(Chuyện có thật: lần chạy đầu của phần đo drift, mức nền SIFT là **1578 px** — vô lý. Hoá ra nhóm **truyền sai thứ tự tham số** nên phép biến đổi bị lộn ngược, mà độ lớn dịch chuyển vẫn khớp 0,999 nên nhìn số không thấy gì. **Chính assert "mức nền phải nhỏ" đã bắt được lỗi này.**)*

---

## 9. Tóm tắt 1 câu

> **Notebook 04 làm hai việc: (1) kiểm tra "cầu nối" giữa file toạ độ drone và ma trận pixel — phát hiện nhóm đọc sai thứ tự quaternion, sửa xong thì cảnh ruộng dùng được (sai số 0,88 px) còn cảnh cỏ thì hỏng; (2) đo độ trôi bản đồ bằng cách so "ghép dồn" với "ghép thẳng" — kết quả `efficientloftr` vỡ bản đồ gấp 28–37 lần mức nhiễu, còn 6 mô hình kia chưa đủ cơ sở để xếp hạng.**
