"""
Upload a nexus-analyst-demo-ingest source corpus into a Nexus context.

Talks to a Nexus deployment's REST API: auth, source upload, curate trigger,
task polling, source/knowledge stats. Point it at your own Nexus host via
NEXUS_API_URL or --api-base.

Usage:
  export PINECONE_API_KEY=...
  export NEXUS_API_URL=https://<your-nexus-host>/api/v0   # optional, override default

  # See available contexts (create them in the console first)
  python upload_to_nexus.py --list-contexts

  # Full one-shot: upload sources, then curate, then report stats
  python upload_to_nexus.py --context-slug nexus-analyst-acme-ecomm-v1 \
      --dataset acme-ecomm --all

  # Just upload sources/<dataset>/* (no curate) -- zips and uploads as one
  # archive above --archive-threshold files, one request per file at or below it
  python upload_to_nexus.py --context-slug <slug> --dataset acme --upload-sources

  # Force one-file-per-request even for a large corpus (the archive path
  # nests every file one directory level deeper -- see upload_archive())
  python upload_to_nexus.py --context-slug <slug> --dataset acme --upload-sources --per-file

  # Just curate (sources already uploaded)
  python upload_to_nexus.py --context-slug <slug> --trigger-curate

  # Just report current source/knowledge stats
  python upload_to_nexus.py --context-slug <slug> --report-stats

  # Preview exactly what --all would do, with no network calls at all
  python upload_to_nexus.py --context-slug <slug> --dataset acme-ecomm --all --dry-run

  # List recent tasks (import / curate / ...) for a context
  python upload_to_nexus.py --context-slug <slug> --list-tasks
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
import time
import zipfile
from pathlib import Path

import httpx

DEFAULT_API_BASE = "https://<your-nexus-host>/api/v0"
REPO_ROOT = Path(__file__).resolve().parent

# Terminal task states — once a task reaches one of these it will not
# transition further, so polling can stop.
_FINAL_STATES = {"completed", "failed", "cancelled"}

# --upload-sources zips and uploads in one request above this many files;
# --archive / --per-file override the default either way.
_ARCHIVE_DEFAULT_THRESHOLD = 5

_MIME = {
    ".md": "text/markdown",
    ".txt": "text/plain",
    ".json": "application/json",
    ".pdf": "application/pdf",
    ".csv": "text/csv",
    ".html": "text/html",
    ".ipynb": "application/x-ipynb+json",
}

_UPLOAD_EXTENSIONS: tuple[str, ...] = (".md", ".txt", ".json", ".pdf", ".csv", ".ipynb")


def collect_upload_files(
    source_dir: Path, extensions: tuple[str, ...] = _UPLOAD_EXTENSIONS
) -> list[Path]:
    return sorted(f for f in source_dir.rglob("*") if f.is_file() and f.suffix in extensions)


def resolve_archive_mode(archive: bool, per_file: bool, file_count: int) -> bool:
    """Decide archive vs. per-file upload. `archive`/`per_file` are explicit
    CLI overrides (mutually exclusive, checked by the caller); absent either,
    more than `_ARCHIVE_DEFAULT_THRESHOLD` files defaults to archive."""
    if archive:
        return True
    if per_file:
        return False
    return file_count > _ARCHIVE_DEFAULT_THRESHOLD


def api_base_url(cli_override: str | None) -> str:
    if cli_override:
        return cli_override.rstrip("/")
    return (os.getenv("NEXUS_API_URL") or DEFAULT_API_BASE).rstrip("/")


def _check(resp: httpx.Response) -> httpx.Response:
    """raise_for_status(), but print the response body first.

    httpx's default exception message is just the status code and URL; the
    server's actual error text (e.g. why a curate or upload was rejected)
    lives in the body, so surface it before raising.
    """
    if resp.status_code >= 400:
        print(f"  ERROR {resp.status_code}: {resp.text[:500]}")
    resp.raise_for_status()
    return resp


def get_token(client: httpx.Client, api_key: str, base: str) -> str:
    resp = _check(client.post(f"{base}/auth/login", json={"api_key": api_key}))
    return resp.json()["token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def list_contexts(client: httpx.Client, token: str, base: str) -> None:
    resp = _check(client.get(f"{base}/contexts", headers=auth_headers(token)))
    rows = resp.json()
    if not rows:
        print("No contexts found. Create one in the Nexus console first.")
        return
    print("slug\tid\tname")
    for context in rows:
        print(f"{context.get('slug')}\t{context.get('id')}\t{context.get('name', '?')}")


def poll_task(
    client: httpx.Client,
    token: str,
    base: str,
    task_id: str,
    label: str,
    poll_interval: float,
    timeout: float,
) -> dict:
    """Poll GET /tasks/{id} until it reaches a final state.

    Raises TimeoutError if it's still active after `timeout` seconds.
    """
    start = time.monotonic()
    last_state = None
    while True:
        task = _check(client.get(f"{base}/tasks/{task_id}", headers=auth_headers(token))).json()
        state = task.get("state")
        if state != last_state:
            print(f"    {label}: {task_id} -> {state} ({time.monotonic() - start:.0f}s)")
            last_state = state
        if state in _FINAL_STATES:
            return task
        if time.monotonic() - start > timeout:
            raise TimeoutError(f"{label}: task {task_id} still {state} after {timeout:.0f}s")
        time.sleep(poll_interval)


def upload_file(
    client: httpx.Client,
    token: str,
    base: str,
    context_slug: str,
    file_path: Path,
    upload_path: str,
) -> str | None:
    """POST one file to import/upload. Returns the import task id, or None on failure.

    One file per request: the server rejects a multipart body carrying more
    than one file field (package multiple files into an archive instead).
    """
    url = f"{base}/contexts/{context_slug}/import/upload"
    params = {"path": upload_path} if upload_path else {}
    mime = _MIME.get(file_path.suffix.lower(), "application/octet-stream")
    with open(file_path, "rb") as f:
        files = {"file": (file_path.name, f, mime)}
        resp = client.post(url, headers=auth_headers(token), params=params, files=files)
    if resp.status_code == 200:
        return resp.json().get("task_id")
    print(f"  WARN: {file_path.name} -> {resp.status_code}: {resp.text[:200]}")
    return None


def upload_directory(
    client: httpx.Client,
    token: str,
    base: str,
    context_slug: str,
    source_dir: Path,
    upload_path: str,
    poll_interval: float,
    task_timeout: float,
    extensions: tuple[str, ...] = _UPLOAD_EXTENSIONS,
) -> dict:
    """Upload every file under `source_dir`, preserving its relative subdirectories.

    A context allows only one import task in flight at a time (a second
    upload 409s while the first is still importing), so each file's task is
    polled to a final state before the next file is sent — uploads are
    sequential, not parallel, regardless of file count.
    """
    files = collect_upload_files(source_dir, extensions)
    print(f"Found {len(files)} files in {source_dir}")
    uploaded = 0
    failed = 0
    for i, fpath in enumerate(files):
        rel = fpath.relative_to(source_dir)
        target = (
            f"{upload_path}/{rel.parent}" if str(rel.parent) != "." else upload_path
        )
        print(f"  [{i + 1}/{len(files)}] {rel} -> {target}")
        task_id = upload_file(client, token, base, context_slug, fpath, target)
        if not task_id:
            failed += 1
            continue
        try:
            task = poll_task(
                client, token, base, task_id, rel.name, poll_interval, task_timeout
            )
        except TimeoutError as e:
            print(f"  WARN: {e}")
            failed += 1
            continue
        if task.get("state") == "completed":
            uploaded += 1
        else:
            failed += 1
            print(
                f"  WARN: {rel} import ended in state={task.get('state')}: {task.get('error')}"
            )
    return {"total": len(files), "uploaded": uploaded, "failed": failed}


def build_archive(files: list[Path], source_dir: Path, dest: Path) -> None:
    """Zip `files` (all under source_dir) into `dest`, each entry named for
    its path relative to source_dir, so the extracted tree reproduces
    source_dir's own subdirectory layout."""
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for fpath in files:
            zf.write(fpath, arcname=fpath.relative_to(source_dir).as_posix())


