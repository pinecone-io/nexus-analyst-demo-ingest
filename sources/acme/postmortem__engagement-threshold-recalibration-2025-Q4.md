---
title: "Postmortem — Engagement threshold recalibration (2025-Q4)"
source_url: "internal://acme/postmortem/2025-q4-engagement-recalibration"
license: "synthetic-demo"
attribution: "Acme Inc internal postmortem-style review (synthetic demo). Author: Marco Chen, reviewed by Elena Volkov."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — Engagement threshold recalibration (2025-Q4)

**Authors**: @marco.chen (Sr CSM), reviewed by @elena.volkov (VP CS)
**Date**: 2025-12-12
**Type**: process review (not an incident — a metric-design recalibration)

## Summary

In Q3 2025, we observed an unusually high churn rate among Business-tier customers who had been classified as "engaged" by our engaged-customer thresholds (≥3 active users, ≥10 successful workflow runs, in 28d). 11 of 142 churned customers were "engaged" at time of churn — an 8% rate, vs the pre-2025-Q3 baseline of ~3%.

This review investigated whether the thresholds had become poorly calibrated.

## Findings

1. **Original threshold logistic regression** (run 2024-Q3) was trained on 2023 + early-2024 data when the average paid customer had 18 seats and ~150 runs/month. The engaged threshold (3 users / 10 runs) caught the bottom-quartile of engagement — was a strong negative signal of churn.

2. **By 2025-Q3, the average paid customer had 47 seats and ~620 runs/month.** The "engaged" threshold became too easy to clear. A customer with 4 active users and 12 runs in 28 days was technically "engaged" by the rule but might be using only ~3% of their paid capacity.

3. **Churn correlation with the rule had weakened.** Renewal probability for "engaged" customers was 88% in 2025-Q3 (down from 92% in 2024). For "not engaged" customers it remained ~70%.

## Decision

After review, we decided NOT to change the engaged-customer thresholds.

Reasoning:
- The engaged flag is a **floor** ("are they at least using the product at all?") not a **ceiling** ("are they getting healthy value?"). The seat-utilization metric is what catches the under-utilization-but-technically-engaged scenarios.
- Changing the thresholds would mark a much larger fraction of customers as "at risk" — overwhelming CSM bandwidth without correspondingly improving renewal predictions.
- The right fix is a separate, more nuanced "value realization score" model (in scoping for 2026-H1).

## Action items

| # | Action | Owner | Due | Status |
|---|---|---|---|---|
| 1 | Maintain engaged-customer thresholds at 3 users / 10 runs / 28d | — | — | retained |
| 2 | Continue surfacing seat-utilization band as the secondary signal | — | — | retained |
| 3 | Scope a "value realization score" model for 2026-H1 | Dan Lee + Elena Volkov | 2026-04-30 | in progress |
| 4 | Re-review engagement thresholds in 2026-Q3 | Marco Chen | 2026-Q3 | pending |

## Why we documented this

So future debates about "should we tighten the engagement bar?" reference this analysis and don't relitigate the decision without new evidence.

## Related

- `glossary__engaged_customer.md`
- `glossary__seat_utilization.md`
- `notion__csm-account-health-runbook.md`
- `dbt__model__account_health.md`
