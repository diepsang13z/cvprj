# 0003 — Kiểm chứng quy ước `trajectory.txt` và `Plane=` (chẩn đoán cầu nối đo drift)

**Ngày:** 2026-10-13
**Notebook:** `notebooks/04_drift_evaluation.ipynb`
**Kết quả thô:** `notebooks/outputs/04_drift_evaluation/trajectory_check.json`

> ## ĐÍNH CHÍNH (cùng ngày, sau khi đọc mã nguồn tác giả)
>
> Bản đầu của log này kết luận "quy ước phần xoay chưa xác minh" và "residual 6–16 px tăng tới 92 px". **Hai kết luận đó sai vì parser của tôi đọc sai thứ tự quaternion.**
>
> Bằng chứng từ mã nguồn tác giả (`github.com/bushuhui/Map2DFusion`, clone ngày 2026-10-13):
> - `src/main.cpp`: mở `datapath + "/trajectory.txt"`, mỗi dòng đọc `<tên ảnh> <pi::SE3d>`.
> - `PIL/src/base/types/SE3.h`: `operator>>` là `is >> x >> y >> z >> rx >> ry >> rz >> w` ⇒ **quaternion theo thứ tự $(x,y,z,w)$, $w$ ở cuối**.
>
> **Kiểm chứng vật lý:** đọc đúng $(x,y,z,w)$ thì trục quang camera trong hệ world là $(-0{,}03; -0{,}02; -0{,}999)$ — hướng thẳng xuống (nadir). Đọc sai $(w,x,y,z)$ thì trục quang là $(-0{,}03; +0{,}16; +0{,}99)$ — camera "nhìn lên trời", vô lý cho ảnh UAV.
>
> **Hệ quả khi sửa lại:**
>
> | Chỉ số | Đọc sai (bản đầu) | Đọc đúng |
> |---|---|---|
> | Residual cặp tham chiếu | 9,97 px | **0,88 px** |
> | Khoảng cách mặt phẳng tối ưu | 200 m | **194 m** (khớp `Plane=` 193,9 m) |
> | Vai trò của phần xoay | tắt xoay thì tốt hơn ⇒ nghi ngờ | **bật xoay tốt hơn hẳn** (0,88 vs 9,96 px) |
> | Residual theo baseline | 6 px → 92 px | **1 px → 21 px (≈3 m)** |
>
> ⇒ Với `phantom3-village-kfs`, cầu nối **đã kiểm chứng được** và phương án dùng trajectory làm tham chiếu **trở nên khả thi**; nó được giữ làm **phép đối chiếu thứ hai** bên cạnh metric tự nhất quán của `RDR-0007` (vì trajectory là quỹ đạo **do SLAM tác giả tái dựng**, không hoàn toàn độc lập). Với `phantom3-grass-kfs`, cầu nối **vẫn không dùng được**. Các con số trong thân log bên dưới giữ nguyên làm hồ sơ quá trình.

---

## 1. Vì sao phải kiểm chứng

Muốn đo drift tích luỹ thì cần một **tham chiếu độc lập**. Ứng viên duy nhất hiện có là `trajectory.txt` đi kèm gói `-kfs`. Nhưng tài liệu dataset **không ghi rõ**:

- quaternion là camera→world hay world→camera, thứ tự thành phần;
- gốc trục, đơn vị và ý nghĩa của $(t_x, t_y, t_z)$;
- `Plane=` trong `config.cfg` là mặt phẳng gì.

Sai một điểm là mọi con số "drift tính bằng mét" trở nên vô nghĩa, nên nhóm kiểm chứng bằng **đối chất với ảnh** trước khi dùng.

---

## 2. Đã xác minh được

Đối chất: dựng homography chuẩn từ pose, so với homography ghép SIFT + RANSAC trên **cặp frame 0–1 ở độ phân giải gốc**, quét toàn bộ tổ hợp quy ước và khoảng cách mặt phẳng.

| Hạng mục | Kết quả |
|---|---|
| Quy ước quaternion | **camera→world** (thử cả hai chiều, chiều này tốt hơn rõ rệt) |
| Nguồn tâm camera | **$C = t$** (dùng trực tiếp `t`, không qua $-R_{wc}^{\\top}t$) |
| Mặt phẳng đất | `Plane=` của config, cách camera frame 0 **191,8 m** |
| Khoảng cách tối ưu do quét độc lập | **190 m** — khớp với `Plane=` |
| Tỷ lệ chuyển động ảnh/pose | **1,000** (trên 6 cặp kiểm tra) ⇒ `t` là **mét thật** |
| Residual nhỏ nhất cặp 0–1 | **~10 px** (nếu bật thành phần xoay thì tệ hơn: ~12 px) |

Kết luận: **công thức cầu nối là đúng về nguyên lý** — pose mô tả đúng chuyển động và đúng tỷ lệ mét của drone.

