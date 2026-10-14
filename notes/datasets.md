# Dataset & Kế hoạch tải (NPU Drone-Map)

Tổng hợp toàn bộ dataset liên quan tới dự án, nội dung từng gói dữ liệu và thứ tự tải tối ưu trong ngân sách ~10 GB. Kiểm chứng ngày **2026-10-13**.

Hồ sơ giới thiệu bộ dataset (xuất xứ, nội dung, metadata, giới hạn): [`docs/logs/datasets/0002_npu_dronemap_intro.md`](../docs/logs/datasets/0002_npu_dronemap_intro.md).

---

## 1. Kết luận nhanh (TL;DR)

- **Chỉ có 1 dataset trong phạm vi dự án:** NPU Drone-Map (đã chốt tại `RDR-0005`). Trang `adv-ci.com/blog/source/` có 2 mục dataset, nhưng chỉ mục này liên quan (mục còn lại — NPU RGB-D — là dữ liệu **trong nhà**, Kinect, ngoài phạm vi).
- **Nguồn tải public duy nhất:** Baidu Pan → thư mục `NPU_Dronemap`, gồm **14 file `*-kfs.tar.gz`**, tổng **~4.29 GB**.
- **"Cả ảnh và metadata" = gói `-kfs`.** Mỗi gói chứa `rgb/` (ảnh undistorted) + `trajectory.txt` (pose R+t từng keyframe) + `config.cfg` (thông số camera) — theo mô tả định dạng "sequence keyframes" trên trang chủ dataset.
- **Với ngân sách 10 GB: tải hết 14 file vẫn dư ~5.7 GB.** Nút thắt thật sự là *tốc độ Baidu* (đang tải chỉ ~60 KB/s → 4.3 GB mất nhiều giờ), không phải dung lượng. Phần dư để dành cho mosaic output, checkpoint, log.

Link tải (hai link **cùng một nội dung**, 14 file như nhau):

| Link | Mật khẩu | Ghi chú |
|---|---|---|
| `https://pan.baidu.com/s/1EvIy4W08G-L38PPDa2MdXA` | `tm5q` | Link đang dùng |
| `https://pan.baidu.com/s/18Wr4UZLiPV-400NeZWeVRw` | `mji5` | Link ghi trên trang chủ dataset |

---

## 2. Bảng 14 gói dữ liệu (tải về nguyên trạng, không cần chọn lọc thêm)

| # | File | Size | Camera | Cảnh (thumbnail dataset; *[suy đoán]* = chỉ đoán từ tên file) | Vai trò trong dự án |
|---|---|---|---|---|---|
| 1 | `phantom3-village-kfs.tar.gz` | 251.9 MB | Phantom 3 | Đồng ruộng ven sông, chia thửa rõ | **Baseline đối chiếu Li et al. 2023** |
| 2 | `phantom3-huangqi-kfs.tar.gz` | 253.0 MB | Phantom 3 | Ruộng dải dài | **Baseline đối chiếu Li et al. 2023** |
| 3 | `phantom3-factory-kfs.tar.gz` | 228.3 MB | Phantom 3 | Khu nhà xưởng, khối kiến trúc *[suy đoán]* | **Baseline đối chiếu Li et al. 2023** |
| 4 | `phantom3-grass-kfs.tar.gz` | 383.2 MB | Phantom 3 | Bãi cỏ trơn, **ít vân nhất** | **Cảnh khó cho RQ1/RQ2** (dự báo lỗi) |
| 5 | `phantom3-centralPark-kfs.tar.gz` | 598.3 MB | Phantom 3 | Công viên dài: bãi cỏ, hồ, cây, đường | Quỹ đạo dài → đo **drift tích luỹ** |
| 6 | `phantom3-freeway-kfs.tar.gz` | 239.9 MB | Phantom 3 | Cao tốc, dải thẳng *[suy đoán]* | Cảnh tuyến tính (aperture problem) |
| 7 | `phantom3-lowlower-kfs.tar.gz` | 501.8 MB | Phantom 3 | Bay thấp (parallax lớn) *[suy đoán]* | Cảnh khó: phá giả định phẳng |
| 8 | `phantom3-ieu-kfs.tar.gz` | 269.3 MB | Phantom 3 | Khuôn viên/đô thị *[suy đoán]* | Đa dạng bổ sung |
| 9 | `phantom3-npu-kfs.tar.gz` | 288.2 MB | Phantom 3 | Khuôn viên trường (đường, nhà) | Cảnh dễ, nhiều vân |
| 10 | `phantom3-highflower-kfs.tar.gz` | 207.3 MB | Phantom 3 | Vùng hoa/đồng bằng phẳng *[suy đoán]* | Đa dạng bổ sung |
| 11 | `gopro-npu-kfs.tar.gz` | 221.5 MB | Hexacopter + GoPro Hero3+ | Khuôn viên + ruộng | Kiểm tra tổng quát (camera méo góc rộng) |
| 12 | `gopro-monticules-kfs.tar.gz` | 291.0 MB | Hexacopter + GoPro Hero3+ | Thửa ruộng chia ô | Kiểm tra tổng quát |
| 13 | `gopro-saplings-kfs.tar.gz` | 349.6 MB | Hexacopter + GoPro Hero3+ | Ô ruộng lặp vân dày | Kiểm tra tổng quát |
| 14 | `inspire1-rail-kfs.tar.gz` | 212.4 MB | DJI Inspire 1 | Hành lang đường sắt *[suy đoán]* | Kiểm tra tổng quát |

