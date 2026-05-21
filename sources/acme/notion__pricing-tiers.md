---
title: "Notion runbook — Pricing tiers (with comments thread + drift)"
source_url: "internal://acme/notion/pricing-tiers"
license: "synthetic-demo"
attribution: "Acme Inc Notion runbook (synthetic demo). Owner: Pricing Committee (rotating chair)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# Pricing tiers — internal reference

> **Last edited**: Dan Lee, 2026-04-01
> **Last reviewed by committee**: 2026-04-01
> **Next review**: 2026-07-01
> **Owner**: Pricing Committee. Current chair: Dan Lee. Rotates quarterly.
> **Stakeholders**: Sales, CS, Marketing, FP&A, Product
>
> 🚧 `// TODO: pre-2024 grandfather table moved to a new sub-page that nobody reads — should consolidate. -dan`

This is the canonical internal reference for Acme's plan pricing, limits, and what's included where. **Don't rely on memory or older Slack threads — pricing has moved.** When in doubt, this doc wins.

⚠️ **Heads up**: there's an in-progress price change for **Pro** (rising $49 → $59 effective 2026-06-15 for new customers). See "Pricing change history" at bottom.

## At-a-glance

| Plan | Price (USD) | Min seats | Run quota / month | Storage | SLA |
|---|---|---|---|---|---|
| **Free** | $0 | 1 | 100 runs | 1 GB | None |
| **Pro** | $49 / seat / month *(→ $59 on 2026-06-15 for new customers)* | 1 | 10,000 runs | 10 GB | 99.5% |
| **Business** | $149 / seat / month | 50 | 100,000 runs | 100 GB | 99.9% |
| **Enterprise** | Custom (typical $50K-$500K ACV) | 250 | Unlimited | 1 TB | 99.95% + custom |

> **Inline comment from rachel.stein** (2026-04-02): the storage column is approximate. Actual storage is per-workflow-run logs + audit trail. We don't actually enforce storage caps because nobody has come close. If we ever do enforce, this column needs updating.

> **Inline comment from elena.volkov** (2026-04-02): also "Free run quota" is technically per-account not per-workflow. If a Free customer has 10 workflows running, they share the 100 quota. This often confuses Free users. Should we clarify in customer-facing comms? See thread: #pricing-discuss 2026-04-02

## Feature matrix