def upload_archive(
    client: httpx.Client,
    token: str,
    base: str,
    context_slug: str,
    archive_path: Path,
    archive_filename: str,
    upload_path: str,
) -> str | None:
    """POST one archive to import/upload. Returns the import task id, or None on failure."""
    url = f"{base}/contexts/{context_slug}/import/upload"
    params = {"path": upload_path} if upload_path else {}
    with open(archive_path, "rb") as f:
        files = {"file": (archive_filename, f, "application/zip")}
        resp = client.post(url, headers=auth_headers(token), params=params, files=files)
    if resp.status_code == 200:
        return resp.json().get("task_id")
    print(f"  WARN: {archive_filename} -> {resp.status_code}: {resp.text[:200]}")
    return None


def upload_directory_as_archive(
    client: httpx.Client,
    token: str,
    base: str,
    context_slug: str,
    source_dir: Path,
    upload_path: str,
    archive_name: str,
    poll_interval: float,
    task_timeout: float,
    extensions: tuple[str, ...] = _UPLOAD_EXTENSIONS,
) -> dict:
    """Zip every file under `source_dir` and upload it as a single archive.

    One request, one import task, regardless of file count -- the server
    allows only one import in flight per context, so this is the fast path
    for a multi-file corpus (see upload_file()'s docstring for why per-file
    uploads are forced sequential).

    The import runtime nests every extracted entry one directory level
    deeper than the same file uploaded individually would land: it always
    extracts an archive under a subdirectory named for the archive's own
    basename (minus extension), to disambiguate repeat uploads that might
    collide. So a file at "<source_dir>/dbt/x.md", archived as
    "<archive_name>.zip" and uploaded with path="uploads", lands at
    "uploads/<archive_name>/dbt/x.md" -- not "uploads/dbt/x.md" the way
    --per-file would place it. This is the import runtime's own behavior,
    not something this client can suppress; `archive_name` at least makes
    the extra segment predictable instead of a bare "upload/".
    """
    files = collect_upload_files(source_dir, extensions)
    print(f"Found {len(files)} files in {source_dir}")
    archive_filename = f"{archive_name}.zip"
    with tempfile.TemporaryDirectory(prefix="nexus-upload-") as tmp_dir:
        archive_path = Path(tmp_dir) / archive_filename
        build_archive(files, source_dir, archive_path)
        size = archive_path.stat().st_size
        print(f"  packaged {len(files)} file(s) into {archive_filename} ({size:,} bytes)")
        task_id = upload_archive(
            client, token, base, context_slug, archive_path, archive_filename, upload_path
        )

    if not task_id:
        return {"total": len(files), "uploaded": 0, "failed": len(files)}
    task = poll_task(client, token, base, task_id, archive_filename, poll_interval, task_timeout)

    output = task.get("output") or {}
    imported = output.get("imported_items", 0)
    out_files = output.get("output_files", 0)
    skipped = output.get("skipped", 0)
    print(
        f"  import {task.get('state')}: {imported} item(s) imported -> {out_files} output "
        f"file(s), {skipped} skipped"
    )
    for item in (output.get("skipped_items") or [])[:10]:
        print(f"    skipped: {item.get('src')} ({item.get('reason')})")
    if task.get("state") != "completed":
        print(f"  ERROR: import did not complete: {task.get('error')}")
        return {"total": len(files), "uploaded": 0, "failed": len(files)}
    nested = f"{upload_path}/{archive_name}" if upload_path else archive_name
    print(f"  landed under {nested}/ -- one directory level deeper than --per-file's {upload_path or '.'}/<relative>")
    return {"total": len(files), "uploaded": imported, "failed": skipped}


