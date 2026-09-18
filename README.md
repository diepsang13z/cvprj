# UAV video 2D aerial mosaicking

Dự án xây dựng mosaic ảnh 2D từ video UAV bằng pipeline đặc trưng cổ điển, matching, RANSAC/homography, warp và blend. Kết quả là ảnh hiện trạng cục bộ, không phải bản đồ georeference.

## Cấu trúc dự án

```text
.
├── AGENTS.md                         # Phạm vi, ràng buộc và quy tắc làm việc
├── RULES.md                          # Ràng buộc cứng của repository
├── STATUS.md                         # Ảnh chụp trạng thái hiện tại
├── README.md                         # Tổng quan và cấu trúc repository
├── docs/
│   ├── INDEX.md                      # Router cho tài liệu context
│   ├── decisions/                    # Quyết định đã chốt (append-only)
│   └── logs/                         # Nhật ký khảo sát và brainstorm
├── notes/
│   └── glossary.md                   # Thuật ngữ dự án
├── refs/
│   ├── README.md                     # Danh mục tài liệu tham khảo
│   └── *.pdf                         # Toàn văn các bài báo tham khảo
├── reports/
│   └── md/
│       └── research_proposal.md      # Bản thuyết minh đề cương đã điền nội dung
└── templates/
    └── Research Proposal template.docx # Mẫu Word gốc của đề cương
```

`docs/INDEX.md` chỉ quản lý tài liệu context. Báo cáo đầu ra và template được liệt kê tại đây để người đọc tìm theo cấu trúc repository.
