# Hướng Dẫn Tổng Thể Dự Án Causal AI Local Demo

## 1. Mục đích của tài liệu này

Tài liệu này là bản giải thích tổng thể, bằng tiếng Việt, cho toàn bộ repository ở **trạng thái hiện tại**.

Mục tiêu của tài liệu là giúp chính chủ dự án hoặc một cộng tác viên kỹ thuật:

- quay lại repo sau thời gian dài vẫn hiểu được hệ thống đang làm gì
- phân biệt rõ phần nào là **runtime thật đang chạy được**
- phần nào là **legacy research**
- phần nào là **giả lập / simulation / causal proxy**
- phần nào mới chỉ là **scaffold hoặc hướng mở rộng**

Tài liệu này không cố làm đẹp lịch sử. Nếu repo phát triển theo kiểu “đi từ notebook nghiên cứu sang demo platform”, tài liệu sẽ nói đúng điều đó.

---

## 2. Tổng quan dự án

### 2.1. Dự án này thực chất giải bài toán gì?

Ở mức business, đây là dự án về **giữ chân khách hàng ngân hàng**.

Bài toán gốc là:

- xác định khách hàng nào có nguy cơ rời bỏ dịch vụ (`churn`)
- chia khách hàng thành các nhóm hành vi / hồ sơ tương đối giống nhau
- từ đó đề xuất một hành động giữ chân phù hợp hơn cho từng nhóm hoặc từng khách hàng

Nói ngắn gọn:

- **phần prediction** trả lời: “khách hàng nào có rủi ro churn?”
- **phần segmentation** trả lời: “khách hàng đó thuộc nhóm nào?”
- **phần recommendation** trả lời: “nên ưu tiên chương trình giữ chân nào?”

### 2.2. Bài toán business là gì?

Theo legacy README và toàn bộ notebook cũ, bài toán business được hiểu như sau:

- ngân hàng mất lợi nhuận khi khách hàng rời bỏ
- mô hình churn truyền thống chỉ cho biết xác suất rời bỏ, nhưng không nói rõ nên can thiệp như thế nào
- dự án muốn đi xa hơn một bước: không chỉ dự đoán churn, mà còn gợi ý “treatment” / “intervention” / “program” phù hợp hơn để giảm churn

### 2.3. Người dùng của hệ thống là ai?

Ở trạng thái repo hiện tại, hệ thống đang phục vụ 3 nhóm người dùng chính:

1. **Người làm data science / chủ repo**
   - upload dữ liệu
   - kiểm tra validation
   - xem profiling
   - chạy pipeline
   - xem diagnostics

2. **Người dùng business / sales**
   - chủ yếu dùng file Excel đầu ra
   - xem danh sách khách hàng cần ưu tiên
   - xem `priority`, `recommended_policy`, `reason_short`

3. **Người bảo trì kỹ thuật trong tương lai**
   - đọc `src/`
   - đọc `docs/`
   - đọc `instructs/`
   - tái sử dụng hoặc mở rộng demo thành service lớn hơn

### 2.4. Đầu vào là gì?

Đầu vào runtime hiện tại là một file `CSV` hoặc `XLSX` có dữ liệu khách hàng.

Contract tối thiểu hiện tại nằm ở [contracts.py](src/causal_app/schemas/contracts.py):

- `CreditScore`
- `Geography`
- `Gender`
- `Age`
- `Tenure`
- `Balance`
- `NumOfProducts`
- `HasCrCard`
- `IsActiveMember`
- `EstimatedSalary`

Các cột tùy chọn:

- `id`
- `CustomerId`
- `Surname`
- `Exited`

### 2.5. Đầu ra là gì?

Đầu ra chính hiện tại là:

- dữ liệu đã validate
- dữ liệu bị reject
- output prediction + segmentation + recommendation
- diagnostics dạng JSON / CSV
- workbook Excel cho business
- log và manifest để truy vết run

### 2.6. Vì sao hệ thống này tồn tại?

Repository hiện tại tồn tại để làm 3 việc cùng lúc:

1. giữ lại toàn bộ **di sản nghiên cứu** từ thời notebook
2. cung cấp một **demo app local** có thể chạy thật
3. tạo nền tảng đủ sạch để sau này có thể:
   - mở rộng demo
   - thêm DB persistence thật
   - thêm API nếu cần
   - hoặc dần dần thay thế wrapper tạm bằng logic serving chắc chắn hơn

---

## 3. Phần “causal AI” trong repo này thực sự có nghĩa gì?

Đây là phần quan trọng nhất để hiểu lại repo một cách thực tế.

### 3.1. “Causal AI” trong ngữ cảnh dự án này là gì?

Trong repo này, “causal AI” không chỉ là “dự đoán ai churn”, mà là cố gắng trả lời thêm:

- nếu áp dụng một chương trình giữ chân nào đó cho khách hàng / nhóm khách hàng
- thì xác suất churn có thể thay đổi như thế nào
- và treatment nào có vẻ tốt hơn so với treatment khác

Ý tưởng lớn là đi từ:

- **predictive ML**

đến:

- **treatment recommendation**

thay vì chỉ dừng ở churn score.

### 3.2. Trong repo này, các khái niệm đang được hiểu như thế nào?

#### `treatment`

Là chương trình hoặc hành động giữ chân khách hàng.

