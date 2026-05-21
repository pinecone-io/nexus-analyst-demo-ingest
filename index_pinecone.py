"""
Chunk + index source markdown to Pinecone for the classic baseline agent.

Reads `output/<dataset>/*.md` (YAML frontmatter + markdown body), chunks by
heading, and upserts to a Pinecone index. Each chunk carries `adapter`,
`dataset`, `source_file`, and `license` metadata so the classic agent's
search tools can filter by source type.

The classic agent in `nexus-analyst-demo/agent-classic/` issues separate
tool calls per adapter (`search_schema`, `search_docs`, `search_notebooks`),
each filtering on the corresponding adapter value.

The index must already exist (create with the Pinecone CLI):

    pc index create -n nexus-analyst-classic -m cosine -c aws -r us-east-1 \\
        --model llama-text-embed-v2 --field_map text=content

Usage:
    PINECONE_API_KEY=pcsk_... python index_pinecone.py \\
        --dataset acme --namespace acme
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import yaml
from pinecone import Pinecone

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_INDEX = "nexus-analyst-classic"
DEFAULT_NAMESPACE = "combined_demo"
BATCH_SIZE = 96
TARGET_CHARS = 8000  # ~2000 tokens soft cap per chunk — matches llama-text-embed-v2 input ceiling

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class Chunk:
    _id: str
    text: str
    adapter: str
    dataset: str
    source_file: str
    license: str
    title: str
    section: str


def parse_md(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, text[m.end():]


def chunk_by_heading(body: str, target_chars: int = TARGET_CHARS) -> list[tuple[str, str]]:
    """Split on `## ` headings, then further split oversized sections by paragraph."""
    parts = re.split(r"(?m)^## (.+)$", body)
    sections: list[tuple[str, str]] = []
    if len(parts) == 1:
        sections.append(("", parts[0].strip()))
    else:
        preamble = parts[0].strip()
        if preamble:
            sections.append(("", preamble))
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""
            sections.append((title, content))

    out: list[tuple[str, str]] = []
    for title, content in sections:
        if not content:
            continue
        if len(content) <= target_chars:
            out.append((title, content))
            continue
        cur = ""
        for paragraph in content.split("\n\n"):
            if len(cur) + len(paragraph) + 2 > target_chars and cur:
                out.append((title, cur.strip()))
                cur = paragraph
            else:
                cur = (cur + "\n\n" + paragraph) if cur else paragraph
        if cur.strip():
            out.append((title, cur.strip()))
    return out


def slugify(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", s).strip("-").lower()[:48]


def build_chunks(dataset: str, output_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(output_dir.glob("*.md")):
        fm, body = parse_md(path)
        if not body.strip():
            continue
        adapter = str(fm.get("adapter", "unknown"))
        title = str(fm.get("title", path.stem))
        license_ = str(fm.get("license", ""))
        for i, (section, content) in enumerate(chunk_by_heading(body)):
            chunks.append(Chunk(
                _id=f"{dataset}__{slugify(path.stem)}__{i:03d}",
                text=content,
                adapter=adapter,
                dataset=dataset,
                source_file=path.name,
                license=license_,
                title=title,
                section=section or "(intro)",
            ))
    return chunks


def upsert_chunks(index, namespace: str, chunks: list[Chunk]) -> None:
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = [asdict(c) for c in chunks[i:i + BATCH_SIZE]]
        index.upsert_records(namespace, batch)
        print(f"  upserted {i + len(batch)}/{len(chunks)}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", action="append", default=[], required=True,
                    help="Dataset name; can be repeated. Reads from output/<dataset>/*.md")
    ap.add_argument("--namespace", default=DEFAULT_NAMESPACE)
    ap.add_argument("--index", default=DEFAULT_INDEX)
    ap.add_argument("--dry-run", action="store_true",
                    help="Print sample chunks and totals without upserting")
    args = ap.parse_args()

    api_key = os.environ.get("PINECONE_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: PINECONE_API_KEY not set", file=sys.stderr)
        return 1

    all_chunks: list[Chunk] = []
    for ds in args.dataset:
        out_dir = REPO_ROOT / "sources" / ds
        if not out_dir.is_dir():
            print(f"ERROR: {out_dir} not found", file=sys.stderr)
            return 1
        ds_chunks = build_chunks(ds, out_dir)
        n_files = len(list(out_dir.glob("*.md")))
        print(f"[{ds}] {len(ds_chunks)} chunks from {n_files} files", file=sys.stderr)
        all_chunks.extend(ds_chunks)

    if args.dry_run:
        for c in all_chunks[:3]:
            print(f"\n--- {c._id} ({c.adapter}, section={c.section!r})")
            print(c.text[:240])
        print(f"\nTotal chunks: {len(all_chunks)}")
        return 0

    pc = Pinecone(api_key=api_key)
    if not pc.has_index(args.index):
        print(
            f"ERROR: index '{args.index}' does not exist. Create it first:\n"
            f"  pc index create -n {args.index} -m cosine -c aws -r us-east-1 \\\n"
            f"      --model llama-text-embed-v2 --field_map text=content",
            file=sys.stderr,
        )
        return 1
    index = pc.Index(args.index)
    upsert_chunks(index, args.namespace, all_chunks)
    print(f"Done. {len(all_chunks)} chunks → {args.index}/{args.namespace}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
