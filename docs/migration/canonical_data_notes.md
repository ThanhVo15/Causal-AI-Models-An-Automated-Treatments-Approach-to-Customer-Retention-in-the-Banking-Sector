# Canonical Data Notes

Baseline notes from Phase 1 audit, preserved before Phase 2 restructuring.

## Most Likely Canonical Raw Datasets

- `Data/train.csv`
- `Data/test.csv`

These were the clearest raw datasets observed in the legacy bundle.

## Important Observed Derived Datasets

- `Data/df_train_clean.csv`
- `Data/data from remote sever/df_cluster.csv`
- `Data/data from remote sever/Pre_Treatment.csv`
- `Data/data from remote sever/df_causal_ai`
- `Data/data from remote sever/train_result.csv`

## Duplicates / Ambiguities

- `Data/data from remote sever/train.csv` appears to duplicate `Data/train.csv`.
- `Data/data from remote sever/1_df_train.csv` appears to duplicate `Data/train.csv`.
- `Data/data from remote sever/df_train_clean.csv` appears to duplicate `Data/df_train_clean.csv`.
- `df_causal_ai` has no file extension.
- The exact generation path for some derived datasets is notebook-driven and not fully reproducible from a clean environment.

## Working Assumptions for Phase 2

- Preserve all observed legacy datasets.
- Do not rename or normalize ambiguous data files yet.
- Treat raw `train.csv` and `test.csv` as the most likely canonical starting point.
- Treat other derived datasets as important legacy intermediates, not yet stable runtime assets.

## Items To Confirm Later

- Whether `df_causal_ai` should remain an extensionless legacy artifact or become a normalized exported dataset in a later phase.
- Which derived files should become official `data/interim/` assets versus which should remain archived legacy outputs.
- Whether future serving logic should rely on any current simulated post-treatment datasets at all.
