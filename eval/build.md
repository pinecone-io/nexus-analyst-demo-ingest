# Build Specification

## Goal

Build a retrieval pipeline that scores well on the eval set under the latency budget. The two stages are `curate.py` (build-time, runs once per build iteration) and `query.py` (query-time, runs on every request).

Curate-time work is free; query-time work is paid for on every request. When questions need facts spread across multiple source files, pre-synthesizing dense **canonical articles** during curate beats running multi-round retrieval at query time

Don't over-optimize `query.py` before you've exhausted what better synthesis on the curate side can do. If p90 won't budge after a few query-side knob tweaks, the next move is usually to invest more in `curate.py`, not less.

## Reference: shape of a canonical article

Below is a sketch of the kind of dense, redundant document that tends to retrieve well in a single top-K hit. It fuses several source files into one article, repeats key facts under multiple phrasings, and cites the originals. Treat this as a structure to mimic — fill it with facts from the actual source corpus, not from this template. Do not do this for every source file, do this for every concepts/entities instead that may span across multiple files

```markdown
# <Concept that fuses 2-4 source files>

This article is the canonical reference for <the cross-source concept>.

## <Entities or tables involved>

- <Entity A>: <where it lives, key identifiers, relevant columns>.
- <Entity B>: <where it lives, key identifiers, relevant columns>.
- <Entity C>: <where it lives, key identifiers, relevant columns>.

## <How they connect>

<Describe the join / lookup / temporal alignment / unit conversion in prose, then
restate the same thing as code or as a formula. Restating in multiple forms is
intentional — it improves embedding recall for differently-phrased user
questions.>

## <Caveats, sentinels, gotchas>

- <Pitfall 1: e.g. a sentinel value that means "missing">
- <Pitfall 2: e.g. a column naming discrepancy between two sources>
- <Pitfall 3: e.g. a partition that's missing from one side>

## Sources

<source-file-1.md>, <source-file-2.md>, <source-file-3.md>.
```

## Authority hierarchy when sources disagree

Source corpora often contain facts at multiple "levels of truth" for the same concept. Curated articles must encode the precedence so query-time synthesis can surface the most authoritative answer first, with lower-authority sources cited as context.

General rule, in descending authority:

1. **Materialized / shipped artifacts** — tables that exist and are queryable today (verifiable via schema dumps), pipelines that run, dashboards in production. If a source file describes a "derived metric" and a corresponding materialized table exists in the warehouse for that metric, the materialized table's fully-qualified name is the canonical answer to "where do I get this metric?" — not the raw base tables that the metric derives from. The base tables are the implementation; the materialized derivation is what queries should target.
2. **Authoritative documentation of shipped artifacts** — schema dumps for column truth, formula definitions for unit/sentinel semantics, runbooks describing live processes.
3. **Organizational context** — Slack threads, call transcripts, postmortems, internal notes. Use these to explain the *why* and the *qualitative state*, not as the source of truth for table identifiers, columns, or formulas.
4. **Drafts, proposals, and WIP** — design docs, RFCs, "TBD"-tagged spec pages, anything explicitly marked as not-shipped (frontmatter flags like `status: draft`, `WIP`, `do not implement`, filenames containing `draft`, banner warnings). These describe intent, not reality. **Never** present a draft as the authoritative source for a table or formula. Surface as forward-looking context only, with the draft status preserved verbatim. If a user asks "where do I find metric X" and the only matching source is a draft, the answer is "X is not yet built — current alternative is Y" (citing the live alternative), not "X lives at table Z".

When two sources disagree, the higher-authority source wins, and the curated article should call out the disagreement rather than silently pick one.

## When latency is the bottleneck, invest in the curate side

If retrieval p90 is over budget after a few rounds of `query.py` knob-tweaking (top_k, rerank cutoffs, candidate thresholds), **stop tuning query and start enriching curate**. Query-side optimization has diminishing returns once the chunks themselves are the limiting factor.

Symptoms that mean the bottleneck is curate, not query:
- The eval pass rate is healthy (≥ threshold) but p90 is 2-4× the budget.
- Single queries pull 5+ chunks and synthesize across them — the model is doing curate-time work at query time.
- Latency is dominated by reranking + cross-chunk synthesis rather than the embedding lookup itself.

Counterintuitive but true: **denser, more verbose canonical articles often improve BOTH accuracy AND latency**. The mechanism:

1. **Fewer chunks needed per query.** A query that previously had to fetch 6 raw chunks and synthesize across them can now hit one canonical article in a single top-K — eliminating the multi-round retrieval cost.
2. **Better embedding recall.** Restating the same fact in multiple phrasings (prose + formula + table + bullet list) gives the embedding more surface area to match against differently-phrased user questions.
3. **Less query-time synthesis.** When the canonical article already pre-fuses the cross-source facts, the query-time LLM has less work to do — just extract and cite, not stitch.
4. **Pre-paid disambiguation.** Authority precedence (materialized > docs > org chatter > draft) is encoded once at curate time. Query time doesn't have to re-rank chunks by authority — the article already privileged the right source.