Xấp xỉ **~400 frame/gói** (ảnh 1920×1080 JPEG, ~0.6 MB/frame) → cả bộ ước tính **~7.000 keyframe**.

---

## 3. Thứ tự tải (3 tầng ưu tiên)

| Tầng | File | Tổng | Khi nào |
|---|---|---|---|
| **1 — Tải trước** | #1 village, #2 huangqi, #3 factory, #4 grass, #5 centralPark | **~1.71 GB** | Đủ chạy baseline + 3 RQ + so sánh được với Li et al. 2023 |
| **2 — Mở rộng** | #6 freeway, #7 lowlower, #8 ieu, #9 npu, #10 highflower | **~1.51 GB** | Khi cần thêm ca khó / quỹ đạo dài cho benchmark diện rộng |
| **3 — Tùy chọn** | #11–#14 toàn bộ `gopro-*` + `inspire1-rail` | **~1.07 GB** | Chỉ khi muốn kiểm tra tính tổng quát đổi camera |

Cộng cả 3 tầng = **4.29 GB < 10 GB** → không cần đánh đổi; chỉ cần tải theo thứ tự vì mạng chậm.

**Lưu ý về lựa chọn đang tải:** `phantom3-centralPark-kfs` (tầng 1) là lựa chọn tốt. `gopro-npu-kfs` là tầng 3 — GoPro góc rộng, méo mạnh, khác hệ camera Phantom 3; nên tải trước 5 file Phantom 3 ở tầng 1 rồi hãy quay lại gói này.

---

## 4. Cấu trúc bên trong mỗi gói (theo trang chủ dataset)

```
<sequence>/                      (giải nén từ <sequence>-kfs.tar.gz)
├── rgb/                         ảnh keyframe undistorted, tên = unix timestamp
├── trajectory.txt               pose từng keyframe: rotation + translation do SLAM tái dựng
└── config.cfg                   thông số camera nội tại (định dạng Svar/EICAM)
```

- **`trajectory.txt` là nguồn đối chiếu**, không phải ground truth đo độc lập. Metric chính đã chốt ở RDR-0007 là chain-vs-direct từ ảnh; xem [audit Notebook 04](notebook_04_drift_evaluation.md) về giới hạn tham chiếu và thang đo.
- **Giữ `config.cfg` và `trajectory.txt` đi cùng `rgb/`** để giữ provenance và khả năng chẩn đoán pose/camera. Thiếu trajectory không ngăn phép đo chain-vs-direct, nhưng thiếu metadata làm mất các phép đối chiếu liên quan.
- Mô tả gói dựa trên trang tác giả; audit notebook đã đọc dữ liệu giải nén `village`/`grass`, không xác minh toàn bộ nội dung 14 archive.

