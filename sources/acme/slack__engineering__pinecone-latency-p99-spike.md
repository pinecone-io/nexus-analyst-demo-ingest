---
title: "Slack #engineering — Pinecone p99 latency spike 2026-03-19"
source_url: "internal://acme/slack/engineering/pinecone-latency-spike-2026-03-19"
license: "synthetic-demo"
attribution: "Acme Inc Slack archives (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

# #engineering — Pinecone p99 latency spike 2026-03-19

**hannah.miles** [2026-03-19 14:12:00 UTC]
🚨 Heads up @on-call — seeing a massive spike in Pinecone p99 query latency on the `prod-v2` index. We’re jumping from a baseline of ~80ms to 340ms+ in the last 20 minutes. 

**hannah.miles** [2026-03-19 14:14:10 UTC]
It’s impacting the AI Workflow Assistant beta. Users are seeing "Step Timeout" errors in `fact_workflow_runs`.

**priya.anand** [2026-03-19 14:16:22 UTC]
@hannah.miles looking now. Is this isolated to a specific pod or global across the index?

**hannah.miles** [2026-03-19 14:18:45 UTC]
Looks global. I’m seeing the latency across all query nodes. Checking the Datadog dashboard for `pinecone.query.latency.p99`.

**tomas.vega** [2026-03-19 14:22:15 UTC]
I’m seeing a corresponding spike in `billing_api` calls for vector storage lookups. @hannah.miles, could this be a specific customer hitting a high-cardinality metadata filter?

**hannah.miles** [2026-03-19 14:25:30 UTC]
Good catch @tomas.vega. Just pulled the logs. `cust_000512` (Vandelay Industries, new Enterprise pilot) is running a workflow that filters on `metadata.source_file_id` where they have ~200k unique values. Pinecone is struggling with the scan.

**priya.anand** [2026-03-19 14:27:05 UTC]
That’ll do it. We don’t have a selective index on that metadata key yet. Who is the CSM for `cust_000512`?

**tomas.vega** [2026-03-19 14:29:12 UTC]
Checking `dim_customers`... looks like @marco.chen owns that account.

**hannah.miles** [2026-03-19 14:32:44 UTC]
I’m going to apply a temporary index hint to the query service to force a more efficient scan, but we really need to re-index with `source_file_id` as a selective field. 

**priya.anand** [2026-03-19 14:35:10 UTC]
@hannah.miles do the hint now to stabilize p99s. @tomas.vega can you check if this usage is going to blow out their pilot credit limit? 340ms queries are expensive on our current Pinecone tier.

**tomas.vega** [2026-03-19 14:38:55 UTC]
They’ve consumed about 40% of their monthly vector-compute quota in the last hour. If this keeps up, they’ll hit the hard cap by EOD.

**hannah.miles** [2026-03-19 14:45:20 UTC]
Hint applied. p99 is dropping back to ~110ms. Still higher than baseline but the timeouts in `fact_workflow_runs` have stopped. 

**marco.chen** [2026-03-19 14:50:05 UTC]
Just saw the alerts. I’m on with the customer now. They were trying to run a bulk migration of their Notion docs into the vector store. I’ve asked them to pause the workflow until we can optimize the index.

**priya.anand** [2026-03-19 14:55:30 UTC]
Thanks @marco.chen. @hannah.miles let's schedule the re-indexing for 22:00 UTC tonight. We should also add a check in the AI Assistant code to warn users when they use high-cardinality metadata filters without an index. 

**hannah.miles** [2026-03-19 15:02:12 UTC]
Copy that. I'll draft the ticket for the index update. 
✅ *Reaction: :white_check_mark: (priya.anand)*
