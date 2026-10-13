# Giới thiệu dataset NPU Drone-Map (bộ dữ liệu team sẽ dùng)

**Mục đích:** hồ sơ giới thiệu bộ dữ liệu chính của đề tài — xuất xứ, nội dung, metadata, giới hạn cần biết trước khi thiết kế thí nghiệm. Bổ trợ cho [`notes/datasets.md`](../../../notes/datasets.md) (kế hoạch tải 14 gói) và `RDR-0005` (quyết định chọn dataset).
**Ngày kiểm chứng:** 2026-10-13. **Nguồn:** `adv-ci.com/blog/` (trang chủ tác giả), trang dataset, bài IROS 2016, Li et al. 2023.

---

## 1. Xuất xứ

- **Tác giả:** Shuhui Bu (布树辉) — giáo sư ĐH Công nghiệp Tây Bắc (Northwestern Polytechnical University, NWPU), Trung Quốc; MSc/PhD ĐH Tsukuba (Nhật), cựu trợ giảng ĐH Kyoto. Hướng nghiên cứu: cảm nhận & điều khiển UAV, thị giác máy tính, học máy. Website: `adv-ci.com/blog`.
- **Nhóm nghiên cứu:** PI-LAB (Pilot Intelligent Laboratory, NWPU) — cùng nhóm với GSLAM (ICCV 2019), SDTAM (2016), TerrainFusion (IROS 2019), PointFusion (IROS 2020).
- **Bộ dữ liệu ra đời để đánh giá Map2DFusion** — hệ ghép bản đồ 2D incremental bằng monocular SLAM, được nhóm giới thiệu là công trình đầu tiên dùng visual SLAM sinh bản đồ 2D realtime:
  > Shuhui Bu, Yong Zhao, Gang Wan, Zhenbao Liu. "Map2DFusion: Real-time Incremental UAV Image Mosaicing based on Monocular SLAM." *IEEE/RSJ IROS*, 2016.
- Sequence cập nhật lần cuối **18/04/2016**; trang dataset tuyên bố "over 100GB data and more captured sequences will be added" — thực tế **không còn bổ sung**: bản public hiện chỉ có **14 gói keyframes (~4.3 GB)**, phần video gốc/đầy đủ chưa từng được phát hành.

## 2. Nội dung bộ dữ liệu

14 sequence, 3 nền tảng bay:

| Nền tảng | Số sequence | Sequence |
|---|---|---|
| DJI Phantom 3 (advanced) | 10 | village, huangqi, factory, grass, centralPark, freeway, lowlower, ieu, npu, highflower |
| Hexacopter tự chế + GoPro Hero3+ | 3 | gopro-npu, gopro-monticules, gopro-saplings |
| DJI Inspire 1 | 1 | inspire1-rail |

- **Cảnh trải rộng:** khuôn viên đại học, công viên, đồng ruộng ven sông, khu nhà xưởng, cao tốc, bãi cỏ ít vân, hành lang đường sắt.
- **Quy mô bản public:** ~400 frame/gói, ảnh **1920×1080** (đo trực tiếp từ `data/sample/`), tổng ~7.000 keyframe / 4.3 GB. Ảnh sinh ra từ frame video đã undistort (không phải ảnh still của camera).
- **Ngữ cảnh bay** — chỉ 3 sequence có số liệu công bố (Li et al. 2023, Bảng 2):

| Sequence | Độ cao bay tối đa | Diện tích mặt đất | Số frame |
|---|---|---|---|
| phantom3-village | 196.6 m | 0.932 km² | 406 |
| phantom3-huangqi | 222.3 m | 1.313 km² | 393 |
| phantom3-factory | 181.8 m | 0.782 km² | 406 |

→ Bay cao 180–220 m, camera gimbal gần nadir, cảnh phẳng — đúng regime giả định homography của đề tài. Dùng các số liệu này để tính trước GSD và ước lượng số frame cần cho mỗi cấu hình thí nghiệm (công thức cần tiêu cự/FOV — lấy từ `config.cfg` khi tải xong; chưa chốt con số ở đây).

## 3. Định dạng & metadata

Ba định dạng cho mỗi sequence (theo mô tả trang chủ dataset):

| Định dạng | Nội dung | Public? |
|---|---|---|
| original | video gốc (`.MOV`/`.MP4`), `.SRT`, `log.DAT`, waypoints, `flight.cfg` | Không |
| unified | toàn bộ frame undistorted (`rgb/`) + `frames.txt` + `gps.txt` (GPS thô) | Không |
| **keyframes** (`-kfs`) | `rgb/` ảnh undistorted + `trajectory.txt` (pose R+t từng keyframe) + `config.cfg` | **Có — bản dùng chính** |

