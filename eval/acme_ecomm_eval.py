"""Evaluation harness for the Acme eCommerce Nexus demo.

Asks the 22 questions in datasets/acme-ecomm/QUESTIONS.md against a live Nexus
context via POST /query, then scores each answer against a checkable-assertion
rubric derived from that file's own "correct answer" / "reasoning chain" /
"the trap" structure — not a bare LLM-judge vibe score.

Scoring has three independent tiers, reported separately, never blended:
  1. Deterministic assertions  — literal/regex checks against concrete facts
     (numbers, table names, experiment ids, dates). Mechanical, reproducible.
  2. Trap markers              — literal/regex checks for the planted wrong
     answer. Scored independently of (1): an answer can contain the right
     fact AND the trap.
  3. Judge-graded criteria     — only for elements that genuinely cannot be
     checked mechanically (framing, emphasis, "declines to over-explain").
     Uses claude-sonnet-5 via Vertex AI. Labeled and reported separately.

Also reports citation counts and distinct source-file counts per answer, and
flags when a question needing N joined sources (from its own "Systems/tables
joined" line) scores fully despite citing fewer than N distinct files — the
"corpus leaked the answer into one document" signal.

Usage:
  # Show the full rubric derivation for all 22 questions. Zero API calls.
  python eval/acme_ecomm_eval.py --dry-run

  # Real run against a context (needs NEXUS_API_KEY — see --env-file)
  python eval/acme_ecomm_eval.py --context nexus-analyst-acme-ecomm-v1

  # Cheap partial runs
  python eval/acme_ecomm_eval.py --limit 3
  python eval/acme_ecomm_eval.py --question Q1 --question Q11

  # Skip judge calls (deterministic + trap only)
  python eval/acme_ecomm_eval.py --no-judge
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_API_BASE = "https://prod.nexus.pinecone.io/api/v0"
DEFAULT_CONTEXT_SLUG = "nexus-analyst-acme-ecomm-v1"
DEFAULT_ENV_PATH = Path("/Users/simon/repositories/nexus-analyst-demo/agent-nexus/.env")
DEFAULT_RESULTS_DIR = REPO_ROOT / "eval" / "results"

# Judge model — per task spec, claude-sonnet-5 via Vertex (claude-opus-5 is
# not available in this project). Region "global" per AnthropicVertex docs.
VERTEX_PROJECT_ID = "mission-control-350520"
VERTEX_REGION = "global"
JUDGE_MODEL = "claude-sonnet-5"
# List price $3.00/$15.00 per MTok; introductory $2.00/$10.00 through
# 2026-08-31 is active as of this writing. Cost estimates use list price
# (the conservative bound) and note the intro rate separately.
JUDGE_INPUT_RATE_PER_TOKEN = 3.00 / 1_000_000
JUDGE_OUTPUT_RATE_PER_TOKEN = 15.00 / 1_000_000
JUDGE_INPUT_RATE_PER_TOKEN_INTRO = 2.00 / 1_000_000
JUDGE_OUTPUT_RATE_PER_TOKEN_INTRO = 10.00 / 1_000_000

# Prod enforces one active query/search turn per project; a comparison_group
# exempts up to MAX_COMPARISON_TURNS (3, per the Nexus API's own constant)
# concurrent turns. A racing create gets a 409 that clears once the other
# query finishes — retry with backoff rather than treating it as fatal.
MAX_COMPARISON_TURNS = 3
_CREATE_MAX_ATTEMPTS = 6
_RETRY_BASE_S = 1.5
_POLL_INTERVAL_S = 1.5
# Server-side hard ceiling on a single query turn is 900s (15 min); mirror it
# as our default poll deadline rather than inventing a shorter one.
_DEFAULT_QUERY_TIMEOUT_S = 900


# --------------------------------------------------------------------------
# Rubric model
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Check:
    """One mechanically-checkable assertion: satisfied if ANY pattern matches."""

    id: str
    description: str
    patterns: tuple[str, ...]  # regex, case-insensitive, any-of semantics

    def evaluate(self, text: str) -> bool:
        return any(re.search(p, text, re.IGNORECASE) for p in self.patterns)


@dataclass(frozen=True)
class JudgeItem:
    """One criterion routed to the LLM judge because it cannot be checked mechanically."""

    id: str
    prompt: str


@dataclass(frozen=True)
class Question:
    id: str
    user_story: str
    question: str
    correct_answer_summary: str  # condensed reference given to the judge; not itself scored
    deterministic: tuple[Check, ...]
    trap: tuple[Check, ...]
    judge: tuple[JudgeItem, ...]
    expects_multi_source: bool
    min_expected_sources: int
    source_hint: str


def chk(id_: str, description: str, *patterns: str) -> Check:
    return Check(id=id_, description=description, patterns=patterns)


def jd(id_: str, prompt: str) -> JudgeItem:
    return JudgeItem(id=id_, prompt=prompt)


def mk_question(
    id_: str,
    user_story: str,
    question: str,
    correct_answer_summary: str,
    deterministic: tuple[Check, ...],
    trap: tuple[Check, ...],
    judge: tuple[JudgeItem, ...],
    expects_multi_source: bool,
    min_expected_sources: int,
    source_hint: str,
) -> Question:
    return Question(
        id=id_,
        user_story=user_story,
        question=question,
        correct_answer_summary=correct_answer_summary,
        deterministic=deterministic,
        trap=trap,
        judge=judge,
        expects_multi_source=expects_multi_source,
        min_expected_sources=min_expected_sources,
        source_hint=source_hint,
    )


# --------------------------------------------------------------------------
# The rubric — one entry per question in datasets/acme-ecomm/QUESTIONS.md.
#
# Every figure/name/date below is copied verbatim from that file (which
# states its numbers are "exact and cross-checked against CANON.md"), so the
# regex targets are grounded in the corpus's own source of truth, not
# invented. min_expected_sources is the count of distinct systems/tables the
# question's own "Systems/tables joined" line names — the join-completeness
# signal used to flag corpus leakage (see --dry-run output and score_answer).
# --------------------------------------------------------------------------

RUBRIC: list[Question] = [
    mk_question(
        "Q1",
        "US-1",
        "Our US conversion number was down about 40 basis points last week "
        "versus the week before — what happened, and does it matter to customers?",
        "Blended US conversion fell 3.24% (wk ending 2026-07-11) to 2.86% "
        "(wk ending 2026-07-18), -0.38pp/'~40bps'. Shift-share decomposition: "
        "~-0.24pp is device mix-shift (app session share 28.0%->37.6%, app "
        "converts structurally lower ~1.50% vs web ~4%); ~-0.14pp is a "
        "genuine, smaller web-conversion softening (4.00%->3.76%). Medallia "
        "verbatims tied to item-page sessions in the window skew toward the "
        "new autoplay media/carousel module ('cluttered', 'annoying "
        "autoplay', 'feels slower'). Neither the shipped roadmap nor the net "
        "in-flight-experiment effect explains the -0.14pp remainder — the "
        "honest answer says so instead of forcing a complete explanation.",
        (
            chk("q1_wk1_rate", "cites the week-of-07-11 blended rate 3.24%", r"3\.24\s*%"),
            chk("q1_wk2_rate", "cites the week-of-07-18 blended rate 2.86%", r"2\.86\s*%"),
            chk(
                "q1_net_move",
                "states the net move as -0.38pp / ~40bps",
                r"0\.38\s*pp",
                r"40\s*bps",
                r"40\s*basis\s*points",
            ),
            chk("q1_mix_effect", "isolates the mix-shift component at ~-0.24pp", r"0\.24\s*pp"),
            chk("q1_rate_effect", "isolates the real/rate component at ~-0.14pp", r"0\.14\s*pp"),
            chk(
                "q1_app_share",
                "cites the app session-share jump 28.0% -> 37.6%",
                r"28(\.0)?\s*%.{0,40}37\.6\s*%",
                r"37\.6\s*%",
            ),
            chk("q1_autoplay", "names the autoplay media/carousel module as the shopper-facing signal", r"autoplay"),
        ),
        (
            chk(
                "q1_trap_all_customer_exp",
                "frames the ENTIRE move as a customer-experience problem",
                r"entire(ly)?\s+(due to|caused by|a result of|explained by).{0,60}(experience|autoplay|cluttered)",
            ),
            chk(
                "q1_trap_autoplay_fully_explains",
                "credits the autoplay experiment with fully explaining the residual/real component",
                r"autoplay.{0,100}(fully|completely|entirely)\s+explains?",
                r"(fully|completely|entirely)\s+explain\w*.{0,100}autoplay",
            ),
        ),
        (
            jd(
                "q1_shopper_meaning_on_real_component",
                "The answer attaches the shopper-side meaning (VOC texture) specifically to the "
                "smaller REAL/rate component, not just as a generic caveat, and explicitly avoids "
                "forcing a complete/tidy explanation for the -0.14pp residual (acknowledges neither "
                "the roadmap nor the net experiment effect explains it, without inventing one that does).",
            ),
        ),
        True,
        3,
        "fact_traffic_daily (weekly, by device) + fact_voc_responses (Medallia) + "
        "dim_experiment/fact_experiment_readouts (cross-reference only)",
    ),
    mk_question(
        "Q2",
        "US-1",
        "US conversion looked like it recovered last quarter — what actually happened?",
        "Blended US conversion rose 3.05% (Q1FY26) -> 3.18% (Q1FY27), +0.13pp "
        "— looks like a clean win but isn't. On 2026-03-02 Acme changed "
        "session counting to exclude bot/crawler traffic and de-dupe "
        "multi-tab sessions (sessions_definition_version 1->2), which "
        "mechanically raises measured conversion. Real story is traffic, not "
        "conversion: US sessions fell -5.6% YoY (402.0M->379.5M) from an "
        "18% paid-search budget cut (Martech, Feb-Mar 2026); orders fell "
        "-1.6% YoY (12.261M->12.068M). Conversion 'improved' mostly on "
        "paper; demand cooled from a self-inflicted spend decision.",
        (
            chk("q2_q1fy26_rate", "cites Q1FY26 conversion 3.05%", r"3\.05\s*%"),
            chk("q2_q1fy27_rate", "cites Q1FY27 conversion 3.18%", r"3\.18\s*%"),
            chk("q2_move", "states the move as +0.13pp", r"0\.13\s*pp"),
            chk(
                "q2_definition_version",
                "names the sessions_definition_version cutover",
                r"sessions?_definition_version",
                r"session\s+(counting|definition)\s+chang",
            ),
            chk(
                "q2_cutover_date",
                "cites the 2026-03-02 cutover date",
                r"2026-03-02",
                r"march\s+2(nd)?,?\s+2026",
            ),
            chk("q2_sessions_yoy", "cites the -5.6% YoY session decline", r"5\.6\s*%"),
            chk(
                "q2_paid_search_cut",
                "names the 18% paid-search budget cut",
                r"18\s*%.{0,30}(paid[- ]search|budget)",
                r"paid[- ]search.{0,30}18\s*%",
            ),
            chk("q2_orders_yoy", "cites the -1.6% YoY orders decline", r"1\.6\s*%"),
        ),
        (
            chk(
                "q2_trap_clean_win",
                "reports the rate move as an unqualified 'clean win'/'real recovery' with no definitional caveat",
                r"clean\s+win",
                r"real\s+recovery",
                r"genuine\s+recovery",
            ),
        ),
        (
            jd(
                "q2_real_story_is_traffic",
                "The answer clearly identifies that the real quarter story is on the TRAFFIC/demand "
                "side (a self-inflicted paid-search cut), not a conversion-rate win, and treats the "
                "rate improvement as partly definitional rather than a customer-experience or "
                "competitive win.",
            ),
        ),
        True,
        3,
        "traffic_conversion_summary/fact_traffic_daily + dim_marketing_calendar (budget-cut event) + "
        "sessions_definition_version signal",
    ),
    mk_question(
        "Q3",
        "US-1",
        "Is our delivery-speed number actually getting better, or is something else going on?",
        "Blended OTP rose 91.65% (Q1FY26) -> 92.38% (Q1FY27), +0.73pp — a "
        "headline win. Decomposed by fulfillment_type, ship-to-home "
        "actually DECLINED slightly 89.50%->89.30% (-0.20pp). The entire "
        "blended improvement is mix-shift: pickup/BOPIS share rose "
        "21.0%->29.0% (+8.0pp), driven by the 'Pickup Perks' campaign "
        "(Jan 2026); pickup hits its promise ~99.6% near-automatically. "
        "Separately, 'Wider Promise Window' (exp_1187, 2026-01-12 to "
        "2026-02-20) was confounded by a concurrent DC sortation automation "
        "rollout at FON2/JOL1: confounded full-window reading +4.2pp OTP, "
        "deconfounded effect only +1.5pp, alongside a real -0.6% conversion "
        "cost; net negative, killed 2026-03-02.",
        (
            chk("q3_otp_q1fy26", "cites blended OTP Q1FY26 91.65%", r"91\.65\s*%"),
            chk("q3_otp_q1fy27", "cites blended OTP Q1FY27 92.38%", r"92\.38\s*%"),
            chk("q3_otp_move", "states the blended move as +0.73pp", r"0\.73\s*pp"),
            chk(
                "q3_ship_to_home_decline",
                "shows ship-to-home OTP DECLINED (89.50% -> 89.30%)",
                r"89\.5\s*0?\s*%.{0,60}89\.3\s*0?\s*%",
                r"89\.3\s*0?\s*%",
            ),
            chk(
                "q3_pickup_share",
                "cites the pickup/BOPIS share rise 21.0% -> 29.0%",
                r"21(\.0)?\s*%.{0,60}29(\.0)?\s*%",
                r"29(\.0)?\s*%",
            ),
            chk("q3_pickup_perks", "names the Pickup Perks campaign", r"pickup\s+perks"),
            chk("q3_exp_id", "cites the Wider Promise Window experiment id exp_1187", r"exp_1187"),
            chk("q3_confound_full", "cites the confounded full-window reading +4.2pp", r"4\.2\s*pp"),
            chk("q3_deconfound", "cites the deconfounded effect +1.5pp", r"1\.5\s*pp"),
            chk("q3_conv_cost", "cites the -0.6% conversion cost of the wider promise window", r"0\.6\s*%"),
        ),
        (
            chk(
                "q3_trap_blended_only",
                "reports on-time-to-promise as improving from the blended number alone",
                r"delivery\s+is\s+improving",
                r"on-time.{0,20}(up|improv\w+)\s+0\.7",
            ),
            chk(
                "q3_trap_confounded_causal",
                "cites the confounded +4.2pp as the clean causal effect of Wider Promise Window",
                r"4\.2\s*pp.{0,60}(clean|causal|the effect of|caused by)",
                r"(caused|drove|delivered)\s+.{0,40}4\.2\s*pp",
            ),
        ),
        (
            jd(
                "q3_two_mechanisms_not_conflated",
                "The answer keeps the two mechanisms distinct: pickup-mix-shift explains the blended "
                "OTP gain, while the DC-automation confound is specific to the Wider Promise Window "
                "experiment's readout — it does not conflate 'the DCs got better' with 'delivery got "
                "better'.",
            ),
        ),
        True,
        4,
        "fulfillment_speed_daily + dim_marketing_calendar (Pickup Perks) + dim_experiment "
        "(Wider Promise Window) + fact_promise_vs_actual",
    ),
    mk_question(
        "Q4",
        "US-1",
        "Are there early warning signs in customer feedback that our dashboards haven't caught yet?",
        "Yes. Medallia 'refund delay' verbatim theme crossed 10% share of "
        "care verbatims (vs ~3.5% baseline) the week of 2025-12-15 — 3 "
        "weeks before avg_refund_cycle_days (4-wk rolling) crossed its "
        "5.0-day SLA threshold (week of 2026-01-05, hit 5.03), and 7 weeks "
        "before formal MBR escalation on 2026-02-02. Root cause: Ontario, "
        "CA returns-processing center ran ~22% understaffed through peak (a "
        "hiring-freeze exception that should have applied didn't) — fixed "
        "shortly after the Feb 2 MBR, metric back to ~3.3 days by mid-March 2026.",
        (
            chk("q4_theme_share", "cites the refund-delay VOC theme crossing 10% share", r"10\s*%"),
            chk("q4_baseline", "cites the ~3.5% baseline share", r"3\.5\s*%"),
            chk(
                "q4_theme_date",
                "cites the week of 2025-12-15 as when VOC crossed",
                r"2025-12-15",
                r"december\s+15,?\s*2025",
            ),
            chk(
                "q4_sla_threshold",
                "cites the 5.0-day SLA alert threshold, crossed at 5.03",
                r"5\.0\d?\s*(day|-day)",
                r"5\.03",
            ),
            chk(
                "q4_sla_date",
                "cites the week of 2026-01-05 as when the quantitative metric crossed",
                r"2026-01-05",
                r"january\s+5,?\s*2026",
            ),
            chk("q4_lead_time_3wk", "states the 3-week VOC lead over the quantitative metric", r"3\s*weeks?"),
            chk(
                "q4_mbr_date",
                "cites the 2026-02-02 MBR escalation date",
                r"2026-02-02",
                r"february\s+2,?\s*2026",
            ),
            chk("q4_lead_time_7wk", "states the 7-week VOC lead over formal escalation", r"7\s*weeks?"),
            chk(
                "q4_root_cause",
                "names the Ontario returns-center understaffing (~22%) as root cause",
                r"ontario",
                r"22\s*%",
            ),
        ),
        (
            chk(
                "q4_trap_late_start",
                "dates the problem's start to early January/February, missing the mid-December VOC signal",
                r"start(ed|ing)?\s+in\s+(early\s+)?(january|february)",
                r"first\s+(noticed|flagged|identified)\s+in\s+(january|february)",
            ),
        ),
        (
            jd(
                "q4_leads_with_voc_not_quant",
                "The answer's headline framing credits VOC (qualitative feedback) with catching the "
                "signal FIRST, with the quantitative metric and formal escalation explicitly "
                "positioned as lagging it by the stated lead times — not merely mentioning all three "
                "dates without establishing which led which.",
            ),
        ),
        True,
        3,
        "fact_voc_responses (Medallia) + refund-cycle-time rolling metric (Care/POR) + "
        "returns-center staffing postmortem/timeline",
    ),
    mk_question(
        "Q5",
        "US-1",
        "Care contact deflection jumped this year — is that a good thing?",
        "Partly. Deflection rose 45.0% (Q4FY26) -> 49.6% (Q1FY27) -> 52.1% "
        "(Q2FY27 QTD), coinciding with 'Ask Acme v2' bot rollout (launched "
        "2025-09-15) — but attribution is inferential, not holdback-proven "
        "(deflection was already climbing pre-bot: +2.3pp prior quarter; "
        "first full post-launch quarter gained less, +2.2pp; the single "
        "largest jump +4.6pp lands 4+ months after launch). CSAT among "
        "deflected contacts DROPPED from 3.70 (Q4FY26) to 3.42 (Q1FY27) "
        "during the exact window the returns-processing understaffing (Q4) "
        "was live — a meaningful share of the Q1FY27 deflection reflects "
        "return-status inquiries pushed to self-serve tracking that "
        "couldn't tell the member when their refund was coming. "
        "Deflected-CSAT partially recovered to 3.55 by Q2FY27 QTD.",
        (
            chk("q5_deflection_q4fy26", "cites deflection Q4FY26 45.0%", r"45(\.0)?\s*%"),
            chk("q5_deflection_q1fy27", "cites deflection Q1FY27 49.6%", r"49\.6\s*%"),
            chk("q5_deflection_q2fy27", "cites deflection Q2FY27 QTD 52.1%", r"52\.1\s*%"),
            chk(
                "q5_bot_launch",
                "names the 'Ask Acme v2' bot and its 2025-09-15 launch date",
                r"ask\s+acme\s+v2",
                r"2025-09-15",
            ),
            chk(
                "q5_csat_drop",
                "cites deflected-CSAT dropping from 3.70 to 3.42",
                r"3\.70.{0,40}3\.42",
                r"3\.42",
            ),
            chk("q5_csat_recover", "cites deflected-CSAT partially recovering to 3.55 in Q2FY27 QTD", r"3\.55"),
            chk(
                "q5_largest_jump_post_launch",
                "notes the single largest jump (+4.6pp) lands months after the bot launch",
                r"4\.6\s*pp",
            ),
        ),
        (
            chk(
                "q5_trap_unambiguous_win",
                "reports deflection-rate-up as an unambiguous win without checking deflected-CSAT",
                r"unambiguous(ly)?\s+(good|positive|a\s+win)",
                r"clear(ly)?\s+(a\s+)?(good|positive)\s+(thing|sign|trend)",
            ),
            chk(
                "q5_trap_full_bot_credit",
                "credits the ENTIRE multi-quarter deflection rise to the bot with no holdback caveat",
                r"(entirely|fully|solely)\s+(due to|driven by|attributable to|because of).{0,40}bot",
            ),
        ),
        (
            jd(
                "q5_joins_csat_with_deflection",
                "The answer explicitly joins the deflection-rate trend with the deflected-CSAT trend "
                "for the SAME quarters, recognizes they moved in opposite directions during Q1FY27, "
                "and connects that to the returns-center staffing incident rather than treating "
                "deflection as a standalone metric.",
            ),
        ),
        True,
        3,
        "care_deflection_daily + fact_care_contacts + fact_voc_responses (overlap with Q4 incident)",
    ),
    mk_question(
        "Q6",
        "US-1",
        "How does conversion in Canada and Mexico compare to the US this quarter?",
        "Q2FY27 QTD: US 3.22%, CA 3.12%, MX 2.67%. CA tracks close to the "
        "US. MX runs meaningfully lower across the ENTIRE 6-quarter window "
        "(~2.5-2.7% throughout) — a stable, structural market-maturity gap, "
        "not a new or worsening trend. (Control — no manufactured trend.)",
        (
            chk("q6_us_rate", "cites US Q2FY27 QTD conversion 3.22%", r"3\.22\s*%"),
            chk("q6_ca_rate", "cites CA Q2FY27 QTD conversion 3.12%", r"3\.12\s*%"),
            chk("q6_mx_rate", "cites MX Q2FY27 QTD conversion 2.67%", r"2\.67\s*%"),
            chk(
                "q6_stability",
                "characterizes the MX gap as stable/structural across the full history, not a new decline",
                r"stable",
                r"structural",
                r"has\s+(always|consistently)\s+(been|run)\s+lower",
                r"not\s+a\s+(new|recent)\s+(trend|decline)",
            ),
        ),
        (
            chk(
                "q6_trap_new_decline",
                "frames MX's lower conversion as a recent/new decline or manufactures a root-cause narrative for it",
                r"(mx|mexico).{0,60}(declin\w+|worsening|dropp\w+|deteriorat\w+)",
                r"(recent|new)\s+(problem|issue|decline).{0,40}(mx|mexico)",
            ),
        ),
        (),
        False,
        1,
        "traffic_conversion_summary/fact_traffic_daily filtered by market — single-table lookup, "
        "deliberately simple control",
    ),
    mk_question(
        "Q7",
        "US-2",
        "Did anything we shipped or are shipping cause this conversion drop?",
        "No. The only launch in the drop window (07-11 to 07-18) is "
        "'Homepage Hero Banner Refresh' (2026-07-13) — homepage-only, no "
        "item-page/search overlap, and query-log/FullStory review shows no "
        "measurable conversion effect. No other roadmap item shipped in "
        "that window. None of the shipped-and-launched roadmap explains "
        "the move — the explanation lives elsewhere (device mix-shift + a "
        "modest real softening, see Q1). Distinct from in-flight "
        "EXPERIMENTS (see Q11), which are relevant but not the same thing "
        "as 'what launched'.",
        (
            chk(
                "q7_banner_name",
                "names 'Homepage Hero Banner Refresh' as the only launch candidate in the window",
                r"homepage\s+hero\s+banner",
            ),
            chk(
                "q7_banner_date",
                "cites the banner's 2026-07-13 launch date",
                r"2026-07-13",
                r"july\s+13,?\s*2026",
            ),
            chk(
                "q7_banner_scope",
                "notes the banner is homepage-only, with no item-page/search overlap",
                r"homepage[- ]only",
                r"no\s+(item[- ]page|search)\s+overlap",
            ),
            chk("q7_no_effect", "states there is no measurable conversion effect from the banner", r"no\s+measurable\s+(conversion\s+)?effect"),
            chk(
                "q7_answer_no",
                "concludes plainly that the shipped roadmap does NOT explain the drop",
                r"\bno\b.{0,60}(explain|caused|responsible|roadmap)",
                r"none\s+of\s+(the|this).{0,40}(roadmap|explains?)",
            ),
        ),
        (
            chk(
                "q7_trap_banner_blamed",
                "credits the Homepage Hero Banner Refresh with causing/explaining the drop on timing alone",
                r"(banner|hero\s+banner).{0,60}(caused|explains?|drove|responsible\s+for)\s+.{0,30}(drop|decline|decrease)",
            ),
        ),
        (
            jd(
                "q7_resists_something_must_be_responsible",
                "The answer explicitly resists the 'something must be responsible' instinct — stating "
                "plainly that no roadmap item explains the move rather than crediting the "
                "nearest-in-time launch by timing alone — and distinguishes this negative roadmap "
                "finding from the separate question of in-flight experiments.",
            ),
        ),
        True,
        3,
        "dim_marketing_calendar (Hero Banner + Item Page Iteration Program) + Jira/Aitable roadmap "
        "cross-reference + fact_traffic_daily",
    ),
    mk_question(
        "Q8",
        "US-2",
        "We ran a checkout redesign test this spring — did it work, and is it safe to keep rolling out?",
        "Checkout Simplify (exp_2214, 2026-02-16 to 2026-03-30, US) shows "
        "+2.1% conversion lift over its full window, shipped 100% on "
        "2026-04-06 on that number. But sitewide 'Nav Refresh' launched "
        "into BOTH arms on 2026-03-01 (mid-experiment) and independently "
        "lifted conversion ~+1.3% sitewide (measured via its own "
        "5%-of-traffic no-launch holdback, exp_2215, held 3 weeks). "
        "Everything after March 1 is confounded. The clean pre-confound "
        "slice (Feb 16-28 only) shows a smaller but defensible +0.8% lift. "
        "Shipping was reasonable, but any forward-looking number should "
        "use +0.8%, not the confounded +2.1% headline.",
        (
            chk("q8_exp_id", "cites the Checkout Simplify experiment id exp_2214", r"exp_2214"),
            chk("q8_full_window_lift", "cites the full-window confounded reading +2.1%", r"2\.1\s*%"),
            chk(
                "q8_ship_date",
                "cites the 2026-04-06 100% ship date",
                r"2026-04-06",
                r"april\s+6,?\s*2026",
            ),
            chk("q8_nav_refresh", "names 'Nav Refresh' as the concurrent, confounding launch", r"nav\s+refresh"),
            chk(
                "q8_nav_refresh_date",
                "cites the 2026-03-01 Nav Refresh launch date landing mid-experiment",
                r"2026-03-01",
                r"march\s+1,?\s*2026",
            ),
            chk("q8_nav_refresh_effect", "cites Nav Refresh's own independently-measured lift ~+1.3%", r"1\.3\s*%"),
            chk("q8_holdback_id", "cites the Nav Refresh holdback experiment id exp_2215", r"exp_2215"),
            chk(
                "q8_clean_slice",
                "cites the pre-confound clean-slice lift +0.8% as the defensible forward-planning number",
                r"0\.8\s*%",
            ),
        ),
        (
            chk(
                "q8_trap_quotes_confounded",
                "quotes +2.1% as 'the checkout redesign's impact' for forward planning without the confound caveat",
                r"2\.1\s*%.{0,60}(impact|lift)\s+of\s+the\s+checkout",
            ),
        ),
        (
            jd(
                "q8_uses_08_not_21_forward",
                "The answer clearly states that any forward-looking/planning use of this experiment's "
                "impact should use the +0.8% pre-confound figure rather than the +2.1% full-window "
                "headline, while still endorsing that shipping the change was reasonable.",
            ),
        ),
        True,
        4,
        "dim_experiment (Checkout Simplify + Nav Refresh Holdback) + fact_experiment_exposures/readouts "
        "+ dim_marketing_calendar (Nav Refresh launch) + Confluence PRD cross-reference",
    ),
    mk_question(
        "Q9",
        "US-2",
        "Cost per order in fulfillment has been dropping — what's driving that, and is it sustainable?",
        "Cost per order fell $7.85 (Q1FY26) -> $7.30 (Q2FY27 QTD), "
        "steepest single-quarter drop (-$1.05) landing Q4FY26->Q1FY27, "
        "coinciding with the DC sortation automation rollout at FON2/JOL1 "
        "(phased 2026-01-12 to 2026-02-15) — the SAME rollout that confounds "
        "the Wider Promise Window experiment in Q3. Caveat: Q4FY26 was the "
        "ONLY quarter with a QoQ INCREASE (+$0.90, ordinary peak/holiday "
        "cost pressure), so part of the following drop is normal "
        "post-holiday reversion, not automation alone. Net of that seasonal "
        "noise, the full 6-quarter decline is a genuine, durable efficiency "
        "gain — distinct from the on-time-rate story (Q3): cost improved "
        "for real while ship-to-home's promise-hit-rate did not.",
        (
            chk("q9_cost_start", "cites cost per order Q1FY26 $7.85", r"\$?\s*7\.85"),
            chk("q9_cost_end", "cites cost per order Q2FY27 QTD $7.30", r"\$?\s*7\.30"),
            chk("q9_steepest_drop", "cites the steepest single-quarter drop of -$1.05", r"\$?\s*1\.05"),
            chk(
                "q9_automation_rollout",
                "names the DC sortation automation rollout at FON2/JOL1",
                r"fon2",
                r"jol1",
                r"sortation\s+automation",
            ),
            chk(
                "q9_automation_dates",
                "cites the 2026-01-12 to 2026-02-15 rollout window",
                r"2026-01-12",
                r"2026-02-15",
            ),
            chk(
                "q9_q4_increase",
                "notes Q4FY26 was the ONLY quarter with a QoQ INCREASE (+$0.90, peak/holiday cost)",
                r"\$?\s*0\.90",
                r"only\s+quarter.{0,40}increase",
            ),
        ),
        (
            chk(
                "q9_trap_credit_otp",
                "credits the same DC automation for the on-time-rate improvement from Q3 (conflating cost and speed)",
                r"(on-time|delivery\s+speed|otp).{0,80}(automation|dc\s+automation|sortation).{0,40}(improv\w*|caused|drove)",
                r"automation.{0,80}(improved|drove|caused).{0,40}(on-time|delivery\s+speed|otp)",
            ),
            chk(
                "q9_trap_full_drop_to_automation",
                "credits the ENTIRE steepest QoQ drop to automation without noting the peak-quarter reversion",
                r"(entirely|fully|solely)\s+(due to|attributable to|driven by)\s+.{0,40}automation",
            ),
        ),
        (
            jd(
                "q9_separates_cost_from_speed",
                "The answer explicitly treats the cost improvement (real, durable) and the on-time-rate "
                "improvement (mostly mix-shift, per Q3) as two DISTINCT conclusions about the same "
                "underlying DC automation event, rather than conflating 'the DCs got better' into one "
                "undifferentiated claim.",
            ),
        ),
        True,
        3,
        "fulfillment_speed_daily (avg_cost_per_order_usd) + dim_fulfillment_node + DC automation "
        "timeline entry (same event as Q3)",
    ),
    mk_question(
        "Q10",
        "US-2",
        "Give me a complete list of everything on the roadmap for Speed and Membership this half.",
        "A complete answer requires BOTH Aitable (legacy, items opened "
        "before 2026-01-15) and Jira (items opened on/after that date) — "
        "the two systems are mid-migration (consolidation kicked off "
        "2026-01-15, not complete as of 'today' 2026-07-20). Confluence "
        "holds PRDs for both eras and can cross-check completeness. A "
        "query against only one ticketing system silently returns a "
        "partial roadmap.",
        (
            chk("q10_both_systems", "names BOTH Aitable and Jira as required sources", r"aitable", r"jira"),
            chk(
                "q10_cutover_date",
                "cites the 2026-01-15 migration cutover date",
                r"2026-01-15",
                r"january\s+15,?\s*2026",
            ),
            chk(
                "q10_mid_migration",
                "states the migration/consolidation is still in progress, not complete",
                r"mid[- ]migration",
                r"still\s+in\s+progress",
                r"not\s+(yet\s+)?complete",
                r"consolidation",
            ),
            chk("q10_confluence_crosscheck", "mentions Confluence PRDs as a completeness cross-check spanning both eras", r"confluence"),
        ),
        (
            chk(
                "q10_trap_jira_only",
                "presents a Jira-only pull as 'the roadmap', silently missing pre-2026-01-15 items",
                r"jira.{0,60}complete\s+(roadmap|list)",
                r"(the\s+roadmap\s+is|here.s\s+the\s+roadmap).{0,80}\bjira\b(?!.{0,80}aitable)",
            ),
        ),
        (),
        True,
        3,
        "Aitable (legacy roadmap cards) + Jira (current roadmap tickets) + Confluence (PRDs both eras)",
    ),
    mk_question(
        "Q11",
        "US-3",
        "Are any of our in-flight tests contributing to or masking this?",
        "Yes — two, masking each other. Both started 2026-06-08 and both "
        "are still running: 'Search Relevance Re-ranking' (exp_2601, "
        "+1.6% conversion lift) and 'Item Page Media Carousel Autoplay' "
        "(exp_2618, -1.5% on its exposed arm — backfired). Equal-weighted "
        "blended net effect is ~+0.05% — essentially a wash. A PM checking "
        "only net effect would see ~0% and wrongly conclude nothing "
        "relevant is running. Neither is the PRIMARY explanation for the "
        "weekly conversion drop (mostly device mix-shift, Q1); the "
        "autoplay experiment's negative arm IS the most plausible source "
        "of Q1's smaller real-degradation component.",
        (
            chk("q11_two_experiments", "identifies TWO in-flight experiments, not zero or one", r"\btwo\b"),
            chk("q11_exp1_id", "cites Search Relevance Re-ranking experiment id exp_2601", r"exp_2601"),
            chk("q11_exp1_lift", "cites Search Relevance Re-ranking's +1.6% lift", r"1\.6\s*%"),
            chk("q11_exp2_id", "cites Item Page Media Carousel Autoplay experiment id exp_2618", r"exp_2618"),
            chk("q11_exp2_effect", "cites the autoplay experiment's -1.5% effect", r"1\.5\s*%"),
            chk(
                "q11_start_date",
                "cites the shared 2026-06-08 start date for both",
                r"2026-06-08",
                r"june\s+8,?\s*2026",
            ),
            chk("q11_net_effect", "cites the near-zero blended net effect (~+0.05%)", r"0\.05\s*%"),
        ),
        (
            chk(
                "q11_trap_net_only",
                "reports only the net experiment effect ('~0%, nothing material') without surfacing the "
                "two individually large offsetting effects",
                r"no\s+material\s+(experiment\s+)?impact",
                r"nothing\s+(relevant|material)\s+is\s+(running|happening)",
                r"net\s+effect\s+is\s+(approximately\s+)?(zero|0%|~0)(?!.{0,150}(exp_2601|exp_2618|1\.6\s*%|1\.5\s*%))",
            ),
        ),
        (
            jd(
                "q11_surfaces_masked_trend",
                "The answer's core point is that a near-zero NET experiment effect is exactly the shape "
                "that HIDES two large, real, offsetting effects — it makes the masking dynamic itself "
                "explicit as the answer to the question asked, not just a list of the two experiments.",
            ),
        ),
        True,
        3,
        "dim_experiment (exp_2601 + exp_2618) + fact_experiment_exposures + fact_experiment_readouts",
    ),
    mk_question(
        "Q12",
        "US-3",
        "Did the authentication-badge test on Collectibles listings actually move the needle?",
        "Yes, cleanly. +6.8% conversion lift on Collectibles listings "
        "showing the prominent 'Acme Verified' badge, tested 2025-10-01 to "
        "2025-11-15, no concurrent launch/marketing event overlapping that "
        "window in Collectibles, shipped to 100% 2025-11-20. Deliberately "
        "uncomplicated, unconfounded result — the same authentication "
        "program whose new-seller-side friction shows up in Q21 (this is "
        "the buyer-side conversion effect; the two are not in tension).",
        (
            chk("q12_lift", "cites the +6.8% conversion lift", r"6\.8\s*%"),
            chk("q12_dates", "cites the test window 2025-10-01 to 2025-11-15", r"2025-10-01", r"2025-11-15"),
            chk("q12_ship_date", "cites the 100% ship date 2025-11-20", r"2025-11-20"),
            chk(
                "q12_clean",
                "states there was no concurrent launch/confound in the window",
                r"no\s+concurrent\s+(launch|campaign|event)",
                r"unconfounded",
                r"\bclean(ly)?\b",
            ),
        ),
        (
            chk(
                "q12_trap_invented_confound",
                "manufactures a caveat/confound that isn't in the data (hedges a result that is actually clean)",
                r"however,?\s+(this\s+)?(result|reading|lift)\s+(is|was)\s+(confounded|complicated|not\s+clean)",
                r"(but|however).{0,60}(concurrent|overlapping)\s+(launch|campaign|event)",
            ),
        ),
        (
            jd(
                "q12_no_manufactured_hedge",
                "The answer reports the clean +6.8% lift as clean, without manufacturing a confound, "
                "caveat, or hedge the source material does not actually support — even though several "
                "other nearby experiments in this corpus ARE confounded.",
            ),
        ),
        True,
        3,
        "dim_experiment (Verified Badge Prominence) + fact_experiment_readouts + "
        "fact_marketplace_listings (+ event-timeline confound check)",
    ),
    mk_question(
        "Q13",
        "US-3",
        "The Membership team just ran a benefit-onboarding-carousel test — should we roll it out?",
        "Ship it, but be precise. Test (2026-05-01 to 2026-06-15, still "
        "inside its full readout horizon as of 'today' 2026-07-20) shows a "
        "genuine +9pp lift in 30-day benefit awareness — consistent with "
        "Q19's finding that awareness is the highest-leverage CLTV lever. "
        "But annual renewal rate can't be validly read for ~12 months per "
        "cohort, so no renewal-rate readout exists yet. Recommendation: "
        "ship (low-risk, aligned with an already-validated mechanism), and "
        "explicitly flag that a renewal-rate claim isn't available until "
        "roughly Q2FY28.",
        (
            chk("q13_test_dates", "cites the test window 2026-05-01 to 2026-06-15", r"2026-05-01", r"2026-06-15"),
            chk("q13_awareness_lift", "cites the +9pp lift in 30-day benefit awareness", r"9\s*pp"),
            chk(
                "q13_no_renewal_yet",
                "states no renewal-rate readout exists yet / can't be validly read yet",
                r"(no|not\s+yet\s+available|cannot\s+be\s+(validly\s+)?read)\s+renewal",
                r"renewal.{0,40}(not\s+yet|no\s+readout|too\s+early)",
            ),
            chk("q13_twelve_months", "cites the ~12-month renewal-cycle maturation window", r"12\s*months?", r"twelve\s+months?"),
            chk("q13_ships", "recommends shipping / rolling out", r"\bship\b", r"roll\s+it\s+out", r"recommend\w*.{0,20}ship"),
        ),
        (
            chk(
                "q13_trap_refuses_action",
                "refuses to recommend action because 'the data isn't all in yet' (overly conservative)",
                r"(too\s+early|not\s+enough\s+data|wait(\s+for)?\s+(more\s+data|the\s+renewal\s+read)).{0,60}(before|to)\s+(decid\w*|recommend|roll)",
            ),
            chk(
                "q13_trap_fabricated_renewal",
                "fabricates or projects a renewal-rate number that doesn't exist yet",
                r"renewal\s+rate\s+(of|is|will\s+be)\s+\d",
            ),
        ),
        (
            jd(
                "q13_holds_both_truths",
                "The answer holds both truths at once: it recommends shipping now on the strength of "
                "the validated awareness->adoption->renewal mechanism AND explicitly states the correct "
                "future point (~Q2FY28) at which a real renewal-rate claim becomes available, rather "
                "than picking only one of act-now or wait-for-data.",
            ),
        ),
        True,
        3,
        "dim_experiment (Benefit Onboarding Carousel) + fact_experiment_readouts + "
        "benefit-adoption/renewal correlation from Q19",
    ),
    mk_question(
        "Q14",
        "US-4",
        "Are there patterns across our verticals that no single PM would see because we're all just looking at our own numbers?",
        "Yes. A listing-accuracy-gap VOC theme (photos/descriptions not "
        "matching true scale/condition/spec) sits at a non-trivial, "
        "roughly steady share in ALL FOUR of Style (14%), Resold (12%), "
        "Collectibles (9%), and B2B (22%). Cross-checking each vertical's "
        "current, complete backlog (5 items each, 20 total) shows NONE of "
        "them owns it — it sits adjacent to several items without any "
        "actually addressing photo/description accuracy. No one owns it "
        "because each PM reads only their own vertical's VOC + backlog. "
        "Recommended owner: camille.duarte (Sr PM Marketplace Seller "
        "Experience, listings-side), sponsored by victor.okonkwo (spans "
        "all three Marketplace sub-verticals) for Marketplace, "
        "coordinating with malik.hendon for the B2B slice.",
        (
            chk("q14_theme_name", "names the 'listing-accuracy-gap' VOC theme", r"listing[- ]accuracy"),
            chk("q14_style_share", "cites Style's share 14%", r"14\s*%"),
            chk("q14_resold_share", "cites Resold's share 12%", r"12\s*%"),
            chk("q14_collectibles_share", "cites Collectibles' share 9%", r"9\s*%"),
            chk("q14_b2b_share", "cites B2B's share 22%", r"22\s*%"),
            chk(
                "q14_all_four",
                "explicitly states the pattern spans ALL FOUR verticals/categories",
                r"all\s+four",
                r"style.{0,80}resold.{0,80}collectibles.{0,80}b2b",
                r"across\s+(all\s+)?(four|4)\s+(verticals|categories)",
            ),
            chk(
                "q14_no_owner",
                "states that NO current backlog item actually owns/addresses this",
                r"no(ne)?\s+(one\s+)?(of\s+them\s+)?owns\s+(it|this)",
                r"not\s+(currently\s+)?owned",
            ),
            chk("q14_owner_rec", "recommends camille.duarte as the owner", r"camille[.\s]?duarte"),
            chk("q14_sponsor_rec", "recommends victor.okonkwo as the sponsor spanning Marketplace", r"victor[.\s]?okonkwo"),
        ),
        (
            chk(
                "q14_trap_single_vertical",
                "scopes the finding to only one vertical instead of the cross-vertical pattern",
                r"only\s+(a\s+)?(minor|small)\s+(issue|concern)\s+(in|for)\s+\w+",
                r"not\s+worth\s+flagging",
            ),
            chk(
                "q14_trap_adjacent_credit",
                "wrongly credits an adjacent backlog item (e.g. Collectibles' badge-visibility work) with already covering this",
                r"badge[- ]visibility.{0,60}(already\s+)?(addresses|covers|handles)",
                r"(already\s+)?(addresses|covers|handles).{0,60}badge[- ]visibility",
            ),
        ),
        (
            jd(
                "q14_surfaces_org_reasoning",
                "The answer explains WHY no one owns this today (each PM reads only their own vertical's "
                "VOC + backlog) and recommends an owner using the SURFACE-based org structure (a role "
                "spanning verticals) rather than defaulting to one of the existing vertical PMs.",
            ),
        ),
        True,
        4,
        "fact_voc_responses (theme_tag=listing-accuracy-gap, 4 verticals) + Jira/Aitable backlog per "
        "vertical (CROSS-VERTICAL BACKLOG SNAPSHOT, 20 items)",
    ),
    mk_question(
        "Q15",
        "US-5",
        "How did the item page do last quarter?",
        "Depends which metric. View-to-cart rate "
        "(add_to_cart_sessions/product_view_sessions) went 18.0% -> 19.9% "
        "(+1.9pp raw) across Q1FY27. Item-page-scoped conversion "
        "(orders/product_view_sessions) was 5.13% for the quarter — "
        "different, larger than standard site conversion (orders/sessions, "
        "3.18%) because the denominator excludes sessions that never "
        "reached a product page. Both metrics inherit the SAME "
        "sessions_definition_version 1->2 cutover (2026-03-02): of "
        "view-to-cart's +1.9pp move, ~+0.8pp is the same "
        "mechanical/definitional bump, ~+1.1pp is real (plausibly the Item "
        "Page Iteration Program, 6 iterations across the quarter). Silently "
        "averaging the whole quarter across the cutover overstates the "
        "real gain by ~40% relative.",
        (
            chk("q15_v2c_start", "cites view-to-cart rate start 18.0%", r"18(\.0)?\s*%"),
            chk("q15_v2c_end", "cites view-to-cart rate end 19.9%", r"19\.9\s*%"),
            chk("q15_v2c_move", "states the raw view-to-cart move as +1.9pp", r"1\.9\s*pp"),
            chk("q15_item_page_conv", "cites item-page-scoped conversion 5.13%", r"5\.13\s*%"),
            chk("q15_site_conv", "cites the DIFFERENT standard site conversion 3.18% for contrast", r"3\.18\s*%"),
            chk("q15_definition_cutover", "names the same sessions_definition_version cutover applying here", r"sessions?_definition_version"),
            chk("q15_split", "splits the +1.9pp move into mechanical (~+0.8pp) and real (~+1.1pp) components", r"0\.8\s*pp", r"1\.1\s*pp"),
            chk("q15_iteration_program", "names the Item Page Iteration Program as the plausible real driver", r"item\s+page\s+iteration\s+program"),
        ),
        (
            chk(
                "q15_trap_silent_average",
                "silently averages the whole quarter across the version cutover without splitting pre/post",
                r"1\.9\s*pp.{0,60}(entirely|all)\s+(real|from\s+the\s+iteration)",
                r"(fully|entirely)\s+attribut\w+.{0,40}iteration\s+program",
            ),
        ),
        (
            jd(
                "q15_states_metric_upfront",
                "The answer explicitly states, up front rather than buried at the end, which item-page "
                "metric(s) it is using and why, before giving the numbers — recognizing that both 'item "
                "page' and 'did well' need a stated definition.",
            ),
        ),
        True,
        2,
        "fact_traffic_daily (product_view_sessions, add_to_cart_sessions, sessions_definition_version) "
        "+ dim_marketing_calendar (Item Page Iteration Program v1-v6)",
    ),
    mk_question(
        "Q16",
        "US-6",
        "Given everything we know, what should I actually prioritize next quarter — and what should I stop doing?",
        "Three ranked recommendations, each with evidence + a metric: "
        "(1) Fund a cross-vertical 'listing accuracy' initiative, owned by "
        "camille.duarte (Q14) — moves Style/Resold/Collectibles return "
        "rate + the listing-accuracy-gap VOC share (14/12/9%, plus B2B's "
        "22%). (2) Kill or redesign 'Item Page Media Carousel Autoplay' "
        "(exp_2618, -1.5%, Q11) — the concrete 'what to stop' — recovers "
        "part of the real-degradation component in Q1's weekly conversion "
        "read. (3) Launch a targeted streaming-benefit awareness push "
        "(Q19: 93% renewal among aware members, only 34% aware) — moves "
        "Acme+ annual renewal rate. A fourth item is flagged as a DECISION "
        "TO MAKE, not a resolved recommendation: the new-seller "
        "authentication-friction trade-off (Q21) — a scoped pilot is the "
        "recommended next step to bring to planning, not a unilateral call.",
        (
            chk("q16_rec1_owner", "names camille.duarte as owner of the cross-vertical listing-accuracy initiative", r"camille[.\s]?duarte"),
            chk("q16_rec2_experiment", "names killing/redesigning the autoplay carousel experiment", r"exp_2618", r"autoplay"),
            chk("q16_rec3_lever", "names the streaming-benefit awareness push as a recommendation", r"streaming.{0,20}(bundle|benefit)"),
            chk("q16_rec3_numbers", "cites the 93% renewal / 34% awareness figures from Q19", r"93\s*%", r"34\s*%"),
            chk(
                "q16_three_ranked",
                "presents (at least) THREE ranked recommendations, not a single 'big swing'",
                r"\b(1\.|first|#1)\b.{0,400}\b(2\.|second|#2)\b.{0,400}\b(3\.|third|#3)\b",
            ),
            chk(
                "q16_auth_tradeoff_flagged",
                "flags the authentication-friction trade-off (Q21) as a DECISION needing to be made, not a resolved recommendation",
                r"authentication.{0,60}(trade-?off|decision)",
                r"(decision|trade-?off).{0,60}authentication",
            ),
        ),
        (
            chk(
                "q16_trap_one_big_swing",
                "gives one single 'big swing' recommendation instead of a ranked portfolio",
                r"the\s+(single\s+)?(biggest|most\s+important)\s+(priority|thing)\s+(is|should\s+be)",
            ),
            chk(
                "q16_trap_resolves_tradeoff",
                "silently resolves the authentication trade-off unilaterally instead of surfacing it as a decision",
                r"(remove|rip\s+out|eliminate)\s+(the\s+)?authentication\s+requirement(?!.{0,150}(pilot|decision|trade-?off))",
                r"(keep|leave)\s+(the\s+)?authentication\s+(as[- ]is|unchanged)(?!.{0,150}(pilot|decision|trade-?off))",
            ),
        ),
        (
            jd(
                "q16_framed_as_input_not_mandate",
                "The overall answer is framed as INPUT to a planning ritual/conversation rather than as "
                "a verdict or mandate, and explicitly separates 'recommendation' (items 1-3) from "
                "'trade-off needing a decision' (item 4) rather than blending them into one "
                "undifferentiated list.",
            ),
        ),
        True,
        5,
        "draws on Q14 (cross-vertical blind spot) + Q11 (offsetting experiments) + Q19 (CLTV lever) + "
        "Q21 (seller auth friction) + member_cltv — a synthesis question",
    ),
    mk_question(
        "Q17",
        "US-6",
        "Marketplace's Style category is decelerating — is this a Style problem?",
        "No. Style GMV grew +6.1% YoY in Q1FY27 (vs ~10% planned/trend) — "
        "looks like a Style-specific problem from the Style dashboard "
        "alone. But Resold GMV accelerated to +90.9% YoY over the "
        "identical window, and Resold's apparel/style-adjacent category "
        "share rose from 51% (year-ago) to 62% (Q1FY27) — a wallet-share "
        "shift toward resale, not a departure from Acme's marketplace. "
        "Total Marketplace GMV is healthy, pacing at 117% of its FY27 "
        "goal. The pattern only appears when Style and Resold are read "
        "together.",
        (
            chk("q17_style_growth", "cites Style GMV growth +6.1% YoY", r"6\.1\s*%"),
            chk("q17_planned_rate", "cites the ~10% planned/trend growth rate for contrast", r"10\s*%"),
            chk("q17_resold_growth", "cites Resold's acceleration to +90.9% YoY", r"90\.9\s*%"),
            chk("q17_category_shift", "cites Resold's apparel-adjacent share rising 51% -> 62%", r"51\s*%.{0,60}62\s*%", r"62\s*%"),
            chk("q17_total_pace", "cites total Marketplace pacing at 117% of its FY27 goal", r"117\s*%"),
            chk(
                "q17_answer_no",
                "concludes plainly this is NOT an isolated Style-specific demand problem",
                r"\bno\b.{0,60}(style[- ]specific|isolated|demand\s+problem)",
                r"not\s+a\s+style\s+problem",
            ),
        ),
        (
            chk(
                "q17_trap_isolated_scope",
                "scopes the investigation to Style-only tables/dashboards and concludes a real, isolated demand problem exists",
                r"style\s+(has|is\s+having)\s+a\s+(real\s+)?(demand|growth)\s+problem",
                r"style[- ]specific\s+(demand|growth)\s+(problem|issue)",
            ),
        ),
        (),
        True,
        3,
        "marketplace_gmv_summary + fact_marketplace_listings (Resold category attribute) + Marketplace "
        "FY27 goal (Company section)",
    ),
    mk_question(
        "Q18",
        "US-6",
        "Trust & Safety wants headcount for Collectibles fraud review, and the Style team wants headcount "
        "to investigate their slowdown. Who should get it?",
        "Collectibles. Its return rate spiked to 11.2% at the peak of the "
        "counterfeit problem (Q3FY26) before 'Acme Verified' (launched "
        "2025-09-08, partnered with GradeSure) brought it to 5.4% by "
        "Q2FY27 — T&S capacity protects a rapidly scaling GMV base "
        "(Collectibles now $100M+/quarter, +372.7% YoY off a small base). "
        "The Style slowdown (per Q17) is not a Style-execution problem — "
        "it's a wallet-share shift to Resold — so headcount aimed at "
        "'fixing Style demand' solves the wrong problem. A draft 'Style "
        "Conversion Recovery Plan' (Confluence, Q1FY27) proposed exactly "
        "that reallocation before the cross-category read superseded it; "
        "never actioned. Recommendation: fund the T&S ask; redirect "
        "Style's request toward jointly instrumenting Resold's category mix.",
        (
            chk("q18_return_rate_peak", "cites Collectibles' return-rate peak 11.2% (Q3FY26)", r"11\.2\s*%"),
            chk("q18_return_rate_now", "cites the post-program return rate 5.4% (Q2FY27)", r"5\.4\s*%"),
            chk("q18_program_name", "names the 'Acme Verified' program and its GradeSure partnership", r"acme\s+verified", r"gradesure"),
            chk("q18_program_launch", "cites the 2025-09-08 program launch date", r"2025-09-08", r"september\s+8,?\s*2025"),
            chk("q18_gmv_scale", "cites Collectibles' scale ($100M+/quarter, +372.7% YoY)", r"372\.7\s*%", r"\$?\s*100\s*M"),
            chk(
                "q18_style_not_execution",
                "explicitly says the Style slowdown is NOT a Style-execution problem (ties back to Q17)",
                r"not\s+an?\s+(execution\s+)?(style\s+)?problem",
                r"wallet[- ]share\s+shift",
            ),
            chk("q18_abandoned_plan", "mentions the abandoned/never-actioned 'Style Conversion Recovery Plan' draft", r"style\s+conversion\s+recovery\s+plan"),
            chk(
                "q18_answer_collectibles",
                "concludes plainly that Collectibles/Trust & Safety should get the headcount",
                r"collectibles\s+should\s+(get|receive)",
                r"fund\s+the\s+trust\s+(and|&)\s+safety",
            ),
        ),
        (
            chk(
                "q18_trap_split_evenly",
                "splits the headcount evenly between the two asks",
                r"split\s+(the\s+headcount\s+)?evenly",
                r"(half|50\s*%)\s+(to\s+)?(each|both)",
            ),
            chk(
                "q18_trap_default_to_bigger_gmv",
                "defaults to Style purely because its absolute GMV is larger",
                r"style.{0,60}(larger|bigger)\s+gmv.{0,60}(therefore|so|thus)",
            ),
        ),
        (
            jd(
                "q18_ts_protecting_not_firefighting",
                "The answer frames Trust & Safety headcount as protecting continued category growth (a "
                "forward-looking justification), not as firefighting an already-solved problem, and "
                "explicitly identifies that the Style ask's underlying premise (an isolated demand "
                "problem) is falsified by the Q17 cross-vertical read.",
            ),
        ),
        True,
        5,
        "marketplace_gmv_summary + fact_marketplace_listings (authenticity_verified, return rate) + "
        "fact_care_contacts + Style/Resold finding from Q17 + Jira/Aitable (2 headcount asks) + "
        "Confluence (abandoned plan)",
    ),
    mk_question(
        "Q19",
        "US-6",
        "What's actually the biggest lever we have to improve Acme+ member lifetime value?",
        "Benefit-adoption depth: members using 2+ benefits renew at 95% "
        "annually vs 71% for free-shipping-only. The single strongest "
        "INDIVIDUAL benefit is the streaming bundle — 93% annual renewal "
        "among members who use it alone, on par with the 2+-benefit cohort "
        "— but only 34% of members are even aware they have it. The "
        "highest-leverage, lowest-effort move is a streaming-bundle "
        "awareness push, not a new benefit or price change. (Side note: "
        "mart average CLTV is $500/member, not $625 — see Q20.)",
        (
            chk("q19_2plus_renewal", "cites 95% annual renewal for the 2+-benefit cohort", r"95\s*%"),
            chk("q19_1benefit_renewal", "cites 71% annual renewal for the free-shipping-only cohort", r"71\s*%"),
            chk("q19_streaming_renewal", "cites 93% annual renewal among streaming-bundle-only users", r"93\s*%"),
            chk("q19_awareness", "cites only 34% awareness of the streaming benefit", r"34\s*%"),
            chk("q19_answer_is_awareness", "concludes the lever is AWARENESS specifically, not a new benefit or price change", r"awareness"),
            chk("q19_cltv_correction", "flags that the naive mart average CLTV ($625) is not the corrected figure ($500)", r"\$?\s*625", r"\$?\s*500"),
        ),
        (
            chk(
                "q19_trap_generic_rec",
                "recommends a generic 'add more benefits' or 'broad renewal discount' instead of the specific awareness lever",
                r"add\s+more\s+benefits",
                r"broad(-|\s+)based\s+renewal\s+discount",
                r"across[- ]the[- ]board\s+discount",
            ),
            chk(
                "q19_trap_quotes_625_uncorrected",
                "quotes the $625 average CLTV figure without the correction to $500",
                r"\$?\s*625(?!.{0,150}500)",
            ),
        ),
        (),
        True,
        3,
        "member_cltv + fact_membership_events (benefit_redeemed) + renewal rate by "
        "benefit-adoption-depth cohort",
    ),
    mk_question(
        "Q20",
        "US-6",
        "Is Acme+ on track to hit its FY27 goals?",
        "Yes on the headline: 14.62M members at Q2FY27 QTD, pacing to "
        "~15.05M by FY27-end vs a 14.8M target (~102%, AHEAD); renewal "
        "rate 87.2% vs an 86.0% target (BEAT). But member_cltv shows 20% "
        "of the member panel (24,000 of 120,000) had ZERO orders in the "
        "trailing 12 months — still-active, still-paying, but dormant. "
        "These members don't hurt the headline count or renewal-rate "
        "goals, so goal-tracking alone is structurally blind to them — "
        "unrealized GMV and a real, silent churn-risk population.",
        (
            chk("q20_member_count", "cites the current member count 14.62M", r"14\.62\s*M"),
            chk("q20_pace", "cites the FY27-end pace ~15.05M", r"15\.05\s*M"),
            chk("q20_target", "cites the 14.8M member target", r"14\.8\s*M"),
            chk("q20_renewal_actual", "cites the 87.2% renewal rate", r"87\.2\s*%"),
            chk("q20_renewal_target", "cites the 86.0% renewal target", r"86(\.0)?\s*%"),
            chk("q20_dormant_pct", "cites the 20% dormant-member share", r"20\s*%"),
            chk("q20_dormant_count", "cites the 24,000 of 120,000 dormant-member figures", r"24,?000", r"120,?000"),
            chk(
                "q20_blind_spot",
                "explicitly states that goal-tracking is structurally blind to this dormant population",
                r"blind\s+to",
                r"doesn.t\s+(hurt|affect)\s+(the\s+)?(headline|goal)",
            ),
        ),
        (
            chk(
                "q20_trap_no_concerns",
                "answers 'yes, ahead on both metrics, no concerns' without surfacing the dormant-member population",
                r"no\s+concerns(?!.{0,200}(dormant|zero\s+orders|24,?000))",
                r"ahead\s+on\s+both(?!.{0,200}(dormant|zero\s+orders))",
            ),
        ),
        (),
        True,
        4,
        "dim_member (panel + true base) + member_cltv (dormant-member count) + Company FY27 goals + "
        "fact_membership_events (net-adds pacing)",
    ),
    mk_question(
        "Q21",
        "US-7",
        "Why are new marketplace sellers churning before they get to their 10th listing?",
        "Category-specific, not universal. Listing-count-based funnel "
        "(500 sellers, onboarded Q3-Q4FY26): Style/Resold new sellers "
        "reach listing 10 at 48%/46%; Collectibles at only 24% — half the "
        "rate — with the steepest relative drop-off happening earliest "
        "(listing 1->5). Root cause: the 'Acme Verified'/GradeSure "
        "authentication requirement is a genuine buyer-trust win "
        "(Collectibles return rate 11.2%->5.4%) that also adds real "
        "friction only new/small Collectibles sellers feel in full. "
        "Seller-side VOC (a SEPARATE stream from buyer Medallia) confirms: "
        "authentication-friction is the dominant theme (~38%) among "
        "Collectibles onboarding-pulse respondents vs ~5-6% for "
        "Style/Resold. Sellers whose debut listing is GradeSure-verified "
        "within 7 days clear listing 10 at 2x the rate (30% vs 15%) — "
        "verification SPEED, not verification itself, is the actionable "
        "lever. Collectibles new sellers also sell through more slowly "
        "(1.8 vs 3.6 orders/active listing/quarter for tenured sellers). "
        "Genuine two-sided trade-off — removing the requirement would "
        "undo a real buyer-trust win.",
        (
            chk("q21_collectibles_10", "cites Collectibles reaching listing 10 at 24%", r"24\s*%"),
            chk("q21_style_10", "cites Style reaching listing 10 at 48%", r"48\s*%"),
            chk("q21_resold_10", "cites Resold reaching listing 10 at 46%", r"46\s*%"),
            chk("q21_auth_program", "names the Acme Verified/GradeSure authentication requirement as root cause", r"acme\s+verified", r"gradesure"),
            chk("q21_seller_voc_theme", "cites authentication-friction as the dominant SELLER-side VOC theme at ~38% for Collectibles", r"38\s*%"),
            chk(
                "q21_seller_voc_separate",
                "notes seller-side VOC is a SEPARATE stream from buyer Medallia",
                r"separate\s+(stream|instrument)",
                r"seller[- ]side\s+voc.{0,40}(separate|different)\s+from",
            ),
            chk("q21_verification_speed", "cites the verification-speed 2x split (30% vs 15%)", r"30\s*%.{0,60}15\s*%", r"\b2x\b"),
            chk("q21_sellthrough", "cites the sell-through comparison 1.8 vs 3.6 orders/active listing/quarter", r"1\.8.{0,40}3\.6", r"3\.6"),
        ),
        (
            chk(
                "q21_trap_undifferentiated",
                "treats 'new sellers churn' as one undifferentiated population-level problem, missing the category difference",
                r"new\s+sellers?\s+(in\s+general|across\s+the\s+board|overall)\s+churn",
            ),
            chk(
                "q21_trap_free_removal",
                "recommends simply removing the authentication requirement without weighing the buyer-side benefit",
                r"(remove|eliminate|drop)\s+(the\s+)?authentication\s+requirement(?!.{0,150}(trade-?off|buyer|return\s+rate|11\.2))",
            ),
            chk(
                "q21_trap_buyer_voc_for_seller",
                "uses buyer-side Medallia data to explain the seller-side problem",
                r"medallia.{0,80}seller",
            ),
        ),
        (
            jd(
                "q21_kpi_definition_care",
                "If the answer discusses 'seller conversion,' it uses the seller-side sell-through/"
                "listing-to-sale concept rather than the buyer-side orders/sessions figure, treating "
                "the two 'conversion' concepts as non-interchangeable.",
            ),
        ),
        True,
        4,
        "dim_seller (application_date, onboarded_date, status) + fact_marketplace_listings "
        "(authenticity_verified) + fact_seller_voc_responses + marketplace_seller_performance",
    ),
    mk_question(
        "Q22",
        "Foundational",
        "What's our total Acme+ membership base, and is that number reliable?",
        "The true active Acme+ base is ~14.62M (Q2FY27 QTD), pacing toward "
        "~15.05M by FY27-end vs a 14.8M target. The dim_member TABLE "
        "itself holds only 120,000 rows — a representative panel (~0.82% "
        "sample), built for cohort/CLTV/benefit-adoption analysis. "
        "COUNT(*) on dim_member is NOT the total membership count and "
        "must never be reported as such; the true total comes from the "
        "membership system's own ledger, never by resumming a panel table.",
        (
            chk("q22_true_total", "cites the true active member base ~14.62M", r"14\.62\s*M"),
            chk("q22_panel_size", "cites the dim_member table's actual row count 120,000", r"120,?000"),
            chk(
                "q22_panel_not_census",
                "explicitly states dim_member is a representative PANEL/sample, not a census/full population",
                r"\b(panel|sample)\b",
                r"not\s+(the\s+)?(full|true|complete)\s+population",
            ),
            chk("q22_warns_against_count_star", "warns explicitly against COUNT(*) on dim_member as the total", r"count\s*\(\s*\*\s*\)"),
        ),
        (
            chk(
                "q22_trap_120k",
                "reports '120,000 Acme+ members' as the answer, confusing the panel with the true population",
                r"120,?000\s+(acme\+?\s+)?members(?!.{0,150}(panel|sample|0\.82|not\s+the))",
            ),
        ),
        (),
        True,
        2,
        "dim_member + Company section FY goals/actuals",
    ),
]


def _validate_rubric(rubric: list[Question]) -> None:
    ids = [qq.id for qq in rubric]
    expected = [f"Q{n}" for n in range(1, 23)]
    if ids != expected:
        raise AssertionError(f"RUBRIC ids must be Q1..Q22 in order; got {ids}")
    for qq in rubric:
        for c in (*qq.deterministic, *qq.trap):
            for p in c.patterns:
                re.compile(p)  # raises re.error on a bad pattern, at import time


_validate_rubric(RUBRIC)
RUBRIC_BY_ID: dict[str, Question] = {qq.id: qq for qq in RUBRIC}


# --------------------------------------------------------------------------
# Env / auth
# --------------------------------------------------------------------------


def load_env_file(path: Path) -> dict[str, str]:
    """Minimal .env parser (KEY=VALUE per line). No external dependency."""
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def resolve_api_key(env_file: str, cli_override: str | None) -> str | None:
    """NEXUS_API_KEY resolution order: --api-key, process env, --env-file. Never logged."""
    if cli_override:
        return cli_override
    if os.environ.get("NEXUS_API_KEY"):
        return os.environ["NEXUS_API_KEY"]
    env = load_env_file(Path(env_file))
    return env.get("NEXUS_API_KEY") or None


# --------------------------------------------------------------------------
# Nexus client
# --------------------------------------------------------------------------


class NexusError(RuntimeError):
    pass


class NexusClient:
    def __init__(self, base_url: str, api_key: str, context_slug: str, http_timeout: float = 120.0):
        self.api_url = base_url.rstrip("/")
        self.context_slug = context_slug
        self._client = httpx.Client(timeout=http_timeout)
        self._token = self._login(api_key)

    def _login(self, api_key: str) -> str:
        r = self._client.post(f"{self.api_url}/auth/login", json={"api_key": api_key})
        r.raise_for_status()
        return r.json()["token"]

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"}

    def create_query(self, ask: str, comparison_group: str | None = None) -> str:
        body: dict[str, Any] = {"ask": ask, "scope": [self.context_slug], "background": True}
        if comparison_group:
            # Turns sharing this string are exempt from the per-project
            # single-active-query cap (up to MAX_COMPARISON_TURNS parallel).
            body["comparison_group"] = comparison_group
        r = None
        for attempt in range(_CREATE_MAX_ATTEMPTS):
            r = self._client.post(f"{self.api_url}/query", headers=self._headers(), json=body)
            if r.status_code != 409:
                break
            if attempt < _CREATE_MAX_ATTEMPTS - 1:
                delay = _RETRY_BASE_S * (2**attempt) + random.uniform(0, _RETRY_BASE_S)
                print(
                    f"    [409] query create busy — backing off {delay:.1f}s "
                    f"(attempt {attempt + 1}/{_CREATE_MAX_ATTEMPTS})",
                    file=sys.stderr,
                )
                time.sleep(delay)
        r.raise_for_status()
        return r.json()["id"]

    def poll_query(self, query_id: str, timeout_s: int = _DEFAULT_QUERY_TIMEOUT_S) -> dict:
        deadline = time.monotonic() + timeout_s
        while True:
            r = self._client.get(f"{self.api_url}/queries/{query_id}", headers=self._headers())
            r.raise_for_status()
            data = r.json()
            status = data.get("status")
            if status in ("completed", "failed", "cancelled"):
                return data
            if time.monotonic() >= deadline:
                raise NexusError(f"query {query_id} timed out after {timeout_s}s (last status={status!r})")
            time.sleep(_POLL_INTERVAL_S)

    def close(self) -> None:
        self._client.close()


def _answer_text(output: Any) -> str:
    if isinstance(output, str):
        return output
    parts: list[str] = []
    for item in output or []:
        for block in (item or {}).get("content") or []:
            if block.get("type") == "output_text":
                parts.append(block.get("text") or "")
    return "".join(parts)


def _citation_label(c: Any) -> str:
    """Human-readable label for a citation — mirrors agent-nexus's own fallback chain."""
    if isinstance(c, str):
        return c
    if not isinstance(c, dict):
        return str(c)
    f = c.get("file") or {}
    return (
        c.get("source")
        or c.get("title")
        or c.get("name")
        or f.get("name")
        or f.get("path")
        or c.get("path")
        or c.get("id")
        or "?"
    )


