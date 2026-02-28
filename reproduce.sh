#!/usr/bin/env bash
set -euo pipefail

DATA_ROOT="${DATA_ROOT:-$(pwd)/data}"
export DATA_ROOT

echo "DATA_ROOT: $DATA_ROOT"

# 1) Download raw dataset (skip if already present)
if [ ! -d "$DATA_ROOT/raw/physionet_e4/Wearable_Dataset" ]; then
  bash scripts/download_physionet_e4.sh
else
  echo "[download] Raw dataset already present; skipping."
fi

# 2) Run preprocessing pipeline
python scripts/make_subject_list.py
python scripts/run_all_subjects.py
python scripts/summarize_windows.py

echo "Done. Outputs in: $DATA_ROOT/processed/physionet_e4/"