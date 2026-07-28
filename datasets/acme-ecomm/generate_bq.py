"""Generate synthetic Acme (eCommerce) warehouse — 22 BQ tables to /tmp/acme_ecomm_data/*.parquet.

Deterministic via seed=42. Run with:
  uv run --with pandas --with numpy --with faker python datasets/acme-ecomm/generate_bq.py

Unlike datasets/acme/generate_bq.py (independent random draws with no stated
aggregate targets), every quarterly number in this warehouse is CONTRACTED by
CANON.md: sessions, conversion rate, GMV, deflection %, on-time %, member
counts, etc. are all stated exactly. So generation here runs TOP-DOWN: pick
the canon total for a (quarter, market/vertical) cut, distribute it across
days/rows with realistic noise, and rescale so the sum lands exactly on the
stated figure. See `allocate_int` / `allocate_float` below — those two
functions are the load-bearing primitive used everywhere a fact table must
roll up to a canon number.

Panel vs. population (CANON arithmetic convention 5): dim_member, dim_seller,
fact_orders, fact_care_contacts, fact_voc_responses, fact_marketplace_listings,
and fact_membership_events are REPRESENTATIVE SAMPLES, not the true
population — so those tables are generated to get RATES right (deflection %,
CLTV/member, return rate, CSAT) but never need their raw counts/sums to hit a
canon total. fact_traffic_daily, fact_experiment_exposures,
fact_experiment_readouts, and fact_promise_vs_actual are FULL POPULATION and
must hit stated totals exactly. Derived marts are authored top-down directly
from canon where the underlying fact is a sample (care_deflection_daily), or
rolled up from a full-population fact where that's legitimate
(traffic_conversion_summary, fulfillment_speed_daily), or built by genuinely
joining panel to sample at row grain (member_cltv, marketplace_seller_performance).
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

OUT = Path("/tmp/acme_ecomm_data")
SEED = 42
TODAY = date(2026, 7, 20)  # "today" snapshot per CANON.md
SESSION_CUTOVER = date(2026, 3, 2)  # sessions_definition_version 1 -> 2 (SIGNAL [session-definition])
R_JUMP = 1.11  # mechanical conversion-rate bump (v2 vs v1) from bot/dup session filtering -- modeling
              # constant solved so Q1FY27's version=1-only conversion lands ~2.96%, matching the
              # DISTRACTORS "flash estimate" figure (see report for the derivation).

fake = Faker()
Faker.seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

MARKETS = ["US", "CA", "MX"]
MARKETPLACE_SUBVERTS = ["STYLE", "RESOLD", "COLLECTIBLES"]


# --------------------------------------------------------------------------
# Fiscal calendar (FY runs Feb 1 -> Jan 31; quarters calendar-month-aligned)
# --------------------------------------------------------------------------
@dataclass
class Quarter:
    label: str
    start: date
    end: date       # full calendar end of the fiscal quarter
    data_end: date  # end of ACTUAL data (== end, except Q2FY27 truncated at TODAY)


QUARTERS = [
    Quarter("Q1FY26", date(2025, 2, 1), date(2025, 4, 30), date(2025, 4, 30)),
    Quarter("Q2FY26", date(2025, 5, 1), date(2025, 7, 31), date(2025, 7, 31)),
    Quarter("Q3FY26", date(2025, 8, 1), date(2025, 10, 31), date(2025, 10, 31)),
    Quarter("Q4FY26", date(2025, 11, 1), date(2026, 1, 31), date(2026, 1, 31)),
    Quarter("Q1FY27", date(2026, 2, 1), date(2026, 4, 30), date(2026, 4, 30)),
    Quarter("Q2FY27", date(2026, 5, 1), date(2026, 7, 31), TODAY),
]
DIM_DATE_START = date(2025, 1, 1)
DIM_DATE_END = date(2027, 1, 31)


def quarter_dates(q: Quarter) -> list[date]:
    n = (q.data_end - q.start).days + 1
    return [q.start + timedelta(days=i) for i in range(n)]


def fiscal_year(d: date) -> int:
    return d.year + 1 if d.month >= 2 else d.year


def fiscal_quarter(d: date) -> int:
    fmi = ((d.month - 2) % 12) + 1  # Feb=1 .. Jan=12
    return ((fmi - 1) // 3) + 1


def fiscal_quarter_label(d: date) -> str:
    return f"Q{fiscal_quarter(d)}FY{fiscal_year(d) % 100:02d}"


def week_ending_date(d: date) -> date:
    days_since_sunday = (d.weekday() + 1) % 7  # Mon=0..Sun=6 -> Mon=1..Sun=0
    return d + timedelta(days=6 - days_since_sunday)


# --------------------------------------------------------------------------
# Small generic helpers -- these are what make "top-down from the canon
# aggregate" possible: pick a realistic per-row weight curve, then apportion
# the exact stated total across rows by that curve.
# --------------------------------------------------------------------------
def rid(prefix: str, i: int, width: int = 6) -> str:
    return f"{prefix}_{i:0{width}d}"


def allocate_int(total: int, weights: np.ndarray) -> np.ndarray:
    """Largest-remainder apportionment: split `total` across len(weights)
    buckets proportional to `weights`, returned as an int array summing
    EXACTLY to `total`."""
    weights = np.asarray(weights, dtype=float)
    if weights.sum() <= 0:
        weights = np.ones_like(weights)
    shares = weights / weights.sum() * total
    floors = np.floor(shares).astype(np.int64)
    remainder = int(total - floors.sum())
    if remainder > 0:
        frac = shares - floors
        idx = np.argsort(-frac)[:remainder]
        floors[idx] += 1
    elif remainder < 0:
        frac = shares - floors
        idx = np.argsort(frac)[: (-remainder)]
        floors[idx] -= 1
    return floors


def allocate_float(total: float, weights: np.ndarray, decimals: int = 2) -> np.ndarray:
    """Proportional split of a float total across buckets, corrected so the
    rounded values sum EXACTLY to `total` (to `decimals` places)."""
    weights = np.asarray(weights, dtype=float)
    if weights.sum() <= 0:
        weights = np.ones_like(weights)
    raw = weights / weights.sum() * total
    rounded = np.round(raw, decimals)
    diff = round(total - rounded.sum(), decimals)
    if diff != 0:
        idx = int(np.argmax(rounded))
        rounded[idx] = round(rounded[idx] + diff, decimals)
    return rounded


def daily_weight_curve(dates: list[date], weekend_boost: float = 1.12, noise_sd: float = 0.07) -> np.ndarray:
    """Realistic daily weight curve: weekend lift + Black Friday/Cyber Monday
    spike + smooth lognormal-ish noise. Normalized only in the sense that
    callers pass this straight into allocate_*, which normalizes internally."""
    n = len(dates)
    w = np.ones(n)
    for i, d in enumerate(dates):
        if d.weekday() >= 5:
            w[i] *= weekend_boost
        # Black Friday / Cyber Monday spike (2025 window; the only one in-scope)
        if date(2025, 11, 28) <= d <= date(2025, 12, 1):
            w[i] *= 2.6
        elif date(2025, 12, 2) <= d <= date(2025, 12, 20):
            w[i] *= 1.35  # broader holiday shopping lift
        elif d.month == 12 and d.day >= 21:
            w[i] *= 1.15
    w *= np.random.lognormal(mean=0.0, sigma=noise_sd, size=n)
    return w


def draws_with_exact_mean(n: int, target_mean: float, lo: int, hi: int, std: float) -> np.ndarray:
    """Integer draws in [lo, hi] whose sample mean equals target_mean exactly
    (to integer-granularity precision), via a realistic-shaped normal draw
    followed by a small nudging correction. Used for CSAT-style bounded scores
    where the mart/reconciliation needs the exact stated average."""
    raw = np.random.normal(target_mean, std, size=n)
    vals = np.clip(np.round(raw), lo, hi).astype(int)
    for _ in range(2000):
        cur = vals.mean()
        diff = target_mean - cur
        if abs(diff) * n < 0.5:
            break
        if diff > 0:
            candidates = np.where(vals < hi)[0]
            if len(candidates) == 0:
                break
            idx = candidates[np.argmin(vals[candidates])]
            vals[idx] += 1
        else:
            candidates = np.where(vals > lo)[0]
            if len(candidates) == 0:
                break
            idx = candidates[np.argmax(vals[candidates])]
            vals[idx] -= 1
    return vals


def rescale_to_mean(vals: np.ndarray, target_mean: float) -> np.ndarray:
    cur = vals.mean()
    if cur <= 0:
        return np.full_like(vals, target_mean)
    return vals * (target_mean / cur)


# --------------------------------------------------------------------------
# CANON.md numbers -- quarterly series, Q1FY26 .. Q2FY27 (index 0..5)
# --------------------------------------------------------------------------
US_CONV = {
    "US": {
        "sessions_m": [402.0, 418.5, 437.0, 598.0, 379.5, 308.0],
        "conv_pct": [3.05, 3.00, 3.10, 3.92, 3.18, 3.22],
        "orders_m": [12.261, 12.555, 13.547, 23.442, 12.068, 9.918],  # stated authoritative (convention 1)
        "gmv_m": [651.1, 672.9, 734.2, 1369.0, 662.5, 551.4],
    },
    "CA": {
        "sessions_m": [44.62, 46.45, 48.51, 66.38, 42.12, 34.19],
        "conv_pct": [2.95, 2.90, 3.00, 3.82, 3.08, 3.12],
        "orders_m": None,  # not stated -- derive per convention 1: ROUND(sessions x conversion_rate)
        "gmv_m": [74.79, 77.26, 84.39, 158.45, 76.22, 63.46],
    },
    "MX": {
        "sessions_m": [28.54, 29.71, 31.03, 42.46, 26.94, 21.87],
        "conv_pct": [2.50, 2.45, 2.55, 3.37, 2.63, 2.67],
        "orders_m": None,
        "gmv_m": [28.80, 29.66, 32.59, 63.51, 29.57, 24.67],
    },
}
for _mkt, _d in US_CONV.items():
    if _d["orders_m"] is None:
        _d["orders_m"] = [round(s * c / 100.0, 6) for s, c in zip(_d["sessions_m"], _d["conv_pct"])]

MARKETPLACE_GMV_M = {
    # Q2FY27 QTD corrected mid-build (coordinator flag): raw canon draft had Marketplace
    # pacing at only 27.3% of Q1FY27 (222.4/815.0) at the 88%-elapsed mark, vs. the
    # conversion channel's 83.2% (639.5/768.3) -- a 3x inconsistency with no narrative
    # basis (Q5's whole story is a HEALTHY marketplace, wallet-share migrating
    # Style->Resold, not a collapse). Corrected Q2FY27 QTD = 815.0 * (639.5/768.3) =
    # 678.4, with Style/Resold/Collectibles rescaled by the same 3.05036x factor so the
    # sub-vertical MIX (and therefore SIGNAL [marketplace-cannibalization]) is untouched.
    "STYLE": [512.0, 530.0, 549.0, 715.0, 543.0, 444.1],
    "RESOLD": [88.0, 97.0, 109.0, 142.0, 168.0, 143.1],
    "COLLECTIBLES": [22.0, 25.0, 61.0, 118.0, 104.0, 91.2],
}
# Invented (not canon-constrained) AOV assumptions used only to back out a plausible
# order count from Marketplace GMV -- judgment call, documented in the ship report.
MARKETPLACE_AOV = {
    "STYLE": [68, 70, 72, 75, 78, 80],
    "RESOLD": [38, 39, 40, 42, 44, 45],
    "COLLECTIBLES": [85, 90, 110, 130, 140, 145],
}

CARE = {
    "contacts_k": [2150, 2205, 2280, 3650, 2050, 1180],
    "deflection_pct": [37.2, 39.5, 42.8, 45.0, 49.6, 52.1],
    "csat_deflected": [3.90, 3.85, 3.80, 3.70, 3.42, 3.55],
    "csat_agent": [4.30, 4.32, 4.35, 4.20, 4.30, 4.31],
    "handle_time_min": [8.4, 8.2, 8.0, 9.1, 7.6, 7.4],
}
SUB_PROGRAMS = ["automate", "avoid", "optimize", "platform", "member_care"]
SUB_PROGRAM_VOLUME_WEIGHT = {"automate": 0.30, "avoid": 0.25, "optimize": 0.20, "platform": 0.15, "member_care": 0.10}
SUB_PROGRAM_DEFLECTION_MULT = {"automate": 1.35, "avoid": 1.20, "optimize": 0.85, "platform": 0.70, "member_care": 0.35}

SPEED = {
    "sth_mix_pct": [77.5, 76.5, 75.4, 74.0, 68.9, 66.8],
    "pickup_mix_pct": [21.0, 22.0, 23.0, 24.0, 29.0, 31.0],
    "dfs_mix_pct": [1.5, 1.5, 1.6, 2.0, 2.1, 2.2],
    "sth_otp": [89.5, 89.9, 90.1, 87.0, 89.3, 89.9],
    "pickup_otp": [99.5, 99.4, 99.5, 99.1, 99.6, 99.6],
    "dfs_otp": [93.0, 93.2, 93.0, 90.5, 93.8, 94.2],
    "blended_otp": [91.65, 92.04, 92.31, 89.97, 92.38, 93.00],
    "cost_per_order": [7.85, 7.78, 7.70, 8.60, 7.55, 7.30],
}
COST_RATIO = {"ship_to_home": 1.35, "bopis": 0.35, "curbside": 0.42, "dfs": 1.10}

MEMBERSHIP = {
    "true_base_m": [12.60, 12.90, 13.35, 13.95, 14.35, 14.62],
    "net_adds_k": [310, 300, 450, 600, 400, 270],
    "renewal_pct": [86.2, 86.4, 86.7, 86.9, 87.0, 87.2],
}

# Total company order pool per quarter (US_CONV + Marketplace), in millions --
# used only as an internal weighting base for fact_promise_vs_actual / fact_orders
# temporal shape. Not itself a canon-stated figure.
TOTAL_ORDERS_M = []
for qi in range(6):
    us_conv_orders = sum(US_CONV[m]["orders_m"][qi] for m in MARKETS)
    mp_orders = sum(MARKETPLACE_GMV_M[sv][qi] / MARKETPLACE_AOV[sv][qi] for sv in MARKETPLACE_SUBVERTS)
    TOTAL_ORDERS_M.append(us_conv_orders + mp_orders)


# --------------------------------------------------------------------------
# Named cast -- pinned per CANON.md, must be reused verbatim
# --------------------------------------------------------------------------
NAMED_ASSOCIATES = [
    # assoc_id, full_name, role, team, manager_assoc_id, hire_date
    ("assoc_100001", "Deborah Osei", "CEO Acme eCommerce", "Executive", None, date(2023, 1, 1)),
    ("assoc_100010", "Felix Arroyo", "SVP Product & Growth", "Product", "assoc_100001", date(2023, 2, 1)),
    ("assoc_100020", "Hannah Brennan", "SVP Customer Care", "Care", "assoc_100001", date(2023, 2, 1)),
    ("assoc_100030", "Victor Okonkwo", "SVP Marketplace", "Marketplace", "assoc_100001", date(2023, 3, 1)),
    ("assoc_100040", "Renee Kowalski", "SVP Membership (Acme+)", "Membership", "assoc_100001", date(2023, 3, 1)),
    ("assoc_100050", "Ben Tanaka", "SVP Supply Chain & Fulfillment", "Fulfillment", "assoc_100001", date(2023, 4, 1)),
    ("assoc_100060", "Carlos Figueroa", "VP Data & Analytics", "Data", "assoc_100001", date(2023, 5, 1)),
    ("assoc_100070", "Nadia Esposito", "Head of Product Operations", "Product Ops", "assoc_100001", date(2023, 6, 1)),
    ("assoc_100110", "Maya Lindqvist", "Director PM US Conversion & Traffic", "Product", "assoc_100010", date(2023, 4, 1)),
    ("assoc_100111", "Owen Faust", "Sr PM Checkout & Conversion", "Product", "assoc_100110", date(2023, 8, 1)),
    ("assoc_100120", "Sanjay Bhatt", "Sr PM Marketplace Collectibles", "Marketplace", "assoc_100030", date(2023, 6, 1)),
    ("assoc_100121", "Ines Delgado", "Sr PM Marketplace Style", "Marketplace", "assoc_100030", date(2023, 7, 1)),
    ("assoc_100122", "Noah Kessler", "Sr PM Marketplace Resold", "Marketplace", "assoc_100030", date(2023, 9, 1)),
    ("assoc_100130", "Aisha Rahman", "Director PM Care (Automate/Avoid)", "Care", "assoc_100020", date(2023, 5, 1)),
    ("assoc_100131", "Julian Moss", "Sr PM Care (Optimize/Platform)", "Care", "assoc_100020", date(2023, 8, 1)),
    ("assoc_100140", "Tara Oduya", "Director PM Speed & Fulfillment", "Fulfillment", "assoc_100050", date(2023, 5, 1)),
    ("assoc_100141", "Leo Brandt", "Sr PM Delivery Promise", "Fulfillment", "assoc_100140", date(2023, 9, 1)),
    ("assoc_100150", "Simone Laurent", "Director PM Membership (Acme+)", "Membership", "assoc_100040", date(2023, 5, 1)),
    ("assoc_100151", "Derek Holloway", "Sr PM Membership Benefits & CLTV", "Membership", "assoc_100150", date(2023, 9, 1)),
    ("assoc_100123", "Camille Duarte", "Sr PM Marketplace Seller Experience (Listings & Optimization)", "Marketplace", "assoc_100030", date(2026, 4, 8)),
    ("assoc_100160", "Malik Hendon", "Sr PM Acme Business (B2B/Wholesale)", "B2B", "assoc_100010", date(2025, 6, 15)),
    ("assoc_100210", "Wei Hartono", "Analytics Engineer (owns core marts)", "Data", "assoc_100060", date(2023, 6, 1)),
    ("assoc_100211", "Amara Shah", "Data Analyst (Finance/MBR)", "Data", "assoc_100060", date(2023, 7, 1)),
    ("assoc_100212", "Connor Blake", "Data Engineer (pipeline/freshness)", "Data", "assoc_100060", date(2023, 8, 1)),
    ("assoc_100213", "Giulia Romano", "Analytics Engineer (Care & VOC/Medallia)", "Data", "assoc_100060", date(2023, 10, 1)),
    ("assoc_100310", "Dominic Paquet", "Care Ops Lead (bot/deflection)", "Care", "assoc_100020", date(2023, 6, 1)),
    ("assoc_100320", "Lucia Ferreira", "Trust & Safety Lead (Marketplace)", "Marketplace", "assoc_100030", date(2025, 9, 1)),
    ("assoc_100330", "Gabriel Stroud", "Fulfillment Ops Lead (DC network)", "Fulfillment", "assoc_100050", date(2023, 7, 1)),
]
NAMED_ASSOC_IDS = {row[0] for row in NAMED_ASSOCIATES}

# forbidden names/handles from the sibling SaaS corpus (DO-NOT-REUSE) -- filtered
# out of any Faker-generated filler name, belt-and-suspenders.
FORBIDDEN_NAMES = {
    "Sam Reyes", "Priya Anand", "Marcus Webb", "Jordan Hayes", "Elena Volkov", "Dan Lee",
    "Rachel Stein", "Jasmine Park", "Tomás Vega", "Anika Schmidt", "Lina Cho", "Rajiv Menon",
    "David Kim", "Nina Patel", "Marco Silva", "Olivia Tran", "Grace Liu", "Tom Becker",
    "Sarah Chen", "Yuki Sato", "Omar Haddad", "Jorge Martinez", "Theo Novak",
}

NAMED_MEMBERS = {
    # member_id -> dict of forced attributes (first name only per canon)
    "mem_1000042": dict(first_name="Dana", tenure_years=4, dormant=False, power_user=True,
                         benefits=["free_shipping", "early_access", "streaming_bundle"]),
    "mem_1000178": dict(first_name="Marisol", tenure_years=2.5, dormant=True, power_user=False,
                         benefits=[]),
    "mem_1000390": dict(first_name="Jamal", tenure_years=1.5, dormant=False, power_user=False,
                         benefits=["free_shipping"]),
    "mem_1000512": dict(first_name="Grethe", tenure_years=1.0, dormant=False, power_user=False,
                         benefits=["free_shipping"], churned_late_ship=True),
    "mem_1000640": dict(first_name="Oskar", tenure_years=None, dormant=False, power_user=False,
                         benefits=["free_shipping", "early_access"], fall_savings_signup=True),
}

# (id, name, category, gmv_tier, onboarded, status, fulfillment_method, home_country)
PINNED_SELLERS = [
    ("sel_500012", "Timeworn Treasures", "collectibles", "top", date(2024, 3, 1), "active", "seller_fulfilled", "US"),
    ("sel_500034", "Northfield Apparel Co.", "style", "mid", date(2024, 6, 1), "active", "ship_with_acme", "US"),
    ("sel_500061", "Loop Resale Collective", "resold", "large", date(2024, 4, 1), "active", "seller_fulfilled", "US"),
    ("sel_500089", "Bramblewood Vintage", "collectibles", "mid", date(2024, 7, 1), "active", "seller_fulfilled", "US"),
    ("sel_500103", "Kestrel & Vine", "style", "large", date(2024, 2, 1), "active", "ship_with_acme", "US"),
    ("sel_500147", "Harlow & Finch", "resold", "mid", date(2024, 5, 1), "active", "seller_fulfilled", "US"),
]
SHARED_CAST_SELLERS = [
    ("sel_500200", "Silverline Card Co.", "collectibles", "mid", date(2024, 8, 12), "active", "seller_fulfilled", "US"),
    ("sel_500201", "Heirloom & Co.", "collectibles", "small", date(2025, 2, 3), "active", "ship_with_acme", "US"),
    ("sel_500202", "Rustbelt Relics", "collectibles", "small", date(2025, 9, 20), "active", "seller_fulfilled", "US"),
    ("sel_500203", "Marrow Lane Vintage", "resold", "mid", date(2024, 11, 5), "active", "seller_fulfilled", "US"),
    ("sel_500204", "ReWear Collective", "resold", "large", date(2024, 5, 14), "active", "ship_with_acme", "US"),
    ("sel_500205", "Thriftline Goods", "resold", "small", date(2025, 6, 1), "active", "seller_fulfilled", "CA"),
    ("sel_500206", "Second Cycle Supply", "resold", "mid", date(2025, 3, 22), "active", "seller_fulfilled", "US"),
    ("sel_500207", "Cascade Denim Works", "style", "large", date(2024, 2, 18), "active", "ship_with_acme", "US"),
    ("sel_500208", "Meridian Threads", "style", "mid", date(2024, 9, 9), "active", "seller_fulfilled", "US"),
    ("sel_500209", "Palisade Footwear", "style", "mid", date(2025, 1, 11), "active", "ship_with_acme", "MX"),
    ("sel_500210", "Amberlyn Studio", "style", "small", date(2025, 7, 30), "active", "seller_fulfilled", "US"),
    ("sel_500211", "Coastal Trading Post", "other", "small", date(2024, 12, 1), "active", "seller_fulfilled", "US"),
    ("sel_500212", "Fernwood Outdoors", "other", "mid", date(2025, 4, 17), "suspended", "seller_fulfilled", "US"),
    ("sel_500213", "Basalt & Bloom", "style", "small", date(2025, 10, 5), "active", "ship_with_acme", "CA"),
]

NAMED_EXPERIMENTS = [
    # experiment_id, name, vertical_code, owner_assoc_id, hypothesis, start, end, status, primary_metric
    ("exp_2401", "Verified Badge Prominence", "MARKETPLACE", "assoc_100120",
     "Making the Acme Verified authenticity badge more prominent on Collectibles listings lifts conversion.",
     date(2025, 10, 1), date(2025, 11, 15), "shipped", "conversion_rate"),
    ("exp_1187", "Wider Promise Window", "SPEED", "assoc_100141",
     "Showing a wider (more conservative) delivery estimate window improves on-time-hit-rate.",
     date(2026, 1, 12), date(2026, 2, 20), "killed", "on_time_rate"),
    ("exp_2214", "Checkout Simplify", "US_CONV", "assoc_100111",
     "A simplified checkout flow (fewer steps, fewer fields) lifts conversion.",
     date(2026, 2, 16), date(2026, 3, 30), "shipped", "conversion_rate"),
    ("exp_2215", "Nav Refresh Holdback", "US_CONV", "assoc_100110",
     "Sitewide nav redesign holdback -- measure independent lift of Nav Refresh vs. no-launch control.",
     date(2026, 3, 1), date(2026, 3, 21), "shipped", "conversion_rate"),
    ("exp_2489", "Bot Handoff Threshold", "CARE", "assoc_100130",
     "Raising the bot-to-human handoff threshold increases deflection without hurting CSAT too much.",
     date(2026, 4, 1), date(2026, 5, 15), "shipped", "deflection_rate"),
    ("exp_2556", "Benefit Onboarding Carousel", "MEMBERSHIP", "assoc_100151",
     "An onboarding carousel highlighting Acme+ benefits raises 30-day benefit awareness.",
     date(2026, 5, 1), date(2026, 6, 15), "shipped", "benefit_awareness_pct"),
    ("exp_2601", "Search Relevance Re-ranking", "US_CONV", "assoc_100111",
     "A re-ranked search relevance model surfaces better-matched results and lifts conversion.",
     date(2026, 6, 8), None, "running", "conversion_rate"),
    ("exp_2618", "Item Page Media Carousel Autoplay", "US_CONV", "assoc_100110",
     "Autoplaying the item-page media carousel increases engagement and lifts conversion.",
     date(2026, 6, 8), None, "running", "conversion_rate"),
]

NAMED_MARKETING_EVENTS = [
    # event_id, name, event_type, vertical_code, market, start, end, owner_assoc_id, notes
    ("camp_000001", "Fall Savings Acme+ Join Promo", "promo", "MEMBERSHIP", None,
     date(2025, 9, 20), date(2025, 10, 15), "assoc_100150", "Discounted first-year join promo."),
    ("camp_000002", "Black Friday", "holiday", None, None,
     date(2025, 11, 28), date(2025, 11, 28), "assoc_100110", "Peak shopping day."),
    ("camp_000003", "Cyber Monday", "holiday", None, None,
     date(2025, 12, 1), date(2025, 12, 1), "assoc_100110", "Peak online shopping day."),
    ("camp_000004", "Acme Verified Authentication Program Launch", "launch", "MARKETPLACE", None,
     date(2025, 9, 8), None, "assoc_100320", "Partnered with GradeSure; authenticity badge program."),
    ("camp_000005", "Ask Acme v2 Bot Launch", "launch", "CARE", None,
     date(2025, 9, 15), None, "assoc_100310", "Revamped care deflection bot."),
    ("camp_000006", "Verified Badge Shipped 100%", "launch", "MARKETPLACE", None,
     date(2025, 11, 20), None, "assoc_100120", "exp_2401 shipped to all Collectibles listings."),
    ("camp_000007", "DC Sortation Automation Phase 1", "launch", "SPEED", None,
     date(2026, 1, 12), date(2026, 2, 15), "assoc_100330", "FON2 (Fontana) + JOL1 (Joliet), phased rollout."),
    ("camp_000008", "Pickup Perks Campaign", "promo", "SPEED", "US",
     date(2026, 1, 15), None, "assoc_100140", "BOPIS/curbside discount campaign."),
    ("camp_000009", "Paid-Search Budget Cut", "budget_change", "US_CONV", "US",
     date(2026, 2, 4), None, "assoc_100010", "-18% paid-search spend, marketing-efficiency initiative."),
    ("camp_000010", "Nav Refresh Sitewide Redesign", "launch", "US_CONV", None,
     date(2026, 3, 1), None, "assoc_100110", "Both experiment arms of exp_2214 get this; 5% holdback (exp_2215)."),
    ("camp_000011", "Checkout Simplify Shipped 100%", "launch", "US_CONV", "US",
     date(2026, 4, 6), None, "assoc_100111", "Shipped on the confounded full-window +2.1% figure."),
    ("camp_000012", "Bot Handoff Threshold Partial Ship", "launch", "CARE", None,
     date(2026, 5, 20), None, "assoc_100130", "Non-billing categories only."),
    ("camp_000013", "Acme+ Streaming Perk Partner Switch: Vidora -> Reelstream", "launch", "MEMBERSHIP", None,
     date(2026, 6, 1), None, "assoc_100040", "Streaming bundle benefit re-platformed."),
    ("camp_000014", "Item Page Iteration v1 (above-fold price/CTA reflow)", "launch", "US_CONV", "US",
     date(2026, 2, 5), date(2026, 2, 5), "assoc_100110", "First of 6 Item Page Iteration Program launches this quarter, pre-cutover (sessions_definition_version 1)."),
    ("camp_000015", "Item Page Iteration v2 (reviews section reorder)", "launch", "US_CONV", "US",
     date(2026, 2, 19), date(2026, 2, 19), "assoc_100110", "Pre-cutover (sessions_definition_version 1)."),
    ("camp_000016", "Item Page Iteration v3 (image gallery zoom/swipe)", "launch", "US_CONV", "US",
     date(2026, 3, 5), date(2026, 3, 5), "assoc_100110", "First iteration on sessions_definition_version 2 (post session-counting fix)."),
    ("camp_000017", "Item Page Iteration v4 (size/fit guidance module)", "launch", "US_CONV", "US",
     date(2026, 3, 19), date(2026, 3, 19), "assoc_100110", "Post-cutover (sessions_definition_version 2)."),
    ("camp_000018", "Item Page Iteration v5 (cross-sell module placement)", "launch", "US_CONV", "US",
     date(2026, 4, 2), date(2026, 4, 2), "assoc_100110", "Post-cutover (sessions_definition_version 2)."),
    ("camp_000019", "Item Page Iteration v6 (sticky add-to-cart bar, mobile)", "launch", "US_CONV", "US",
     date(2026, 4, 16), date(2026, 4, 16), "assoc_100110", "Last of 6 Item Page Iteration Program launches this quarter."),
    ("camp_000020", "Homepage Hero Banner Refresh", "launch", "US_CONV", "US",
     date(2026, 7, 13), date(2026, 7, 13), "assoc_100110", "Homepage-only; no item-page or search overlap -- coincidental-timing distractor for the Q2FY27 WoW conversion dip."),
]


# --------------------------------------------------------------------------
# Dimensions
# --------------------------------------------------------------------------
def gen_dim_date() -> pd.DataFrame:
    rows = []
    d = DIM_DATE_START
    while d <= DIM_DATE_END:
        rows.append({
            "date": d,
            "fiscal_year": fiscal_year(d),
            "fiscal_quarter": fiscal_quarter(d),
            "fiscal_quarter_label": fiscal_quarter_label(d),
            "fiscal_week": (d - date(fiscal_year(d) - 1, 2, 1)).days // 7 + 1,
            "week_ending_date": week_ending_date(d),
            "is_peak_holiday": fiscal_quarter(d) == 4,
            "day_of_week": d.strftime("%A"),
            "is_weekend": d.weekday() >= 5,
        })
        d += timedelta(days=1)
    return pd.DataFrame(rows)


def gen_dim_vertical() -> pd.DataFrame:
    top = [
        ("US_CONV", "US/CA/MX Conversion + Traffic", True, "Digital storefront traffic, conversion and GMV across US/CA/MX."),
        ("MARKETPLACE", "Marketplace", True, "3rd-party seller marketplace across Style, Resold and Collectibles."),
        ("CARE", "Customer Care", True, "Customer support contacts, deflection and CSAT."),
        ("SPEED", "Speed / Fulfillment", True, "Delivery promise, on-time performance and fulfillment cost."),
        ("MEMBERSHIP", "Membership (Acme+)", True, "Acme+ paid membership: signups, renewals, benefits, CLTV."),
        ("CLUB", "Club (warehouse-membership banner)", False, "Warehouse-club format banner, light coverage."),
        ("B2B", "Acme Business (B2B/wholesale)", False, "B2B/wholesale channel, light coverage."),
        ("PAYMENTS", "Payments", False, "Payment dispute/settlement and tender match rate."),
        ("OPD_DFS", "Online Pickup & Delivery -- Delivery From Store", False, "Reports off fulfillment_speed_daily filtered fulfillment_type='dfs'."),
        ("MARTECH", "Retail media / marketing technology", False, "Retail media and marketing technology, light coverage."),
        ("MPCX", "Marketplace Customer Experience", False, "Marketplace-side customer experience, light coverage."),
        ("SPLITS", "Order Splits (multi-shipment orders)", False, "Multi-shipment order splitting, light coverage."),
        ("POR", "Post-Order Returns", False, "Shares avg_refund_cycle_days with Care -- same series, different org lens."),
        ("CSI", "Customer Satisfaction Index (composite)", False, "Composite satisfaction index, light coverage."),
        ("REVIEWS", "Ratings & Reviews", False, "Ratings and reviews, light coverage."),
        ("FS_LATER", "Financial Services -- Pay Later (BNPL)", False, "Buy-now-pay-later financial services, light coverage."),
    ]
    subs = {
        "US_CONV": [("US", "United States"), ("CA", "Canada"), ("MX", "Mexico")],
        "MARKETPLACE": [("COLLECTIBLES", "Collectibles"), ("RESOLD", "Resold"), ("STYLE", "Style")],
        "CARE": [("AUTOMATE", "Automate"), ("AVOID", "Avoid"), ("OPTIMIZE", "Optimize"), ("PLATFORM", "Platform"), ("W+", "Member Care (W+)")],
        "SPEED": [("FD", "Fast Delivery"), ("PROMISE", "Promise"), ("EFFICIENCY", "Efficiency")],
        "PAYMENTS": [("DS", "Dispute & Settlement"), ("MATCH", "Tender/ID Match Rate")],
    }
    rows = []
    for code, name, deep, desc in top:
        rows.append({
            "vertical_code": code, "vertical_name": name, "sub_vertical_code": None,
            "sub_vertical_name": None, "is_deep_dive": deep, "customer_facing_desc": desc,
        })
        for sub_code, sub_name in subs.get(code, []):
            rows.append({
                "vertical_code": code, "vertical_name": name, "sub_vertical_code": sub_code,
                "sub_vertical_name": sub_name, "is_deep_dive": deep,
                "customer_facing_desc": f"{desc} ({sub_name}).",
            })
    return pd.DataFrame(rows)


def gen_dim_associate(n_total: int = 180) -> pd.DataFrame:
    rows = []
    for assoc_id, name, role, team, mgr, hire in NAMED_ASSOCIATES:
        rows.append({
            "assoc_id": assoc_id, "full_name": name, "role": role, "team": team,
            "manager_assoc_id": mgr, "hire_date": hire, "termination_date": None,
            "location": random.choice(["SF", "Bentonville", "Remote-NA"]), "is_active": True,
        })

    team_mgr = {
        "Product": ("assoc_100010", ["Product Manager", "Associate PM", "Product Analyst", "Product Designer"]),
        "Care": ("assoc_100020", ["Care Ops Analyst", "Care Program Manager", "QA Specialist", "Workforce Planner"]),
        "Marketplace": ("assoc_100030", ["Seller Ops Analyst", "Category Manager", "Trust & Safety Analyst", "Marketplace Analyst"]),
        "Membership": ("assoc_100040", ["Membership Analyst", "Benefits Program Manager", "Lifecycle Marketing Manager"]),
        "Fulfillment": ("assoc_100050", ["DC Ops Manager", "Network Planner", "Fulfillment Analyst", "Last-Mile Ops Lead"]),
        "Data": ("assoc_100060", ["Analytics Engineer", "Data Analyst", "Data Engineer", "BI Developer"]),
        "Product Ops": ("assoc_100070", ["Program Manager", "Roadmap Analyst", "Ops Coordinator"]),
    }
    locations = ["SF", "Bentonville", "Remote-NA", "Toronto", "Mexico City"]
    loc_w = [0.30, 0.30, 0.20, 0.12, 0.08]
    next_id = 100400
    n_filler = n_total - len(NAMED_ASSOCIATES)
    team_names = list(team_mgr.keys())
    for i in range(n_filler):
        team = team_names[i % len(team_names)]
        mgr, roles = team_mgr[team]
        name = fake.name()
        while name in FORBIDDEN_NAMES:
            name = fake.name()
        hire = date(2023, 6, 1) + timedelta(days=random.randint(0, (TODAY - date(2023, 6, 1)).days))
        terminated = random.random() < 0.06
        term_date = hire + timedelta(days=random.randint(180, 700)) if terminated else None
        if term_date and term_date > TODAY:
            term_date, terminated = None, False
        rows.append({
            "assoc_id": rid("assoc", next_id, width=6), "full_name": name,
            "role": random.choice(roles), "team": team, "manager_assoc_id": mgr,
            "hire_date": hire, "termination_date": term_date,
            "location": random.choices(locations, weights=loc_w)[0], "is_active": not terminated,
        })
        next_id += 1
    return pd.DataFrame(rows)


def gen_dim_fulfillment_node(n_total: int = 180) -> pd.DataFrame:
    rows = [
        {"node_id": "fc_JOL1", "node_type": "dc", "node_name": "Joliet DC (JOL1)", "market": "US",
         "opened_date": date(2019, 3, 1), "store_format": None, "is_active": True},
        {"node_id": "fc_FON2", "node_type": "dc", "node_name": "Fontana DC (FON2)", "market": "US",
         "opened_date": date(2020, 6, 1), "store_format": None, "is_active": True},
        {"node_id": "fc_ONT1", "node_type": "returns_center", "node_name": "Ontario Returns Processing Center", "market": "US",
         "opened_date": date(2018, 1, 1), "store_format": None, "is_active": True},
    ]
    dc_cities = ["Dallas", "Atlanta", "Phoenix", "Columbus", "Allentown", "Reno", "Charlotte",
                 "Sacramento", "Indianapolis", "Memphis", "Tampa", "Denver", "Toronto", "Montreal",
                 "Calgary", "Mexico City", "Monterrey", "Guadalajara"]
    for i, city in enumerate(dc_cities):
        market = "CA" if city in ("Toronto", "Montreal", "Calgary") else "MX" if city in ("Mexico City", "Monterrey", "Guadalajara") else "US"
        rows.append({
            "node_id": rid("fc", 1000 + i, width=4), "node_type": "dc", "node_name": f"{city} DC",
            "market": market, "opened_date": date(2019, 1, 1) + timedelta(days=random.randint(0, 2000)),
            "store_format": None, "is_active": True,
        })
    for i in range(12):
        rows.append({
            "node_id": rid("fc", 2000 + i, width=4), "node_type": "sortation_center",
            "node_name": f"{fake.city()} Sortation Center", "market": random.choice(MARKETS),
            "opened_date": date(2020, 1, 1) + timedelta(days=random.randint(0, 2200)),
            "store_format": None, "is_active": True,
        })
    for i in range(8):
        rows.append({
            "node_id": rid("fc", 3000 + i, width=4), "node_type": "returns_center",
            "node_name": f"{fake.city()} Returns Processing Center", "market": random.choice(MARKETS),
            "opened_date": date(2019, 1, 1) + timedelta(days=random.randint(0, 2200)),
            "store_format": None, "is_active": True,
        })
    n_stores = n_total - len(rows)
    formats = ["supercenter", "neighborhood", "club"]
    fmt_w = [0.45, 0.40, 0.15]
    for i in range(n_stores):
        market = random.choices(MARKETS, weights=[0.72, 0.16, 0.12])[0]
        opened = date(2015, 1, 1) + timedelta(days=random.randint(0, (TODAY - date(2015, 1, 1)).days))
        rows.append({
            "node_id": rid("str", 4000 + i, width=4), "node_type": "store",
            "node_name": f"{fake.city()} {random.choice(formats).title()}", "market": market,
            "opened_date": opened, "store_format": random.choices(formats, weights=fmt_w)[0],
            "is_active": random.random() > 0.03,
        })
    return pd.DataFrame(rows)


APPLICATION_DATE_CUTOVER = date(2025, 8, 1)  # Q3FY26 start -- application_date starts being captured


def _application_date_for(onboarded: date, lo: int = 3, hi: int = 45) -> date | None:
    """General rule (not one of the 3 pinned archetypes): application_date is
    populated only from Q3FY26 onward (when Acme started capturing it) -- NULL
    for earlier/legacy panel rows where it was never captured."""
    if onboarded < APPLICATION_DATE_CUTOVER:
        return None
    return onboarded - timedelta(days=random.randint(lo, hi))


# --------------------------------------------------------------------------
# New-seller onboarding funnel cohort (customer story US-7) -- ~500 sellers
# (200 Collectibles + 150 Resold + 150 Style, onboarded Q3FY26-Q4FY26) + the 3
# pinned archetypes (sel_500241-243, CANONICAL NEW-SELLER ARCHETYPES). This
# cohort is one of dim_seller's three deliberate strata (top sellers + random
# tail + this funnel cohort) -- NOT additional rows on top -- so gen_dim_seller
# shrinks its random-filler count by the same amount, keeping the panel at the
# canon-stated ~2,560. Drives the exact listing-count funnel percentages + the
# verification-timing split consumed by gen_new_seller_cohort_listings()
# (SIGNAL [seller-auth-friction]).
# --------------------------------------------------------------------------
NEW_SELLER_PINNED = [
    # seller_id, seller_name, category, application_date, onboarded_date, verified_fast, stage, sustained
    ("sel_500241", "Thistledown Card Co.", "collectibles", date(2025, 11, 3), date(2025, 11, 10), False, "never5", False),
    ("sel_500242", "Wrenfield Collectibles", "collectibles", date(2025, 10, 2), date(2025, 10, 8), True, "reach10", True),
    ("sel_500243", "Larkspur Apparel Co.", "style", date(2025, 12, 1), date(2025, 12, 5), None, "reach10", False),
]
NEW_SELLER_PINNED_IDS = {r[0] for r in NEW_SELLER_PINNED}

# category -> (n_total INCLUDING the pinned archetypes, n_reach5 [>=5, cumulative],
# n_reach10 [>=10, cumulative], n_sustained [subset of n_reach10])
NEW_SELLER_FUNNEL = {
    "collectibles": (200, 92, 48, 38),
    "resold": (150, 111, 69, 60),
    "style": (150, 114, 72, 63),
}
# Collectibles-only verification-speed split (debut listing GradeSure-verified within 7
# days or not), each bucket with its OWN listing-10 clear rate -- SIGNAL [seller-auth-friction].
COLLECTIBLES_VERIFIED_SPLIT = {"fast_n": 120, "slow_n": 80, "fast_reach10": 36, "slow_reach10": 12}


def _assign_cohort_stages(n_total: int, n_reach10: int, n_reach5: int, n_sustained: int,
                            fast_n: int | None = None, fast_reach10: int | None = None
                            ) -> tuple[list[str], list[bool], list[bool | None]]:
    """Deterministic-count, randomly-shuffled bucket assignment for n_total
    GENERIC (non-pinned) cohort sellers. Returns parallel lists (stage,
    sustained, verified_fast) of length n_total, stage in
    {"never5","reach5","reach10"}. The reach5/never5 split is intentionally
    NOT correlated with the fast/slow verification bucket beyond the stated
    reach10 sub-rates -- canon gives no basis for correlating the earlier
    stages to verification speed, only the listing-10 clear rate."""
    idx = list(range(n_total))
    random.shuffle(idx)
    if fast_n is not None:
        fast_idx = set(idx[:fast_n])
        fast_list = [i for i in idx if i in fast_idx]
        slow_list = [i for i in idx if i not in fast_idx]
        reach10_idx = set(random.sample(fast_list, fast_reach10) + random.sample(slow_list, n_reach10 - fast_reach10))
        fast_flags = {i: (i in fast_idx) for i in idx}
    else:
        reach10_idx = set(random.sample(idx, n_reach10))
        fast_flags = {i: None for i in idx}
    remaining = [i for i in idx if i not in reach10_idx]
    reach5only_idx = set(random.sample(remaining, n_reach5 - n_reach10))
    sustained_idx = set(random.sample(sorted(reach10_idx), n_sustained))

    stages, sustained, fast = [], [], []
    for i in range(n_total):
        if i in reach10_idx:
            stages.append("reach10")
        elif i in reach5only_idx:
            stages.append("reach5")
        else:
            stages.append("never5")
        sustained.append(i in sustained_idx)
        fast.append(fast_flags[i])
    return stages, sustained, fast


def _cohort_listing_count(stage: str, sustained: bool) -> int:
    if stage == "never5":
        # steepest relative drop happens earliest (listing 1->5) -- skew low
        return random.choices([1, 2, 3, 4], weights=[0.40, 0.30, 0.20, 0.10])[0]
    if stage == "reach5":
        return random.randint(5, 9)
    return random.randint(12, 25) if sustained else random.randint(10, 14)


def _cohort_listing_schedule(onboarded: date, n_listings: int, sustained: bool) -> list[date]:
    """Spread n_listings dates from onboarding. Non-sustained sellers stop
    well before the trailing-90d window (TODAY-90); sustained sellers get
    >=1 listing inside it -- the observable proxy for "10+ listings AND >=1
    new listing in trailing 90d" since there's no separate activity-date
    column on fact_marketplace_listings."""
    if n_listings <= 0:
        return []
    recent_cutoff = TODAY - timedelta(days=90)
    if sustained:
        tail = TODAY - timedelta(days=random.randint(2, 80))
        if n_listings == 1:
            return [tail]
        span_end = max(recent_cutoff - timedelta(days=random.randint(0, 20)), onboarded + timedelta(days=1))
        span = max((span_end - onboarded).days, 1)
        head = sorted(onboarded + timedelta(days=random.randint(0, span)) for _ in range(n_listings - 1))
        return head + [tail]
    stop_days = random.randint(30, 150)
    cap = min(onboarded + timedelta(days=stop_days), recent_cutoff - timedelta(days=random.randint(1, 30)))
    cap = max(cap, onboarded + timedelta(days=1))
    span = max((cap - onboarded).days, 1)
    return sorted(onboarded + timedelta(days=random.randint(0, span)) for _ in range(n_listings))


def _cohort_listing_rows(seller_id: str, cat: str, stage: str, verified_fast: bool | None,
                          dates: list[date], listing_seq: list[int]) -> list[dict]:
    price_mu = {"collectibles": 70, "resold": 35, "style": 55}[cat]
    base_verified_p = {"resold": 0.20, "style": 0.15}.get(cat)
    removed_w = [0.75, 0.20, 0.05] if stage == "never5" else [0.93, 0.05, 0.02]
    out = []
    for li, ldate in enumerate(dates):
        listing_seq[0] += 1
        price = float(np.random.lognormal(np.log(price_mu), 0.9 if cat == "collectibles" else 0.6))
        if cat == "collectibles":
            if li == 0:
                verified = (random.random() < 0.95) if verified_fast else (random.random() < 0.35)
            else:
                verified = random.random() < 0.90
        else:
            verified = random.random() < base_verified_p
        out.append({
            "listing_id": rid("lst", 900_000 + listing_seq[0], width=7), "seller_id": seller_id,
            "category": cat, "listed_date": ldate, "price_usd": round(price, 2),
            "status": random.choices(["active", "removed", "suspended"], weights=removed_w)[0],
            "authenticity_verified": verified,
        })
    return out


def gen_new_seller_cohort() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (dim_seller-shaped rows w/ bookkeeping cols, fact_marketplace_listings
    -shaped rows) for the ~500-seller new-seller onboarding funnel cohort + the 3
    pinned archetypes (sel_500241-243)."""
    seller_rows: list[dict] = []
    listing_rows: list[dict] = []
    listing_seq = [0]
    next_id = 500244
    name_suffixes = ["Trading Co.", "Goods", "Supply", "Collective", "Studio", "Outfitters", "Market", "House"]
    onboard_lo, onboard_hi = date(2025, 8, 1), date(2026, 1, 31)

    # per-category generic (non-pinned) bucket targets, after deducting the 3 pinned slots
    generic_targets = {
        "collectibles": dict(n_total=198, n_reach5=91, n_reach10=47, n_sustained=37, fast_n=119, fast_reach10=35),
        "resold": dict(n_total=150, n_reach5=111, n_reach10=69, n_sustained=60, fast_n=None, fast_reach10=None),
        "style": dict(n_total=149, n_reach5=113, n_reach10=71, n_sustained=63, fast_n=None, fast_reach10=None),
    }

    for cat, tgt in generic_targets.items():
        stages, sustained_flags, fast_flags = _assign_cohort_stages(
            tgt["n_total"], tgt["n_reach10"], tgt["n_reach5"], tgt["n_sustained"],
            fast_n=tgt["fast_n"], fast_reach10=tgt["fast_reach10"])
        for i in range(tgt["n_total"]):
            seller_id = rid("sel", next_id, width=6)
            next_id += 1
            onboarded = onboard_lo + timedelta(days=random.randint(0, (onboard_hi - onboard_lo).days))
            stage, sustained, verified_fast = stages[i], sustained_flags[i], fast_flags[i]
            if verified_fast is True:
                application_date = onboarded - timedelta(days=random.randint(1, 6))
            elif verified_fast is False:
                application_date = onboarded - timedelta(days=random.randint(7, 30))
            else:
                application_date = onboarded - timedelta(days=random.randint(3, 14))
            name = f"{fake.last_name()} {random.choice(name_suffixes)}"
            seller_rows.append({
                "seller_id": seller_id, "seller_name": name, "category_focus": cat,
                "onboarded_date": onboarded, "application_date": application_date, "status": "active",
                "fulfillment_method": random.choices(["seller_fulfilled", "ship_with_acme"], weights=[0.70, 0.30])[0],
                "home_country": random.choices(["US", "CA", "MX"], weights=[0.85, 0.10, 0.05])[0],
                "_gmv_tier": "small",
            })
            n_listings = _cohort_listing_count(stage, sustained)
            dates = _cohort_listing_schedule(onboarded, n_listings, sustained)
            listing_rows += _cohort_listing_rows(seller_id, cat, stage, verified_fast, dates, listing_seq)

    for sid, name, cat, app_date, onboarded, verified_fast, stage, sustained in NEW_SELLER_PINNED:
        seller_rows.append({
            "seller_id": sid, "seller_name": name, "category_focus": cat,
            "onboarded_date": onboarded, "application_date": app_date, "status": "active",
            "fulfillment_method": "seller_fulfilled", "home_country": "US", "_gmv_tier": "small",
        })
        n_listings = 3 if sid == "sel_500241" else (12 if sid == "sel_500242" else 10)
        if sid == "sel_500243":
            # "reached listing 10 within 10 weeks" -- force all 10 inside that window
            span = 70
            dates = sorted(onboarded + timedelta(days=random.randint(0, span)) for _ in range(n_listings))
        else:
            dates = _cohort_listing_schedule(onboarded, n_listings, sustained)
        listing_rows += _cohort_listing_rows(sid, cat, stage, verified_fast, dates, listing_seq)

    return pd.DataFrame(seller_rows), pd.DataFrame(listing_rows)