Trong runtime hiện tại, các treatment option được khai báo trong [contracts.py](src/causal_app/schemas/contracts.py):

- `No Program`
- `Wealth Accumulator Program`
- `Engage & Elevate`
- `Starter Growth Plan`
- `Reconnect & Reward`
- `Premium Balance Rewards`

#### `outcome`

Outcome mà repo quan tâm thực chất là:

- xác suất churn sau can thiệp
- hay nói đơn giản hơn: churn có giảm hay không sau khi áp treatment

Trong runtime hiện tại, outcome không phải là một biến “real-world observed outcome” được theo dõi online.

Nó là giá trị được suy ra từ dữ liệu legacy, cụ thể là bảng `df_causal_ai`.

#### `recommendation`

Là đề xuất treatment tốt nhất hiện tại cho một record đầu vào.

Trong runtime, treatment được chọn dựa trên:

- cluster của khách hàng
- churn probability hiện tại
- bảng policy summary được tạo từ legacy `df_causal_ai`

#### `effect`

Trong runtime hiện tại, effect gần nhất với khái niệm này là:

- `expected_absolute_change`
- `estimated_post_churn`

Tức là repo đang biểu diễn tác động như một thay đổi kỳ vọng trong xác suất churn.

### 3.3. Phần nào là prediction?

Phần prediction hiện chạy thật trong runtime là:

- [legacy_churn.py](src/causal_app/models/churn/legacy_churn.py)

Nó dùng:

- preprocessing notebook-derived trong [legacy_bank.py](src/causal_app/preprocessing/legacy_bank.py)
- `GradientBoostingClassifier`
- dữ liệu legacy `train.csv`

Điểm rất quan trọng:

- đây là **temporary shim**
- không phải artifact gốc được train và lưu từ thời nghiên cứu
- nếu không có artifact phù hợp, code sẽ build lại từ `legacy train.csv`

### 3.4. Phần nào là segmentation?

Phần segmentation runtime nằm ở:

- [legacy_segmentation.py](src/causal_app/models/segmentation/legacy_segmentation.py)

Nó:

- không tái hiện toàn bộ pipeline embedding/clustering phức tạp trong notebook 3
- mà học một wrapper gần đúng từ `df_cluster.csv`
- dùng `NearestCentroid`

Tức là:

- đây là **segmentation wrapper**
- không phải artifact clustering gốc từ notebook research

### 3.5. Phần nào là recommendation?

Phần recommendation runtime nằm ở:

- [legacy_policy.py](src/causal_app/models/recommendation/legacy_policy.py)

Nó:

- đọc `df_causal_ai`
- nhóm dữ liệu theo `cluser_label` và `Treatment`
- tính thống kê như `mean_p_pre`, `mean_p_post`, `mean_delta`
- chọn treatment tốt nhất theo bảng policy tóm tắt

Điểm quan trọng:

- runtime hiện tại **không** chạy lại toàn bộ causal estimator notebook 6
- runtime hiện tại **không** build một causal graph mới
- runtime hiện tại **không** serve DoWhy / DRLearner / ForestDRLearner như một service inference thật

Nó đang dùng một **cluster-level policy summary** rút ra từ dữ liệu legacy.

### 3.6. Phần nào là simulation?

Phần simulation vẫn là một thành phần rất quan trọng của câu chuyện hiện tại.

Theo notebook legacy và flow runtime:

- dữ liệu `df_causal_ai` là đầu vào then chốt cho recommendation runtime
- nhưng `df_causal_ai` không phải raw intervention log từ production system
- nó là kết quả downstream của pipeline nghiên cứu, có gắn treatment và `p_churn_post`

Điều này có nghĩa:

- một phần rất đáng kể của “causal recommendation” hiện tại vẫn mang tính **simulation-backed**
- không nên mô tả nó như hệ thống causal inference production-grade trên dữ liệu intervention thật

### 3.7. Phần nào thật sự có thể coi là causal inference?

Nếu xét **theo notebook nghiên cứu**, notebook 6 có:

- `causallearn`
- `dowhy`
- causal graph
- matching / refutation / learner

Nếu xét **theo runtime hiện tại**, phần “causal inference” thật sự đang được dùng là rất hạn chế:

- runtime chỉ dùng policy summary đã được rút từ dữ liệu legacy downstream
- không dùng trực tiếp graph discovery hoặc causal estimators notebook-level mỗi lần chạy

Vì vậy, cách nói trung thực nhất là:

- repo có **gốc nghiên cứu causal AI**
- nhưng demo runtime hiện tại là một **local decision-support demo**
- trong đó recommendation layer vẫn phụ thuộc vào **legacy simulated causal table**

### 3.8. Hàm ý business của mô hình là gì?

Repo hiện tại đang gửi đi thông điệp business như sau:

- không chỉ ưu tiên khách hàng theo churn risk
- mà còn gợi ý treatment nào nên đi kèm
- treatment được chọn theo pattern quan sát trong dữ liệu legacy đã được tổng hợp

Về mặt business, output phù hợp nhất hiện tại là:

- **ưu tiên ai trước**
- **dùng policy nào trước**
- **vì sao policy đó được đề xuất**

Chứ không phải:

- cam kết chắc chắn rằng treatment đó sẽ tạo hiệu ứng nhân quả ngoài đời thực

---