def _citation_source_key(c: Any) -> str:
    """Identity key for DISTINCT SOURCE FILE counting — prefers the literal path/file name
    over a title (two chunks of the same file should collapse to one source)."""
    if isinstance(c, str):
        key = c
    elif not isinstance(c, dict):
        key = str(c)
    else:
        f = c.get("file") or {}
        key = (
            f.get("path")
            or f.get("name")
            or c.get("path")
            or c.get("source")
            or c.get("title")
            or c.get("name")
            or c.get("id")
            or "?"
        )
    # Normalize to the basename: one citation for a file may carry a full
    # path (file.path) while another citation for the SAME file carries only
    # a bare title/name (no file.path) — without this, inconsistent citation
    # shapes inflate the distinct-source count and mask the corpus-leak
    # signal this function exists to compute.
    return key.rsplit("/", 1)[-1]


@dataclass
class QueryResult:
    question_id: str
    answer_text: str
    citations: list[dict]
    model: str | None
    runtime_ms: int | None
    cost_usd: float | None
    usage: dict
    status: str | None
    error: str | None
    steps_rollup: dict
    raw: dict


def extract_result(question_id: str, data: dict) -> QueryResult:
    usage = data.get("usage") or {}
    return QueryResult(
        question_id=question_id,
        answer_text=_answer_text(data.get("output")).strip(),
        citations=data.get("citations") or [],
        model=data.get("model"),
        runtime_ms=data.get("runtime_ms"),
        cost_usd=usage.get("cost_usd"),
        usage=usage,
        status=data.get("status"),
        error=data.get("error"),
        steps_rollup={"steps": data.get("steps") or [], "rollup": data.get("rollup")},
        raw=data,
    )