---

## 5. Dữ liệu KHÔNG có trong link public (và có cần không)

Bộ NPU Drone-Map **nguồn đầy đủ là 100+ GB** (theo trang chủ: "over 100GB data and more captured sequences will be added", gồm video gốc + unified + keyframes + GCP của tất cả sequence). Link Baidu public **chỉ phát hành 4.3 GB keyframes** — phần khác (~96 GB) chưa từng được công bố bản tải.

| Định dạng | Nội dung | Có trong Baidu share? | Dự án có cần? |
|---|---|---|---|
| **keyframes** (`-kfs`) | ảnh + `trajectory.txt` + `config.cfg` | **Có** (toàn bộ 14 file) | **Có — dùng chính** |
| **unified** | toàn bộ frame video + `frames.txt` + `gps.txt` (GPS thô) | Không | Không bắt buộc (keyframe đã đủ) |
| **original** | video gốc `.MOV`/`.MP4`, `.SRT`, `log.DAT`, waypoints | Không | Không (chỉ cần nếu tự trích frame từ video) |
| **GCPs** (`<sequence>-GCPs.zip`) | tọa độ GPS điểm khống chế | Không | Không (mosaic dự án không georeference) |

Cần các định dạng trên → liên hệ tác giả: Shuhui Bu `<bushuhui@nwpu.edu.cn>`, Yong Zhao `<zd5945@126.com>`.

### 5.1 Còn gì "cứu được" từ trang tác giả (kiểm chứng 2026-10-13)

Rà lại `adv-ci.com/blog/source/` + `npu-drone-map-dataset/` sau khi gặp bế tắc về tham chiếu drift:

| Mục | Dùng được gì | Có sẵn không |
|---|---|---|
| **Mã nguồn Map2DFusion** (`github.com/bushuhui/Map2DFusion`) | **Quyết định nhất**: `src/main.cpp` đọc `trajectory.txt` thành `pi::SE3d`; `PIL/src/base/types/SE3.h` cho biết **quaternion thứ tự $(x,y,z,w)$** và format mỗi dòng là `<tên ảnh> <SE3>`. `Plane=` là một **SE3** (không phải "điểm + pháp tuyến"). Nhờ đó cầu nối pose được sửa và sai số giảm từ 9,97 px xuống 0,88 px | **Có, tải tự do** |
| **GCP** (`<sequence>-GCPs.zip`) | **Ground truth độc lập thật** (marker id + toạ độ GPS) → hiệu chỉnh/kiểm chứng tuyệt đối, đo được sai số mét | Trang dataset ghi có cho *một số* sequence, nhưng **không nằm trong share Baidu đang dùng** |
| **`gps.txt`** (format unified) | GPS thô mỗi frame `(timestamp longitude latitude altitude gpsNumber)` → tham chiếu thứ hai độc lập với ảnh | Cần gói **unified**, không có trong link `-kfs` |
| **`.SRT` / `log.DAT`** (format original) | GPS thô từ Phantom 3 | Cần gói **original** (~100 GB) |
| **Tham số camera EICAM** | Chốt ngữ nghĩa `config.cfg` | Có link tải riêng trên trang dataset |
| **Danh sách MD5** | Xác minh file tải về | Trang dataset ghi có |
| **Link Baidu thứ hai** `pan.baidu.com/s/1kUt2ScR#path=/Dataset/NPU/DroneMap` (trên trang `source/`) | Đường dẫn tới **thư mục cha** `/Dataset/NPU/DroneMap` — có thể chứa cả original/unified/GCPs, khác với share `mji5` chỉ có 14 gói `-kfs` | Cần thử liệt kê |

