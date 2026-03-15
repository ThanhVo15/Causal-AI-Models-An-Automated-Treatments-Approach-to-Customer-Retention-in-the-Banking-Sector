# Phase 01 File Inventory

Observed from the current workspace only. Recommendations are planning guidance, not implemented changes.

| Path | Current role | Recommendation | Notes |
| --- | --- | --- | --- |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/` | Actual nested project folder containing code, data, docs, and its own `.git` | keep | Important structural note: the project is nested inside the workspace root. |
| `.../README.md` | High-level project description and methodology summary | keep | Rewrite later for maintainability and honest scope; currently presentation-oriented. |
| `.../slide.pdf` | Presentation artifact | archive | Useful historical/presentation context, not runtime logic. |
| `.../01.png` | Static methodology/result image used in README | keep | Later likely move to docs/assets. |
| `.../1_Estimated_Loss_Profit_by_Churn.ipynb` | Business framing / revenue-churn estimation notebook | keep | Research/business context notebook; not a serving module candidate. |
| `.../2_Predict Churn Model.ipynb` | EDA, preprocessing, feature selection, churn model training, SHAP/PDP | convert | Keep a slim notebook later, but extract reusable preprocessing/training/inference logic. |
| `.../3_Clustering Model.ipynb` | Clustering experimentation, embeddings, cluster evaluation, plots | convert | Keep a slim exploratory notebook later; extract reusable clustering logic and plotting helpers. |
| `.../4_Clustering_Analyst.ipynb` | Cluster descriptive analysis and narrative recommendations | keep | Could later stay as report notebook or become docs. |
| `.../5_CAI_P_Post_Generated.ipynb` | Preprocessing pipeline reuse, churn pre-score generation, synthetic treatment/post-outcome simulation | convert | Core reusable logic is a future module candidate; notebook currently mixes pipeline saving, simulation, and analysis. |
| `.../6_CAI_Model.ipynb` | Causal graph, matching/IPW, causal estimators, recommendation/effect analysis | convert | Keep a slim comparison/report notebook later; extract graph/matching/recommendation logic. |
| `.../Save_Model.ipynb` | Duplicate/overlapping pipeline save-load notebook | deprecate | Strong duplication with notebook 5; likely absorb into later Python module/script. |
| `.../Data/` | Current data/artifact directory | keep | Needs later separation into raw/interim/artifacts, but not yet changed. |
| `.../Data/train.csv` | Raw observed training dataset | keep | Most likely canonical raw train file observed in repo. |
| `.../Data/test.csv` | Raw observed test dataset | keep | Most likely canonical raw test file observed in repo. |
| `.../Data/df_train_clean.csv` | Derived cleaned/preprocessed export | keep | Useful reference for flow understanding; later should become regenerable interim data. |
| `.../Data/data from remote sever/` | Working export folder from prior environment | archive | Folder name contains typo; appears to mix duplicates and intermediate outputs. |
| `.../Data/data from remote sever/train.csv` | Duplicate raw train export | archive | Same content as root `Data/train.csv` was observed by checksum. |
| `.../Data/data from remote sever/1_df_train.csv` | Duplicate raw train export under alternate name | archive | Same content as root `Data/train.csv` was observed by checksum. |
| `.../Data/data from remote sever/df_train_clean.csv` | Duplicate cleaned export | archive | Same content as root `Data/df_train_clean.csv` was observed by checksum. |
| `.../Data/data from remote sever/df_cluster.csv` | Derived clustered dataset export | keep | Important for understanding flow; later should become regenerable interim artifact. |
| `.../Data/data from remote sever/Pre_Treatment.csv` | Derived pre-treatment style dataset export | keep | Important observed intermediate, but currently not clearly documented. |
| `.../Data/data from remote sever/df_causal_ai` | Derived causal-stage dataset export | keep | Important observed intermediate; note the missing file extension and unclear generation path. |
| `.../Data/data from remote sever/train_result.csv` | Training result log for causal estimators | keep | Observed experiment log, not source data. Later likely move to artifacts/experiments. |

## Additional Notes

- No `.py` source files were observed in the current nested project.
- No `requirements.txt`, `pyproject.toml`, `environment.yml`, `Makefile`, or tests were observed.
- Notebook-heavy logic means the inventory is organized around notebooks and exported CSVs rather than modules/scripts.
