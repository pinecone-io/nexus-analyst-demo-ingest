# VRS (value realization score) kickoff — 2026-01-08  [STATUS: PARKED]
owners: dan lee, elena volkov

proposal: a per-customer "value realization score" to capture healthy-but-underutilizing
accounts that the binary engaged flag misses.

proposed (NOT BUILT) schema for acme.marts.value_realization_score:
- vrs_band  (proposed enum)
- champion_login_recency  (proposed signal — admin/champion last login)
- feature_adoption_depth  (proposed)

>>> none of this exists in BigQuery. there is no value_realization_score table. <<<
for current health use the account_health mart; for engagement use account_health.is_engaged.

status: scoping, then PARKED (no eng bandwidth 2026-H1). revisit later.
