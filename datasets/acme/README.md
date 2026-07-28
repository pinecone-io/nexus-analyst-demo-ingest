# acme dataset — generation toolchain

Acme Inc is a fictitious B2B SaaS workflow-automation company. This directory
generates both halves of the demo dataset: the BigQuery warehouse and the
internal-document corpus that describes it.

`CANON.md` is the contract. Both halves must agree with it, and every generated
document must agree with every other. Read it before changing anything here.

## Warehouse

```bash
uv run --with pandas --with numpy --with faker python -m datasets.acme.generate_bq
python datasets/acme/upload_bq.py        # bq load --replace into nexus-analyst-demo:acme
```

`generate_bq.py` is deterministic — `SEED=42`, `TODAY=2026-05-04`,
`FOUNDED=2023-01-01` — and writes 13 base tables as parquet to `/tmp/acme_data`.
Row-count targets are per-function constants (`n_target=...`), so it rescales.

It does **not** build the 5 derived marts (`arr_snapshot`, `nrr_trailing_12`,
`account_health`, `bookings_attribution`, `workflow_runs_daily`). Those are
`CREATE OR REPLACE TABLE` DDL; the documentation-grade equivalents live in
`sources/acme-raw/dbt/marts/`.

## Documents

```bash
uv run --no-project --with google-genai python datasets/acme/gen_docs.py
uv run --no-project --with google-genai python datasets/acme/gen_one.py <out> <adapter> <topic> <focus>
uv run --no-project --with google-genai python datasets/acme/gen_grow.py <file> <prompt> [target_kb]
```

`gen_docs.py` holds a `FILES` list of declarative specs (path / adapter / topic /
focus), injects `CANON.md` as immutable fact, and writes into `sources/acme-raw/`.
It skips files that already exist, so reruns are additive. `gen_one.py` does a
single file; `gen_grow.py` appends to an existing one until it hits a size target
(this is how the 300–500 KB bulk files were built).

Model and project are env-overridable:

| var | default |
|---|---|
| `GEN_MODEL` | `gemini-3.5-flash-lite` |
| `VERTEX_PROJECT_ID` | `mission-control-350520` |

Output volume is what costs money here, so the renderer wants a cheap model and a
detailed spec — not the reverse. The largest, most signal-dense files in the
existing corpus were hand-authored rather than rendered; that remains the right
call for anchor documents.

## Two layers, two destinations

`sources/acme-raw/` is the noisy layer, organised by system of record (slack,
gong, meetings, query_logs, postmortems, docs, dbt, schema, scratch). It is what
the nexus context is built from.

`sources/acme/` is the curated layer — one topic per file — and is what the
Pinecone baseline index is built from. See the repo README for the ship scripts.