def gen_dim_seller(n_total: int = 2560) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (dim_seller, cohort_listings) -- the second element is the
    pre-built fact_marketplace_listings rows for the new-seller cohort, which
    must be merged into the final fact_marketplace_listings table by the
    caller (see gen_fact_marketplace_listings's exclude_seller_ids param)."""
    rows = []
    for sid, name, cat, tier, onboard, status, fmethod, country in PINNED_SELLERS + SHARED_CAST_SELLERS:
        rows.append({
            "seller_id": sid, "seller_name": name, "category_focus": cat, "onboarded_date": onboard,
            "application_date": _application_date_for(onboard),
            "status": status, "fulfillment_method": fmethod, "home_country": country, "_gmv_tier": tier,
        })

    cohort_sellers, cohort_listings = gen_new_seller_cohort()
    rows += cohort_sellers.to_dict("records")

    n_filler = n_total - len(rows)
    cats = ["collectibles", "resold", "style", "other"]
    cat_w = [0.20, 0.28, 0.40, 0.12]
    tiers = ["top", "large", "mid", "small"]
    tier_w = [0.01, 0.04, 0.25, 0.70]
    countries = ["US", "CA", "MX"]
    country_w = [0.80, 0.12, 0.08]
    next_num = 501000  # past the new-seller cohort's reserved 500244-500740 range
    for i in range(n_filler):
        cat = random.choices(cats, weights=cat_w)[0]
        onboard = date(2024, 1, 1) + timedelta(days=random.randint(0, (TODAY - date(2024, 1, 1)).days))
        status = random.choices(["active", "suspended", "offboarded"], weights=[0.92, 0.04, 0.04])[0]
        name = f"{fake.last_name()} {random.choice(['& Co.', 'Trading Co.', 'Goods', 'Supply', 'Collective', 'Studio', 'Works', 'Outfitters'])}"
        rows.append({
            "seller_id": rid("sel", next_num, width=6), "seller_name": name, "category_focus": cat,
            "onboarded_date": onboard, "application_date": _application_date_for(onboard), "status": status,
            "fulfillment_method": random.choices(["seller_fulfilled", "ship_with_acme"], weights=[0.65, 0.35])[0],
            "home_country": random.choices(countries, weights=country_w)[0],
            "_gmv_tier": random.choices(tiers, weights=tier_w)[0],
        })
        next_num += 1
    df = pd.DataFrame(rows)
    return df, cohort_listings


def gen_dim_experiment(n_total: int = 85) -> pd.DataFrame:
    rows = []
    for eid, name, vc, owner, hyp, start, end, status, metric in NAMED_EXPERIMENTS:
        rows.append({
            "experiment_id": eid, "experiment_name": name, "vertical_code": vc, "owner_assoc_id": owner,
            "hypothesis": hyp, "start_date": start, "end_date": end, "status": status, "primary_metric": metric,
        })
    verticals_pool = ["US_CONV", "MARKETPLACE", "CARE", "SPEED", "MEMBERSHIP", "CLUB", "B2B", "PAYMENTS",
                      "MARTECH", "MPCX", "REVIEWS"]
    vert_w = [0.22, 0.18, 0.16, 0.16, 0.12, 0.03, 0.03, 0.03, 0.03, 0.02, 0.02]
    owners = [a[0] for a in NAMED_ASSOCIATES if a[3] in ("Product", "Marketplace", "Care", "Fulfillment", "Membership")]
    hyp_templates = [
        "A UI change to {area} improves {metric}.",
        "A new {area} algorithm improves {metric} without hurting guardrails.",
        "Changing {area} messaging improves {metric}.",
        "A pricing/promo change on {area} improves {metric}.",
        "Reducing friction in {area} improves {metric}.",
    ]
    areas = ["search ranking", "PDP layout", "cart", "notifications", "onboarding", "recommendations",
             "returns flow", "seller onboarding", "listing quality", "delivery messaging", "loyalty prompts"]
    metrics_pool = ["conversion_rate", "on_time_rate", "deflection_rate", "return_rate", "renewal_rate",
                    "aov", "csat", "seller_nps"]
    statuses = ["running", "shipped", "killed", "paused"]
    status_w = [0.20, 0.45, 0.25, 0.10]
    next_num = 3000
    for qi, q in enumerate(QUARTERS):
        n_this_q = max(0, (n_total - len(NAMED_EXPERIMENTS)) // 6)
        for _ in range(n_this_q):
            start = q.start + timedelta(days=random.randint(0, max(1, (q.data_end - q.start).days)))
            dur = random.randint(14, 56)
            status = random.choices(statuses, weights=status_w)[0]
            end = start + timedelta(days=dur) if status != "running" else None
            if end and end > TODAY:
                end = None
                status = "running"
            vc = random.choices(verticals_pool, weights=vert_w)[0]
            hyp = random.choice(hyp_templates).format(area=random.choice(areas), metric=random.choice(metrics_pool))
            rows.append({
                "experiment_id": rid("exp", next_num, width=4), "experiment_name": f"{random.choice(areas).title()} Test {next_num}",
                "vertical_code": vc, "owner_assoc_id": random.choice(owners), "hypothesis": hyp,
                "start_date": start, "end_date": end, "status": status,
                "primary_metric": random.choice(metrics_pool),
            })
            next_num += 1
    return pd.DataFrame(rows)


def gen_dim_marketing_calendar(n_total: int = 140) -> pd.DataFrame:
    rows = []
    for eid, name, etype, vc, market, start, end, owner, notes in NAMED_MARKETING_EVENTS:
        rows.append({
            "event_id": eid, "event_name": name, "event_type": etype, "vertical_code": vc, "market": market,
            "start_date": start, "end_date": end, "planned_spend_usd": None, "actual_spend_usd": None,
            "owner_assoc_id": owner, "notes": notes,
        })
    holidays = [
        ("Valentine's Day", (2, 14)), ("Memorial Day", (5, 26)), ("Independence Day", (7, 4)),
        ("Labor Day", (9, 1)), ("Halloween", (10, 31)), ("Back to School", (8, 15)),
        ("Mother's Day", (5, 11)), ("Father's Day", (6, 15)), ("Christmas", (12, 25)),
        ("New Year Sale", (1, 2)),
    ]
    owners = [a[0] for a in NAMED_ASSOCIATES]
    n_filler = n_total - len(rows)
    campaign_templates = ["{v} Spring Refresh", "{v} Loyalty Push", "{v} Flash Sale", "{v} Awareness Campaign",
                          "{v} Retention Offer", "{v} Category Spotlight"]
    verticals_pool = ["US_CONV", "MARKETPLACE", "CARE", "SPEED", "MEMBERSHIP", "CLUB", "MARTECH", "B2B"]
    for i in range(n_filler):
        if i < len(holidays) * 2:
            name, (m, d) = holidays[i % len(holidays)]
            yr = 2025 if i < len(holidays) else 2026
            try:
                start = date(yr, m, d)
            except ValueError:
                start = date(yr, m, 28)
            if start < DIM_DATE_START or start > DIM_DATE_END:
                continue
            rows.append({
                "event_id": rid("camp", 100 + i, width=6), "event_name": name, "event_type": "holiday",
                "vertical_code": None, "market": None, "start_date": start, "end_date": start,
                "planned_spend_usd": None, "actual_spend_usd": None, "owner_assoc_id": random.choice(owners),
                "notes": "Recurring retail calendar event.",
            })
        else:
            vc = random.choice(verticals_pool)
            start = DIM_DATE_START + timedelta(days=random.randint(30, (min(TODAY, DIM_DATE_END) - DIM_DATE_START).days))
            dur = random.randint(7, 45)
            planned = round(random.uniform(20_000, 900_000), 2)
            actual = round(planned * random.uniform(0.85, 1.10), 2)
            rows.append({
                "event_id": rid("camp", 100 + i, width=6),
                "event_name": random.choice(campaign_templates).format(v=vc.title()),
                "event_type": random.choices(["campaign", "promo"], weights=[0.6, 0.4])[0],
                "vertical_code": vc, "market": random.choice(MARKETS + [None]),
                "start_date": start, "end_date": start + timedelta(days=dur),
                "planned_spend_usd": planned, "actual_spend_usd": actual,
                "owner_assoc_id": random.choice(owners), "notes": "Standard marketing calendar entry.",
            })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# dim_member + membership lifecycle simulation (drives fact_membership_events,
# SIGNAL [cltv-join-drop], SIGNAL [benefit-adoption-cltv])
# --------------------------------------------------------------------------
BENEFIT_CODES = ["early_access", "streaming_bundle", "member_pricing", "birthday_reward", "extended_returns"]
# free_shipping is the baseline every paying member has -- not counted toward "extra benefit depth".

# Renewal-rate-by-benefit-depth base rates (SIGNAL [benefit-adoption-cltv]): 0 extra benefits=71%,
# streaming-bundle-alone=93%, other-single-benefit solved so the 1-benefit cohort blends to 89%
# (0.40*93 + 0.60*R = 89 -> R = 86.33), 2+ benefits=95%.
BASE_RENEWAL_RATE = {0: 0.71, "streaming": 0.93, "other1": 0.8633, 2: 0.95}
# small per-quarter uplift so the depth-mix-weighted average matches canon's stated overall
# renewal_pct per quarter (86.2..87.2) -- solved against the 30/40(16 streaming/24 other)/30 depth mix.
Q_RENEWAL_DELTA_PP = [0.90, 0.76, 1.13, 1.43, 0.58, 0.52]


def quarter_index_for_date(d: date) -> int | None:
    for i, q in enumerate(QUARTERS):
        if q.start <= d <= q.end:
            return i
    return None


def cohort_renewal_rate(depth: int, streaming_only: bool, quarter_idx: int) -> float:
    if depth <= 0:
        base = BASE_RENEWAL_RATE[0]
    elif depth == 1:
        base = BASE_RENEWAL_RATE["streaming"] if streaming_only else BASE_RENEWAL_RATE["other1"]
    else:
        base = BASE_RENEWAL_RATE[2]
    return min(0.99, base + Q_RENEWAL_DELTA_PP[quarter_idx] / 100.0)


def gen_dim_member(n_total: int = 120_000) -> pd.DataFrame:
    n_dormant = 24_000  # SIGNAL [cltv-join-drop]: exactly 20% of the 120,000-member panel
    dormant_idx = set(np.random.choice(n_total, size=n_dormant, replace=False).tolist())
    dormant_idx.discard(41)    # Dana -- never dormant
    dormant_idx.discard(389)   # Jamal
    dormant_idx.discard(511)   # Grethe
    dormant_idx.discard(639)   # Oskar
    dormant_idx.add(177)       # Marisol -- forced dormant (canon poster child)
    # keep the forced set at exactly 24,000
    while len(dormant_idx) < n_dormant:
        cand = random.randint(0, n_total - 1)
        if cand not in (41, 389, 511, 639):
            dormant_idx.add(cand)
    while len(dormant_idx) > n_dormant:
        cand = next(iter(dormant_idx - {177}))
        dormant_idx.discard(cand)

    depth_roll = np.random.random(n_total)
    depths = np.where(depth_roll < 0.30, 0, np.where(depth_roll < 0.70, 1, 2))
    streaming_only = (depths == 1) & (np.random.random(n_total) < 0.40)
    plan_types = np.random.choice(["annual", "monthly"], size=n_total, p=[0.60, 0.40])
    home_markets = np.random.choice(MARKETS, size=n_total, p=[0.70, 0.18, 0.12])
    channels = np.random.choice(
        ["organic", "paid_search", "promo", "referral", "partner", "store"], size=n_total,
        p=[0.30, 0.20, 0.15, 0.15, 0.10, 0.10],
    )

    # signup dates: 78% long-tenured (spread well before the modeled window -- a mature membership
    # base), 22% distributed across the 6 modeled quarters proportional to net_adds_k SHAPE (flavor
    # realism only -- true-base member counts are NOT derivable from this panel, convention 5).
    pre_window_mask = np.random.random(n_total) < 0.78
    pre_start, pre_end = date(2015, 1, 1), date(2025, 1, 31)
    pre_span = (pre_end - pre_start).days
    q_weights = np.array(MEMBERSHIP["net_adds_k"], dtype=float)
    q_weights = q_weights / q_weights.sum()

    rows = []
    for i in range(n_total):
        mid = rid("mem", 1000001 + i, width=7)
        is_dormant = i in dormant_idx
        depth = int(depths[i])
        stream_only = bool(streaming_only[i])
        plan_type = plan_types[i]
        home_market = home_markets[i]
        channel = channels[i]
        if pre_window_mask[i]:
            signup = pre_start + timedelta(days=int(np.random.beta(2.0, 1.0) * pre_span))
        else:
            qi = np.random.choice(6, p=q_weights)
            q = QUARTERS[qi]
            span = max((q.data_end - q.start).days, 1)
            signup = q.start + timedelta(days=random.randint(0, span))

        if i == 41:  # Dana -- power benefit-user, 4yr tenure, renews every year, high CLTV
            plan_type, depth, stream_only, is_dormant = "annual", 2, False, False
            signup = TODAY - timedelta(days=round(4 * 365.25))
        elif i == 177:  # Marisol -- dormant, poster child for [cltv-join-drop]
            plan_type, is_dormant = "annual", True
            signup = TODAY - timedelta(days=round(2.5 * 365.25))
        elif i == 389:  # Jamal -- churn-risk, 2 open P1 care contacts, NPS detractor
            depth, is_dormant = 0, False
            signup = TODAY - timedelta(days=round(1.5 * 365.25))
        elif i == 511:  # Grethe -- churned after 2 late ship-to-home deliveries
            depth, is_dormant = 0, False
            signup = TODAY - timedelta(days=round(1.0 * 365.25))
        elif i == 639:  # Oskar -- signed up via Fall Savings promo, 2-benefit adopter, renews reliably
            plan_type, depth, stream_only, channel, is_dormant = "annual", 1, False, "promo", False
            signup = date(2025, 9, 25)

        price = 98.00 if plan_type == "annual" else 14.95
        rows.append({
            "member_id": mid, "signup_date": signup, "home_market": home_market,
            "plan_type": plan_type, "plan_price_usd": price,
            "status": "active", "cancel_date": None, "acquisition_channel": channel,
            "dormant_flag": is_dormant, "depth_flag": depth, "streaming_only_flag": stream_only,
        })
    return pd.DataFrame(rows)


def simulate_membership_lifecycle(dm: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Walk each annual-plan member's yearly renewal decisions (drawn from
    `cohort_renewal_rate`) through the modeled window, and give monthly-plan
    members an independent simple churn hazard. Emits signup/renewal/cancel/
    benefit_redeemed rows for fact_membership_events and finalizes each
    member's dim_member status/cancel_date to match."""
    window_start, window_end = QUARTERS[0].start, TODAY
    events: list[dict] = []
    statuses: list[str] = []
    cancel_dates: list[object] = []

    for row in dm.itertuples(index=False):
        mid = row.member_id
        signup = row.signup_date
        events.append({"member_id": mid, "event_date": signup, "event_type": "signup", "benefit_code": None,
                       "channel": row.acquisition_channel})
        status, cancel_date = "active", None

        if row.plan_type == "annual":
            anniversary = signup + timedelta(days=365)
            while anniversary <= window_end:
                if anniversary < window_start:
                    anniversary += timedelta(days=365)
                    continue
                qi = quarter_index_for_date(anniversary)
                if qi is None:
                    anniversary += timedelta(days=365)
                    continue
                rate = cohort_renewal_rate(row.depth_flag, row.streaming_only_flag, qi)
                if random.random() < rate:
                    events.append({"member_id": mid, "event_date": anniversary, "event_type": "renewal",
                                   "benefit_code": None, "channel": "email"})
                    anniversary += timedelta(days=365)
                else:
                    events.append({"member_id": mid, "event_date": anniversary, "event_type": "cancel",
                                   "benefit_code": None, "channel": "email"})
                    status, cancel_date = "cancelled", anniversary
                    break
            if status == "active" and random.random() < 0.015:
                status = "paused"
        else:  # monthly -- independent simple hazard, not tied to the benefit-depth signal
            d = signup + timedelta(days=30)
            while d <= window_end:
                if random.random() < 0.02:
                    status, cancel_date = "cancelled", d
                    events.append({"member_id": mid, "event_date": d, "event_type": "cancel",
                                   "benefit_code": None, "channel": "email"})
                    break
                d += timedelta(days=30)
            if status == "active" and random.random() < 0.01:
                status = "paused"

        # named-archetype status overrides
        if mid == "mem_1000178":  # Marisol -- still paying/active despite being order-dormant
            status, cancel_date = "active", None
        elif mid == "mem_1000512":  # Grethe -- churned
            status = "cancelled"
            cancel_date = cancel_date or (TODAY - timedelta(days=200))

        active_until = min(cancel_date, window_end) if cancel_date else window_end
        active_span = max((active_until - max(signup, window_start)).days, 0)
        active_start = max(signup, window_start)

        def redeem(code: str, every_days: float, cap: int) -> None:
            if active_span <= 0:
                return
            n = min(int(np.random.poisson(active_span / every_days)), cap)
            for _ in range(n):
                ed = active_start + timedelta(days=random.randint(0, active_span))
                events.append({"member_id": mid, "event_date": ed, "event_type": "benefit_redeemed",
                               "benefit_code": code, "channel": random.choice(["web", "app"])})

        redeem("free_shipping", 400.0, 6)
        extra: list[str] = []
        if row.depth_flag >= 1:
            extra.append("streaming_bundle" if row.streaming_only_flag else random.choice(
                [b for b in BENEFIT_CODES if b != "streaming_bundle"]))
        if row.depth_flag >= 2:
            pool = [b for b in BENEFIT_CODES if b not in extra]
            extra += random.sample(pool, k=min(len(pool), 1))
        for code in extra:
            redeem(code, 500.0, 5)

        statuses.append(status)
        cancel_dates.append(cancel_date)

    dm = dm.copy()
    dm["status"] = statuses
    dm["cancel_date"] = cancel_dates
    ev = pd.DataFrame(events).sort_values(["event_date", "member_id"]).reset_index(drop=True)
    ev.insert(0, "event_id", [rid("mbev", i + 1, width=7) for i in range(len(ev))])
    return dm, ev


# --------------------------------------------------------------------------
# fact_traffic_daily -- full population. US_CONV (deep, per-market canon targets),
# Marketplace (deep, per-sub-vertical GMV targets), and 9 "light" verticals
# (metric rows only, no canon targets). This is the table SIGNAL
# [session-definition] lives in, and the jitter fix (status-check note #3)
# is implemented in `_us_conv_rates_for_quarter` below.
# --------------------------------------------------------------------------
DEVICE_SHARE = {"web": 0.55, "app": 0.42, "store_kiosk": 0.03}
LIGHT_VERTICALS = ["CLUB", "B2B", "PAYMENTS", "MARTECH", "MPCX", "SPLITS", "CSI", "REVIEWS", "FS_LATER"]
LIGHT_VERTICAL_BASE_SESSIONS = {
    "CLUB": 900, "B2B": 120, "PAYMENTS": 500, "MARTECH": 350, "MPCX": 300,
    "SPLITS": 220, "CSI": 150, "REVIEWS": 600, "FS_LATER": 380,
}

# Item Page surface (SIGNAL [item-page-metric-choice]): product_view_sessions holds
# to ~62% of US_CONV sessions everywhere; add_to_cart_sessions/product_view_sessions
# jumps at the SAME sessions_definition_version cutover as the site-wide conversion
# rate (SIGNAL [session-definition]) -- 18.0% pre-cutover -> 19.9% post, the exact
# Q1FY27 raw move canon states (the two version-bases apply uniformly, not just
# within Q1FY27, since the cutover only ever occurs once in the modeled window).
PV_SHARE_OF_SESSIONS = 0.62
VIEW_TO_CART_RATE = {1: 0.180, 2: 0.199}

# US Conversion -- weekly detail (Q2FY27, the live WoW question): the only two days
# spans in the whole dataset where device carries a DIFFERENTIATED conversion rate
# (elsewhere device is a flat proportional split of the blended day rate). US market
# only. Week-over-week: 3.24% -> 2.86%, decomposing into -0.24pp device-mix shift
# (app share 28.0%->37.6%) and -0.14pp real web-conversion softening.
WOW_WEEK_STARTS = [date(2026, 7, 5), date(2026, 7, 12)]  # Sun-Sat weeks ending 07-11 / 07-18
WOW_WEEKS = {
    date(2026, 7, 5): dict(sessions_m=26.80, orders=868_320,
                            device_share={"web": 0.690, "app": 0.280, "store_kiosk": 0.030},
                            device_conv={"web": 0.0400, "app": 0.0150, "store_kiosk": 0.0200}),
    date(2026, 7, 12): dict(sessions_m=26.40, orders=755_038,
                             device_share={"web": 0.594, "app": 0.376, "store_kiosk": 0.030},
                             device_conv={"web": 0.0376, "app": 0.0150, "store_kiosk": 0.0200}),
}


def _pv_atc_daily(dates: list[date], sessions_daily: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Exact-reconciling product_view_sessions / add_to_cart_sessions per day,
    aligned with `sessions_daily` (allocate_int against the day's ACTUAL
    allocated sessions, not the nominal quarter target, so pv <= sessions
    always holds)."""
    n = len(dates)
    pv_jitter = np.random.normal(1.0, 0.015, size=n)
    pv_total = int(round(sessions_daily.sum() * PV_SHARE_OF_SESSIONS))
    pv_daily = allocate_int(pv_total, np.maximum(sessions_daily * pv_jitter, 1e-6))

    is_v2 = np.array([d >= SESSION_CUTOVER for d in dates])
    atc_daily = np.zeros(n, dtype=np.int64)
    atc_jitter = np.random.normal(1.0, 0.02, size=n)
    for mask, rate in ((~is_v2, VIEW_TO_CART_RATE[1]), (is_v2, VIEW_TO_CART_RATE[2])):
        if not mask.any():
            continue
        sub_pv = pv_daily[mask]
        sub_total = int(round(sub_pv.sum() * rate))
        atc_daily[mask] = allocate_int(sub_total, np.maximum(sub_pv * atc_jitter[mask], 1e-6))
    return pv_daily, atc_daily


def _wow_week_series(wk_start: date, info: dict) -> list[tuple[date, int, int, dict, dict]]:
    """One named Q2FY27 WoW week -> per-day (date, sessions, orders,
    device_sessions, device_orders), exact to the week's stated sessions/order
    totals and device mix/conversion rates (convention 1: the stated ORDER
    total is authoritative -- recomputing from the rounded device conv rates
    may drift by a rounding hair, expected, not "corrected" back)."""
    week_dates = [wk_start + timedelta(days=k) for k in range(7)]
    day_w = daily_weight_curve(week_dates, weekend_boost=1.05, noise_sd=0.03)
    sess_by_day = allocate_int(round(info["sessions_m"] * 1_000_000), day_w)

    device_sessions_by_day = []
    devices = list(info["device_share"].keys())
    shares = np.array(list(info["device_share"].values()))
    for s_day in sess_by_day:
        dev_counts = allocate_int(int(s_day), shares)
        device_sessions_by_day.append(dict(zip(devices, (int(x) for x in dev_counts))))

    cells = [(i, dev) for i in range(7) for dev in devices]
    raw_w = np.array([max(device_sessions_by_day[i][dev] * info["device_conv"][dev], 1e-6) for i, dev in cells])
    counts = allocate_int(info["orders"], raw_w)
    device_orders_by_day = [dict() for _ in range(7)]
    for (i, dev), c in zip(cells, counts):
        device_orders_by_day[i][dev] = int(c)

    return [(d, int(sess_by_day[i]), sum(device_orders_by_day[i].values()),
             device_sessions_by_day[i], device_orders_by_day[i]) for i, d in enumerate(week_dates)]


def _us_conv_rates_for_quarter(dates: list[date], sessions_total_m: float, orders_total_m: float) -> tuple[np.ndarray, np.ndarray]:
    """Per-day (sessions, conversion-rate) for one market x quarter slice.
    Handles the sessions_definition_version cutover (mechanical rate jump,
    SIGNAL [session-definition]) and applies INDEPENDENT day-level jitter to
    the realized rate so cross-market gaps aren't bit-exact constant week to
    week -- while sessions*rate is rescaled to hit the exact quarter totals."""
    n = len(dates)
    sess_weights = daily_weight_curve(dates)
    sessions_daily = allocate_float(sessions_total_m * 1_000_000, sess_weights, decimals=0)

    is_v2 = np.array([d >= SESSION_CUTOVER for d in dates])
    blended_rate = orders_total_m / sessions_total_m
    if is_v2.any() and (~is_v2).any():
        w1, w2 = sessions_daily[~is_v2].sum(), sessions_daily[is_v2].sum()
        c1 = blended_rate * (w1 + w2) / (w1 + R_JUMP * w2)
        c2 = R_JUMP * c1
        base_rate = np.where(is_v2, c2, c1)
    else:
        base_rate = np.full(n, blended_rate)

    jitter = np.random.normal(1.0, 0.035, size=n)
    noisy_rate = np.clip(base_rate * jitter, 0.0002, None)
    orders_raw = sessions_daily * noisy_rate
    orders_daily = allocate_int(round(orders_total_m * 1_000_000), orders_raw)
    return sessions_daily.astype(np.int64), orders_daily


def gen_fact_traffic_daily() -> pd.DataFrame:
    rows = []
    for qi, q in enumerate(QUARTERS):
        dates = quarter_dates(q)
        versions = [1 if d < SESSION_CUTOVER else 2 for d in dates]

        # ---- US_CONV: deep, per-market canon targets ----
        for market in MARKETS:
            sessions_total = US_CONV[market]["sessions_m"][qi]
            orders_total = US_CONV[market]["orders_m"][qi]
            gmv_total = US_CONV[market]["gmv_m"][qi]

            # US Conversion weekly detail: the two named Q2FY27 WoW weeks get an
            # exact device mix/conversion override, US market only. Generate them
            # from their OWN stated totals, subtract that budget from the normal
            # quarter-level allocation, then stitch both back into calendar order
            # -- so the quarter grand total is untouched (no regression).
            wow_daily: dict[date, tuple[int, int, dict, dict]] = {}
            if market == "US" and q.label == "Q2FY27":
                for wk in WOW_WEEK_STARTS:
                    for d, sess, ordr, dev_sess, dev_ord in _wow_week_series(wk, WOW_WEEKS[wk]):
                        wow_daily[d] = (sess, ordr, dev_sess, dev_ord)
                override_dates = set(wow_daily.keys())
                other_dates = [d for d in dates if d not in override_dates]
                override_sessions_m = sum(v[0] for v in wow_daily.values()) / 1_000_000
                override_orders_m = sum(v[1] for v in wow_daily.values()) / 1_000_000
                sess_other, ord_other = _us_conv_rates_for_quarter(
                    other_dates, sessions_total - override_sessions_m, orders_total - override_orders_m)
                other_map = {d: (int(sess_other[j]), int(ord_other[j])) for j, d in enumerate(other_dates)}
                sessions_daily = np.array([other_map[d][0] if d in other_map else wow_daily[d][0] for d in dates])
                orders_daily = np.array([other_map[d][1] if d in other_map else wow_daily[d][1] for d in dates])
            else:
                sessions_daily, orders_daily = _us_conv_rates_for_quarter(dates, sessions_total, orders_total)

            aov_noise = np.random.normal(1.0, 0.05, size=len(dates))
            gmv_daily = allocate_float(gmv_total * 1_000_000, np.maximum(orders_daily * aov_noise, 1e-6), decimals=2)
            units_mult = np.random.normal(1.5, 0.15, size=len(dates))
            pv_daily, atc_daily = _pv_atc_daily(dates, sessions_daily)

            for i, d in enumerate(dates):
                s, o, g = int(sessions_daily[i]), int(orders_daily[i]), float(gmv_daily[i])
                pv, atc = int(pv_daily[i]), int(atc_daily[i])
                cos = int(round(atc * np.random.normal(0.55, 0.03)))
                cos = max(cos, o)
                if d in wow_daily:
                    _, _, dev_sess, dev_ord = wow_daily[d]
                    for dev, dsess in dev_sess.items():
                        frac = dsess / s if s > 0 else 0.0
                        dord = dev_ord.get(dev, 0)
                        rows.append({
                            "date": d, "market": market, "vertical_code": "US_CONV", "sub_vertical_code": None,
                            "device": dev, "sessions": dsess,
                            "sessions_definition_version": versions[i],
                            "product_view_sessions": max(int(round(pv * frac)), 0),
                            "add_to_cart_sessions": max(int(round(atc * frac)), 0),
                            "checkout_started_sessions": max(int(round(cos * frac)), dord),
                            "orders": dord, "units": max(int(round(dord * units_mult[i])), 0),
                            "gmv_usd": round(g * frac, 2),
                        })
                else:
                    for dev, dw in DEVICE_SHARE.items():
                        rows.append({
                            "date": d, "market": market, "vertical_code": "US_CONV", "sub_vertical_code": None,
                            "device": dev, "sessions": max(int(round(s * dw)), 0),
                            "sessions_definition_version": versions[i],
                            "product_view_sessions": max(int(round(pv * dw)), 0),
                            "add_to_cart_sessions": max(int(round(atc * dw)), 0),
                            "checkout_started_sessions": max(int(round(cos * dw)), 0),
                            "orders": max(int(round(o * dw)), 0), "units": max(int(round(o * dw * units_mult[i])), 0),
                            "gmv_usd": round(g * dw, 2),
                        })

        # ---- Marketplace: deep, per-sub-vertical GMV targets (invented AOV backs out orders) ----
        for sv in MARKETPLACE_SUBVERTS:
            gmv_total = MARKETPLACE_GMV_M[sv][qi]
            aov = MARKETPLACE_AOV[sv][qi]
            weights = daily_weight_curve(dates, weekend_boost=1.08)
            gmv_daily = allocate_float(gmv_total * 1_000_000, weights, decimals=2)
            aov_noise = np.random.normal(1.0, 0.06, size=len(dates))
            orders_daily = np.maximum(np.round(gmv_daily / (aov * aov_noise)), 0).astype(np.int64)
            conv_noise = np.clip(np.random.normal(0.05, 0.008, size=len(dates)), 0.015, 0.12)
            sessions_daily = np.maximum(orders_daily, 1) / conv_noise
            for i, d in enumerate(dates):
                s = int(round(sessions_daily[i]))
                o, g = int(orders_daily[i]), float(gmv_daily[i])
                pv = int(round(s * np.random.normal(0.78, 0.03)))
                atc = int(round(pv * np.random.normal(0.30, 0.03)))
                cos = max(int(round(atc * np.random.normal(0.50, 0.03))), o)
                for dev, dw in DEVICE_SHARE.items():
                    rows.append({
                        "date": d, "market": "US", "vertical_code": "MARKETPLACE", "sub_vertical_code": sv,
                        "device": dev, "sessions": max(int(round(s * dw)), 0),
                        "sessions_definition_version": versions[i],
                        "product_view_sessions": max(int(round(pv * dw)), 0),
                        "add_to_cart_sessions": max(int(round(atc * dw)), 0),
                        "checkout_started_sessions": max(int(round(cos * dw)), 0),
                        "orders": max(int(round(o * dw)), 0),
                        "units": max(int(round(o * dw * np.random.normal(1.2, 0.1))), 0),
                        "gmv_usd": round(g * dw, 2),
                    })

        # ---- Light verticals: metric rows only, no canon targets ----
        for vc in LIGHT_VERTICALS:
            base = LIGHT_VERTICAL_BASE_SESSIONS[vc]
            for d in dates:
                s = int(np.random.poisson(base))
                conv = float(np.clip(np.random.normal(0.035, 0.01), 0.005, 0.10))
                o = int(round(s * conv))
                aov = float(np.random.uniform(500, 2500)) if vc == "B2B" else float(np.random.uniform(25, 90))
                g = round(o * aov, 2)
                pv = int(round(s * 0.80))
                atc = int(round(pv * 0.30))
                cos = max(int(round(atc * 0.50)), o)
                rows.append({
                    "date": d, "market": "US", "vertical_code": vc, "sub_vertical_code": None,
                    "device": "web", "sessions": s,
                    "sessions_definition_version": 1 if d < SESSION_CUTOVER else 2,
                    "product_view_sessions": pv, "add_to_cart_sessions": atc, "checkout_started_sessions": cos,
                    "orders": o, "units": int(round(o * 1.2)), "gmv_usd": g,
                })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# fact_promise_vs_actual -- full population. SIGNAL [otp-mix-shift] lives here
# (and in the fulfillment_speed_daily mart derived from it): blended on-time
# rises mostly via pickup-mix growth while ship-to-home itself is flat/down.
# --------------------------------------------------------------------------
PICKUP_SPLIT = {"bopis": 0.62, "curbside": 0.38}
MARKET_ORDER_SHARE = {"US": 0.82, "CA": 0.10, "MX": 0.08}
FULFILLMENT_NODE_POOL = ["fc_JOL1", "fc_FON2", "fc_1000", "fc_1001", "fc_1002", "fc_1003", "fc_1012", "fc_1015"]


def _channel_rate_series(dates: list[date], promised_total: float, on_time_rate_target: float) -> tuple[np.ndarray, np.ndarray]:
    weights = daily_weight_curve(dates, weekend_boost=1.05)
    promised_daily = allocate_int(int(round(promised_total)), weights)
    jitter = np.random.normal(1.0, 0.012, size=len(dates))
    rate_noisy = np.clip(on_time_rate_target * jitter, 0.0, 1.0)
    on_time_daily = allocate_int(int(round(promised_total * on_time_rate_target)), promised_daily * rate_noisy)
    on_time_daily = np.minimum(on_time_daily, promised_daily)
    return promised_daily, on_time_daily


def gen_fact_promise_vs_actual() -> pd.DataFrame:
    rows = []
    for qi, q in enumerate(QUARTERS):
        dates = quarter_dates(q)
        total_orders = TOTAL_ORDERS_M[qi] * 1_000_000
        sth_total = total_orders * SPEED["sth_mix_pct"][qi] / 100.0
        pickup_total = total_orders * SPEED["pickup_mix_pct"][qi] / 100.0
        dfs_total = total_orders * SPEED["dfs_mix_pct"][qi] / 100.0
        channel_targets = {
            "ship_to_home": (sth_total, SPEED["sth_otp"][qi] / 100.0),
            "bopis": (pickup_total * PICKUP_SPLIT["bopis"], SPEED["pickup_otp"][qi] / 100.0),
            "curbside": (pickup_total * PICKUP_SPLIT["curbside"], SPEED["pickup_otp"][qi] / 100.0),
            "dfs": (dfs_total, SPEED["dfs_otp"][qi] / 100.0),
        }
        for ftype, (total, rate) in channel_targets.items():
            promised_daily, on_time_daily = _channel_rate_series(dates, total, rate)
            for i, d in enumerate(dates):
                promised, on_time = int(promised_daily[i]), int(on_time_daily[i])
                if promised <= 0:
                    continue
                mkt_weights = np.array([MARKET_ORDER_SHARE[m] for m in MARKETS]) * np.random.normal(1.0, 0.05, 3)
                promised_by_mkt = allocate_int(promised, mkt_weights)
                on_time_by_mkt = np.minimum(allocate_int(on_time, promised_by_mkt), promised_by_mkt)
                for mi, market in enumerate(MARKETS):
                    p_m, ot_m = int(promised_by_mkt[mi]), int(on_time_by_mkt[mi])
                    if p_m <= 0:
                        continue
                    if ftype in ("ship_to_home", "dfs"):
                        node_w = np.random.dirichlet(np.ones(len(FULFILLMENT_NODE_POOL)))
                        p_by_node = allocate_int(p_m, node_w)
                        ot_by_node = np.minimum(allocate_int(ot_m, np.maximum(p_by_node, 1)), p_by_node)
                        for ni, node_id in enumerate(FULFILLMENT_NODE_POOL):
                            pn, otn = int(p_by_node[ni]), int(ot_by_node[ni])
                            if pn <= 0:
                                continue
                            late = pn - otn
                            avg_late = None
                            if late > 0:
                                base_late = 2.2 if ftype == "ship_to_home" else 1.5
                                if node_id == "fc_JOL1" and date(2025, 12, 8) <= d <= date(2025, 12, 10):
                                    base_late *= 1.8  # winter-storm disruption, JOL1, Dec 2025
                                avg_late = round(float(np.clip(np.random.normal(base_late, 0.4), 0.2, None)), 2)
                            rows.append({
                                "date": d, "market": market, "vertical_code": "SPEED", "fulfillment_type": ftype,
                                "orders_promised": pn, "orders_on_time": otn,
                                "avg_days_late_when_late": avg_late, "node_id": node_id,
                            })
                    else:
                        late = p_m - ot_m
                        avg_late = round(float(np.clip(np.random.normal(1.0, 0.3), 0.2, None)), 2) if late > 0 else None
                        rows.append({
                            "date": d, "market": market, "vertical_code": "SPEED", "fulfillment_type": ftype,
                            "orders_promised": p_m, "orders_on_time": ot_m,
                            "avg_days_late_when_late": avg_late, "node_id": None,
                        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# dim_experiment fact tables. SIGNAL [assigned-vs-exposed] lives in exposures
# (exp_2214 specifically); SIGNAL [checkout-confound] and [wider-window-confound]
# live in the readouts (two checkpoint rows per confounded experiment).
# --------------------------------------------------------------------------
EXPERIMENT_READOUTS_NAMED = {
    "exp_2401": [
        {"as_of_date": date(2025, 11, 15), "metric_name": "conversion_rate", "lift_pct": 6.8,
         "is_significant": True, "notes": "Clean result -- no concurrent launch/campaign in Collectibles during the window."},
    ],
    "exp_1187": [
        {"as_of_date": date(2026, 1, 26), "metric_name": "on_time_rate", "lift_pct": 1.5,
         "is_significant": True, "notes": "Deconfounded/isolated estimate, pre-automation-ramp volume only (SIGNAL [wider-window-confound])."},
        {"as_of_date": date(2026, 2, 20), "metric_name": "on_time_rate", "lift_pct": 4.2,
         "is_significant": True, "notes": "Full-window readout -- CONFOUNDED by concurrent DC sortation automation at FON2+JOL1 (2026-01-12 to 2026-02-15)."},
        {"as_of_date": date(2026, 2, 20), "metric_name": "conversion_rate", "lift_pct": -0.6,
         "is_significant": True, "notes": "Conversion cost from the less-attractive wider promise message. Net negative once deconfounded; killed 2026-03-02."},
    ],
    "exp_2214": [
        {"as_of_date": date(2026, 2, 28), "metric_name": "conversion_rate", "lift_pct": 0.8,
         "is_significant": True, "notes": "Pre-confound sub-window (Feb16-28), clean read, exposed-basis (per-protocol)."},
        {"as_of_date": date(2026, 3, 30), "metric_name": "conversion_rate", "lift_pct": 2.1,
         "is_significant": True, "notes": "Full-window readout, exposed-basis -- CONFOUNDED by Nav Refresh (exp_2215) launching into both arms 2026-03-01. Shipped 100% 2026-04-06 on this number."},
    ],
    "exp_2215": [
        {"as_of_date": date(2026, 3, 21), "metric_name": "conversion_rate", "lift_pct": 1.3,
         "is_significant": True, "notes": "Independent sitewide lift from Nav Refresh, measured via 5%-of-traffic 3-week no-launch holdback."},
    ],
    "exp_2489": [
        {"as_of_date": date(2026, 5, 15), "metric_name": "deflection_rate", "lift_pct": 3.0,
         "is_significant": True, "notes": "+3pp deflection (percentage points, not relative %)."},
        {"as_of_date": date(2026, 5, 15), "metric_name": "csat", "lift_pct": -0.15,
         "is_significant": True, "notes": "-0.15 CSAT (absolute, 1-5 scale) among late-escalated users."},
    ],
    "exp_2556": [
        {"as_of_date": date(2026, 6, 15), "metric_name": "benefit_awareness_pct", "lift_pct": 9.0,
         "is_significant": True, "notes": "+9pp 30-day benefit awareness (percentage points). Renewal-rate readout not yet valid -- needs ~12mo/cohort, revisit ~Q2FY28."},
    ],
    "exp_2601": [
        {"as_of_date": date(2026, 7, 20), "metric_name": "conversion_rate", "lift_pct": 1.6,
         "is_significant": True, "notes": "Interim readout, still running (started 2026-06-08). SIGNAL [offsetting-experiments]: equal-weighted with exp_2618's -1.5% nets to a ~+0.05% topline wash."},
    ],
    "exp_2618": [
        {"as_of_date": date(2026, 7, 20), "metric_name": "conversion_rate", "lift_pct": -1.5,
         "is_significant": True, "notes": "Interim readout, still running (started 2026-06-08). Well-meaning autoplay feature backfired -- see SIGNAL [offsetting-experiments]."},
    ],
}
# SIGNAL [assigned-vs-exposed]: ~16% of Checkout Simplify's assigned sessions were never exposed.
EXPOSURE_RATE_OVERRIDE = {"exp_2214": 0.84}


def gen_fact_experiment_exposures(dim_experiment: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for exp in dim_experiment.itertuples(index=False):
        end = min(exp.end_date if exp.end_date is not None else TODAY, TODAY)
        start = exp.start_date
        if start > end:
            continue
        dates = [start + timedelta(days=i) for i in range((end - start).days + 1)]
        base_daily = random.randint(400, 15000)
        exposure_rate = EXPOSURE_RATE_OVERRIDE.get(exp.experiment_id, random.uniform(0.88, 0.96))
        control_base_rate = random.uniform(0.02, 0.06)
        named = EXPERIMENT_READOUTS_NAMED.get(exp.experiment_id)
        named_conv = [r for r in (named or []) if r["metric_name"] in ("conversion_rate", "on_time_rate", "deflection_rate")]

        exp_rows: list[dict] = []
        for d in dates:
            # Exposure rate reflects a client-side/technical phenomenon (cart abandonment before
            # the experiment surface renders) that happens BEFORE a unit could see either arm, so
            # it should not itself differ by variant -- draw the day's noise once and share it, or
            # independent per-arm noise can accumulate into a spurious asymmetry that swamps a small
            # true effect and can even flip the sign of the assigned-vs-exposed comparison.
            day_exposure_noise = np.random.normal(1.0, 0.02)
            for variant, is_treatment in (("control", False), ("treatment", True)):
                noise = np.random.normal(1.0, 0.06)
                assigned = max(1, int(round(base_daily / 2 * noise)))
                exposed = int(round(assigned * np.clip(exposure_rate * day_exposure_noise, 0.5, 1.0)))
                exposed = min(exposed, assigned)
                exp_rows.append({
                    "experiment_id": exp.experiment_id, "variant": variant, "exposure_date": d,
                    "units_assigned": assigned, "units_exposed": exposed, "is_treatment": is_treatment,
                })

        if exp.experiment_id == "exp_2214":
            # This experiment's readouts (+0.8% pre-confound, +2.1% full-window) are exact, named
            # numbers referenced directly in the demo's question set -- distribute the EXACT target
            # conversion counts across days (weighted, noisy shape) rather than letting independent
            # per-row rate noise (needed for realism elsewhere) risk swamping a true effect this
            # small when aggregated. See _order_context-style allocate_int usage elsewhere for the
            # same "exact aggregate, noisy distribution" pattern.
            for pre in (True, False):
                period_rows = [r for r in exp_rows if (r["exposure_date"] <= date(2026, 2, 28)) == pre]
                for variant, base_rate in (("control", 0.0310 if pre else 0.0314),
                                            ("treatment", (0.0310 * 1.008) if pre else (0.0314 * 1.02612))):
                    sub = [r for r in period_rows if r["variant"] == variant]
                    exposed_arr = np.array([r["units_exposed"] for r in sub], dtype=float)
                    target_total = int(round(exposed_arr.sum() * base_rate))
                    noise = np.random.normal(1.0, 0.04, size=len(sub))
                    converted_arr = allocate_int(target_total, np.maximum(exposed_arr * noise, 0.01))
                    for r, c in zip(sub, converted_arr):
                        r["units_converted"] = int(c)
        else:
            for r in exp_rows:
                rate = control_base_rate
                if r["is_treatment"] and named_conv:
                    rate = control_base_rate * (1 + named_conv[-1]["lift_pct"] / 100.0)
                elif r["is_treatment"]:
                    rate = control_base_rate * (1 + random.uniform(-0.03, 0.08))
                rate = max(rate, 0.001) * float(np.random.normal(1.0, 0.05))
                r["units_converted"] = int(round(r["units_exposed"] * np.clip(rate, 0.0005, 0.5)))

        for r in exp_rows:
            r.pop("is_treatment", None)
        rows.extend(exp_rows)
    return pd.DataFrame(rows)


def gen_fact_experiment_readouts(dim_experiment: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for exp in dim_experiment.itertuples(index=False):
        named = EXPERIMENT_READOUTS_NAMED.get(exp.experiment_id)
        if named:
            for r in named:
                sample_size = random.randint(20_000, 400_000)
                rows.append({"experiment_id": exp.experiment_id, "variant": "treatment", "as_of_date": r["as_of_date"],
                             "metric_name": r["metric_name"], "metric_value": round(random.uniform(1, 10), 4),
                             "sample_size_units": sample_size, "lift_vs_control_pct": r["lift_pct"],
                             "is_significant": r["is_significant"], "notes": r["notes"]})
                rows.append({"experiment_id": exp.experiment_id, "variant": "control", "as_of_date": r["as_of_date"],
                             "metric_name": r["metric_name"], "metric_value": round(random.uniform(1, 10), 4),
                             "sample_size_units": sample_size, "lift_vs_control_pct": None,
                             "is_significant": False, "notes": "Control arm."})
        else:
            as_of = min(exp.end_date if exp.end_date is not None else TODAY, TODAY)
            sample_size = random.randint(5_000, 150_000)
            lift = round(random.uniform(-4.0, 9.0), 2)
            sig = bool(abs(lift) > 1.5 and random.random() < 0.6)
            rows.append({"experiment_id": exp.experiment_id, "variant": "treatment", "as_of_date": as_of,
                         "metric_name": exp.primary_metric, "metric_value": round(random.uniform(1, 100), 4),
                         "sample_size_units": sample_size, "lift_vs_control_pct": lift,
                         "is_significant": sig, "notes": "Routine readout."})
            rows.append({"experiment_id": exp.experiment_id, "variant": "control", "as_of_date": as_of,
                         "metric_name": exp.primary_metric, "metric_value": round(random.uniform(1, 100), 4),
                         "sample_size_units": sample_size, "lift_vs_control_pct": None,
                         "is_significant": False, "notes": "Control arm."})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# fact_orders -- representative sample (~400,000 rows), NOT the source for
# company GMV/order totals (convention 5). Two pools: member-linked orders
# (built per non-dormant panel member so member_cltv's trailing-12mo join has
# real rows to aggregate) and a general/guest pool that rounds out realistic
# market/vertical/channel shape. Also carries the return/refund columns that
# drive the refund-cycle-days signal ([voc-leads-quant] / [por-care-shared]).
# --------------------------------------------------------------------------
FULFILLMENT_TYPE_POOL_1P = ["ship_to_home", "bopis", "curbside", "dfs"]
RETURN_REASON_CODES = ["wrong_size", "not_as_described", "changed_mind", "damaged_in_transit",
                        "quality_issue", "arrived_late", "duplicate_order"]


def _pick_fulfillment_type(qi: int) -> str:
    weights = [SPEED["sth_mix_pct"][qi], SPEED["pickup_mix_pct"][qi] * PICKUP_SPLIT["bopis"],
               SPEED["pickup_mix_pct"][qi] * PICKUP_SPLIT["curbside"], SPEED["dfs_mix_pct"][qi]]
    return random.choices(FULFILLMENT_TYPE_POOL_1P, weights=weights)[0]


def _refund_cycle_days(return_date_: date) -> float:
    """Baseline ~3.3 days; elevated Dec2025-Feb2026 (Ontario returns-center
    understaffing), peaking around the turn of the year, recovered by
    mid-March 2026. SIGNAL [voc-leads-quant] / [por-care-shared]."""
    baseline = 3.3
    if date(2025, 12, 1) <= return_date_ <= date(2026, 3, 5):
        peak = date(2026, 1, 3)
        if return_date_ <= peak:
            frac = (return_date_ - date(2025, 12, 1)).days / max((peak - date(2025, 12, 1)).days, 1)
        else:
            frac = 1 - (return_date_ - peak).days / max((date(2026, 3, 5) - peak).days, 1)
        baseline += 3.2 * max(frac, 0)
    return round(max(baseline + random.gauss(0, 0.5), 0.5), 2)


def _order_context(channel: str, market: str, qi: int, pick_seller_fn):
    if channel == "3P":
        cat = random.choices(["collectibles", "resold", "style", "other"], weights=[0.20, 0.28, 0.40, 0.12])[0]
        seller_id = pick_seller_fn(cat)
        sub_vc = {"collectibles": "COLLECTIBLES", "resold": "RESOLD", "style": "STYLE"}.get(cat)
        aov = MARKETPLACE_AOV[sub_vc][qi] if sub_vc in MARKETPLACE_AOV else 55.0
        gmv = round(float(np.random.lognormal(np.log(max(aov, 5)), 0.5)), 2)
        return seller_id, sub_vc, "MARKETPLACE", "ship_to_home", gmv
    if random.random() < 0.03:
        # small B2B presence -- light vertical, "no 3P sellers" (canon), so B2B only ever
        # shows up as a 1P order. Without this, fact_orders never emits vertical_code='B2B'
        # at all, which would make SIGNAL [listing-accuracy-blind-spot]'s B2B cut (22% of
        # B2B post-purchase verbatims) unreachable via the order_id join fact_voc_responses
        # relies on (it has no sub_vertical_code column of its own).
        gmv = round(float(np.random.uniform(500, 2500)), 2)
        return None, None, "B2B", "ship_to_home", gmv
    aov = US_CONV[market]["gmv_m"][qi] * 1_000_000 / max(US_CONV[market]["orders_m"][qi] * 1_000_000, 1)
    gmv = round(float(np.random.lognormal(np.log(max(aov, 5)), 0.4)), 2)
    return None, None, "US_CONV", _pick_fulfillment_type(qi), gmv


# Collectibles return-rate arc (SIGNAL, "return rate spiked to 11.2% at the peak of the
# counterfeit problem... before Acme Verified brought it down to 5.4%"): 9.8% baseline ->
# 11.2% Q3FY26 counterfeit spike -> recovering through Acme Verified (launched 2025-09-08,
# 100%-rollout 2025-11-20) -> 5.4% by Q2FY27.
RETURN_RATE_COLLECTIBLES_BY_Q = [0.098, 0.103, 0.112, 0.090, 0.068, 0.054]


def _maybe_return(order_date_: date, gmv: float, p_return: float = 0.08):
    if random.random() >= p_return:
        return False, None, None, None, None
    return_date_ = order_date_ + timedelta(days=random.randint(2, 25))
    if return_date_ > TODAY:
        return False, None, None, None, None
    reason = random.choice(RETURN_REASON_CODES)
    refund_amt = round(gmv * random.uniform(0.85, 1.0), 2)
    refund_issued = return_date_ + timedelta(days=round(_refund_cycle_days(return_date_)))
    return True, return_date_, reason, refund_amt, refund_issued


def gen_fact_orders(dim_member: pd.DataFrame, dim_seller: pd.DataFrame, n_target: int = 400_000) -> pd.DataFrame:
    active_sellers = dim_seller[dim_seller["status"] == "active"].copy()
    tier_weight = {"top": 400.0, "large": 60.0, "mid": 10.0, "small": 2.0}
    active_sellers["_w"] = active_sellers["_gmv_tier"].map(tier_weight)

    # Pre-draw large pools of seller picks per category (vectorized) instead of calling
    # DataFrame.sample() per order -- ~150K individual weighted-sample calls would be very slow.
    seller_pools: dict[str, np.ndarray] = {}
    for cat in ["collectibles", "resold", "style", "other"]:
        pool = active_sellers[active_sellers["category_focus"] == cat]
        if len(pool) == 0:
            pool = active_sellers
        p = pool["_w"].to_numpy(dtype=float)
        p = p / p.sum()
        seller_pools[cat] = np.random.choice(pool["seller_id"].to_numpy(), size=160_000, p=p)
    seller_pool_pos = {cat: 0 for cat in seller_pools}

    def pick_seller(cat: str) -> str:
        pos = seller_pool_pos[cat]
        pool = seller_pools[cat]
        if pos >= len(pool):
            pos = 0
        seller_pool_pos[cat] = pos + 1
        return pool[pos]

    rows = []
    seq = 0

    def emit(order_date_, member_id, market, qi, channel):
        nonlocal seq
        seq += 1
        seller_id, sub_vc, vertical_code, fulfillment_type, gmv = _order_context(channel, market, qi, pick_seller)
        units = max(1, int(round(np.random.lognormal(np.log(1.4), 0.4))))
        p_return = RETURN_RATE_COLLECTIBLES_BY_Q[qi] if sub_vc == "COLLECTIBLES" else 0.08
        is_returned, return_date_, reason, refund_amt, refund_issued = _maybe_return(order_date_, gmv, p_return)
        rows.append({
            "order_id": rid("ord", seq, width=8), "order_date": order_date_, "member_id": member_id,
            "market": market, "vertical_code": vertical_code, "sub_vertical_code": sub_vc,
            "channel": channel, "seller_id": seller_id, "fulfillment_type": fulfillment_type,
            "gmv_usd": gmv, "units": units,
            "device": random.choices(["web", "app", "store_kiosk"], weights=[0.55, 0.42, 0.03])[0],
            "is_returned": is_returned, "return_date": return_date_, "return_reason_code": reason,
            "refund_usd": refund_amt, "refund_issued_date": refund_issued,
        })

    # ---- Member-linked orders: only non-dormant members get any rows here ----
    non_dormant = dim_member[~dim_member["dormant_flag"]]
    for m in non_dormant.itertuples(index=False):
        lifetime_n = 1 + int(np.random.poisson(2.0))
        if m.member_id == "mem_1000042":       # Dana -- power benefit-user
            lifetime_n = 22
        elif m.member_id == "mem_1000640":     # Oskar -- renews reliably, moderate shopper
            lifetime_n = max(lifetime_n, 6)
        cancel = m.cancel_date
        window_end = min(cancel, TODAY) if cancel else TODAY
        window_start = max(m.signup_date, QUARTERS[0].start)

        order_dates = []
        # Guaranteed trailing-12mo order -- independent of cancel_date/window_end, so the
        # dormant/non-dormant split stays exactly the 24,000/96,000 panel designation
        # (SIGNAL [cltv-join-drop]) rather than being diluted by members who happen to have
        # cancelled their membership more than a year before "today" (a different, unrelated
        # reason to have zero trailing orders).
        trailing_lo = max(m.signup_date, TODAY - timedelta(days=365))
        if trailing_lo <= TODAY:
            order_dates.append(trailing_lo + timedelta(days=random.randint(0, (TODAY - trailing_lo).days)))

        if window_start < window_end:
            span = (window_end - window_start).days
            order_dates += [window_start + timedelta(days=random.randint(0, span)) for _ in range(max(lifetime_n - 1, 0))]

        for od in order_dates:
            qi = quarter_index_for_date(od)
            if qi is None:
                qi = 5 if od > QUARTERS[-1].end else 0
            channel = "3P" if random.random() < 0.22 else "1P"
            emit(od, m.member_id, m.home_market, qi, channel)

    # ---- General/guest pool: rounds out realistic market/vertical shape, no member link ----
    n_general = max(0, n_target - len(rows))
    q_weights = np.array(TOTAL_ORDERS_M) / sum(TOTAL_ORDERS_M)
    q_counts = allocate_int(n_general, q_weights)
    for qi, n_q in enumerate(q_counts):
        q = QUARTERS[qi]
        span = max((q.data_end - q.start).days, 0)
        for _ in range(int(n_q)):
            od = q.start + timedelta(days=random.randint(0, span))
            market = random.choices(MARKETS, weights=[0.82, 0.10, 0.08])[0]
            channel = "3P" if random.random() < 0.35 else "1P"
            emit(od, None, market, qi, channel)

    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# fact_care_contacts -- representative sample (~50,000 rows). Rates (deflection
# %, CSAT, handle time) are calibrated per-quarter, per-sub-program so the
# volume-weighted blend reconciles to CANON's company-wide quarterly figures.
# SIGNAL [care-deflection-quality-confound] falls out naturally since
# CSAT-deflected is drawn to the exact stated quarterly mean, which itself
# dips Q4FY26->Q1FY27 while deflection keeps climbing.
# --------------------------------------------------------------------------
CARE_RESOLUTION_CODES = ["resolved", "escalated", "refund_issued", "information_provided",
                          "pending_callback", "no_action_needed"]


def gen_fact_care_contacts(dim_member: pd.DataFrame, dim_associate: pd.DataFrame,
                            fact_orders: pd.DataFrame, n_total: int = 50_000) -> pd.DataFrame:
    care_assoc_ids = dim_associate[(dim_associate["team"] == "Care") & dim_associate["is_active"]]["assoc_id"].tolist()
    member_ids = dim_member["member_id"].tolist()
    member_market = dict(zip(dim_member["member_id"], dim_member["home_market"]))
    order_ids_by_q: dict[int, list[str]] = {i: [] for i in range(6)}
    for o in fact_orders.itertuples(index=False):
        qi = quarter_index_for_date(o.order_date)
        if qi is not None:
            order_ids_by_q[qi].append(o.order_id)

    sub_names = list(SUB_PROGRAM_VOLUME_WEIGHT.keys())
    sub_w = [SUB_PROGRAM_VOLUME_WEIGHT[s] for s in sub_names]
    weighted_avg_mult = sum(SUB_PROGRAM_VOLUME_WEIGHT[s] * SUB_PROGRAM_DEFLECTION_MULT[s] for s in sub_names)

    q_counts = allocate_int(n_total, np.array(CARE["contacts_k"], dtype=float))
    rows = []
    seq = 0
    for qi, n_q in enumerate(q_counts):
        n_q = int(n_q)
        q = QUARTERS[qi]
        span = max((q.data_end - q.start).days, 0)
        base_deflection = CARE["deflection_pct"][qi] / weighted_avg_mult / 100.0
        handle_time_target = CARE["handle_time_min"][qi]

        sub_programs = random.choices(sub_names, weights=sub_w, k=n_q)
        deflect_roll = np.random.random(n_q)
        deflected_flags = [deflect_roll[i] < min(0.99, base_deflection * SUB_PROGRAM_DEFLECTION_MULT[sub_programs[i]])
                            for i in range(n_q)]
        agent_closed_flags = [None if deflected_flags[i] else (random.random() < 0.94) for i in range(n_q)]
        n_deflected = sum(1 for f in deflected_flags if f)
        n_agent_closed = sum(1 for f in agent_closed_flags if f)

        csat_defl_iter = iter(draws_with_exact_mean(max(n_deflected, 1), CARE["csat_deflected"][qi], 1, 5, 0.9))
        csat_agent_iter = iter(draws_with_exact_mean(max(n_agent_closed, 1), CARE["csat_agent"][qi], 1, 5, 0.7))
        handle_time_iter = iter(rescale_to_mean(
            np.random.gamma(4.0, handle_time_target / 4.0, max(n_agent_closed, 1)), handle_time_target))

        for i in range(n_q):
            seq += 1
            d = q.start + timedelta(days=random.randint(0, span))
            sub_program = sub_programs[i]
            deflected = deflected_flags[i]
            channel = random.choices(["chat", "phone", "bot", "email"], weights=[0.30, 0.25, 0.30, 0.15])[0]
            if deflected and channel not in ("bot", "chat"):
                channel = "bot"
            member_id = random.choice(member_ids) if random.random() < 0.55 else None
            market = member_market.get(member_id, random.choice(MARKETS)) if member_id else \
                random.choices(MARKETS, weights=[0.82, 0.10, 0.08])[0]
            order_id = None
            if sub_program in ("avoid", "optimize") and order_ids_by_q[qi] and random.random() < 0.4:
                order_id = random.choice(order_ids_by_q[qi])
            opened = datetime.combine(d, datetime.min.time()) + timedelta(seconds=random.randint(0, 86399))

            if deflected:
                closed = opened + timedelta(minutes=random.uniform(0.5, 6))
                deflection_type = random.choice(["bot", "self_service_kb", "in_app_faq"])
                csat = int(next(csat_defl_iter))
                handle_time = None
                assoc_id = None
            elif agent_closed_flags[i]:
                ht = float(next(handle_time_iter))
                closed = opened + timedelta(minutes=ht)
                deflection_type = None
                csat = int(next(csat_agent_iter))
                handle_time = round(ht, 2)
                assoc_id = random.choice(care_assoc_ids) if care_assoc_ids else None
            else:
                closed, deflection_type, csat, handle_time = None, None, None, None
                assoc_id = random.choice(care_assoc_ids) if care_assoc_ids else None

            rows.append({
                "contact_id": rid("case", seq, width=7), "member_id": member_id, "order_id": order_id,
                "market": market, "sub_program": sub_program, "channel": channel,
                "opened_at": opened, "closed_at": closed, "deflected": deflected,
                "deflection_type": deflection_type, "resolution_code": random.choice(CARE_RESOLUTION_CODES),
                "csat_score": csat, "handle_time_minutes": handle_time, "assoc_id": assoc_id,
            })

    # named archetype: Jamal (mem_1000390) -- 2 open (unresolved) P1 care contacts
    jamal_idx = [i for i, r in enumerate(rows) if r["member_id"] == "mem_1000390"]
    for i in jamal_idx[:2]:
        rows[i].update(closed_at=None, deflected=False, deflection_type=None,
                        resolution_code="escalated", csat_score=None, handle_time_minutes=None)
    for _ in range(max(0, 2 - len(jamal_idx))):
        seq += 1
        d = QUARTERS[-1].start + timedelta(days=random.randint(0, max((TODAY - QUARTERS[-1].start).days, 0)))
        rows.append({
            "contact_id": rid("case", seq, width=7), "member_id": "mem_1000390", "order_id": None,
            "market": "US", "sub_program": "member_care", "channel": "phone",
            "opened_at": datetime.combine(d, datetime.min.time()) + timedelta(hours=10),
            "closed_at": None, "deflected": False, "deflection_type": None, "resolution_code": "escalated",
            "csat_score": None, "handle_time_minutes": None,
            "assoc_id": random.choice(care_assoc_ids) if care_assoc_ids else None,
        })

    df = pd.DataFrame(rows)
    df["csat_score"] = df["csat_score"].astype("Int64")
    return df


# --------------------------------------------------------------------------
# fact_marketplace_listings -- representative sample (~35,000 rows) tied to the
# ~2,500-seller panel. authenticity_verified ramps with the Acme Verified
# program (launch 2025-09-08 -> 100% Collectibles rollout 2025-11-20), which
# is what makes the Collectibles return-rate signal (9.8%->11.2%->5.4%)
# plausible at the listing level.
# --------------------------------------------------------------------------
def gen_fact_marketplace_listings(dim_seller: pd.DataFrame, n_total: int = 31_000,
                                    exclude_seller_ids: set[str] | None = None) -> pd.DataFrame:
    tier_weight = {"top": 25.0, "large": 12.0, "mid": 4.0, "small": 1.0}
    ds = dim_seller.copy()
    if exclude_seller_ids:
        # the new-seller cohort gets its OWN precisely-authored listings (exact
        # funnel-stage counts, gen_new_seller_cohort) -- excluded here so the
        # general/uncontrolled sampler below doesn't dilute those exact counts.
        ds = ds[~ds["seller_id"].isin(exclude_seller_ids)]
    ds["_w"] = ds["_gmv_tier"].map(tier_weight)
    sellers = ds.sample(n=n_total, replace=True, weights=ds["_w"], random_state=SEED).reset_index(drop=True)

    rows = []
    for i, s in enumerate(sellers.itertuples(index=False)):
        span = max((TODAY - s.onboarded_date).days, 1)
        listed = s.onboarded_date + timedelta(days=random.randint(0, span))
        cat = s.category_focus
        if cat == "collectibles":
            price = float(np.random.lognormal(np.log(70), 0.9))
            verified_p = 0.05 if listed < date(2025, 9, 8) else (0.45 if listed < date(2025, 11, 20) else 0.90)
        elif cat == "resold":
            price, verified_p = float(np.random.lognormal(np.log(35), 0.6)), 0.20
        elif cat == "style":
            price, verified_p = float(np.random.lognormal(np.log(55), 0.6)), 0.15
        else:
            price, verified_p = float(np.random.lognormal(np.log(40), 0.7)), 0.10

        status_w = [0.90, 0.07, 0.03]
        if s.seller_id == "sel_500089":  # Bramblewood Vintage -- counterfeit violations
            status_w = [0.55, 0.20, 0.25]
            verified_p *= 0.3
        status = random.choices(["active", "removed", "suspended"], weights=status_w)[0]
        rows.append({
            "listing_id": rid("lst", i + 1, width=7), "seller_id": s.seller_id, "category": cat,
            "listed_date": listed, "price_usd": round(price, 2), "status": status,
            "authenticity_verified": random.random() < verified_p,
        })
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# fact_voc_responses -- representative sample (~40,000 rows). SIGNAL
# [voc-leads-quant]: the "refund delay" theme_tag share is a scripted weekly
# curve crossing 10% the week of 2025-12-15 (11.2%), peaking 16.1% week of
# 2026-01-05, off a ~3.5% baseline -- weeks ahead of the quantitative metric.
# --------------------------------------------------------------------------
THEME_TAGS_OTHER = ["shipping_speed", "product_quality", "pricing", "customer_service",
                    "checkout_experience", "app_bugs", "return_process", "membership_value", None]
THEME_WEIGHTS_OTHER = [0.12, 0.10, 0.08, 0.10, 0.08, 0.06, 0.08, 0.08, 0.30]

# SIGNAL [listing-accuracy-blind-spot]: a steady-state (not rising) theme share of each
# vertical's post-purchase verbatims -- keyed off the LINKED ORDER's sub_vertical_code
# (Marketplace) or vertical_code (B2B), since fact_voc_responses itself carries no
# sub_vertical_code column (CROSS-VERTICAL BACKLOG SNAPSHOT in CANON.md).
LISTING_ACCURACY_GAP_RATE = {"STYLE": 0.14, "RESOLD": 0.12, "COLLECTIBLES": 0.09}
LISTING_ACCURACY_GAP_RATE_B2B = 0.22


def _refund_delay_theme_share(d: date) -> float:
    baseline = 0.035
    checkpoints = [
        (date(2025, 11, 24), 0.045), (date(2025, 12, 8), 0.085), (date(2025, 12, 15), 0.112),
        (date(2025, 12, 22), 0.135), (date(2025, 12, 29), 0.150), (date(2026, 1, 5), 0.161),
        (date(2026, 1, 12), 0.145), (date(2026, 1, 19), 0.120), (date(2026, 1, 26), 0.095),
        (date(2026, 2, 2), 0.070), (date(2026, 2, 9), 0.055), (date(2026, 2, 16), 0.045),
        (date(2026, 2, 23), 0.037), (date(2026, 2, 28), 0.035),
    ]
    if d < checkpoints[0][0] or d > checkpoints[-1][0]:
        return baseline
    for (d0, v0), (d1, v1) in zip(checkpoints, checkpoints[1:]):
        if d0 <= d <= d1:
            frac = (d - d0).days / max((d1 - d0).days, 1)
            return v0 + (v1 - v0) * frac
    return baseline


def gen_fact_voc_responses(dim_member: pd.DataFrame, fact_orders: pd.DataFrame,
                             fact_care_contacts: pd.DataFrame, n_total: int = 40_000) -> pd.DataFrame:
    member_ids = dim_member["member_id"].tolist()
    member_market = dict(zip(dim_member["member_id"], dim_member["home_market"]))
    order_sample = fact_orders.sample(n=min(len(fact_orders), 20_000), random_state=SEED)
    care_sample = fact_care_contacts.sample(n=min(len(fact_care_contacts), 20_000), random_state=SEED)

    full_dates: list[date] = []
    for q in QUARTERS:
        full_dates += quarter_dates(q)
    date_weights = daily_weight_curve(full_dates).tolist()
    date_choices = random.choices(full_dates, weights=date_weights, k=n_total)

    rows = []
    for i, d in enumerate(date_choices):
        survey_type = random.choices(["post_purchase", "post_care_contact", "nps"], weights=[0.45, 0.35, 0.20])[0]
        order_id = member_id = vertical_code = None
        sub_vertical_code = None
        market = random.choice(MARKETS)
        if survey_type == "post_purchase" and len(order_sample):
            o = order_sample.iloc[random.randrange(len(order_sample))]
            order_id, member_id, vertical_code, market = o["order_id"], o["member_id"], o["vertical_code"], o["market"]
            sub_vertical_code = o["sub_vertical_code"]
        elif survey_type == "post_care_contact" and len(care_sample):
            c = care_sample.iloc[random.randrange(len(care_sample))]
            member_id, market = c["member_id"], c["market"]
        else:
            if random.random() < 0.7:
                member_id = random.choice(member_ids)
            market = member_market.get(member_id, random.choice(MARKETS)) if member_id else random.choice(MARKETS)

        score_type = {"nps": "nps_0_10", "post_care_contact": "csat_1_5", "post_purchase": "ces_1_7"}[survey_type]

        if survey_type == "post_purchase" and vertical_code == "MARKETPLACE":
            accuracy_gap_p = LISTING_ACCURACY_GAP_RATE.get(sub_vertical_code, 0.0)
        elif survey_type == "post_purchase" and vertical_code == "B2B":
            accuracy_gap_p = LISTING_ACCURACY_GAP_RATE_B2B
        else:
            accuracy_gap_p = 0.0
        refund_p = _refund_delay_theme_share(d)
        remaining = max(0.0, 1 - refund_p - accuracy_gap_p)
        w_other = np.array(THEME_WEIGHTS_OTHER) / sum(THEME_WEIGHTS_OTHER) * remaining
        tag_pool = ["refund_delay", "listing-accuracy-gap"] + THEME_TAGS_OTHER
        tag_w = [refund_p, accuracy_gap_p] + w_other.tolist()
        theme_tag = random.choices(tag_pool, weights=tag_w)[0]

        if theme_tag == "refund_delay":
            sentiment = "negative"
            verbatim = random.choice([
                "Still waiting on my refund -- it's been over a week since the item scanned as received.",
                "Return shows received but the refund hasn't posted yet, getting frustrating.",
                "Refund is taking way longer than the app originally estimated.",
            ])
        elif theme_tag == "listing-accuracy-gap":
            sentiment = random.choices(["negative", "neutral"], weights=[0.75, 0.25])[0]
            verbatim = random.choice([
                "Item arrived way smaller than the photos made it look -- listing didn't mention actual scale.",
                "Description said 'excellent condition' but there was a scratch not shown in any photo.",
                "The spec sheet didn't match what showed up -- wrong pallet configuration for this SKU.",
                "Photos don't represent the true condition/size of the item at all.",
            ])
        elif theme_tag is None:
            sentiment = random.choices(["positive", "neutral", "negative"], weights=[0.55, 0.30, 0.15])[0]
            verbatim = "General shopping experience feedback, nothing specific called out."
        else:
            sentiment = random.choices(["positive", "neutral", "negative"], weights=[0.40, 0.30, 0.30])[0]
            verbatim = f"Feedback related to {theme_tag.replace('_', ' ')}."

        if score_type == "nps_0_10":
            score = {"positive": random.choice([9, 10]), "neutral": random.choice([7, 8]),
                     "negative": random.choice([0, 2, 4, 5, 6])}[sentiment]
        elif score_type == "csat_1_5":
            score = {"positive": random.choice([4, 5]), "neutral": 3, "negative": random.choice([1, 2])}[sentiment]
        else:  # ces_1_7 (customer effort score, lower is better -- negative sentiment = high effort)
            score = {"positive": random.choice([1, 2]), "neutral": random.choice([3, 4]),
                     "negative": random.choice([5, 6, 7])}[sentiment]

        rows.append({
            "response_id": rid("voc", i + 1, width=7), "member_id": member_id, "order_id": order_id,
            "market": market, "vertical_code": vertical_code, "survey_type": survey_type,
            "responded_at": datetime.combine(d, datetime.min.time()) + timedelta(hours=random.randint(8, 21)),
            "score": float(score), "score_type": score_type, "verbatim_text": verbatim,
            "theme_tag": theme_tag, "sentiment": sentiment,
        })

    df = pd.DataFrame(rows)
    jamal_mask = df["member_id"] == "mem_1000390"
    if jamal_mask.any():
        idx = df[jamal_mask].index[0]
        df.loc[idx, "survey_type"] = "nps"
        df.loc[idx, "score_type"] = "nps_0_10"
        df.loc[idx, "score"] = 3.0
        df.loc[idx, "sentiment"] = "negative"
        df.loc[idx, "theme_tag"] = "customer_service"
        df.loc[idx, "responded_at"] = datetime(2026, 3, 15, 14, 0)
    return df


# ==========================================================================
# Derived marts (5 original + 1 added mid-build: marketplace_gmv_summary --
# fact_orders is a sample and can't be the full-population GMV-by-sub-vertical
# source, so this mart plays the same authoritative role for Marketplace that
# traffic_conversion_summary plays for US_CONV.)
# ==========================================================================
def gen_mart_traffic_conversion_summary(ftd: pd.DataFrame) -> pd.DataFrame:
    df = ftd.copy()
    df["fiscal_week_ending"] = df["date"].apply(week_ending_date)
    g = df.groupby(["fiscal_week_ending", "market", "vertical_code"], as_index=False).agg(
        sessions=("sessions", "sum"), orders=("orders", "sum"), gmv_usd=("gmv_usd", "sum"),
        _sv_weighted=("sessions", "sum"),
    )
    # sessions_definition_version: session-volume-weighted mode (1 or 2) for the week
    def _week_version(sub: pd.DataFrame) -> int:
        w = (sub["sessions_definition_version"] * sub["sessions"]).sum()
        s = sub["sessions"].sum()
        return int(round(w / s)) if s > 0 else 1
    ver = df.groupby(["fiscal_week_ending", "market", "vertical_code"]).apply(_week_version).rename("sessions_definition_version").reset_index()
    g = g.drop(columns=["_sv_weighted"]).merge(ver, on=["fiscal_week_ending", "market", "vertical_code"], how="left")
    g["conversion_rate"] = np.where(g["sessions"] > 0, round(g["orders"] / g["sessions"] * 100, 4), 0.0)

    # orders_yoy_pct: match this week to the same (market, vertical) week 364 days earlier
    prior = g[["fiscal_week_ending", "market", "vertical_code", "orders"]].copy()
    prior["fiscal_week_ending"] = prior["fiscal_week_ending"] + timedelta(days=364)
    prior = prior.rename(columns={"orders": "orders_prior_year"})
    g = g.merge(prior, on=["fiscal_week_ending", "market", "vertical_code"], how="left")
    g["orders_yoy_pct"] = np.where(
        g["orders_prior_year"].notna() & (g["orders_prior_year"] > 0),
        round((g["orders"] - g["orders_prior_year"]) / g["orders_prior_year"] * 100, 3), np.nan,
    )
    return g[["fiscal_week_ending", "market", "vertical_code", "sessions", "sessions_definition_version",
              "orders", "conversion_rate", "gmv_usd", "orders_yoy_pct"]]


def gen_mart_marketplace_gmv_summary(ftd: pd.DataFrame) -> pd.DataFrame:
    mp = ftd[ftd["vertical_code"] == "MARKETPLACE"].copy()
    mp["fiscal_week_ending"] = mp["date"].apply(week_ending_date)
    g = mp.groupby(["fiscal_week_ending", "sub_vertical_code"], as_index=False).agg(
        gmv_usd=("gmv_usd", "sum"), orders=("orders", "sum"))
    total_span = max((QUARTERS[-1].data_end - QUARTERS[0].start).days, 1)

    def take_rate_for(d: date) -> float:
        frac = min(max((d - QUARTERS[0].start).days / total_span, 0), 1)
        return round(13.2 + (13.6 - 13.2) * frac, 3)

    g["take_rate"] = g["fiscal_week_ending"].apply(take_rate_for)
    return g[["fiscal_week_ending", "sub_vertical_code", "gmv_usd", "orders", "take_rate"]]


def gen_mart_fulfillment_speed_daily(fpva: pd.DataFrame) -> pd.DataFrame:
    g = fpva.groupby(["date", "market", "vertical_code", "fulfillment_type"], as_index=False).agg(
        orders_promised=("orders_promised", "sum"), orders_on_time=("orders_on_time", "sum"))
    day_totals = g.groupby(["date", "market"])["orders_promised"].transform("sum")
    g["pct_of_total_orders"] = np.where(day_totals > 0, round(g["orders_promised"] / day_totals, 4), 0.0)
    g["on_time_rate"] = np.where(g["orders_promised"] > 0, round(g["orders_on_time"] / g["orders_promised"], 4), 0.0)

    qi_of = g["date"].apply(quarter_index_for_date)
    cost = np.full(len(g), np.nan)
    for qi in range(6):
        mask = (qi_of == qi).values
        if not mask.any():
            continue
        mix = {"ship_to_home": SPEED["sth_mix_pct"][qi] / 100.0,
               "bopis": SPEED["pickup_mix_pct"][qi] / 100.0 * PICKUP_SPLIT["bopis"],
               "curbside": SPEED["pickup_mix_pct"][qi] / 100.0 * PICKUP_SPLIT["curbside"],
               "dfs": SPEED["dfs_mix_pct"][qi] / 100.0}
        weighted_ratio = sum(mix[ft] * COST_RATIO[ft] for ft in mix)
        base_cost = SPEED["cost_per_order"][qi] / weighted_ratio
        rows_ft = g.loc[mask, "fulfillment_type"].values
        noise = np.random.normal(1.0, 0.015, size=mask.sum())
        cost[mask] = [base_cost * COST_RATIO[ft] for ft in rows_ft] * noise
    g["avg_cost_per_order_usd"] = np.round(cost, 2)
    return g[["date", "market", "vertical_code", "fulfillment_type", "orders_promised", "on_time_rate",
              "pct_of_total_orders", "avg_cost_per_order_usd"]]


def gen_mart_care_deflection_daily() -> pd.DataFrame:
    rows = []
    weighted_avg_mult = sum(SUB_PROGRAM_VOLUME_WEIGHT[s] * SUB_PROGRAM_DEFLECTION_MULT[s] for s in SUB_PROGRAMS)
    for qi, q in enumerate(QUARTERS):
        dates = quarter_dates(q)
        weights = daily_weight_curve(dates, weekend_boost=1.03)
        total_contacts = CARE["contacts_k"][qi] * 1000
        base_deflection = CARE["deflection_pct"][qi] / weighted_avg_mult / 100.0
        for sp in SUB_PROGRAMS:
            sp_total = int(round(total_contacts * SUB_PROGRAM_VOLUME_WEIGHT[sp]))
            vol_daily = allocate_int(sp_total, weights)
            sp_rate = min(0.99, base_deflection * SUB_PROGRAM_DEFLECTION_MULT[sp])
            deflected_total = int(round(sp_total * sp_rate))
            defl_noise = np.random.normal(1.0, 0.05, size=len(dates))
            deflected_daily = np.minimum(allocate_int(deflected_total, np.maximum(vol_daily * defl_noise, 0)), vol_daily)
            for i, d in enumerate(dates):
                cv = int(vol_daily[i])
                if cv <= 0:
                    continue
                rows.append({
                    "date": d, "sub_program": sp, "contact_volume": cv,
                    "deflection_rate": round(float(deflected_daily[i] / cv), 4),
                    "avg_csat_deflected": round(float(np.clip(CARE["csat_deflected"][qi] * np.random.normal(1.0, 0.008), 1, 5)), 3),
                    "avg_csat_agent_assisted": round(float(np.clip(CARE["csat_agent"][qi] * np.random.normal(1.0, 0.008), 1, 5)), 3),
                    "avg_handle_time_minutes": round(float(np.clip(CARE["handle_time_min"][qi] * np.random.normal(1.0, 0.015), 1, None)), 2),
                })
    return pd.DataFrame(rows)


def gen_mart_member_cltv(dim_member: pd.DataFrame, fact_orders: pd.DataFrame) -> pd.DataFrame:
    member_orders = fact_orders[fact_orders["member_id"].notna()]
    trailing_start = TODAY - timedelta(days=365)
    trailing = member_orders[member_orders["order_date"] >= trailing_start]

    lifetime_agg = member_orders.groupby("member_id").agg(
        lifetime_orders=("order_id", "count"), lifetime_gmv_usd=("gmv_usd", "sum")).reset_index()
    trailing_agg = trailing.groupby("member_id").agg(
        trailing_12mo_orders=("order_id", "count"), trailing_12mo_gmv_usd=("gmv_usd", "sum")).reset_index()

    df = dim_member[["member_id", "signup_date", "status", "depth_flag"]].copy()
    # LEFT JOIN dim_member to fact_orders (canonical build) -- an INNER JOIN would silently drop the
    # dormant 20% of the panel. SIGNAL [cltv-join-drop].
    df = df.merge(lifetime_agg, on="member_id", how="left").merge(trailing_agg, on="member_id", how="left")
    df["lifetime_orders"] = df["lifetime_orders"].fillna(0).astype(int)
    df["lifetime_gmv_usd"] = df["lifetime_gmv_usd"].fillna(0.0).round(2)
    df["trailing_12mo_orders"] = df["trailing_12mo_orders"].fillna(0).astype(int)
    df["trailing_12mo_gmv_usd"] = df["trailing_12mo_gmv_usd"].fillna(0.0).round(2)  # COALESCE(...,0)
    df["tenure_days"] = df["signup_date"].apply(lambda d: (TODAY - d).days)
    df["signup_cohort_quarter"] = df["signup_date"].apply(fiscal_quarter_label)
    df["benefits_adopted_count"] = df["depth_flag"].astype(int) + 1  # +1 = baseline free_shipping every paying member has
    df["is_active"] = df["status"] != "cancelled"

    # projected_cltv_usd calibrated so avg(non-dormant) = $625/member (the wrong INNER-JOIN figure) and
    # avg(all 120,000, dormant COALESCE'd to 0) = $500/member (the correct LEFT-JOIN figure) --
    # SIGNAL [cltv-join-drop]: 625 x 0.80 = 500 exactly, matching the 96,000/120,000 non-dormant share.
    non_dormant_mask = (df["trailing_12mo_orders"] > 0).values
    n_non_dormant = int(non_dormant_mask.sum())
    raw = rescale_to_mean(np.random.lognormal(mean=np.log(500), sigma=0.6, size=n_non_dormant), 625.0)
    projected = np.zeros(len(df))
    projected[non_dormant_mask] = raw
    df["projected_cltv_usd"] = np.round(projected, 2)

    return df[["member_id", "signup_cohort_quarter", "tenure_days", "lifetime_orders", "lifetime_gmv_usd",
               "trailing_12mo_gmv_usd", "trailing_12mo_orders", "benefits_adopted_count", "is_active",
               "projected_cltv_usd"]]


def gen_mart_marketplace_seller_performance(dim_seller: pd.DataFrame, fact_marketplace_listings: pd.DataFrame,
                                              fact_orders: pd.DataFrame) -> pd.DataFrame:
    listings = fact_marketplace_listings
    active_listings = listings[listings["status"] == "active"].groupby("seller_id").size().rename("active_listings")

    orders_3p = fact_orders[fact_orders["channel"] == "3P"]
    trailing_orders = orders_3p[orders_3p["order_date"] >= TODAY - timedelta(days=90)]
    trailing_gmv = trailing_orders.groupby("seller_id")["gmv_usd"].sum().rename("trailing_90d_gmv_usd")
    order_counts = orders_3p.groupby("seller_id").size().rename("n_orders")
    return_counts = orders_3p[orders_3p["is_returned"]].groupby("seller_id").size().rename("n_returns")

    df = dim_seller[["seller_id", "category_focus"]].copy()
    for s in (active_listings, trailing_gmv, order_counts, return_counts):
        df = df.merge(s, on="seller_id", how="left")
    df["active_listings"] = df["active_listings"].fillna(0).astype(int)
    df["trailing_90d_gmv_usd"] = df["trailing_90d_gmv_usd"].fillna(0.0).round(2)
    df["n_orders"] = df["n_orders"].fillna(0)
    df["n_returns"] = df["n_returns"].fillna(0)
    df["return_rate"] = np.where(df["n_orders"] > 0, round(df["n_returns"] / df["n_orders"], 4), 0.0)
    df["avg_days_to_ship"] = np.round(np.random.uniform(1.0, 4.5, size=len(df)), 2)
    df["authenticity_flag_count"] = np.random.poisson(np.where(df["category_focus"] == "collectibles", 1.2, 0.2))
    df["avg_buyer_rating"] = np.round(np.clip(np.random.normal(4.5, 0.35, size=len(df)), 2.0, 5.0), 2)
    return df[["seller_id", "category_focus", "active_listings", "trailing_90d_gmv_usd", "return_rate",
               "avg_days_to_ship", "authenticity_flag_count", "avg_buyer_rating"]]


NEW_SELLER_COHORT_ID_MAX = 500740  # generic cohort IDs are sel_500244..sel_500740 (497 = 200+150+150-3 pinned)


def _is_new_seller_cohort_id(seller_id: str) -> bool:
    if seller_id in NEW_SELLER_PINNED_IDS:
        return True
    try:
        num = int(seller_id.split("_")[1])
    except (IndexError, ValueError):
        return False
    return 500244 <= num <= NEW_SELLER_COHORT_ID_MAX


# --------------------------------------------------------------------------
# fact_seller_voc_responses -- NEW TABLE (24th). Representative panel, ~4,000
# rows. Seller-side VOC ("Seller Pulse", launched 2026-04-20) -- a fully
# separate stream from buyer-side fact_voc_responses/Medallia: own survey
# types, own score types, own theme vocabulary. Quarterly NPS draws from the
# WHOLE active seller panel; the onboarding-pulse types (L1/L5/L10) are only
# meaningful for sellers actually moving through the onboarding funnel, so
# they're scoped to the new-seller cohort (SIGNAL [seller-auth-friction]).
# --------------------------------------------------------------------------
SELLER_PULSE_LAUNCH = date(2026, 4, 20)
AUTH_FRICTION_RATE = {"collectibles": 0.38, "style": 0.05, "resold": 0.06}
SELLER_VOC_THEMES_OTHER = ["pricing-confusion", "payout-timing", "support-responsiveness",
                           "category-fit", "shipping-labels", None]
SELLER_VOC_WEIGHTS_OTHER = [0.10, 0.08, 0.08, 0.06, 0.06, 0.42]


def _seller_voc_row(i: int, seller_id: str, cat: str, survey_type: str) -> dict:
    onboarding_pulse = survey_type in ("onboarding_pulse_l1", "onboarding_pulse_l5", "onboarding_pulse_l10")
    auth_p = setup_p = perf_p = 0.0
    if onboarding_pulse:
        if survey_type in ("onboarding_pulse_l1", "onboarding_pulse_l5"):
            auth_p = AUTH_FRICTION_RATE.get(cat, 0.0)
            setup_p = 0.18  # category-agnostic, hits hardest listing 1->5
        if survey_type in ("onboarding_pulse_l5", "onboarding_pulse_l10"):
            perf_p = 0.15  # category-agnostic, concentrated listing 5->10

    remaining = max(0.0, 1 - auth_p - setup_p - perf_p)
    w_other = np.array(SELLER_VOC_WEIGHTS_OTHER) / sum(SELLER_VOC_WEIGHTS_OTHER) * remaining
    pool = ["authentication-friction", "listing-setup-complexity", "no-performance-visibility"] + SELLER_VOC_THEMES_OTHER
    weights = [auth_p, setup_p, perf_p] + w_other.tolist()
    theme_tag = random.choices(pool, weights=weights)[0]

    if theme_tag == "authentication-friction":
        sentiment = "negative"
        verbatim = random.choice([
            "GradeSure turnaround is the bottleneck -- I can't list faster than they can verify.",
            "Every new listing sits pending authentication for days before it's even visible to buyers.",
            "Wish there was a way to pre-verify a batch instead of waiting per-listing.",
        ])
    elif theme_tag == "listing-setup-complexity":
        sentiment = random.choices(["negative", "neutral"], weights=[0.65, 0.35])[0]
        verbatim = random.choice([
            "No way to bulk-upload -- I'm re-typing nearly the same listing over and over.",
            "Wish there was a duplicate-listing button, setup for each new item takes forever.",
            "The listing form has too many required fields for a simple item.",
        ])
    elif theme_tag == "no-performance-visibility":
        sentiment = random.choices(["negative", "neutral"], weights=[0.60, 0.40])[0]
        verbatim = random.choice([
            "I can see my listing is live but no idea why it isn't converting.",
            "No visibility into how my listing compares to similar ones that ARE selling.",
            "Wish I could see views vs. buys per listing so I know what to fix next.",
        ])
    elif theme_tag is None:
        sentiment = random.choices(["positive", "neutral", "negative"], weights=[0.50, 0.30, 0.20])[0]
        verbatim = "General seller experience feedback, nothing specific called out."
    else:
        sentiment = random.choices(["positive", "neutral", "negative"], weights=[0.35, 0.30, 0.35])[0]
        verbatim = f"Feedback related to {theme_tag.replace('-', ' ')}."

    score_type = "seller_nps_0_10" if survey_type == "quarterly_seller_nps" else "ces_1_7"
    if score_type == "seller_nps_0_10":
        score = {"positive": random.choice([9, 10]), "neutral": random.choice([7, 8]),
                  "negative": random.choice([0, 2, 4, 5, 6])}[sentiment]
    else:  # ces_1_7 (customer effort score, lower is better -- negative sentiment = high effort)
        score = {"positive": random.choice([1, 2]), "neutral": random.choice([3, 4]),
                  "negative": random.choice([5, 6, 7])}[sentiment]

    span = max((TODAY - SELLER_PULSE_LAUNCH).days, 0)
    responded_at = datetime.combine(SELLER_PULSE_LAUNCH + timedelta(days=random.randint(0, span)),
                                     datetime.min.time()) + timedelta(hours=random.randint(8, 20))
    return {
        "response_id": rid("svoc", i, width=7), "seller_id": seller_id, "survey_type": survey_type,
        "responded_at": responded_at, "score": float(score), "score_type": score_type,
        "verbatim_text": verbatim, "theme_tag": theme_tag, "sentiment": sentiment,
    }


def gen_fact_seller_voc_responses(dim_seller: pd.DataFrame, n_total: int = 4_000) -> pd.DataFrame:
    active = dim_seller[dim_seller["status"] == "active"].copy()
    tier_weight = {"top": 3.0, "large": 2.0, "mid": 1.3, "small": 1.0}

    n_onboarding = int(round(n_total * 0.55))
    n_quarterly = n_total - n_onboarding

    cohort = active[active["seller_id"].apply(_is_new_seller_cohort_id)]
    rows = []
    seq = 0
    pulse_types = ["onboarding_pulse_l1", "onboarding_pulse_l5", "onboarding_pulse_l10"]
    pulse_w = [0.30, 0.40, 0.30]
    cohort_sample = cohort.sample(n=n_onboarding, replace=True, random_state=SEED).reset_index(drop=True)
    for s in cohort_sample.itertuples(index=False):
        seq += 1
        survey_type = random.choices(pulse_types, weights=pulse_w)[0]
        rows.append(_seller_voc_row(seq, s.seller_id, s.category_focus, survey_type))

    w = active["_gmv_tier"].map(tier_weight).fillna(1.0).to_numpy(dtype=float)
    quarterly_sample = active.sample(n=n_quarterly, replace=True, weights=w, random_state=SEED).reset_index(drop=True)
    for s in quarterly_sample.itertuples(index=False):
        seq += 1
        rows.append(_seller_voc_row(seq, s.seller_id, s.category_focus, "quarterly_seller_nps"))

    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# Sell-through top-up (Collectibles new-vs-tenured contrast, 1.8 vs 3.6 orders
# per active listing per quarter -- "illustrative" per CANON.md, seller-side
# conversion is a DIFFERENT metric than buyer-side conversion). Deliberately
# engineered ON TOP of the emergent general/guest 3P order pool -- never
# subtracted -- so this never disturbs Marketplace GMV (built independently
# off fact_traffic_daily/marketplace_gmv_summary, convention 5).
# --------------------------------------------------------------------------
def _seller_3p_order_row(seq: int, order_date_: date, seller_id: str, sub_vc: str, gmv: float) -> dict:
    units = max(1, int(round(np.random.lognormal(np.log(1.4), 0.4))))
    is_returned, return_date_, reason, refund_amt, refund_issued = _maybe_return(order_date_, gmv, 0.054)
    return {
        "order_id": rid("ord", seq, width=8), "order_date": order_date_, "member_id": None,
        "market": "US", "vertical_code": "MARKETPLACE", "sub_vertical_code": sub_vc,
        "channel": "3P", "seller_id": seller_id, "fulfillment_type": "ship_to_home",
        "gmv_usd": gmv, "units": units,
        "device": random.choices(["web", "app", "store_kiosk"], weights=[0.55, 0.42, 0.03])[0],
        "is_returned": is_returned, "return_date": return_date_, "return_reason_code": reason,
        "refund_usd": refund_amt, "refund_issued_date": refund_issued,
    }


def gen_sell_through_topup_orders(dim_seller: pd.DataFrame, listings: pd.DataFrame,
                                    fact_orders_general: pd.DataFrame) -> pd.DataFrame:
    active_by_seller = listings[listings["status"] == "active"].groupby("seller_id").size()
    orders_3p = fact_orders_general.loc[fact_orders_general["channel"] == "3P", ["seller_id", "order_date"]]
    seq = [9_000_000]
    rows: list[dict] = []
    stats: list[str] = []

    def topup(sellers: pd.DataFrame, windows: dict, target_rate: float, label: str) -> None:
        if len(sellers) == 0:
            return
        active_total = int(active_by_seller.reindex(sellers["seller_id"]).fillna(0).sum())
        target_total = int(round(target_rate * max(active_total, 1)))
        win_df = pd.DataFrame({"seller_id": list(windows.keys()),
                                "lo": [w[0] for w in windows.values()], "hi": [w[1] for w in windows.values()]})
        merged = orders_3p[orders_3p["seller_id"].isin(windows.keys())].merge(win_df, on="seller_id", how="inner")
        existing = 0
        if len(merged):
            existing = int(sum(1 for lo, od, hi in zip(merged["lo"], merged["order_date"], merged["hi"]) if lo <= od <= hi))
        delta = max(target_total - existing, 0)
        added = 0
        if delta > 0 and active_total > 0:
            weights_map = active_by_seller.reindex(sellers["seller_id"]).fillna(0)
            w = np.maximum(weights_map.to_numpy(dtype=float) * np.random.normal(1.0, 0.1, size=len(sellers)), 0.01)
            counts = allocate_int(delta, w)
            for sid, n in zip(sellers["seller_id"], counts):
                lo, hi = windows[sid]
                span = max((hi - lo).days, 1)
                for _ in range(int(n)):
                    seq[0] += 1
                    od = lo + timedelta(days=random.randint(0, span))
                    gmv = round(float(np.random.lognormal(np.log(85), 0.5)), 2)
                    rows.append(_seller_3p_order_row(seq[0], od, sid, "COLLECTIBLES", gmv))
                    added += 1
        stats.append(f"{label}: active_listings={active_total} target_ratio={target_rate} "
                      f"target_orders~{target_total} existing_emergent={existing} topped_up={added}")

    cohort_ids = {sid for sid in dim_seller["seller_id"] if _is_new_seller_cohort_id(sid)}
    new_sellers = dim_seller[dim_seller["seller_id"].isin(cohort_ids) & (dim_seller["category_focus"] == "collectibles")]
    new_windows = {r.seller_id: (r.onboarded_date, min(r.onboarded_date + timedelta(days=90), TODAY))
                   for r in new_sellers.itertuples(index=False)}
    topup(new_sellers, new_windows, 1.8, "new (first 90d)")

    tenure_cutoff = TODAY - timedelta(days=365)
    tenured = dim_seller[(dim_seller["category_focus"] == "collectibles") & (dim_seller["status"] == "active")
                          & (~dim_seller["seller_id"].isin(cohort_ids))
                          & (dim_seller["onboarded_date"] <= tenure_cutoff)]
    t_lo, t_hi = TODAY - timedelta(days=90), TODAY
    tenured_windows = {sid: (t_lo, t_hi) for sid in tenured["seller_id"]}
    topup(tenured, tenured_windows, 3.6, "tenured (12mo+)")

    for line in stats:
        print(f"  sell-through topup -- {line}")
    return pd.DataFrame(rows)


# ----------------------------- main -----------------------------------
def _write(df: pd.DataFrame, name: str) -> None:
    df.to_parquet(OUT / f"{name}.parquet", index=False)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    print("=== Acme eCommerce synthetic data gen -> /tmp/acme_ecomm_data ===")

    print("dim_date ...")
    dim_date = gen_dim_date()
    _write(dim_date, "dim_date")

    print("dim_vertical ...")
    _write(gen_dim_vertical(), "dim_vertical")

    print("dim_associate ...")
    dim_associate = gen_dim_associate()
    _write(dim_associate, "dim_associate")

    print("dim_fulfillment_node ...")
    _write(gen_dim_fulfillment_node(), "dim_fulfillment_node")

    print("dim_seller (+ new-seller onboarding funnel cohort) ...")
    dim_seller, cohort_listings = gen_dim_seller()
    cohort_ids = {sid for sid in dim_seller["seller_id"] if _is_new_seller_cohort_id(sid)}
    _write(dim_seller.drop(columns=["_gmv_tier"]), "dim_seller")

    print("dim_experiment ...")
    dim_experiment = gen_dim_experiment()
    _write(dim_experiment, "dim_experiment")

    print("dim_marketing_calendar ...")
    _write(gen_dim_marketing_calendar(), "dim_marketing_calendar")

    print("dim_member + membership lifecycle simulation (this one takes a bit) ...")
    dim_member = gen_dim_member()
    dim_member, fact_membership_events = simulate_membership_lifecycle(dim_member)
    _write(dim_member.drop(columns=["dormant_flag", "depth_flag", "streaming_only_flag"]), "dim_member")
    _write(fact_membership_events, "fact_membership_events")

    print("fact_traffic_daily ...")
    fact_traffic_daily = gen_fact_traffic_daily()
    _write(fact_traffic_daily, "fact_traffic_daily")

    print("fact_promise_vs_actual ...")
    fact_promise_vs_actual = gen_fact_promise_vs_actual()
    _write(fact_promise_vs_actual, "fact_promise_vs_actual")

    print("fact_experiment_exposures ...")
    _write(gen_fact_experiment_exposures(dim_experiment), "fact_experiment_exposures")

    print("fact_experiment_readouts ...")
    _write(gen_fact_experiment_readouts(dim_experiment), "fact_experiment_readouts")

    print("fact_orders (this one takes a bit) ...")
    fact_orders = gen_fact_orders(dim_member, dim_seller)

    print("fact_marketplace_listings (general + new-seller cohort) ...")
    fact_marketplace_listings_general = gen_fact_marketplace_listings(dim_seller, exclude_seller_ids=cohort_ids)
    fact_marketplace_listings = pd.concat([fact_marketplace_listings_general, cohort_listings], ignore_index=True)

    print("sell-through top-up orders (Collectibles new-vs-tenured, 1.8 vs 3.6) ...")
    topup_orders = gen_sell_through_topup_orders(dim_seller, fact_marketplace_listings, fact_orders)
    fact_orders = pd.concat([fact_orders, topup_orders], ignore_index=True)

    _write(fact_orders, "fact_orders")
    _write(fact_marketplace_listings, "fact_marketplace_listings")

    print("fact_care_contacts ...")
    fact_care_contacts = gen_fact_care_contacts(dim_member, dim_associate, fact_orders)
    _write(fact_care_contacts, "fact_care_contacts")

    print("fact_voc_responses ...")
    _write(gen_fact_voc_responses(dim_member, fact_orders, fact_care_contacts), "fact_voc_responses")

    print("fact_seller_voc_responses (NEW TABLE) ...")
    _write(gen_fact_seller_voc_responses(dim_seller), "fact_seller_voc_responses")

    print("mart: traffic_conversion_summary ...")
    _write(gen_mart_traffic_conversion_summary(fact_traffic_daily), "traffic_conversion_summary")

    print("mart: marketplace_gmv_summary ...")
    _write(gen_mart_marketplace_gmv_summary(fact_traffic_daily), "marketplace_gmv_summary")

    print("mart: fulfillment_speed_daily ...")
    _write(gen_mart_fulfillment_speed_daily(fact_promise_vs_actual), "fulfillment_speed_daily")

    print("mart: care_deflection_daily ...")
    _write(gen_mart_care_deflection_daily(), "care_deflection_daily")

    print("mart: member_cltv ...")
    _write(gen_mart_member_cltv(dim_member, fact_orders), "member_cltv")

    print("mart: marketplace_seller_performance ...")
    _write(gen_mart_marketplace_seller_performance(dim_seller, fact_marketplace_listings, fact_orders),
           "marketplace_seller_performance")

    print("\nrow counts:")
    total = 0
    for p in sorted(OUT.glob("*.parquet")):
        df = pd.read_parquet(p)
        total += len(df)
        print(f"  {p.name:42s} {len(df):>9,} rows  {p.stat().st_size / 1024:>9.1f} KB")
    print(f"\n{len(list(OUT.glob('*.parquet')))} tables, {total:,} total rows")


if __name__ == "__main__":
    main()