# --------------------------------------------------------------------------
# Judge (claude-sonnet-5 via Vertex AI) — lazy import so --dry-run and
# --no-judge never require the `anthropic` package to be installed.
# --------------------------------------------------------------------------


class JudgeClient:
    def __init__(
        self,
        project_id: str = VERTEX_PROJECT_ID,
        region: str = VERTEX_REGION,
        model: str = JUDGE_MODEL,
    ):
        self._project_id = project_id
        self._region = region
        self._model = model
        self._client = None
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.call_count = 0
        self.error_count = 0

    def _get(self):
        if self._client is None:
            from anthropic import AnthropicVertex  # deferred: optional dependency

            self._client = AnthropicVertex(project_id=self._project_id, region=self._region)
        return self._client

    def judge(self, question: Question, answer_text: str, item: JudgeItem) -> tuple[bool | None, str]:
        system = (
            "You are a strict grading assistant for a retrieval-agent evaluation. "
            "You will be given a question, a reference describing what a correct answer "
            "must establish, one specific gradeable criterion, and a candidate answer. "
            "Decide only whether the candidate answer satisfies that ONE criterion. Do not "
            "reward the answer for unrelated correctness and do not penalize it for unrelated "
            "flaws — a separate deterministic scorer already checks the concrete facts. "
            "Respond with strict JSON only."
        )
        user = (
            f"QUESTION:\n{question.question}\n\n"
            f"REFERENCE (what a correct answer establishes):\n{question.correct_answer_summary}\n\n"
            f"CRITERION TO GRADE:\n{item.prompt}\n\n"
            f"CANDIDATE ANSWER:\n{answer_text if answer_text else '(empty — no answer text was returned)'}\n\n"
            "Does the candidate answer satisfy the criterion above?"
        )
        schema = {
            "type": "object",
            "properties": {
                "satisfied": {"type": "boolean"},
                "note": {"type": "string", "description": "one-sentence justification"},
            },
            "required": ["satisfied", "note"],
            "additionalProperties": False,
        }
        self.call_count += 1
        try:
            resp = self._get().messages.create(
                model=self._model,
                max_tokens=300,
                system=system,
                messages=[{"role": "user", "content": user}],
                thinking={"type": "disabled"},
                output_config={"effort": "low", "format": {"type": "json_schema", "schema": schema}},
            )
        except Exception as e:  # noqa: BLE001 — judge failures must degrade, not crash the run
            self.error_count += 1
            return None, f"judge call error: {e}"

        usage = getattr(resp, "usage", None)
        if usage is not None:
            self.total_input_tokens += getattr(usage, "input_tokens", 0) or 0
            self.total_output_tokens += getattr(usage, "output_tokens", 0) or 0

        text = next((b.text for b in resp.content if getattr(b, "type", None) == "text"), "{}")
        try:
            parsed = json.loads(text)
            return bool(parsed.get("satisfied")), str(parsed.get("note") or "")
        except (json.JSONDecodeError, AttributeError):
            self.error_count += 1
            return None, f"judge response unparsable: {text[:200]}"

    def cost_usd(self, intro_pricing: bool = False) -> float:
        in_rate = JUDGE_INPUT_RATE_PER_TOKEN_INTRO if intro_pricing else JUDGE_INPUT_RATE_PER_TOKEN
        out_rate = JUDGE_OUTPUT_RATE_PER_TOKEN_INTRO if intro_pricing else JUDGE_OUTPUT_RATE_PER_TOKEN
        return self.total_input_tokens * in_rate + self.total_output_tokens * out_rate


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------


