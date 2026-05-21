# nexus-analyst-demo-ingest

Source materials + ship scripts for the [Nexus Analyst](https://github.com/pinecone-io/nexus-analyst-demo) demo.

Two destinations:
- **Nexus context** (used by `agent-nexus`) — `upload_to_nexus.py`
- **Pinecone index** (used by `agent-classic`) — `index_pinecone.py`

Both read from the same `sources/<dataset>/` markdown corpus.

## Layout

```
sources/
  acme/                        synthetic enterprise warehouse — 126 docs (dbt
                               models, glossaries, Slack threads, Gong calls,
                               Notion runbooks, query logs, postmortems)
  acme-raw/                    raw pre-curation Acme corpus
eval/
  build.md                     dataset-agnostic spec for the Nexus build agent
  acme/                        Acme retrieval eval sets (v3 + legacy)
datasets/
  acme/manifest.yaml           per-dataset metadata (bq_reference, context slug)
upload_to_nexus.py             Nexus REST uploader + curate/build triggers
index_pinecone.py              Pinecone semantic-index ingester
LICENSES/                      upstream license texts
NOTICE.md                      per-source attribution
```

Each source file is a markdown doc with YAML frontmatter (`title`, `source_url`,
`license`, `attribution`, `fetched_at`, `adapter`). PDFs are accepted too —
Nexus reads them directly.

## Add a source

1. Confirm permissive license (MIT, Apache 2.0, CC-BY, public domain, or
   `synthetic-demo` for fixture data).
2. Drop the file under `sources/<dataset>/`. Use the adapter prefix as a hint:
   - `bq_schema__*` — BigQuery schema dumps
   - `dbt__model__*` — dbt model docs
   - `glossary__*` — metric definitions
   - `gong__*` — sales call transcripts
   - `notion__*` / `notion_runbook__*` — internal runbooks
   - `slack__*` — thread transcripts
   - `query_log__*` — analyst query examples
   - `postmortem__*` — incident postmortems
3. Include frontmatter:
   ```yaml
   ---
   title: "Human-readable title"
   source_url: https://...
   license: mit | apache-2.0 | cc-by-4.0 | cc0-1.0 | pd-us-gov | synthetic-demo
   attribution: "Upstream attribution string"
   fetched_at: 2026-04-30T...
   adapter: bq_schema | dbt_model | glossary | gong_call | ...
   ---
   ```
4. Update `NOTICE.md` if the source is new upstream.

## Ship to Nexus

```bash
uv venv && source .venv/bin/activate
uv pip install -e .
export PINECONE_API_KEY=pcsk_...
export NEXUS_API_URL=https://<your-nexus-host>/api/v0   # or dev

# Discover existing contexts
python upload_to_nexus.py --list-contexts

# Full one-shot: upload sources + build.md + eval, then curate
python upload_to_nexus.py --context-id <slug-or-uuid> --dataset acme --all

# Granular flags
python upload_to_nexus.py --context-id <slug> --dataset acme --upload-sources
python upload_to_nexus.py --context-id <slug> --upload-build-md --upload-eval
python upload_to_nexus.py --context-id <slug> --trigger-curate
python upload_to_nexus.py --context-id <slug> --trigger-build
python upload_to_nexus.py --context-id <slug> --list-tasks
```

`--context-id` accepts either a UUID or a slug.

## Ship to Pinecone (classic baseline)

```bash
export PINECONE_API_KEY=pcsk_...

# Create the index once (CLI)
pc index create -n nexus-analyst-classic -m cosine -c aws -r us-east-1 \
    --model llama-text-embed-v2 --field_map text=content

# Index sources
python index_pinecone.py --dataset acme --namespace acme
```

## License gate

Source files carry a `license:` frontmatter field. Permissive set:

`mit, apache-2.0, bsd-2-clause, bsd-3-clause, isc, cc0-1.0, unlicense, pd-us-gov, cc-by-4.0, nyc-open-data, synthetic-demo`

Anything outside this set is dropped at upload time. Source-of-truth is the
upstream artifact (repo `LICENSE` file, page footer) — see `NOTICE.md` for full
per-source attribution.
