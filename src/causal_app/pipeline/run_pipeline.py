from __future__ import annotations

import argparse
from pathlib import Path

from causal_app.pipeline.engine import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local causal AI pipeline without notebooks.")
    parser.add_argument("--input", required=True, help="Path to the input CSV or XLSX file.")
    parser.add_argument(
        "--run-label",
        default=None,
        help="Optional human-readable label to include in the generated run id.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Optional explicit run output directory. Defaults to storage/runs/<generated-run-id>/",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    result = run_pipeline(
        input_path=Path(args.input),
        run_label=args.run_label,
        output_dir=Path(args.output_dir) if args.output_dir else None,
    )
    print(f"run_id={result.run_id}")
    print(f"run_dir={result.run_dir}")
    print(f"export_path={result.export_path}")
    print(f"accepted_rows={result.accepted_rows}")
    print(f"rejected_rows={result.rejected_rows}")


if __name__ == "__main__":
    main()