@dataclass
class ScoreResult:
    question_id: str
    deterministic_passed: int
    deterministic_total: int
    deterministic_detail: list[dict]
    trap_triggered: bool
    trap_detail: list[dict]
    judge_notes: list[dict]
    citation_count: int
    distinct_source_count: int
    distinct_sources: list[str]
    min_expected_sources: int
    low_source_count: bool
    single_source_pass_risk: bool
    cost_usd: float | None
    runtime_ms: int | None
    model: str | None
    query_failed: bool


def score_answer(
    question: Question,
    result: QueryResult,
    judge: JudgeClient | None,
    use_judge: bool,
) -> ScoreResult:
    text = result.answer_text

    det_detail = [{"id": c.id, "description": c.description, "passed": c.evaluate(text)} for c in question.deterministic]
    det_passed = sum(1 for d in det_detail if d["passed"])

    trap_detail = [{"id": c.id, "description": c.description, "triggered": c.evaluate(text)} for c in question.trap]
    trap_triggered = any(d["triggered"] for d in trap_detail)

    judge_notes: list[dict] = []
    for item in question.judge:
        if use_judge and judge is not None and text:
            satisfied, note = judge.judge(question, text, item)
        else:
            satisfied, note = None, "judge skipped (--no-judge, no judge configured, or empty answer)"
        judge_notes.append({"id": item.id, "criterion": item.prompt, "satisfied": satisfied, "note": note})

    distinct_sources = sorted({_citation_source_key(c) for c in result.citations})
    low_source_count = question.expects_multi_source and len(distinct_sources) < question.min_expected_sources
    single_source_pass_risk = (
        low_source_count and len(question.deterministic) > 0 and det_passed == len(question.deterministic)
    )

    return ScoreResult(
        question_id=question.id,
        deterministic_passed=det_passed,
        deterministic_total=len(question.deterministic),
        deterministic_detail=det_detail,
        trap_triggered=trap_triggered,
        trap_detail=trap_detail,
        judge_notes=judge_notes,
        citation_count=len(result.citations),
        distinct_source_count=len(distinct_sources),
        distinct_sources=distinct_sources,
        min_expected_sources=question.min_expected_sources,
        low_source_count=low_source_count,
        single_source_pass_risk=single_source_pass_risk,
        cost_usd=result.cost_usd,
        runtime_ms=result.runtime_ms,
        model=result.model,
        query_failed=result.status in ("failed", "cancelled") or (result.status != "completed" and not text),
    )


