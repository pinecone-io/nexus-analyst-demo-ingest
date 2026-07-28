"""
Append-loop that grows acme-ecomm's `bulk: True` source files up toward their
realistic target KB size.

gen_rounds.py generates one document per spec in a single LLM call. That's
correct for the ~80 discrete specs (a ticket/PRD/readout genuinely IS
8-21KB), but the 9 specs marked `"bulk": True` state an explicit 80-300KB
target in their `focus` text that a single call cannot fill -- they come out
at whatever one pass naturally produces (observed: 12-56KB) and need
repeated continuation passes to reach size. This script is that loop: read
the file's tail, generate more of the same content, append, repeat until its
target is met -- never rewriting what's already there.

Discovery, not hardcoding: the bulk specs, their paths, and their KB targets
are pulled directly out of gen_rounds.py's own ROUNDS table via
`ast.literal_eval` on that single module-level assignment (also grabs
SYSTEMS, for the same reason). gen_rounds.py itself is deliberately NEVER
imported -- importing it eagerly requires google-genai AND reads CANON.md as
an import-time side effect (see its own docstring), neither of which this
script needs just to read a static spec table. `ast.parse`-ing it is a pure
syntax operation with no such side effects.

LEDGER.jsonl reuse: `load_ledger` / `filter_ledger` / `render_ledger` below
are kept intentionally byte-for-byte identical to gen_rounds.py's own
functions of the same name (same rule: events at or before a round's as-of
date, chronological, ISO-string sort). Duplicated rather than imported for
the same reason ROUNDS is AST-parsed instead of imported. A continuation for
a file assigned to round X sees exactly the ledger snapshot the original
generation pass for round X would have seen -- no more, no less.

Reference precedent: datasets/acme/gen_grow.py does the same append-loop for
the sibling B2B SaaS corpus (fixed file, fixed CANON.md, no rounds/ledger
concept). This script follows its shape (tail-for-continuity, append not
rewrite, temperature 1.0, same model/pricing) with four deliberate
differences, called out rather than silently copied:
  1. The sibling's later passes truncate CANON to `CANON[:3000]` chars to
     save tokens. acme-ecomm's CANON.md is ~72KB (vs the sibling's ~12KB) --
     3000 chars would drop nearly all of it (the numbers tables, SIGNALS,
     cast lists). Input tokens are the cheap side of pricing (0.3 vs 2.5 per
     1M); this script feeds CANON_TEXT in full on every pass, always.
  2. This script also tracks, per file, which CANON SIGNALS already look
     present in the existing content (a best-effort fingerprint scan of
     dollar figures / percentages / backticked identifiers / experiment IDs
     drawn from each signal's own CANON text) and tells the model not to
     restate them -- the sibling's growth loop has no signal-repetition
     concern to guard against in the first place (single-doc, no rounds).
  3. Continuations must not extend past their round's as-of date (same
     rule the original generation obeyed) -- if the existing content's own
     timeline already reaches that boundary, the prompt asks for MORE
     density inside the already-covered window rather than pushing past it.
  4. Live smoke-testing (see the return report) caught the model doing
     exactly the two things #2/#3 guard against anyway, a few passes in:
     drifting a date past the round boundary (a Slack-archive continuation
     pulls hard toward "the next thing is tomorrow"), and once, echoing a
     second YAML frontmatter block mid-document. Instruction alone didn't
     fully prevent either, so grow_file() also detects both after the fact
     (find_dates_past_boundary / has_frontmatter_leak) and retries the same
     pass once before accepting it with a loud, unmissable warning -- never
     silently truncating (a mid-generation cut risks being worse than the
     violation itself). The sibling's single-shot loop has no such check
     because it never revisits an already-settled timeline.

Usage (matches gen_rounds.py's own uv invocation convention -- this repo's
.venv deliberately does NOT carry google-genai as a project dependency; see
pyproject.toml, and gen_rounds.py's module docstring):
  uv run --no-project --with google-genai python datasets/acme-ecomm/grow_bulk.py --dry-run --all
  uv run --no-project --with google-genai python datasets/acme-ecomm/grow_bulk.py --all
  uv run --no-project --with google-genai python datasets/acme-ecomm/grow_bulk.py --file query_logs/bulk__q1fy27-bq-audit-log.md
  uv run --no-project --with google-genai python datasets/acme-ecomm/grow_bulk.py --all --max-appends 2 --target-kb 40

`--dry-run` makes zero API calls and needs no google-genai install at all
(the import is deferred into make_client()/grow_file()) -- it only reads
gen_rounds.py, CANON.md, LEDGER.jsonl, and the existing source files.
"""
import argparse
import ast
import calendar
import json
import os
import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

