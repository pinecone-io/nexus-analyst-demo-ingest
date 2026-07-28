"""Generate synthetic Acme Inc warehouse — 13 BQ tables to /tmp/acme_data/*.parquet.

Deterministic via seed=42. Run with: python -m datasets.acme.generate
"""

from __future__ import annotations

import hashlib
import json
import random
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

OUT = Path("/tmp/acme_data")
SEED = 42
TODAY = date(2026, 5, 4)
FOUNDED = date(2023, 1, 1)

fake = Faker()
Faker.seed(SEED)
random.seed(SEED)
np.random.seed(SEED)


# ----------------------------- helpers --------------------------------

def rid(prefix: str, i: int, width: int = 6) -> str:
    return f"{prefix}_{i:0{width}d}"


def date_range_skewed(start: date, end: date, n: int, recency_weight: float = 1.5) -> list[date]:
    """Sample n dates in [start, end), skewed toward `end` by recency_weight (1=uniform)."""
    span = (end - start).days
    u = np.random.beta(recency_weight, 1.0, size=n)
    offsets = (u * span).astype(int)
    return [start + timedelta(days=int(o)) for o in offsets]


def ts_in_day(d: date) -> datetime:
    secs = random.randint(0, 86399)
    return datetime.combine(d, datetime.min.time()) + timedelta(seconds=secs)


# ----------------------------- dimensions -----------------------------

def gen_dim_dates() -> pd.DataFrame:
    rows = []
    d = date(2022, 1, 1)
    end = date(2026, 12, 31)
    while d <= end:
        rows.append({
            "date": d,
            "year": d.year,
            "quarter": (d.month - 1) // 3 + 1,
            "month": d.month,
            "month_name": d.strftime("%B"),
            "week": d.isocalendar()[1],
            "day_of_week": d.strftime("%A"),
            "is_weekend": d.weekday() >= 5,
            "is_business_day": d.weekday() < 5,
        })
        d += timedelta(days=1)
    return pd.DataFrame(rows)


def gen_dim_plans() -> pd.DataFrame:
    return pd.DataFrame([
        {"plan_tier": "Free", "monthly_price_per_seat_usd": 0, "min_seats": 1,
         "workflow_run_quota_per_month": 100, "storage_gb": 1, "sla_uptime_pct": None},
        {"plan_tier": "Pro", "monthly_price_per_seat_usd": 49, "min_seats": 1,
         "workflow_run_quota_per_month": 10000, "storage_gb": 10, "sla_uptime_pct": 99.5},
        {"plan_tier": "Business", "monthly_price_per_seat_usd": 149, "min_seats": 50,
         "workflow_run_quota_per_month": 100000, "storage_gb": 100, "sla_uptime_pct": 99.9},
        {"plan_tier": "Enterprise", "monthly_price_per_seat_usd": None, "min_seats": 250,
         "workflow_run_quota_per_month": None, "storage_gb": 1000, "sla_uptime_pct": 99.95},
    ])