def summarize_steps(steps_rollup: dict) -> dict:
    steps = steps_rollup.get("steps") or []
    tool_calls: list[str] = []
    for s in steps:
        for k in ("fns", "tool_calls", "strategy"):
            v = s.get(k)
            if isinstance(v, list):
                tool_calls.extend(str(x) for x in v)
            elif isinstance(v, str):
                tool_calls.append(v)
    return {"step_count": len(steps), "tool_calls": tool_calls, "rollup": steps_rollup.get("rollup")}


# --------------------------------------------------------------------------
# Persistence
# --------------------------------------------------------------------------


def append_jsonl(path: Path, obj: dict) -> None:
    with open(path, "a") as f:
        f.write(json.dumps(obj, default=str) + "\n")


def _utc_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def select_questions(question_ids: list[str] | None, limit: int | None) -> list[Question]:
    if question_ids:
        missing = [i for i in question_ids if i not in RUBRIC_BY_ID]
        if missing:
            raise SystemExit(f"Unknown --question id(s): {missing}. Valid: Q1..Q22")
        selected = [RUBRIC_BY_ID[i] for i in question_ids]
    else:
        selected = list(RUBRIC)
    if limit is not None:
        selected = selected[:limit]
    return selected


def print_dry_run(questions: list[Question]) -> None:
    print("=" * 100)
    print("ACME E-COMMERCE EVAL — DRY RUN (rubric derivation only; zero API calls)")
    print("=" * 100)
    total_det = total_trap = total_judge = 0
    story_counts: dict[str, int] = {}
    for question in questions:
        story_counts[question.user_story] = story_counts.get(question.user_story, 0) + 1
        print(f"\n{'-' * 100}")
        print(f"[{question.id}] {question.user_story}")
        print(f"Q: {question.question}")
        print(
            f"Corpus-leak sensitivity: expects_multi_source={question.expects_multi_source}, "
            f"min_expected_sources={question.min_expected_sources}"
        )
        print(f"  Systems/tables this join requires: {question.source_hint}")
        print(f"Deterministic assertions ({len(question.deterministic)}):")
        for c in question.deterministic:
            pats = "  OR  ".join(c.patterns)
            print(f"  [{c.id}] {c.description}")
            print(f"        pattern(s): {pats}")
        print(f"Trap markers ({len(question.trap)}):")
        for c in question.trap:
            pats = "  OR  ".join(c.patterns)
            print(f"  [{c.id}] {c.description}")
            print(f"        pattern(s): {pats}")
        if question.judge:
            print(f"Routed to judge ({len(question.judge)}) — cannot be checked mechanically:")
            for j in question.judge:
                print(f"  [{j.id}] {j.prompt}")
        else:
            print("Routed to judge: none — fully mechanical")
        total_det += len(question.deterministic)
        total_trap += len(question.trap)
        total_judge += len(question.judge)

    print(f"\n{'=' * 100}")
    print(
        f"TOTALS across {len(questions)} questions: {total_det} deterministic checks, "
        f"{total_trap} trap markers, {total_judge} judge-routed criteria."
    )
    print("Per-user-story question counts: " + ", ".join(f"{k}={v}" for k, v in story_counts.items()))
    print("Zero API calls made.")


