---
title: "Zendesk ticket export — 2025-2026 (raw CSV-style dump)"
source_url: "internal://acme/zendesk-ticket-export-2025-2026"
license: "synthetic-demo"
attribution: "Synthetic content, Acme Inc internal demo. Acme Inc is a fictitious company."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: notion_runbook
---

# ZENDESK SYSTEM EXPORT: TICKETS_RAW_DUMP_2025_2026
# Export Parameters: All tickets created >= 2025-01-01; Format: PIPE_DELIMITED; Encoding: UTF-8
# Note: Internal notes are appended to the 'notes' column. Some truncation may occur in legacy view.

ticket_id | customer_id | company | opened | closed | priority | category | channel | csat | resolution_hrs | assigned_to | status | notes
TK-10042 | cust_000700 | Cobalt Systems | 2025-01-02 09:12:33 | 2025-01-02 14:20:11 | P3 | billing | email | 5 | 5.1 | emp_081 | resolved | Customer requested change of billing email to ap@cobaltsys.com. Updated in Stripe and internal CRM.
TK-10043 | cust_000702 | Driftwood Media | 2025-01-02 10:45:01 | 2025-01-03 09:00:00 | P4 | auth | web | 4 | 22.2 | emp_080 | resolved | Forgot password loop. User error; sent manual reset link.
TK-10044 | cust_000704 | Onyx Robotics | 2025-01-03 14:22:10 | 2025-01-03 15:45:22 | P1 | integration | api | 5 | 1.4 | emp_085 | resolved | [URGENT] Salesforce integration returning AUTH_FAILED for all write-back jobs. Found expired OAuth token on customer side. Refreshed.
TK-10045 | cust_000701 | Marigold Health | 2025-01-04 08:30:00 | 2025-01-06 11:20:00 | P2 | sso | email | | 74.8 | emp_088 | resolved | SAML cert update. Coordination with their IT team (Theo Novak) took longer than expected. Escalated to Olivia Tran (CSM) to confirm metadata.
TK-10046 | cust_000708 | Kestrel Networks | 2025-01-05 11:00:12 | 2025-01-05 12:30:45 | P3 | onboarding | chat | 3 | 1.5 | emp_082 | resolved | User asked how to set up their first webhook. Provided docs. Customer seems frustrated with the UI lag.
TK-10047 | cust_000713 | Harbor Dynamics | 2025-01-05 16:45:00 | 2025-01-06 10:00:00 | P2 | runs | web | | 17.2 | emp_085 | resolved | Multiple workflow runs failing with STEP_TIMEOUT. Investigated; the target API (Jira) was responding slowly. Added retry logic with backoff.
TK-10048 | cust_000704 | Onyx Robotics | 2025-01-07 09:00:00 | 2025-01-07 10:15:00 | P4 | billing | email | 5 | 1.2 | emp_081 | resolved | Requesting W-9 for FY25. Sent.
TK-10049 | cust_000705 | Pebble Digital | 2025-01-08 13:00:00 | 2025-01-10 14:00:00 | P3 | performance | email | 2 | 49.0 | emp_083 | resolved | "App is slow." Vague report. No specific workflow IDs provided. Customer CSAT 2 given because 'it took too long to ask for more info'.
TK-10050 | cust_000710 | Sable Analytics | 2025-01-11 10:20:33 | 2025-01-11 11:00:00 | P4 | auth | web | | 0.7 | emp_080 | resolved | Access request for new user. 
TK-10051 | cust_000287 | Beacon Studios | 2025-01-12 14:00:00 | 2025-01-12 15:30:00 | P3 | data-sync | email | 5 | 1.5 | emp_084 | resolved | Sync delay between Acme and BigQuery. Small lag due to worker node restart. Resolved.
TK-10052 | cust_000701 | Marigold Health | 2025-01-14 09:15:00 | | P2 | integration | web | | | emp_085 | escalated | Postgres connector not honoring schema mapping for 'jsonb' columns. Moving to engineering (Priya's team).
TK-10053 | cust_000704 | Onyx Robotics | 2025-01-15 11:30:00 | 2025-01-15 11:45:00 | P4 | billing | email | | 0.2 | emp_081 | resolved | Copy of December invoice. Sent.
TK-10054 | cust_000709 | Willow Works | 2025-01-16 16:00:00 | 2025-01-17 09:00:00 | P3 | runs | email | 4 | 17.0 | emp_082 | resolved | Workflow failed with RATE_LIMITED. Customer was hitting Shopify API limits. Advised on batching.
TK-10055 | cust_000711 | Ember Industries | 2025-01-18 10:00:00 | 2025-01-20 14:00:00 | P2 | sso | chat | | 52.0 | emp_088 | resolved | Azure AD provisioning issues. Some users not appearing in Acme. Fixed mapping in SCIM settings.
TK-10056 | cust_000708 | Kestrel Networks | 2025-01-19 13:45:00 | 2025-01-20 09:30:00 | P3 | performance | web | | 19.7 | emp_086 | resolved | Dashboard loading time > 5 seconds. Internal Note: Account is using 70 seats on a Business plan but has extremely complex canvas.
TK-10057 | cust_000703 | Yarrow Logistics | 2025-01-21 08:12:00 | 2025-01-21 08:30:00 | P4 | auth | email | 5 | 0.3 | emp_080 | resolved | Locked out after too many attempts. Reset.
TK-10058 | cust_000706 | Tamarind Group | 2025-01-22 15:20:00 | 2025-01-23 11:00:00 | P3 | onboarding | chat | 4 | 19.6 | emp_082 | resolved | "How do I use the NetSuite connector?" Sent guide and scheduled 15m with CSM (Marco Silva).
TK-10059 | cust_000701 | Marigold Health | 2025-01-24 10:00:00 | 2025-01-24 10:30:00 | P1 | performance | web | 5 | 0.5 | emp_085 | resolved | [INTERNAL EMERGENCY] Site 503 for this specific tenant. Database lock issue. Restarted pod. resolved quickly.
TK-10060 | cust_000707 | Verdant Cloud | 2025-01-25 11:00:00 | 2025-01-26 14:00:00 | P2 | integration | email | | 27.0 | emp_084 | resolved | Hubspot sync failing. AUTH_FAILED error. Customer had revoked Acme's app access in Hubspot by mistake.
TK-10061 | cust_000704 | Onyx Robotics | 2025-01-28 09:00:00 | 2025-01-28 09:15:00 | P4 | billing | email | 5 | 0.2 | emp_081 | resolved | Change of address for FY25 taxes.
TK-10062 | cust_000700 | Cobalt Systems | 2025-01-30 14:30:00 | 2025-01-30 16:00:00 | P3 | runs | web | 5 | 1.5 | emp_085 | resolved | Error code SCHEMA_MISMATCH on payload. Explained that the source JSON changed.
TK-10063 | cust_000704 | Onyx Robotics | 2025-02-01 10:00:00 | 2025-02-04 10:00:00 | P1 | integration | email | 1 | 72.0 | emp_085 | resolved | CRITICAL: All runs for Onyx production pipeline failing. AUTH_FAILED on internal proxy. Resolution took 3 days due to timezone mismatch with their lead dev. Internal Note: Flagged as at_risk per account_health rules (P1 > 48h).
TK-10064 | cust_000704 | Onyx Robotics | 2025-02-01 11:00:00 | 2025-02-04 10:05:00 | P1 | integration | chat | | 71.1 | emp_085 | closed | DUPLICATE of TK-10063.
TK-10065 | cust_000704 | Onyx Robotics | 2025-02-02 09:00:00 | 2025-02-04 10:05:00 | P1 | sso | email | | 49.1 | emp_088 | closed | DUPLICATE of TK-10063 (Customer spamming channels).
TK-10066 | cust_000708 | Kestrel Networks | 2025-02-05 15:00:00 | 2025-02-05 16:30:00 | P3 | performance | email | 2 | 1.5 | emp_086 | resolved | Sluggish workflow canvas. Customer says "For $10k/mo I expect better perf."
TK-10067 | cust_000714 | Quartz Foundry | 2025-02-07 10:00:00 | 2025-02-07 14:00:00 | P2 | data-sync | email | 5 | 4.0 | emp_084 | resolved | BigQuery destination failing with NULL_PAYLOAD. Customer had an empty column in source CSV. 
TK-10068 | cust_000700 | Cobalt Systems | 2025-02-09 11:15:00 | 2025-02-09 12:00:00 | P4 | billing | email | | 0.7 | emp_081 | resolved | Invoice inquiry.
TK-10069 | cust_000702 | Driftwood Media | 2025-02-11 13:00:00 | 2025-02-12 09:00:00 | P3 | runs | web | 5 | 20.0 | emp_082 | resolved | Workflow not firing on webhook. Testing showed the webhook URL was truncated in their system.
TK-10070 | cust_000713 | Harbor Dynamics | 2025-02-13 16:00:00 | 2025-02-13 16:45:00 | P4 | auth | chat | | 0.7 | emp_080 | resolved | Password reset.
TK-10071 | cust_000703 | Yarrow Logistics | 2025-02-15 10:00:00 | 2025-02-15 11:00:00 | P2 | runs | api | 5 | 1.0 | emp_085 | resolved | High error rate (RATE_LIMITED). Advised on increasing the delay between steps.
TK-10072 | cust_000706 | Tamarind Group | 2025-02-17 14:00:00 | 2025-02-18 10:00:00 | P3 | data-sync | email | 3 | 20.0 | emp_084 | resolved | Data not appearing in Looker. Acme was pushing to the wrong schema.
TK-10073 | cust_000704 | Onyx Robotics | 2025-02-19 09:00:00 | 2025-02-19 14:00:00 | P2 | integration | email | | 5.0 | emp_085 | resolved | Snowflake connector auth issues.
TK-10074 | cust_000701 | Marigold Health | 2025-02-20 11:00:00 | 2025-02-21 15:00:00 | P3 | onboarding | web | | 28.0 | emp_082 | resolved | New team member needs training on the logic builder. Pointed to Acme University.
TK-10075 | cust_000711 | Ember Industries | 2025-02-22 13:00:00 | 2025-02-22 14:30:00 | P4 | auth | email | 5 | 1.5 | emp_080 | resolved | New user seat request.
TK-10076 | cust_000700 | Cobalt Systems | 2025-02-24 10:30:00 | 2025-02-24 11:15:00 | P3 | performance | chat | 4 | 0.7 | emp_086 | resolved | UI jitter on Chrome. Suggested clearing cache.
TK-10077 | cust_000708 | Kestrel Networks | 2025-02-26 15:00:00 | 2025-02-27 10:00:00 | P2 | integration | email | 2 | 19.0 | emp_085 | resolved | Salesforce sandbox refresh broke the connection. Note: Customer is really unhappy about the manual effort to reconnect 50 workflows.
TK-10078 | cust_000709 | Willow Works | 2025-02-28 09:00:00 | 2025-03-01 11:00:00 | P3 | billing | email | 4 | 26.0 | emp_081 | resolved | Credit card failed. Updated.
TK-10079 | cust_000714 | Quartz Foundry | 2025-03-02 11:00:00 | 2025-03-02 12:00:00 | P4 | onboarding | web | | 1.0 | emp_082 | resolved | Documentation request for SOC2. Sent to legal.
TK-10080 | cust_000707 | Verdant Cloud | 2025-03-04 14:00:00 | 2025-03-06 10:00:00 | P3 | runs | email | | 44.0 | emp_085 | resolved | "Why did my workflow stop?" Step timeout on a large CSV parsing. Optimized the step.
TK-10081 | cust_000704 | Onyx Robotics | 2025-03-07 09:00:00 | 2025-03-07 10:00:00 | P4 | sso | email | | 1.0 | emp_088 | resolved | Just adding a new SSO admin.
TK-10082 | cust_000703 | Yarrow Logistics | 2025-03-09 13:00:00 | 2025-03-10 15:00:00 | P2 | performance | web | | 26.0 | emp_086 | resolved | 400 errors in the logs. Actually was an INTEGRATION_DOWN on their end (AWS Lambda).
TK-10083 | cust_000700 | Cobalt Systems | 2025-03-12 10:00:00 | 2025-03-12 11:30:00 | P3 | integration | chat | 5 | 1.5 | emp_085 | resolved | Slack notify bot stopped working. Token needed re-auth.
TK-10084 | cust_000712 | Juniper Collective | 2025-03-14 16:00:00 | 2025-03-15 09:00:00 | P4 | billing | email | | 17.0 | emp_081 | resolved | Requesting an itemized receipt.
TK-10085 | cust_000287 | Beacon Studios | 2025-03-16 11:00:00 | 2025-03-16 12:00:00 | P3 | auth | web | 5 | 1.0 | emp_080 | resolved | MFA setup help.
TK-10086 | cust_000705 | Pebble Digital | 2025-03-18 14:00:00 | 2025-03-20 10:00:00 | P3 | onboarding | email | 3 | 44.0 | emp_082 | resolved | How to export data to Google Sheets? Shared integration docs.
TK-10087 | cust_000704 | Onyx Robotics | 2025-03-22 09:12:00 | 2025-03-25 14:00:00 | P1 | runs | api | | 76.8 | emp_085 | resolved | Production outage: All scheduled runs hung in 'pending'. Queue overflow on Acme side. Internal Note: Second P1 over 48h in 60 days. Account is heavily flagged in health model. CSM (Olivia Tran) aware.
TK-10088 | cust_000708 | Kestrel Networks | 2025-03-24 10:00:00 | 2025-03-24 11:30:00 | P3 | billing | email | 1 | 1.5 | emp_081 | resolved | "Stop charging us for inactive seats." Note: Customer is aggressive. Business plan seat minimums explained. CSM (Marco Silva) alerted.
TK-10089 | cust_000701 | Marigold Health | 2025-03-26 15:00:00 | 2025-03-27 10:00:00 | P2 | integration | email | | 19.0 | emp_085 | resolved | FHIR API integration failing on POST. Fixed by adjusting payload headers.
TK-10090 | cust_000711 | Ember Industries | 2025-03-28 13:00:00 | 2025-03-31 09:00:00 | P3 | data-sync | email | 5 | 68.0 | emp_084 | resolved | Sync interval changed from 15m to 1h without notice. Found it was a user setting change on their side.
TK-10091 | cust_000714 | Quartz Foundry | 2025-04-01 10:00:00 | 2025-04-01 12:00:00 | P4 | billing | email | | 2.0 | emp_081 | resolved | Billing contact update.
TK-10092 | cust_000706 | Tamarind Group | 2025-04-03 14:00:00 | 2025-04-05 10:00:00 | P3 | onboarding | web | | 44.0 | emp_082 | resolved | Question about audit logs for SOC2 compliance. Verified Business plan features.
TK-10093 | cust_000713 | Harbor Dynamics | 2025-04-06 09:00:00 | 2025-04-06 10:00:00 | P4 | auth | chat | 5 | 1.0 | emp_080 | resolved | Simple login issue.
TK-10094 | cust_000700 | Cobalt Systems | 2025-04-08 11:00:00 | 2025-04-08 15:00:00 | P2 | runs | api | | 4.0 | emp_085 | resolved | Workflow aborted: STEP_TIMEOUT. The SQL query was too heavy. Advised on indexing.
TK-10095 | cust_000704 | Onyx Robotics | 2025-04-10 13:00:00 | | P3 | performance | web | | | emp_086 | open | "The canvas is lagging when we have more than 50 steps." Ongoing investigation.
TK-10096 | cust_000702 | Driftwood Media | 2025-04-12 10:00:00 | 2025-04-12 11:30:00 | P4 | billing | email | 5 | 1.5 | emp_081 | resolved | Receipt request.
TK-10097 | cust_000710 | Sable Analytics | 2025-04-14 15:00:00 | 2025-04-15 10:00:00 | P3 | sso | email | | 19.0 | emp_088 | resolved | SSO user cannot login. Found duplicate email in Acme system from a previous Free trial. Merged.
TK-10098 | cust_000708 | Kestrel Networks | 2025-04-17 09:00:00 | 2025-04-20 14:00:00 | P2 | integration | email | 1 | 77.0 | emp_085 | resolved | Stripe integration not pulling metadata correctly. Fixed. Internal Note: Customer said "we are evaluating other tools" in this thread. Account status: at_risk.
TK-10099 | cust_000709 | Willow Works | 2025-04-19 11:00:00 | 2025-04-19 12:00:00 | P4 | auth | web | | 1.0 | emp_080 | resolved | Password help.
TK-10100 | cust_000701 | Marigold Health | 2025-04-21 14:00:00 | 2025-04-23 10:00:00 | P3 | performance | email | 4 | 44.0 | emp_086 | resolved | Data export to S3 taking 20 minutes. Optimized file compression.
TK-10101 | cust_000703 | Yarrow Logistics | 2025-04-25 09:00:00 | 2025-04-25 10:00:00 | P4 | onboarding | chat | 5 | 1.0 | emp_082 | resolved | New user guide requested.
TK-10102 | cust_000704 | Onyx Robotics | 2025-04-27 11:00:00 | 2025-04-30 09:00:00 | P2 | runs | api | 2 | 70.0 | emp_085 | resolved | Intermittent AUTH_FAILED on production runs. Internal Note: Found it was a race condition in the Acme auth proxy. Hotfixed. Onyx is NOT happy.
TK-10103 | cust_000714 | Quartz Foundry | 2025-05-02 10:00:00 | 2025-05-02 11:30:00 | P3 | billing | email | | 1.5 | emp_081 | resolved | Tax ID update.
TK-10104 | cust_000707 | Verdant Cloud | 2025-05-04 14:00:00 | 2025-05-06 10:00:00 | P2 | integration | web | | 44.0 | emp_084 | resolved | BigQuery connector failing with "access denied". Verified they didn't have write permissions on the dataset.
TK-10105 | cust_000700 | Cobalt Systems | 2025-05-08 09:00:00 | 2025-05-08 10:00:00 | P4 | auth | email | 5 | 1.0 | emp_080 | resolved | Login issues.
TK-10106 | cust_000713 | Harbor Dynamics | 2025-05-11 11:00:00 | 2025-05-13 14:00:00 | P3 | sso | email | | 51.0 | emp_088 | resolved | Adding new SSO provider (Okta).
TK-10107 | cust_000704 | Onyx Robotics | 2025-05-15 15:00:00 | 2025-05-15 15:30:00 | P4 | billing | email | | 0.5 | emp_081 | resolved | Missing invoice from March. Resent.
TK-10108 | cust_000702 | Driftwood Media | 2025-05-18 10:00:00 | 2025-05-18 11:30:00 | P3 | runs | api | | 1.5 | emp_085 | resolved | "Workflow failed with error code NULL_PAYLOAD." The trigger source was empty.
TK-10109 | cust_000710 | Sable Analytics | 2025-05-20 14:00:00 | 2025-05-22 10:00:00 | P2 | integration | email | 5 | 44.0 | emp_084 | resolved | Salesforce sync lag. Cleared the queue.
TK-10110 | cust_000708 | Kestrel Networks | 2025-05-24 09:00:00 | 2025-05-27 11:00:00 | P3 | performance | email | 2 | 74.0 | emp_086 | resolved | Page load speed issues. Note: Customer is mentioning Acme is "expensive for what it is." Churn risk is rising.
TK-10111 | cust_000709 | Willow Works | 2025-05-28 11:00:00 | 2025-05-28 12:00:00 | P4 | auth | web | | 1.0 | emp_080 | resolved | Password reset.
TK-10112 | cust_000701 | Marigold Health | 2025-06-01 14:00:00 | 2025-06-03 10:00:00 | P3 | onboarding | chat | 5 | 44.0 | emp_082 | resolved | Question about HIPAA compliance settings. Sent whitepaper.
TK-10113 | cust_000703 | Yarrow Logistics | 2025-06-05 09:00:00 | 2025-06-05 10:00:00 | P4 | billing | email | | 1.0 | emp_081 | resolved | Changed credit card.
TK-10114 | cust_000704 | Onyx Robotics | 2025-06-08 11:00:00 | | P1 | performance | api | | | emp_086 | open | [CRITICAL] Data latency > 10 minutes on production flows. Internal Note: Flagged as at_risk. CSM (Olivia Tran) on a call with them now.
TK-10115 | cust_000714 | Quartz Foundry | 2025-06-11 14:00:00 | 2025-06-11 15:30:00 | P3 | auth | web | 5 | 1.5 | emp_080 | resolved | 2FA issues.
TK-10116 | cust_000707 | Verdant Cloud | 2025-06-14 10:00:00 | 2025-06-14 11:30:00 | P4 | billing | email | | 1.5 | emp_081 | resolved | Update billing address.
TK-10117 | cust_000700 | Cobalt Systems | 2025-06-17 15:00:00 | 2025-06-19 10:00:00 | P2 | runs | email | | 43.0 | emp_085 | resolved | Step timeout on an HTTP request. Increased timeout to 60s.
TK-10118 | cust_000713 | Harbor Dynamics | 2025-06-20 09:00:00 | 2025-06-21 14:00:00 | P3 | integration | chat | 4 | 29.0 | emp_084 | resolved | Netsuite auth expiring too quickly. Investigated OAuth scope.
TK-10119 | cust_000704 | Onyx Robotics | 2025-06-24 11:00:00 | 2025-06-25 15:00:00 | P2 | sso | email | | 28.0 | emp_088 | resolved | Syncing new group from Okta.
TK-10120 | cust_000702 | Driftwood Media | 2025-06-27 14:00:00 | 2025-06-27 15:30:00 | P4 | onboarding | web | | 1.5 | emp_082 | resolved | "How do I rename a workflow?"
TK-10121 | cust_000710 | Sable Analytics | 2025-06-29 10:00:00 | 2025-06-30 09:00:00 | P3 | billing | email | 5 | 23.0 | emp_081 | resolved | Question about seat counts.
TK-10122 | cust_000708 | Kestrel Networks | 2025-07-02 15:00:00 | 2025-07-05 10:00:00 | P2 | performance | email | 1 | 67.0 | emp_086 | resolved | "Platform is unusable today." General outage in the NA-West region. Note: Customer requested service credit. Churn probability is high.
TK-10123 | cust_000709 | Willow Works | 2025-07-04 09:00:00 | 2025-07-04 10:00:00 | P4 | auth | web | | 1.0 | emp_080 | resolved | Password help.
TK-10124 | cust_000701 | Marigold Health | 2025-07-07 11:00:00 | 2025-07-08 14:00:00 | P3 | data-sync | email | 5 | 27.0 | emp_084 | resolved | Data from June missing in BigQuery. Triggered a manual backfill.
TK-10125 | cust_000703 | Yarrow Logistics | 2025-07-10 14:00:00 | 2025-07-10 15:30:00 | P4 | billing | chat | | 1.5 | emp_081 | resolved | Credit card update.
TK-10126 | cust_000704 | Onyx Robotics | 2025-07-13 11:00:00 | 2025-07-13 11:30:00 | P1 | runs | api | 5 | 0.5 | emp_085 | resolved | Workflow aborted on production trigger. Found SCHEMA_MISMATCH. Quick fix by their team.
TK-10127 | cust_000714 | Quartz Foundry | 2025-07-16 16:00:00 | 2025-07-17 09:00:00 | P3 | onboarding | web | | 17.0 | emp_082 | resolved | New dev wants to know about the Acme CLI. Pointed to GitHub repo.
TK-10128 | cust_000707 | Verdant Cloud | 2025-07-19 10:00:00 | 2025-07-21 14:00:00 | P2 | integration | email | | 52.0 | emp_084 | resolved | Hubspot oauth tokens expiring every 4 hours. Bug in our token refresh logic for enterprise apps. Hotfixed.
TK-10129 | cust_000700 | Cobalt Systems | 2025-07-22 13:00:00 | 2025-07-22 14:30:00 | P4 | auth | email | 5 | 1.5 | emp_080 | resolved | Access request for a contractor.
TK-10130 | cust_000713 | Harbor Dynamics | 2025-07-25 10:00:00 | 2025-07-27 09:00:00 | P3 | performance | chat | 4 | 47.0 | emp_086 | resolved | Slowness when viewing execution history. Account has 100k+ runs. Suggesting a cleanup of old runs.
TK-10131 | cust_000704 | Onyx Robotics | 2025-07-28 15:00:00 | | P2 | performance | web | | | emp_086 | open | "The canvas is still lagging. We have 500 seats licensed, but only 20 people can use the tool at once without it freezing." Escalating to Priya.
TK-10132 | cust_000702 | Driftwood Media | 2025-08-01 09:00:00 | 2025-08-01 10:00:00 | P4 | billing | email | 5 | 1.0 | emp_081 | resolved | Receipt request.
TK-10133 | cust_000710 | Sable Analytics | 2025-08-04 11:00:00 | 2025-08-06 14:00:00 | P3 | runs | api | | 51.0 | emp_085 | resolved | Workflow failed with STEP_TIMEOUT. The Slack API was down. Acme retry handled it, but they wanted to know why.
TK-10134 | cust_000708 | Kestrel Networks | 2025-08-07 14:00:00 | 2025-08-10 10:00:00 | P2 | integration | email | 1 | 68.0 | emp_084 | resolved | "Our integrations are failing randomly." AUTH_FAILED intermittent. Internal Note: No technical fault found. Customer seems to be looking for reasons to complain. Flagged for CSM (Marco Silva).
TK-10135 | cust_000709 | Willow Works | 2025-08-12 10:00:00 | 2025-08-12 11:30:00 | P4 | auth | web | | 1.5 | emp_080 | resolved | Password help.
TK-10136 | cust_000701 | Marigold Health | 2025-08-15 15:00:00 | 2025-08-17 09:00:00 | P3 | sso | chat | 5 | 42.0 | emp_088 | resolved | Just a question about changing the SSO display name.
TK-10137 | cust_000703 | Yarrow Logistics | 2025-08-18 09:00:00 | 2025-08-18 10:00:00 | P4 | onboarding | chat | | 1.0 | emp_082 | resolved | Link to the API docs.
TK-10138 | cust_000704 | Onyx Robotics | 2025-08-21 11:00:00 | 2025-08-22 15:00:00 | P2 | data-sync | email | 4 | 28.0 | emp_084 | resolved | Sync delay for their BigQuery table. Found a large backlog of runs. Cleared.
TK-10139 | cust_000714 | Quartz Foundry | 2025-08-24 14:00:00 | 2025-08-24 15:30:00 | P3 | auth | web | | 1.5 | emp_080 | resolved | MFA reset for one user.
TK-10140 | cust_000707 | Verdant Cloud | 2025-08-27 10:00:00 | 2025-08-27 11:30:00 | P4 | billing | email | 5 | 1.5 | emp_081 | resolved | Invoice copy.
TK-10141 | cust_000700 | Cobalt Systems | 2025-08-30 15:00:00 | 2025-09-01 10:00:00 | P2 | performance | email | | 43.0 | emp_086 | resolved | Slowness in the workflow editor. Suggested they reduce the number of active integrations in one canvas.
TK-10142 | cust_000713 | Harbor Dynamics | 2025-09-02 09:00:00 | 2025-09-03 14:00:00 | P3 | onboarding | chat | 5 | 29.0 | emp_082 | resolved | Question about user permissions for Business tier.
TK-10143 | cust_000704 | Onyx Robotics | 2025-09-05 11:00:00 | 2025-09-05 12:00:00 | P1 | runs | api | | 1.0 | emp_085 | resolved | Workflow failed with RATE_LIMITED. Customer was doing a bulk migration. Temporary increase in limit granted.
TK-10144 | cust_000702 | Driftwood Media | 2025-09-08 14:00:00 | 2025-09-08 15:30:00 | P4 | auth | web | 5 | 1.5 | emp_080 | resolved | Access request.
TK-10145 | cust_000710 | Sable Analytics | 2025-09-11 10:00:00 | 2025-09-12 09:00:00 | P3 | data-sync | email | | 23.0 | emp_084 | resolved | Sync failing with SCHEMA_MISMATCH. Customer changed a column name in their Postgres DB.
TK-10146 | cust_000708 | Kestrel Networks | 2025-09-14 15:00:00 | 2025-09-16 10:00:00 | P3 | billing | email | 1 | 43.0 | emp_081 | resolved | "We want to cancel our contract early. Your support is too slow." Transferred to Sarah Chen (AE) for churn mitigation. Note: Account is heavily at_risk. 
TK-10147 | cust_000709 | Willow Works | 2025-09-17 09:00:00 | 2025-09-17 10:00:00 | P4 | auth | web | | 1.0 | emp_080 | resolved | Password help.
TK-10148 | cust_000701 | Marigold Health | 2025-09-20 11:00:00 | 2025-09-22 14:00:00 | P2 | integration | email | 5 | 51.0 | emp_084 | resolved | Hubspot to Slack notification flow not firing. User error in Hubspot trigger settings.
TK-10149 | cust_000703 | Yarrow Logistics | 2025-09-23 14:00:00 | 2025-09-23 15:30:00 | P4 | billing | chat | | 1.5 | emp_081 | resolved | Change of credit card.
TK-10150 | cust_000704 | Onyx Robotics | 2025-09-26 11:00:00 | 2025-09-28 09:00:00 | P2 | performance | api | 4 | 46.0 | emp_086 | resolved | Execution time increased for all runs. Internal Note: Found it was a shared worker bottleneck in the NA-West pod. Scaled up.
TK-10151 | cust_000714 | Quartz Foundry | 2025-09-29 16:00:00 | 2025-09-30 09:00:00 | P3 | sso | web | | 17.0 | emp_088 | resolved | Syncing new users from Azure AD.
TK-10152 | cust_000707 | Verdant Cloud | 2025-10-02 10:00:00 | 2025-10-02 11:30:00 | P4 | auth | email | 5 | 1.5 | emp_080 | resolved | Access request.
TK-10153 | cust_000700 | Cobalt Systems | 2025-10-05 15:00:00 | 2025-10-07 10:00:00 | P3 | runs | email | | 43.0 | emp_085 | resolved | Step timeout on an HTTP request.
TK-10154 | cust_000713 | Harbor Dynamics | 2025-10-08 09:00:00 | 2025-10-09 14:00:00 | P2 | integration | chat | 5 | 29.0 | emp_084 | resolved | NetSuite integration failing on large transfers. Advised on batching settings.
TK-10155 | cust_000708 | Kestrel Networks | 2025-10-11 11:00:00 | 2025-10-15 09:00:00 | P3 | billing | email | 1 | 94.0 | emp_081 | resolved | [CHURN SIGNAL] "Budget cuts across the board. We need to move to the Free tier immediately." Note: Explained that moving to Free counts as a churn for the contract. AE sarah.chen is handling the exit conversation.
TK-10156 | cust_000704 | Onyx Robotics | 2025-10-14 14:00:00 | 2025-10-14 15:30:00 | P4 | auth | web | | 1.5 | emp_080 | resolved | New seat request.
TK-10157 | cust_000710 | Sable Analytics | 2025-10-17 10:00:00 | 2025-10-18 09:00:00 | P3 | performance | email | 5 | 23.0 | emp_086 | resolved | UI responsiveness.
TK-10158 | cust_000708 | Kestrel Networks | 2025-10-20 15:00:00 | 2025-10-21 10:00:00 | P2 | integration | email | | 19.0 | emp_084 | resolved | Data export requested. Customer is officially churned on 2025-11-01 per Finance.
TK-10159 | cust_000709 | Willow Works | 2025-10-23 09:00:00 | 2025-10-23 10:00:00 | P4 | auth | web | | 1.0 | emp_080 | resolved | Password help.
TK-10160 | cust_000701 | Marigold Health | 2025-10-26 11:00:00 | 2025-10-28 14:00:00 | P2 | data-sync | email | 5 | 51.0 | emp_084 | resolved | BigQuery sync lag again. Found the customer changed their service account permissions.
TK-10161 | cust_000703 | Yarrow Logistics | 2025-10-29 14:00:00 | 2025-10-29 15:30:00 | P4 | onboarding | chat | | 1.5 | emp_082 | resolved | Logic builder question.
TK-10162 | cust_000704 | Onyx Robotics | 2025-11-01 11:00:00 | | P1 | integration | api | | | emp_085 | open | [CRITICAL] Slack integration failing for all notification flows. AUTH_FAILED. Internal Note: Onyx Robotics is at_risk. P1 over 48h triggered again.
TK-10163 | cust_000714 | Quartz Foundry | 2025-11-04 16:00:00 | 2025-11-05 09:00:00 | P3 | billing | web | | 17.0 | emp_081 | resolved | Tax exemption document upload.
TK-10164 | cust_000707 | Verdant Cloud | 2025-11-07 10:00:00 | 2025-11-07 11:30:00 | P4 | auth | email | 5 | 1.5 | emp_080 | resolved | Access request.
TK-10165 | cust_000700 | Cobalt Systems | 2025-11-10 15:00:00 | 2025-11-12 10:00:00 | P2 | runs | email | | 43.0 | emp_085 | resolved | Workflow failed with RATE_LIMITED on the Shopify API.
TK-10166 | cust_000713 | Harbor Dynamics | 2025-11-13 09:00:00 | 2025-11-14 14:00:00 | P3 | sso | chat | 5 | 29.0 | emp_088 | resolved | Adding a new group to Acme.
TK-10167 | cust_000287 | Beacon Studios | 2025-11-16 11:00:00 | 2025-11-16 12:00:00 | P4 | billing | email | | 1.0 | emp_081 | resolved | Invoice inquiry.
TK-10168 | cust_000702 | Driftwood Media | 2025-11-19 14:00:00 | 2025-11-19 15:30:00 | P3 | onboarding | web | | 1.5 | emp_082 | resolved | Question about loops in the builder.
TK-10169 | cust_000710 | Sable Analytics | 2025-11-22 10:00:00 | 2025-11-23 09:00:00 | P3 | performance | email | 5 | 23.0 | emp_086 | resolved | UI responsiveness.
TK-10170 | cust_000705 | Pebble Digital | 2025-11-25 15:00:00 | 2025-11-26 10:00:00 | P4 | billing | email | | 19.0 | emp_081 | resolved | Receipt request.
TK-10171 | cust_000711 | Ember Industries | 2025-11-28 09:00:00 | 2025-11-28 10:00:00 | P4 | auth | web | | 1.0 | emp_080 | resolved | MFA help.
TK-10172 | cust_000701 | Marigold Health | 2025-12-01 11:00:00 | 2025-12-02 14:00:00 | P2 | integration | email | 5 | 27.0 | emp_084 | resolved | Hubspot oauth tokens again. Same issue as Verdant Cloud earlier.
TK-10173 | cust_000703 | Yarrow Logistics | 2025-12-04 14:00:00 | 2025-12-04 15:30:00 | P4 | auth | chat | | 1.5 | emp_080 | resolved | Access request.
TK-10174 | cust_000704 | Onyx Robotics | 2025-12-07 11:00:00 | | P3 | performance | api | | | emp_086 | open | "The tool is slow. What is my health score? I heard we are flagged at risk." Internal Note: Customer heard about their health score status from somewhere. Need to tread carefully.
TK-10175 | cust_000714 | Quartz Foundry | 2025-12-10 16:00:00 | 2025-12-11 09:00:00 | P3 | data-sync | web | | 17.0 | emp_084 | resolved | Sync failing with NULL_PAYLOAD.
TK-10176 | cust_000707 | Verdant Cloud | 2025-12-13 10:00:00 | 2025-12-13 11:30:00 | P4 | billing | email | 5 | 1.5 | emp_081 | resolved | Update billing address.
TK-10177 | cust_000700 | Cobalt Systems | 2025-12-16 15:00:00 | 2025-12-18 10:00:00 | P2 | runs | email | | 43.0 | emp_085 | resolved | Workflow failed with STEP_TIMEOUT.
TK-10178 | cust_000713 | Harbor Dynamics | 2025-12-19 09:00:00 | 2025-12-20 14:00:00 | P3 | onboarding | chat | 5 | 29.0 | emp_082 | resolved | Logic builder question.
TK-10179 | cust_000704 | Onyx Robotics | 2025-12-23 11:00:00 | 2025-12-23 11:30:00 | P1 | runs | api | | 0.5 | emp_085 | resolved | [INTERNAL EMERGENCY] Site 503. Restarted pod. Quick fix.
TK-10180 | cust_000702 | Driftwood Media | 2025-12-26 14:00:00 | 2025-12-26 15:30:00 | P4 | billing | email | 5 | 1.5 | emp_081 | resolved | Invoice inquiry.
TK-10181 | cust_000710 | Sable Analytics | 2025-12-29 10:00:00 | 2025-12-30 09:00:00 | P3 | sso | email | | 23.0 | emp_088 | resolved | SSO user cannot login. Found duplicate email in Acme system.
TK-10182 | cust_000287 | Beacon Studios | 2026-01-02 11:00:00 | 2026-01-05 09:00:00 | P3 | billing | email | 5 | 70.0 | emp_081 | resolved | "We are being acquired by a larger firm. We need to migrate our account next month." Note: Beacon Studios is a Business account (65 seats). Churn likely in Feb due to parent company choice.
TK-10183 | cust_000705 | Pebble Digital | 2026-01-04 15:00:00 | 2026-01-05 10:00:00 | P4 | auth | email | | 19.0 | emp_080 | resolved | Password reset.
TK-10184 | cust_000711 | Ember Industries | 2026-01-07 09:00:00 | 2026-01-07 10:00:00 | P4 | onboarding | web | | 1.0 | emp_082 | resolved | Link to the API docs.
TK-10185 | cust_000701 | Marigold Health | 2026-01-10 11:00:00 | 2026-01-11 14:00:00 | P2 | integration | email | 5 | 27.0 | emp_084 | resolved | Hubspot integration failing again. Same OAuth issue.
TK-10186 | cust_000703 | Yarrow Logistics | 2026-01-13 14:00:00 | 2026-01-13 15:30:00 | P4 | auth | chat | | 1.5 | emp_080 | resolved | Access request.
TK-10187 | cust_000704 | Onyx Robotics | 2026-01-16 11:00:00 | 2026-01-20 09:00:00 | P1 | runs | api | 1 | 94.0 | emp_085 | resolved | [CRITICAL] Production outage. All runs for Onyx failing with AUTH_FAILED. Internal Note: P1 > 48h triggered again. Onyx Robotics is officially critical/at_risk in account_health. Olivia Tran (CSM) has escalated to Sam Reyes (CEO).
TK-10188 | cust_000714 | Quartz Foundry | 2026-01-19 16:00:00 | 2026-01-20 09:00:00 | P3 | billing | web | | 17.0 | emp_081 | resolved | Tax exemption document upload.
TK-10189 | cust_000707 | Verdant Cloud | 2026-01-22 10:00:00 | 2026-01-22 11:30:00 | P4 | auth | email | 5 | 1.5 | emp_080 | resolved | Access request.
TK-10190 | cust_000700 | Cobalt Systems | 2026-01-25 15:00:00 | 2026-01-27 10:00:00 | P2 | runs | email | | 43.0 | emp_085 | resolved | Workflow failed with RATE_LIMITED.
TK-10191 | cust_000713 | Harbor Dynamics | 2026-01-28 09:00:00 | 2026-01-29 14:00:00 | P3 | onboarding | chat | 5 | 29.0 | emp_082 | resolved | Logic builder question.
TK-10192 | cust_000712 | Juniper Collective | 2026-01-30 11:00:00 | 2026-02-01 10:00:00 | P3 | billing | email | | 47.0 | emp_081 | resolved | "We are churning. The product doesn't fit our needs anymore." Transferred to yuki.sato (AE). Churn confirmed.
TK-10193 | cust_000287 | Beacon Studios | 2026-02-02 14:00:00 | 2026-02-03 10:00:00 | P2 | billing | email | | 20.0 | emp_081 | resolved | [CHURN] Final invoice request. Account churning on 2026-02-18 due to acquisition. 
TK-10194 | cust_000704 | Onyx Robotics | 2026-02-05 11:00:00 | | P2 | performance | api | | | emp_086 | open | "The tool is slow again. Why is our health score 'at risk'? We need a meeting with your VP of CS." Note: Elena Volkov (VP CS) alerted.
TK-10195 | cust_000702 | Driftwood Media | 2026-02-08 14:00:00 | 2026-02-08 15:30:00 | P4 | auth | web | 5 | 1.5 | emp_080 | resolved | Access request.
TK-10196 | cust_000710 | Sable Analytics | 2026-02-11 10:00:00 | 2026-02-12 09:00:00 | P3 | data-sync | email | | 23.0 | emp_084 | resolved | Sync failing with SCHEMA_MISMATCH.
TK-10197 | cust_000705 | Pebble Digital | 2026-02-14 15:00:00 | 2026-02-15 10:00:00 | P4 | billing | email | | 19.0 | emp_081 | resolved | Invoice copy.
TK-10198 | cust_000711 | Ember Industries | 2026-02-17 09:00:00 | 2026-02-17 10:00:00 | P4 | auth | web | | 1.0 | emp_080 | resolved | Password help.
TK-10199 | cust_000701 | Marigold Health | 2026-02-20 11:00:00 | 2026-02-22 14:00:00 | P2 | integration | email | 5 | 51.0 | emp_084 | resolved | Hubspot oauth tokens failing again. Same issue.
TK-10200 | cust_000703 | Yarrow Logistics | 2026-02-23 14:00:00 | 2026-02-23 15:30:00 | P4 | billing | chat | | 1.5 | emp_081 | resolved | Credit card update.
TK-10201 | cust_000704 | Onyx Robotics | 2026-02-26 11:00:00 | 2026-02-28 09:00:00 | P2 | performance | api | 2 | 46.0 | emp_086 | resolved | Slowness when viewing execution history. 
TK-10202 | cust_000714 | Quartz Foundry | 2026-03-01 16:00:00 | 2026-03-02 09:00:00 | P3 | sso | web | | 17.0 | emp_088 | resolved | Syncing new users from Azure AD.
TK-10203 | cust_000707 | Verdant Cloud | 2026-03-04 10:00:00 | 2026-03-04 11:30:00 | P4 | auth | email | 5 | 1.5 | emp_080 | resolved | Access request.
TK-10204 | cust_000700 | Cobalt Systems | 2026-03-07 15:00:00 | 2026-03-09 10:00:00 | P2 | runs | email | | 43.0 | emp_085 | resolved | Workflow failed with STEP_TIMEOUT.
TK-10205 | cust_000713 | Harbor Dynamics | 2026-03-10 09:00:00 | 2026-03-11 14:00:00 | P3 | onboarding | chat | 5 | 29.0 | emp_082 | resolved | Logic builder question.
TK-10206 | cust_000704 | Onyx Robotics | 2026-03-14 11:00:00 | 2026-03-14 11:30:00 | P1 | runs | api | | 0.5 | emp_085 | resolved | Workflow failed with RATE_LIMITED.
TK-10207 | cust_000702 | Driftwood Media | 2026-03-17 14:00:00 | 2026-03-17 15:30:00 | P4 | billing | email | 5 | 1.5 | emp_081 | resolved | Receipt request.
TK-10208 | cust_000710 | Sable Analytics | 2026-03-20 10:00:00 | 2026-03-21 09:00:00 | P3 | performance | email | | 23.0 | emp_086 | resolved | UI responsiveness.
TK-10209 | cust_000705 | Pebble Digital | 2026-03-23 15:00:00 | 2026-03-24 10:00:00 | P4 | auth | email | | 19.0 | emp_080 | resolved | Password reset.
TK-10210 | cust_000711 | Ember Industries | 2026-03-26 09:00:00 | 2026-03-26 10:00:00 | P4 | onboarding | web | | 1.0 | emp_082 | resolved | Link to the API docs.
TK-10211 | cust_000701 | Marigold Health | 2026-03-29 11:00:00 | 2026-03-31 14:00:00 | P2 | integration | email | 5 | 51.0 | emp_084 | resolved | Hubspot integration failing again. Same issue.
TK-10212 | cust_000703 | Yarrow Logistics | 2026-04-01 14:00:00 | 2026-04-01 15:30:00 | P4 | auth | chat | | 1.5 | emp_080 | resolved | Access request.
TK-10213 | cust_000704 | Onyx Robotics | 2026-04-04 11:00:00 | 2026-04-08 09:00:00 | P1 | runs | api | 1 | 94.0 | emp_085 | resolved | [CRITICAL] Production outage for Onyx. Auth proxy failure again. Internal Note: Third P1 > 48h this year. Onyx Robotics is critical/at_risk in account_health. Olivia Tran (CSM) has escalated again.
TK-10214 | cust_000714 | Quartz Foundry | 2026-04-07 16:00:00 | 2026-04-08 09:00:00 | P3 | billing | web | | 17.0 | emp_081 | resolved | Tax exemption document upload.
TK-10215 | cust_000707 | Verdant Cloud | 2026-04-10 10:00:00 | 2026-04-10 11:30:00 | P4 | auth | email | 5 | 1.5 | emp_080 | resolved | Access request.
TK-10216 | cust_000700 | Cobalt Systems | 2026-04-13 15:00:00 | 2026-04-15 10:00:00 | P2 | runs | email | | 43.0 | emp_085 | resolved | Workflow failed with RATE_LIMITED.
TK-10217 | cust_000713 | Harbor Dynamics | 2026-04-16 09:00:00 | 2026-04-17 14:00:00 | P3 | onboarding | chat | 5 | 29.0 | emp_082 | resolved | Logic builder question.
TK-10218 | cust_000704 | Onyx Robotics | 2026-04-19 11:00:00 | 2026-04-19 11:30:00 | P1 | runs | api | | 0.5 | emp_085 | resolved | Workflow failed with RATE_LIMITED.
TK-10219 | cust_000702 | Driftwood Media | 2026-04-22 14:00:00 | 2026-04-22 15:30:00 | P4 | auth | web | 5 | 1.5 | emp_080 | resolved | Access request.
TK-10220 | cust_000710 | Sable Analytics | 2026-04-25 10:00:00 | 2026-04-26 09:00:00 | P3 | data-sync | email | | 23.0 | emp_084 | resolved | Sync failing with SCHEMA_MISMATCH.
TK-10221 | cust_000705 | Pebble Digital | 2026-04-28 15:00:00 | 2026-04-29 10:00:00 | P4 | billing | email | | 19.0 | emp_081 | resolved | Invoice copy.
TK-10222 | cust_000711 | Ember Industries | 2026-04-30 09:00:00 | 2026-04-30 10:00:00 | P4 | auth | web | | 1.0 | emp_080 | resolved | Password help.
TK-10223 | cust_000704 | Onyx Robotics | 2026-05-02 11:00:00 | | P2 | performance | api | | | emp_086 | open | "The tool is slow again. Why is our health score 'at risk'?" Note: Customer is asking about health score again. Elena Volkov (VP CS) alerted.
TK-10224 | cust_000701 | Marigold Health | 2026-05-04 10:00:00 | | P3 | integration | email | | | emp_084 | open | "Hubspot integration failing again. Same issue." Ongoing investigation.

# --- [END OF EXPORT] ---