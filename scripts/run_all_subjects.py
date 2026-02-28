# scripts/run_all_subjects.py
# Run full preprocessing for all subjects listed in subjects_stress.txt
# Works locally and on PVC via DATA_ROOT env var.

from pathlib import Path
import os
import sys
import subprocess

# ---- Portable paths ----
SCRIPT_DIR = Path(__file__).resolve().parent          # .../scripts
PROJECT_ROOT = SCRIPT_DIR.parent                      # repo root
DATA_ROOT = Path(os.environ.get("DATA_ROOT", PROJECT_ROOT / "data"))

PROCESSED_ROOT = DATA_ROOT / "processed" / "physionet_e4"
SUBJECT_LIST = PROCESSED_ROOT / "subjects_stress.txt"

SCRIPT_ALIGN = SCRIPT_DIR / "preprocess_one_subject.py"
SCRIPT_LABEL = SCRIPT_DIR / "label_and_window_subject.py"


def run_checked(cmd, env):
    print("\n>>", " ".join(cmd))
    subprocess.check_call(cmd, env=env)


def main():
    if not SUBJECT_LIST.exists():
        raise FileNotFoundError(
            f"Missing subject list: {SUBJECT_LIST}\n"
            f"Did you run scripts/make_subject_list.py with DATA_ROOT={DATA_ROOT}?"
        )

    subjects = [s.strip() for s in SUBJECT_LIST.read_text().splitlines() if s.strip()]
    print(f"DATA_ROOT: {DATA_ROOT}")
    print(f"Running full preprocessing for {len(subjects)} subjects...")

    env = os.environ.copy()
    env["DATA_ROOT"] = str(DATA_ROOT)

    ok = 0
    failures = []

    for s in subjects:
        print(f"\n=== {s} ===")
        try:
            # 1) create aligned64
            run_checked([sys.executable, str(SCRIPT_ALIGN), "--subject", s], env)

            # 2) label + windows
            run_checked([sys.executable, str(SCRIPT_LABEL), "--subject", s], env)

            ok += 1
        except Exception as e:
            failures.append(s)
            print(f"FAILED for {s}: {e}")

    print("\n====================")
    print(f"Done. OK={ok}, FAIL={len(failures)}")
    if failures:
        print("Failures:", failures)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
