CREATE TABLE IF NOT EXISTS uploaded_dataset (
    id BIGSERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    row_count BIGINT,
    column_count BIGINT,
    status TEXT NOT NULL DEFAULT 'received',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pipeline_run (
    id BIGSERIAL PRIMARY KEY,
    dataset_id BIGINT REFERENCES uploaded_dataset(id),
    run_label TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stage_execution_log (
    id BIGSERIAL PRIMARY KEY,
    run_id BIGINT REFERENCES pipeline_run(id),
    stage_name TEXT NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS export_file (
    id BIGSERIAL PRIMARY KEY,
    run_id BIGINT REFERENCES pipeline_run(id),
    file_name TEXT NOT NULL,
    storage_path TEXT NOT NULL,
    export_type TEXT NOT NULL DEFAULT 'unknown',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