## 4. Kiến trúc end-to-end của hệ thống hiện tại

## 4.1. Bức tranh tổng thể

Luồng hiện tại có thể hiểu ngắn gọn như sau:

```text
Upload file
  -> đọc file CSV/XLSX
  -> validate schema + kiểu dữ liệu + duplicate
  -> profiling nhẹ
  -> preprocessing
  -> churn prediction
  -> segmentation
  -> recommendation
  -> diagnostics
  -> export CSV/JSON/Excel
  -> process tracking + log + manifest
```

## 4.2. Luồng chi tiết từng bước

### Bước 1. Upload dữ liệu

Điểm vào UI:

- [01_Upload.py](apps/streamlit/pages/01_Upload.py)

Chức năng:

- nhận file người dùng upload
- hoặc đăng ký file example legacy `test.csv`
- lưu file vào `storage/uploads/`
- ghi metadata upload vào file `.upload.json`

Input:

- file `CSV` hoặc `XLSX`

Output:

- file đã lưu trong `storage/uploads/`
- metadata upload

### Bước 2. Đọc file

Module:

- [files.py](src/causal_app/ingestion/files.py)

Chức năng:

- kiểm tra path có tồn tại không
- kiểm tra suffix có phải `.csv` hoặc `.xlsx` không
- đọc file bằng `pandas`
- chặn file rỗng

Input:

- path tới file input

Output:

- `DataFrame`

### Bước 3. Validation

Module:

- [validation.py](src/causal_app/ingestion/validation.py)

Chức năng:

- chuẩn hóa tên cột
- thêm `_source_row_number`
- kiểm tra cột bắt buộc
- chuẩn hóa `Gender`
- chuẩn hóa `Geography`
- ép kiểu numeric
- ép kiểu binary
- kiểm tra duplicate theo `CustomerId`, nếu không có thì `id`
- tách `accepted` và `rejected`

Input:

- raw `DataFrame`

Output:

- `accepted_df`
- `rejected_df`
- `ValidationResult`

Ý nghĩa business:

- đây là lớp bảo vệ đầu tiên để không đưa dữ liệu bẩn vào pipeline

### Bước 4. Profiling

Module:

- [summary.py](src/causal_app/profiling/summary.py)

UI:

- [02_Data_Profiling.py](apps/streamlit/pages/02_Data_Profiling.py)

Chức năng:

- đếm số dòng, số cột
- tổng hợp tình trạng cột
- thiếu dữ liệu
- duplicate summary
- numeric summary

Lưu ý:

- đây chỉ là **profiling nhẹ**
- không phải profiling engine đầy đủ kiểu `ydata-profiling`

### Bước 5. Preprocessing

Module:

- [legacy_bank.py](src/causal_app/preprocessing/legacy_bank.py)

Chức năng:

- bỏ metadata columns như `id`, `CustomerId`, `Surname`
- xử lý kiểu dữ liệu
- tạo `Age_Group`
- scale / encode một số trường

Repo hiện có 2 projection quan trọng:

1. pipeline churn
2. feature projector cho segmentation / causal-style downstream

### Bước 6. Churn prediction

Module:

- [legacy_churn.py](src/causal_app/models/churn/legacy_churn.py)

Input:

- `accepted_df`

Output:

- `churn_probability`

Artifact hiện có:

- `artifacts/models/phase_03/legacy_churn_pipeline.pkl`
- `artifacts/models/phase_03/legacy_churn_pipeline.json`

Lưu ý:

- artifact hiện có trên disk là wrapper tạm, không phải artifact gốc từ nghiên cứu
- JSON metadata hiện đang **không hoàn toàn đồng bộ** với convention mới nhất trong code Phase 6

### Bước 7. Segmentation

Module:

- [legacy_segmentation.py](src/causal_app/models/segmentation/legacy_segmentation.py)

Input:

- `accepted_df`

Output:

- `assigned_cluster`

Artifact hiện có:

- `artifacts/models/phase_03/legacy_cluster_segmenter.pkl`
- `artifacts/models/phase_03/legacy_cluster_segmenter.json`

Lưu ý:

- cluster này là wrapper từ `df_cluster.csv`
- không phải full notebook clustering stack

### Bước 8. Recommendation

Module:

- [legacy_policy.py](src/causal_app/models/recommendation/legacy_policy.py)

Input:

- `assigned_cluster`
- `churn_probability`

Output:

- `recommended_treatment`
- `estimated_post_churn`
- `expected_absolute_change`
- `policy_scope`
- `policy_sample_size`

Artifact hiện có:

- `artifacts/models/phase_03/legacy_policy_summary.csv`
- `artifacts/models/phase_03/legacy_policy_summary.json`

Lưu ý quan trọng:

- logic này dựa trên bảng legacy `df_causal_ai`
- đây là **policy wrapper**
- không phải causal serving layer production-ready

### Bước 9. Diagnostics

Module:

- [summary.py](src/causal_app/models/diagnostics/summary.py)

Output diagnostics gồm:

- số dòng input / accepted / rejected
- duplicate key column
- reject reason counts
- cluster counts
- treatment counts
- churn summary
- stage results

File sinh ra:

- `diagnostics.json`

### Bước 10. Export

Module:

- [excel.py](src/causal_app/export/excel.py)
- [business_output.py](src/causal_app/export/business_output.py)