DATASET_DIR = Path(__file__).parent
REPO = Path(__file__).resolve().parents[2]
SOURCES_DIR = REPO / "sources" / "acme-ecomm"

GEN_ROUNDS_PATH = DATASET_DIR / "gen_rounds.py"
CANON_PATH = DATASET_DIR / "CANON.md"
LEDGER_PATH = DATASET_DIR / "LEDGER.jsonl"

MODEL = os.environ.get("GEN_MODEL", "gemini-3.5-flash-lite")
PROJECT = os.environ.get("VERTEX_PROJECT_ID", "mission-control-350520")
LOCATION = "global"
TEMPERATURE = 1.0
MAX_OUTPUT_TOKENS = 65536

# Published gemini-3.5-flash-lite rate (same as gen_rounds.py).
PRICE_IN_PER_1M_USD = 0.30
PRICE_OUT_PER_1M_USD = 2.50

TAIL_CHARS = 2000  # continuity window, matches datasets/acme/gen_grow.py's convention
DEFAULT_MAX_APPENDS = 30  # safety stop per file; the 200-300KB file needs the most passes

# Eager read, matching gen_rounds.py / datasets/acme/{gen_docs,gen_one,gen_grow}.py convention.
CANON_TEXT = CANON_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Absolute date ceiling -- parsed from CANON's own "Today" snapshot rather
# than hardcoded a second time, so this can never drift out of sync with the
# canon file (see discover_bulk_specs' boundary_date: no per-file boundary,
# however a document's own span or round is computed, may ever exceed this).
# ---------------------------------------------------------------------------
_CANON_TODAY_RE = re.compile(r'"Today"\s*snapshot\*\*:\s*\w+,\s*\*\*(\d{4}-\d{2}-\d{2})\*\*')


def _parse_canon_today(canon_text: str) -> str:
    m = _CANON_TODAY_RE.search(canon_text)
    if not m:
        raise RuntimeError(
            "CANON.md's '\"Today\" snapshot' line not found or reformatted -- "
            "update _CANON_TODAY_RE to match. This is the absolute date ceiling "
            "for every bulk-file boundary computation and must not silently fall back."
        )
    return m.group(1)


ABSOLUTE_CEILING_DATE = _parse_canon_today(CANON_TEXT)


# ---------------------------------------------------------------------------
# Pull ROUNDS + SYSTEMS out of gen_rounds.py's AST -- see module docstring
# for why this doesn't just `import gen_rounds`.
# ---------------------------------------------------------------------------
def _extract_module_literals(path: Path, names: tuple[str, ...]) -> dict:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in names:
                    found[t.id] = ast.literal_eval(node.value)
    missing = set(names) - found.keys()
    if missing:
        raise RuntimeError(
            f"{path} no longer defines module-level {sorted(missing)!r} -- "
            f"update grow_bulk.py's discovery logic to match"
        )
    return found


_GEN_ROUNDS_LITERALS = _extract_module_literals(GEN_ROUNDS_PATH, ("ROUNDS", "SYSTEMS"))
ROUNDS: list[dict] = _GEN_ROUNDS_LITERALS["ROUNDS"]
SYSTEMS: dict[str, str] = _GEN_ROUNDS_LITERALS["SYSTEMS"]


# ---------------------------------------------------------------------------
# Bulk spec discovery
# ---------------------------------------------------------------------------
_TARGET_RE = re.compile(r"target\s+(\d+)\s*-\s*(\d+)\s*KB", re.IGNORECASE)


def _parse_target_kb(focus_text: str) -> tuple[int, int] | None:
    m = _TARGET_RE.search(focus_text)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


# A handful of bulk specs deliberately span MORE than their containing round
# (e.g. a spec filed under round "q1fy26" -- as-of 2025-04-15 -- whose own
# title says its content runs "(2025-02 through 2025-07)", i.e. through
# Q2FY26). Validating those against the round's as-of date alone flags every
# legitimate date in the back half of the document as a violation. Where a
# document states its own "(YYYY-MM[-DD] through YYYY-MM[-DD])" span, that IS
# the real boundary; the round's as-of date is only a fallback for specs that
# don't declare one (most of them -- for those, round date and true boundary
# coincide by construction).
_SPAN_RE = re.compile(r"\((\d{4}-\d{2}(?:-\d{2})?)\s+through\s+(\d{4}-\d{2}(?:-\d{2})?)\)")