def trigger_curate(
    client: httpx.Client, token: str, base: str, context_slug: str, force: bool = True
) -> str:
    """POST /curate. Returns the curate task id.

    Note for future callers: a manifest update (PUT on the context) already
    force-triggers a re-curate when the curate-relevant part of the manifest
    changed. Calling this right after such an update pays for curation twice.
    """
    resp = _check(
        client.post(
            f"{base}/contexts/{context_slug}/curate",
            headers={**auth_headers(token), "Content-Type": "application/json"},
            json={"force": force},
        )
    )
    return resp.json()["task_id"]


def curate_and_wait(
    client: httpx.Client,
    token: str,
    base: str,
    context_slug: str,
    poll_interval: float,
    task_timeout: float,
) -> bool:
    """Trigger curate, poll to a final state, and report runtime + token spend.

    Returns True iff the curate task completed successfully. There is no
    dollar `cost` field on the task record — tokens_prompt/tokens_completion
    are the actual stored numbers closest to "cost"; a $ estimate would
    require porting the console's client-side price table, which is itself
    labeled an approximation, so it isn't reproduced here.
    """
    task_id = trigger_curate(client, token, base, context_slug)
    print(f"  curate task: {task_id}")
    task = poll_task(client, token, base, task_id, "curate", poll_interval, task_timeout)
    tokens_prompt = task.get("tokens_prompt", 0)
    tokens_completion = task.get("tokens_completion", 0)
    print(
        f"  curate {task.get('state')}: runtime={task.get('runtime_seconds')}s "
        f"tokens_prompt={tokens_prompt} tokens_completion={tokens_completion} "
        f"tokens_total={tokens_prompt + tokens_completion}"
    )
    if task.get("state") != "completed":
        print(f"  ERROR: curate did not complete: {task.get('error')}")
        return False
    return True


