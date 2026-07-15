# Project Memory Master

## 1. Mục đích của file này

Đây là file memory chính của repo sau lượt documentation synthesis / cleanup.

Future prompt hoặc future maintainer nên đọc file này trước tiên để hiểu:

- dự án này thực chất là gì
- runtime source-of-truth hiện ở đâu
- phần nào là legacy, phần nào là scaffold
- những giới hạn nào không được overclaim
- các quyết định kiến trúc lớn đã chốt qua các phase trước

## 2. Tóm tắt bản chất dự án

- Đây là một repo đã được hiện đại hóa dần từ bundle notebook nghiên cứu về churn banking + causal AI thành local Python demo platform.
- Runtime hiện tại là:
  - Streamlit app trong `apps/streamlit/`
  - core engine trong `src/causal_app/`
  - file-based storage trong `storage/`
  - business Excel export
- Legacy research vẫn nằm trong `legacy_snapshot/`.
- Postgres hiện mới là foundation/scaffold, chưa là state source chính của app.
- FastAPI chưa có code runtime thật trong repo; nó chỉ là hướng mở rộng được cân nhắc cho tương lai.

## 3. Source-of-truth hiện tại

### Runtime source-of-truth

- `src/causal_app/`
- `apps/streamlit/`
- `pyproject.toml`
- `Dockerfile`
- `docker-compose.yml`
- `README.md`
- `docs/PROJECT_MASTER_GUIDE_VI.md`

### Runtime generated outputs

- `storage/`
- `artifacts/models/phase_03/`

### Historical / legacy source material

- `legacy_snapshot/`

### Project memory

- `instructs/PROJECT_MEMORY_MASTER.md`
- `instructs/OPEN_ITEMS.md`
- `instructs/archive/`

## 4. Lịch sử phase tóm tắt

### Phase 1

- audit repo research cũ
- xác định đây là bundle notebook/demo, chưa phải platform maintainable

### Phase 2

- tạo repo structure mới
- thêm nền Docker + Postgres + Streamlit
- giữ nguyên legacy bundle trong `legacy_snapshot/`

### Phase 3

- trích xuất core engine runnable vào `src/causal_app/`
- tách ingestion, validation, preprocessing, churn, segmentation, recommendation, diagnostics, export

### Phase 4

- nối Streamlit với engine
- tạo luồng upload, profiling, process tracking, dashboard, export

### Phase 5

- tối ưu business output
- thêm workbook Excel rõ ràng hơn cho sales/business
- thêm `priority` và `reason_short` theo rule deterministic

### Phase 6

- thêm test nhỏ nhưng thật
- tăng logging / observability
- chuẩn hóa hơn về docs, artifact manifest, local run flow
- quyết định: chưa thêm FastAPI ngay

## 5. Kiến trúc hiện tại

Luồng runtime hiện tại:

1. Upload file `CSV/XLSX`
2. Read file
3. Validate contract
4. Profiling nhẹ
5. Preprocess
6. Churn prediction
7. Segmentation
8. Recommendation
9. Diagnostics
10. Excel export
11. Process tracking bằng file trong `storage/`

## 6. Điều cần nhớ về phần causal

- Prediction runtime là thật, nhưng là wrapper notebook-derived.
- Segmentation runtime là wrapper từ `df_cluster.csv`, không phải clustering stack gốc.
- Recommendation runtime phụ thuộc vào `df_causal_ai` và policy summary suy ra từ đó.
- Runtime hiện tại không chạy lại causal graph discovery hoặc DRLearner/DoWhy notebook-level.
- `df_causal_ai` mang tính simulation-backed, nên recommendation hiện tại không được mô tả như production-grade causal inference service.

## 7. Những quyết định kiến trúc lớn đã chốt

1. Giữ nguyên legacy bundle trong `legacy_snapshot/`, không rewrite nội bộ.
2. Tách research legacy khỏi runtime code.
3. Dùng `src/causal_app/` làm nguồn logic runtime.
4. Dùng Streamlit làm local demo UI chính.
5. Dùng Postgres như foundation tương lai, nhưng chưa ép app phụ thuộc vào DB.
6. Dùng file-based outputs và traceability trước khi nghĩ tới backend/service phức tạp hơn.
7. Giữ recommendation explanation ở mức deterministic/template-based, không dùng LLM.
8. Chưa thêm FastAPI; chỉ chuẩn bị khả năng mở rộng.
9. Không promote `data/` và `notebooks/` top-level thành source-of-truth khi chưa có dữ liệu/notebook mới được chuẩn hóa.

## 8. Trạng thái hiện tại theo nhóm

### Real / chạy được

- Streamlit app local
- pipeline CLI
- CSV/XLSX ingestion
- validation
- profiling nhẹ
- churn / segmentation / recommendation wrappers
- diagnostics
- Excel workbook
- tests nhỏ bằng pytest
- logging và manifest per run

### Partial

- recommendation vẫn mang tính legacy wrapper
- Postgres chưa được app dùng thật
- profiling còn đơn giản
- test coverage còn mỏng
- artifact metadata convention mới chưa được backfill đồng loạt vào toàn bộ file cũ trong `artifacts/models/phase_03/`

### Legacy

- notebooks cũ
- dữ liệu trung gian cũ
- slide, ảnh, README cũ
- nested `.git` trong legacy snapshot

### Scaffold / placeholder

- `data/`
- `notebooks/`
- `configs/`

## 9. Mismatch quan trọng giữa memory cũ và repo thật

1. Một số phase notes cũ nói về hướng artifact metadata mới, nhưng các file JSON hiện đang nằm sẵn trong `artifacts/models/phase_03/` vẫn là bản cũ, chưa được rebuild đồng loạt theo convention mới.
2. Historical phase docs nói nhiều chỗ “chưa verified”; hiện tại repo đã có:
   - local `.venv` run thành công
   - Streamlit boot smoke test thành công
   - pytest pass
   - sample workbook thật trong `storage/exports/`
   - nhiều run output thật trong `storage/runs/`
3. `instructs/` hiện chỉ nên giữ file memory hiện hành ở root; phase files chi tiết được archive để giảm nhiễu khi đọc repo.

## 10. Open rules cho future prompts

1. Đọc file này trước.
2. Sau đó đọc `instructs/OPEN_ITEMS.md`.
3. Chỉ đọc `instructs/archive/` khi cần lịch sử phase chi tiết.
4. Không được overstate phần causal/recommendation hiện tại.
5. Không được xóa `legacy_snapshot/` nếu engine còn phụ thuộc vào đó.
6. Không được coi Postgres là state source chính của app hiện tại.
7. Khi mô tả repo, phải phân biệt rõ:
   - observed in repo now
   - inferred from archived phase docs
   - planned but not implemented

## 11. Nên đọc gì tiếp theo?

1. `README.md`
2. `docs/PROJECT_MASTER_GUIDE_VI.md`
3. `instructs/OPEN_ITEMS.md`
4. `src/causal_app/`
5. `apps/streamlit/`
6. `legacy_snapshot/`
