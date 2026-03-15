# File Inventory Baseline

Baseline captured before Phase 2 restructuring.

| Path | Type | Current purpose | Recommendation | Notes |
| --- | --- | --- | --- | --- |
| `Causal-AI-Models-An-Automated-Treatments-Approach-to-Customer-Retention-in-the-Banking-Sector/` | nested repo folder | Main legacy research/demo bundle | archive | Contains its own `.git`; preserve as legacy bundle. |
| `.../README.md` | markdown | Legacy project overview | keep | Useful historical overview; later superseded by root README. |
| `.../slide.pdf` | pdf | Presentation artifact | archive | Not runtime logic. |
| `.../01.png` | image | Methodology/result figure | keep | Useful doc asset. |
| `.../1_Estimated_Loss_Profit_by_Churn.ipynb` | notebook | Business framing and churn economics | keep | Research/report notebook. |
| `.../2_Predict Churn Model.ipynb` | notebook | EDA, preprocessing, churn training, SHAP/PDP | convert | Reusable logic later belongs in Python modules. |
| `.../3_Clustering Model.ipynb` | notebook | Clustering experiments and plots | convert | Keep exploratory narrative later, extract reusable logic. |
| `.../4_Clustering_Analyst.ipynb` | notebook | Cluster profiling and narrative recommendations | keep | Could remain as reporting notebook. |
| `.../5_CAI_P_Post_Generated.ipynb` | notebook | Pipeline reuse, churn pre-score, treatment simulation | convert | Important future module source, but preserve legacy behavior first. |
| `.../6_CAI_Model.ipynb` | notebook | Causal graph, matching, estimators, treatment recommendations | convert | Important future module source, but still research-bound today. |
| `.../Save_Model.ipynb` | notebook | Duplicate pipeline save/load notebook | deprecate | Strong overlap with notebook 5. |
| `.../Data/train.csv` | csv | Likely canonical raw train data | keep | Highest-confidence raw train dataset observed. |
| `.../Data/test.csv` | csv | Likely canonical raw test data | keep | Highest-confidence raw test dataset observed. |
| `.../Data/df_train_clean.csv` | csv | Derived cleaned export | keep | Important reference intermediate; later should be regenerable. |
| `.../Data/data from remote sever/` | folder | Legacy working export folder | archive | Name contains typo; holds mixed duplicates and derived outputs. |
| `.../Data/data from remote sever/train.csv` | csv | Duplicate raw train export | archive | Observed duplicate of root `train.csv`. |
| `.../Data/data from remote sever/1_df_train.csv` | csv | Alternate duplicate raw train export | archive | Observed duplicate of root `train.csv`. |
| `.../Data/data from remote sever/df_train_clean.csv` | csv | Duplicate cleaned export | archive | Observed duplicate of root `df_train_clean.csv`. |
| `.../Data/data from remote sever/df_cluster.csv` | csv | Derived clustering output | keep | Important legacy intermediate. |
| `.../Data/data from remote sever/Pre_Treatment.csv` | csv | Derived pre-treatment stage output | keep | Important observed intermediate, still ambiguous. |
| `.../Data/data from remote sever/df_causal_ai` | extensionless csv-like file | Derived causal stage dataset | keep | Important observed intermediate; missing extension. |
| `.../Data/data from remote sever/train_result.csv` | csv | Legacy causal model training log | keep | Likely future experiments artifact. |
| `instructs/*.md` | markdown | Persistent phase memory | keep | Source of truth for phased modernization. |

## Notes

- No Python package, tests, dependency manifest, or app/runtime scaffolding were observed in the legacy bundle at baseline.
- Phase 2 should preserve legacy files rather than rewriting them.
