"""
Chronological-round document generator for the acme-ecomm demo corpus.

Unlike datasets/acme/gen_docs.py (a static file list, generated blind to each
other), this generator runs in ROUNDS ordered by simulated time. Round N
generates the documents that "exist" as of that round's date, across every
system of record -- and each document can see (and should reference) what
earlier rounds already produced, via a LEDGER of events that accumulates as
generation proceeds. That's what makes the corpus referentially rich instead
of just internally consistent: a Q4 postmortem can say "this regressed after
the checkout experiment we shipped last round" because that experiment is
literally in its prompt.

Inputs (both live in this directory, written by another agent -- read-only
here, never modified):
  - CANON.md      frozen fact sheet: company, cast, warehouse, a dated
                   timeline of events across ~6 fiscal quarters.
  - QUESTIONS.md  the demo's question set. Not read by this script at
                   runtime, but the ROUNDS table below was hand-aligned to
                   the events/experiments/dates it plants, so generation
                   produces documents that actually make those questions
                   answerable. See the comment above ROUNDS.

Output: sources/acme-ecomm/<system>/<file>.md, one file per spec in ROUNDS.
State: datasets/acme-ecomm/LEDGER.jsonl -- one JSON event object per line,
appended after every document. Resumable: a document already on disk is
skipped, and restart rebuilds all state by re-reading the ledger file plus
whatever's already in sources/acme-ecomm/ -- there is no separate run-state
file to go stale.

Usage:
  uv run --no-project --with google-genai python datasets/acme-ecomm/gen_rounds.py --round q3fy26
  uv run --no-project --with google-genai python datasets/acme-ecomm/gen_rounds.py --all
  uv run --no-project --with google-genai python datasets/acme-ecomm/gen_rounds.py --all --dry-run
  uv run --no-project --with google-genai python datasets/acme-ecomm/gen_rounds.py --round q4fy26 --limit 2
"""
import argparse
import json
import os
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from google import genai

REPO = Path(__file__).resolve().parents[2]
DATASET_DIR = Path(__file__).parent
SOURCES_DIR = REPO / "sources" / "acme-ecomm"

CANON_PATH = DATASET_DIR / "CANON.md"
LEDGER_PATH = DATASET_DIR / "LEDGER.jsonl"

# Eager read, matching datasets/acme/{gen_docs,gen_one,gen_grow}.py convention.
# Requires CANON.md to exist -- see the module docstring in verification notes
# for how to smoke-test this file before the real CANON.md lands.
CANON_TEXT = CANON_PATH.read_text(encoding="utf-8")

MODEL = os.environ.get("GEN_MODEL", "gemini-3.5-flash-lite")
PROJECT = os.environ.get("VERTEX_PROJECT_ID", "mission-control-350520")
LOCATION = "global"
TEMPERATURE = 1.0
MAX_OUTPUT_TOKENS = 65536

# Published gemini-3.5-flash-lite rate.
PRICE_IN_PER_1M_USD = 0.30
PRICE_OUT_PER_1M_USD = 2.50


# ---------------------------------------------------------------------------
# Systems of record -- mirrors how sources/acme-raw/ is organised (slack,
# gong, meetings, query_logs, postmortems, docs, dbt, schema, scratch),
# adapted to what a retail/eCommerce org actually runs on. `aitable` is here
# because QUESTIONS.md (read directly, before CANON.md existed) turned out to
# lean on a legacy-roadmap-tracker-vs-Jira split as a load-bearing trap -- not
# one of the systems named in the original task brief, but real evidence
# trumps the a priori guess, and CANON.md (now landed) confirms it under
# SIGNAL [aitable-jira-split].
#
# `adapter` values in each spec below are taken VERBATIM from CANON.md's own
# "STYLE" section (its authors already fixed the adapter vocabulary), not
# invented here: bq_query_log, hive_query_log, fullstory_session_note,
# expo_experiment, marketing_calendar_export, mbr_deck_notes, medallia_verbatim,
# aitable_card, jira_ticket, confluence_page, slack_thread, postmortem,
# meeting_notes, org_announcement.
# ---------------------------------------------------------------------------
SYSTEMS = {
    "slack": "Slack channel archives (adapter: slack_thread)",
    "expo": "Expo-equivalent experiment platform -- specs and readouts, dim_experiment / fact_experiment_readouts (adapter: expo_experiment)",
    "medallia": "Medallia VOC survey verbatims and theme reports, fact_voc_responses (adapter: medallia_verbatim)",
    "jira": "Jira tickets -- current-era eng/product work, incidents, escalations, committed 2026-01-15 onward (adapter: jira_ticket)",
    "aitable": "Aitable -- legacy roadmap tracker, superseded by Jira 2026-01-15 but not fully migrated (adapter: aitable_card)",
    "confluence": "Confluence wiki pages -- PRDs, retros, rollout plans (adapter: confluence_page)",
    "fullstory": "FullStory session-replay analysis notes -- referenced qualitatively, not a BQ table (adapter: fullstory_session_note)",
    "marketing_calendar": "Marketing campaign calendar entries, dim_marketing_calendar (adapter: marketing_calendar_export)",
    "query_logs": "BigQuery / Hive analyst query logs (adapter: bq_query_log or hive_query_log)",
    "meetings": "Meeting notes -- MBRs (adapter: mbr_deck_notes) and other leadership/launch syncs (adapter: meeting_notes)",
    "postmortems": "Incident postmortems (adapter: postmortem)",
    "gong": "Call transcripts -- vendor / partner / exec calls",
    "dbt": "dbt model documentation for warehouse marts",
    "schema": "Warehouse schema dumps",
    "scratch": "Analyst scratch notes and working docs",
    "docs": "General internal docs, catch-all -- also where a company-wide org_announcement adapter doc would live",
}

SYSTEM = """You are generating synthetic internal documents for "Acme" -- a fictitious, \
Walmart-scale retail / eCommerce company (physical + online, multiple markets, a \
Marketplace business with several sub-verticals, a paid membership program, \
DC-based fulfillment) -- for an analytics demo.

RULES:
1. Everything must be internally consistent with the CANON provided below -- it is frozen and authoritative.
2. Everything must be consistent with the LEDGER of prior events you are given -- those things have
   already happened. Reference them naturally where relevant ("since last week's launch review...",
   "the experiment we killed three weeks ago...") instead of writing this document as if it exists in
   isolation. Do not re-narrate an old event as if it were new.
3. Use ONLY the people, teams, programs, vendors, markets, and numbers established in the CANON or the
   LEDGER. Never invent facts that contradict either. You MAY invent minor incidental specifics (a
   ticket number, the exact wording of a Slack aside) as long as they don't contradict CANON/LEDGER.
4. Write in a natural, messy, human voice appropriate for the document's system of record.
5. Heavy noise is GOOD -- off-topic chatter, mundane detail, tangents, process overhead. Signal should
   be buried, not headlined.
6. Don't summarize or compress. Be verbose and detailed for the document type.
7. Stay inside this round's simulated time period. The LEDGER you're given is a hard boundary on
   "what's already happened" -- don't reference anything later than that, and don't resolve a thread
   (an open ticket, an in-flight experiment) before its own natural conclusion.
8. Acme's fiscal year starts Feb 1 (Q1=Feb-Apr, Q2=May-Jul, Q3=Aug-Oct, Q4=Nov-Jan). Use fiscal-quarter
   framing (e.g. "Q1FY27") where a document would naturally use it, alongside plain dates.
9. Include YAML frontmatter at the very start, exactly as given.
10. At the VERY END of the document, after all document content, emit one fenced code block tagged
    LEDGER containing a JSON array of the NEW datable events this document introduces (meetings,
    experiments, launches, incidents, decisions, notable metric shifts) -- i.e. events not already in
    the LEDGER you were given. Format:
```LEDGER
[{"date": "YYYY-MM-DD", "kind": "meeting|experiment|launch|incident|decision|metric_shift|event", "vertical": "<a vertical_code from CANON's taxonomy, e.g. MARKETPLACE, CARE, SPEED>", "owner": "<a handle from CANON's ORG/PEOPLE, e.g. hannah.brennan>", "summary": "one line, specific enough for a future document to cite"}]
```
    If the document introduces no new datable event, emit `[]`. Nothing may follow this block."""


