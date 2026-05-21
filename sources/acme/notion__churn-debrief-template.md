---
title: "Notion runbook — Churn debrief template (with patterns observed)"
source_url: "internal://acme/notion/churn-debrief-template"
license: "synthetic-demo"
attribution: "Acme Inc Notion runbook (synthetic demo). Owner: VP CS (Elena Volkov)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Churn debrief template

> **Owner**: Elena Volkov (VP CS)
> **Mandatory for**: any paid customer churn (Pro / Business / Enterprise). Free downgrades exempt.
> **Due**: within 10 business days of churn confirmation
> **Last reviewed**: 2026-04-01
>
> 🚧 `// TODO: we keep getting "Free downgrades" that are functionally Pro/Business churns (customer drops to Free instead of cancelling cleanly). Should we treat these as churns too? Currently they're invisible in the "logo churn" metric. -elena 2026-03-22`

Use this template for every churn debrief. Post in `#cs-handoff` and link from CRM. Examples in the wild: `slack__cs-handoff__cust000287-churn-debrief.md`.

---

## Template

```markdown
# Churn debrief — <Customer Name> (cust_xxxxxx)

**Owning CSM**: @<csm-name>
**Owning AE**: @<ae-name>
**Plan at churn**: <Pro|Business|Enterprise>
**Seats / MRR / ARR**: <X seats / $Y MRR / $Z ARR>
**Tenure**: <N months>
**Renewal date had been**: <YYYY-MM-DD>
**Actual churn date**: <YYYY-MM-DD>

## Churn reason (canonical taxonomy)

Pick one primary, optionally one secondary:
- competitor
- price
- feature_gap
- no_decision
- timing
- voluntary_consolidation
- involuntary (payment failure)

**Primary**: <one>
**Secondary**: <one or none>

## Engagement at churn

- 28d active users / paid seats: <X / Y> (utilization <Z>)
- Trailing 28d successful workflow runs: <N>
- NPS in the last completed quarter: <score, segment>
- Was account "engaged" per glossary definition? <yes / no>

## Read

A 1-2 sentence summary of *why* they churned, in plain language. Did the product fail? Was it a relationship loss? A consolidation? Be honest.

## Preventability

Was this preventable? Mark one:
- **Preventable** — we missed signals or didn't act on them
- **Partially preventable** — we acted but couldn't move the customer
- **Not preventable** — driven by factors outside our control (M&A, budget freeze, parent-company consolidation)

If preventable or partially: what would we do differently next time?

## Post-mortem actions

| Owner | Action | Due |
|---|---|---|
| ... | ... | ... |

## CRM updates

- [ ] `loss_reason` set in CRM
- [ ] Account flagged as "do not contact" / "winback eligible / ineligible"
- [ ] Reference opt-in if applicable (rare for churns but valuable when it happens)

---
```

## Why we do this

Two reasons:

1. **Pattern detection.** Aggregating debrief outcomes lets us identify systemic causes (e.g., a feature gap mentioned in 5+ debriefs becomes a Product priority).
2. **Honest accountability.** The "preventability" question forces the team to confront what we missed, instead of always blaming the customer or the market.

## Where it lives

- Posted in `#cs-handoff` (channel of record)
- Linked from the customer's Salesforce record
- Aggregated quarterly into a churn dashboard owned by Elena

## Patterns observed (FY2025-2026 so far)

> **Note**: this section is updated quarterly. Last updated 2026-04-01.

| Loss reason | Count YTD | % |
|---|---|---|
| competitor | 14 | 31% |
| price | 9 | 20% |
| feature_gap | 8 | 18% |
| voluntary_consolidation | 6 | 13% |
| no_decision | 4 | 9% |
| timing | 3 | 7% |
| involuntary | 1 | 2% |

> Of `feature_gap` churns, 4 of 8 mentioned Salesforce CPQ depth. This is the strongest signal we have for the H1 2026 product priority `CPQ-DEEP-2026`.

> Of `competitor` churns, the breakdown by named competitor:
> - Workato: 8
> - Tray: 4
> - Boomi: 1
> - "Internal build" (customer built a homegrown tool): 1

## Sub-page link history

- [Churn debrief Q1 2026 archive] — all Q1 2026 debriefs
- [Churn debrief Q4 2025 archive]
- [Churn debrief Q3 2025 archive]
- [Older debriefs (pre-2025)] — kept for reference, not actively maintained

## Edge cases / FAQ

> **Q: Customer churned but their primary admin says they "might come back next year". Do I still write a debrief?**
> Yes. Write it now. If they return we celebrate. If they don't, we have the post-mortem on file.

> **Q: Customer is downgrading from Business to Free, not technically cancelling. Debrief required?**
> Currently no, but elena's TODO above flags this as a gap. Use your judgment — for a 50-seat Business → Free downgrade, write the debrief. For a 5-seat Pro → Free, skip.

> **Q: Customer ghosted us — never explicitly cancelled, just stopped paying. Debrief?**
> Yes. Mark loss reason as `involuntary` and note the ghost pattern in the read section.

## Comment thread

> **2026-04-01** — `elena.volkov`: Updated patterns observed table. Added Workato/Tray/Boomi competitor breakdown.
> **2026-03-22** — `elena.volkov`: Added the Free downgrade gap TODO.
> **2025-12-04** — `rajiv.patel`: Added the "ghost pattern" FAQ entry after we had three of those in November.
> **2025-09-15** — `elena.volkov`: Initial version.
