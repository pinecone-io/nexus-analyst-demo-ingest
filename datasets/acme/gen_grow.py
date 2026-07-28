"""Grow an existing source file by appending more LLM-generated content.
Usage: python gen_grow.py <file_path> <continuation_prompt> [target_kb]
"""
import os
import sys
from pathlib import Path
from google import genai

CANON = (Path(__file__).parent / "CANON.md").read_text()
MODEL = os.environ.get("GEN_MODEL", "gemini-3.5-flash-lite")
PROJECT = os.environ.get("VERTEX_PROJECT_ID", "mission-control-350520")

def grow(path, prompt, target_kb=300):
    client = genai.Client(vertexai=True, project=PROJECT, location="global")
    p = Path(path)
    current = p.read_text(encoding="utf-8")
    current_kb = len(current.encode("utf-8")) // 1024

    # Take last 2000 chars as context for continuation
    tail = current[-2000:] if len(current) > 2000 else current

    full_prompt = f"""You are CONTINUING an existing internal document for Acme Inc (fictitious B2B SaaS).

Here is the END of the document so far (last ~2000 chars):
---
{tail}
---

CONTINUE generating MORE content in the SAME format and voice. Do NOT repeat the frontmatter or title. Just continue with new entries/threads/queries/records that haven't been covered yet.

{prompt}

CANONICAL FACTS (never contradict):
{CANON}

Generate as much content as possible. Fill the entire output window. Do NOT summarize or truncate. Keep going with new varied entries."""

    system = """You are continuing a synthetic internal document for Acme Inc (fictitious B2B SaaS).
Match the existing format exactly. Use ONLY canon facts/people/customers. Heavy noise is good.
Natural messy human voice. Correct BigQuery paths: nexus-analyst-demo.acme.<table> (FLAT). Dates 2025-2026.
Do NOT add frontmatter, titles, or meta-commentary. Just continue the content."""

    passes = 0
    while current_kb < target_kb:
        passes += 1
        r = client.models.generate_content(
            model=MODEL, contents=full_prompt,
            config=genai.types.GenerateContentConfig(
                temperature=1.0, max_output_tokens=65536, system_instruction=system))
        new_text = r.text or ""
        if not new_text.strip():
            print(f"  pass {passes}: empty response, stopping")
            break
        with open(p, "a", encoding="utf-8") as f:
            f.write("\n\n" + new_text)
        current = p.read_text(encoding="utf-8")
        current_kb = len(current.encode("utf-8")) // 1024
        print(f"  pass {passes}: +{len(new_text)//1024}KB → {current_kb}KB total", flush=True)
        # Update tail for next pass
        tail = current[-2000:]
        full_prompt = f"""Continue the document. Last ~2000 chars:
---
{tail}
---
{prompt}
CANONICAL FACTS: {CANON[:3000]}...
Generate MORE varied entries. Fill the output window."""

    print(f"  DONE: {current_kb}KB, {passes} passes, {len(current.splitlines())} lines")
    return current_kb

if __name__ == "__main__":
    grow(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 300)
