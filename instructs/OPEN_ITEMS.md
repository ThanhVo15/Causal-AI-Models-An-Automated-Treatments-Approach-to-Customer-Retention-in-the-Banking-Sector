# Open Items

## 1. Kiến trúc / sản phẩm

- Streamlit vẫn là UI chính và hiện đủ cho local demo.
- FastAPI chưa cần thêm ngay.
- Postgres vẫn chưa được dùng trong app flow thực tế.

## 2. Causal / recommendation

- Recommendation runtime vẫn phụ thuộc vào legacy `df_causal_ai`.
- Chưa có causal serving layer thật từ notebook 6.
- Không có confidence/business value score chuẩn hóa.

## 3. Dữ liệu

- `data/` vẫn là placeholder.
- Chưa có curated sample dataset sạch trong `data/samples/`.
- `df_causal_ai` vẫn là file legacy không có extension và có ý nghĩa rất quan trọng nhưng không hoàn toàn “clean”.

## 4. Testing / runtime

- Chưa có browser automation cho Streamlit.
- Chưa có Dockerized integration test.
- Chưa có regression test cho full sample run lớn.

## 5. Persistence / observability

- Failed runs chưa được đưa lên app như first-class records.
- Log đã có file-based traceability nhưng chưa có UI log viewer.
- Postgres tables hiện vẫn chưa nhận dữ liệu thật từ app.

## 6. Business output

- `policy_support_rows` chưa có meaning business thống nhất.
- Chưa có revenue-weighted priority.
- Chưa có business stakeholder sign-off chính thức cho workbook.