def _parse_declared_span_end(*texts: str) -> str | None:
    """Search title/topic (then focus, as a fallback source -- see module
    docstring) for a clean '(YYYY-MM[-DD] through YYYY-MM[-DD])' span and
    return its END, expanded to that month's last day when given as YYYY-MM.
    Messier phrasing ("late Jan 2026", a bare year range) intentionally
    doesn't match -- those specs fall back to the round's as-of date, which
    is safe because none of them currently have content past it."""
    for text in texts:
        m = _SPAN_RE.search(text)
        if not m:
            continue
        end = m.group(2)
        if len(end) == 7:  # YYYY-MM only -- expand to that month's last day
            y, mo = int(end[:4]), int(end[5:7])
            end = f"{y:04d}-{mo:02d}-{calendar.monthrange(y, mo)[1]:02d}"
        return end
    return None


@dataclass
class BulkSpec:
    path: str
    system: str
    adapter: str
    topic: str
    focus: str
    round_name: str
    round_date: str
    target_low_kb: int | None
    target_high_kb: int | None
    boundary_date: str  # the REAL date ceiling for this doc -- see _parse_declared_span_end


def discover_bulk_specs() -> list[BulkSpec]:
    """Every spec with `"bulk": True` in gen_rounds.py's ROUNDS table, in
    round order. Each spec inherits its containing round's name/date -- that
    IS the "round-appropriate" as-of date for its ledger snapshot, same as
    gen_rounds.py's own run_round() uses `round_meta["date"]` for every spec
    in that round regardless of the spec's own content window."""
    specs = []
    for round_ in ROUNDS:
        for spec in round_.get("specs", []):
            if not spec.get("bulk"):
                continue
            parsed = _parse_target_kb(spec.get("focus", ""))
            low, high = parsed if parsed else (None, None)
            span_end = _parse_declared_span_end(spec.get("topic", ""), spec.get("focus", ""))
            boundary_date = min(span_end or round_["date"], ABSOLUTE_CEILING_DATE)
            specs.append(
                BulkSpec(
                    path=spec["path"],
                    system=spec["system"],
                    adapter=spec.get("adapter", ""),
                    topic=spec.get("topic", ""),
                    focus=spec.get("focus", ""),
                    round_name=round_["name"],
                    round_date=round_["date"],
                    target_low_kb=low,
                    target_high_kb=high,
                    boundary_date=boundary_date,
                )
            )
    return specs


# ---------------------------------------------------------------------------
# CANON SIGNALS -- parsed once, used for the "don't restate an already-buried
# signal" heuristic. CANON.md's SIGNALS section uses one consistent bullet
# shape: `- **[tag-name]** rest of the bullet text...`, verified against the
# live file (23 signals as of this writing).
# ---------------------------------------------------------------------------
_SIGNALS_SECTION_RE = re.compile(r"^## SIGNALS\b.*?\n(.*?)\n---", re.DOTALL | re.MULTILINE)
_SIGNAL_BULLET_RE = re.compile(r"\*\*\[([a-z0-9-]+)\]\*\*\s*(.+?)(?=\n- \*\*\[|\Z)", re.DOTALL)

# Fingerprints auto-derived from each signal's OWN CANON text -- dollar
# figures, signed percentages, backticked identifiers, experiment IDs, and
# comma-grouped counts. Not hand-curated per tag (so it survives CANON.md
# edits); a best-effort scan, not a guarantee -- see module docstring point 2.
_FINGERPRINT_RE = re.compile(r"\$[\d][\d,.]*[MBK]?|[+-]?\d+(?:\.\d+)?%|`[^`]+`|exp_\d+|\b\d{2,3},\d{3}\b")


def _parse_canon_signals(canon_text: str) -> dict[str, str]:
    m = _SIGNALS_SECTION_RE.search(canon_text)
    body = m.group(1) if m else ""
    return {tag: text.strip() for tag, text in _SIGNAL_BULLET_RE.findall(body)}


def _fingerprints(text: str) -> set[str]:
    return set(_FINGERPRINT_RE.findall(text))


CANON_SIGNALS: dict[str, str] = _parse_canon_signals(CANON_TEXT)
_SIGNAL_FINGERPRINTS: dict[str, set[str]] = {tag: _fingerprints(body) for tag, body in CANON_SIGNALS.items()}


