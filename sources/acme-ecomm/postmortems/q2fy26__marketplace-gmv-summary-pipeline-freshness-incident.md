---
title: "Postmortem: marketplace_gmv_summary mart freshness delay"
source_url: "internal://acme-ecomm/postmortems/q2fy26__marketplace-gmv-summary-pipeline-freshness-incident"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2025-07-15T12:00:00+00:00'
adapter: postmortem
---

# Incident Postmortem: `marketplace_gmv_summary` Pipeline Freshness Delay (Q2FY26)

**Incident ID:** INC-88231
**Date of Incident:** 2025-06-20
**Author / Owner:** connor.blake (Data Engineer, pipeline/freshness)
**Status:** Resolved / Closed
**Impact Window:** ~14 hours (2025-06-20 02:15 UTC to 2025-06-20 16:30 UTC)

---

## 1. Executive Summary

On the morning of June 20, 2025, during the standard Q2FY26 reporting cycle, the BigQuery derived mart `nexus-analyst-demo.acme_ecomm.marketplace_gmv_summary` failed to update its daily partition by the standard 6:00 AM ET SLA. The table remained ~14 hours stale, reflecting only data through the end of June 19. 

Because of this delay, a small cohort of marketplace analysts and finance team members pulling mid-month numbers for Style, Resold, and Collectibles sub-vertical GMV splits extracted outdated figures for approximately half a business day before the underlying Airflow DAG was successfully restarted and backfilled. No customer-facing site experiences were impacted, and core production transactional databases (`fact_orders`, `fact_traffic_daily`) were entirely unaffected. The root cause was traced to a silent retry-logic bug in the nightly orchestration container that mismanaged transient BigQuery rate-limit exceptions during high-concurrency partition swaps.

---

## 2. Timeline of Events (All Times Eastern ET)

*   **02:15 AM (2025-06-20):** The scheduled nightly Airflow job `dbt_marketplace_marts_nightly` triggers. Upstream base fact tables (`fact_orders`, `fact_marketplace_listings`) complete successfully with no anomalies, continuing the stable operational rhythm we have maintained since carlos.figueroa's promotion to VP Data & Analytics back in March (`assoc_100060`).
*   **02:18 AM:** The task executing `marketplace_gmv_summary` encounters a 429 Too Many Requests error from the BigQuery API slot allocator due to concurrent execution with an ad-hoc query batch kicked off by the analytics engineering pod.
*   **02:22 AM:** The custom retry wrapper catches the exception but evaluates the error signature against a deprecated regex string, incorrectly classifying a resource exhaustion error as a non-retryable fatal schema violation.
*   **02:25 AM:** The Airflow task marks itself as `FAILED`, and the downstream alerting webhook to the `#data-pipeline-alerts` Slack channel fires, though it is briefly buried beneath morning infrastructure noise and automated build notifications.
*   **06:00 AM:** Standard SLA checkpoint. The dashboard consumer views in Compass still display the stale `fiscal_week_ending` partition from the prior cycle. 
*   09:12 AM: amara.shah (Data Analyst, Finance/MBR) files an informal Slack ping in `#data-reliability`: *"Hey team, is marketplace_gmv_summary supposed to be showing Sunday's date for today's MBR prep pull? My Style vs Resold cuts look identical to yesterday's."*
*   **09:45 AM:** connor.blake acknowledges the Slack ping, pulls the orchestration logs, and identifies the failed DAG run.
*   **11:30 AM:** Root cause identified as the retry-logic regex bug in the ingestion wrapper script. A hotfix branch `fix/marketplace-retry-regex` is cut for review.
*   **02:00 PM:** Hotfix merged by wei.hartono (Analytics Engineer) and deployed to the production Airflow environment.
*   **04:30 PM:** Manual backfill execution completes successfully. `marketplace_gmv_summary` is fully refreshed with fresh partitions, verified by amara.shah, and the incident is closed.

---

## 3. Root Cause Analysis

The incident was driven by ordinary data-engineering technical debt colliding with a peak concurrency window in the BigQuery warehouse:

1.  **Retry-Logic Defect:** The Python wrapper handling BigQuery API calls relied on an exception-matching list written during the initial flat-dataset migration (when we unified everything under `nexus-analyst-demo.acme_ecomm`). A minor schema refactoring in May left behind an unhandled exception subclass string for API concurrency limits.
2.  **Alerting Visibility:** While the Slack notification fired, our current alerting configuration sends raw task IDs without contextual impact mapping (e.g., whether the failed table is a high-priority board source like `marketplace_gmv_summary` or a light-vertical supporting view). This allowed the failure to sit unacknowledged for several hours until an analyst actively attempted to query the table.

---

## 4. Corrective Actions & Action Items

| ID | Action Item | Owner | Target Date | Status |
|---|---|---|---|---|
| AI-01 | Update BigQuery client wrapper exception-matching regex to catch all transient 429/503 resource exhaustion codes universally. | connor.blake | 2025-07-05 | Completed |
| AI-02 | Implement priority tags on Airflow DAG tasks so board-source marts (`marketplace_gmv_summary`, `traffic_conversion_summary`) trigger high-urgency Paging/Slack alerts. | wei.hartono | 2025-07-18 | In Progress |
| AI-03 | Add automated freshness tests in dbt (`dbt-expectations` freshness macro) to fail silently running dashboards or flag stale states directly in Compass UI caching layers. | connor.blake | 2025-08-01 | Backlogged |

---

## 5. Side Notes & Tangential Chatter (Internal Slack Excerpts)

*   *connor.blake*: "Man, I swear BigQuery slots have been acting squirrelly ever since the finance team started running those massive multi-year CLTV JOIN queries without partitions. We should really remind everyone about the `member_cltv` join traps we documented back in March when amara fixed those nested paths."
*   *wei.hartono*: "Agreed, but let's make sure we finish the Looker-to-Compass migration tasks first before we touch the ingestion wrappers again. I'm still getting pinged by people looking at the Compass dashboard PDT showing old Q4 numbers."
*   *amara.shah*: "All good on my end now, got the fresh cuts for Style and Resold just in time for the afternoon sync with victor.okonkwo. Thanks for the quick fix!"
