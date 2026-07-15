# Documentation Refresh Summary

## Mục tiêu

Lượt này tập trung vào **documentation synthesis + cleanup**, không xây tính năng mới.

Mục tiêu chính:

- giúp owner quay lại repo sau thời gian dài vẫn hiểu được hệ thống hiện tại
- gom tài liệu phân mảnh thành ít điểm đọc hơn
- giữ traceability lịch sử phase nhưng không để root `instructs/` quá ồn

## File chính được tạo / cập nhật

- `docs/PROJECT_MASTER_GUIDE_VI.md`
- `README.md`
- `instructs/PROJECT_MEMORY_MASTER.md`
- `instructs/OPEN_ITEMS.md`
- `instructs/archive/README.md`

## `instructs/` đã được dọn như thế nào

- root `instructs/` chỉ giữ:
  - `PROJECT_MEMORY_MASTER.md`
  - `OPEN_ITEMS.md`
  - `archive/`
- toàn bộ phase notes chi tiết được chuyển vào `instructs/archive/`

## Những gì được hợp nhất

- phase history từ Phase 1 đến Phase 6
- các quyết định kiến trúc quan trọng
- current source-of-truth structure
- open items vẫn còn hiệu lực
- caveat về causal/recommendation, Postgres, artifact metadata, và legacy dependency

## Mismatch / caveat đáng nhớ

- memory cũ có chỗ mô tả artifact metadata theo convention mới, nhưng file JSON đang nằm sẵn trong `artifacts/models/phase_03/` chưa được rebuild đồng loạt.
- historical phase docs có chỗ nói “chưa verified”, nhưng repo hiện tại đã có:
  - sample run outputs thật trong `storage/runs/`
  - workbook Excel thật trong `storage/exports/`
  - pytest pass
  - Streamlit smoke test pass
- Postgres vẫn chỉ là foundation/scaffold; app hiện tại chưa dùng DB làm state source chính.

## Cách đọc repo sau lượt cleanup

1. `README.md`
2. `docs/PROJECT_MASTER_GUIDE_VI.md`
3. `instructs/PROJECT_MEMORY_MASTER.md`
4. `instructs/OPEN_ITEMS.md`
5. chỉ vào `instructs/archive/` nếu cần lịch sử phase chi tiết