def gen_dim_employees() -> pd.DataFrame:
    """100 employees. Hardcode VPs + CEO. Generate the rest by team headcount."""
    rows = []
    # leadership locked
    leaders = [
        ("emp_001", "Sam Reyes", "Executive", "CEO", None, date(2023, 1, 1), "SF"),
        ("emp_010", "Priya Anand", "Engineering", "VP Engineering", "emp_001", date(2023, 1, 15), "SF"),
        ("emp_020", "Marcus Webb", "Sales", "VP Sales", "emp_001", date(2023, 2, 1), "SF"),
        ("emp_030", "Jordan Hayes", "Engineering", "VP Infrastructure", "emp_001", date(2023, 6, 1), "SF"),
        ("emp_040", "Elena Volkov", "CS", "VP Customer Success", "emp_001", date(2023, 3, 1), "Amsterdam"),
        ("emp_050", "Dan Lee", "Product", "VP Product", "emp_001", date(2023, 2, 15), "SF"),
        ("emp_060", "Rachel Stein", "Finance", "CFO", "emp_001", date(2023, 4, 1), "SF"),
        ("emp_070", "Jasmine Park", "Marketing", "VP Marketing", "emp_001", date(2023, 5, 1), "SF"),
        ("emp_080", "Tomás Vega", "People", "Head of People", "emp_001", date(2023, 7, 1), "Remote-NA"),
        ("emp_090", "Anika Schmidt", "Legal", "General Counsel", "emp_001", date(2024, 1, 15), "Amsterdam"),
    ]
    leader_ids = {row[3].split()[-1] if row[3].startswith("VP") or row[3] == "CEO" else None: row[0] for row in leaders}
    for emp_id, name, team, role, mgr, hire, loc in leaders:
        rows.append({
            "employee_id": emp_id, "full_name": name, "team": team, "role": role,
            "manager_employee_id": mgr, "hire_date": hire, "termination_date": None,
            "location": loc, "is_active": True,
        })

    # team headcount targets (VPs already counted above)
    plan = {
        "Engineering": (28, ["Software Engineer", "Senior Engineer", "Staff Engineer", "Engineering Manager"], "emp_010"),
        "Sales": (18, ["AE", "Senior AE", "Sales Engineer", "SDR", "Sales Manager"], "emp_020"),
        "CS": (14, ["CSM", "Senior CSM", "Support Engineer", "CS Manager"], "emp_040"),
        "Marketing": (9, ["Marketing Specialist", "Content Marketer", "Demand Gen", "Marketing Manager"], "emp_070"),
        "Product": (8, ["Product Manager", "Senior PM", "Product Designer"], "emp_050"),
        "Design": (5, ["Product Designer", "Brand Designer", "Design Manager"], "emp_050"),
        "Finance": (4, ["Accountant", "FP&A Analyst", "Finance Manager"], "emp_060"),
        "People": (3, ["Recruiter", "People Operations"], "emp_080"),
        "Legal": (1, ["Paralegal"], "emp_090"),
    }

    next_id = 100
    for team, (count, roles, mgr) in plan.items():
        for _ in range(count):
            emp_id = rid("emp", next_id, width=3)
            next_id += 1
            hire = FOUNDED + timedelta(days=random.randint(30, (TODAY - FOUNDED).days - 30))
            terminated = random.random() < 0.05
            term_date = hire + timedelta(days=random.randint(180, 800)) if terminated else None
            if term_date and term_date > TODAY:
                term_date = None
                terminated = False
            rows.append({
                "employee_id": emp_id,
                "full_name": fake.name(),
                "team": team,
                "role": random.choice(roles),
                "manager_employee_id": mgr,
                "hire_date": hire,
                "termination_date": term_date,
                "location": random.choices(
                    ["SF", "Amsterdam", "Remote-NA", "Remote-EU"],
                    weights=[0.45, 0.20, 0.20, 0.15],
                )[0],
                "is_active": not terminated,
            })

    return pd.DataFrame(rows)