Output:

- workbook Excel
- CSV kỹ thuật
- summary JSON

### Bước 11. Process tracking

UI:

- [03_Process_Tracking.py](apps/streamlit/pages/03_Process_Tracking.py)

Nguồn dữ liệu:

- `run_summary.json`
- `diagnostics.json`
- `artifact_manifest.json`
- `run.log`

### Bước 12. Storage và traceability

Storage runtime:

- `storage/uploads/`
- `storage/runs/`
- `storage/profiles/`
- `storage/exports/`
- `storage/logs/`

Traceability hiện có:

- `run_summary.json`
- `artifact_manifest.json`
- `run.log`
- `pipeline.log`

---

## 5. Giải thích từng folder lớn

## 5.1. Bảng tổng hợp nhanh

| Folder | Chứa gì | Vai trò | Trạng thái |
| --- | --- | --- | --- |
| `instructs/` | project memory | lưu quyết định, lịch sử phase, open items | hỗ trợ bảo trì |
| `src/` | core Python package | nguồn logic runtime chính | source-of-truth runtime |
| `apps/` | Streamlit UI | lớp demo/app | runtime thật |
| `docs/` | tài liệu | giải thích repo, startup, kiến trúc, data | support material |
| `notebooks/` | placeholder notebook mới | chưa dùng nhiều | scaffold |
| `storage/` | output runtime | upload, run output, export, log | generated output |
| `artifacts/` | model wrapper artifacts | artifact local cho engine | generated/runtime support |
| `db/` | SQL bootstrap | nền cho Postgres | scaffold |
| `configs/` | README placeholder cho config tương lai | nơi dự kiến để config hóa sau này | scaffold |
| `tests/` | test tự động | pytest unit/integration nhỏ | thật, nhưng còn mỏng |
| `legacy_snapshot/` | repo cũ archive | nguồn tham chiếu lịch sử | legacy |
| `data/` | placeholder data chuẩn hóa tương lai | chưa là nguồn dữ liệu chính | scaffold |

## 5.2. `instructs/`

Đây là “project memory”.

Vai trò:

- giữ quyết định kiến trúc
- giữ các caveat quan trọng
- nhắc future agent hoặc future self phải tôn trọng gì

Sau lượt cleanup này, trạng thái hiện tại là:

- `instructs/` root chỉ còn:
  - `PROJECT_MEMORY_MASTER.md`
  - `OPEN_ITEMS.md`
  - `archive/`
- phase history cũ đã được đưa vào `instructs/archive/`

### `src/`

Đây là **nguồn logic runtime chính**.

Nếu hỏi “khi app chạy thật thì logic ở đâu?”, câu trả lời là:

- ở `src/causal_app/`

Các nhóm module chính:

- `ingestion/`
- `profiling/`
- `preprocessing/`
- `models/`
- `pipeline/`
- `export/`
- `schemas/`
- `utils/`

### `apps/`

Hiện tại chỉ có:

- `apps/streamlit/`

Vai trò:

- lớp giao diện local cho người dùng kỹ thuật
- không phải backend service riêng
- gọi trực tiếp Python core engine

### `docs/`

Chứa tài liệu hiện hành.

Nhóm tài liệu nổi bật:

- `docs/PROJECT_MASTER_GUIDE_VI.md`
- `docs/user_guide/`
- `docs/architecture/`
- `docs/migration/`
- `docs/data_dictionary/`

### `notebooks/`

Hiện tại về bản chất là **placeholder**.

Notebook research thật đang nằm trong:

- `legacy_snapshot/.../*.ipynb`

Tức là:

- `notebooks/` hiện chưa phải nơi source-of-truth của research notebook

### `storage/`

Đây là nơi chứa **output runtime sinh ra trong lúc chạy**.

Ý nghĩa từng thư mục:

- `uploads/`: file input đã đăng ký / upload
- `runs/`: toàn bộ output theo từng run
- `profiles/`: chỗ để dành cho profile output tương lai
- `exports/`: workbook Excel
- `logs/`: log dùng chung

Lưu ý:

- đây là generated output
- không phải code nguồn

### `artifacts/`

Đây là nơi chứa model artifacts local mà engine dùng.

Hiện tại đáng chú ý nhất là:

- `artifacts/models/phase_03/`

Nó chứa:

- churn wrapper artifact
- segmentation wrapper artifact
- policy summary artifact

### `db/`

Chứa:

- `db/init/001_foundation.sql`

Vai trò:

- khởi tạo schema Postgres cơ bản khi chạy Docker

Nhưng hiện trạng:

- app chưa ghi dữ liệu vào Postgres
- nên đây là scaffold thật nhưng chưa được wiring vào flow runtime

### `configs/`

Hiện tại chủ yếu là placeholder.

Các file README ở đây nói rất rõ:

- chưa có config schema cuối cùng
- chưa có config serving-ready

Vì vậy:

- `configs/` tồn tại để mở đường
- chứ chưa phải nơi app thực sự phụ thuộc mạnh

### `tests/`

Hiện đã có test thật, nhưng phạm vi còn nhỏ.

Test đang tập trung vào:

- ingestion
- validation
- business output shaping
- export workbook
- artifact manifest

### `legacy_snapshot/`

Đây là phần cực kỳ quan trọng để hiểu repo.

