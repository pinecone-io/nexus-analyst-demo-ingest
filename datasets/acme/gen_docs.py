"""
LLM-driven bulk source generator for Acme demo corpus.
Generates 13 source files across all semantic spaces using Gemini,
then writes them to sources/acme-raw/.

Usage:
  uv run --no-project --with google-genai python datasets/acme/gen_docs.py
"""
import os
import sys
from pathlib import Path
from google import genai

REPO = Path(__file__).resolve().parents[2]
RAW = REPO / "sources" / "acme-raw"

CANON = (Path(__file__).parent / "CANON.md").read_text()

MODEL = os.environ.get("GEN_MODEL", "gemini-3.5-flash-lite")

# 13 files across semantic spaces — each targets topics that should show up
# in diverse top-K searches to saturate the baseline's retrieval.
FILES = [
    {
        "path": "meetings/bulk__weekly-data-team-standup-notes-2025.md",
        "adapter": "notion_runbook",
        "topic": "Weekly data team standup notes spanning all of 2025",
        "focus": """Generate ~50 weekly standup entries (Jan-Dec 2025). Each entry: date header, 4-6 bullet points from team members about what they're working on.
Cover ALL semantic spaces across the entries: ARR reporting, NRR calculations, dbt model ownership, account health mart, bookings attribution, engagement definition changes, schema questions, Looker dashboard issues, support ticket analysis, workflow run performance, marketing attribution, churn analysis, board prep.
Include lots of mundane noise: PTO notices, sprint planning refs, Looker migration status, backfill tasks, PR reviews, on-call handoffs.
Bury these signals naturally across different weeks:
- Someone mentions the NRR mart uses a LEFT JOIN so churned customers stay at $0 (not dropped)
- Someone reminds team that bookings_acv_usd is already annualized
- Discussion about the engaged-customer threshold recalibration in Q4 2025
- Rajiv notes the dataset is flat (no nested marts paths)
- Brief mention that the VRS spec is still parked/not built
- Lina clarifies arr_snapshot is the canonical board ARR source, not dim_customers.current_mrr_usd
Target: 400KB+ of realistic standup notes.""",
    },
    {
        "path": "docs/bulk__data-warehouse-faq-internal.md",
        "adapter": "notion_runbook",
        "topic": "Internal data warehouse FAQ — Acme data team wiki",
        "focus": """Generate a comprehensive internal FAQ document (60+ Q&A pairs) covering every aspect of the Acme warehouse.
Organize into sections: Getting Started, Schema & Tables, Metrics & Definitions, Common Queries, Troubleshooting, dbt Models, Dashboards.
Cover: how to compute ARR, where NRR lives, what engaged means, account health bands, bookings attribution, plan tiers, churn definitions, support ticket analysis, workflow runs, marketing touches, user events.
Include wrong-but-corrected entries (FAQ: "Q: Is ARR in dim_customers? A: No — use arr_snapshot. dim_customers.current_mrr_usd drifts intraday.").
Include noise FAQ entries: how to get Looker access, VPN setup, dbt dev environment, PR review process, on-call rotation.
Every signal from the canon should appear somewhere in the FAQ, stated accurately.
Target: 350KB+.""",
    },
    {
        "path": "query_logs/bulk__bq-audit-log-2026-Q1.md",
        "adapter": "query_log",
        "topic": "BigQuery query audit log export — 2026 Q1",
        "focus": """Generate a large query audit log: 200+ real-looking BigQuery queries that Acme analysts ran in Q1 2026.
Format each entry: timestamp, user (from the cast), bytes billed, duration, then the SQL.
Queries should span ALL tables (dim_customers, fact_subscriptions, fact_workflow_runs, fact_user_events, fact_support_tickets, fact_opportunities, fact_nps_responses, fact_marketing_touches, arr_snapshot, nrr_trailing_12, account_health, bookings_attribution, workflow_runs_daily).
Include correct FQT paths (`nexus-analyst-demo.acme.table_name` — FLAT, no nested marts).
Mix in: simple SELECTs, JOINs, aggregations, window functions, CTEs.
Include a few WRONG queries with comments like "-- this returned 0 rows, path doesn't exist" for `acme.marts.cs.account_health`.
Include queries computing ARR, NRR, engagement, health bands, bookings by channel, churn cohorts, support CSAT, workflow error rates.
Some queries should reference specific cast customers (cust_000700 Cobalt Systems, cust_000704 Onyx Robotics, etc.) with correct attributes.
Target: 400KB+.""",
    },
    {
        "path": "slack/bulk__slack-cs-at-risk-2025-2026.md",
        "adapter": "slack_thread",
        "topic": "Slack #cs-at-risk channel archive 2025-2026",
        "focus": """Generate a long Slack #cs-at-risk channel archive with 80+ threads spanning 2025-2026.
CSMs (marco.silva, olivia.tran, grace.liu) posting about accounts that are flagged, at risk, or churning.
Reference specific cast customers with their EXACT attributes (tier, seats, MRR, region, CSM, AE).
Cover: accounts hitting critical health band, low utilization, P1 tickets, NPS detractors, upcoming renewals at risk, expansion blockers, churn debriefs.
Include discussions about WHY Enterprise health rules differ (no utilization — unlimited seats, critical only on uncollectible).
Include threads about Beacon Studios (cust_000287) churn debrief aftermath.
Include Kestrel Networks (cust_000708) budget-cut churn.
Include noise: team scheduling, OOO notices, unrelated process discussions, emoji reactions.
Bury signals about account_health_status enum, the Enterprise vs non-Enterprise critical rule, engagement definition.
Target: 350KB+.""",
    },
    {
        "path": "slack/bulk__slack-revenue-ops-2025-2026.md",
        "adapter": "slack_thread",
        "topic": "Slack #revenue-ops channel archive 2025-2026",
        "focus": """Generate a long Slack #revenue-ops channel archive with 70+ threads.
Finance + RevOps people (lina.cho, rachel.stein, jorge.martinez) discussing ARR, bookings, pipeline, quotas, board reporting.
Topics: ARR reconciliation, bookings by channel, NRR methodology for board, quota attainment, pipeline coverage, deal reviews.
Include threads where someone asks about bookings_acv_usd and gets told it's already annualized.
Include threads where someone tries to derive ARR from dim_customers and gets corrected (use arr_snapshot).
Include discussions about free-to-paid conversions not appearing in bookings_attribution.
Include NRR deep-dives: the fixed-cohort method, GRR vs NRR, why churned customers stay at $0.
Reference specific deals with cast customers and their exact ACV/tier/channel.
Include noise: expense reports, team lunch, meeting scheduling, CRM migration updates from jorge.martinez.
Target: 350KB+.""",
    },
    {
        "path": "dbt/bulk__dbt-model-docs-full-export.sql",
        "adapter": "dbt_model",
        "topic": "Full dbt model documentation export — all models",
        "focus": """Generate a comprehensive dbt model documentation dump covering 40+ models.
For each model: a SQL block with comments, schema description, column descriptions, tests, dependencies.
Cover the full dbt project structure: staging (stg_*), intermediate (int_*), marts (finance: arr_snapshot, nrr_trailing_12; cs: account_health; product: workflow_runs_daily; sales: bookings_attribution).
IMPORTANT: dbt folder paths (marts/finance/, marts/cs/) are FILESYSTEM ONLY — the actual BigQuery tables are FLAT under `nexus-analyst-demo.acme.*`. Include comments that make this explicit.
Include owner annotations (lina.cho owns finance, rajiv.menon owns core, david.kim owns staging, nina.patel owns product).
Include TODO/FIXME comments, deprecation notices, WIP models.
Include the VRS draft model that's commented out / never built.
Include correct column types, join patterns, materialization strategies.
Target: 400KB+.""",
    },
    {
        "path": "postmortems/bulk__incident-archive-2025-2026.md",
        "adapter": "postmortem",
        "topic": "Incident postmortem archive — 2025-2026",
        "focus": """Generate 15-20 detailed incident postmortems spanning 2025-2026.
Format: each with ## header, date, severity, affected systems, timeline, root cause, resolution, action items.
Cover incidents across: dbt freshness failures, Looker cache issues, BigQuery cost spikes, workflow run stale data, Stripe invoice pipeline stuck, Pinecone index rebuild, Salesforce attribution mismatch, engagement threshold recalibration.
Include incidents that touch metric definitions: one where NRR was briefly computed wrong (INNER JOIN instead of LEFT JOIN, inflated the number), one where ARR showed $42M (stale Looker PDT), one where engagement count dropped because the threshold was recalibrated in Q4 2025.
Include mundane incidents: SSL cert expiry, staging environment down, CI/CD pipeline broken, Slack bot outage.
Reference specific tables, marts, team members from the cast. Include action items assigned to specific people.
Target: 350KB+.""",
    },
    {
        "path": "gong/bulk__gong-cs-qbr-calls-2025-2026.md",
        "adapter": "gong_call",
        "topic": "Gong CS/QBR call transcripts — 2025-2026",
        "focus": """Generate 12-15 detailed QBR and CS call transcripts.
Each call: header with account, date, attendees (Acme CSM/AE from cast + customer-side names), then timestamped speaker turns.
Cover: quarterly business reviews, health check calls, expansion discussions, renewal negotiations, escalation calls.
Use cast customers with their EXACT attributes. Include calls for:
- Cobalt Systems (cust_000700, Business, 80 seats, EMEA) — QBR, discussing utilization and health metrics
- Onyx Robotics (cust_000704, Enterprise, 500 seats) — expansion discussion, someone asks about VRS and gets told it's not built yet
- Marigold Health (cust_000701, Enterprise, 300 seats) — renewal, discussing value delivered
- Harbor Dynamics (cust_000713, Business, 150 seats, APAC) — escalation about P1 tickets
- Yarrow Logistics (cust_000703, Business, 120 seats, APAC) — QBR, workflow run performance review
Include lots of small talk, tangents, meeting logistics noise.
Bury signals: what "engaged" means when a customer asks, the Enterprise health rules, VRS not existing.
Target: 350KB+.""",
    },
    {
        "path": "scratch/bulk__analyst-scratch-notes-2026.md",
        "adapter": "notion_runbook",
        "topic": "Analyst scratch notes and working docs — 2026",
        "focus": """Generate a large collection of analyst scratch notes, working documents, and draft analyses from Q1-Q2 2026.
Include notes from: lina.cho (finance/ARR/NRR), rajiv.menon (dbt/schema), nina.patel (product/engagement), david.kim (pipeline/freshness), marco.silva (CS/health).
Cover: board prep scratch work, metric reconciliation notes, ad-hoc analysis drafts, meeting prep, investigation notes.
Include a scratch section where someone tries to compute NRR manually and gets it wrong (INNER JOIN), then corrects it.
Include Lina's board prep notes with ARR by tier (~$39M total), NRR (1.07), GRR (0.94).
Include Nina's engagement analysis notes about the Q4 2025 threshold change.
Include David's notes about the flat dataset structure (correcting someone who asked about nested paths).
Include draft VRS spec notes that are explicitly marked as "parked" / "not built".
Include lots of TODO items, abandoned queries, random thoughts, meeting action items.
Target: 350KB+.""",
    },
    {
        "path": "docs/bulk__onboarding-guide-data-analysts.md",
        "adapter": "notion_runbook",
        "topic": "Data analyst onboarding guide — Acme internal",
        "focus": """Generate a comprehensive onboarding guide for new data analysts joining Acme.
Sections: Welcome, Tools & Access, Warehouse Overview, Key Tables, Metrics We Track, Common Queries, dbt Development, Dashboard Ownership, Processes, FAQ.
Cover every table and mart with descriptions and example queries.
Explicitly state the FLAT dataset convention (no nested paths).
Walk through how to compute every key metric: ARR, NRR, GRR, engagement, churn rate, bookings, pipeline coverage, NPS.
Include gotchas section: "Don't use dim_customers for ARR", "bookings_acv_usd is already annual", "NRR uses LEFT JOIN not INNER", "VRS columns don't exist yet", "Enterprise health rules differ".
Include sections about team structure, who owns what, Slack channels to join, meeting cadence.
Include lots of operational noise: how to set up your dbt dev environment, Looker training, BigQuery cost management, PR review norms.
Target: 400KB+.""",
    },
    {
        "path": "slack/bulk__slack-engineering-2025-2026.md",
        "adapter": "slack_thread",
        "topic": "Slack #engineering channel archive 2025-2026",
        "focus": """Generate a long Slack #engineering channel archive with 60+ threads.
Engineers (priya.anand, david.kim, rajiv.menon + invented eng names using IDs in 0720-0730 range) discussing pipeline issues, dbt runs, BigQuery performance, workflow engine, integrations.
Topics: dbt run failures, BigQuery slot contention, workflow run latency spikes, Pinecone index issues, Stripe webhook reliability, Salesforce sync, schema migrations.
Include threads about: p95/p99 workflow duration spikes, AUTH_FAILED error codes, rate limiting, step timeouts, integration downtime.
Include discussions about workflow_runs_daily mart, error_code analysis, duration percentiles.
Include noise: deploy announcements, PR reviews, tech debt discussions, architecture proposals, incident response coordination.
Reference specific tables and correct schema. Some threads should cross-reference postmortem docs.
Target: 350KB+.""",
    },
    {
        "path": "docs/bulk__metric-definitions-handbook.md",
        "adapter": "notion_runbook",
        "topic": "Metric definitions handbook — official Acme reference",
        "focus": """Generate the official Acme metric definitions handbook.
For EVERY metric Acme tracks, provide: definition, formula, canonical source table, SQL example, owner, caveats, related metrics.
Metrics to cover (30+): ARR, MRR, NRR, GRR, logo churn, revenue churn, engaged customer, active user, paid customer, seat utilization, account health status, bookings ACV, pipeline coverage, quota attainment, NPS, CSAT, workflow success rate, workflow error rate, p95 duration, support resolution time, first response time, expansion MRR, contraction MRR, new ARR, churn ARR, net new ARR, LTV, CAC, payback period, gross margin.
For each, include the canonical SQL and the correct source table (FLAT paths).
Include a "Common Mistakes" callout for metrics where people get it wrong (NRR join type, ARR source, bookings annualization, engagement threshold, Enterprise health rules, VRS not existing).
This document should be THE authoritative reference — every signal from the canon appears here.
Target: 400KB+.""",
    },
    {
        "path": "meetings/bulk__board-meeting-prep-notes-2025-2026.md",
        "adapter": "notion_runbook",
        "topic": "Board meeting prep notes and minutes — 2025-2026",
        "focus": """Generate detailed board meeting prep notes and minutes for 6-8 board meetings spanning 2025-2026.
Each meeting: agenda, prep notes (who's pulling what), the actual metrics presented, Q&A from board members, action items.
Cover: ARR growth trajectory (~$39M), NRR trend (1.07), GRR (0.94), bookings by channel, pipeline, churn analysis, expansion, engagement metrics, product usage.
Include board member questions that probe the numbers: "Is that NRR on a fixed cohort?", "Why doesn't the ARR match what I see in the Looker dashboard?" (stale cache), "What's our exposure in at-risk accounts?", "How do you define engaged?".
Include sam.reyes (CEO) and rachel.stein (CFO) presenting; lina.cho preparing the numbers.
Include discussions about wanting a "value realization score" — and the team saying it's still in draft.
Include lots of logistical noise: scheduling, catering, slide formatting, who's presenting what.
Include references to specific tables and correct numbers from the canon.
Target: 400KB+.""",
    },
]