def print_question_result(question: Question, result: QueryResult, score: ScoreResult, wall_s: float) -> None:
    print(f"\n[{question.id}] {question.user_story} — {question.question}")
    if score.query_failed:
        print(f"  !!! QUERY FAILED (status={result.status!r}): {result.error}")
    print(f"  deterministic: {score.deterministic_passed}/{score.deterministic_total} passed")
    for d in score.deterministic_detail:
        mark = "PASS" if d["passed"] else "FAIL"
        print(f"    [{mark}] {d['id']}: {d['description']}")
    trap_word = "TRIGGERED" if score.trap_triggered else "not triggered"
    print(f"  trap: {trap_word}")
    for d in score.trap_detail:
        if d["triggered"]:
            print(f"    [HIT ] {d['id']}: {d['description']}")
    if score.judge_notes:
        satisfied_n = sum(1 for j in score.judge_notes if j["satisfied"] is True)
        graded_n = sum(1 for j in score.judge_notes if j["satisfied"] is not None)
        print(f"  judge: {satisfied_n}/{graded_n} satisfied ({len(score.judge_notes) - graded_n} skipped/unparsable)")
        for j in score.judge_notes:
            verdict = "?" if j["satisfied"] is None else ("SAT" if j["satisfied"] else "UNSAT")
            print(f"    [{verdict}] {j['id']}: {j['note']}")
    print(
        f"  citations: {score.citation_count} (distinct sources: {score.distinct_source_count}, "
        f"expects >= {score.min_expected_sources})"
        + ("  <-- FEWER SOURCES THAN THIS JOIN NEEDS" if score.low_source_count else "")
    )
    if score.single_source_pass_risk:
        print("  !!! CORPUS-LEAK SIGNAL: all deterministic checks passed despite too few distinct sources")
    cost_s = f"${score.cost_usd:.4f}" if score.cost_usd is not None else "n/a"
    runtime_s = f"{score.runtime_ms}ms" if score.runtime_ms is not None else "n/a"
    print(f"  model: {score.model or 'n/a'} | server runtime: {runtime_s} | cost: {cost_s} | wall: {wall_s:.1f}s")


