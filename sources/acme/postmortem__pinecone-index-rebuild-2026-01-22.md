---
title: "Postmortem — Pinecone index rebuild 2026-01-22"
source_url: "internal://acme/postmortem/pinecone-rebuild-2026-01-22"
license: "synthetic-demo"
attribution: "Acme Inc Engineering Postmortem (synthetic demo). Lead: Hannah Miles (Sr Eng)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — Pinecone index rebuild 2026-01-22

**Status**: Completed
**Date**: 2026-01-22
**Incident Lead**: @hannah.miles
**Participants**: @tomas.vega, @david.kim, @dan.lee
**Severity**: SEV-2 (AI Workflow Assistant offline for 4 hours)

## Summary
On 2026-01-22, the AI Workflow Assistant (Beta) became unresponsive for all users. The root cause was a Pinecone index failure triggered by an unvalidated metadata schema change during a bulk ingestion for a new Business-tier customer (`cust_000412`, Drag Industries). The ingestion pipeline attempted to write nested JSON objects into the vector metadata, which violated Pinecone’s flatness requirements and exceeded the 40KB metadata limit per vector. This caused the index to enter a "Degraded" state, eventually requiring a full teardown and rebuild from the Snowflake/BigQuery source.

## Timeline (All times UTC)
- **14:10**: Bulk ingestion started for `cust_000412` as part of their initial onboarding.
- **14:22**: Pinecone index `workflow-embeddings-v2` begins reporting 5xx errors on upsert.
- **14:45**: First customer report from `cust_000412` via Intercom: "AI assistant is returning 'Internal Server Error' on every prompt."
- **14:55**: @hannah.miles paged by Support. Incident declared.
- **15:10**: Investigation reveals the index is in a `TERMINATING_STATE` due to an unrecoverable metadata validation error during the background indexing job.
- **15:30**: Decision made to wipe the index and rebuild from the `fact_workflow_runs` and `dim_templates` source tables.
- **18:45**: Index rebuild complete. AI features restored.
- **19:00**: Incident closed.

## Detection
The incident was detected via a support ticket from **Drag Industries** (`cust_000412`). While our Datadog monitors showed a spike in 5xx errors for the `ai-gateway` service, the alerting threshold was set too high (10% error rate over 5 minutes) to trigger an immediate page, as the AI features are currently in Beta. 

See `slack__engineering__pinecone-latency-p99-spike.md` for the initial discussion on latency trends that preceded the total failure.

## Root Cause
The `ingest-embeddings` worker did not enforce a flat schema for vector metadata. When `cust_000412` synced their custom workflow definitions, several steps contained deeply nested JSON configurations (specifically around their SAP integration). 

1. **Metadata Nesting**: Pinecone requires metadata to be a flat key-value pair of strings, numbers, or booleans. The worker passed a raw JSON blob from the `step_configuration` column.
2. **Size Limit**: The nested blob for three specific workflows exceeded 40KB. 
3. **Index Corruption**: The combination of the size violation and the nesting caused the Pinecone control plane to stall the index during a compaction cycle, leading to the degraded state.

## Impact
- **Product**: The "AI Workflow Assistant" was completely offline for all Pro, Business, and Enterprise customers.
- **Customers**: ~120 active users attempted to use the assistant during the window and received errors.
- **Onboarding**: Drag Industries (`cust_000412`) had a poor Day 1 experience, requiring a high-touch sync with @marco.chen to explain the outage.

## Resolution
We performed a hard reset of the Pinecone index. Because we do not yet have a "Blue/Green" index deployment strategy for the AI features, this necessitated a 4-hour downtime while the embeddings were re-generated and re-indexed from the BigQuery source.

## Lessons Learned
- **Beta features need production-grade alerts**: We treated the AI gateway as a "best effort" service. As we move toward the $59 Pro price increase in `notion__pricing-tiers.md`, these features are becoming core value drivers.
- **Schema validation at the edge**: We cannot trust the product DB to provide "clean" metadata for third-party vector stores.
- **Rebuild time is too high**: 4 hours to rebuild the index is unacceptable for a SEV-2.

## Action Items
1. **Metadata Validator**: Implement a pre-flight validator in the `ingest-embeddings` worker to flatten JSON and truncate to 35KB (safety margin). [Owner: @tomas.vega] — **DONE 2026-01-25**
2. **Index Versioning**: Implement a Blue/Green indexing strategy so we can cut back to a "Last Known Good" index if a rebuild is triggered. [Owner: @hannah.miles] — **Target 2026-Q2**
3. **Alerting Refactor**: Lower the PagerDuty threshold for `ai-gateway` 5xx errors to 2% over 2 minutes. [Owner: @david.kim] — **DONE 2026-01-23**
4. **Customer Outreach**: @marco.chen to provide a formal apology and technical summary to the Drag Industries team. [Owner: @marco.chen] — **DONE 2026-01-23**

## Related Docs
- `slack__engineering__pinecone-latency-p99-spike.md`
- `dbt__model__workflow_runs_daily.md` (Source for embedding generation)
- `notion__csm-account-health-runbook.md` (Referenced for Drag Industries outreach)