**Lưu ý quan trọng về nguồn gốc trajectory:** trang dự án Map2DFusion ghi *"A monocular SLAM system is used to estimate camera position and attitude … When GPS information is available, the estimated trajectory is transformed to WGS84 coordinates after time synchronized automatically."* ⇒ `trajectory.txt` trong gói `-kfs` là **quỹ đạo do SLAM tác giả tái dựng** (không phải thiết bị đo độc lập). Vì vậy nó dùng được để **đối chiếu**, không nên coi là ground truth tuyệt đối khi đánh giá phương pháp dựa trên ảnh.

---

## 6. Việc cần làm trong repo

1. **`data/sample/` đã xoá (2026-10-13):** xác minh bằng SHA-256 — `rgb02` trùng khít `rgb01`, và 406/406 tên file + 406/406 nội dung của `rgb01` trùng khít `data/phantom3-village-kfs/rgb`. Toàn bộ 812 ảnh (~504 MB) không có gì riêng biệt nên đã xoá; dùng trực tiếp sequence thật.
2. `data/phantom3-village-kfs/` (406 frame, 1920×1080, cảnh đồng ruộng ven sông) **có kèm** `config.cfg` + `trajectory.txt` → dùng được để đo drift, tốt hơn hẳn sample cũ (sample không có metadata).
3. Giải nén về `data/<sequence>/`, **không hardcode đường dẫn** (`AGENTS.md`); loader đọc theo tham số thư mục. `.gitignore` đã có dòng `data/` (2026-10-13). Lưu ý: 812 ảnh `data/sample/` **vẫn còn trong git index** (đã commit từ trước) dù file đã xoá khỏi working tree — commit kế tiếp sẽ ghi nhận việc xoá; muốn giảm pack phải commit rồi `git gc`.
4. Dung lượng làm việc dự kiến: 1 sequence ~0.25–0.6 GB; chạy benchmark 5 sequence tầng 1 ~1.7 GB — vừa thoải mái Colab/Kaggle, không cần cắt thêm.

---

## 7. Đưa dữ liệu lên Colab / Kaggle

- **Không upload thẳng vào session Colab/Kaggle:** `files.upload()` chậm, đĩa session bị xóa sạch mỗi lần ngắt kết nối → session sau phải up lại từ đầu. Tốn thời gian hơn chứ không tiết kiệm.
- Nguyên tắc: up **một lần** lên nơi lưu trữ bền; mỗi session chỉ copy + giải nén một lần.

| Nơi lưu | Cách dùng trong session | Hợp khi |
|---|---|---|
| Google Drive (private) | `drive.mount(...)` → `cp` file `.tar.gz` sang `/content` → giải nén | Chạy Colab là chính |
| Kaggle Dataset (private) | Up bằng `kaggle datasets create/version`; notebook đọc trực tiếp `/kaggle/input/...` | Chạy Kaggle là chính (khỏi copy) |
| HuggingFace repo private | `hf upload` / `snapshot_download` | Upload hay đứt (có resume), tải trong Colab nhanh |

- Lưu trữ dạng `.tar.gz` nguyên gói; chỉ giải nén vào `/content` (đĩa local) khi chạy — đọc trực tiếp hàng nghìn JPEG nhỏ qua Drive mount rất chậm.
- **Giữ chế độ private**: dataset không ghi license rõ ràng → không phát hành lại công khai.

---

## 8. Các mục khác trên `adv-ci.com/blog/source/`

Trang này là **danh mục source code + dữ liệu** của tác giả (≈25 mục), không phải kho dataset: chỉ **2 mục là dataset** — NPU Drone-Map (đang dùng) và NPU RGB-D (không dùng); còn lại là phần mềm.

### 8.1 Mục là dataset

| Mục | Là gì | Vì sao không dùng |
|---|---|---|
| **NPU RGB-D Dataset** | Chuỗi ảnh màu + depth quay bằng **Kinect for Xbox 360** trong khuôn viên NWPU (trong nhà; tác giả nêu các khó khăn: chuyển động nhanh, rolling shutter, cảnh lặp vân, depth kém) để đánh giá thuật toán SLAM RGB-D | Ảnh **trong nhà**, không phải ảnh UAV → không dùng được cho mosaicking trên không; thuộc phần ngoài phạm vi (3D/SLAM) |

