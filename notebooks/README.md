# UAV Aerial Mosaicking Experiments

## Phạm vi và trạng thái nghiên cứu

- Ba RQ giữ theo RDR-0003: dự báo lỗi, phân luồng matcher, phục hồi.
- [RDR-0011](../docs/logs/decisions/RDR-0011_loso_and_technical_readiness.md) chọn
  **leave-one-sequence-out (LOSO)** và **chỉ sửa kỹ thuật trước**.
- RDR-0008 vẫn **Proposed**. Các giá trị sai số bước, NCC, inlier ratio,
  ngân sách escalation và policy mặc định chưa được chấp nhận là phương pháp chính thức.
- Không gọi bất đồng với SIFT tham chiếu là độ chính xác thực địa.
  Chain-vs-direct cần overlap; không đo được phải báo riêng, không thay bằng 0.
- Không suy ra khả năng tổng quát từ cửa sổ đã dùng để chọn chỉ báo.
  Village/grass đã được dùng khám phá; LOSO không xoá lịch sử đó.

## Chỉ chạy trên hosted runtime

Theo [RULES.md §8](../RULES.md), không chạy notebook, cell, model hay pipeline
trên máy cá nhân, kể cả Colab local runtime. Chỉ dùng hosted Colab/Kaggle.
Máy cá nhân chỉ dùng kiểm tra JSON, cú pháp và đường dẫn.

Qua kiểm tra tĩnh không có nghĩa đã chạy thành công trên Colab. Cần chạy
self-check và smoke trên hosted runtime trước khi chạy toàn dataset.
Không có cam kết thời gian chạy hoặc quota GPU trước khi đo.

## Cấu trúc Google Drive

Giữ nguyên thư mục của nhóm; không cần đổi `dataset` thành `data`, không tạo symlink:

```text
MyDrive/mosaicking_from_uav_video_research/
  dataset/
    <sequence>/
      rgb/*.jpg
      config.cfg
      trajectory.txt
  classical_mosaicking_baseline.ipynb
  deep_matching_pilot.ipynb
  feature_matcher_benchmark.ipynb
  accumulated_drift_evaluation.ipynb
  failure_aware_mosaicking_pipeline.ipynb
  outputs/
```

Metadata pose không phải ground truth độc lập. Chẩn đoán trajectory chỉ là
phép đối chiếu bổ sung; không dùng kết luận village/grass ép các sequence khác.

## Luồng chạy

1. Upload bản notebook hiện tại lên Drive, mở trong Colab hosted runtime.
2. Chọn runtime phù hợp: GPU cho learned matcher; ghi phần cứng thực tế
   trong artifact. OpenCV SIFT/ORB vẫn chạy CPU dù runtime có GPU.
3. Đọc cấu hình đầu notebook. Root mặc định là thư mục Drive ở trên;
   `UAV_PROJECT_ROOT` cho root khác, `UAV_OUTPUT_ROOT` cho thư mục kết quả.
   Dùng thư mục bền vững, không `/content` tạm, cho kết quả Colab.
4. Chạy từ runtime sạch, cấp quyền mount Drive. Không bỏ qua lỗi dependency,
   dữ liệu, self-check hoặc provenance để tiếp tục một run không hợp lệ.
5. Chạy cấu hình nhỏ trước; kiểm tra artifact, số frame thực xử lý,
   trạng thái thất bại/không đo được và marker hoàn tất.
6. Sau smoke, chọn phạm vi full trong cấu hình. Chạy đủ sequence và đủ frame
   khác với ghép thành công hết frame hay có tham chiếu hợp lệ cho hết frame.
7. Notebook drift cần một run benchmark hoàn tất, đúng dữ liệu; dùng
   `UAV_INPUT_RUN` để chỉ định thư mục run. Không lấy homography từ bộ ảnh khác.
8. Trước khi đóng phiên, kiểm tra kết quả đã ở Drive. Với Kaggle, cần lưu
   notebook version/output và bàn giao artifact; mount/directory tồn tại
   không tự bảo đảm dữ liệu còn sau khi phiên bị xoá.

## Vai trò của 5 notebook

| Notebook | Vai trò | Giới hạn diễn giải |
|---|---|---|
| `classical_mosaicking_baseline.ipynb` | SIFT/ORB baseline, homography và mosaic | RMSE inlier không phải độ chính xác toàn bản đồ |
| `deep_matching_pilot.ipynb` | SIFT/SuperPoint + LightGlue | Pilot ảnh gốc; không trộn timing với benchmark 640 px |
| `feature_matcher_benchmark.ipynb` | So sánh các adapter trên cùng input/cấu hình | Báo backend/device và phạm vi timing; lỗi matcher là kết quả |
| `accumulated_drift_evaluation.ipynb` | Chain-vs-direct trên output benchmark có provenance | Báo common support, coverage và tham chiếu không hợp lệ |
| `failure_aware_mosaicking_pipeline.ipynb` | Chỉ báo, mô phỏng routing và thí nghiệm recovery | Phân biệt mô phỏng/cost cache với chạy online, cấu hình khám phá với protocol xác nhận |

## Artifact và tái lập

- Run mới phải nằm trong thư mục mới; không ghi đè `notebooks/outputs/` lịch sử.
- Giữ manifest, input hash/frame IDs, cấu hình, phiên bản thư viện, kết quả
  từng cặp/sequence, failure log và marker hoàn tất cùng một run.
- Run dở dang không phải run đã hoàn tất. Checkpoint giúp giữ công việc đã
  xong; không đồng nghĩa tự động resume hoặc được trộn với run khác.
- `N/A`/`null` là phép đo không khả dụng, không phải sai số bằng 0.
- Split giữ ảnh nhưng có thể tạo mảnh một frame. Báo số/kích thước mảnh và
  cạnh ghép thành công; không dùng retained frames một mình để kết luận thắng.
- Không so thời gian khác phạm vi (matcher-only với pipeline, có IO với
  không IO) như cùng một thước đo.

## LOSO: ranh giới protocol đã chốt

Mỗi fold giữ lại một sequence; mọi bước hiệu chỉnh dùng các sequence còn lại.
Ghi train/test sequence, cấu hình và trạng thái ngân sách khả thi cho từng fold.
Không chọn lại ngưỡng từ kết quả sequence giữ lại. Một fold không khả thi hoặc
không đủ tham chiếu phải được báo, không đổi sang ngưỡng dự phòng âm thầm.

LOSO có thể cho các ngưỡng khác nhau giữa fold. Nó đánh giá quy trình hiệu chỉnh,
không chứng minh một ngưỡng duy nhất phù hợp mọi cảnh. Các ngưỡng hiện có vẫn là
khám phá cho tới quyết định phương pháp tiếp theo; không tự đổi RDR-0008 thành Accepted.

## Tài liệu/kết quả lịch sử

Các ghi chú trong `docs/explain/`, output cũ và số liệu paper là hồ sơ lịch sử,
không phải bằng chứng phiên bản notebook hiện tại đã chạy. Không tự thay số liệu
paper bằng run mới, hoặc trộn artifact cũ/mới khi schema và cấu hình khác nhau.
Luồng chia việc cũ bằng ba file `scan_<matcher>.json` không được coi là tính năng
nhập/ghép dữ liệu nếu notebook hiện tại không cung cấp đường chạy đó.