|   | Free | Pro | Business | Enterprise |
|---|---|---|---|---|
| All integrations | ✅ | ✅ | ✅ | ✅ |
| Workflow templates library | ✅ | ✅ | ✅ | ✅ |
| Email support | — | ✅ | ✅ | ✅ |
| Live chat support | — | — | ✅ | ✅ |
| Dedicated CSM | — | — | — | ✅ |
| SSO (SAML/OIDC) | — | — | ✅ | ✅ |
| Google OAuth login | ✅ | ✅ | ✅ | ✅ |
| Audit log (90 days) | — | — | ✅ | — |
| Audit log (unlimited) | — | — | — | ✅ |
| RBAC | — | — | basic | advanced |
| SCIM provisioning | — | — | — | ✅ |
| AI Workflow Assistant | — | beta | beta | beta |
| Custom workflows runbook review | — | — | — | ✅ |
| Custom contract terms | — | — | — | ✅ |
| Multi-region deployment | — | — | — | ✅ |
| PII scrubbing flag (per-step) | ❓ ([NEEDS UPDATE](#)) | shipped 2026-04-30 | shipped 2026-04-30 | shipped 2026-04-30 |

> 🚧 `// TODO: confirm with @hannah.miles whether PII scrubbing flag is on Free or just Pro+. she said "all paid" but did she include Free? -dan`

## Pricing change history

| Date | Change |
|---|---|
| 2024-Q1 | Launched Free + Pro ($39) + Business ($129) + Enterprise (custom) |
| 2024-Q4 | Pro raised $39 → $49, Business raised $129 → $149 (new customers) |
| 2025-Q3 | Added 1-year and 2-year multi-year discount (5% / 8%) |
| **2026-Q2 (planned)** | Pro raises $49 → $59 effective 2026-06-15 (new customers; 12-month grandfather) |

> **Note**: There's also a draft proposal to introduce a new tier between Pro and Business called "Team" priced at ~$89/seat/month with a 10-seat minimum. Not approved yet, see RFC in #pricing-discuss 2026-03-12. Currently shelved pending Q2 review.

## What gets stored where in the warehouse

- `dim_plans` — current plan limits and prices (slowly changing — assume updated when pricing committee changes anything)
- `dim_customers.current_plan_tier` — convenience field, refreshes nightly. **Don't trust for board reporting** — see `notion__data-warehouse-conventions.md`
- `fact_subscriptions` — source of truth for what plan a customer is on right now (`is_current = TRUE`) and the full historical chain

If you need to know what a customer paid in a given month, sum `fact_invoices.amount_usd` for that customer in that month. If you need to know what they're paying right now, use `fact_subscriptions.mrr_usd` filtered to `is_current = TRUE`.

## Discount approval matrix

| Discount | Approver |
|---|---|
| 0-10% off list | AE |
| 10-20% off list | Sales Manager |
| 20-30% off list | VP Sales (Marcus Webb) |
| >30% off list | CFO (Rachel Stein) |
| Custom packaging (e.g. non-standard seat counts on Business) | CFO |
| Multi-year >2 years | CFO + CEO (Sam Reyes) |

> **Edit log entry — marcus.webb 2026-03-15**: We had three exceptions in Q1 where AEs gave 12-15% discounts without escalating to me. All three closed cleanly so I'm not making a stink, but FYI to AEs reading this — please escalate if >10%.

## Common AE questions

> **Q: Can a customer mix tiers (some Pro seats + some Business seats)?**
> No. Plan applies to whole account.

> **Q: Can we sell Business to a 30-seat customer (below the 50-seat min)?**
> Only with CFO approval. We've made exceptions; see `gong__discovery__cust000412-drag-industries.md` for an example (30-seat custom Business package approved Q2 2026).

> **Q: Does Free count toward ARR?**
> No. ARR explicitly filters out `plan_tier = 'Free'`. See `glossary__arr.md`.

> **Q: What's the difference between "audit log 90 days" on Business and "audit log unlimited" on Enterprise?**
> Business retains audit events for 90 days then deletes. Enterprise retains forever. Some Business customers ask for an extended retention add-on. We don't sell that as a package but Enterprise upgrade is the answer.

> **Q: Does Pro really not include SSO? What about customers who specifically need SAML SSO at <50 seats?**
> Real answer: this is a sales-friction point. We've discussed adding SAML to Pro for years. Currently the answer is "they need Business OR they can use Google OAuth login (which is on Pro)." If a customer specifically needs SAML at small scale, escalate to Marcus — he can sometimes negotiate a custom package.
> 🚧 `// TODO: schedule a sales-team retro on this. half the customers we lose to competitors at 5-30 seats lose us specifically because of SAML on Pro. -marcus 2026-04-08`

## Comments / change history (Notion footer)

> **2026-04-15** — `dan.lee`: Updated PII scrubbing entry. Confirmed Pro+ only after talking to Hannah.
>
> **2026-04-02** — `elena.volkov`: Added clarifier about Free quota being per-account.
>
> **2026-04-02** — `rachel.stein`: Storage column note — we don't actually enforce.
>
> **2026-04-01** — `dan.lee`: Added 2026-Q2 Pro $49→$59 change to history.
>
> **2026-03-15** — `marcus.webb`: Discount approval matrix updated, added Q1 exception note.
>
> **2025-12-12** — `rachel.stein`: Added multi-year discount section (5% 1-year, 8% 2-year). Also moved old grandfather table to a sub-page.
>
> **2025-09-04** — `dan.lee`: Initial committee-owned version. Replaces the previous Google Doc.

## Drafts / WIP / out-of-scope (do not use yet)

> **Draft**: a proposed "Solo" tier at $19/month for individual builders. Out of scope per CEO 2026-03 — we're not chasing the consumer / single-user market. Keeping the draft here in case the conversation reopens.

> **Draft**: usage-based pricing model (charge per workflow run above quota). Discussed in Q4 2025 product offsite. Decision: NO. PLG simplicity wins.
