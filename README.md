# Causal AI Local Demo

Repository này là phiên bản đã được dọn lại của một project nghiên cứu cũ về **customer churn + treatment recommendation trong banking**. Ở trạng thái hiện tại, repo đóng vai trò là một **local demo platform** bằng Python, có thể chạy end-to-end từ upload dữ liệu đến export workbook Excel cho business.

## Hệ thống hiện làm được gì?

- nhận file khách hàng `CSV` hoặc `XLSX`
- validate contract đầu vào và tách dòng bị reject
- profiling dữ liệu ở mức nhẹ
- tính `churn_probability`
- gán `segment / cluster`
- đề xuất `recommended_policy`
- sinh diagnostics và process-tracking output
- export workbook Excel cho business/sales

UI chính là **Streamlit** trong `apps/streamlit/`.  
Core engine nằm trong **`src/causal_app/`**.

## Điều cần hiểu ngay trước khi dùng

- Recommendation hiện tại **không phải** causal serving production-grade.
- Runtime đang dùng các **wrapper artifact** local, được dựng từ legacy data:
  - churn wrapper
  - segmentation wrapper
  - policy summary wrapper
- Lớp recommendation hiện vẫn phụ thuộc vào legacy `df_causal_ai`, nên mang tính **simulation-backed**.
- Postgres đã có schema nền trong `db/init/`, nhưng app hiện vẫn dùng **file-based run state** trong `storage/`, chưa ghi metadata thật vào DB.
- `data/`, `notebooks/`, và `configs/` ở top-level hiện chủ yếu là placeholder/scaffold, không phải source-of-truth runtime.

## Nên đọc gì đầu tiên?

- Hướng dẫn tổng thể tiếng Việt:
  - [`docs/PROJECT_MASTER_GUIDE_VI.md`](./docs/PROJECT_MASTER_GUIDE_VI.md)
- Memory rút gọn của project:
  - [`instructs/PROJECT_MEMORY_MASTER.md`](./instructs/PROJECT_MEMORY_MASTER.md)
- Các điểm còn mở:
  - [`instructs/OPEN_ITEMS.md`](./instructs/OPEN_ITEMS.md)
- Tóm tắt lượt dọn tài liệu:
  - [`docs/DOCUMENTATION_REFRESH_SUMMARY.md`](./docs/DOCUMENTATION_REFRESH_SUMMARY.md)

## Cấu trúc repo ở mức cao

- `src/causal_app/`: source-of-truth cho logic runtime
- `apps/streamlit/`: giao diện demo local
- `storage/`: upload, run outputs, workbook export, logs
- `artifacts/models/phase_03/`: artifact wrappers hiện tại cho demo engine
- `legacy_snapshot/`: bundle notebook/data cũ được archive nguyên vẹn
- `docs/`: tài liệu hiện hành
- `instructs/`: project memory đã được gom gọn
- `tests/`: test nhỏ nhưng là test thật

## Chạy nhanh

### Cách 1: local Python

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install pytest
.venv/bin/streamlit run apps/streamlit/app.py
```

Mở `http://localhost:8501`.

### Cách 2: Docker

```bash
docker compose up --build
```

Mở `http://localhost:8501`.

## Chạy pipeline không cần mở app

```bash
.venv/bin/python -m causal_app.pipeline.run_pipeline \
  --input legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/test.csv \
  --run-label smoke-test
```

## Output nằm ở đâu?

- upload: `storage/uploads/`
- output theo run: `storage/runs/<run-id>/`
- workbook Excel: `storage/exports/<run-id>.xlsx`
- log dùng chung: `storage/logs/pipeline.log`

## Workbook Excel hiện tại có gì?

Workbook business hiện có các sheet:

- `Summary`
- `Customer_Action_List`
- `Reject_Report`
- `Run_Metadata`
- `Field_Definitions`

`Customer_Action_List` là sheet chính cho sales/business.  
`reason_short` là logic **deterministic/template-based**, không dùng LLM.

## Những gì đã được verify thật

Đã có bằng chứng chạy thật trong workspace:

- `py_compile`
- `pytest`
- pipeline CLI trên file legacy `test.csv`
- Streamlit boot smoke test
- `docker compose config`

## Caveat quan trọng

- Đừng overclaim phần “causal”.
- Đừng nhầm artifact hiện tại với artifact nghiên cứu gốc.
- Đừng coi Postgres là nguồn state chính của app ở thời điểm này.
- Đừng coi `legacy_snapshot/` là runtime source-of-truth, nhưng cũng chưa được xóa nó vì engine hiện vẫn cần traceability từ đó.

## Legacy research bundle

Bundle notebook cũ vẫn nằm tại:

- [`legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/`](./legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/)

Nếu muốn hiểu toàn bộ repo từ đầu đến cuối bằng tiếng Việt, hãy bắt đầu từ:

- [`docs/PROJECT_MASTER_GUIDE_VI.md`](./docs/PROJECT_MASTER_GUIDE_VI.md)