def likely_covered_signals(existing_text: str) -> list[str]:
    """Signal tags whose fingerprints show up often enough in the existing
    file that the signal was probably already planted somewhere in it.
    Heuristic (see module docstring) -- used to steer continuations away
    from restating a signal, never to guarantee it wasn't restated."""
    covered = []
    for tag, fps in _SIGNAL_FINGERPRINTS.items():
        if not fps:
            continue
        hits = sum(1 for fp in fps if fp in existing_text)
        if hits >= max(2, (len(fps) + 2) // 3):
            covered.append(tag)
    return sorted(covered)


# ---------------------------------------------------------------------------
# LEDGER: load / filter / render -- kept intentionally byte-for-byte
# identical to gen_rounds.py's own functions of the same name. See module
# docstring for why this is a deliberate duplication, not drift.
# ---------------------------------------------------------------------------
def load_ledger() -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    events = []
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[ledger] WARN  LEDGER.jsonl line {lineno} malformed ({e}), skipped")
    return events


def filter_ledger(events: list[dict], as_of_date: str) -> list[dict]:
    """Events at or before as_of_date, chronological. ISO YYYY-MM-DD dates
    sort correctly as plain strings, no date parsing needed."""

    def key(ev):
        return ev.get("date") or "0000-00-00"

    return sorted((ev for ev in events if key(ev) <= as_of_date), key=key)


def render_ledger(events: list[dict]) -> str:
    if not events:
        return "(empty -- this is the first round; nothing has happened yet)"
    return "\n".join(
        f"- {ev.get('date', '????-??-??')} [{ev.get('kind', 'event')}/{ev.get('vertical', '?')}] "
        f"(owner: {ev.get('owner', '?')}) {ev.get('summary', '')}"
        for ev in events
    )


# ---------------------------------------------------------------------------
# Defensive LEDGER-block stripping. None of the 9 bulk specs' focus text asks
# for a new datable event (they're noise/reference archives citing EXISTING
# events, not minting them) -- growth passes are told not to emit a trailing
# ```LEDGER block at all. This is a backstop in case a pass does anyway: it
# is discarded, never appended to LEDGER.jsonl, so a growth-invented "event"
# can never leak into what later rounds see as canon.
# ---------------------------------------------------------------------------
_LEDGER_FENCE_RE = re.compile(r"```\s*LEDGER\s*\n.*?\n```", re.DOTALL | re.IGNORECASE)


def strip_stray_ledger_block(text: str, *, source_path: str) -> str:
    cleaned, n = _LEDGER_FENCE_RE.subn("", text)
    if n:
        print(
            f"    [ledger] NOTE  {source_path}: stripped {n} unexpected LEDGER block(s) "
            f"from a growth pass (discarded, not appended to LEDGER.jsonl)"
        )
    return cleaned.rstrip()


def _next_day(iso_date: str) -> str:
    y, m, d = (int(x) for x in iso_date.split("-"))
    return (date(y, m, d) + timedelta(days=1)).isoformat()


# ---------------------------------------------------------------------------
# Defensive date-boundary check. Empirically (see the return report's
# smoke-test note), a continuation pass can drift past its round's as-of
# date after a few passes -- a Slack-archive continuation especially wants
# to keep advancing time forward, which is a strong prior the prompt
# instruction alone doesn't always overcome. This does not block or rewrite
# anything (truncating mid-generation risks a worse, mid-sentence cut); it
# flags loudly so a run is never silently trusted past this boundary.
#
# NOT \b on both ends: \b only fires at a \w/\W transition, and a digit and a
# letter are BOTH \w -- so `\b(20\d{2}-\d{2}-\d{2})\b` never matches a date
# immediately followed by a time (e.g. the bq_query_log adapter's own
# "2026-07-21T00:15:33Z", or a YAML `fetched_at: '...T12:00:00+00:00'`), the
# single most common shape in this corpus. That let query_logs bulk files
# drift 19 days past boundary across many passes with zero warnings raised.
# Lookaround for "not a digit" on both sides catches those while still
# rejecting a date embedded in a longer digit run (e.g. a job id).
# ---------------------------------------------------------------------------
_DATE_RE = re.compile(r"(?<!\d)(20\d{2}-\d{2}-\d{2})(?!\d)")


def find_dates_past_boundary(text: str, as_of_date: str) -> list[str]:
    return sorted({m for m in _DATE_RE.findall(text) if m > as_of_date})


# Defensive frontmatter-leak check. Empirically (see the return report), a
# continuation pass can emit a SECOND YAML frontmatter block mid-document
# despite the explicit "do not add frontmatter" instruction -- likely echoing
# the shape of the frontmatter it saw described in the prompt/CANON. Same
# treatment as the date check: detect and warn loudly, never silently strip
# (a false-positive strip could delete legitimate content that merely
# mentions one of these words).
_FRONTMATTER_LEAK_RE = re.compile(
    r"^---\s*$\n(?:[^\n]*\n){0,8}?(?:title|source_url|adapter|license|attribution|fetched_at):\s",
    re.MULTILINE,
)


def has_frontmatter_leak(text: str) -> bool:
    return bool(_FRONTMATTER_LEAK_RE.search(text))


# ---------------------------------------------------------------------------
# Cost tracking
# ---------------------------------------------------------------------------
def estimate_tokens(text: str) -> int:
    """Rough chars/4 heuristic, used for dry-run/projection estimates and as
    a fallback when the API doesn't return usage (shouldn't happen)."""
    return max(1, len(text) // 4)


class CostTracker:
    """Single-threaded (this script grows files serially, one at a time --
    the append-loop is inherently sequential per file, and gen_grow.py's own
    reference implementation is fully serial too), so no lock needed."""

    def __init__(self):
        self.calls = 0
        self.prompt_tokens = 0
        self.output_tokens = 0

    def add(self, prompt_tokens: int, output_tokens: int) -> None:
        self.calls += 1
        self.prompt_tokens += prompt_tokens
        self.output_tokens += output_tokens

    @staticmethod
    def cost_usd(prompt_tokens: int, output_tokens: int) -> float:
        return prompt_tokens / 1_000_000 * PRICE_IN_PER_1M_USD + output_tokens / 1_000_000 * PRICE_OUT_PER_1M_USD

    def line(self) -> str:
        return (
            f"[running total: {self.calls} call(s), {self.prompt_tokens:,} in / "
            f"{self.output_tokens:,} out tok, ${self.cost_usd(self.prompt_tokens, self.output_tokens):.4f}]"
        )


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------
CONTINUATION_SYSTEM = """You are continuing a synthetic internal document for "Acme" -- a \
fictitious, Walmart-scale retail/eCommerce company (the acme-ecomm demo corpus). Match the \
existing document's format, structure, and voice exactly -- same headers, timestamps, and \
field shapes as what you're shown. Use ONLY canon facts/people/customers/sellers/members/IDs; \
never invent a new named entity, and never reuse a name/handle/ID from the UNRELATED sibling \
"Acme Inc" B2B SaaS corpus (datasets/acme/CANON.md) -- different company, different people, \
different BigQuery dataset, never confused. Heavy noise is good; signal should be rare and \
buried, never headlined, and never repeated within the same document. Natural, messy, human \
voice appropriate to the document's system of record. Correct BigQuery paths are always FLAT: \
nexus-analyst-demo.acme_ecomm.<table> -- never acme_ecomm.marts.* nesting. Dates 2025-2026 \
only, never later than the round's as-of date given in the prompt. Do NOT add frontmatter, a \
title, or meta-commentary about being an AI or about this being a continuation. Do NOT emit a \
LEDGER block. Just continue the content."""


def build_continuation_prompt(spec: BulkSpec, existing_text: str, ledger_events: list[dict]) -> str:
    tail = existing_text[-TAIL_CHARS:] if len(existing_text) > TAIL_CHARS else existing_text

    covered = likely_covered_signals(existing_text)
    if covered:
        covered_note = (
            "Signals that a best-effort scan says LIKELY already appear somewhere earlier in "
            "this document (heuristic, not certain -- err on the side of trusting it). Do NOT "
            "restate these; if you include a signal at all this pass, prefer one not listed:\n"
            + "\n".join(f"- [{tag}]" for tag in covered)
        )
    else:
        covered_note = (
            "(no CANON signal reliably detected yet in the existing document by this "
            "best-effort scan -- you MAY introduce one if it fits naturally, but most passes "
            "should be pure noise; do not force one in)"
        )

    return f"""You are CONTINUING an existing internal document for Acme's eCommerce corpus \
(acme-ecomm demo). This document already exists on disk; you are only asked for MORE of it.

ROUND: {spec.round_name}  (as-of {spec.round_date})
SYSTEM OF RECORD: {spec.system} ({SYSTEMS.get(spec.system, "unlisted system")})
DOCUMENT: {spec.topic}
ADAPTER: {spec.adapter}

ORIGINAL DOCUMENT BRIEF (what this file already is -- stay in this lane):
{spec.focus}

Here is the END of the document as it stands right now (continue SEAMLESSLY from here -- do \
NOT repeat it, do NOT restate the frontmatter or a title, just keep going where it left off):
---
{tail}
---

{covered_note}

CANONICAL FACTS (frozen; never contradict):
{CANON_TEXT}

LEDGER -- everything that has happened at or before this round's as-of date ({spec.round_date}), \
{len(ledger_events)} event(s) (listed below). Separately, THIS DOCUMENT's own hard date ceiling is \
{spec.boundary_date} (see HARD DATE CEILING, rule 7 below) -- nothing you write may be dated, or \
reference anything, later than that. If the document's own internal dates already \
reach at or near that boundary, add MORE entries INTERLEAVED WITHIN the already-covered window \
(more density between existing dates) rather than extending past it:
{render_ledger(ledger_events)}

NOW CONTINUE the document with MORE of the same kind of content -- new entries/threads/queries/
tickets/rows that have NOT already appeared. Rules:
1. Match the existing format, structure, and voice EXACTLY.
2. Heavy noise is GOOD -- ordinary chatter, routine queries, mundane operational detail. Per \
CANON's STYLE section, bury roughly one signal per several hundred lines; most of what you add \
should be plausible filler, not signal.
3. Never restate a signal, fact, or specific number that's already in this document -- that \
makes it prominent instead of buried. See the covered-signals note above.
4. Use ONLY people/teams/customers/sellers/members/IDs established in CANON or the LEDGER. You \
may invent minor incidental specifics (a job ID, a timestamp, a Slack aside) as long as they \
don't contradict CANON/LEDGER.
5. Do NOT add a new frontmatter block, a new title, or any meta-commentary. This document \
already has exactly one YAML frontmatter block, at the very top (not shown to you here, since \
you're only continuing the end) -- never write a line that's just `---` followed by `title:` / \
`source_url:` / `adapter:` / `license:` / `fetched_at:`, that IS a frontmatter block and this \
one must not repeat. Do NOT emit a trailing ```LEDGER block -- this growth pass does not mint \
new canonical timeline events, only noise/reference content that cites what's already happened.
6. Fill as much of the output window as you can with NEW, varied, non-repetitive content. Do \
not summarize or truncate.
7. HARD DATE CEILING, repeated because continuations tend to drift past it once a timeline is \
already near the edge: the latest ANY date or timestamp may read is {spec.boundary_date}. Do not \
write {_next_day(spec.boundary_date)} or any later date, and do not time-skip forward to manufacture \
room -- if today ({spec.boundary_date}) is already densely covered, add earlier-in-the-window or \
same-day entries instead. Advancing the calendar is not a valid way to fit more content in.

Continue now."""


# ---------------------------------------------------------------------------
# Growth loop
# ---------------------------------------------------------------------------
def make_client():
    from google import genai  # deferred: --dry-run never needs this installed, see module docstring

    return genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


MAX_ATTEMPTS_PER_PASS = 2  # empirically (see return report), a pass that drifts past the date
# boundary or leaks a frontmatter block usually doesn't on a regenerate at the same temperature;
# one retry is cheap (a discarded attempt still costs one call) and meaningfully raises the odds
# of landing a clean pass without an unbounded/silent regenerate loop.


def _violations(text: str, as_of_date: str) -> list[str]:
    """Both known failure modes found during this script's own smoke-testing
    (see return report): the model can advance past its round's date
    boundary, or echo a second YAML frontmatter block mid-document, despite
    the prompt explicitly forbidding both."""
    problems = []
    overshoot = find_dates_past_boundary(text, as_of_date)
    if overshoot:
        problems.append(f"date(s) past boundary {as_of_date}: {overshoot}")
    if has_frontmatter_leak(text):
        problems.append("stray mid-document frontmatter block")
    return problems


def _generate_one_attempt(client, spec: BulkSpec, current: str, ledger_events: list[dict], tracker: CostTracker) -> tuple[str | None, str | None]:
    """One real API call. Returns (text, error) -- exactly one is None.
    Tracks cost for every real attempt, including ones later discarded for
    violating a check (the call genuinely happened and was billed)."""
    from google import genai

    prompt = build_continuation_prompt(spec, current, ledger_events)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                system_instruction=CONTINUATION_SYSTEM,
            ),
        )
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"

    text = strip_stray_ledger_block(response.text or "", source_path=spec.path)
    usage = getattr(response, "usage_metadata", None)
    prompt_tokens = getattr(usage, "prompt_token_count", None) or estimate_tokens(prompt)
    output_tokens = getattr(usage, "candidates_token_count", None) or estimate_tokens(text)
    tracker.add(prompt_tokens, output_tokens)

    if not text.strip():
        return None, "empty response"
    return text, None


