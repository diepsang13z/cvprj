# Đợt quét dataset — theo RDR-0002 (2026-09-19)

**Mục đích:** shortlist dataset cho team quyết định. **Tiêu chí (RDR-0002):** opensource + dữ liệu drone (UAV) thật. **Tiêu chí phụ:** RGB, chuỗi khung liên tiếp có chồng lấn, gần nadir, cảnh tương đối phẳng, phù hợp mosaicking homography; bonus: telemetry (GPS/IMU), GCP/orthophoto/pose GT cho đo drift.

**Phương pháp:** dự kiến quét bằng ba nhánh song song nhưng subagent thất bại đồng loạt (`usage_limit_reached`) → kiểm chứng trực tiếp tại phiên chính bằng trang chính thức: Dryad, Hugging Face, WHU GPCV, adv-ci.com, GitHub, MDPI JATS XML, PMC. Ngày kiểm: 2026-09-19. Mọi số liệu là quan sát trên nguồn chính tại thời điểm kiểm.

## Bảng ứng viên

| # | Tên | Nguồn | License | Drone thật | Nội dung | Telemetry/GT | Phù hợp | Truy cập | Rủi ro chính |
|---|---|---|---|---|---|---|---|---|---|
| 1 | UMCD | umcd-dataset.net | "freely available only for research purposes" (không có license chuẩn) | có — bay thấp 6–15 m | 30 chuỗi không geo + 10 cặp geo (20 video), ~3.5 GB | telemetry: độ cao, tốc độ, GPS đi kèm video | **mosaicking-specific nhất** | tải trực tiếp `umcd.zip` + mật khẩu qua email (avola@di.uniroma1.it) | research-only + mật khẩu → RDR-0002 tranh cãi |
| 2 | NPU Drone-Map | adv-ci.com/blog/source/npu-drone-map-dataset | không ghi license | có — Phantom3, hexacopter (GoPro), Inspire | nhiều chuỗi 100+ GB: video gốc, ảnh undistorted, keyframes | **.SRT, gps.txt (lon/lat/alt), GCPs ở một số chuỗi, trajectory.txt (R+t), camera params** | rất phù hợp; đã dùng trong Li et al. 2023 | Baidu Pan, pwd mji5 (URL công khai) | Baidu khó tải ngoài TQ; không license chuẩn |
| 3 | DroneZaic | Dryad doi:10.5061/dryad.r4xgxd2q7 | Dryad (CC0 theo chính sách Dryad; chưa xác nhận trực tiếp — README 403) | có — DJI, nông nghiệp | raw videos 38.2 GB + processed 30.9 GB + models 1.2 GB | paper nêu telemetry kém chính xác; code hỗ trợ DJI .SRT | stress domain: cánh đồng repetitive texture, quỹ đạo tự do | tải thẳng Dryad | 70.4 GB nặng; license cần xác nhận khi tải |
| 4 | Aerial234 | huggingface.co/datasets/RussRobin/Aerial234 | **cc-by-4.0** | có — drone quét liên tục khuôn viên Southeast University | 234 ảnh, mục đích sinh ra để stitch thành 1 panorama | không nêu | challenge stitching đơn panorama, cảnh phức tạp | gated (click-through đồng ý chia sẻ thông tin liên hệ) | không video; gate HF |
| 5 | WHU Aerial Video | gpcv.whu.edu.cn (WHU_Areial_Video_Dataset) | không ghi license | có — DJI M300 RTK + DJI P1 | 2 chuỗi video: strip đều + bất quy tắc, 60 fps, 3860×2160, GSD 3 cm, độ cao 200 m | **RTK, 16 GCP (GPS 9 mm), GT pose keyframes, intrinsics (apriltag), quan trắc GCP** | tốt nhất cho đo drift/sai số hình học tuyệt đối | trang không có link tải hoạt động; liên hệ lab (jishunping@whu.edu.cn) | cần email; license không rõ |
| 6 | ODMdata (tập con helenenschacht, bellus, waterbury, seneca, toledo…) | github.com/OpenDroneMap/ODMdata | license theo từng repo, không đồng nhất | có | bộ ảnh chụp theo strip, hàng trăm ảnh | EXIF GPS; helenenschacht/waterbury RTK; bellus/helenenschacht có GCP | dùng được như frame-set; RTK/GCP cho sai số tuyệt đối | GitHub/Drive | không video; phải kiểm license từng repo |
| 7 | VisDrone-VID | github.com/VisDrone/VisDrone-Dataset | README không ghi license | có — 14 thành phố | video detection/tracking, 288 clip | không | yếu cho mosaicking (chếch góc, tập trung đối tượng) | Drive/Baidu | license không rõ |
| 8 | UDD | github.com/MarcWong/UDD | "only for non-commercial use" (phần ảnh) | có — đô thị | ảnh chuỗi trên không; M1 dùng cho reconstruction | không | trung bình | Drive/Baidu | non-commercial |
| 9 | StitchBench | huggingface.co/datasets/RussRobin/StitchBench | **cc-by-4.0** | phần aerial = Aerial234 | benchmark stitching ảnh tự nhiên (OBJ-GSP, AAAI 2025) | không | chỉ phần aerial liên quan | gated | không phải dataset UAV thuần |