- **GCP** (`<sequence>-GCPs.zip`) chỉ có ở một số sequence — cũng không public.
- **Điểm mạnh cho đề tài:** ảnh đã undistort sẵn (bỏ bước hiệu chuẩn/sửa méo); có `trajectory.txt` làm **pose ground truth** để đo drift tích luỹ.
- **Điểm thiếu:** không có mosaic ground truth; không có nhãn "ca ghép lỗi" (phải tự sinh cho RQ1); không có license chuẩn.
- **Chưa kiểm chứng trực tiếp nội dung archive** (Baidu chặn tải ngoài client): mô tả `rgb/` + `trajectory.txt` + `config.cfg` là theo trang chủ dataset, chưa mở file thật. Xác nhận lại ngay khi tải xong gói keyframe đầu tiên.

## 4. Đề tài dùng bộ này thế nào

- Xem `RDR-0005` (dataset duy nhất của đề tài) và [`notes/datasets.md`](../../../notes/datasets.md) (thứ tự tải 3 tầng, tổng 4.3 GB).
- **RQ1 (dự báo lỗi):** cần cặp frame khó — `grass` (ít vân), `centralPark` (lặp vân tán cây), `freeway` (dải tuyến tính) — để có tỉ lệ lỗi thực đáng phân tích.
- **RQ2 (phân luồng matcher):** đo latency ↔ chất lượng trên cùng tập frame, đối chiếu classical với learned.
- **RQ3 (phục hồi):** cần đoạn quay gắt / mất dấu cục bộ — ưu tiên `centralPark`, `lowlower`.
- **Đối chiếu văn liệu:** chạy lại trên `village`/`huangqi`/`factory` để so được với baseline Li et al. 2023 (bài này chọn đúng 3 sequence đó từ bộ NPU).
- Bộ dữ liệu **không kèm mosaic tham chiếu** → cách đánh giá chất lượng ghép (chỉ số nội tại, đối chiếu pose GT, so sánh tương đối giữa cấu hình) là quyết định phương pháp: cần ghi `RDR` trước khi chốt (RULES §4).

## 5. Giới hạn cần biết trước khi thiết kế thí nghiệm

- **Không license** → chỉ dùng nội bộ cho nghiên cứu, không phát hành lại; bản lưu trên cloud phải để chế độ private.
- **Keyframe đã được tác giả lọc sẵn:** khoảng cách giữa frame lớn hơn video gốc → chạy trên keyframe "dễ thở" hơn chạy realtime trên chuỗi video liên tục; mọi kết luận về routing/latency phải nói rõ là đo trên keyframe.
- **Điều kiện bay lý tưởng** (cao 180–220 m, gimbal, cảnh phẳng) → parallax thấp, gần như không có vật thể cao; không đại diện cho bay thấp / địa hình gồ ghề ⇒ hạn chế khả năng ngoại suy kết quả.
- **Tuổi dữ liệu:** 2016, video 1080p — chất lượng và độ phân giải thấp hơn chuẩn hiện nay.
- Trang dataset **không công bố bảng thống kê per-sequence** (độ cao, số frame) cho toàn bộ 14 sequence; chỉ 3 sequence có số liệu qua Li et al. 2023.

## 6. Nguồn kiểm chứng

- `adv-ci.com/blog/` — trang chủ tác giả: tiểu sử, hướng nghiên cứu, danh mục công trình (Map2DFusion IROS 2016, GSLAM ICCV 2019, TerrainFusion IROS 2019, PointFusion IROS 2020).
- `adv-ci.com/blog/source/npu-drone-map-dataset/` — mô tả dataset: phần cứng, 3 định dạng, GCP, camera params, link Baidu (`mji5`), liên hệ tác giả.
- `adv-ci.com/blog/projects/map2dfusion/` — trang dự án; video demo dùng `phantom3-village` (có GPS), `phantom3-grass` (cảnh khó), `gopro-npu`.
- Thumbnail sequence: `adv-ci.com/blog/source/npu-drone-map-dataset/images/npu-dronemap-images1.png` và `...-images2.png`.
- Li et al. 2023, *Remote Sensing* 15(8):2127 — Bảng 1 (camera), Bảng 2 (thông số 3 sequence).
- Kiểm tra cục bộ: `data/sample/rgb01` — 406 ảnh 1920×1080, MD5 trùng hoàn toàn với `rgb02`.