def grow_file(client, spec: BulkSpec, target_kb: int, max_appends: int, tracker: CostTracker) -> tuple[float, float] | None:
    """Append continuations to spec's file until it reaches target_kb (or
    max_appends is hit, or a pass comes back empty/errors). Returns
    (before_kb, after_kb), or None if the file doesn't exist yet.

    Idempotent/resumable by construction: current size is always re-read
    from disk, never tracked in separate state, so a re-run after an
    interruption just continues from whatever's already there -- same
    resumability story as gen_rounds.py itself.
    """
    out_path = SOURCES_DIR / spec.path
    if not out_path.exists():
        print(f"  SKIP  {spec.path}  (not generated yet by gen_rounds.py)")
        return None

    existing = out_path.read_text(encoding="utf-8")
    before_kb = len(existing.encode("utf-8")) / 1024
    if before_kb >= target_kb:
        print(f"  OK    {spec.path}  {before_kb:.1f}KB already >= target {target_kb}KB -- skipping")
        return before_kb, before_kb

    all_events = load_ledger()
    ledger_events = filter_ledger(all_events, spec.round_date)

    current = existing
    current_kb = before_kb
    passes = 0
    while current_kb < target_kb and passes < max_appends:
        passes += 1
        text, problems, fatal = None, [], None
        for attempt in range(1, MAX_ATTEMPTS_PER_PASS + 1):
            candidate, err = _generate_one_attempt(client, spec, current, ledger_events, tracker)
            if candidate is None:
                fatal = err
                break
            problems = _violations(candidate, spec.boundary_date)
            text = candidate
            if not problems:
                break
            if attempt < MAX_ATTEMPTS_PER_PASS:
                print(f"    [retry] {spec.path} pass {passes} attempt {attempt}: {'; '.join(problems)} -- regenerating once")

        if fatal is not None:
            print(f"  STOP  {spec.path}  pass {passes}: {fatal} -- stopping this file, resumable next run")
            break
        if problems:
            print(
                f"    WARN  {spec.path} pass {passes}: kept after {MAX_ATTEMPTS_PER_PASS} attempt(s), "
                f"still has: {'; '.join(problems)} -- appended anyway (no auto-truncation, that risks "
                f"a worse mid-sentence cut); review this pass by hand before trusting the file."
            )

        with out_path.open("a", encoding="utf-8") as f:
            f.write("\n\n" + text)
        current = out_path.read_text(encoding="utf-8")
        current_kb = len(current.encode("utf-8")) / 1024
        added_kb = len(text.encode("utf-8")) / 1024
        print(f"  pass {passes}: +{added_kb:.1f}KB -> {current_kb:.1f}KB total  {tracker.line()}")

    status = "DONE" if current_kb >= target_kb else "STOP"
    print(f"  {status}  {spec.path}  {before_kb:.1f}KB -> {current_kb:.1f}KB  (target {target_kb}KB, {passes} pass(es))")
    return before_kb, current_kb


