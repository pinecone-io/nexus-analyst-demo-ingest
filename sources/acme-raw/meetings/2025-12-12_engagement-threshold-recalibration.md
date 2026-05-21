# notes — engagement threshold recalibration review — 2025-12-12
attendees: marco chen, elena volkov, dan lee
(my rough notes, cleaned up a bit -mc)

why we met: engaged customers were churning more than expected. engaged accounts renewing at
~88% vs the 92-95% we'd expect for "engaged". so is the threshold too loose?

current threshold: >=3 active users AND >=10 successful workflow runs in 28d.

findings:
- threshold was set in 2024 when avg paid customer was ~18 seats / 150 runs/mo. now it's ~47 seats / 620 runs. the bar got easy to clear.
- BUT renewal prediction for "not engaged" is still way worse (~70%), so the flag still has signal as a floor.

decision: KEEP the threshold as is (3 users / 10 runs / 28d). engaged is a floor ("are they using it at all"), not a health ceiling. seat-utilization + account_health bands catch the "technically engaged but under-utilizing" case. revisit in 2026-Q3.

action items:
- [ ] dan: nothing to change in account_health.is_engaged
- [ ] marco: keep surfacing utilization_band as secondary signal
- [parked] value realization score model for the nuanced case (2026-H1, see vrs kickoff)