Nó là:

- bundle cũ nguyên vẹn
- gồm notebook, data, slide, image, README cũ
- được giữ lại để không mất traceability

Phần lớn câu chuyện học thuật / nghiên cứu causal AI ban đầu vẫn nằm ở đây.

### `data/`

Hiện tại là placeholder.

Theo đúng repo state:

- chưa có dữ liệu canonical được promote vào đây
- dữ liệu legacy vẫn nằm trong `legacy_snapshot/.../Data/`

---

## 6. Giải thích tech stack

## 6.1. Python

### Nó là gì?

Ngôn ngữ chính của repo.

### Dùng để làm gì trong dự án này?

- viết core engine
- viết Streamlit app
- đọc file dữ liệu
- chạy preprocessing, prediction, export

### Có đang dùng thật không?

- Có, đây là lớp cốt lõi nhất

### Có thể thay thế không?

- Về lý thuyết có thể, nhưng không thực tế với repo này

## 6.2. `pandas`

### Dùng để làm gì?

- đọc `CSV/XLSX`
- xử lý dataframe
- validation
- diagnostics
- export Excel/CSV

### Có đang dùng thật không?

- Có, dùng rất nhiều

## 6.3. `scikit-learn`

### Dùng để làm gì?

- `GradientBoostingClassifier`
- preprocessing pipeline
- encoding / scaling
- `NearestCentroid`

### Có đang dùng thật không?

- Có

### Caveat

- một phần logic vẫn là notebook-derived wrapper chứ không phải pipeline production clean-room

## 6.4. Streamlit

### Nó là gì?

Framework Python để dựng web app nhanh cho data app/demo app.

### Dùng để làm gì trong dự án này?

- tạo demo UI local
- upload file
- xem profiling
- theo dõi process
- xem dashboard
- tải export

### Có đang dùng thật không?

- Có

### Có bắt buộc không?

- Với demo hiện tại, gần như là giao diện chính

### Có thể thay thế bằng gì?

- Gradio
- FastAPI + frontend riêng
- Dash

Nhưng hiện tại Streamlit là lựa chọn hợp lý nhất vì repo vẫn thiên về local demo.

## 6.5. Postgres

### Nó là gì?

Database quan hệ.

### Dùng để làm gì trong dự án này?

Ở thời điểm hiện tại:

- chỉ mới có **foundation schema**
- chưa phải nơi app ghi run thật

### Có đang dùng thật không?

- Mức scaffold là có
- Mức app runtime thật thì chưa

### Có bắt buộc không?

- Chưa bắt buộc để demo local

## 6.6. Docker / Docker Compose

### Docker là gì?

Docker cho phép đóng gói app vào container để chạy nhất quán hơn.

### `Dockerfile` trong repo này dùng để làm gì?

- build image Python + app
- copy code cần thiết vào image
- cài dependency
- chạy Streamlit

### `docker-compose.yml` dùng để làm gì?

- chạy nhiều service cùng lúc
- hiện tại là:
  - `app`
  - `postgres`

### Có đang dùng thật không?

- Có, ở mức local startup path

### Có bắt buộc không?

- Không bắt buộc, vì repo vẫn chạy được qua `.venv`

## 6.7. `openpyxl`

### Dùng để làm gì?

- ghi workbook Excel
- format header, freeze panes, autofilter, width

### Có đang dùng thật không?

- Có

## 6.8. `pytest`

### Dùng để làm gì?

- chạy test tự động

### Có đang dùng thật không?

- Có

Hiện tại test suite còn nhỏ nhưng là test thật.

## 6.9. FastAPI

### Có trong repo không?

- Không có code FastAPI runtime trong repo hiện tại

### Vậy nó xuất hiện ở đâu?

- chỉ xuất hiện như một quyết định kiến trúc trong memory Phase 6
- theo hướng: “có thể cân nhắc sau, nhưng chưa nên thêm bây giờ”

### Kết luận

- FastAPI hiện tại **không phải** một thành phần đang được dùng thật

---

## 7. Docker, Docker Compose, Postgres và quan hệ giữa các thành phần

## 7.1. `Dockerfile` là gì trong repo này?

File này mô tả cách build image cho app.

Nó đang làm các việc chính:

- dùng base image `python:3.11-slim`
- cài `build-essential`, `libpq-dev`
- copy source code, docs, legacy snapshot, artifacts vào image
- tạo sẵn thư mục `storage/...`
- `pip install -e .`
- chạy `streamlit run apps/streamlit/app.py`

Nói đơn giản:

- đây là “công thức đóng gói app”

## 7.2. `docker-compose.yml` là gì trong repo này?

Đây là file orchestration local.

Nó định nghĩa 2 service:

### `postgres`

- dùng image `postgres:16-alpine`
- mở port `5432`
- mount `db/init/` để init schema
- có persistent volume `postgres_data`

### `app`

- build từ `Dockerfile`
- mở port `8501`
- mount `./storage` vào `/app/storage`
- truyền env vars như:
  - `APP_NAME`
  - `APP_ENV`
  - `LOG_LEVEL`
  - `POSTGRES_*`
  - `DATABASE_URL`
  - `STORAGE_ROOT`

## 7.3. Volume dùng để làm gì?

### Volume database

- `postgres_data`
- dùng để giữ dữ liệu Postgres sau khi restart container