# ---------------------------------------------------------------------------
# Dry-run preview + rough cost/pass projection
# ---------------------------------------------------------------------------
ASSUMED_KB_PER_PASS = 8  # empirical: 5 live continuation passes on a scratch copy of the
# richest bulk file (slack/bulk__q2fy27-data-help-full-history-archive.md) added
# 8.1/7.4/8.7/5.3/2.3KB (mean ~6.4KB, trending down as the "already covered" list grows) --
# notably less than the 12-56KB gen_rounds.py's own single-shot ONE-DOCUMENT prompt produces.
# A continuation prompt is a different, less generative task for the model than "write the
# whole document"; plan passes accordingly. Adjust this constant if a fuller run shows a
# different steady-state figure.


def _resolve_target(spec: BulkSpec, target_override: int | None) -> int | None:
    return target_override if target_override is not None else spec.target_high_kb


def _current_kb(spec: BulkSpec) -> float:
    out_path = SOURCES_DIR / spec.path
    if not out_path.exists():
        return 0.0
    return len(out_path.read_text(encoding="utf-8").encode("utf-8")) / 1024


def print_dry_run(specs: list[BulkSpec], target_override: int | None) -> None:
    print(f"model={MODEL} project={PROJECT} location={LOCATION}  (dry-run: zero API calls)\n")
    all_events = load_ledger()
    shown = False

    for s in specs:
        out_path = SOURCES_DIR / s.path
        exists = out_path.exists()
        current_kb = _current_kb(s)
        target = _resolve_target(s, target_override)
        rng = f"{s.target_low_kb}-{s.target_high_kb}KB" if s.target_low_kb is not None else "UNPARSEABLE"
        will_grow = exists and target is not None and current_kb < target
        if not exists:
            note = "MISSING on disk"
        elif target is None:
            note = "no target"
        elif will_grow:
            note = "will grow"
        else:
            note = "already at/above target"
        boundary_flag = " (doc's own span extends past round date)" if s.boundary_date > s.round_date else ""
        print(
            f"  {s.path:<68} round={s.round_name:<7}({s.round_date}) now={current_kb:7.1f}KB  "
            f"parsed={rng:<13} target={target}KB  boundary={s.boundary_date}{boundary_flag}  [{note}]"
        )

        if not shown and will_grow:
            ledger_events = filter_ledger(all_events, s.round_date)
            existing = out_path.read_text(encoding="utf-8")
            prompt = build_continuation_prompt(s, existing, ledger_events)
            print("\n" + "=" * 78)
            print(f"FULL ASSEMBLED PROMPT for the first append pass of: {s.path}")
            print("=" * 78)
            print(prompt)
            print("=" * 78)
            print(
                f"(~{estimate_tokens(prompt):,} input tokens estimated for this prompt; "
                f"system_instruction adds ~{estimate_tokens(CONTINUATION_SYSTEM):,} more)\n"
            )
            shown = True

    print_projection(specs, target_override, all_events)