---

## 3. Chưa đủ tin cậy để công bố drift

> ⚠️ **Mục này giữ nguyên làm hồ sơ quá trình.** Các số ở đây (residual 6 px → 92 px) là của lần chạy **trước khi sửa thứ tự quaternion** — xem khối **ĐÍNH CHÍNH ở đầu file** để biết số đúng: 1,0 px → 21,2 px (≈3 m), và `village` thực tế **dùng được**.

Ba lý do, đều có số liệu:

1. **Sai số một bước còn lớn và tích luỹ tuyến tính.** Gap 1 frame ≈ 6 px (≈1 m); gap 19 frame ≈ **92 px (≈14 m)**, tăng **15 lần**. Tăng tuyến tính nghĩa là sai số hệ thống từng bước, không phải nhiễu ngẫu nhiên.
2. **Quy ước phần xoay chưa xác minh.** Tắt thành phần xoay lại cho residual nhỏ hơn ⇒ quaternion xoay có thể sai trục/thứ tự hoặc gắn với hệ khác. Chưa kết luận được nó sai ở đâu.
3. **Hai sequence không cùng hệ quy chiếu.**

| Sequence | Tâm camera frame 0 | Cách mặt phẳng z=0 | Bước dịch chuyển/frame | Đánh giá |
|---|---|---|---|---|
| `phantom3-village-kfs` | (−2,6 ; 280,7 ; 166,0), \|C\| = 326 m | 166,0 m | 0,97 – 16,0 m | dùng được về nguyên lý |
| `phantom3-grass-kfs` | (0,0 ; 0,0 ; 0,0) | **0,0 m** (camera nằm trên mặt phẳng) | 0,35 – 1,0 m | **suy biến**, cho số vô nghĩa |

Vì `grass` có gốc toạ độ đặt ngay tại drone và khoảng cách tới mặt phẳng giả định ≈ 0, phép chia $1/d$ trong công thức homography phát nổ — thử nghiệm đầu cho ra "drift" 7,6 triệu pixel cho **cả 7 mô hình**. Đây là lỗi của cầu nối, không phải lỗi mô hình.

**Lưu ý:** ba con số "7,6 triệu pixel" ở trên là **quan sát từ script đo drift đầu tiên, script đó đã bị thay thế** — hiện **không tái lập được từ repo** vì không artifact nào còn lưu giá trị đó. Phần tái lập được là **cơ chế** gây lỗi (mục 6 của notebook: `grass` cách mặt phẳng z=0 đúng 0,0 m), kiểm chứng lại bằng assert trong notebook.

4. **Nguồn gốc pose chưa xác minh.** Cầu nối kiểm được *quy ước* và *tỷ lệ mét*, nhưng **không** kiểm được pose này do thiết bị đo độc lập hay do một hệ tái dựng của tác giả sinh ra. Nếu là hệ tái dựng thì nó không phải ground truth độc lập, và mọi so sánh dựa vào nó bị quy chiếu vòng. Đây là câu hỏi phải hỏi tác giả dataset.

---

## 4. Quyết định cần nhóm chốt (chưa chốt trong log này)

Theo `RULES.md` mục 4, công thức/metric đo drift là quyết định phương pháp, agent không tự chốt. Ba lựa chọn:

1. **Hỏi tác giả dataset** xác nhận quy ước `trajectory.txt` và `Plane=` (email đã ghi ở `notes/datasets.md` mục 5). Rẻ nhất, và là cách duy nhất để số liệu mét có giá trị công bố.
2. **Chuyển sang metric tự nhất quán, không cần ngoại lai:** so $H^{\\text{chuỗi}}_{i \\to 0}$ (tích luỹ tuần tự) với $H^{\\text{trực tiếp}}_{i \\to 0}$ (ghép thẳng frame $i$ với frame 0). Đo đúng sai số tích luỹ, cùng hệ pixel, không phụ thuộc trajectory. Hạn chế: chỉ áp dụng được khi hai frame còn đủ vùng chồng nhau.
3. **Tạm dùng trajectory để so thứ hạng** giữa các mô hình, ghi rõ là tương đối, không quy đổi ra mét. Yếu nhất vì kế thừa toàn bộ sai số đã nêu.

---

## 5. Hệ quả tới kế hoạch

- **Không** đưa bảng drift nào vào báo cáo cho tới khi mục 4 được chốt.
- Phát hiện `efficientloftr` vỡ bản đồ ở `notes/models.md` **vẫn giữ nguyên giá trị**, vì nó dựa trên **ảnh mosaic kiểm tra bằng mắt** và kích thước canvas, không dựa trên trajectory.
- `notebooks/04_drift_evaluation.ipynb` được giữ lại làm **notebook chẩn đoán**: mọi assert trong đó mã hoá các kết luận ở mục 2 và 3, chạy lại là kiểm chứng lại được.
