"""Upload /tmp/acme_ecomm_data/*.parquet -> BigQuery `nexus-analyst-demo.acme_ecomm.*`.

Run: python datasets/acme-ecomm/upload_bq.py

Additive only -- creates/loads the acme_ecomm dataset, never touches the
existing acme dataset (the SaaS Acme Inc demo).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

PROJECT = "nexus-analyst-demo"
DATASET = "acme_ecomm"
SRC = Path("/tmp/acme_ecomm_data")
LOCATION = "US"


def run(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}")
    return subprocess.call(cmd)


def main() -> None:
    print(f"=== Creating dataset {PROJECT}:{DATASET} (no-op if exists) ===")
    subprocess.call([
        "bq", f"--location={LOCATION}", "mk", "--dataset",
        "--description=Acme (eCommerce) -- synthetic omnichannel retailer + marketplace demo for Nexus Analyst. "
        "Digital commerce + marketplace + membership. Distinct from the acme (Acme Inc SaaS) dataset.",
        f"{PROJECT}:{DATASET}",
    ])

    parquets = sorted(SRC.glob("*.parquet"))
    print(f"\n=== Loading {len(parquets)} tables ===")
    failed = []
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
            failed.append(table)

    print("\n=== Done ===")
    if failed:
        print(f"FAILED tables: {failed}")


if __name__ == "__main__":
    main()