## Đã loại (vi phạm RDR-0002 hoặc không phù hợp)

| Tên | Lý do loại |
|---|---|
| Mid-Air | mô phỏng (simulator) |
| MovingDrone (OrthoTrack) | photorealistic → dữ liệu tổng hợp |
| Blackbird | tổng hợp |
| OpenAerialMap | mở nhưng không phải chuỗi video/ảnh UAV liên tiếp cho mosaicking |
| ERA Dataset | tổng hợp từ YouTube, license rối |
| Semantic Drone Dataset | trang TU Graz 404 tại thời điểm kiểm; ảnh phân đoạn, không phải chuỗi |
| UAVScenes / UAVD4L | không xác minh được trang chủ tại thời điểm kiểm (404) — để ngỏ, không tính |

## Khuyến nghị cho team

- **Tổ hợp đề xuất:** NPU Drone-Map (chính cho pipeline + eval; có video, .SRT, GPS log, GCP, trajectory) + DroneZaic (stress nông nghiệp repetitive) + Aerial234 (challenge một panorama phức tạp) + WHU Aerial Video (RTK/GCP/GT pose cho đo drift — nếu xin được link). UMCD giữ làm lựa chọn nếu team chấp nhận "research-only + mật khẩu": nó là dataset duy nhất thiết kế riêng cho đánh giá mosaicking.
- **Điểm cần team quyết định:**
  1. "Opensource" trong RDR-0002 đọc thế nào: bắt buộc license chuẩn (CC-BY…) hay chỉ cần tải được + dùng cho nghiên cứu? License chuẩn đã xác minh: cc-by-4.0 (Aerial234, StitchBench); CC0 theo chính sách Dryad (DroneZaic, chưa xác nhận trực tiếp). NPU/WHU/UMCD không có license chuẩn.
  2. Chấp nhận Baidu Pan (NPU Drone-Map) và mật khẩu/email (UMCD, WHU) không?
  3. Ngân sách tải về: DroneZaic 70 GB vs UMCD 3.5 GB vs NPU 100+ GB.

## Bằng chứng kiểm chứng

- UMCD: trang chính thức — cấu trúc dataset, telemetry, câu "freely available only for research purposes", cơ chế mật khẩu qua email.
- NPU Drone-Map: adv-ci.com — phần cứng, định dạng (original/unified/keyframes), GCP, camera params, link Baidu (pwd mji5). Paper Li et al. 2023 (MDPI XML): "Data Availability: available upon request" nhưng ref [34] trỏ trang adv-ci công khai.
- DroneZaic: Dryad — danh sách file 70.40 GB, DOI; README không đọc được (403 khi tải trực tiếp) → license chưa xác nhận trực tiếp.
- Aerial234 / StitchBench: HF dataset card — license cc-by-4.0, access gated.
- WHU Aerial Video: trang GPCV — thông số kỹ thuật, GCP 9 mm, GT; HTML không chứa link tải hoạt động.
- ODMdata: bảng README GitHub — số ảnh, kích thước, cờ EXIF/GCP/RTK từng tập.
- VisDrone / UDD: README GitHub.

## Điểm bất định

- License chính xác của DroneZaic (chỉ suy từ chính sách Dryad), NPU, WHU, UMCD (không có license chuẩn).
- Link tải WHU không hoạt động trên trang → chỉ liên hệ được qua email.
- Baidu Pan có thể chặn tải ngoài Trung Quốc; chưa thử tải thật.
- Aerial234 gate HF yêu cầu đồng ý chia sẻ thông tin liên hệ — chưa thực hiện.
- Chưa xác minh UAVScenes/UAVD4L (trang 404 lúc kiểm) — có thể bổ sung đợt sau.
