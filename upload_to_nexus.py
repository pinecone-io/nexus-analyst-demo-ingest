"""
Upload nexus-analyst-ingest output + eval/build instructions into a Nexus context.

Talks to a Nexus deployment's REST API (auth, context listing, source upload,
strategy/build + curate triggers, task status). Point it at your own Nexus
host via NEXUS_API_URL or --api-base.

Usage:
  export PINECONE_API_KEY=...
  export NEXUS_API_URL=https://<your-nexus-host>/api/v0   # optional, override default

  # See available contexts (create them in the console first)
  python upload_to_nexus.py --list-contexts

  # Full one-shot for Acme: upload artifacts + build.md + eval, then curate + build
  python upload_to_nexus.py --context-id <UUID> --dataset acme --all

  # Just upload artifacts (no curate, no eval)
  python upload_to_nexus.py --context-id <UUID> --dataset acme

  # Upload eval + build.md only, then trigger build
  python upload_to_nexus.py --context-id <UUID> --dataset acme \
      --upload-eval --upload-build-md --trigger-build

  # List async tasks (curate / build) for a context
  python upload_to_nexus.py --context-id <UUID> --list-tasks
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import httpx

DEFAULT_API_BASE = "https://<your-nexus-host>/api/v0"
REPO_ROOT = Path(__file__).resolve().parent


def api_base_url(cli_override: str | None) -> str:
    if cli_override:
        return cli_override.rstrip("/")
    return (
        os.getenv("NEXUS_API_URL")
        or os.getenv("AUTOCONTEXT_API_URL")
        or DEFAULT_API_BASE
    ).rstrip("/")


def get_token(client: httpx.Client, api_key: str, base: str) -> str:
    resp = client.post(f"{base}/auth/login", json={"api_key": api_key})
    resp.raise_for_status()
    return resp.json()["token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def list_contexts(client: httpx.Client, token: str, base: str) -> None:
    resp = client.get(f"{base}/contexts", headers=auth_headers(token))
    resp.raise_for_status()
    rows = resp.json()
    if not rows:
        print("No contexts found. Create one in the Nexus console first.")
        return
    print("id\tname")
    for context in rows:
        print(f"{context.get('id')}\t{context.get('name', '?')}")


_MIME = {
    ".md": "text/markdown",
    ".txt": "text/plain",
    ".json": "application/json",
    ".pdf": "application/pdf",
    ".csv": "text/csv",
    ".html": "text/html",
    ".ipynb": "application/x-ipynb+json",
}


def upload_file(
    client: httpx.Client,
    token: str,
    base: str,
    context_id: str,
    file_path: Path,
    upload_path: str,
) -> bool:
    url = f"{base}/contexts/{context_id}/source/upload"
    params = {"path": upload_path} if upload_path else {}
    mime = _MIME.get(file_path.suffix.lower(), "application/octet-stream")
    with open(file_path, "rb") as f:
        files = {"file": (file_path.name, f, mime)}
        resp = client.post(url, headers=auth_headers(token), params=params, files=files)
    if resp.status_code == 200:
        return True
    print(f"  WARN: {file_path.name} -> {resp.status_code}: {resp.text[:200]}")
    return False


def upload_directory(
    client: httpx.Client,
    token: str,
    base: str,
    context_id: str,
    source_dir: Path,
    upload_path: str,
    extensions: tuple[str, ...] = (".md", ".txt", ".json", ".pdf", ".csv", ".ipynb"),
) -> dict:
    files = sorted(
        f for f in source_dir.rglob("*") if f.is_file() and f.suffix in extensions
    )
    print(f"Found {len(files)} files in {source_dir}")
    uploaded = 0
    failed = 0
    for i, fpath in enumerate(files):
        rel = fpath.relative_to(source_dir)
        target = (
            f"{upload_path}/{rel.parent}" if str(rel.parent) != "." else upload_path
        )
        if upload_file(client, token, base, context_id, fpath, target):
            uploaded += 1
        else:
            failed += 1
        if (i + 1) % 50 == 0:
            time.sleep(0.5)  # courteous pacing
    return {"total": len(files), "uploaded": uploaded, "failed": failed}


def upload_build_md(
    client: httpx.Client,
    token: str,
    base: str,
    context_id: str,
    md_path: Path,
) -> None:
    """Upload build.md to the context's code workspace.

    Endpoint per autocontext repo `api/src/rest/handlers/context_code.rs`:
        PUT /contexts/{slug-or-id}/code/build/instructions
        body: {"content": "<markdown>"}
    Creator-only (auth.principal must match context creator).
    """
    content = md_path.read_text()
    resp = client.put(
        f"{base}/contexts/{context_id}/code/build/instructions",
        headers={**auth_headers(token), "Content-Type": "application/json"},
        json={"content": content},
    )
    resp.raise_for_status()
    print(f"build.md uploaded ({len(content):,} chars): {resp.status_code}")


def clear_evals(
    client: httpx.Client, token: str, base: str, context_id: str
) -> int:
    """Delete every existing eval on the context. Returns count deleted."""
    resp = client.get(
        f"{base}/contexts/{context_id}/evals", headers=auth_headers(token)
    )
    resp.raise_for_status()
    evals = resp.json().get("evals", [])
    n = 0
    for ev in evals:
        eid = ev.get("id")
        if not eid:
            continue
        d = client.delete(
            f"{base}/contexts/{context_id}/evals/{eid}",
            headers=auth_headers(token),
        )
        if d.status_code == 200:
            n += 1
    return n


def upload_eval(
    client: httpx.Client,
    token: str,
    base: str,
    context_id: str,
    eval_path: Path,
    replace: bool = True,
) -> None:
    """Upload retrieval eval set: one POST per case to /evals.

    Old autocontext API stored evals as a single `eval.json` file; current dev
    API exposes per-case CRUD at `/contexts/{id}/evals` with payload
    `{input, expected_output}` (server assigns id; `match_type` is implicit).
    """
    with open(eval_path) as f:
        data = json.load(f)
    cases = data.get("test_cases", data) if isinstance(data, dict) else data

    if replace:
        deleted = clear_evals(client, token, base, context_id)
        if deleted:
            print(f"  cleared {deleted} existing evals")

    posted = 0
    failed = 0
    for case in cases:
        body = {
            "input": case["input"],
            "expected_output": case.get("expected_output", ""),
        }
        r = client.post(
            f"{base}/contexts/{context_id}/evals",
            headers={**auth_headers(token), "Content-Type": "application/json"},
            json=body,
        )
        if r.status_code == 200:
            posted += 1
        else:
            failed += 1
            print(f"  WARN eval {case.get('id', '?')}: {r.status_code} {r.text[:200]}")
    print(f"evals uploaded: {posted}/{len(cases)} ({failed} failed)")


def trigger_curate(
    client: httpx.Client, token: str, base: str, context_id: str, force: bool = True
) -> None:
    resp = client.post(
        f"{base}/contexts/{context_id}/knowledge/curate",
        headers={**auth_headers(token), "Content-Type": "application/json"},
        json={"force": force},
    )
    resp.raise_for_status()
    print(f"curate triggered: {resp.json()}")


def trigger_build(
    client: httpx.Client,
    token: str,
    base: str,
    context_id: str,
    force: bool = False,
    eval_pass_rate_threshold: float | None = None,
    retrieval_p90_latency_ms: int | None = None,
    build_timeout_seconds: int | None = None,
) -> None:
    """Start a build run.

    Endpoint per autocontext repo `api/src/rest/handlers/context_workflows.rs`:
        POST /contexts/{slug-or-id}/code/build
        body: {
          "force": bool,
          "eval_pass_rate_threshold": float | null,    # default 1.0 server-side
          "retrieval_p90_latency_ms": int | null,
          "build_timeout_seconds": int | null,         # default 3600 server-side
        }
    Cancels any active build tasks before starting a new one.
    """
    body: dict = {"force": force}
    if eval_pass_rate_threshold is not None:
        body["eval_pass_rate_threshold"] = eval_pass_rate_threshold
    if retrieval_p90_latency_ms is not None:
        body["retrieval_p90_latency_ms"] = retrieval_p90_latency_ms
    if build_timeout_seconds is not None:
        body["build_timeout_seconds"] = build_timeout_seconds

    resp = client.post(
        f"{base}/contexts/{context_id}/code/build",
        headers={**auth_headers(token), "Content-Type": "application/json"},
        json=body,
    )
    resp.raise_for_status()
    print(f"build triggered: {resp.json()}")


def list_tasks(
    client: httpx.Client, token: str, base: str, context_id: str
) -> None:
    resp = client.get(
        f"{base}/contexts/{context_id}/tasks", headers=auth_headers(token)
    )
    resp.raise_for_status()
    tasks_data = resp.json()
    tasks = tasks_data.get("items", []) if isinstance(tasks_data, dict) else tasks_data
    for t in tasks:
        tid = t.get("id", "?")
        wf = t.get("workflow", "?")
        status = t.get("state", "?")  # Note: 'state' not 'status'
        created = (t.get("created_at", "?") or "")[:19]
        print(f"  {tid}  {wf:<10} {status:<12} {created}")


def dataset_paths(dataset: str | None = None) -> dict:
    """Resolve standard nexus-analyst-demo-ingest paths.

    Sources live under sources/<dataset>/ (with --dataset) or sources/ when no
    dataset is given. The eval set + build.md are dataset-agnostic and live
    under eval/ at the repo root.
    """
    if dataset:
        source_dir = REPO_ROOT / "sources" / dataset
    else:
        source_dir = REPO_ROOT / "sources"
    return {
        "source_dir": source_dir,
        "eval": REPO_ROOT / "eval" / "retrieval_eval_set.json",
        "build_md": REPO_ROOT / "eval" / "build.md",
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--api-base", default=None, help=f"override base (default {DEFAULT_API_BASE})")
    p.add_argument("--list-contexts", action="store_true")
    p.add_argument("--context-id", help="Nexus context UUID")
    p.add_argument(
        "--dataset",
        default="acme",
        help="Dataset name under datasets/ and output/ (default acme)",
    )
    p.add_argument(
        "--upload-path",
        default="uploads",
        help="Remote path prefix for source uploads (default 'uploads')",
    )
    p.add_argument("--upload-sources", action="store_true", help="Upload output/<dataset>/*.md")
    p.add_argument("--upload-build-md", action="store_true", help="Upload build.md")
    p.add_argument("--upload-eval", action="store_true", help="Upload retrieval_eval_set.json")
    p.add_argument("--trigger-curate", action="store_true")
    p.add_argument("--trigger-build", action="store_true")
    p.add_argument(
        "--all",
        action="store_true",
        help="Shortcut: upload sources + build.md + eval, then curate + build",
    )
    p.add_argument("--list-tasks", action="store_true")
    args = p.parse_args()

    base = api_base_url(args.api_base)

    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("ERROR: PINECONE_API_KEY not set")
        return 1

    print(f"API: {base}")

    with httpx.Client(timeout=120) as client:
        print("Authenticating...")
        token = get_token(client, api_key, base)
        print("OK")

        if args.list_contexts:
            list_contexts(client, token, base)
            return 0

        if not args.context_id:
            print("ERROR: --context-id required (or use --list-contexts)")
            return 1

        ctx = args.context_id
        paths = dataset_paths(args.dataset)

        # --all expands to the full pipeline
        if args.all:
            args.upload_sources = True
            args.upload_build_md = True
            args.upload_eval = True
            args.trigger_curate = True
            args.trigger_build = True

        if args.upload_sources:
            src = paths["source_dir"]
            if not src.is_dir():
                print(f"ERROR: {src} not found — run `python -m datasets.{args.dataset}.run` first")
                return 1
            print(f"\nUploading sources: {src} -> {args.upload_path}")
            result = upload_directory(
                client, token, base, ctx, src, args.upload_path
            )
            print(
                f"  {result['uploaded']}/{result['total']} ok, {result['failed']} failed"
            )

        if args.upload_build_md:
            md = paths["build_md"]
            if not md.is_file():
                print(f"ERROR: {md} not found")
                return 1
            print(f"\nUploading build.md: {md}")
            upload_build_md(client, token, base, ctx, md)

        if args.upload_eval:
            ev = paths["eval"]
            if not ev.is_file():
                print(f"ERROR: {ev} not found")
                return 1
            print(f"\nUploading eval: {ev}")
            upload_eval(client, token, base, ctx, ev)

        if args.trigger_curate:
            print("\nTriggering curate...")
            trigger_curate(client, token, base, ctx)

        if args.trigger_build:
            print("\nTriggering build...")
            trigger_build(client, token, base, ctx)

        if args.list_tasks:
            print("\nTasks:")
            list_tasks(client, token, base, ctx)

    return 0


if __name__ == "__main__":
    sys.exit(main())
