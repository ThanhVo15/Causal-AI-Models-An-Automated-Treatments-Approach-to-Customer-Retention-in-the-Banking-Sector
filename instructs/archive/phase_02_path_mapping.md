# Phase 02 Path Mapping

## Executed Moves

| Old path | New path | Status | Notes |
| --- | --- | --- | --- |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/` | moved | Full legacy bundle archived intact. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/README.md` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/README.md` | moved-with-parent | No content change. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/1_Estimated_Loss_Profit_by_Churn.ipynb` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/1_Estimated_Loss_Profit_by_Churn.ipynb` | moved-with-parent | Preserved untouched. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/2_Predict Churn Model.ipynb` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/2_Predict Churn Model.ipynb` | moved-with-parent | Preserved untouched. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/3_Clustering Model.ipynb` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/3_Clustering Model.ipynb` | moved-with-parent | Preserved untouched. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/4_Clustering_Analyst.ipynb` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/4_Clustering_Analyst.ipynb` | moved-with-parent | Preserved untouched. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/5_CAI_P_Post_Generated.ipynb` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/5_CAI_P_Post_Generated.ipynb` | moved-with-parent | Preserved untouched. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/6_CAI_Model.ipynb` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/6_CAI_Model.ipynb` | moved-with-parent | Preserved untouched. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Save_Model.ipynb` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Save_Model.ipynb` | moved-with-parent | Preserved untouched. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/Data/` | moved-with-parent | Preserved untouched. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/slide.pdf` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/slide.pdf` | moved-with-parent | Preserved untouched. |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/01.png` | `legacy_snapshot/Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/01.png` | moved-with-parent | Preserved untouched. |

## New Scaffolded Paths

| Path | Status | Notes |
| --- | --- | --- |
| `README.md` | scaffolded | New root overview for the modernized repo layout. |
| `pyproject.toml` | scaffolded | Minimal Python package manifest. |
| `.env.example` | scaffolded | Minimal env template. |
| `Dockerfile` | scaffolded | Streamlit app image foundation. |
| `docker-compose.yml` | scaffolded | Local app + Postgres stack. |
| `src/causal_app/` | scaffolded | Future reusable package boundary. |
| `apps/streamlit/` | scaffolded | Minimal UI shell and pages. |
| `db/init/001_foundation.sql` | scaffolded | Minimal Postgres bootstrap. |
| `storage/` | scaffolded | Persistent local runtime directories. |
| `docs/migration/` | scaffolded | Phase 1 lock artifacts. |

## Explicit Non-Moves

| Path | Status | Notes |
| --- | --- | --- |
| `instructs/` | untouched | Kept at repo root as persistent project memory. |
| archived legacy bundle internals | untouched after move | No internal rewrites or notebook extraction were performed in Phase 2. |
| new `data/` directories | empty placeholders | No legacy datasets were promoted into them yet. |
| new `notebooks/` directories | empty placeholders except READMEs | No legacy notebooks were migrated into them yet. |
