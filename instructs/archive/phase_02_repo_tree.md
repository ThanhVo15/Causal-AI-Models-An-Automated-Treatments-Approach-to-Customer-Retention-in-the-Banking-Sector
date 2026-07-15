# Phase 02 Repo Tree

Tree below reflects the intended structural view after Phase 2.
Auto-generated caches such as `__pycache__/` are omitted from this summary.

```text
repo/
  README.md
  pyproject.toml
  .env.example
  .gitignore
  .dockerignore
  Dockerfile
  docker-compose.yml

  instructs/
    phase_01_baseline.md
    phase_01_file_inventory.md
    phase_01_flow_map.md
    phase_01_open_questions.md
    phase_02_restructure_summary.md
    phase_02_repo_tree.md
    phase_02_path_mapping.md
    phase_02_open_items.md

  configs/
    app/README.md
    model/README.md
    data/README.md

  data/
    raw/README.md
    interim/README.md
    samples/README.md

  storage/
    uploads/.gitkeep
    runs/.gitkeep
    profiles/.gitkeep
    exports/.gitkeep
    logs/.gitkeep

  db/
    init/
      001_foundation.sql

  notebooks/
    research/README.md
    reports/README.md
    archive/README.md

  src/
    causal_app/
      __init__.py
      config.py
      ingestion/__init__.py
      profiling/__init__.py
      pipeline/__init__.py
      preprocessing/__init__.py
      models/
        __init__.py
        churn/__init__.py
        segmentation/__init__.py
        recommendation/__init__.py
        diagnostics/__init__.py
      export/__init__.py
      schemas/__init__.py
      utils/
        __init__.py
        paths.py
        status.py

  artifacts/
    models/.gitkeep
    figures/.gitkeep
    experiments/.gitkeep

  apps/
    streamlit/
      app.py
      pages/
        01_Upload.py
        02_Data_Profiling.py
        03_Process_Tracking.py
        04_Dashboard.py
        05_Export.py

  docs/
    architecture/
      local_demo_foundation.md
    migration/
      phase_1_audit_baseline.md
      file_inventory.md
      move_plan.md
      canonical_data_notes.md
    data_dictionary/
      legacy_data_sources.md
    user_guide/
      local_startup.md

  tests/
    unit/.gitkeep
    integration/.gitkeep
    fixtures/.gitkeep

  legacy_snapshot/
    README.md
    Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/
      README.md
      *.ipynb
      Data/
      slide.pdf
      01.png
      .git/
```

## Major Directory Meanings

- `legacy_snapshot/`: untouched archived research bundle
- `src/causal_app/`: future reusable application code
- `apps/streamlit/`: current local UI scaffold
- `db/init/`: minimal Postgres bootstrap
- `storage/`: persisted local runtime data
- `docs/migration/`: frozen migration baseline artifacts
- `instructs/`: persistent phase memory