def gen_dim_customers(employees: pd.DataFrame) -> pd.DataFrame:
    n = 800
    rows = []
    aes = employees[(employees["team"] == "Sales") & (employees["role"].isin(["AE", "Senior AE"])) & employees["is_active"]]["employee_id"].tolist()
    csms = employees[(employees["team"] == "CS") & (employees["role"].isin(["CSM", "Senior CSM"])) & employees["is_active"]]["employee_id"].tolist()

    signup_dates = date_range_skewed(FOUNDED, TODAY, n, recency_weight=1.8)
    countries_pop = ["US", "GB", "DE", "FR", "NL", "CA", "AU", "IE", "SE", "ES"]
    country_w = [0.60, 0.08, 0.06, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.04]
    industries = ["SaaS", "E-commerce", "Finance", "Healthcare", "Education", "Media", "Other"]
    ind_w = [0.30, 0.20, 0.15, 0.10, 0.10, 0.10, 0.05]
    bands = ["1-10", "11-50", "51-200", "201-1000", "1001-5000", "5000+"]
    band_w = [0.25, 0.30, 0.20, 0.15, 0.07, 0.03]
    plan_tiers = ["Free", "Pro", "Business", "Enterprise"]
    plan_w = [0.30, 0.40, 0.25, 0.05]
    use_cases = [
        "Lead routing from forms to Salesforce",
        "Slack alerts from Stripe events",
        "Sync HubSpot contacts to GSheets",
        "Auto-tag GitHub issues from Linear",
        "Daily revenue digest to Slack",
        "Onboarding email sequences",
        "Ticket triage from Intercom to Zendesk",
        "Data sync between Postgres and Snowflake",
        "AI-powered customer support routing",
        "Marketing attribution sync",
    ]
    channels = ["organic", "paid_search", "content", "referral", "outbound", "partner"]
    channel_w = [0.30, 0.20, 0.15, 0.15, 0.15, 0.05]

    for i, sd in enumerate(sorted(signup_dates)):
        cust_id = rid("cust", i + 1)
        plan = random.choices(plan_tiers, weights=plan_w)[0]
        country = random.choices(countries_pop, weights=country_w)[0]
        region = "NA" if country in ("US", "CA") else "APAC" if country == "AU" else "EMEA"
        band = random.choices(bands, weights=band_w)[0]
        # account_tier loosely correlated with plan + employee_count
        if plan == "Enterprise":
            tier = "Ent"
        elif plan == "Business":
            tier = random.choices(["MM", "Ent"], weights=[0.7, 0.3])[0]
        elif plan == "Pro":
            tier = random.choices(["SMB", "MM"], weights=[0.7, 0.3])[0]
        else:
            tier = "SMB"

        # status: 8% churned, 2% paused (only customers >180d old eligible)
        age_days = (TODAY - sd).days
        if age_days > 180:
            status = random.choices(["active", "churned", "paused"], weights=[0.90, 0.08, 0.02])[0]
        else:
            status = "active"
        churn_date = None
        if status == "churned":
            churn_date = sd + timedelta(days=random.randint(60, age_days - 1))
            current_plan = "Free"  # downgraded effectively
            current_mrr = 0
        else:
            current_plan = plan
            if plan == "Free":
                current_mrr = 0
            elif plan == "Pro":
                seats = random.randint(1, 10)
                current_mrr = 49 * seats
            elif plan == "Business":
                seats = random.randint(50, 120)
                current_mrr = 149 * seats
            else:  # Enterprise
                # ACV between 50K and 500K → MRR
                acv = random.choice([50_000, 75_000, 100_000, 150_000, 200_000, 300_000, 500_000])
                current_mrr = acv / 12

        rows.append({
            "customer_id": cust_id,
            "company_name": fake.company(),
            "signup_date": sd,
            "country": country,
            "region": region,
            "industry": random.choices(industries, weights=ind_w)[0],
            "employee_count_band": band,
            "account_tier": tier,
            "current_plan_tier": current_plan,
            "current_mrr_usd": round(current_mrr, 2),
            "status": status,
            "churn_date": churn_date,
            "csm_employee_id": random.choice(csms) if (plan in ("Business", "Enterprise") and status == "active") else None,
            "ae_employee_id": random.choice(aes) if (tier in ("MM", "Ent") and status != "paused") else None,
            "acquisition_channel": random.choices(channels, weights=channel_w)[0],
            "primary_use_case": random.choice(use_cases),
        })
    return pd.DataFrame(rows)


