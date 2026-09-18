# RULES

Ràng buộc cứng của repo. Không có ngoại lệ trừ khi người dùng yêu cầu rõ trong lượt đó.

## 1. Tài liệu context tối đa 200 dòng

Mọi file tài liệu được liệt kê trong `docs/INDEX.md` phải **≤ 200 dòng**. Ngoại lệ duy nhất: `docs/logs/**`.

- Vượt ngưỡng → tách file, hoặc đẩy phần chi tiết vào `docs/logs/` và giữ lại bản chắt lọc.
- File mới phải thỏa ngay khi tạo, không "để sau rút gọn".
- Đếm bằng `wc -l <file>`.
- Lý do: file dài bị đọc trọn mỗi lần, tốn context và chìm phần quan trọng.

## 2. Không tự ý git add / commit / push

KHÔNG chạy `git add`, `git commit`, `git push`, `git tag`, `git rebase`, `git reset --hard` — tức mọi lệnh ghi vào lịch sử hoặc remote — **trừ khi người dùng yêu cầu rõ ràng trong lượt đó**.

- "Viết xong file X" không phải là yêu cầu commit.
- Được phép: lệnh git chỉ đọc (`status`, `diff`, `log`, `show`, `blame`).
- Xong việc: dừng ở mức thay đổi working tree, liệt kê file đã sửa, để người dùng tự quyết định commit.

## 3. Thêm quy tắc mới

Thêm mục đánh số tiếp theo ngay tại đây. Khi mâu thuẫn, `RULES.md` thắng mọi mô tả khác trong repo.
