# Phase 01 Flow Map

## Observed High-Level Flow

1. Business framing
   - `1_Estimated_Loss_Profit_by_Churn.ipynb`
   - Reads a train-style dataset from a hardcoded external path and explores revenue/loss framing.

2. Churn modeling
   - `2_Predict Churn Model.ipynb`
   - Reads `train.csv` and `test.csv` from hardcoded paths.
   - Performs EDA, cleaning, feature selection, model comparison, SHAP, and PDP.
   - Selects/uses Gradient Boosting as an important downstream churn model.

3. Saved preprocessing/churn pipeline
   - `Save_Model.ipynb`
   - Rebuilds custom preprocessing classes and a `GradientBoostingClassifier` pipeline.
   - Saves/loads the pipeline to an external path, not into the repo.

4. Clustering / segmentation
   - `3_Clustering Model.ipynb`
   - Reads raw train data from a hardcoded external path.
   - Cleans/scales data, engineers `Age_Group`, experiments with embeddings and multiple clustering methods.
   - Exports `df_cluster.csv`.

5. Cluster analysis / narrative
   - `4_Clustering_Analyst.ipynb`
   - Reads `df_cluster.csv`.
   - Produces descriptive cluster plots and narrative/policy-style analysis.

6. Post-treatment simulation / causal input building
   - `5_CAI_P_Post_Generated.ipynb`
   - Reads `df_cluster.csv` and a train-style dataset from hardcoded external paths.
   - Recreates the preprocessing + churn pipeline.
   - Produces `p_pre`, assigns treatments by cluster, simulates treatment effects, and attempts to write a causal-stage dataset.

7. Causal recommendation / effect analysis
   - `6_CAI_Model.ipynb`
   - Reads `df_causal_ai`.
   - Builds an FCI causal graph with background knowledge.
   - Runs matching/IPW-style preparation and trains causal estimators such as DRLearner, ForestDRLearner, and SNet.
   - Produces treatment recommendation/effect summaries and writes `train_result.csv`.

## Observed Data Dependency Chain

- Likely raw starting point:
  - `Data/train.csv`
  - `Data/test.csv`
- Observed derived chain:
  - `train.csv` -> `df_train_clean.csv`
  - `df_train_clean.csv` / cleaned train features -> `df_cluster.csv`
  - `df_cluster.csv` + churn pipeline output -> pre-treatment / causal-style dataset
  - causal-style dataset -> `df_causal_ai`
  - `df_causal_ai` -> `train_result.csv`

## Likely Canonical Datasets

- Most likely canonical raw datasets:
  - `Data/train.csv`
  - `Data/test.csv`
- Most likely important observed derived datasets:
  - `Data/df_train_clean.csv`
  - `Data/data from remote sever/df_cluster.csv`
  - `Data/data from remote sever/Pre_Treatment.csv`
  - `Data/data from remote sever/df_causal_ai`
- Confidence note:
  - raw train/test are the clearest canonical files
  - canonical status of the intermediate derived files is less certain because generation is notebook-driven and duplicated across paths

## Dependencies and Ambiguities

- Notebook 5 appears to depend on both:
  - cluster output from notebook 3
  - a saved churn pipeline equivalent to `Save_Model.ipynb`
- Notebook 6 depends on `df_causal_ai` already existing.
- Notebook 5 references `df_cai` without defining it inside the notebook, which suggests hidden state or a missing step.
- Notebook 3 contains experimental branches with undefined `rfm_data`, GPU-only imports, and recorded errors, so not every branch is part of a clean canonical flow.
- Multiple environment/path styles exist:
  - Google Colab paths
  - Windows drive paths
  - Linux server paths
- This makes the observed flow semantically understandable but not yet reproducible end-to-end from a clean environment.

## Important Interpretation Risk

- The causal stage currently appears to rely on simulated treatment assignment and simulated post-treatment churn probabilities.
- Future phases must not accidentally describe the current repo as if it were already trained on real observed intervention outcomes unless that is later verified and documented separately.