def report_stats(client: httpx.Client, token: str, base: str, context_slug: str) -> None:
    s = _check(
        client.get(f"{base}/contexts/{context_slug}/source/stats", headers=auth_headers(token))
    ).json()
    print(
        f"\nSource stats: {s['file_count']} files, {s['dir_count']} dirs, "
        f"{s['total_size']:,} bytes"
    )
    if "max_files_per_context" in s:
        print(
            f"  preview quota: {s['used_files']}/{s['max_files_per_context']} files, "
            f"{s['used_bytes']:,}/{s['max_bytes_per_context']:,} bytes "
            f"(includes retained _inbox originals, not just published source)"
        )

    k = _check(
        client.get(f"{base}/contexts/{context_slug}/knowledge/stats", headers=auth_headers(token))
    ).json()
    print(
        f"Knowledge stats: {k['file_count']} files, {k['dir_count']} dirs, "
        f"{k['total_size']:,} bytes"
    )
    print(
        "  note: sqlite-format curate artifacts store their rows in one shared "
        "_context.vN.sqlite catalog file, not as individual knowledge files -- "
        "file_count undercounts actual knowledge volume for a sqlite-heavy manifest."
    )


def list_tasks(client: httpx.Client, token: str, base: str, context_slug: str) -> None:
    resp = _check(
        client.get(f"{base}/tasks", headers=auth_headers(token), params={"context": context_slug})
    )
    tasks_data = resp.json()
    tasks = tasks_data.get("items", []) if isinstance(tasks_data, dict) else tasks_data
    for t in tasks:
        tid = t.get("id", "?")
        wf = t.get("workflow", "?")
        status = t.get("state", "?")
        created = (t.get("created_at", "?") or "")[:19]
        print(f"  {tid}  {wf:<10} {status:<12} {created}")


def source_dir_for(dataset: str | None) -> Path:
    """Resolve the sources/<dataset>/ dir (or sources/ when no dataset is given)."""
    return REPO_ROOT / "sources" / dataset if dataset else REPO_ROOT / "sources"


def dry_run_upload(
    source_dir: Path,
    upload_path: str,
    archive_name: str | None = None,
    extensions: tuple[str, ...] = _UPLOAD_EXTENSIONS,
) -> None:
    """Print the file -> destination-path mapping that a real run would produce.

    `archive_name`, when given, previews archive mode's extra nesting
    (see upload_directory_as_archive()'s docstring) so the quirk shows up
    before any upload happens, not after.
    """
    if not source_dir.is_dir():
        print(f"  WARN: {source_dir} not found")
        return
    files = collect_upload_files(source_dir, extensions)
    base_path = f"{upload_path}/{archive_name}" if archive_name else upload_path
    total_bytes = 0
    for fpath in files:
        rel = fpath.relative_to(source_dir)
        target = f"{base_path}/{rel.parent}" if str(rel.parent) != "." else base_path
        size = fpath.stat().st_size
        total_bytes += size
        print(f"  {rel} ({size:,} bytes) -> path={target}")
    print(f"  {len(files)} files, {total_bytes:,} bytes total")


