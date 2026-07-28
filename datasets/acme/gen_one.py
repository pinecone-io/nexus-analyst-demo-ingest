"""Generate one source file via Gemini. Args: output_path adapter topic focus"""
import sys, os
from pathlib import Path
from google import genai

CANON = (Path(__file__).parent / "CANON.md").read_text()
MODEL = os.environ.get("GEN_MODEL", "gemini-3.5-flash-lite")
PROJECT = os.environ.get("VERTEX_PROJECT_ID", "mission-control-350520")

def gen(out_path, adapter, topic, focus):
    client = genai.Client(vertexai=True, project=PROJECT, location="global")
    prompt = f"""Generate the following internal document for Acme Inc (a fictitious B2B SaaS).

DOCUMENT: {topic}
OUTPUT FORMAT: Start with YAML frontmatter, then the full document body.

---
title: "{topic}"
source_url: "internal://acme/{Path(out_path).stem.replace('bulk__','')}"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: {adapter}
---

INSTRUCTIONS:
{focus}

CANONICAL FACTS (never contradict):
{CANON}

Generate the FULL document. Be extremely verbose. Target 300KB+. Do not truncate."""

    system = """You generate synthetic internal documents for Acme Inc (fictitious B2B SaaS).
Rules: use ONLY canon facts/people/customers. Heavy noise is good. Natural messy human voice.
Correct BigQuery paths: `nexus-analyst-demo.acme.<table>` (FLAT, no nested marts). Dates 2025-2026."""

    r = client.models.generate_content(
        model=MODEL, contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=1.0, max_output_tokens=65536, system_instruction=system))
    text = r.text or ""
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    size = len(text.encode("utf-8"))
    print(f"{size//1024}KB  {len(text.splitlines())} lines  {p}")
    return size

if __name__ == "__main__":
    gen(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