SYSTEM = """You are generating synthetic internal documents for a fictitious company called "Acme Inc" (a B2B SaaS workflow automation platform). The content is for an analytics demo.

RULES:
1. Everything must be internally consistent with the CANON provided.
2. Use ONLY the people, customers, IDs, and numbers from the CANON. Never invent contradicting facts.
3. Write in a natural, messy, human voice appropriate for the document type.
4. Heavy noise is GOOD — off-topic chatter, mundane details, tangents. The signal should be buried.
5. Make it LONG. Target the specified size. Don't summarize or compress — be verbose, include repetition across entries (different people asking similar questions in different months is realistic).
6. All dates should be in 2025-2026 range.
7. Use correct BigQuery FQT paths: `nexus-analyst-demo.acme.<table>` (FLAT, no nested marts).
8. Include YAML frontmatter at the very start (before anything else)."""


def generate_file(spec: dict) -> tuple[Path, int]:
    prompt = f"""Generate the following document for Acme Inc's internal corpus.

DOCUMENT: {spec['topic']}

INSTRUCTIONS:
{spec['focus']}

YAML FRONTMATTER (put this at the very top):
---
title: "{spec['topic']}"
source_url: "internal://acme/{spec['path'].replace('bulk__', '').replace('.md', '').replace('.sql', '')}"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: {spec['adapter']}
---

CANONICAL FACTS (never contradict these):
{CANON}

NOW GENERATE THE FULL DOCUMENT. Be extremely verbose and detailed. Target 400KB+ of content. Do not truncate or summarize."""

    client = genai.Client(
        vertexai=True,
        project=os.environ.get("VERTEX_PROJECT_ID", "mission-control-350520"),
        location="global",
    )

    out_path = RAW / spec["path"]
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"  generating {spec['path']}...", end="", flush=True)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=1.0,
            max_output_tokens=65536,
            system_instruction=SYSTEM,
        ),
    )

    text = response.text or ""
    out_path.write_text(text, encoding="utf-8")
    size = len(text.encode("utf-8"))
    print(f" {size/1024:.0f}KB ({len(text.splitlines())} lines)", flush=True)
    return out_path, size


def main():
    # Check for existing bulk files to skip
    existing = {p.name for p in RAW.rglob("bulk__*")}
    print(f"Found {len(existing)} existing bulk files: {existing}")
    print(f"Generating {len(FILES)} files...\n")

    total = 0
    generated = []
    for i, spec in enumerate(FILES):
        fname = Path(spec["path"]).name
        if fname in existing:
            existing_path = RAW / spec["path"]
            if existing_path.exists():
                size = existing_path.stat().st_size
                print(f"[{i+1}/{len(FILES)}] SKIP {spec['path']} (exists, {size/1024:.0f}KB)")
                total += size
                generated.append((existing_path, size))
                continue

        print(f"[{i+1}/{len(FILES)}] ", end="")
        try:
            path, size = generate_file(spec)
            total += size
            generated.append((path, size))
        except Exception as e:
            print(f" ERROR: {e}")
            generated.append((None, 0))

    print(f"\n{'='*60}")
    print(f"Total: {total/1024/1024:.1f}MB across {sum(1 for p,_ in generated if p)} files")
    for p, s in generated:
        if p:
            print(f"  {s/1024:6.0f}KB  {p.relative_to(RAW)}")


if __name__ == "__main__":
    main()
