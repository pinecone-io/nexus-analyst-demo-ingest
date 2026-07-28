"""Upload /tmp/acme_data/*.parquet → BigQuery `nexus-analyst-demo.acme.*`.

Run: python -m datasets.acme.upload_bq
"""

from __future__ import annotations

import subprocess
from pathlib import Path

PROJECT = "nexus-analyst-demo"
DATASET = "acme"
SRC = Path("/tmp/acme_data")
LOCATION = "US"


def run(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}")
    return subprocess.call(cmd)


def main() -> None:
    # Create dataset (idempotent — error if exists is OK)
    print(f"=== Creating dataset {PROJECT}:{DATASET} (no-op if exists) ===")
    subprocess.call([
        "bq", f"--location={LOCATION}", "mk", "--dataset",
        "--description=Acme Inc — synthetic Enterprise BI demo for Nexus Analyst.",
        f"{PROJECT}:{DATASET}",
    ])

    parquets = sorted(SRC.glob("*.parquet"))
    print(f"\n=== Loading {len(parquets)} tables ===")
    for p in parquets:
        table = p.stem
        rc = run([
            "bq", "load",
            "--source_format=PARQUET",
            "--replace",
            f"--location={LOCATION}",
            f"{PROJECT}:{DATASET}.{table}",
            str(p),
        ])
        if rc != 0:
            print(f"  !! {table} FAILED")

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