def dry_run(args: argparse.Namespace, base: str) -> int:
    print("DRY RUN -- no network calls will be made\n")

    if args.list_contexts:
        print(f"would GET  {base}/contexts")
        return 0

    if not args.context_slug:
        print("ERROR: --context-slug required (or use --list-contexts)")
        return 1

    ctx = args.context_slug
    print(f"would POST {base}/auth/login")
    print(f"context slug: {ctx}\n")

    actions = (args.upload_sources, args.trigger_curate, args.report_stats, args.list_tasks)

    if args.upload_sources:
        source_dir = source_dir_for(args.dataset)
        file_count = len(collect_upload_files(source_dir)) if source_dir.is_dir() else 0
        use_archive = resolve_archive_mode(args.archive, args.per_file, file_count)
        mode = "archive" if use_archive else "per-file"
        print(f"would upload sources from {source_dir} (dataset={args.dataset!r}, {mode} mode):")
        archive_name = source_dir.name if use_archive else None
        dry_run_upload(source_dir, args.upload_path, archive_name)
        if use_archive:
            print(
                f"  would POST {base}/contexts/{ctx}/import/upload?path={args.upload_path} "
                f"(one request, {archive_name}.zip), then GET {base}/tasks/{{id}} polled to a final state"
            )
        else:
            print(
                f"  each file: POST {base}/contexts/{ctx}/import/upload?path=<target>, "
                f"then GET {base}/tasks/{{id}} polled to a final state before the next file"
            )
        print()

    if args.trigger_curate:
        print(f"would POST {base}/contexts/{ctx}/curate")
        print(f"  then poll GET {base}/tasks/{{id}} to a final state\n")

    if args.report_stats:
        print(f"would GET  {base}/contexts/{ctx}/source/stats")
        print(f"would GET  {base}/contexts/{ctx}/knowledge/stats\n")

    if args.list_tasks:
        print(f"would GET  {base}/tasks?context={ctx}\n")

    if not any(actions):
        print("(no action flags set -- pass --upload-sources / --trigger-curate / --report-stats / --all)")

    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--api-base", default=None, help=f"override base (default {DEFAULT_API_BASE})")
    p.add_argument("--list-contexts", action="store_true")
    p.add_argument("--context-slug", help="Nexus context slug (a UUID also works)")
    p.add_argument(
        "--dataset",
        default="acme",
        help="Dataset name under sources/ (default acme)",
    )
    p.add_argument(
        "--upload-path",
        default="uploads",
        help="Remote path prefix for source uploads (default 'uploads')",
    )
    p.add_argument("--upload-sources", action="store_true", help="Upload sources/<dataset>/*")
    p.add_argument(
        "--archive",
        action="store_true",
        help=f"Zip sources/<dataset>/* and upload as one archive (default above "
        f"{_ARCHIVE_DEFAULT_THRESHOLD} files; nests one directory level deeper, see README)",
    )
    p.add_argument(
        "--per-file",
        action="store_true",
        help=f"Upload one file per request, polling each to completion before the next "
        f"(default at or below {_ARCHIVE_DEFAULT_THRESHOLD} files)",
    )
    p.add_argument("--trigger-curate", action="store_true")
    p.add_argument("--report-stats", action="store_true", help="Report source + knowledge stats")
    p.add_argument(
        "--all",
        action="store_true",
        help="Shortcut: upload sources, then curate, then report stats",
    )
    p.add_argument("--list-tasks", action="store_true")
    p.add_argument(
        "--poll-interval",
        type=float,
        default=3.0,
        help="Seconds between task-status polls (default 3.0)",
    )
    p.add_argument(
        "--task-timeout",
        type=float,
        default=3600.0,
        help="Max seconds to wait for any one task (import or curate) to finish (default 3600)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be uploaded/curated/reported and which endpoints "
        "would be hit, without making any network calls",
    )
    args = p.parse_args()

    if args.archive and args.per_file:
        print("ERROR: --archive and --per-file are mutually exclusive")
        return 1

    if args.all:
        args.upload_sources = True
        args.trigger_curate = True
        args.report_stats = True

    base = api_base_url(args.api_base)
    print(f"API: {base}")

    if args.dry_run:
        return dry_run(args, base)

    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        print("ERROR: PINECONE_API_KEY not set")
        return 1

    with httpx.Client(timeout=120) as client:
        print("Authenticating...")
        token = get_token(client, api_key, base)
        print("OK")

        if args.list_contexts:
            list_contexts(client, token, base)
            return 0

        if not args.context_slug:
            print("ERROR: --context-slug required (or use --list-contexts)")
            return 1

        ctx = args.context_slug
        ok = True

        if args.upload_sources:
            source_dir = source_dir_for(args.dataset)
            if not source_dir.is_dir():
                print(f"ERROR: {source_dir} not found")
                return 1
            file_count = len(collect_upload_files(source_dir))
            use_archive = resolve_archive_mode(args.archive, args.per_file, file_count)
            mode = "archive" if use_archive else "per-file"
            print(f"\nUploading sources: {source_dir} -> {args.upload_path} ({mode} mode)")
            if use_archive:
                result = upload_directory_as_archive(
                    client,
                    token,
                    base,
                    ctx,
                    source_dir,
                    args.upload_path,
                    source_dir.name,
                    args.poll_interval,
                    args.task_timeout,
                )
            else:
                result = upload_directory(
                    client,
                    token,
                    base,
                    ctx,
                    source_dir,
                    args.upload_path,
                    args.poll_interval,
                    args.task_timeout,
                )
            print(f"  {result['uploaded']}/{result['total']} ok, {result['failed']} failed")
            if result["failed"]:
                ok = False

        if args.trigger_curate:
            print("\nCurating...")
            if not curate_and_wait(
                client, token, base, ctx, args.poll_interval, args.task_timeout
            ):
                ok = False

        if args.report_stats:
            report_stats(client, token, base, ctx)

        if args.list_tasks:
            print("\nTasks:")
            list_tasks(client, token, base, ctx)

        if not any(
            (args.upload_sources, args.trigger_curate, args.report_stats, args.list_tasks)
        ):
            print("(no action flags set -- pass --upload-sources / --trigger-curate / --report-stats / --all)")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