def print_projection(specs: list[BulkSpec], target_override: int | None, all_events: list[dict]) -> None:
    print(
        f"--- rough growth projection (planning estimate, NOT a guarantee -- assumes "
        f"~{ASSUMED_KB_PER_PASS}KB output/pass; real output-per-pass varies by adapter, see "
        f"the return report for the empirical smoke-test figure) ---"
    )
    canon_tok = estimate_tokens(CANON_TEXT)
    sys_tok = estimate_tokens(CONTINUATION_SYSTEM)
    total_add_kb = 0.0
    total_passes = 0
    total_cost = 0.0

    for s in specs:
        current_kb = _current_kb(s)
        target = _resolve_target(s, target_override)
        if target is None or current_kb >= target:
            continue
        add_kb = target - current_kb
        passes = max(1, -(-int(round(add_kb)) // ASSUMED_KB_PER_PASS))  # ceil div

        ledger_events = filter_ledger(all_events, s.round_date)
        ledger_tok = estimate_tokens(render_ledger(ledger_events))
        approx_in_tok = canon_tok + sys_tok + ledger_tok + estimate_tokens(s.focus) + 300  # +300: template scaffolding/tail
        approx_out_tok = ASSUMED_KB_PER_PASS * 1024 // 4

        cost = passes * CostTracker.cost_usd(approx_in_tok, approx_out_tok)
        total_add_kb += add_kb
        total_passes += passes
        total_cost += cost
        print(f"  {s.path:<68} +{add_kb:6.1f}KB  ~{passes:2d} pass(es)  ~${cost:.3f}")

    print(
        f"  TOTAL: ~{total_add_kb:.0f}KB to add across {sum(1 for s in specs if _resolve_target(s, target_override) and _current_kb(s) < _resolve_target(s, target_override))} file(s), "
        f"~{total_passes} pass(es), ~${total_cost:.2f}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Append-loop that grows acme-ecomm's bulk source files toward their realistic target KB size."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--file", metavar="PATH",
        help="grow one bulk file (path relative to sources/acme-ecomm/, e.g. query_logs/bulk__q1fy27-bq-audit-log.md)",
    )
    group.add_argument("--all", action="store_true", help="grow every bulk file discovered from gen_rounds.py's ROUNDS table")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="list files + targets and print one real assembled prompt; makes zero API calls",
    )
    parser.add_argument(
        "--max-appends", type=int, default=DEFAULT_MAX_APPENDS, metavar="N",
        help=f"safety stop: max continuation passes PER FILE (default {DEFAULT_MAX_APPENDS})",
    )
    parser.add_argument(
        "--target-kb", type=int, default=None, metavar="N",
        help="override the parsed target KB for the selected file(s) (applies to every file selected this run)",
    )
    args = parser.parse_args()

    if args.max_appends < 1:
        parser.error("--max-appends must be >= 1")

    all_specs = discover_bulk_specs()
    if not all_specs:
        parser.error(f"no bulk: True specs found in {GEN_ROUNDS_PATH}")

    if args.file:
        selected = [s for s in all_specs if s.path == args.file]
        if not selected:
            selected = [s for s in all_specs if Path(s.path).name == Path(args.file).name]
        if not selected:
            known = "\n  ".join(s.path for s in all_specs)
            parser.error(f"{args.file!r} is not a known bulk spec. Known bulk files:\n  {known}")
    else:
        selected = all_specs

    unparseable = [s for s in selected if s.target_high_kb is None]
    if unparseable and args.target_kb is None:
        for s in unparseable:
            print(
                f"WARN  {s.path}: could not parse a 'target N-MKB' range from its focus text -- "
                f"pass --target-kb to force a value. focus starts: {s.focus[:160]!r}"
            )
        selected = [s for s in selected if s.target_high_kb is not None]
        if not selected:
            parser.error("no selected spec has a parseable target, and no --target-kb override was given")

    print(
        f"Discovered {len(all_specs)} bulk spec(s) in {GEN_ROUNDS_PATH.relative_to(REPO)}; "
        f"{len(selected)} selected this run.\n"
    )

    if args.dry_run:
        print_dry_run(selected, args.target_kb)
        return

    client = make_client()
    tracker = CostTracker()
    results = []
    for s in selected:
        target = args.target_kb if args.target_kb is not None else s.target_high_kb
        result = grow_file(client, s, target, args.max_appends, tracker)
        if result is not None:
            results.append((s.path, result[0], result[1], target))

    print("\n--- summary (before -> after, target) ---")
    for path, before_kb, after_kb, target in results:
        print(f"  {path:<68} {before_kb:7.1f}KB -> {after_kb:7.1f}KB   (target {target}KB)")
    print(f"\n{tracker.line()}")


if __name__ == "__main__":
    main()