### Bind mount app storage

- `./storage:/app/storage`

Mục đích:

- giữ upload, run output, export, log trên máy host
- không để mất output khi recreate container

## 7.4. Postgres schema hiện có gì?

Trong [001_foundation.sql](db/init/001_foundation.sql), hiện có 4 bảng:

1. `uploaded_dataset`
2. `pipeline_run`
3. `stage_execution_log`
4. `export_file`

Ý nghĩa:

- đây là nền để sau này lưu metadata upload/run/export

Nhưng hiện trạng rất quan trọng:

- Streamlit app **chưa ghi** dữ liệu vào các bảng này
- process tracking hiện vẫn là **file-based**

## 7.5. Quan hệ giữa Streamlit, core engine, Postgres, Docker

### Quan hệ hiện tại

- **Streamlit** là giao diện
- **core engine trong `src/`** là nơi xử lý thật
- **storage/** là nơi lưu output runtime thật
- **Postgres** mới là scaffold, chưa là nguồn run-state chính
- **Docker** chỉ là cách chạy gói local stack dễ hơn

### Quan hệ chưa có

- Streamlit chưa gọi một REST API backend riêng
- Streamlit chưa dùng Postgres như nguồn dữ liệu chính

---

## 8. Model và pipeline hiện tại

## 8.1. Có những model / wrapper nào đang tồn tại?

### Churn model

- class: `LegacyChurnModel`
- file: [legacy_churn.py](src/causal_app/models/churn/legacy_churn.py)
- artifact:
  - `legacy_churn_pipeline.pkl`
  - `legacy_churn_pipeline.json`

### Segmentation model

- class: `LegacySegmenter`
- file: [legacy_segmentation.py](src/causal_app/models/segmentation/legacy_segmentation.py)
- artifact:
  - `legacy_cluster_segmenter.pkl`
  - `legacy_cluster_segmenter.json`

### Recommendation policy wrapper

- class: `LegacyPolicyRecommender`
- file: [legacy_policy.py](src/causal_app/models/recommendation/legacy_policy.py)
- artifact:
  - `legacy_policy_summary.csv`
  - `legacy_policy_summary.json`

## 8.2. Prediction output là gì?

Prediction output cốt lõi là:

- `churn_probability`

Nó là xác suất churn theo wrapper churn hiện tại.

## 8.3. Segmentation output là gì?

- `assigned_cluster`

Đây là ID cluster mà khách hàng được gán vào.

## 8.4. Recommendation output là gì?

Các cột chính:

- `recommended_treatment`
- `estimated_post_churn`
- `expected_absolute_change`
- `policy_scope`
- `policy_sample_size`

## 8.5. Diagnostics output là gì?

File `diagnostics.json` đang chứa:

- `input_rows`
- `accepted_rows`
- `rejected_rows`
- `duplicate_key_column`
- `validation_reject_reason_counts`
- `diagnostic_reject_reason_counts`
- `cluster_counts`
- `recommended_treatment_counts`
- `churn_probability_summary`
- `stage_results`

## 8.6. Luồng phụ thuộc giữa các bước

```text
raw input
  -> validate_input_dataframe
  -> accepted_df
     -> LegacyCausalFeatureProjector / preprocessing
     -> LegacyChurnModel.predict_proba
     -> LegacySegmenter.predict
     -> LegacyPolicyRecommender.recommend
     -> final recommendations
     -> diagnostics + workbook + csv/json outputs
```

---

## 9. Giải thích output Excel

Đây là phần bắt buộc nếu muốn hiểu repo ở góc độ business.

Workbook được tạo bởi:

- [excel.py](src/causal_app/export/excel.py)

Logic shaping business output nằm ở:

- [business_output.py](src/causal_app/export/business_output.py)

## 9.1. Workbook có những sheet nào?

Theo runtime hiện tại:

- `Summary`
- `Customer_Action_List`
- `Reject_Report`
- `Run_Metadata`
- `Field_Definitions`

## 9.2. `Summary` để làm gì?

Sheet này dành cho:

- người xem business tổng quát
- data scientist cần snapshot nhanh

Nó trả lời các câu hỏi:

- file có bao nhiêu dòng?
- có bao nhiêu dòng hợp lệ?
- có bao nhiêu dòng bị reject?
- priority phân bố thế nào?
- risk level phân bố thế nào?
- policy phân bố thế nào?
- hạn chế quan trọng là gì?

## 9.3. `Customer_Action_List` để làm gì?

Đây là sheet quan trọng nhất cho sales/business.

Các cột đáng chú ý:

- `customer_id`
- `churn_probability`
- `risk_level`
- `segment_id`
- `recommended_policy`
- `expected_post_churn`
- `expected_improvement`
- `priority_score`
- `priority_band`
- `reason_short`
- `policy_support_rows`
- `warning_note`

### Sheet này dùng cho ai?

- sales
- retention team
- người cần một danh sách ưu tiên hành động

### `priority` là gì?

Hiện tại là logic **deterministic**, không phải AI explanation hoặc tối ưu revenue phức tạp.

Nguồn:

- `churn_probability`
- `expected_absolute_change`

Derived:

- `risk_level`
- `expected_improvement`
- `priority_score`
- `priority_band`

Rule hiện tại:

- `High` nếu `churn_probability >= 0.75`
- `Medium` nếu `>= 0.50`
- còn lại `Low`
- `P1` nếu High và improvement đủ lớn
- `P2` nếu High, hoặc Medium + improvement đủ
- còn lại `P3`

### `reason_short` là gì?

Đây là mô tả ngắn, **rule-based** và **template-based**.

Nó không dùng GPT, không dùng LLM.

Nó lấy từ các trường:

- `risk_level`
- `recommended_policy`
- `segment_id`
- `expected_improvement`
- `policy_scope`

Ví dụ:

- `High churn risk; Engage & Elevate is prioritized for cluster 1 based on the strongest estimated reduction.`

Ý nghĩa:

- giúp business hiểu nhanh vì sao record được đưa lên danh sách hành động
- nhưng không được hiểu là diễn giải causal đầy đủ

## 9.4. `Reject_Report` để làm gì?

Sheet này phục vụ:

- data owner
- người sửa file input
- vận hành dữ liệu

Nó cho biết:

- dòng nào bị reject
- reject vì lý do gì
- reason code
- diễn giải người đọc hiểu được

Ví dụ lý do:

- duplicate `CustomerId`
- invalid `Gender`
- invalid `Geography`
- invalid field dạng số / binary

## 9.5. `Run_Metadata` để làm gì?

Dùng để truy vết:

- run id
- file input
- export path
- stage timing snapshot

Đây là sheet quan trọng khi cần:

- gửi workbook cho người khác nhưng vẫn muốn biết nó được sinh từ run nào

## 9.6. `Field_Definitions` để làm gì?

Là từ điển cột nhẹ.

Nó nói:

- cột này đến từ field nào
- ý nghĩa là gì
- cách derive là gì

## 9.7. Output nào dành cho sales, output nào dành cho data scientist?

### Dành cho sales/business

- `Customer_Action_List`
- `Summary`

### Dành cho vận hành dữ liệu

- `Reject_Report`

### Dành cho data scientist / technical reviewer

- `Run_Metadata`
- `Field_Definitions`
- `policy_options.csv`
- `diagnostics.json`
- `run_summary.json`
- `artifact_manifest.json`
- `run.log`

---

## 10. Dữ liệu và artifact trong repo

## 10.1. Dữ liệu legacy đang ở đâu?

Dữ liệu legacy hiện nằm trong:

- `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/`

Các file quan trọng đã quan sát được:

- `train.csv` `(165034, 14)`
- `test.csv` `(110023, 13)`
- `df_train_clean.csv`
- `data from remote sever/df_cluster.csv`
- `data from remote sever/Pre_Treatment.csv`
- `data from remote sever/df_causal_ai`
- `data from remote sever/train_result.csv`

## 10.2. Ý nghĩa thực dụng của từng file legacy quan trọng

### `train.csv`

Dataset train thô có:

- feature khách hàng
- `Exited`

Đây là raw starting point quan trọng nhất cho runtime churn wrapper hiện tại.

### `test.csv`

Dataset holdout-style không có `Exited`.

Hiện được dùng như sample demo tiện lợi cho upload / smoke run.

### `df_cluster.csv`

Dữ liệu đã gắn `Cluster`.

Runtime segmentation wrapper hiện học từ file này.

### `Pre_Treatment.csv`

Dữ liệu trung gian đã được project sang schema causal-style hơn.

Nó giúp hiểu giai đoạn giữa churn / cluster và causal stage trong research flow.

### `df_causal_ai`

File rất quan trọng trong câu chuyện causal.

Nó có các cột:

- feature đã xử lý
- `p_pre`
- `cluser_label`
- `Treatment`
- `p_churn_post`

Runtime recommendation hiện phụ thuộc trực tiếp vào file này.

### `train_result.csv`

Log kết quả train của causal estimators trong legacy research.

Nó không phải runtime source-of-truth cho app hiện tại.

## 10.3. Artifact runtime hiện tại ở đâu?

Trong:

- `artifacts/models/phase_03/`

Đây là artifact local cho demo engine, không phải registry hoàn chỉnh.

## 10.4. Generated outputs hiện tại ở đâu?

Trong:

- `storage/uploads/`
- `storage/runs/`
- `storage/exports/`
- `storage/logs/`

Repo hiện đang có một số sample run thật đã sinh trước đó.

Điểm quan trọng:

- đây là generated outputs
- không nên nhầm với code nguồn

---

## 11. Cách chạy dự án

## 11.1. Chạy bằng Python local

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/pip install pytest
.venv/bin/streamlit run apps/streamlit/app.py
```

Mở:

- `http://localhost:8501`

## 11.2. Chạy bằng Docker

```bash
docker compose up --build
```

Sau đó mở:

- `http://localhost:8501`

## 11.3. Biến môi trường chính

Trong `.env.example` hiện có:

- `APP_NAME`
- `APP_ENV`
- `LOG_LEVEL`
- `STREAMLIT_PORT`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DATABASE_URL`
- `STORAGE_ROOT`

## 11.4. Sau khi startup thì kỳ vọng thấy gì?

UI có 5 phần chính:

- `Upload`
- `Data Profiling`
- `Process Tracking`
- `Dashboard`
- `Export`

## 11.5. Output được lưu ở đâu?

### Upload

- `storage/uploads/<upload-id>__<filename>`
- `storage/uploads/<upload-id>.upload.json`

### Theo từng run

- `storage/runs/<run-id>/prepared_features.csv`
- `storage/runs/<run-id>/recommendations.csv`
- `storage/runs/<run-id>/rejected_rows.csv`
- `storage/runs/<run-id>/policy_options.csv`
- `storage/runs/<run-id>/diagnostics.json`
- `storage/runs/<run-id>/run_summary.json`
- `storage/runs/<run-id>/run.log`
- `storage/runs/<run-id>/artifact_manifest.json`

### Workbook

- `storage/exports/<run-id>.xlsx`

### Log dùng chung

- `storage/logs/pipeline.log`

## 11.6. Các lỗi thường gặp

### Docker daemon chưa chạy

Khi dùng Docker, nếu daemon chưa chạy thì `docker compose` sẽ fail.

### Thiếu dependency nếu chạy local

Nếu không cài `.venv` đúng cách, app và pipeline sẽ không chạy.

### Reject quá nhiều dòng

Với sample legacy `test.csv`, số reject có thể rất lớn do duplicate `CustomerId`.

### Hiểu nhầm về causal validity

Nếu coi recommendation hiện tại như causal service production-ready thì sẽ hiểu sai hệ thống.

---

## 12. Những giới hạn hiện tại

## 12.1. Cái gì là “real”?

Những thứ đang là thật và chạy được:

- Streamlit app local
- ingestion CSV/XLSX
- validation
- profiling nhẹ
- churn wrapper inference
- segmentation wrapper inference
- recommendation wrapper inference
- diagnostics
- Excel export
- file-based process tracking
- test tự động nhỏ
- log và manifest

## 12.2. Cái gì là “partial”?

- recommendation logic vẫn là wrapper từ legacy simulated policy data
- profiling chưa sâu
- Postgres đã có schema nhưng app chưa dùng
- artifact versioning đã có convention nhưng file artifact cũ trên disk chưa đồng bộ hoàn toàn

## 12.3. Cái gì là “legacy”?

- toàn bộ notebook research
- dataset trung gian cũ
- slide, ảnh, README cũ
- nested `.git` trong legacy snapshot

## 12.4. Cái gì là “scaffold / placeholder”?

- `data/raw`, `data/interim`, `data/samples`
- `notebooks/research`, `notebooks/reports`, `notebooks/archive`
- `configs/`

## 12.5. Owner cần cẩn thận điều gì?

1. Đừng overclaim causal inference runtime hiện tại.
2. Đừng nhầm wrapper artifact hiện tại với artifact nghiên cứu gốc.
3. Đừng coi Postgres là nguồn state thật của app lúc này.
4. Đừng coi notebook cũ là pipeline production sạch.
5. Đừng quên `legacy_snapshot/` hiện vẫn là dependency quan trọng.

---

## 13. Hướng phát triển tiếp theo

## 13.1. Những gì nên giữ ổn định

- contract input hiện tại
- luồng upload -> validate -> run -> export
- workbook business-friendly hiện tại
- log + manifest per run

## 13.2. Những gì có thể cải thiện tiếp

- surfacing failed runs rõ hơn trong app
- dùng Postgres thật cho run metadata
- thêm regression test trên sample run lớn
- làm rõ business meaning của `policy_support_rows`
- tạo curated sample dataset sạch trong `data/samples/`

## 13.3. Có cần FastAPI ngay không?

Theo repo hiện tại:

- **chưa cần ngay**

Lý do:

- Streamlit vẫn là consumer chính
- app chưa dùng DB như backend thật
- recommendation layer còn đang tạm

Nếu sau này cần:

- nhiều client hơn
- UI khác ngoài Streamlit
- automation qua HTTP
- service boundary rõ hơn

thì khi đó FastAPI mới đáng đưa vào.

## 13.4. Streamlit hiện tại có đủ không?

Cho mục tiêu:

- demo local
- thử nghiệm nội bộ
- trình bày luồng end-to-end

thì **đủ**.

Cho mục tiêu:

- multi-client
- backend API reuse
- production service

thì **chưa đủ**.

---

## 14. Kết luận ngắn gọn

Nếu phải tóm repo hiện tại trong một đoạn:

> Đây là một repo đã được chuyển dần từ notebook nghiên cứu causal AI về churn banking sang một local demo platform bằng Python. Hệ thống hiện đã chạy được end-to-end theo hướng upload dữ liệu, validate, chấm churn, gán segment, đề xuất treatment, sinh diagnostics và export Excel. Tuy nhiên, lớp recommendation hiện tại vẫn là wrapper dựa trên dữ liệu causal legacy có yếu tố simulation, chưa phải causal serving production-grade. Repo đã sạch hơn nhiều, dễ hiểu hơn, và đủ tốt để demo hoặc tiếp tục mở rộng, nhưng vẫn cần giữ sự trung thực về giới hạn của phần causal và persistence hiện tại.

Nếu bạn quay lại repo sau 6-12 tháng, hãy đọc theo thứ tự này:

1. `README.md`
2. `docs/PROJECT_MASTER_GUIDE_VI.md`
3. `instructs/PROJECT_MEMORY_MASTER.md`
4. `instructs/OPEN_ITEMS.md`
5. sau đó mới đi vào `src/`, `apps/`, và `legacy_snapshot/`
