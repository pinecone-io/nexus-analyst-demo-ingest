---
title: "Notion runbook — Enterprise POC playbook (with field anecdotes)"
source_url: "internal://acme/notion/enterprise-poc-playbook"
license: "synthetic-demo"
attribution: "Acme Inc Notion runbook (synthetic demo). Owner: VP Sales (Marcus Webb)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Enterprise POC playbook

> **Last reviewed**: 2026-01-15 by marcus.webb
> **Owner**: Marcus Webb (VP Sales)
> **Audience**: Enterprise AEs (emp_2xx series), Sales Engineers, Solution Architects
>
> 🚧 `// TODO: revisit the "When NOT to offer a POC" section after Q1 — we lost 2 deals last quarter where we should have offered a POC and didn't, in retrospect. -marcus 2026-04-08`

POCs are how we win Enterprise deals against incumbents (Workato, Tray, Boomi). This playbook codifies what we offer, how we run it, and what counts as a successful POC.

## What we offer

- **Length**: 60 days, extendable once by 30 days with VP Sales approval
- **Cost to customer**: $0 (Acme bears the cost — software + SA hours)
- **Acme staffing**: 1 Solution Architect (~10h/week) + AE light-touch + 1 SE for product Q&A
- **Customer staffing required**: At least 1 technical builder, ideally 2-3 stakeholders across functions

> **Note**: We've experimented with paid POCs ($10K) for very large prospects (>$200K ACV) but it doesn't work — prospects feel they're paying to evaluate, which kills momentum. Reverted to free POCs in Q3 2025. Don't bring back unless explicitly approved.

## When to offer a POC

- Deal size $100K+ ACV (smaller deals don't justify the SA cost)
- Customer is genuinely evaluating (not just kicking tires) — they've done discovery, named specific use cases, and have a budget approved
- Active competitor in play (Workato, Tray, Boomi, n8n self-hosted)
- POC is gated on a clear "if we deliver X, you'll buy" commitment

## When NOT to offer a POC

- Customer is happy in trial / Pro and just needs a Business upgrade
- Free or self-serve trial would suffice
- Deal is below $100K and no clear strategic reason
- Customer can't articulate success criteria
- Customer has a history of running POCs with multiple vendors and not buying (we've had 2 of these — see "Prospect blocklist" sub-page if you have access)

> **Field note from sarah.lopez (2026-04-08)**: I had a deal in Q1 where I declined a POC because it was a Mid-Market account ($65K ACV) — they ended up going with a competitor specifically because the competitor offered a POC. Should I have escalated? Maybe. Adding this as data point for the playbook revision.

> **Field note from ben.cohen (2026-03-18)**: For Nimbus Finance (`gong__discovery__nimbus-finance.md`), the POC structure was slightly modified — they wanted us to migrate 5 specific Workato workflows AS the POC scope rather than freestyle building. Worked well, faster eval, clearer success criteria. Worth considering as a "migration POC" pattern when the prospect is replacing an incumbent.

## POC structure

### Week 0 — kickoff

- Lock the **success criteria** in writing (success doc — email or PDF). Examples:
  - "Replicate Workato workflow X in Acme. Within 5% latency. Run for 14 days at production volume without errors."
  - "Demonstrate Salesforce-CPQ integration depth equivalent to or better than Workato's."
- Identify **technical champion** on customer side. SA pairs with them.
- Set check-in cadence (weekly is standard).

### Weeks 1-4 — build

- SA pairs with customer technical champion to build the POC workflows.
- AE absent unless escalation.
- Weekly written status update from SA → customer + AE.

### Weeks 5-8 — production-mirror run

- POC workflows run against production-mirror data (or production with appropriate gating).
- Monitor success rate, latency, error codes.
- Customer evaluates against success criteria.

### Week 8-9 — wrap

- Joint review meeting (SA + AE + champion + customer's decision-maker).
- Walk through results vs success criteria.
- AE pivots to commercial conversation. Quote within 5 business days.

> **Pro tip**: At the kickoff, also identify the "anti-champion" — the person on the customer side most likely to push back or sabotage the deal. Usually procurement or a competing-vendor advocate. SA should plan how to engage them constructively. Half the failed POCs I've seen failed because the anti-champion was ignored. -marcus

## Sales-cycle metrics

Track the following in CRM for every POC:

- POC start date
- Success criteria locked (yes/no)
- Champion identified (yes/no)
- Quote sent date
- Closed date (won or lost)
- Loss reason (if lost) — we strongly want to capture this

## What goes in the warehouse

POCs themselves don't have a fact table, but their outcomes show up in:

- `fact_opportunities` — every POC should be a `Qualified` or `Proposal` stage opp with `amount_usd` set to the forecast ACV. When closed, transitions to `Closed_Won` (with `customer_id` populated) or `Closed_Lost` (with `loss_reason` populated).
- `dim_employees.role` — Solution Architects are roled as `Sales Engineer` (we don't have a separate SA role yet).

> 🚧 `// TODO: split SA from SE in dim_employees. they're different roles, the conflation muddies our analytics on POC win rate by SA. -jorge.martinez 2026-02-15`

## Win-rate target

We track POC win rate quarterly. Current target: ≥ 60%. Q1 2026: 64% (29 POCs run, 18 won).

| Quarter | POCs run | Won | Win rate |
|---|---|---|---|
| Q1 2026 | 29 | 18 | 64% |
| Q4 2025 | 24 | 15 | 63% |
| Q3 2025 | 21 | 14 | 67% |
| Q2 2025 | 18 | 11 | 61% |

## Loss-reason taxonomy

When a POC loses, AE must capture one of:

| Reason | Definition |
|---|---|
| `competitor` | Customer chose another vendor |
| `price` | Acme deemed too expensive (vs willingness to pay) |
| `feature_gap` | Specific missing feature was the deciding factor |
| `no_decision` | Customer decided to defer / not buy |
| `timing` | Customer had budget freeze / leadership change |

These map directly to `fact_opportunities.loss_reason`.

> **Field reflection**: Looking at our Q1 losses, `competitor` was 6 of 11 losses, mostly to Workato. `feature_gap` was 3 of 11 — and 2 of those mentioned Salesforce CPQ depth, which is now an active product priority (`CPQ-DEEP-2026`). Pattern recognition is working.

## Drafts / WIP

> **Draft**: a "POC retrospective" template — to be filled out within 2 weeks of every POC closure (won or lost). Currently informal; want to formalize.

> **Draft**: paid SA hours add-on for prospects who want extended POC support beyond the 60+30 day standard. Considered but not approved — adds friction to deals.

## Comment thread

> **2026-04-08** — `marcus.webb`: Added field notes from Sarah and Ben. Will revisit "When NOT to offer" criteria.
> **2026-03-18** — `ben.cohen`: Suggested "migration POC" pattern.
> **2026-02-15** — `jorge.martinez`: SA/SE conflation TODO.
> **2026-01-15** — `marcus.webb`: Quarterly review, no major changes.

## Related

- `gong__discovery__nimbus-finance.md` — example of a discovery → POC pitch
- `gong__churn-call__cust000287-beacon-studios.md` — example of `competitor` loss reason
- `notion__pricing-tiers.md` — discount approval matrix