The ceiling on what query-side tuning can achieve is set by the chunks. If chunks are raw source slices, multi-faceted questions WILL require multi-chunk fetch and that latency is unavoidable. If chunks include pre-synthesized canonical articles, multi-faceted questions can land on a single article — and the latency drops by an integer factor, not a percentage.

When the build optimizer is stuck (eval passing but latency over budget, or both close to threshold but not improving), the right next move is almost always: **rewrite `curate.py` to author one or more canonical articles**, not tweak `query.py` further. The build.md author has explicitly flagged this trade-off so the build agent should not waste iterations on retrieval params alone.

## Patterns for cross-source fusion

Per-file summarization is the easy path: rewrite each input as a denser version of itself. This helps embedding recall but doesn't reduce the number of chunks a multi-faceted query has to fetch — the per-file shape is preserved.

The valuable curate-side move is **fusing several source files into one canonical article** that an embedding can hit in a single top-K. The agent's job at curate-time is to recognize the patterns below in the source corpus and emit one canonical article per recognized cluster, not to slavishly copy these examples.

These patterns are *shapes of fusion*, not literal recipes. Adapt them to whatever the actual corpus contains. The examples below intentionally use placeholders so the agent doesn't pattern-match on specific filenames or domains.

**Concept-centric fusion.**
A glossary-style definition file describes term `X`. A pipeline / model file computes a value derived from `X`. A runbook references `X` as part of a workflow. A discussion thread debates how `X` should change. All four point to the same concept. → Fuse into one canonical article keyed on `X`: definition + how it's computed + where it's used operationally + outstanding ambiguities. A single retrieval hit answers "what is X?", "how do we compute X?", "where does X show up?", and "is the team rethinking X?".

**Entity-centric fusion.**
A schema file describes table `T`. A documentation file describes the model that produces `T`. Quality-control or freshness conventions mention `T` indirectly. A query-pattern file shows the canonical SQL idiom against `T`. → Fuse into one entity article for `T`: schema + producer model + freshness expectations + canonical query patterns. Anyone asking "where do I get `T` and how do I query it correctly" lands on the article.

**Pipeline-lineage fusion.**
A derived artifact `D` reads from base inputs `A` and `B`, with a refresh cadence and downstream consumers. The base inputs have their own description files. The downstream consumers (dashboards, alerts, other derived artifacts) are described elsewhere. → Fuse into one lineage article for `D`: upstream inputs + transformation logic + cadence + downstream impact. A single hit answers "what feeds `D`" and "what breaks if `D` is wrong".

**Incident / decision history fusion.**
A postmortem describes incident `I`. The team's chat thread during `I` is preserved. The model file's history records the remediation that landed after `I`. → Fuse into one history article for `I`: timeline + root cause + remediation + lasting code/process change. Future questions about "what happened with `I`" or "why does the model do `X` now" hit one article.

**Process / runbook fusion.**
A runbook describes a multi-step workflow. The data inputs the workflow consumes are described in separate model/schema files. The escalation paths and ownership are in another doc. → Fuse into one process article: triggers + cadence + data inputs + decision criteria + escalation/ownership. A single hit serves "walk me through how we handle X".

**Authority precedence within a single article.**
Inside any canonical article that fuses sources of differing authority (shipped vs. draft, runbook vs. scratch note, glossary vs. slack debate), explicitly preserve the precedence. The shipped artifact is the answer; the draft is forward-looking context with its draft status restated; the chatter is the qualitative why. Encoding precedence at curate-time means query-time synthesis doesn't have to re-rank chunks by authority on every request.

**Negative-fusion (anti-pattern to surface).**
When the corpus contains a description of something that does NOT exist in the queryable warehouse (proposed table, named-but-unbuilt mart, deprecated path), produce a small "negative-knowledge" article that pairs the description with the explicit non-existence claim and points at the real alternative. This makes the negative assertion retrievable as a single chunk, so questions about the non-existent artifact don't drag in the proposal as if it were authoritative.

The number of canonical articles a corpus needs is roughly the count of *cross-source concepts*, not the count of source files. A 50-file corpus might collapse into 10-15 canonical articles; some files will participate in multiple articles, and that's fine — redundancy across articles improves recall.

## How to produce these articles

`curate.py` is the program that produces canonical articles. The build agent's job is to **write code in `curate.py`** that reads the source files at curate time and synthesizes the articles dynamically. The articles must be derived from the source corpus by `curate.py` itself.

Do NOT:
- Hardcode the article content (or substantial fragments of it) inside `curate.py` as Python string literals.
- Ask an external LLM (or use your own training-data knowledge) for facts that should come from the source files.
- Pre-compute the articles outside `curate.py` and paste them in.

If the agent reads source files and authors the article text directly, that's the agent doing curate work — not `curate.py` doing curate work. The pipeline must be reproducible: running `curate.py` from scratch on the source corpus must regenerate the same articles. That's only true if `curate.py` is the one reading sources and synthesizing, typically via an LLM call inside the script.
