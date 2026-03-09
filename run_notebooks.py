"""Re-execute all recipe .ipynb notebooks in-place from the project root."""

import glob
import sys
import time

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

PROJECT_ROOT = "/Users/gareth/dev/benchmark-urbanism/cityseer-examples"
DELAY = 10

notebooks = sorted(glob.glob("recipes/**/*.ipynb", recursive=True))
failed = []

for nb_path in notebooks:
    print(f"=== Running: {nb_path} ===", flush=True)
    try:
        with open(nb_path) as f:
            nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
        ep.preprocess(nb, {"metadata": {"path": PROJECT_ROOT}})
        with open(nb_path, "w") as f:
            nbformat.write(nb, f)
        print(f"OK: {nb_path}", flush=True)
    except Exception as e:
        failed.append((nb_path, str(e).split("\n")[-1]))
        print(f"FAILED: {nb_path} — {failed[-1][1]}", flush=True)
    print(f"Waiting {DELAY}s...", flush=True)
    time.sleep(DELAY)

print("\n=== Summary ===")
if failed:
    print(f"{len(failed)} notebooks failed:")
    for path, err in failed:
        print(f"  {path}: {err}")
    sys.exit(1)
else:
    print(f"All {len(notebooks)} notebooks succeeded.")
