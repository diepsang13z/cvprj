# Project Rules

Tài liệu quy định nguyên tắc vận hành, quản lý context và kỹ thuật áp dụng xuyên suốt dự án. Mọi Agent và cộng tác viên phải tuân thủ.

---

## 1. Giới hạn độ dài Context File

- Mọi file context được dẫn link trong `docs/INDEX.md` (gồm `RULES.md`, `AGENTS.md` và các tài liệu đặc tả) phải **≤ 200 dòng**.
- Ngoại lệ duy nhất: `docs/logs/**` không áp dụng giới hạn này.
- Vượt ngưỡng → tách file, hoặc đẩy chi tiết vào `docs/logs/` và giữ bản chắt lọc ở chỗ cũ.
- File mới phải thỏa ngay khi tạo, không "để sau rút gọn".
- Lý do: file dài bị đọc trọn mỗi lần, tốn context và chìm phần quan trọng.

## 2. Kỷ luật Git

- **Tuyệt đối không tự ý chạy lệnh ghi/đổi trạng thái git** (`add`, `commit`, `push`, `checkout`, `rebase`, `reset`, `tag`) trừ khi người dùng yêu cầu rõ trong lượt đó.
- Chỉ sửa working tree, báo cáo thay đổi và đề xuất commit message; đợi xác nhận mới thực thi.
- Nhánh làm việc: mỗi người một nhánh `<tên>/work`, mở pull request vào `main`. **Không commit thẳng `main`.**
- Không tạo nhánh lồng tên nhánh khác (ví dụ `remotes/origin/<tên>/work`) — lỗi này làm `git push` trần báo *"upstream branch does not match"*.

## 3. Nguồn sự thật cao nhất (Single Source of Truth)

- Quyết định đã chốt nằm ở `docs/decisions/` (mã `RDR-NNNN`), đọc theo **chủ đề**; quyết định mới chỉ thay quyết định cũ khi ghi rõ phạm vi thay thế.
- `docs/decisions/` hoạt động **append-only**: chỉ thêm mới, không sửa đè quyết định cũ.
- Việc đang mở do [GitHub Issues](https://github.com/diepsang13z/cvprj/issues) quản lý (khi nhóm dùng); trước mắt ghi ở `docs/logs/progress/`.
- Mâu thuẫn giữa `AGENTS.md` / `README.md` / `docs/INDEX.md` với `docs/decisions/` → **decisions thắng**.

## 4. Kỷ luật giai đoạn khám phá (Exploratory Discipline)

- Khi một quyết định phương pháp **chưa có `RDR`** (chọn matcher, metric, ngưỡng kích hoạt, công thức đo drift, cách blend…), Agent **KHÔNG tự chốt thay nhóm**.
- Phạm vi hành vi được phép: phân tích dữ liệu, bóc tách cấu trúc dataset, đối soát văn hiến, brainstorm ý tưởng. Việc chốt phương pháp do nhóm quyết và ghi thành `RDR`.

## 5. Quy ước đặt tên file & thư mục

- Tên file và thư mục **chỉ dùng chữ thường, chữ số và dấu gạch dưới `_`**. Không dùng gạch ngang `-`, khoảng trắng, dấu tiếng Việt hoặc ký tự đặc biệt.
- **Ngoại lệ 1 — mã quyết định:** `RDR-NNNN` giữ gạch ngang vì là mã, không phải dấu phân tách từ. Phần slug phía sau dùng `_`: `RDR-0004_lecturer_review_after_persen_proposal.md`.
- **Ngoại lệ 2 — file điều hướng/quản lý context viết HOA:** `README.md`, `AGENTS.md`, `RULES.md`, `INDEX.md`. Nội dung là kiến thức/nhật ký → chữ thường. Ví dụ `refs/INDEX.md` (điều hướng) vs `notes/glossary.md` (nội dung).
- **Chỉ áp cho file tạo mới.** File cũ đã đúng quy ước thì giữ nguyên; file nội dung không đổi tên chỉ vì quy ước này.
- **Quy ước `refs/`:** `<năm>_<tác_giả_chính_không_dấu>_<chủ_đề_ngắn>.pdf`.

## 6. Kỷ luật ghi quyết định, việc mở, nhật ký

Ba nguồn tách theo vòng đời thay đổi; **không giữ một file trạng thái phải đồng bộ thủ công**.

| Loại thông tin | Nguồn | Khi nào cập nhật | Cách |
| --- | --- | --- | --- |
| Quyết định đã chốt | `docs/decisions/` | Nhóm chốt/thay đổi | Thêm `RDR` mới, nêu rõ phạm vi thay thế |
| Việc đang mở | GitHub Issues (hoặc `docs/logs/progress/`) | Có việc mới/hoàn thành | Một issue mỗi việc; đóng khi xong |
| Việc đã xảy ra | `docs/logs/progress/YYYY_MM_DD_<tên>.md` | Mỗi phiên | Mở file mới; không sửa file người khác |

- File nhật ký có **4 mục bắt buộc:** `Đã làm` · `Bằng chứng` · `Còn lại cho người khác` · `Đang chặn`. Mục trống ghi "không".
- **Nhật ký là bản chụp, không phải bản nháp:** bất biến sau khi ghi — không sửa, không xoá nội dung cũ kể cả khi sai. Đính chính bằng cách chèn dòng (giá trị cũ · mới · ngày · căn cứ), không sửa đè.
- Lý do, tiêu chí và quyết định không bao giờ sửa, chỉ đính chính bằng `RDR` mới.

## 7. Thêm quy tắc mới

Thêm mục đánh số tiếp theo ngay tại đây. Khi mâu thuẫn, `RULES.md` thắng mọi mô tả khác trong repo.