### 8.2 Phần mềm cùng bộ — đọc khi cần, không phải dữ liệu

| Mục | Là gì | Vì sao không dùng (và khi nào nên đọc) |
|---|---|---|
| **Map2DFusion** | Hệ mosaicking incremental realtime của chính tác giả dataset — C++, monocular SLAM, LGPL-3.0, lần cập nhật cuối 2019; video demo dùng `phantom3-village` (có GPS), `phantom3-grass` (cảnh khó), `gopro-npu` | Không dùng làm code baseline (C++/SLAM, đã cũ; pipeline dự án là Python/OpenCV + model pretrained). Chỉ đọc để đối chiếu ý tưởng: chọn keyframe, fusion đa băng tần thích ứng |
| **EICAM** | Thư viện C++ mô hình camera (PinHole, ATAN, OpenCV, OCAM…) + config hiệu chuẩn mẫu (`GoProMiddle1080`…), nằm trong repo `PIL` | Gói `-kfs` đã là ảnh undistorted → không cần tự sửa méo. Chỉ cần đọc nếu muốn hiểu ý nghĩa các tham số trong `config.cfg` |
| **PI-Base** | Thư viện C++ đọc tham số định dạng **Svar** | `config.cfg` trong gói kfs dùng đúng định dạng Svar này — chỉ cần đọc file để hiểu cú pháp, không cần build (Python tự parse được) |

### 8.3 Phần mềm không liên quan

| Nhóm | Mục | Là gì | Vì sao không dùng |
|---|---|---|---|
| Bay / trạm mặt đất | RTMapper, FastGCS, SimpGCS, opmapcontrol_ex, qFlightInstruments, Hands-Free, ArDrone Autoflight Toolkit, Dynamic Path Planning | Phần mềm tạo bản đồ realtime, trạm điều khiển UAV (MAVLink/APM), widget bản đồ Qt, nền tảng robot, toolkit bay tự động cho AR.Drone 2, demo path planning A* | Dự án xử lý **hậu kỳ trên ảnh** — không điều khiển drone, không realtime, không cần bản đồ nền |
| SLAM / SfM / 3D | PI-SLAM, GSLAM, Sequence SfM, FastSLAM GUI | Framework SLAM/SfM (PI-LAB) và GUI kèm theo | Ngoài phạm vi (`AGENTS.md`: không 3D/SLAM) |
| Học sâu / thị giác khác | PI-CNN, PI-SLIC, CDBN, DeepNet with CUDA, camshiftKalman, FrontFace | Trích feature map CNN, superpixel, mạng deep belief (MATLAB/CUDA), toolbox deep learning cũ (RBM/DBN), tracking vật thể camshift+Kalman, frontal hóa khuôn mặt | Không liên quan ghép ảnh; dự án dùng model pretrained (SuperPoint/LightGlue), không tự viết toolbox huấn luyện kiểu 2014–2016 |
| Tiện ích | Shell Toolkit, pyKanjiDict | Toolkit bash shell; từ điển Kanji tiếng Nhật | Không liên quan |

---

## 9. Nguồn kiểm chứng

- Trang dataset: `adv-ci.com/blog/source/npu-drone-map-dataset/` — định dạng gói, danh sách sequence, GCP, camera params, link Baidu (`mji5`).
- Trang index: `adv-ci.com/blog/source/` — toàn bộ danh mục source/data.
- Li et al. 2023 (Remote Sensing 15(8):2127) — bảng sequence dùng thử nghiệm: Phantom3-village/huangqi/factory, số frame.
- Kiểm tra trực tiếp share Baidu (đã giải mã `pwd`, liệt kê thư mục): 14 file, tổng 4.295,7 MB; hai link `tm5q` và `mji5` trùng nội dung.
- Kiểm tra cục bộ (2026-10-13): `data/sample/` cũ đã xoá sau khi xác minh SHA-256 trùng hoàn toàn với `data/phantom3-village-kfs/rgb`; 8 sequence `-kfs` đã giải nén đều có `rgb/` + `config.cfg` (+ `trajectory.txt`, trừ centralPark).