def gen_dim_users(customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    next_id = 1
    for _, c in customers.iterrows():
        plan = c["current_plan_tier"]
        if c["status"] == "churned":
            user_count = random.randint(1, 5)
        elif plan == "Free":
            user_count = random.randint(1, 3)
        elif plan == "Pro":
            user_count = random.randint(2, 10)
        elif plan == "Business":
            user_count = random.randint(20, 100)
        else:  # Enterprise
            user_count = random.randint(80, 400)

        domain = c["company_name"].lower().replace(",", "").replace(".", "").replace(" ", "")[:24] + ".com"
        first_signup = c["signup_date"]

        # admin first
        first_user_id = rid("user", next_id)
        next_id += 1
        rows.append({
            "user_id": first_user_id,
            "customer_id": c["customer_id"],
            "email_domain": domain,
            "role": "admin",
            "signup_date": first_signup,
            "last_login_date": (TODAY - timedelta(days=random.randint(0, 60))) if c["status"] != "churned" else c["churn_date"],
            "is_active": c["status"] != "churned" and random.random() < 0.85,
            "invited_by_user_id": None,
        })
        for _ in range(user_count - 1):
            u_id = rid("user", next_id)
            next_id += 1
            user_signup = first_signup + timedelta(days=random.randint(1, max(2, (TODAY - first_signup).days)))
            if user_signup > TODAY:
                user_signup = TODAY
            churned = c["status"] == "churned"
            ll = c["churn_date"] if churned else (TODAY - timedelta(days=random.randint(0, 90)))
            role = random.choices(["admin", "builder", "viewer"], weights=[0.10, 0.55, 0.35])[0]
            rows.append({
                "user_id": u_id,
                "customer_id": c["customer_id"],
                "email_domain": domain,
                "role": role,
                "signup_date": user_signup,
                "last_login_date": ll if random.random() < 0.85 else None,
                "is_active": (not churned) and random.random() < 0.65,
                "invited_by_user_id": first_user_id,
            })
    return pd.DataFrame(rows)


def gen_fact_subscriptions(customers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    sub_seq = 0
    for _, c in customers.iterrows():
        signup = c["signup_date"]
        plan = c["current_plan_tier"]
        status = c["status"]

        # initial subscription always Free
        sub_seq += 1
        first_id = rid("sub", sub_seq)
        last_id = first_id
        last_plan = "Free"
        last_seats = 1
        last_mrr = 0
        last_start = signup
        rows.append({
            "subscription_id": first_id,
            "customer_id": c["customer_id"],
            "plan_tier": "Free",
            "start_date": signup,
            "end_date": None,
            "mrr_usd": 0,
            "seat_count": 1,
            "billing_cycle": "monthly",
            "is_current": False,
            "change_type": "new",
            "changed_from_subscription_id": None,
        })

        # path: Free → upgrade?
        if plan != "Free" or status == "churned":
            target_plan = plan if plan != "Free" else random.choice(["Pro", "Business"])
            up_date = signup + timedelta(days=random.randint(7, 90))
            if up_date > TODAY:
                up_date = TODAY
            sub_seq += 1
            up_id = rid("sub", sub_seq)
            seats = (random.randint(2, 10) if target_plan == "Pro"
                     else random.randint(50, 120) if target_plan == "Business"
                     else random.randint(250, 500))
            mrr = (49 * seats if target_plan == "Pro"
                   else 149 * seats if target_plan == "Business"
                   else random.choice([50_000, 75_000, 100_000, 150_000, 200_000, 300_000]) / 12)
            # close out previous
            for r in rows:
                if r["subscription_id"] == last_id:
                    r["end_date"] = up_date
                    break
            rows.append({
                "subscription_id": up_id,
                "customer_id": c["customer_id"],
                "plan_tier": target_plan,
                "start_date": up_date,
                "end_date": None,
                "mrr_usd": round(mrr, 2),
                "seat_count": seats,
                "billing_cycle": random.choices(["monthly", "annual"], weights=[0.4, 0.6])[0],
                "is_current": False,
                "change_type": "upgrade",
                "changed_from_subscription_id": last_id,
            })
            last_id = up_id
            last_plan = target_plan
            last_seats = seats
            last_mrr = mrr
            last_start = up_date

            # maybe seat changes
            if random.random() < 0.3 and (TODAY - up_date).days > 90:
                sc_date = up_date + timedelta(days=random.randint(60, max(61, (TODAY - up_date).days - 30)))
                if sc_date <= TODAY:
                    sub_seq += 1
                    sc_id = rid("sub", sub_seq)
                    new_seats = max(1, last_seats + random.choice([-10, -5, 5, 10, 20]))
                    if last_plan == "Pro":
                        new_mrr = 49 * new_seats
                    elif last_plan == "Business":
                        new_mrr = 149 * new_seats
                    else:
                        new_mrr = last_mrr
                    for r in rows:
                        if r["subscription_id"] == last_id:
                            r["end_date"] = sc_date
                            break
                    rows.append({
                        "subscription_id": sc_id,
                        "customer_id": c["customer_id"],
                        "plan_tier": last_plan,
                        "start_date": sc_date,
                        "end_date": None,
                        "mrr_usd": round(new_mrr, 2),
                        "seat_count": new_seats,
                        "billing_cycle": "annual" if random.random() < 0.5 else "monthly",
                        "is_current": False,
                        "change_type": "seat_change",
                        "changed_from_subscription_id": last_id,
                    })
                    last_id = sc_id
                    last_seats = new_seats
                    last_mrr = new_mrr
                    last_start = sc_date

        # churn?
        if status == "churned":
            sub_seq += 1
            ch_id = rid("sub", sub_seq)
            for r in rows:
                if r["subscription_id"] == last_id:
                    r["end_date"] = c["churn_date"]
                    break
            rows.append({
                "subscription_id": ch_id,
                "customer_id": c["customer_id"],
                "plan_tier": "Free",
                "start_date": c["churn_date"],
                "end_date": None,
                "mrr_usd": 0,
                "seat_count": 1,
                "billing_cycle": "monthly",
                "is_current": True,
                "change_type": "churn",
                "changed_from_subscription_id": last_id,
            })
        else:
            for r in rows:
                if r["subscription_id"] == last_id:
                    r["is_current"] = True
                    break

    return pd.DataFrame(rows)


def gen_fact_invoices(subs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    inv_seq = 0
    for _, s in subs.iterrows():
        if s["mrr_usd"] == 0:
            continue
        start = s["start_date"]
        end = s["end_date"] if s["end_date"] is not None else TODAY
        cycle = s["billing_cycle"]
        d = start
        while d < end:
            inv_seq += 1
            if cycle == "monthly":
                period_end = d + timedelta(days=30)
                amount = s["mrr_usd"]
            else:
                period_end = d + timedelta(days=365)
                amount = s["mrr_usd"] * 12 * 0.85  # annual discount
            if period_end > end:
                period_end = end
            status_pick = random.choices(["paid", "open", "void", "uncollectible"], weights=[0.93, 0.04, 0.01, 0.02])[0]
            paid_at = ts_in_day(d + timedelta(days=random.randint(0, 14))) if status_pick == "paid" else None
            rows.append({
                "invoice_id": rid("inv", inv_seq),
                "customer_id": s["customer_id"],
                "subscription_id": s["subscription_id"],
                "invoice_date": d,
                "period_start": d,
                "period_end": period_end,
                "amount_usd": round(amount, 2),
                "status": status_pick,
                "paid_at": paid_at,
            })
            d = period_end + timedelta(days=1)
            if cycle == "annual":
                break
    return pd.DataFrame(rows)


def gen_fact_workflow_runs(customers: pd.DataFrame, n_target: int = 100_000) -> pd.DataFrame:
    """Distribute runs across non-Free, non-churned customers, weighted by plan."""
    weights_by_plan = {"Free": 0, "Pro": 1.0, "Business": 6.0, "Enterprise": 30.0}
    elig = customers[customers["status"] != "churned"].copy()
    elig["weight"] = elig["current_plan_tier"].map(weights_by_plan)
    elig = elig[elig["weight"] > 0]
    elig["weight"] = elig["weight"] / elig["weight"].sum()

    rows = []
    cust_ids = elig["customer_id"].tolist()
    weights = elig["weight"].tolist()
    signup_lookup = dict(zip(elig["customer_id"], elig["signup_date"]))

    # per-customer workflow ids
    wf_pool = {}
    wf_seq = 0
    for cid in cust_ids:
        n_wfs = random.randint(2, 12)
        wfs = []
        for _ in range(n_wfs):
            wf_seq += 1
            wfs.append(rid("wf", wf_seq))
        wf_pool[cid] = wfs

    triggers = ["schedule", "webhook", "manual", "api"]
    trig_w = [0.40, 0.35, 0.10, 0.15]
    error_codes = ["AUTH_FAILED", "RATE_LIMITED", "STEP_TIMEOUT", "INTEGRATION_DOWN", "USER_ERROR", "VALIDATION_ERROR"]

    chosen = np.random.choice(cust_ids, size=n_target, p=weights)
    for i, cid in enumerate(chosen):
        wf = random.choice(wf_pool[cid])
        signup = signup_lookup[cid]
        # bias triggered_at toward recent
        days_window = max(1, (TODAY - signup).days)
        u = np.random.beta(2.0, 1.0)
        days_back_from_today = int((1 - u) * min(days_window, 540))
        run_date = TODAY - timedelta(days=days_back_from_today)
        run_ts = ts_in_day(run_date)
        status = random.choices(["success", "error", "timeout", "partial"], weights=[0.93, 0.04, 0.02, 0.01])[0]
        rows.append({
            "run_id": rid("wfr", i + 1, width=8),
            "workflow_id": wf,
            "customer_id": cid,
            "triggered_at": run_ts,
            "triggered_by": random.choices(triggers, weights=trig_w)[0],
            "status": status,
            "duration_ms": int(np.random.lognormal(mean=7.5, sigma=1.0)),
            "step_count": random.randint(2, 25),
            "error_code": random.choice(error_codes) if status != "success" else None,
        })
    return pd.DataFrame(rows)


def gen_fact_user_events(users: pd.DataFrame, customers: pd.DataFrame, n_target: int = 100_000) -> pd.DataFrame:
    cust_status = dict(zip(customers["customer_id"], customers["status"]))
    cust_plan = dict(zip(customers["customer_id"], customers["current_plan_tier"]))
    elig_users = users[users["is_active"]].copy()
    if len(elig_users) == 0:
        return pd.DataFrame()
    # weight by plan
    plan_w = {"Free": 0.5, "Pro": 1.0, "Business": 4.0, "Enterprise": 10.0}
    elig_users["plan_weight"] = elig_users["customer_id"].map(cust_plan).map(plan_w).fillna(0.0)
    w = elig_users["plan_weight"].values
    w = w / w.sum()

    events = ["login", "workflow_created", "workflow_run_succeeded", "workflow_run_failed",
              "integration_connected", "integration_disconnected", "template_imported",
              "invite_sent", "billing_viewed", "upgrade_clicked", "support_ticket_opened"]
    event_w = [0.35, 0.05, 0.30, 0.05, 0.05, 0.01, 0.05, 0.03, 0.05, 0.04, 0.02]

    chosen_idx = np.random.choice(len(elig_users), size=n_target, p=w)
    chosen_users = elig_users.iloc[chosen_idx]

    rows = []
    for i, u in enumerate(chosen_users.itertuples(index=False)):
        cid = u.customer_id
        if cust_status.get(cid) == "churned":
            continue
        signup_to_now = max(1, (TODAY - u.signup_date).days)
        u_uniform = np.random.beta(2.5, 1.0)
        days_ago = int((1 - u_uniform) * min(signup_to_now, 365))
        ev_date = TODAY - timedelta(days=days_ago)
        evname = random.choices(events, weights=event_w)[0]
        rows.append({
            "event_id": rid("evt", i + 1, width=8),
            "user_id": u.user_id,
            "customer_id": cid,
            "event_at": ts_in_day(ev_date),
            "event_name": evname,
            "properties_json": json.dumps({"source": random.choice(["web", "api", "ios", "android"])}),
        })
    return pd.DataFrame(rows)


def gen_fact_support_tickets(customers: pd.DataFrame, employees: pd.DataFrame, users: pd.DataFrame, n_target: int = 3000) -> pd.DataFrame:
    support_ids = employees[(employees["team"] == "CS") & employees["is_active"]]["employee_id"].tolist()
    elig = customers[customers["status"] != "churned"]
    if len(elig) == 0 or len(support_ids) == 0:
        return pd.DataFrame()
    plan_w = {"Free": 0.5, "Pro": 1.0, "Business": 3.0, "Enterprise": 8.0}
    weights = elig["current_plan_tier"].map(plan_w).fillna(0.0).values
    weights = weights / weights.sum()
    chosen_cust = np.random.choice(elig["customer_id"].values, size=n_target, p=weights)

    user_lookup = users.groupby("customer_id")["user_id"].apply(list).to_dict()

    channels = ["email", "intercom", "portal", "csm"]
    channel_w = [0.35, 0.30, 0.25, 0.10]
    priorities = ["P1", "P2", "P3", "P4"]
    pri_w = [0.05, 0.20, 0.50, 0.25]
    categories = ["auth", "billing", "integration", "workflow", "data", "onboarding", "feature_request", "bug"]
    cat_w = [0.10, 0.10, 0.20, 0.20, 0.10, 0.10, 0.10, 0.10]

    rows = []
    for i, cid in enumerate(chosen_cust):
        opened = ts_in_day(TODAY - timedelta(days=random.randint(0, 540)))
        pri = random.choices(priorities, weights=pri_w)[0]
        cat = random.choices(categories, weights=cat_w)[0]
        is_closed = random.random() < 0.92
        if is_closed:
            target_hours = {"P1": 4, "P2": 16, "P3": 48, "P4": 120}[pri]
            res_hours = max(0.1, np.random.gamma(2.0, target_hours / 2.0))
            closed = opened + timedelta(hours=res_hours)
            csat = random.choices([1, 2, 3, 4, 5, None], weights=[0.05, 0.05, 0.10, 0.30, 0.40, 0.10])[0]
        else:
            res_hours = None
            closed = None
            csat = None
        u_pool = user_lookup.get(cid, [])
        u_id = random.choice(u_pool) if u_pool else None
        rows.append({
            "ticket_id": rid("tkt", i + 1, width=6),
            "customer_id": cid,
            "user_id": u_id,
            "opened_at": opened,
            "closed_at": closed,
            "channel": random.choices(channels, weights=channel_w)[0],
            "priority": pri,
            "category": cat,
            "resolution_time_hours": round(res_hours, 2) if res_hours else None,
            "csat_score": csat,
            "assigned_to_employee_id": random.choice(support_ids),
        })
    return pd.DataFrame(rows)


def gen_fact_opportunities(customers: pd.DataFrame, employees: pd.DataFrame, n_target: int = 500) -> pd.DataFrame:
    aes = employees[(employees["team"] == "Sales") & (employees["role"].isin(["AE", "Senior AE"])) & employees["is_active"]]["employee_id"].tolist()
    sdrs = employees[(employees["team"] == "Sales") & (employees["role"] == "SDR") & employees["is_active"]]["employee_id"].tolist()

    biz_ent = customers[customers["current_plan_tier"].isin(["Business", "Enterprise"])].copy()
    rows = []
    stages = ["Prospecting", "Qualified", "Proposal", "Negotiation", "Closed_Won", "Closed_Lost"]
    stage_w = [0.10, 0.15, 0.10, 0.10, 0.40, 0.15]
    loss_reasons = ["competitor", "price", "no_decision", "feature_gap", "timing"]

    # ~70% map to known customers (Closed_Won)
    for i in range(n_target):
        stage = random.choices(stages, weights=stage_w)[0]
        if stage == "Closed_Won" and len(biz_ent) > 0:
            c = biz_ent.sample(1).iloc[0]
            cust_id = c["customer_id"]
            account_name = c["company_name"]
            created = c["signup_date"] - timedelta(days=random.randint(15, 90))
            close_d = c["signup_date"] + timedelta(days=random.randint(0, 30))
            won_d = close_d
            amount = c["current_mrr_usd"] * 12 if c["current_mrr_usd"] > 0 else random.choice([50_000, 100_000, 150_000])
            loss = None
        else:
            cust_id = None
            account_name = fake.company()
            created = TODAY - timedelta(days=random.randint(7, 360))
            close_d = created + timedelta(days=random.randint(30, 180))
            if close_d > TODAY:
                close_d = close_d
            won_d = None
            amount = random.choice([20_000, 50_000, 75_000, 100_000, 150_000, 250_000])
            loss = random.choice(loss_reasons) if stage == "Closed_Lost" else None

        rows.append({
            "opportunity_id": rid("opp", i + 1, width=5),
            "customer_id": cust_id,
            "account_name": account_name,
            "ae_employee_id": random.choice(aes) if aes else None,
            "sdr_employee_id": random.choice(sdrs) if sdrs and random.random() < 0.6 else None,
            "created_date": created,
            "stage": stage,
            "amount_usd": amount,
            "close_date": close_d,
            "closed_won_at": won_d,
            "loss_reason": loss,
        })
    return pd.DataFrame(rows)


def gen_fact_nps_responses(customers: pd.DataFrame, users: pd.DataFrame, n_target: int = 2000) -> pd.DataFrame:
    elig = customers[customers["current_plan_tier"].isin(["Pro", "Business", "Enterprise"]) & (customers["status"] != "churned")]
    if len(elig) == 0:
        return pd.DataFrame()
    user_lookup = users.groupby("customer_id")["user_id"].apply(list).to_dict()
    comments = [
        "Great product, saves us hours every week.",
        "Workflow editor could be more intuitive.",
        "Support has been responsive and helpful.",
        "Pricing jumps between tiers feel steep.",
        "Integrations cover most of what we need.",
        "Lacking a few enterprise features (audit log granularity, RBAC).",
        "We've recommended this to two other teams already.",
        "Hit run quotas faster than expected on Pro.",
        "Setup took longer than the docs suggested.",
        "The Slack integration is the most reliable one we use.",
    ]
    rows = []
    cust_ids = elig["customer_id"].sample(n=n_target, replace=True, random_state=SEED).tolist()
    quarters = ["2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1"]
    for i, cid in enumerate(cust_ids):
        # promoter/passive/detractor distribution: 50/30/20
        seg = random.choices(["promoter", "passive", "detractor"], weights=[0.50, 0.30, 0.20])[0]
        score = random.choice([9, 10]) if seg == "promoter" else random.choice([7, 8]) if seg == "passive" else random.choice([0, 2, 4, 5, 6])
        quarter = random.choice(quarters)
        u_pool = user_lookup.get(cid, [])
        u_id = random.choice(u_pool) if u_pool else None
        # quarter → mid-quarter timestamp
        q_year = int(quarter.split("-")[0])
        q_num = int(quarter.split("Q")[1])
        q_month = (q_num - 1) * 3 + 2
        ts = datetime(q_year, q_month, 15, random.randint(8, 18), random.randint(0, 59))
        rows.append({
            "response_id": rid("nps", i + 1, width=5),
            "customer_id": cid,
            "user_id": u_id,
            "responded_at": ts,
            "score": score,
            "comment": random.choice(comments) if random.random() < 0.5 else None,
            "segment": seg,
            "survey_quarter": quarter,
        })
    return pd.DataFrame(rows)


def gen_fact_marketing_touches(customers: pd.DataFrame, n_target: int = 5000) -> pd.DataFrame:
    channels = ["paid_search", "social", "content", "email", "webinar", "conference", "partner"]
    chan_w = [0.30, 0.20, 0.20, 0.15, 0.05, 0.05, 0.05]
    sources = {
        "paid_search": [("google", "cpc"), ("bing", "cpc")],
        "social": [("linkedin", "social"), ("twitter", "social"), ("youtube", "social")],
        "content": [("blog", "organic"), ("docs", "organic"), ("template-library", "organic")],
        "email": [("newsletter", "email"), ("nurture", "email")],
        "webinar": [("webinar", "event")],
        "conference": [("saastr", "event"), ("dreamforce", "event")],
        "partner": [("partner-portal", "referral")],
    }
    campaigns = ["spring-2025-launch", "g2-comparison", "enterprise-rampup-2026", "ai-workflows-launch", "always-on-brand", "competitor-alt", "free-trial-promo"]

    cust_signup = dict(zip(customers["customer_id"], customers["signup_date"]))
    cust_arr_list = customers["customer_id"].tolist()
    rows = []
    for i in range(n_target):
        ch = random.choices(channels, weights=chan_w)[0]
        utm_src, utm_med = random.choice(sources[ch])
        campaign = random.choice(campaigns)
        # ~25% touches map to a customer
        if random.random() < 0.25:
            cid = random.choice(cust_arr_list)
            signup = cust_signup[cid]
            t_date = signup - timedelta(days=random.randint(0, 90))
            attrib = round(random.choice([1000, 5000, 10_000, 20_000, 50_000]), 2) if random.random() < 0.3 else None
        else:
            cid = None
            t_date = TODAY - timedelta(days=random.randint(0, 540))
            attrib = None
        rows.append({
            "touch_id": rid("tch", i + 1, width=6),
            "lead_email_hash": hashlib.sha256(f"lead_{i}@{fake.domain_name()}".encode()).hexdigest()[:32],
            "customer_id": cid,
            "touched_at": ts_in_day(t_date),
            "channel": ch,
            "campaign": campaign,
            "utm_source": utm_src,
            "utm_medium": utm_med,
            "utm_campaign": campaign,
            "attributed_revenue_usd": attrib,
        })
    return pd.DataFrame(rows)


# ----------------------------- main -----------------------------------

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    print("=== Acme synthetic data gen → /tmp/acme_data ===")
    print("dim_dates ...")
    dd = gen_dim_dates()
    dd.to_parquet(OUT / "dim_dates.parquet", index=False)

    print("dim_plans ...")
    dp = gen_dim_plans()
    dp.to_parquet(OUT / "dim_plans.parquet", index=False)

    print("dim_employees ...")
    de = gen_dim_employees()
    de.to_parquet(OUT / "dim_employees.parquet", index=False)

    print("dim_customers ...")
    dc = gen_dim_customers(de)
    dc.to_parquet(OUT / "dim_customers.parquet", index=False)

    print("dim_users ...")
    du = gen_dim_users(dc)
    du.to_parquet(OUT / "dim_users.parquet", index=False)

    print("fact_subscriptions ...")
    fs = gen_fact_subscriptions(dc)
    fs.to_parquet(OUT / "fact_subscriptions.parquet", index=False)

    print("fact_invoices ...")
    fi = gen_fact_invoices(fs)
    fi.to_parquet(OUT / "fact_invoices.parquet", index=False)

    print("fact_workflow_runs ...")
    fwr = gen_fact_workflow_runs(dc)
    fwr.to_parquet(OUT / "fact_workflow_runs.parquet", index=False)

    print("fact_user_events ...")
    fue = gen_fact_user_events(du, dc)
    fue.to_parquet(OUT / "fact_user_events.parquet", index=False)

    print("fact_support_tickets ...")
    fst = gen_fact_support_tickets(dc, de, du)
    fst.to_parquet(OUT / "fact_support_tickets.parquet", index=False)

    print("fact_opportunities ...")
    fop = gen_fact_opportunities(dc, de)
    fop.to_parquet(OUT / "fact_opportunities.parquet", index=False)

    print("fact_nps_responses ...")
    fnps = gen_fact_nps_responses(dc, du)
    fnps.to_parquet(OUT / "fact_nps_responses.parquet", index=False)

    print("fact_marketing_touches ...")
    fmt = gen_fact_marketing_touches(dc)
    fmt.to_parquet(OUT / "fact_marketing_touches.parquet", index=False)

    print("\nrow counts:")
    for p in sorted(OUT.glob("*.parquet")):
        df = pd.read_parquet(p)
        print(f"  {p.name:35s} {len(df):>8} rows  {p.stat().st_size/1024:>8.1f} KB")


if __name__ == "__main__":
    main()