def print_summary(questions: list[Question], scores: list[ScoreResult], judge: JudgeClient | None) -> None:
    by_id = {s.question_id: s for s in scores}

    flagged = [
        s
        for s in scores
        if s.query_failed
        or s.trap_triggered
        or s.deterministic_passed < s.deterministic_total
        or s.single_source_pass_risk
        or any(j["satisfied"] is False for j in s.judge_notes)
    ]

    print(f"\n{'#' * 100}")
    print("FLAGGED QUESTIONS — read this before the aggregate numbers below")
    print(f"{'#' * 100}")
    if not flagged:
        print("(none — every question passed all deterministic checks, avoided its trap, and cited "
              "enough distinct sources)")
    for s in sorted(flagged, key=lambda x: x.question_id):
        q = RUBRIC_BY_ID[s.question_id]
        reasons = []
        if s.query_failed:
            reasons.append("QUERY FAILED")
        if s.deterministic_passed < s.deterministic_total:
            reasons.append(f"deterministic {s.deterministic_passed}/{s.deterministic_total}")
        if s.trap_triggered:
            reasons.append("TRAP TRIGGERED")
        if s.single_source_pass_risk:
            reasons.append(f"passed fully on {s.distinct_source_count} source(s), needs >={s.min_expected_sources}")
        unsat = [j["id"] for j in s.judge_notes if j["satisfied"] is False]
        if unsat:
            reasons.append(f"judge unsatisfied: {unsat}")
        print(f"  [{s.question_id}] {q.user_story}: " + "; ".join(reasons))

    print(f"\n{'=' * 100}")
    print("SUMMARY")
    print(f"{'=' * 100}")

    det_passed_total = sum(s.deterministic_passed for s in scores)
    det_total_total = sum(s.deterministic_total for s in scores)
    trap_hits = sum(1 for s in scores if s.trap_triggered)
    judge_all = [j for s in scores for j in s.judge_notes]
    judge_graded = [j for j in judge_all if j["satisfied"] is not None]
    judge_satisfied = [j for j in judge_graded if j["satisfied"] is True]
    low_source_n = sum(1 for s in scores if s.low_source_count)
    leak_risk_n = sum(1 for s in scores if s.single_source_pass_risk)
    failed_n = sum(1 for s in scores if s.query_failed)

    pct = (det_passed_total / det_total_total * 100) if det_total_total else 0.0
    print(
        f"Deterministic (mechanical) score: {det_passed_total}/{det_total_total} checks passed "
        f"({pct:.1f}%) across {len(scores)} questions — this is the number to trust for correctness."
    )
    print(f"Trap triggers: {trap_hits}/{len(scores)} questions fell for a planted trap.")
    if not judge_all:
        print("Judge-graded criteria: none routed (or --no-judge).")
    elif judge_graded:
        n_skipped = len(judge_all) - len(judge_graded)
        print(
            f"Judge-graded criteria (SEPARATE, NOT blended into the number above): "
            f"{len(judge_satisfied)}/{len(judge_graded)} satisfied "
            f"({n_skipped} skipped/unparsable of {len(judge_all)} total)."
        )
    else:
        print(
            f"Judge-graded criteria (SEPARATE, NOT blended into the number above): "
            f"none graded — all {len(judge_all)} were skipped (--no-judge / empty answer) or unparsable."
        )
    print(
        f"Corpus-leak signal: {low_source_n}/{len(scores)} questions cited fewer distinct sources than "
        f"their join requires; {leak_risk_n} of those PASSED FULLY anyway (the strong signal)."
    )
    if failed_n:
        print(f"Query failures: {failed_n}/{len(scores)}.")

    print("\nPer-user-story rollup:")
    story_order: list[str] = []
    for question in questions:
        if question.user_story not in story_order:
            story_order.append(question.user_story)
    for story in story_order:
        story_scores = [s for s in scores if RUBRIC_BY_ID[s.question_id].user_story == story]
        if not story_scores:
            continue
        d_p = sum(s.deterministic_passed for s in story_scores)
        d_t = sum(s.deterministic_total for s in story_scores)
        t_hits = sum(1 for s in story_scores if s.trap_triggered)
        j_all = [j for s in story_scores for j in s.judge_notes]
        j_graded = [j for j in j_all if j["satisfied"] is not None]
        j_sat = [j for j in j_graded if j["satisfied"] is True]
        pct_s = (d_p / d_t * 100) if d_t else 0.0
        if not j_all:
            j_str = "no judge items"
        elif j_graded:
            j_str = f"{len(j_sat)}/{len(j_graded)} judge"
        else:
            j_str = f"0 graded ({len(j_all)} skipped)"
        ids = ", ".join(s.question_id for s in story_scores)
        print(f"  {story:<12} ({ids}): deterministic {d_p}/{d_t} ({pct_s:.0f}%), traps {t_hits}/{len(story_scores)}, {j_str}")

    total_query_cost = sum(s.cost_usd for s in scores if s.cost_usd is not None)
    total_runtime_ms = sum(s.runtime_ms for s in scores if s.runtime_ms is not None)
    print(f"\nTotal nexus query cost (server-reported usage.cost_usd): ${total_query_cost:.4f}")
    print(f"Total nexus server runtime: {total_runtime_ms / 1000:.1f}s across {len(scores)} queries")
    if judge is not None and judge.call_count:
        print(
            f"Judge calls: {judge.call_count} ({judge.error_count} errored) — "
            f"{judge.total_input_tokens} input / {judge.total_output_tokens} output tokens — "
            f"${judge.cost_usd():.4f} at list price (${judge.cost_usd(intro_pricing=True):.4f} at "
            f"the 2026-08-31 intro rate)"
        )


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Acme eCommerce Nexus evaluation harness — checkable-assertion scoring, not a bare LLM judge."
    )
    p.add_argument("--api-base", default=DEFAULT_API_BASE, help=f"Nexus API base (default {DEFAULT_API_BASE})")
    p.add_argument("--context", default=DEFAULT_CONTEXT_SLUG, help=f"Nexus context slug (default {DEFAULT_CONTEXT_SLUG})")
    p.add_argument("--env-file", default=str(DEFAULT_ENV_PATH), help="Path to .env holding NEXUS_API_KEY")
    p.add_argument("--api-key", default=None, help="Override NEXUS_API_KEY directly (prefer --env-file; never printed)")
    p.add_argument("--dry-run", action="store_true", help="Print the full rubric derivation for all selected questions; zero API calls")
    p.add_argument("--limit", type=int, default=None, help="Only run the first N selected questions")
    p.add_argument("--question", action="append", default=None, metavar="ID", help="Run only this question id (repeatable), e.g. --question Q1 --question Q11")
    p.add_argument("--no-judge", action="store_true", help="Skip LLM-judge calls; judge-routed criteria are reported as skipped")
    p.add_argument("--concurrency", type=int, default=1, help=f"Parallel in-flight queries, max {MAX_COMPARISON_TURNS} (shares one comparison_group)")
    p.add_argument("--comparison-group", default=None, help="Override the comparison_group used to exempt parallel turns")
    p.add_argument("--out", default=None, help="Results JSONL path override (default eval/results/acme_ecomm_eval_<UTC timestamp>.jsonl)")
    p.add_argument("--query-timeout", type=int, default=_DEFAULT_QUERY_TIMEOUT_S, help=f"Per-query poll deadline in seconds (default {_DEFAULT_QUERY_TIMEOUT_S}, the server's own hard ceiling)")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    questions = select_questions(args.question, args.limit)

    if args.dry_run:
        print_dry_run(questions)
        return 0

    if args.concurrency > MAX_COMPARISON_TURNS:
        print(
            f"WARNING: prod exempts at most {MAX_COMPARISON_TURNS} parallel turns per comparison_group; "
            f"clamping --concurrency {args.concurrency} -> {MAX_COMPARISON_TURNS}",
            file=sys.stderr,
        )
        args.concurrency = MAX_COMPARISON_TURNS

    api_key = resolve_api_key(args.env_file, args.api_key)
    if not api_key:
        print(
            f"ERROR: no NEXUS_API_KEY found (checked --api-key, $NEXUS_API_KEY, and {args.env_file})",
            file=sys.stderr,
        )
        return 1

    out_path = Path(args.out) if args.out else DEFAULT_RESULTS_DIR / f"acme_ecomm_eval_{_utc_stamp()}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Context: {args.context} @ {args.api_base}")
    print(f"Results persisted incrementally to: {out_path}")

    client = NexusClient(args.api_base, api_key, args.context)
    judge = None if args.no_judge else JudgeClient()
    comparison_group = args.comparison_group or f"acme-ecomm-eval-{_utc_stamp()}"

    def process_one(question: Question) -> tuple[QueryResult, ScoreResult, float]:
        print(f"\n>>> {question.id} ({question.user_story}): {question.question}")
        t0 = time.monotonic()
        try:
            qid = client.create_query(
                question.question,
                comparison_group=comparison_group if args.concurrency > 1 else None,
            )
            data = client.poll_query(qid, timeout_s=args.query_timeout)
        except Exception as e:  # noqa: BLE001 — one question's transport failure must not kill the run
            data = {
                "status": "failed",
                "error": str(e),
                "output": "",
                "citations": [],
                "usage": {},
                "model": None,
                "runtime_ms": None,
                "steps": [],
                "rollup": None,
            }
        result = extract_result(question.id, data)
        score = score_answer(question, result, judge, use_judge=not args.no_judge)
        wall_s = time.monotonic() - t0
        print_question_result(question, result, score, wall_s)
        record = {
            "question_id": question.id,
            "recorded_at": _utc_iso(),
            "wall_s": round(wall_s, 2),
            "result": dataclasses.asdict(result),
            "score": dataclasses.asdict(score),
        }
        append_jsonl(out_path, record)
        return result, score, wall_s

    scores: list[ScoreResult] = []
    try:
        if args.concurrency <= 1:
            for question in questions:
                _, score, _ = process_one(question)
                scores.append(score)
        else:
            with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
                futures = {ex.submit(process_one, question): question for question in questions}
                for fut in as_completed(futures):
                    _, score, _ = fut.result()
                    scores.append(score)
    finally:
        client.close()

    scores.sort(key=lambda s: int(s.question_id[1:]))
    print_summary(questions, scores, judge)
    return 0


if __name__ == "__main__":
    sys.exit(main())