# ---------------------------------------------------------------------------
# FULL ROUND / SPEC TABLE -- all 6 of CANON's fiscal quarters, all 16
# declared SYSTEMS, and every row of CANON's ~46-event dated timeline.
#
# Provenance: the original 3-round / 13-spec version of this table was
# drafted by reading QUESTIONS.md alone (CANON.md didn't exist yet),
# inferring the fiscal calendar and event spine from what the 15 questions
# planted. CANON.md has since landed in this same directory, and the
# inference checked out almost exactly -- same fiscal calendar (Feb-start
# FY, confirmed in CANON's Company section), same experiment names AND IDs
# (Checkout Simplify/exp_2214, Nav Refresh/exp_2215, Wider Promise Window/
# exp_1187, Verified Badge Prominence/exp_2401), same dates, same
# Aitable/Jira split. Those original q3fy26/q4fy26/q1fy27 rounds and their
# 13 specs are UNCHANGED below (3 of them -- both jira docs and the
# confluence PRD in q3fy26 -- are already generated on disk; the rest were
# drafted but never run). This expansion adds q1fy26, q2fy26, and q2fy27 as
# new rounds, and appends new specs to the three existing rounds to close
# the gaps a prior comment here flagged as not yet covered (the paid-search
# cut, the session-counting change, the Style/Resold mix-shift narrative,
# Bot Handoff Threshold, Benefit Onboarding Carousel, the CLTV join
# distinction, and Q1FY26/Q2FY26 in full) -- every one of those now has a
# spec. All new specs were appended after existing ones (never interleaved
# ahead of or edited into them), so the 3 already-generated files' specs are
# byte-identical to before.
#
# Round dates (as-of cutoffs), all ~75-88% through their fiscal quarter,
# matching the existing rounds' own convention: q1fy26=2025-04-15 (Q1FY26:
# 2025-02-01..2025-04-30), q2fy26=2025-07-15 (Q2FY26: 2025-05-01..2025-07-31),
# q3fy26=2025-10-15 (Q3FY26: 2025-08-01..2025-10-31), q4fy26=2026-01-25
# (Q4FY26: 2025-11-01..2026-01-31), q1fy27=2026-04-15 (Q1FY27:
# 2026-02-01..2026-04-30), q2fy27=2026-07-20 (Q2FY27: 2026-05-01..2026-07-31,
# IN FLIGHT -- 2026-07-20 is CANON's own "today" snapshot date, so this round
# uses it exactly rather than picking an earlier cutoff). A spec whose focus
# text cites ITS OWN round's fiscal-quarter figures is written with
# QTD/"pacing toward" language, never as a closed-quarter final number --
# every round's date lands 2-15 days before that quarter's actual close, so
# the quarter is never really over yet from the document's own vantage
# (matching how the original 13 specs already hedge this, e.g. "projected to
# land around $61M" rather than stating a final Q3FY26 Collectibles GMV).
#
# The task brief's own round-naming example ("2025-Q3, 2025-Q4, 2026-Q1") is
# calendar-quarter shaped; this uses fiscal-quarter names (q1fy26 .. q2fy27)
# instead because that's the convention CANON.md itself uses -- flagged for
# confirmation in the return-report, not silently overridden.
#
# Adapter-name judgment call (flagged, not silently decided): CANON.md's
# STYLE section pins adapter names for 12 of the 16 SYSTEMS above (the ones
# tied to the customer's distinctly-named tools -- Jira, Confluence, Aitable,
# Medallia, Expo, FullStory, Marketing Calendar, plus meetings/postmortems/
# slack/query_logs/docs-as-announcement) but is SILENT on gong, dbt, schema,
# and scratch -- generic backend/analyst tooling CANON's author evidently
# didn't think needed a customer-specific respecification. Rather than invent
# new adapter strings, specs below reuse the names already established
# elsewhere in THIS repo's actual pipeline (see README.md's adapter-prefix
# list and datasets/acme/gen_docs.py's real usage): gong -> gong_call,
# dbt -> dbt_model, schema -> bq_schema. scratch and non-announcement docs/
# content reuse confluence_page (Confluence is this company's own established
# wiki tool per CANON, so an informal personal scratch page or a general FAQ/
# reference doc living there is a realistic, not a strained, fit). No spec
# below uses an adapter string that isn't either CANON-verbatim or one of
# these three repo-wide, already-real names.
#
# BULK vs DISCRETE (the noise-density convention): CANON's own STYLE section
# calls for ~1 signal buried per several hundred lines, and the sibling
# datasets/acme corpus's actual bulk files (e.g.
# sources/acme-raw/slack/bulk__slack-data-help-2025H2-2026Q1.md, 309KB) are
# the calibration target. Specs marked `"bulk": True` below (filenames also
# `bulk__`-prefixed, matching the sibling's own naming) are exports/archives
# meant to land in that size class -- an order of magnitude bigger than the
# discrete specs, which stay at the original 6-9KB (a single ticket/PRD/
# experiment readout is CORRECTLY that size; it is not a bug that they're
# smaller than the bulk files). Each bulk spec's `focus` states an explicit
# target KB range. Because a single gemini-3.5-flash-lite call is unlikely to
# fill a 100-300KB target in one pass, every bulk spec is a candidate for
# datasets/acme/gen_grow.py's append-loop (run against the file this script
# produces, after the fact, to reach full size) -- called out inline above
# each one, not just here.
# ---------------------------------------------------------------------------
ROUNDS = [
    {
        "name": "q1fy26",
        "date": "2025-04-15",  # fiscal Q1FY26 = Feb-Apr 2025
        "specs": [
            {
                "path": "docs/q1fy26__carlos-figueroa-vp-data-analytics-promotion.md",
                "system": "docs",
                "adapter": "org_announcement",
                "topic": "Org announcement: carlos.figueroa promoted to VP Data & Analytics",
                "focus": (
                    "A company-wide announcement dated 2025-03-10: carlos.figueroa promoted "
                    "Director -> VP Data & Analytics (assoc_100060), per CANON. Cover the new "
                    "reporting context (Data team: wei.hartono, amara.shah, connor.blake, "
                    "giulia.romano) and a brief FY26 Q1 kickoff framing -- do not state any "
                    "Q1FY26 figures as final/closed (the quarter doesn't close until 2025-04-30). "
                    "Ordinary announcement noise: congratulatory tone, an upcoming all-hands date, "
                    "one unrelated facilities aside. End with a LEDGER 'decision' event dated "
                    "2025-03-10, vertical 'DATA', owner carlos.figueroa."
                ),
                "parallel_ok": True,
            },
            {
                "path": "schema/q1fy26__acme-ecomm-bigquery-warehouse-schema-reference.md",
                "system": "schema",
                "adapter": "bq_schema",
                "topic": "BigQuery schema reference dump: acme_ecomm dataset (23 tables)",
                "focus": (
                    "A schema/information-schema-style reference dump, owned by wei.hartono, "
                    "listing all 23 tables in the FLAT `nexus-analyst-demo.acme_ecomm` dataset -- "
                    "8 dimensions + 9 base facts + 6 derived marts, per CANON's Warehouse section "
                    "-- with column names/types for each. For every panel/sample table (dim_member "
                    "120,000 rows, dim_seller ~2,500, fact_orders ~400,000, fact_care_contacts "
                    "~50,000, fact_marketplace_listings ~35,000, fact_membership_events ~450,000, "
                    "fact_voc_responses ~40,000) include its stated row count and a 'representative "
                    "panel, not full population' annotation verbatim from CANON's arithmetic "
                    "convention 5. Reiterate the flat-dataset rule (no `acme_ecomm.marts.*` "
                    "nesting) in a header comment. Dry reference material, minimal narrative. "
                    "Emits no new event -- end with an empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "dbt/q1fy26__core-marts-model-documentation.md",
                "system": "dbt",
                "adapter": "dbt_model",
                "topic": "dbt model documentation: the 6 canonical derived marts",
                "focus": (
                    "A dbt-style model-doc export (SQL blocks with descriptive comments, column "
                    "docs, `depends_on` refs, owner annotations), owned by wei.hartono, for the 6 "
                    "derived marts: traffic_conversion_summary, fulfillment_speed_daily, "
                    "care_deflection_daily, member_cltv, marketplace_seller_performance, "
                    "marketplace_gmv_summary. For member_cltv, the SQL comment MUST show the "
                    "canonical LEFT JOIN dim_member to fact_orders with "
                    "COALESCE(trailing_12mo_gmv_usd, 0), with an inline warning against an INNER "
                    "JOIN (drops the 20%/24,000 dormant members, inflates CLTV from $500 to a "
                    "wrong $625) -- CANON's SIGNAL [cltv-join-drop] verbatim. For "
                    "marketplace_gmv_summary, a comment noting it is full-population and the "
                    "canonical source for Marketplace GMV-by-sub-vertical (never `fact_orders` for "
                    "that cut, per convention 5). Mostly dry technical reference; light noise via "
                    "a couple of TODO/FIXME comments. Emits no new event -- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "meetings/q1fy26__april-mbr-q1fy26-qtd-review.md",
                "system": "meetings",
                "adapter": "mbr_deck_notes",
                "topic": "MBR notes: April 2025 Monthly Business Review, Q1FY26 QTD",
                "focus": (
                    "Notes from the April 2025 Monthly Business Review -- per CANON's cadence, an "
                    "MBR reviews the prior fiscal month (so this one covers March 2025), presented "
                    "by carlos.figueroa (freshly VP as of 2025-03-10 -- reference that LEDGER "
                    "event) and vertical leads. Frame all Q1FY26 figures as QUARTER-TO-DATE/pacing "
                    "toward CANON's stated Q1FY26 column (the quarter doesn't close until "
                    "2025-04-30, still 2 weeks out) -- e.g. 'tracking to roughly 3.05% US "
                    "conversion, $651M US GMV' rather than stating them as final. Cover the 5 deep "
                    "verticals this way (US/CA/MX conversion+traffic, Marketplace, Care, Speed, "
                    "Membership) plus one-line, deliberately thin metric-row mentions of a few of "
                    "the 11 light verticals (CLUB, B2B, PAYMENTS, OPD_DFS, MARTECH) -- no "
                    "storyline for those, just a status word each. Do not cite FY27 goals (not set "
                    "yet this early). Ordinary MBR noise: attendance, action items, next-meeting "
                    "date. End with a LEDGER 'meeting' event dated 2025-04-15."
                ),
                "parallel_ok": False,
            },
            {
                "path": "gong/q1fy26__fy26-kickoff-leadership-call.md",
                "system": "gong",
                "adapter": "gong_call",
                "topic": "Gong call transcript: FY26 kickoff leadership sync (internal exec call)",
                "focus": (
                    "An internal Gong-recorded call -- deborah.osei (CEO) with the SVP staff "
                    "(felix.arroyo, hannah.brennan, victor.okonkwo, renee.kowalski, ben.tanaka, "
                    "carlos.figueroa) opening FY26, congratulating carlos.figueroa on the VP "
                    "promotion (reference that LEDGER event from this round), setting tone across "
                    "Marketplace/Care/Speed/Membership/US_CONV. Include a couple of throwaway "
                    "one-liners touching light verticals (B2B wholesale pipeline, a Payments "
                    "dispute-rate mention, Club banner renewal timing) as pure texture, no figures "
                    "attached. Heavy call-transcript noise: scheduling crosstalk, an offsite-venue "
                    "tangent, a dog barking on the line. Do not state FY26 full-year actuals (the "
                    "year has barely started). End with a LEDGER 'meeting' event dated 2025-04-10."
                ),
                "parallel_ok": False,
            },
            {
                "path": "aitable/q1fy26__legacy-roadmap-care-marketplace-cards.md",
                "system": "aitable",
                "adapter": "aitable_card",
                "topic": "Aitable roadmap export: Care and Marketplace initiative cards (legacy tracker, Q1FY26)",
                "focus": (
                    "Aitable roadmap cards for Q1FY26, administered by nadia.esposito's Product "
                    "Ops team -- Care initiatives (owners aisha.rahman, julian.moss, "
                    "dominic.paquet) and Marketplace initiatives (owners sanjay.bhatt, "
                    "ines.delgado, noah.kessler, victor.okonkwo). Fields: owner, status, target "
                    "quarter, linked doc. Mix of shipped/in-progress/backlog cards. Include one "
                    "early, vague backlog card floating 'explore a customer-facing trust signal "
                    "for Collectibles' with no owner assigned yet -- do NOT name GradeSure or "
                    "exp_2401 (neither exists yet at this point in the timeline). Purely noise/"
                    "context, no dependency on other Q1FY26 docs. Mention in passing that Jira "
                    "exists for engineering work but roadmap ideation still lives here. Emits no "
                    "new event -- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "query_logs/bulk__q1fy26-q2fy26-bq-audit-log.md",
                "system": "query_logs",
                "adapter": "bq_query_log",
                "bulk": True,  # BULK -- candidate for gen_grow.py's append-loop if the first pass undershoots the target.
                "topic": "BigQuery analyst query audit log — Q1FY26 & Q2FY26 (2025-02 through 2025-07)",
                "focus": (
                    "BULK export, target 90-130KB. 150+ realistic analyst BigQuery queries against "
                    "`nexus-analyst-demo.acme_ecomm` across Q1FY26 and Q2FY26, timestamped, by user "
                    "(Data & Analytics team plus a few PM self-serve queries), with bytes-billed/"
                    "duration metadata, spanning all 23 tables. Include: a query correctly computing "
                    "US conversion via `traffic_conversion_summary` tracking toward CANON's "
                    "3.05%/3.00% Q1/Q2 figures; a couple of queries where an analyst runs `SELECT "
                    "COUNT(*) FROM dim_member` and gets 120,000, with an inline correction noting "
                    "that's the panel, not the true multi-million-member base (an early instance of "
                    "SIGNAL [sample-vs-population]); a query against `marketplace_gmv_summary` "
                    "confirming Style/Resold/Collectibles Q1/Q2 splits; a couple of WRONG queries "
                    "hitting `acme_ecomm.marts.membership.member_cltv` with a '-- table not found, "
                    "flat dataset' comment; routine JOINs, window functions, CTEs. Mostly mundane -- "
                    "bury real signal roughly every 100-200 lines, never headlined. NOTE: candidate "
                    "for gen_grow.py's append-loop to reach the target size."
                ),
                "parallel_ok": True,
            },
        ],
    },
    {
        "name": "q2fy26",
        "date": "2025-07-15",  # fiscal Q2FY26 = May-Jul 2025
        "specs": [
            {
                "path": "confluence/q2fy26__rewear-collective-resold-milestone-and-seller-tiering.md",
                "system": "confluence",
                "adapter": "confluence_page",
                "topic": "Confluence page: ReWear Collective (sel_500204) crosses $1M trailing-90d GMV",
                "focus": (
                    "A Confluence note, owned by victor.okonkwo's Marketplace team (noah.kessler, "
                    "Resold PM, contributing), marking ReWear Collective (sel_500204) crossing $1M "
                    "trailing-90d GMV on 2025-05-14 and becoming a top-20 Resold seller (per CANON; "
                    "fulfillment_method ship_with_acme). Frame this as an early, still-modest data "
                    "point -- at this point it reads as one seller having a good run, NOT a category "
                    "trend (Resold's dramatic +90.9% YoY acceleration doesn't show up until "
                    "Q1FY27 -- do not foreshadow it). Include seller-tiering GMV thresholds and light "
                    "ship_with_acme-vs-seller_fulfilled economics discussion. Noise: a passing "
                    "mention of sel_500147 Harlow & Finch (Resold, mid-tier, 'nothing exciting "
                    "happening there, which is fine'). End with a LEDGER 'metric_shift' event dated "
                    "2025-05-14, vertical MARKETPLACE, owner victor.okonkwo."
                ),
                "parallel_ok": True,
            },
            {
                "path": "jira/q2fy26__acme-plus-streaming-perk-vidora-launch.md",
                "system": "jira",
                "adapter": "jira_ticket",
                "topic": "Jira ticket: Acme+ streaming-perk launch, partner Vidora",
                "focus": (
                    "A Jira release ticket, owned by renee.kowalski's Membership team "
                    "(simone.laurent, derek.holloway contributing), for the Acme+ streaming "
                    "benefit launching 2025-06-01 under original partner 'Vidora' per CANON. "
                    "Cover benefit mechanics (bundled into monthly/annual plans at no extra cost), "
                    "rollout scope, and a forward-looking renewal-lift HYPOTHESIS for adopters -- do "
                    "not state the eventual ~93% figure as an already-measured result, that's a "
                    "later, matured-cohort read. Routine release-process comments. End with a "
                    "LEDGER 'launch' event dated 2025-06-01, vertical MEMBERSHIP, owner "
                    "renee.kowalski."
                ),
                "parallel_ok": True,
            },
            {
                "path": "gong/q2fy26__vidora-partnership-account-call.md",
                "system": "gong",
                "adapter": "gong_call",
                "topic": "Gong call transcript: Vidora partnership account-management call",
                "focus": (
                    "A vendor call transcript, renee.kowalski's team with Vidora's account team, "
                    "shortly after the 2025-06-01 streaming-perk launch (reference that LEDGER "
                    "event from earlier this round). Routine partner check-in: integration health, "
                    "early redemption volume, an upcoming content-catalog refresh on Vidora's side "
                    "-- ordinary vendor-relationship texture. Must NOT foreshadow the eventual "
                    "2026-06-01 switch to Reelstream. Standard call noise: small talk, action "
                    "items, next-call scheduling. Emits no new event -- empty LEDGER array."
                ),
                "parallel_ok": False,
            },
            {
                "path": "fullstory/q2fy26__mobile-checkout-friction-session-review.md",
                "system": "fullstory",
                "adapter": "fullstory_session_note",
                "topic": "FullStory session-replay note: mobile checkout friction, US conversion baseline",
                "focus": (
                    "A qualitative FullStory session-replay note, from maya.lindqvist's US "
                    "Conversion & Traffic team, reviewing mobile checkout session replays during "
                    "Q2FY26 (conversion tracking toward CANON's ~3.00% for the quarter). Describe "
                    "observed friction (excess form fields, address-autocomplete misfires, a "
                    "confusing shipping-method toggle) as plausible qualitative groundwork for a "
                    "future checkout push -- do NOT name 'Checkout Simplify' or exp_2214 (owen."
                    "faust's initiative, doesn't start until 2026-02-16) or claim any decision has "
                    "been made; pure exploratory observation. Usual FullStory-note noise: session "
                    "counts reviewed, device/browser breakdown, a couple of dead ends. Emits no new "
                    "event -- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "medallia/q2fy26__voc-baseline-theme-report-q2fy26.md",
                "system": "medallia",
                "adapter": "medallia_verbatim",
                "topic": "Medallia VOC theme report: Q2FY26 baseline theme distribution",
                "focus": (
                    "A routine quarterly VOC theme report from giulia.romano's analytics team, "
                    "establishing the BASELINE theme distribution well before anything unusual "
                    "happens -- state the ~3.5% baseline share for 'refund delay' verbatims "
                    "explicitly (the same baseline CANON's SIGNAL [voc-leads-quant] references), "
                    "alongside a few other themes (shipping-speed satisfaction, checkout ease, "
                    "Marketplace authenticity trust, membership benefit awareness) at their own "
                    "baseline shares. A representative batch of mostly mundane/neutral-to-positive "
                    "verbatim quotes. This document's whole point is to be the unremarkable 'before' "
                    "picture -- nothing here should read as an early warning; that comes in "
                    "Q4FY26. End with a LEDGER 'metric_shift' event dated 2025-07-10, tagged "
                    "explicitly as a baseline reading (not an anomaly), vertical CARE, owner "
                    "giulia.romano."
                ),
                "parallel_ok": True,
            },
            {
                "path": "scratch/q2fy26__analyst-scratch-fy26-h1-exploration.md",
                "system": "scratch",
                "adapter": "confluence_page",
                "topic": "Analyst scratch notes: H1FY26 exploratory data pulls",
                "focus": (
                    "Informal scratch/working notes from amara.shah (Data Analyst, Finance/MBR) -- "
                    "a personal draft Confluence page, half-finished thoughts exploring H1FY26 "
                    "(Q1+Q2FY26) data ahead of an upcoming board deck. Ad hoc SQL snippets, a "
                    "couple of dead-end explorations, a few 'come back to this' TODOs, and a "
                    "correct-but-buried aside that `fact_orders` is a ~400,000-row sample, not the "
                    "population (a light early echo of SIGNAL [sample-vs-population], stated in "
                    "passing). Messy, non-linear, realistic personal notes, not polished. Emits no "
                    "new event -- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "slack/q2fy26__data-help-warehouse-onboarding-thread.md",
                "system": "slack",
                "adapter": "slack_thread",
                "topic": "Slack #data-help thread: new-analyst onboarding on the acme_ecomm warehouse",
                "focus": (
                    "A #data-help Slack thread, wei.hartono and connor.blake fielding onboarding "
                    "questions from a newer analyst about the acme_ecomm warehouse -- the "
                    "flat-dataset rule (no `acme_ecomm.marts.*` nesting), the panel-vs-population "
                    "distinction on `dim_member`/`dim_seller`/`fact_orders` (correctly stated, per "
                    "convention 5), and where fiscal-quarter boundaries live (`dim_date`). Ordinary "
                    "Slack noise: emoji reactions, an office-snacks tangent, a VPN-access question. "
                    "A deliberate second, different-voice restatement of the flat-dataset and "
                    "sample-vs-population conventions for retrieval redundancy. Emits no new event "
                    "-- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "docs/q2fy26__acme-ecomm-glossary-and-fiscal-calendar-reference.md",
                "system": "docs",
                "adapter": "confluence_page",
                "topic": "Internal glossary: acme_ecomm metric definitions and fiscal calendar reference",
                "focus": (
                    "A glossary-style internal reference doc defining core terms for anyone new to "
                    "the acme_ecomm warehouse: the Feb-start fiscal calendar (Q1 Feb-Apr, Q2 "
                    "May-Jul, Q3 Aug-Oct, Q4 Nov-Jan/peak-holiday), the 16-vertical taxonomy naming "
                    "the 5 deep verticals explicitly (US_CONV, MARKETPLACE, CARE, SPEED, "
                    "MEMBERSHIP) vs. the 11 light ones, and definitions for conversion rate, GMV, "
                    "on-time-to-promise, deflection rate, CLTV -- all matching CANON's arithmetic "
                    "conventions exactly (never re-derive GMV from conversion rate; `*_usd` columns "
                    "already FX-converted). Dry reference material, minimal narrative. Emits no new "
                    "event -- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "postmortems/q2fy26__marketplace-gmv-summary-pipeline-freshness-incident.md",
                "system": "postmortems",
                "adapter": "postmortem",
                "topic": "Postmortem: marketplace_gmv_summary mart freshness delay",
                "focus": (
                    "A minor incident postmortem, owned by connor.blake (Data Engineer, pipeline/"
                    "freshness), covering a Q2FY26 pipeline delay where `marketplace_gmv_summary` "
                    "ran ~14 hours stale after an upstream job failure, causing a handful of "
                    "analysts to pull outdated Style/Resold/Collectibles GMV splits for a day "
                    "before the fix landed. Root cause: a retry-logic bug in the nightly job -- "
                    "deliberately ordinary data-engineering noise, NOT connected to any of the "
                    "corpus's larger narratives. Standard postmortem structure (timeline, root "
                    "cause, action items), brief. End with a LEDGER 'incident' event dated "
                    "2025-06-20, vertical MARKETPLACE, owner connor.blake."
                ),
                "parallel_ok": True,
            },
        ],
    },
    {
        "name": "q3fy26",
        "date": "2025-10-15",  # fiscal Q3FY26 = Aug-Oct 2025
        "specs": [
            {
                "path": "jira/q3fy26__collectibles-counterfeit-listings-epic.md",
                "system": "jira",
                "adapter": "jira_ticket",
                "topic": "Jira epic: Collectibles counterfeit-listing spike and the Trust & Safety response",
                "focus": (
                    "A Jira epic (with sub-tickets and a comment thread) tracking the Collectibles "
                    "counterfeit-listing spike CANON dates to 2025-08-04 (a viral vintage-card "
                    "auction result triggers a flood of new sellers/buyers, some bad-faith), and the "
                    "compliance action against seller sel_500089 'Bramblewood Vintage' (flagged "
                    "2025-08-12 for 3 counterfeit-listing violations, suspended 2025-09-02). Cover "
                    "lucia.ferreira's hiring/onboarding as Trust & Safety Lead (started 2025-09-01, "
                    "an urgent backfill in direct response to the 08-04 spike, reporting to "
                    "victor.okonkwo) and the epic's proposal that leads into the Acme Verified "
                    "authentication partnership. Invent ticket numbers and secondary comment "
                    "authors freely -- names, dates, and the seller must match CANON exactly. End "
                    "with a LEDGER 'incident' event dated 2025-08-04 for the spike."
                ),
                "parallel_ok": False,
            },
            {
                "path": "confluence/q3fy26__acme-verified-program-prd.md",
                "system": "confluence",
                "adapter": "confluence_page",
                "topic": "Confluence PRD: the 'Acme Verified' authenticity-badge program",
                "focus": (
                    "A Confluence PRD, owned by lucia.ferreira, for the 'Acme Verified' "
                    "authenticity-badge program -- partner: GradeSure -- which per CANON launches "
                    "2025-09-08. Write this as the PRD authored in the runup to that launch, "
                    "explicitly citing the Collectibles counterfeit epic and Bramblewood Vintage "
                    "suspension from earlier this round (via the LEDGER) as the motivating "
                    "incident. Cover partner selection (why GradeSure), badge design, rollout "
                    "plan, and success metrics (return-rate reduction target). End with a LEDGER "
                    "'launch' event dated 2025-09-08."
                ),
                "parallel_ok": False,
            },
            {
                "path": "jira/q3fy26__ask-acme-v2-bot-launch.md",
                "system": "jira",
                "adapter": "jira_ticket",
                "topic": "Jira release ticket: 'Ask Acme v2' customer-care deflection bot",
                "focus": (
                    "A Jira release ticket, owned by dominic.paquet (Care Ops Lead), for 'Ask Acme "
                    "v2', a revamped customer-support chatbot aimed at improving contact "
                    "deflection, launching 2025-09-15 per CANON. Independent of the Collectibles/"
                    "authentication thread elsewhere this round -- safe to generate without seeing "
                    "those docs. Include rollout scope, the deflection metric it's meant to move, "
                    "and a handful of routine release-process comments. End with a LEDGER 'launch' "
                    "event dated 2025-09-15."
                ),
                "parallel_ok": True,
            },
            {
                "path": "aitable/q3fy26__legacy-roadmap-speed-membership.md",
                "system": "aitable",
                "adapter": "aitable_card",
                "topic": "Aitable roadmap export: Speed and Membership initiative cards (legacy tracker)",
                "focus": (
                    "An export of Aitable roadmap cards -- the legacy roadmap tracker, still the "
                    "system of record this quarter, administered by nadia.esposito's Product Ops "
                    "team -- covering Speed/fulfillment initiatives (owners like tara.oduya, "
                    "leo.brandt) and Membership initiatives (simone.laurent, derek.holloway). Card "
                    "fields: owner, status, target quarter, linked PRD; a mix of shipped, "
                    "in-progress, and abandoned cards. Purely noise/context for this round -- no "
                    "dependency on the other Q3 docs. Mention in passing, as background chatter "
                    "rather than a headline, that there's talk of eventually moving this tracker "
                    "to Jira."
                ),
                "parallel_ok": True,
            },
            {
                "path": "expo/q3fy26__exp-verified-badge-prominence-kickoff.md",
                "system": "expo",
                "adapter": "expo_experiment",
                "topic": "Expo experiment spec: 'Verified Badge Prominence' on Collectibles listings",
                "focus": (
                    "An experiment kickoff spec (hypothesis, variants, primary metric, guardrail "
                    "metrics, target sample size) for 'Verified Badge Prominence' (exp_2401), "
                    "owned by sanjay.bhatt, starting 2025-10-01 per CANON, making the Acme Verified "
                    "authenticity badge more prominent on Collectibles listings. This follows "
                    "directly from the PRD earlier this round "
                    "-- cite it and reuse the program name rather than inventing a new one. This is "
                    "a kickoff spec only (the experiment is still running as of this round's "
                    "as-of date, 2025-10-15) -- do NOT report a readout or ship decision yet, that "
                    "belongs to a later round. End with a LEDGER 'experiment' event dated "
                    "2025-10-01."
                ),
                "parallel_ok": False,
            },
            {
                "path": "marketing_calendar/q3fy26__fall-savings-acme-plus-join-promo.md",
                "system": "marketing_calendar",
                "adapter": "marketing_calendar_export",
                "topic": "Marketing calendar: 'Fall Savings' Acme+ join promo",
                "focus": (
                    "Marketing calendar entry, owned by simone.laurent (Director PM Membership), "
                    "for the 'Fall Savings' Acme+ join promotion running 2025-09-20 through "
                    "2025-10-15 per CANON. Include channel mix, target segment (non-members "
                    "browsing during peak fall shopping prep), and the internal signup-lift goal. "
                    "Note in passing, as a small aside not a headline, that mem_1000640 'Oskar' "
                    "signs up via this exact promo (per CANON's member archetypes) -- just tag the "
                    "acquisition_channel on new signups, do NOT state his later 2-benefit-adopter/"
                    "reliable-renewal outcome, that's a much later cohort read. Independent of the "
                    "other Q3 threads. End with a LEDGER 'launch' event dated 2025-09-20, vertical "
                    "MEMBERSHIP, owner simone.laurent."
                ),
                "parallel_ok": True,
            },
            {
                "path": "fullstory/q3fy26__collectibles-listing-trust-signals-session-review.md",
                "system": "fullstory",
                "adapter": "fullstory_session_note",
                "topic": "FullStory session-replay note: buyer hesitation signals on unverified Collectibles listings",
                "focus": (
                    "A FullStory session-replay note, from sanjay.bhatt's team, reviewing buyer "
                    "session replays on Collectibles listings during the counterfeit-spike "
                    "aftermath (reference the epic and Bramblewood suspension via this round's "
                    "LEDGER) -- observing hesitation patterns (repeated listing/seller-profile "
                    "back-and-forth, abandoned carts on high-value ungraded items) that motivate "
                    "testing a more prominent authenticity badge. This is the qualitative "
                    "groundwork feeding sanjay.bhatt's rationale for kicking off `exp_2401` this "
                    "same round. Emits no new event (qualitative input, not a dated milestone) -- "
                    "empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "gong/q3fy26__gradesure-partnership-scoping-call.md",
                "system": "gong",
                "adapter": "gong_call",
                "topic": "Gong call transcript: GradeSure partnership scoping call",
                "focus": (
                    "A vendor scoping call transcript between lucia.ferreira (+ sanjay.bhatt) and "
                    "GradeSure's partnership team, in the runup to the 2025-09-08 Acme Verified "
                    "launch (reference that LEDGER launch event and the Collectibles counterfeit "
                    "epic as motivating context, both from earlier this round). Cover integration "
                    "approach (intake hubs, digital cert linking for listings above $250), a "
                    "plausible pricing/rev-share structure (invent specifics, not in CANON), and a "
                    "rollout timeline matching the actual 2025-09-08 launch date. Ordinary "
                    "vendor-call noise. Emits no new event (the launch is already logged by this "
                    "round's PRD doc) -- empty LEDGER array."
                ),
                "parallel_ok": False,
            },
        ],
    },
    {
        "name": "q4fy26",
        "date": "2026-01-25",  # fiscal Q4FY26 = Nov 2025 - Jan 2026
        "specs": [
            {
                "path": "medallia/q4fy26__voc-refund-delay-theme-emerging.md",
                "system": "medallia",
                "adapter": "medallia_verbatim",
                "topic": "Medallia VOC report: 'refund delay' verbatim theme climbing",
                "focus": (
                    "A Voice-of-Customer theme report, from giulia.romano's analytics team, "
                    "showing the 'refund delay' verbatim theme climbing from its ~3.5% baseline "
                    "share of care-related verbatims to cross 10% the week of 2025-12-15 per "
                    "CANON -- include a batch of representative raw verbatim quotes and a "
                    "week-over-week trend table. This is a leading indicator: nothing quantitative "
                    "has flagged the underlying refund-cycle problem yet, so this should read as "
                    "an early, still-easy-to-dismiss signal, not a five-alarm fire. End with a "
                    "LEDGER 'metric_shift' event dated 2025-12-15."
                ),
                "parallel_ok": False,
            },
            {
                "path": "jira/q4fy26__returns-center-staffing-investigation.md",
                "system": "jira",
                "adapter": "jira_ticket",
                "topic": "Jira ticket: refund-cycle-time SLA breach, returns-center staffing investigation",
                "focus": (
                    "A Jira ticket, owned by hannah.brennan (SVP Customer Care), opened when the "
                    "quantitative 4-week-rolling avg_refund_cycle_days metric crosses its 5.0-day "
                    "SLA alert threshold the week of 2026-01-05 per CANON -- three weeks AFTER "
                    "giulia.romano's Medallia theme report from earlier this round already flagged "
                    "the same problem qualitatively (cite that LEDGER event explicitly; a comment "
                    "should note VOC saw this coming first). The comment thread should trace "
                    "toward -- but not yet conclusively pin down -- a specific returns-processing "
                    "site (Ontario, CA) running understaffed through peak, hinting at a "
                    "hiring-freeze-exception gap without fully resolving it. Leave this ticket "
                    "still-open at the end of the round -- the formal root-cause-and-fix lands at "
                    "the Feb 2 MBR, a later round's document. End with a LEDGER 'incident' event "
                    "dated 2026-01-05."
                ),
                "parallel_ok": False,
            },
            {
                "path": "confluence/q4fy26__dc-automation-and-promise-window-rollout-plan.md",
                "system": "confluence",
                "adapter": "confluence_page",
                "topic": "Confluence rollout plan: DC sortation automation + a concurrent delivery-promise experiment",
                "focus": (
                    "A Confluence rollout-planning page covering TWO things landing at the same "
                    "two distribution centers -- FON2 (Fontana) and JOL1 (Joliet) -- in the same "
                    "week of 2026-01-12 per CANON: gabriel.stroud's DC sortation-automation "
                    "hardware/software rollout (Phase 1, phased through 2026-02-15), and -- "
                    "separately owned by leo.brandt, separately motivated -- the 'Wider Promise "
                    "Window' experiment (exp_1187) widening the delivery-estimate window shown to "
                    "customers. Write them as two genuinely separate initiatives that happen to "
                    "share a rollout window and DC footprint -- do not have the authors notice the "
                    "overlap themselves (that recognition belongs to a later document, once both "
                    "wrap). End with a LEDGER block with BOTH as separate events dated 2026-01-12 "
                    "(kind 'launch' for the automation, 'experiment' for the promise-window test)."
                ),
                "parallel_ok": True,
            },
            {
                "path": "jira/q4fy26__roadmap-tracker-migration-cutover.md",
                "system": "jira",
                "adapter": "jira_ticket",
                "topic": "Jira ticket: roadmap-tracking migration cutover from Aitable to Jira",
                "focus": (
                    "A Jira ticket/announcement, from nadia.esposito's Product Ops team, declaring "
                    "2026-01-15 (per CANON) as the cutover after which new roadmap items are "
                    "tracked in Jira instead of Aitable (the legacy tracker -- reference the "
                    "earlier LEDGER event), with a note that existing Aitable cards will be "
                    "migrated 'over time'. Be honest that migration is NOT instantly complete -- "
                    "don't claim the old tracker is immediately empty. End with a LEDGER "
                    "'decision' event dated 2026-01-15."
                ),
                "parallel_ok": True,
            },
            {
                "path": "marketing_calendar/q4fy26__pickup-perks-campaign-launch.md",
                "system": "marketing_calendar",
                "adapter": "marketing_calendar_export",
                "topic": "Marketing calendar: 'Pickup Perks' BOPIS/curbside discount campaign",
                "focus": (
                    "Marketing calendar entries, owned by tara.oduya (Director PM Speed & "
                    "Fulfillment), for the 'Pickup Perks' discount campaign promoting "
                    "buy-online-pickup-in-store / curbside orders, launching 2026-01-15 per "
                    "CANON. Include dates, channel mix, target segment, and the internal goal "
                    "(shift order mix toward pickup). Independent of the other Q4 threads. End "
                    "with a LEDGER 'launch' event dated 2026-01-15."
                ),
                "parallel_ok": True,
            },
            {
                "path": "expo/q4fy26__exp-verified-badge-prominence-readout-and-ship.md",
                "system": "expo",
                "adapter": "expo_experiment",
                "topic": "Expo experiment readout: 'Verified Badge Prominence' clean +6.8% lift, ships to 100%",
                "focus": (
                    "The readout for `exp_2401` ('Verified Badge Prominence,' Collectibles), owned "
                    "by sanjay.bhatt, closing out the kickoff from last round (reference that "
                    "LEDGER event). Per CANON: ends 2025-11-15 with a clean **+6.8%** conversion "
                    "lift on badge-prominent Collectibles listings, no concurrent launch or "
                    "marketing event overlapping the window in Collectibles -- an intentionally "
                    "uncomplicated, unconfounded result; do NOT invent a confound or hedge, a "
                    "clean win is fine to report as fully clean. Ships to 100% of Collectibles "
                    "listings 2025-11-20. Mention the Collectibles return-rate context (11.2% at "
                    "the counterfeit peak, already stabilizing) as supporting color. This is the "
                    "direct, load-bearing source for 'did the authentication-badge test move the "
                    "needle' -- state the clean result plainly, no manufactured caveat. End with a "
                    "LEDGER block with TWO events: the readout (2025-11-15, kind 'experiment') and "
                    "the 100% ship (2025-11-20, kind 'launch')."
                ),
                "parallel_ok": True,
            },
            {
                "path": "marketing_calendar/q4fy26__black-friday-cyber-monday-peak-calendar.md",
                "system": "marketing_calendar",
                "adapter": "marketing_calendar_export",
                "topic": "Marketing calendar: Black Friday / Cyber Monday peak-holiday events",
                "focus": (
                    "Marketing calendar entries for Black Friday (2025-11-28, owned by "
                    "maya.lindqvist, US_CONV/all-verticals per CANON) and the Cyber Monday week "
                    "immediately after (beginning 2025-12-01) -- planned spend, channel mix, and "
                    "the expected seasonal volume spike. Note Q4FY26 is PACING toward a sharp "
                    "session jump (up from Q3's closed 437.0M US sessions) rather than stating the "
                    "quarter's own 598.0M figure as already-final -- the quarter doesn't close "
                    "until 2026-01-31, still days away from this round's date. State plainly this "
                    "is the fiscal peak/holiday quarter (Nov-Jan) by definition. Independent of the "
                    "other Q4 threads. End with a LEDGER 'event' entry dated 2025-11-28 for Black "
                    "Friday, vertical US_CONV, owner maya.lindqvist."
                ),
                "parallel_ok": True,
            },
            {
                "path": "postmortems/q4fy26__jol1-winter-storm-dc-disruption.md",
                "system": "postmortems",
                "adapter": "postmortem",
                "topic": "Postmortem: winter storm disrupts JOL1 (Joliet) distribution center for 36 hours",
                "focus": (
                    "An incident postmortem, owned by gabriel.stroud (Fulfillment Ops Lead), for a "
                    "winter storm disrupting the JOL1 (Joliet) DC for 36 hours starting 2025-12-08, "
                    "landing squarely in peak/Cyber-Monday-adjacent volume. Cover impact (delayed "
                    "outbound shipments, a temporary ship-to-home on-time-rate hit), root cause "
                    "(weather, not systemic), and recovery timeline. Frame this as ONE contributor, "
                    "alongside ordinary peak-volume strain, to a ship-to-home OTP dip PACING toward "
                    "roughly the mid-to-high-80s% for the quarter -- do not state Q4FY26's exact "
                    "final blended/ship-to-home OTP figures as already-closed (the quarter doesn't "
                    "close until 2026-01-31); do not claim the storm is the ONLY cause. Standard "
                    "postmortem structure with action items (e.g. a cold-weather contingency "
                    "staffing plan for next winter). End with a LEDGER 'incident' event dated "
                    "2025-12-08, vertical SPEED, owner gabriel.stroud."
                ),
                "parallel_ok": True,
            },
            {
                "path": "gong/q4fy26__peak-season-ops-review-call.md",
                "system": "gong",
                "adapter": "gong_call",
                "topic": "Gong call transcript: peak-season (Black Friday/Cyber Monday) ops review call",
                "focus": (
                    "An internal exec ops-review call, ben.tanaka (SVP Supply Chain & Fulfillment) "
                    "with gabriel.stroud and tara.oduya, held shortly after Cyber Monday week, "
                    "reviewing peak performance -- volume vs. plan and the JOL1 storm disruption "
                    "(reference that postmortem's LEDGER event from earlier this round). Include "
                    "early, vague chatter about ops scoping automation options for FON2/JOL1 next "
                    "quarter -- do NOT give it the exp_1187/DC-automation specifics yet (those land "
                    "in this round's existing Confluence rollout-plan doc, dated 2026-01-12, still "
                    "ahead of this call); keep this call's mention exploratory only. Ordinary call "
                    "noise. Emits no new event -- empty LEDGER array."
                ),
                "parallel_ok": False,
            },
            {
                "path": "jira/q4fy26__bramblewood-vintage-reinstatement-compliance-review.md",
                "system": "jira",
                "adapter": "jira_ticket",
                "topic": "Jira ticket: Bramblewood Vintage (sel_500089) reinstated after compliance review",
                "focus": (
                    "A Jira ticket, owned by lucia.ferreira, closing out the compliance review "
                    "opened when Bramblewood Vintage (sel_500089) was suspended 2025-09-02 "
                    "(reference that LEDGER event from two rounds ago). Per CANON, the seller is "
                    "reinstated 2026-01-15 after completing the review -- cover what the review "
                    "required (documentation audit, corrected sourcing practices) and any "
                    "conditions attached (e.g. a probationary monitoring period). Note this lands "
                    "on the SAME date as the Aitable-to-Jira roadmap cutover (pure coincidence of "
                    "timing, unrelated systems) -- do NOT have the author remark on the coincidence, "
                    "per this corpus's convention of separate initiatives not noticing shared "
                    "timing themselves. End with a LEDGER 'decision' event dated 2026-01-15, "
                    "vertical MARKETPLACE, owner lucia.ferreira."
                ),
                "parallel_ok": True,
            },
            {
                "path": "meetings/q4fy26__ask-acme-v2-first-quarter-launch-review.md",
                "system": "meetings",
                "adapter": "meeting_notes",
                "topic": "Launch-review sync notes: Ask Acme v2's first full quarter",
                "focus": (
                    "Meeting notes from a launch-review sync, dominic.paquet (Care Ops Lead) "
                    "presenting Ask Acme v2's performance since the 2025-09-15 launch (reference "
                    "that LEDGER event from two rounds ago) -- deflection has risen 39.5% (Q2FY26) "
                    "-> 42.8% (Q3FY26) -> and is QTD-trending toward roughly 45% this quarter per "
                    "CANON (do not state Q4FY26's deflection as a final closed number -- the "
                    "quarter doesn't close until 2026-01-31), alongside CSAT-deflected softening "
                    "slightly (3.80 -> 3.70 QTD). Present this as encouraging but NOT yet claim the "
                    "bot is solely responsible -- deflection was already climbing pre-bot (+2.3pp "
                    "the prior quarter), state that caveat plainly, seeding the inferential-"
                    "attribution point a later cross-quarter read will need to grapple with. "
                    "Routine meeting noise: attendees, next steps, next-review scheduling. End "
                    "with a LEDGER 'meeting' event dated 2026-01-20."
                ),
                "parallel_ok": True,
            },
            {
                "path": "query_logs/bulk__q3fy26-q4fy26-bq-audit-log.md",
                "system": "query_logs",
                "adapter": "bq_query_log",
                "bulk": True,  # BULK -- candidate for gen_grow.py's append-loop.
                "topic": "BigQuery analyst query audit log — Q3FY26 & Q4FY26 peak season (2025-08 through 2026-01)",
                "focus": (
                    "BULK export, target 120-180KB. 200+ analyst queries spanning Q3FY26 and "
                    "Q4FY26 (the counterfeit spike, Acme Verified launch, Ask Acme v2, peak/"
                    "holiday volume, the emerging refund-delay problem), through this round's own "
                    "as-of date (do not extend past late January 2026). Heavier-than-usual traffic "
                    "against `fact_marketplace_listings`/`marketplace_seller_performance` "
                    "(Collectibles investigation queries -- some analysts correctly scaling panel "
                    "ratios against `marketplace_gmv_summary` per convention 5, some getting "
                    "corrected when they don't), `fact_care_contacts`/`care_deflection_daily` (Ask "
                    "Acme v2 monitoring), and `fact_orders` refund columns (early refund-cycle-days "
                    "pulls in December/January that show the metric CLIMBING without yet being "
                    "dramatically flagged, consistent with SIGNAL [voc-leads-quant] -- the "
                    "quantitative metric lags VOC). Include a couple of queries incorrectly "
                    "treating `dim_seller`/`fact_marketplace_listings` counts as the true "
                    "population (~38,000 true sellers vs. the ~2,500-seller panel), corrected "
                    "inline. Mostly noise; bury signal every 100-200 lines. NOTE: candidate for "
                    "gen_grow.py's append-loop to reach the target size."
                ),
                "parallel_ok": True,
            },
            {
                "path": "slack/bulk__q4fy26-returns-ops-and-peak-season-slack.md",
                "system": "slack",
                "adapter": "slack_thread",
                "bulk": True,  # BULK -- candidate for gen_grow.py's append-loop.
                "topic": "Slack archive: #returns-ops and #fulfillment-ops channels, peak season through the SLA breach (2025-11 through late Jan 2026)",
                "focus": (
                    "BULK export, target 100-150KB. A multi-channel Slack archive (#returns-ops "
                    "primary, crossover from #fulfillment-ops and #random) spanning Nov 2025 "
                    "through late January 2026 -- STOP before 2026-02-02 (the formal MBR "
                    "escalation is a LATER round's event, not yet happened from this document's "
                    "vantage). Cover: routine peak-season operational chatter, day-of reactions to "
                    "the JOL1 storm disruption (reference this round's postmortem LEDGER event), "
                    "informal grumbling in December about returns processing feeling backed up "
                    "(consistent with, but less formal than, giulia.romano's Medallia report and "
                    "hannah.brennan's Jira ticket already logged this round), and scattered "
                    "mentions of the Ontario, CA returns-processing center specifically running "
                    "short-staffed through peak (the eventual root cause -- buried as one aside "
                    "among many, never headlined). Heavy unrelated noise: holiday PTO scheduling, "
                    "a broken badge-reader ticket, office party planning, a running joke about a "
                    "mislabeled pallet. NOTE: candidate for gen_grow.py's append-loop to reach the "
                    "target size."
                ),
                "parallel_ok": False,
            },
        ],
    },
    {
        "name": "q1fy27",
        "date": "2026-04-15",  # fiscal Q1FY27 = Feb-Apr 2026
        "specs": [
            {
                "path": "expo/q1fy27__exp-checkout-simplify-nav-refresh-confound.md",
                "system": "expo",
                "adapter": "expo_experiment",
                "topic": "Expo experiment readout: checkout-simplification test, confounded mid-flight by a sitewide nav redesign",
                "focus": (
                    "An experiment readout, from owen.faust, for 'Checkout Simplify' (exp_2214, "
                    "2026-02-16 to 2026-03-30 per CANON). Midway through -- 2026-03-01 -- "
                    "maya.lindqvist's team ships 'Nav Refresh', a sitewide navigation redesign, "
                    "into BOTH arms at once (unrelated team, unrelated motivation), with a "
                    "5%-of-traffic 3-week no-launch holdback (exp_2215) carved out to measure its "
                    "effect independently (readout completes 2026-03-21). Report Checkout "
                    "Simplify's full-window lift AND flag that it's contaminated by Nav Refresh; "
                    "include enough of a pre-contamination sub-window breakdown (Feb 16-28) that a "
                    "reader could reconstruct a cleaner number. Ships to 100% 2026-04-06 on the "
                    "(contaminated) headline number anyway -- note that decision without "
                    "editorializing on it. End with a LEDGER block with THREE events: the Nav "
                    "Refresh launch (2026-03-01), the holdback readout (2026-03-21), and the "
                    "Checkout Simplify ship decision (2026-04-06)."
                ),
                "parallel_ok": False,
            },
            {
                "path": "jira/q1fy27__delivery-promise-experiment-kill-decision.md",
                "system": "jira",
                "adapter": "jira_ticket",
                "topic": "Jira ticket: delivery-promise-window experiment killed on a net-negative readout",
                "focus": (
                    "A Jira ticket, landing with tara.oduya, closing out 'Wider Promise Window' "
                    "(exp_1187) from two rounds ago (reference its LEDGER kickoff event, owned "
                    "then by leo.brandt, and the Confluence rollout plan that flagged it shared a "
                    "DC footprint/timing with gabriel.stroud's sortation-automation rollout). The "
                    "comment thread works through deconfounding the experiment's 2026-02-20 "
                    "full-window readout (+4.2pp on-time-hit-rate, confounded) from the "
                    "automation's effect, lands on a net-negative conclusion (worse conversion "
                    "from a less-attractive promise, without a clean offsetting on-time-rate win "
                    "once automation is backed out), and kills the test 2026-03-02 per CANON. End "
                    "with a LEDGER 'decision' event dated 2026-03-02."
                ),
                "parallel_ok": True,
            },
            {
                "path": "confluence/q1fy27__mbr-refund-delay-escalation-and-root-cause.md",
                "system": "confluence",
                "adapter": "confluence_page",
                "topic": "Confluence page: Monthly Business Review escalation of the refund-delay problem, root cause and fix",
                "focus": (
                    "A Confluence write-up, from hannah.brennan, of the 2026-02-02 Monthly "
                    "Business Review (per CANON) where the still-open returns-processing/"
                    "refund-delay ticket from two rounds ago (reference it via the LEDGER) finally "
                    "gets formally escalated -- note explicitly that the monthly review cadence, "
                    "not the underlying rolling metric, is what triggered action, and that "
                    "giulia.romano's VOC report had flagged the same problem qualitatively even "
                    "earlier than the ticket did. Land on the root cause (the Ontario, CA "
                    "returns-processing center ran ~22% understaffed through peak because a "
                    "hiring-freeze exception that should have applied there didn't) and the fix "
                    "that follows (staffing restored 2026-02-20). End with a LEDGER 'decision' "
                    "event dated 2026-02-02 for the fix, and a 'metric_shift' event for the "
                    "metric's recovery."
                ),
                "parallel_ok": True,
            },
            {
                "path": "marketing_calendar/q1fy27__paid-search-budget-cut.md",
                "system": "marketing_calendar",
                "adapter": "marketing_calendar_export",
                "topic": "Marketing calendar: 18% paid-search budget cut (marketing-efficiency initiative)",
                "focus": (
                    "Marketing calendar entry (event_type: budget_change), owned by felix.arroyo "
                    "(SVP Product & Growth, who approves growth-marketing spend per CANON's ORG "
                    "section), for an 18% paid-search budget cut beginning 2026-02-04 -- an "
                    "explicit, DELIBERATE marketing-efficiency initiative, NOT a reaction to any "
                    "demand-side or competitive problem. State plainly this is expected to reduce "
                    "paid-search-driven sessions materially, a known and planned tradeoff against "
                    "near-term traffic in exchange for spend efficiency. This is the single most "
                    "load-bearing document explaining Q1FY27's US session decline -- write it "
                    "factually, without editorializing on whether it was the right call. "
                    "Standalone, independent decision. End with a LEDGER 'decision' event dated "
                    "2026-02-04, vertical MARTECH, owner felix.arroyo."
                ),
                "parallel_ok": True,
            },
            {
                "path": "dbt/q1fy27__sessions-definition-version-2-model-change.md",
                "system": "dbt",
                "adapter": "dbt_model",
                "topic": "dbt model change doc: sessions_definition_version 1→2 (bot/crawler filtering + de-dup)",
                "focus": (
                    "A dbt model-change/migration doc, owned by wei.hartono, describing the "
                    "2026-03-02 change to `fact_traffic_daily`'s session-counting logic: bot/"
                    "crawler traffic filtering plus multi-tab session de-duplication, bumping "
                    "`sessions_definition_version` from 1 to 2. Include the SQL logic change as a "
                    "code block, and an explicit callout -- matching CANON's SIGNAL "
                    "[session-definition] verbatim -- that this MECHANICALLY raises measured "
                    "conversion rate by shrinking the session denominator, independent of any real "
                    "behavior change, and that `traffic_conversion_summary` carries the version "
                    "flag forward ON PURPOSE rather than silently adjusting historical rows, so "
                    "anyone comparing conversion across the boundary must check the version column "
                    "first. Describe the mechanism and its forward effect; do NOT cite Q1FY27's "
                    "exact final closed conversion rate as if already settled (the quarter doesn't "
                    "close until 2026-04-30). This is the single most load-bearing document for the "
                    "definitional half of the 'did conversion really improve' question -- state the "
                    "mechanical-inflation point clearly and technically, not buried. End with a "
                    "LEDGER 'decision' event dated 2026-03-02, vertical US_CONV, owner wei.hartono."
                ),
                "parallel_ok": True,
            },
            {
                "path": "expo/q1fy27__exp-bot-handoff-threshold-kickoff.md",
                "system": "expo",
                "adapter": "expo_experiment",
                "topic": "Expo experiment spec: 'Bot Handoff Threshold' kickoff (Care)",
                "focus": (
                    "An experiment kickoff spec (hypothesis, variants, primary metric = deflection "
                    "rate, guardrail = CSAT among escalated contacts, sample size), for 'Bot "
                    "Handoff Threshold' (`exp_2489`), owned by aisha.rahman (Director PM Care, "
                    "Automate/Avoid), starting 2026-04-01 per CANON -- testing a later hand-off-to-"
                    "human threshold in the Ask Acme v2 bot flow (reference its 2025-09-15 launch "
                    "LEDGER event) to push deflection higher. Kickoff spec only -- the experiment "
                    "is still running as of this round's as-of date (2026-04-15); do NOT report a "
                    "readout yet (it lands 2026-05-15, a later round). Note the guardrail metric "
                    "explicitly: CSAT-among-deflected is already a sensitive area this fiscal year "
                    "(the Q4FY26 refund-delay dip, now recovering per this round's MBR doc), so the "
                    "team is watching guardrails carefully. End with a LEDGER 'experiment' event "
                    "dated 2026-04-01, vertical CARE, owner aisha.rahman."
                ),
                "parallel_ok": True,
            },
            {
                "path": "confluence/q1fy27__style-conversion-recovery-plan-draft-abandoned.md",
                "system": "confluence",
                "adapter": "confluence_page",
                "topic": "Confluence draft (undated, circa Q1FY27): 'Style Conversion Recovery Plan' — never actioned",
                "focus": (
                    "An undated/lightly-dated draft page, authored by ines.delgado (Sr PM "
                    "Marketplace Style), proposing to move Trust & Safety headcount off "
                    "Collectibles onto Style in response to Style's deceleration -- QTD/pacing "
                    "toward roughly +6% YoY this quarter, well below the ~10% planned trend (per "
                    "CANON; do not state the precise final +6.1% as an already-closed number, the "
                    "quarter doesn't close until 2026-04-30). Write it as a genuinely-argued draft "
                    "that circulated for comment but was ultimately SET ASIDE / never actioned -- "
                    "do NOT resolve within this document WHY it was set aside (that cross-vertical "
                    "realization belongs to later synthesis, not this Style-siloed draft, which "
                    "should read as reasonable-at-the-time). Name sel_500103 Kestrel & Vine as the "
                    "specific large Style account cited in the headcount ask, per CANON. Include a "
                    "comment thread with mixed reactions but no final decision recorded. End with "
                    "a LEDGER 'event' entry (kind 'event', not 'decision' -- it was never decided) "
                    "dated 2026-03-15 for 'draft circulated, no action taken', vertical "
                    "MARKETPLACE, owner ines.delgado."
                ),
                "parallel_ok": True,
            },
            {
                "path": "fullstory/q1fy27__checkout-funnel-drop-off-pre-experiment-review.md",
                "system": "fullstory",
                "adapter": "fullstory_session_note",
                "topic": "FullStory session-replay note: checkout funnel drop-off review ahead of Checkout Simplify",
                "focus": (
                    "A FullStory session-replay note from owen.faust's team, reviewing checkout "
                    "funnel session replays in early February 2026, just ahead of the 'Checkout "
                    "Simplify' experiment kickoff (2026-02-16, already in this round's LEDGER) -- "
                    "describing the specific friction points the experiment variant addresses "
                    "(redundant form steps, an unclear guest-checkout path), building on the "
                    "qualitative groundwork from a similar Q2FY26 review. Keep this dated BEFORE "
                    "2026-02-16 in-narrative (early Feb) even though the round's fetched_at is "
                    "later -- frame it as 'the review that fed the experiment design,' written "
                    "contemporaneously and only exported now. Emits no new event -- empty LEDGER "
                    "array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "medallia/q1fy27__voc-refund-delay-theme-recovery.md",
                "system": "medallia",
                "adapter": "medallia_verbatim",
                "topic": "Medallia VOC report: 'refund delay' theme share recovering post-fix",
                "focus": (
                    "A follow-up VOC theme report from giulia.romano's team, tracking the 'refund "
                    "delay' verbatim theme AFTER the Ontario staffing fix (reference the "
                    "2026-02-02 MBR escalation and 2026-02-20 staffing-restored LEDGER events from "
                    "this round) -- showing the theme share declining back down from its 16.1% "
                    "week-of-2026-01-05 peak toward baseline as the backlog clears through March "
                    "2026. Frame this as the qualitative confirmation the fix worked, giving VOC a "
                    "full-circle role (flagged it first, confirms the recovery last). Include "
                    "representative verbatims showing the tone shift. End with a LEDGER "
                    "'metric_shift' event dated 2026-03-15 for the theme-share recovery, vertical "
                    "CARE, owner giulia.romano."
                ),
                "parallel_ok": False,
            },
            {
                "path": "slack/q1fy27__eng-checkout-nav-refresh-timing-overlap-thread.md",
                "system": "slack",
                "adapter": "slack_thread",
                "topic": "Slack thread: engineering notices Checkout Simplify and Nav Refresh timing overlap",
                "focus": (
                    "A #product-eng Slack thread where an engineer on maya.lindqvist's Nav "
                    "Refresh team casually flags to owen.faust's Checkout Simplify team that their "
                    "two changes are about to overlap in production (Nav Refresh launching "
                    "2026-03-01 into both Checkout Simplify arms, per this round's existing LEDGER "
                    "events) -- a real-time, informal version of the confound the formal readout "
                    "doc analyzes in full. Keep this appropriately uncertain/informal ('hey, "
                    "doesn't this mess with your readout?') rather than fully resolving the "
                    "analysis -- that resolution belongs to the formal readout doc. Ordinary Slack "
                    "noise around it. Emits no new event -- empty LEDGER array."
                ),
                "parallel_ok": False,
            },
            {
                "path": "query_logs/bulk__q1fy27-bq-audit-log.md",
                "system": "query_logs",
                "adapter": "bq_query_log",
                "bulk": True,  # BULK -- candidate for gen_grow.py's append-loop.
                "topic": "BigQuery analyst query audit log — Q1FY27 (2026-02 through the round's April 15 as-of date)",
                "focus": (
                    "BULK export, target 100-150KB. 180+ analyst queries across Q1FY27 QTD -- "
                    "heavy activity around the paid-search-cut/session-definition-change period "
                    "(analysts pulling `fact_traffic_daily`/`traffic_conversion_summary`, some "
                    "naively comparing pre/post 2026-03-02 conversion without checking "
                    "`sessions_definition_version`, corrected inline per SIGNAL "
                    "[session-definition]), Checkout Simplify / Nav Refresh monitoring queries "
                    "against `fact_experiment_exposures`/`fact_experiment_readouts` (including one "
                    "query using ASSIGNED units instead of EXPOSED units and getting a diluted "
                    "number, corrected per SIGNAL [assigned-vs-exposed]), and Wider Promise Window "
                    "/ DC automation queries against `fulfillment_speed_daily`. Include a flash-"
                    "estimate query early in the quarter landing near the ~2.96% distractor figure "
                    "CANON describes (pre-full-reprocessing partial data), later superseded. "
                    "Mostly noise; bury signal every 100-200 lines. NOTE: candidate for "
                    "gen_grow.py's append-loop to reach the target size."
                ),
                "parallel_ok": True,
            },
            {
                "path": "confluence/q1fy27__marketplace-category-mix-shift-synthesis.md",
                "system": "confluence",
                "adapter": "confluence_page",
                "topic": "Confluence analysis: Marketplace category mix-shift — Style deceleration is a Resold wallet-share shift, not a demand problem",
                "focus": (
                    "A cross-vertical analysis page, jointly authored by victor.okonkwo's "
                    "Marketplace data partner (wei.hartono pulling the numbers) with input from "
                    "noah.kessler (Resold PM) and ines.delgado (Style PM), making the case CANON's "
                    "SIGNAL [marketplace-cannibalization] describes: Style GMV is QTD-tracking to "
                    "roughly +6.1% YoY this quarter (vs. an ~10% planned trend) while Resold is "
                    "QTD-tracking to roughly +90.9% YoY over the identical window, with Resold's "
                    "apparel/style-adjacent category share rising from 51% (year-ago) to ~62% -- a "
                    "within-marketplace wallet-share shift, not a demand loss, with total "
                    "Marketplace GMV pacing at ~117% of its FY27 goal. Explicitly reference and "
                    "gently supersede the earlier, Style-siloed 'Style Conversion Recovery Plan' "
                    "draft from earlier this round (via LEDGER) as an example of what the isolated "
                    "view gets wrong. This is the direct, load-bearing source for the correct "
                    "cross-vertical synthesis. End with a LEDGER 'decision' event dated 2026-04-10 "
                    "(the synthesis lands, superseding the earlier draft's framing, without a "
                    "formal headcount decision either way), vertical MARKETPLACE, owner "
                    "victor.okonkwo."
                ),
                "parallel_ok": False,
            },
        ],
    },
    {
        "name": "q2fy27",
        "date": "2026-07-20",  # fiscal Q2FY27 = May-Jul 2026, IN FLIGHT -- this is CANON's own "today"
        "specs": [
            {
                "path": "jira/q2fy27__exp-bot-handoff-threshold-readout-partial-ship.md",
                "system": "jira",
                "adapter": "jira_ticket",
                "topic": "Jira ticket: Bot Handoff Threshold readout — partial ship (non-billing only)",
                "focus": (
                    "A Jira ticket, owned by aisha.rahman, closing the loop on `exp_2489` 'Bot "
                    "Handoff Threshold' kicked off last round (reference that LEDGER event). Per "
                    "CANON: readout completes 2026-05-15 with **+3pp** deflection but **-0.15 "
                    "CSAT** among late-escalated users; the team decides on a partial ship "
                    "2026-05-20 -- non-billing categories only, explicitly holding back "
                    "billing-related contacts because CSAT sensitivity there is judged too high. "
                    "The comment thread should walk through the tradeoff honestly (real deflection "
                    "gain, real CSAT cost, reasoning for the category carve-out) rather than "
                    "presenting an unambiguous win. End with a LEDGER block with TWO events: the "
                    "readout (2026-05-15, kind 'experiment') and the partial-ship decision "
                    "(2026-05-20, kind 'decision'), vertical CARE, owner aisha.rahman."
                ),
                "parallel_ok": True,
            },
            {
                "path": "expo/q2fy27__exp-benefit-onboarding-carousel-readout.md",
                "system": "expo",
                "adapter": "expo_experiment",
                "topic": "Expo experiment readout: 'Benefit Onboarding Carousel' — +9pp 30-day benefit awareness",
                "focus": (
                    "An experiment readout, owned by derek.holloway (Sr PM Membership Benefits & "
                    "CLTV), for 'Benefit Onboarding Carousel' (`exp_2556`), running 2026-05-01 to "
                    "2026-06-15 per CANON. Report the genuine **+9pp** lift in 30-day benefit "
                    "awareness, and explicitly flag the renewal-rate readout is NOT yet valid -- "
                    "annual renewal needs roughly a 12-month/cohort lag, so no renewal-rate number "
                    "exists yet for this cohort (do not fabricate one). Tie this to the already-"
                    "established benefit-adoption-depth/renewal correlation (2+ benefits = 95% "
                    "renewal vs 71% free-shipping-only; streaming-bundle-alone = 93% despite only "
                    "34% awareness) as the validated mechanism justifying the expectation of a "
                    "future renewal lift, while being precise it isn't measured yet. End with a "
                    "LEDGER 'experiment' event dated 2026-06-15, vertical MEMBERSHIP, owner "
                    "derek.holloway."
                ),
                "parallel_ok": True,
            },
            {
                "path": "gong/q2fy27__reelstream-partnership-transition-call.md",
                "system": "gong",
                "adapter": "gong_call",
                "topic": "Gong call transcript: Acme+ streaming-perk partner transition, Vidora → Reelstream",
                "focus": (
                    "A vendor transition call transcript, renee.kowalski's team with a joint "
                    "Vidora-offboarding + Reelstream-onboarding session, covering the 2026-06-01 "
                    "partner switch per CANON -- catalog/integration handoff, member-facing "
                    "communication plan, and an explicit note that Reelstream's own retention/"
                    "renewal performance ISN'T independently validated yet (only 7 weeks live as of "
                    "'today,' 2026-07-20) -- reference CANON's own framing near-verbatim: the 93% "
                    "renewal figure is a category-level read spanning BOTH partner eras, not "
                    "Reelstream-specific. Ordinary vendor-call noise. End with a LEDGER 'launch' "
                    "event dated 2026-06-01, vertical MEMBERSHIP, owner renee.kowalski."
                ),
                "parallel_ok": True,
            },
            {
                "path": "meetings/q2fy27__q2fy27-mbr-fy27-goals-pace-review.md",
                "system": "meetings",
                "adapter": "mbr_deck_notes",
                "topic": "MBR notes: Q2FY27 QTD business review — FY27 goals pace-to-target",
                "focus": (
                    "The 'today' (2026-07-20) Monthly Business Review, presented by "
                    "carlos.figueroa and vertical SVPs, reviewing FY27 goal pace exactly per "
                    "CANON's Company-section goals table: total digital+marketplace GMV $7.62B "
                    "run-rate vs $7.53B target (101.2%, AHEAD); US conversion 3.22% QTD vs 3.35% "
                    "target (96.1%, BEHIND); US sessions ~1,540M run-rate vs 1,650M target (93.3%, "
                    "BEHIND); Marketplace GMV $3.89B run-rate vs $3.32B target (117.1%, AHEAD); "
                    "Care deflection 52.1% QTD vs 50.0% target (104.2%, AHEAD, CSAT caveat noted); "
                    "Speed blended OTP 93.00% QTD vs 93.5% target (99.5%, BEHIND, mix-shift caveat "
                    "noted); Acme+ members 14.62M pacing to ~15.05M vs 14.8M target (101.7%, "
                    "AHEAD); Acme+ renewal 87.2% vs 86.0% target (101.4%, BEAT). Explicitly label "
                    "Q2FY27 as QTD/pace (81 of 92 days elapsed, 88.0%), never a closed quarter. "
                    "Include FY26 full-year actuals as YoY reference ($3,976.6M conversion-channel "
                    "GMV, $2,968.0M Marketplace, $6,944.6M total). Standard MBR noise: attendance, "
                    "action items. End with a LEDGER 'meeting' event dated 2026-07-20."
                ),
                "parallel_ok": True,
            },
            {
                "path": "confluence/q2fy27__aitable-jira-migration-status-update.md",
                "system": "confluence",
                "adapter": "confluence_page",
                "topic": "Confluence status page: Aitable→Jira roadmap migration — still not complete",
                "focus": (
                    "A living Confluence status page, owned by nadia.esposito's Product Ops team, "
                    "giving an honest 'as of today' (2026-07-20) update on the Aitable-to-Jira "
                    "roadmap consolidation that kicked off 2026-01-15 (reference that LEDGER "
                    "event) -- state PLAINLY, matching CANON's SIGNAL [aitable-jira-split] and "
                    "timeline note verbatim, that migration is NOT complete more than six months "
                    "later: items opened before 2026-01-15 largely still live in Aitable, items "
                    "opened on/after live in Jira, Confluence PRDs span both eras. Include a "
                    "punch-list of what's left and why it's dragged (competing priorities, cards "
                    "without clear owners). Load-bearing source confirming the migration is still "
                    "incomplete -- state that clearly, don't soften it into 'almost done.' Emits no "
                    "new event (status update, not a new milestone) -- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "aitable/q2fy27__legacy-roadmap-remaining-unmigrated-cards.md",
                "system": "aitable",
                "adapter": "aitable_card",
                "topic": "Aitable roadmap export: remaining pre-2026-01-15 cards still not migrated to Jira",
                "focus": (
                    "An export of Aitable cards STILL not migrated to Jira as of 'today' "
                    "(2026-07-20) -- a genuine long tail: some abandoned/stale cards (no update in "
                    "months), a few still-active initiatives whose owners just haven't done the "
                    "administrative migration, spanning multiple verticals (a couple of old Speed "
                    "and Membership cards left over from the Q1FY26 export earlier in the corpus, "
                    "plus older Care/Marketplace ideation cards). Exists specifically to make 'a "
                    "query against only one ticketing system returns a partial roadmap' concrete "
                    "and real -- a reader who only queries Jira misses everything here. "
                    "Administered by nadia.esposito's team. Emits no new event -- empty LEDGER "
                    "array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "schema/q2fy27__dim-member-panel-vs-population-clarification.md",
                "system": "schema",
                "adapter": "bq_schema",
                "topic": "Schema reference note: dim_member panel size vs. true Acme+ population",
                "focus": (
                    "A short, precise schema/data-dictionary clarification note, owned by "
                    "wei.hartono, addressing a recurring question: `dim_member` holds exactly "
                    "120,000 rows, a representative panel (~0.82% sample) of the true ~14.62M "
                    "active Acme+ base as of Q2FY27 QTD (per CANON). State explicitly and "
                    "unambiguously that `COUNT(*)` on `dim_member` is NEVER the total membership "
                    "count, and that the true company-level total comes from the membership "
                    "system's own ledger (reflected in Company-section/MBR figures), never by "
                    "resumming a panel table -- this is THE direct, load-bearing source for the "
                    "single most structurally important gotcha in the schema. Extend the same "
                    "caveat to `dim_seller` (~2,500 of ~38,000 true), `fact_orders` (~400,000), "
                    "`fact_care_contacts` (~50,000), `fact_voc_responses` (~40,000), "
                    "`fact_marketplace_listings` (~35,000), `fact_membership_events` (~450,000), "
                    "per CANON's SIGNAL [sample-vs-population]. Dry, precise reference material. "
                    "Emits no new event -- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "dbt/q2fy27__member-cltv-dormant-population-explainer.md",
                "system": "dbt",
                "adapter": "dbt_model",
                "topic": "dbt model note: member_cltv dormant-member population and the $500 vs $625 join trap",
                "focus": (
                    "A dbt model documentation note, owned by wei.hartono, walking through "
                    "`member_cltv`'s canonical LEFT JOIN + COALESCE(0) construction with fresh "
                    "Q2FY27 framing -- 20% of the 120,000-member panel (24,000 members) show zero "
                    "trailing-12-month orders, still-active/still-paying but dormant; correct "
                    "average CLTV is $500/member, while an INNER JOIN wrongly computes $625/member "
                    "(a 25% overstatement) by silently dropping the dormant population. Frame this "
                    "explicitly as relevant to 'is Acme+ on track' -- goal-tracking metrics (member "
                    "count, renewal rate) are both AHEAD of FY27 target and structurally blind to "
                    "this dormant population, since dormant members haven't cancelled and still "
                    "count as active. Reference mem_1000178 'Marisol' by name as the canonical "
                    "dormant archetype per CANON. Emits no new event -- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "docs/q2fy27__clhs-parked-spec-status-note.md",
                "system": "docs",
                "adapter": "confluence_page",
                "topic": "Status note: 'Customer Lifetime Health Score' (CLHS) remains a parked/draft spec",
                "focus": (
                    "A brief internal status note, owned jointly by derek.holloway and "
                    "renee.kowalski, clarifying that 'Customer Lifetime Health Score' (CLHS) -- a "
                    "proposed composite membership-health score that keeps coming up in "
                    "conversation -- remains PARKED/draft as of 'today' (2026-07-20): no table, no "
                    "columns exist, per CANON's SIGNAL [clhs-parked]. State the current shipped "
                    "proxy instead: `member_cltv` plus benefit-adoption rate. Exists specifically "
                    "so a reader who encounters CLHS mentioned elsewhere has a clear, correct, "
                    "citable source confirming it isn't real yet. Emits no new event -- empty "
                    "LEDGER array."
                ),
                "parallel_ok": True,
            },
            {
                "path": "docs/q2fy27__compass-dashboard-gmv-restatement-note.md",
                "system": "docs",
                "adapter": "confluence_page",
                "topic": "Data-quality note: Compass dashboard's stale Q4FY26 Marketplace GMV figure",
                "focus": (
                    "A short internal data-quality note, owned by connor.blake (Data Engineer, "
                    "pipeline/freshness), documenting that the 'Compass' internal BI tool's cached "
                    "view (a PDT) may still show Q4FY26 Marketplace GMV as the stale flash-reported "
                    "**$952.4M** figure to anyone who hasn't forced a refresh, when the canonical, "
                    "mart-reconciled figure (after a February 2026 returns-timing reclass) is "
                    "**$975.0M** -- per CANON's SIGNAL [gmv-restatement]. Include instructions for "
                    "forcing a Compass refresh. Exists to make the $952.4M-vs-$975.0M distractor "
                    "self-correcting rather than a silent trap. End with a LEDGER 'decision' event "
                    "dated 2026-02-10 for the restatement itself (narrated retrospectively from "
                    "today's vantage), vertical MARKETPLACE, owner connor.blake."
                ),
                "parallel_ok": True,
            },
            {
                "path": "confluence/q2fy27__benefit-adoption-cltv-lever-analysis.md",
                "system": "confluence",
                "adapter": "confluence_page",
                "topic": "Confluence analysis: benefit-adoption depth is the strongest Acme+ CLTV lever",
                "focus": (
                    "A strategic analysis page, owned by derek.holloway, building the case per "
                    "CANON's SIGNAL [benefit-adoption-cltv]: members using 2+ Acme+ benefits renew "
                    "at 95% annually vs 71% for free-shipping-only members (a steep "
                    "71%->89%->95% gradient by adoption depth); the single strongest INDIVIDUAL "
                    "benefit is the streaming bundle at 93% renewal alone (spanning both the "
                    "Vidora and Reelstream eras -- reference this round's partner-switch LEDGER "
                    "event), despite only 34% of members even knowing they have it. Written as a "
                    "refreshed analysis ahead of the Q2FY27 MBR (reference that LEDGER event), "
                    "connecting this to why the Benefit Onboarding Carousel experiment (this round, "
                    "reference its LEDGER event) was a sound bet, and flagging the still-open next "
                    "step: a DEDICATED streaming-bundle awareness campaign hasn't been executed "
                    "yet, only tested via the carousel's general onboarding nudge. Mention "
                    "mem_1000042 'Dana' (power benefit-user, 4-year tenure, high CLTV) as the "
                    "archetype of full adoption. End with a LEDGER 'decision' event dated "
                    "2026-07-05 recommending a dedicated awareness campaign as the next concrete "
                    "step, vertical MEMBERSHIP, owner derek.holloway."
                ),
                "parallel_ok": False,
            },
            {
                "path": "docs/bulk__zendesk-style-care-ticket-export-2026-q2.md",
                "system": "docs",
                "adapter": "confluence_page",
                "bulk": True,  # BULK -- candidate for gen_grow.py's append-loop.
                "topic": "Bulk export: customer-care ticket archive (Zendesk-style), Q2FY27",
                "focus": (
                    "BULK export, target 80-120KB. A large export of individual customer-care "
                    "contact tickets (distinct from the aggregate `fact_care_contacts` mart) "
                    "spanning Q2FY27, covering the `automate`/`avoid`/`optimize`/`platform`/"
                    "`member_care` sub-programs and `chat`/`phone`/`bot`/`email` channels, "
                    "reflecting Q2FY27 QTD figures (1,180K contacts, 52.1% deflection, 3.55 "
                    "CSAT-deflected, 4.31 CSAT-agent-assisted, 7.4 min avg handle time per CANON). "
                    "Include a handful of tickets tagged to the Bot Handoff Threshold's non-"
                    "billing partial ship (reference this round's LEDGER event) and a couple of "
                    "member-care tickets referencing mem_1000390 'Jamal' (churn-risk, 2 open P1 "
                    "contacts, an NPS detractor response) and mem_1000512 'Grethe' (churned after "
                    "two late ship-to-home deliveries) by their CANON archetypes. Heavy "
                    "ticket-volume noise: routine order-status questions, address-change requests, "
                    "password resets. NOTE: candidate for gen_grow.py's append-loop to reach the "
                    "target size."
                ),
                "parallel_ok": False,
            },
            {
                "path": "slack/bulk__q2fy27-data-help-full-history-archive.md",
                "system": "slack",
                "adapter": "slack_thread",
                "bulk": True,  # BULK -- the richest noise/signal file in the corpus; strongest candidate for gen_grow.py's append-loop across multiple passes.
                "topic": "Slack archive: #data-help channel, full corpus history (2025-02 through 2026-07-20)",
                "focus": (
                    "BULK export, target 200-300KB -- mirror the sibling corpus's "
                    "bulk__slack-data-help-2025H2-2026Q1.md (309KB) in density and shape. A long "
                    "#data-help archive spanning nearly the WHOLE modeled window (Feb 2025 through "
                    "'today' 2026-07-20), wei.hartono/connor.blake/amara.shah/giulia.romano "
                    "fielding ad hoc analyst questions across every table and mart, interleaved "
                    "with heavy off-topic noise (#random-style tangents, PTO, office logistics, a "
                    "Looker-to-Compass-analog dashboard migration as fine background noise per "
                    "CANON's DISTRACTORS). Scatter CORRECT, buried restatements of essentially "
                    "every SIGNAL in CANON across different weeks/threads: flat-dataset rule, "
                    "sample-vs-population, the session-definition cutover, the CLTV join trap "
                    "($500 vs $625), the paid-search cut as the real Q1FY27 traffic driver, the "
                    "Checkout Simplify/Nav Refresh confound, the Wider Promise Window/DC-automation "
                    "confound, the OTP mix-shift, the VOC-leads-quant refund-delay lead time, the "
                    "Style/Resold wallet-share shift, the CLHS-parked status, the flat BigQuery "
                    "path correction. Each should appear ONCE, in passing, correctly, amid heavy "
                    "unrelated chatter -- roughly one signal per several hundred lines, exactly per "
                    "CANON's STYLE section. NOTE: candidate for gen_grow.py's append-loop -- likely "
                    "needs several passes to reach target size."
                ),
                "parallel_ok": True,
            },
            {
                "path": "gong/bulk__q2fy27-exec-and-partner-calls-archive.md",
                "system": "gong",
                "adapter": "gong_call",
                "bulk": True,  # BULK -- candidate for gen_grow.py's append-loop.
                "topic": "Gong call archive: exec and partner calls, full corpus history (2025-2026)",
                "focus": (
                    "BULK export, target 100-150KB. 15-20 call transcripts spanning the corpus's "
                    "history -- internal exec syncs (SVP staff, MBR-prep calls) and partner/vendor "
                    "calls (GradeSure, Vidora, Reelstream, a DC-automation hardware vendor for the "
                    "FON2/JOL1 rollout) -- lightly expanding on calls already referenced elsewhere "
                    "plus several net-new ones for texture (a Q3FY26 board-prep call, a Q4FY26 "
                    "peak-readiness call, a Q1FY27 growth-marketing efficiency call touching the "
                    "paid-search cut, a Q2FY27 marketplace category-mix review touching the "
                    "Style/Resold shift). Heavy call-transcript noise (scheduling, small talk, "
                    "tangents). Bury signal sparsely. NOTE: candidate for gen_grow.py's "
                    "append-loop."
                ),
                "parallel_ok": True,
            },
            {
                "path": "meetings/bulk__weekly-leadership-sync-notes-full-history.md",
                "system": "meetings",
                "adapter": "meeting_notes",
                "bulk": True,  # BULK -- candidate for gen_grow.py's append-loop.
                "topic": "Weekly leadership sync notes archive, full corpus history (2025-02 through 2026-07-20)",
                "focus": (
                    "BULK export, target 150-200KB. ~60-70 weekly (non-MBR) leadership sync "
                    "entries across the full modeled window, each a short dated set of bullet "
                    "points from vertical leads -- mirroring the sibling corpus's weekly-standup-"
                    "notes pattern but for Acme's product/ops leadership. Cover routine operational "
                    "chatter across ALL 16 verticals over time (giving the 11 light verticals "
                    "their metric-row/light-mention presence across many entries, never a "
                    "storyline), with the 5 deep verticals' major beats appearing as brief "
                    "one-line forward-pointers the week they happen (e.g. the week of the "
                    "counterfeit spike, the week Ask Acme v2 launches, the week the paid-search "
                    "cut begins) -- terse pointers, NOT full retellings (the full story lives in "
                    "the dedicated documents already in the corpus). Heavy mundane noise: "
                    "headcount updates, budget review scheduling, minor process changes, a "
                    "recurring joke about a leaky office ceiling. NOTE: candidate for "
                    "gen_grow.py's append-loop."
                ),
                "parallel_ok": True,
            },
            {
                "path": "query_logs/bulk__q2fy27-bq-audit-log.md",
                "system": "query_logs",
                "adapter": "bq_query_log",
                "bulk": True,  # BULK -- candidate for gen_grow.py's append-loop.
                "topic": "BigQuery analyst query audit log — Q2FY27 QTD (2026-05 through 2026-07-20)",
                "focus": (
                    "BULK export, target 100-150KB. 150+ analyst queries across Q2FY27 QTD -- "
                    "heavy activity around FY27 goal-pace reporting ahead of the 2026-07-20 MBR "
                    "(queries correctly pulling from Company-section-reconciling marts, never "
                    "re-deriving GMV from conversion rate per convention 2), Bot Handoff Threshold "
                    "and Benefit Onboarding Carousel experiment monitoring queries, and at least "
                    "one query explicitly demonstrating the `dim_member` COUNT(*)=120,000 mistake "
                    "getting corrected against the true ~14.62M base (a fresh instance of SIGNAL "
                    "[sample-vs-population]). Mostly noise; bury signal every 100-200 lines. NOTE: "
                    "candidate for gen_grow.py's append-loop."
                ),
                "parallel_ok": True,
            },
            {
                "path": "scratch/q2fy27__analyst-scratch-fy27-h1-close-notes.md",
                "system": "scratch",
                "adapter": "confluence_page",
                "topic": "Analyst scratch notes: H1FY27 close-out exploration ahead of the Q2FY27 MBR",
                "focus": (
                    "Informal scratch notes from amara.shah, prepping numbers ahead of the "
                    "2026-07-20 MBR (reference that LEDGER event) -- half-finished cross-checks of "
                    "the FY27 goal-pace figures, a correct but casually-stated aside re-deriving "
                    "that Marketplace's 117.1%-of-goal pace is being carried by Resold's "
                    "acceleration even as Style decelerates (a personal, informal echo of the "
                    "wallet-share-shift finding, stated in passing, not as a polished conclusion), "
                    "and a couple of dead-end tangents. Messy, realistic, non-linear. Emits no new "
                    "event -- empty LEDGER array."
                ),
                "parallel_ok": True,
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Small concurrency-safe helpers
# ---------------------------------------------------------------------------
_print_lock = threading.Lock()


def safe_print(msg: str) -> None:
    with _print_lock:
        print(msg, flush=True)


def estimate_tokens(text: str) -> int:
    """Rough chars/4 heuristic, used only when the API doesn't return usage
    (shouldn't happen) and for dry-run previews (no API call to ask)."""
    return max(1, len(text) // 4)


class PromptShown:
    """Thread-safe latch so --dry-run prints the full assembled prompt for
    exactly the first document it would generate, across the whole
    invocation (not once per round)."""

    def __init__(self):
        self._lock = threading.Lock()
        self._shown = False

    def show_once(self) -> bool:
        with self._lock:
            if self._shown:
                return False
            self._shown = True
            return True


class Limit:
    """Mutable --limit counter. Only run_round's single orchestrating thread
    mutates `remaining`; worker threads only read batch membership decisions
    made by that thread, so no lock is needed here. Under --concurrency > 1
    the cap is best-effort (a whole concurrent batch is admitted or not, so
    it can overshoot by up to batch size - 1) -- fine for what --limit is
    for here (cheap smoke tests), called out rather than engineered away."""

    def __init__(self, n: int | None):
        self.remaining = n


class CostTracker:
    def __init__(self):
        self._lock = threading.Lock()
        self.calls = 0
        self.prompt_tokens = 0
        self.output_tokens = 0

    def add(self, prompt_tokens: int, output_tokens: int) -> None:
        with self._lock:
            self.calls += 1
            self.prompt_tokens += prompt_tokens
            self.output_tokens += output_tokens

    def snapshot(self) -> tuple[int, int, int]:
        with self._lock:
            return self.calls, self.prompt_tokens, self.output_tokens

    @staticmethod
    def cost_usd(prompt_tokens: int, output_tokens: int) -> float:
        return (
            prompt_tokens / 1_000_000 * PRICE_IN_PER_1M_USD
            + output_tokens / 1_000_000 * PRICE_OUT_PER_1M_USD
        )

    def line(self) -> str:
        calls, pt, ot = self.snapshot()
        return (
            f"[running total: {calls} call(s), {pt:,} in / {ot:,} out tok, "
            f"${self.cost_usd(pt, ot):.4f}]"
        )


# ---------------------------------------------------------------------------
# LEDGER: persistence, filtering, rendering, extraction
# ---------------------------------------------------------------------------
REQUIRED_EVENT_FIELDS = ("date", "kind", "vertical", "owner", "summary")
LEDGER_FENCE_RE = re.compile(r"```\s*LEDGER\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)
_ledger_io_lock = threading.Lock()


def load_ledger() -> list[dict]:
    """Rebuild ledger state from disk. This -- plus which output files
    already exist -- is the entire resumability story; there is no separate
    run-state file that could go stale relative to it."""
    if not LEDGER_PATH.exists():
        return []
    events = []
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as e:
                safe_print(f"[ledger] WARN  LEDGER.jsonl line {lineno} malformed ({e}), skipped")
    return events


def append_ledger_events(events: list[dict]) -> None:
    """Durably append. Called before the doc file is written for the same
    document (see process_spec) so that a crash between the two duplicates
    an event on retry rather than silently losing it -- see the design note
    in process_spec for the tradeoff this encodes."""
    if not events:
        return
    with _ledger_io_lock:
        with LEDGER_PATH.open("a", encoding="utf-8") as f:
            for ev in events:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())


def filter_ledger(events: list[dict], as_of_date: str) -> list[dict]:
    """Events at or before as_of_date, chronological. ISO YYYY-MM-DD dates
    sort correctly as plain strings, no date parsing needed."""

    def key(ev):
        return ev.get("date") or "0000-00-00"

    return sorted((ev for ev in events if key(ev) <= as_of_date), key=key)


def render_ledger(events: list[dict]) -> str:
    if not events:
        return "(empty -- this is the first round; nothing has happened yet)"
    return "\n".join(
        f"- {ev.get('date', '????-??-??')} [{ev.get('kind', 'event')}/{ev.get('vertical', '?')}] "
        f"(owner: {ev.get('owner', '?')}) {ev.get('summary', '')}"
        for ev in events
    )


def extract_ledger_block(text: str, *, source_path: str, round_name: str) -> tuple[str, list[dict]]:
    """Pull the trailing ```LEDGER fenced JSON array off `text`, returning
    (text-with-block-removed, validated events). Defensive per the task
    spec: missing or malformed blocks are logged and treated as zero new
    events -- the document itself is always kept."""
    matches = list(LEDGER_FENCE_RE.finditer(text))
    if not matches:
        safe_print(f"    [ledger] WARN  {source_path}: no LEDGER block found -- 0 events extracted, document kept as-is")
        return text, []

    if len(matches) > 1:
        safe_print(f"    [ledger] WARN  {source_path}: {len(matches)} LEDGER blocks found, using the first and leaving the rest in the document")

    m = matches[0]
    cleaned = (text[: m.start()] + text[m.end():]).rstrip() + "\n"

    try:
        payload = json.loads(m.group(1).strip())
        if not isinstance(payload, list):
            raise ValueError("top-level LEDGER JSON is not an array")
    except (json.JSONDecodeError, ValueError) as e:
        safe_print(f"    [ledger] WARN  {source_path}: malformed LEDGER JSON ({e}) -- 0 events extracted, document kept")
        return cleaned, []

    events = []
    for idx, raw_ev in enumerate(payload):
        if not isinstance(raw_ev, dict):
            safe_print(f"    [ledger] WARN  {source_path}: event #{idx} is not an object, skipped")
            continue
        missing = [f for f in REQUIRED_EVENT_FIELDS if f not in raw_ev]
        if missing:
            safe_print(f"    [ledger] WARN  {source_path}: event #{idx} missing {missing}, skipped")
            continue
        events.append({
            "date": str(raw_ev["date"]),
            "kind": str(raw_ev["kind"]),
            "vertical": str(raw_ev["vertical"]),
            "owner": str(raw_ev["owner"]),
            "summary": str(raw_ev["summary"]),
            "source_path": source_path,
            "round": round_name,
        })
    return cleaned, events


# ---------------------------------------------------------------------------
# Prompt assembly
# ---------------------------------------------------------------------------
def build_prompt(spec: dict, round_meta: dict, ledger_events: list[dict]) -> str:
    slug = Path(spec["path"]).stem
    frontmatter = f"""---
title: "{spec['topic']}"
source_url: "internal://acme-ecomm/{spec['system']}/{slug}"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '{round_meta["date"]}T12:00:00+00:00'
adapter: {spec['adapter']}
---"""

    return f"""Generate the following document for Acme's internal corpus.

ROUND: {round_meta['name']}  (documents in this round are dated around {round_meta['date']})
SYSTEM OF RECORD: {spec['system']} ({SYSTEMS.get(spec['system'], 'unlisted system')})
DOCUMENT: {spec['topic']}

INSTRUCTIONS:
{spec['focus']}

YAML FRONTMATTER (put this at the very top, verbatim):
{frontmatter}

CANONICAL FACTS (frozen; never contradict):
{CANON_TEXT}

LEDGER -- everything that has happened at or before this round's date ({len(ledger_events)} event(s)). Reference naturally, stay consistent, do not contradict:
{render_ledger(ledger_events)}

NOW GENERATE THE FULL DOCUMENT for the {round_meta['name']} round. Be detailed and realistic for a
{spec['system']} document. Weave in references to relevant LEDGER events where natural instead of
writing as if in isolation.

At the very end, after all document content, append the LEDGER extraction block exactly as
instructed in the system prompt."""


def make_client() -> genai.Client:
    return genai.Client(vertexai=True, project=PROJECT, location=LOCATION)


# ---------------------------------------------------------------------------
# Per-document generation
# ---------------------------------------------------------------------------
def process_spec(
    client: genai.Client | None,
    spec: dict,
    round_meta: dict,
    ledger_snapshot: list[dict],
    tracker: CostTracker,
    *,
    dry_run: bool,
    prompt_shown: PromptShown,
) -> list[dict]:
    """Generate (or dry-run-preview) one document. Returns the list of new
    ledger events it introduced (empty for dry-run, skips, and failures).

    Caller (run_round) guarantees this is only called for specs whose output
    path does not already exist -- that's the resumability/idempotency gate,
    checked once, not re-checked here.
    """
    prompt = build_prompt(spec, round_meta, ledger_snapshot)

    if dry_run:
        est_in = estimate_tokens(prompt)
        if prompt_shown.show_once():
            safe_print(
                f"  DRY-RUN  {spec['path']}  (~{est_in:,} input tok est.) -- full assembled prompt below\n"
                + "-" * 70 + f"\n{prompt}\n" + "-" * 70
            )
        else:
            safe_print(f"  DRY-RUN  {spec['path']}  (~{est_in:,} input tok est.; prompt shown once above for the first doc only)")
        return []

    out_path = SOURCES_DIR / spec["path"]
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=MAX_OUTPUT_TOKENS,
                system_instruction=SYSTEM,
            ),
        )
        text = response.text or ""
        cleaned, events = extract_ledger_block(text, source_path=spec["path"], round_name=round_meta["name"])

        usage = getattr(response, "usage_metadata", None)
        prompt_tokens = getattr(usage, "prompt_token_count", None) or estimate_tokens(prompt)
        output_tokens = getattr(usage, "candidates_token_count", None) or estimate_tokens(text)

        # Durability boundary: ledger events land on disk BEFORE the doc
        # file. If the process crashes between these two writes, the doc
        # file is absent on restart, so it gets regenerated -- producing a
        # duplicate ledger entry (thematically consistent, since the retry
        # uses the same spec/prompt shape) rather than a silently missing
        # one. A duplicate is discoverable later (grep by source_path); a
        # silent gap in what future rounds see is not. That's the tradeoff;
        # see the return-report for the alternative ordering considered.
        append_ledger_events(events)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(cleaned, encoding="utf-8")

        tracker.add(prompt_tokens, output_tokens)
        size_kb = len(cleaned.encode("utf-8")) / 1024
        safe_print(f"  DONE   {spec['path']}  {size_kb:.0f}KB  +{len(events)} ledger event(s)  {tracker.line()}")
        return events

    except Exception as e:
        safe_print(f"  ERROR  {spec['path']}  {type(e).__name__}: {e} -- skipping, will retry next run")
        return []


def run_round(
    client: genai.Client | None,
    round_meta: dict,
    all_events: list[dict],
    tracker: CostTracker,
    *,
    dry_run: bool,
    limit: Limit,
    concurrency: int,
    prompt_shown: PromptShown,
) -> None:
    specs = round_meta["specs"]
    safe_print(f"\n=== round {round_meta['name']}  (as-of {round_meta['date']})  {len(specs)} spec(s) ===")
    for s in specs:
        tag = "||" if s.get("parallel_ok") else "->"
        note = ""
        if (SOURCES_DIR / s["path"]).exists():
            note += " [exists, will skip]"
        if s["system"] not in SYSTEMS:
            note += f" [warn: unregistered system {s['system']!r}]"
        safe_print(f"  {tag} {s['system']:<20} {s['path']}{note}")

    i = 0
    while i < len(specs):
        spec = specs[i]
        if (SOURCES_DIR / spec["path"]).exists():
            i += 1
            continue  # already reported as SKIP in the preview above

        if limit.remaining is not None and limit.remaining <= 0:
            safe_print(f"  STOP  --limit reached; {len(specs) - i} spec(s) left untouched this round")
            return

        # Batch this spec with however many immediately-following specs are
        # also marked parallel_ok, up to --concurrency and whatever's left
        # of --limit. Sequential (concurrency=1, the default) never batches.
        batch = [spec]
        i += 1
        if concurrency > 1 and spec.get("parallel_ok"):
            while (
                i < len(specs)
                and len(batch) < concurrency
                and specs[i].get("parallel_ok")
                and not (SOURCES_DIR / specs[i]["path"]).exists()
                and (limit.remaining is None or len(batch) < limit.remaining)
            ):
                batch.append(specs[i])
                i += 1

        # Everyone in this batch sees the SAME ledger snapshot (as-of the
        # round's date) -- by construction they don't need each other's
        # output, so there's no well-defined "before/after" between them.
        ledger_snapshot = filter_ledger(all_events, round_meta["date"])

        if len(batch) == 1:
            results = [process_spec(client, batch[0], round_meta, ledger_snapshot, tracker, dry_run=dry_run, prompt_shown=prompt_shown)]
        else:
            safe_print(f"  -- concurrent batch of {len(batch)}: {', '.join(s['path'] for s in batch)}")
            with ThreadPoolExecutor(max_workers=len(batch)) as ex:
                futures = [
                    ex.submit(process_spec, client, s, round_meta, ledger_snapshot, tracker, dry_run=dry_run, prompt_shown=prompt_shown)
                    for s in batch
                ]
                results = [f.result() for f in futures]

        for events in results:
            all_events.extend(events)
        if limit.remaining is not None:
            limit.remaining -= len(batch)


def main() -> None:
    parser = argparse.ArgumentParser(description="Chronological-round document generator for the acme-ecomm dataset.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--round", dest="round_name", metavar="NAME", help="Generate one round by name (see ROUNDS).")
    group.add_argument("--all", action="store_true", help="Generate every round in chronological order.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be generated + the first assembled prompt; makes no API calls.")
    parser.add_argument("--limit", type=int, default=None, metavar="N", help="Stop after touching N new documents, total across the invocation (skips due to existing files don't count).")
    parser.add_argument(
        "--concurrency", type=int, default=1, metavar="N",
        help="Max concurrent generations for consecutive specs marked parallel_ok within a round (default 1 = fully sequential, as expected).",
    )
    args = parser.parse_args()

    if args.concurrency < 1:
        parser.error("--concurrency must be >= 1")

    if args.round_name:
        rounds = [r for r in ROUNDS if r["name"] == args.round_name]
        if not rounds:
            known = ", ".join(r["name"] for r in ROUNDS)
            parser.error(f"unknown round {args.round_name!r}. known rounds: {known}")
    else:
        rounds = ROUNDS

    all_events = load_ledger()
    safe_print(f"Loaded {len(all_events)} existing ledger event(s) from {LEDGER_PATH}")
    safe_print(f"model={MODEL} project={PROJECT} location={LOCATION} dry_run={args.dry_run} concurrency={args.concurrency}")

    client = None if args.dry_run else make_client()
    tracker = CostTracker()
    limit = Limit(args.limit)
    prompt_shown = PromptShown()

    for round_meta in rounds:
        before = tracker.snapshot()
        run_round(client, round_meta, all_events, tracker, dry_run=args.dry_run, limit=limit, concurrency=args.concurrency, prompt_shown=prompt_shown)
        after = tracker.snapshot()
        d_calls, d_in, d_out = after[0] - before[0], after[1] - before[1], after[2] - before[2]
        if d_calls:
            safe_print(
                f"  -- round {round_meta['name']} subtotal: {d_calls} call(s), {d_in:,} in / {d_out:,} out tok, "
                f"${CostTracker.cost_usd(d_in, d_out):.4f}"
            )
        if limit.remaining is not None and limit.remaining <= 0:
            safe_print("--limit reached; stopping.")
            break

    calls, pt, ot = tracker.snapshot()
    safe_print(
        f"\n=== grand total: {calls} call(s), {pt:,} in-tok / {ot:,} out-tok, ${CostTracker.cost_usd(pt, ot):.4f} "
        f"(@ ${PRICE_IN_PER_1M_USD}/1M in, ${PRICE_OUT_PER_1M_USD}/1M out) ==="
    )


if __name__ == "__main__":
    main()
