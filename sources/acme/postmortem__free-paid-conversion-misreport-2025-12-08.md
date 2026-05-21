---
title: "Postmortem — Free→Paid conversion misreport 2025-12-08"
source_url: "internal://acme/postmortem/free-paid-conversion-misreport"
license: "synthetic-demo"
attribution: "Acme Inc internal postmortem (synthetic demo). Lead: Dan Lee (Product)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: postmortem
---

# Postmortem — Free→Paid conversion misreport (Nov 2025)

**Date**: 2025-12-08  
**Author**: @dan.lee  
**Status**: Completed  
**Impact**: Reporting error in the November Monthly Business Review (MBR) deck. No customer impact; internal metrics only.

## Summary

On 2025-12-04, the Product team reported a record-high Free→Paid conversion rate of **14.2%** for the November cohort. On 2025-12-06, @jasmine.park (Marketing) flagged a discrepancy while preparing the ROAS report, which showed a conversion rate of **11.8%**. 

The investigation revealed a fundamental mismatch in how "conversion cohorts" were defined between Product and Marketing. Product was using a calendar-month signup cohort (anyone who signed up in Nov), while Marketing was using a campaign-window cohort (anyone who converted in Nov, regardless of signup date).

## Timeline

- **2025-12-04 09:00 AM**: @dan.lee publishes Nov MBR deck with 14.2% conversion rate.
- **2025-12-06 11:30 AM**: @jasmine.park pings #data-help noting that her Looker dashboard for "Paid Conversions by Channel" shows only 11.8% for the same period.
- **2025-12-06 02:00 PM**: @david.kim investigates the SQL behind the two Looker tiles.
- **2025-12-07 10:00 AM**: Root cause identified: Product’s query was filtering `dim_customers.signup_date` to November, while Marketing’s query was filtering `fact_subscriptions.start_date` to November for `change_type = 'upgrade'`.
- **2025-12-08 09:00 AM**: Corrected figure (11.8% for the campaign window, 12.1% for the Nov signup cohort) published.
- **2025-12-08 04:00 PM**: Canonical definition finalized in `slack__data-help__free-to-paid-conversion-window.md`.

## Root Cause

The discrepancy was caused by **metric drift** and the lack of a canonical dbt model for conversion rates.

1. **Product Definition (Cohort-based)**: Looked at all users who signed up in Nov and checked if they ever upgraded. This is the correct way to measure product-led growth (PLG) efficiency, but it requires a "lookback window" (e.g., 14-day conversion) which wasn't applied.
2. **Marketing Definition (Volume-based)**: Looked at all upgrades that happened in Nov, divided by all signups that happened in Nov. This is a common "blended" conversion rate used for ROAS, but it includes "late bloomers" (users who signed up in Oct but converted in Nov).

Because Acme had a surge of October signups that converted in early November, the Marketing denominator was larger, leading to the lower (and more accurate for that period) 11.8% figure.

## Resolution

We have standardized the definition of "Conversion Rate" to prevent this in future MBRs. 

- **Primary Metric**: "Signup Month Conversion" (Cohort-based). This will be reported with a fixed 14-day window to ensure consistency.
- **Secondary Metric**: "Monthly Conversion Volume" (Blended). Used by Marketing for channel performance.

The logic has been moved into a new dbt model (see `dbt__model__conversion_funnel.md` - *drafting*) to ensure both Looker dashboards pull from the same source.

## Action Items

| Task | Owner | Status |
|---|---|---|
| Publish canonical SQL definition to `#data-help` | @dan.lee | **Done** |
| Create `marts/product/conversion_funnel.sql` dbt model | @david.kim | In Progress |
| Update Marketing ROAS dashboard to use new dbt model | @jasmine.park | Pending |
| Update MBR template to distinguish between Cohort vs Blended conversion | @lina.cho | **Done** |

## Lessons Learned

1. **Beware of "Simple" Ratios**: Conversion rate is never just `A / B`. It is always `A (in window X) / B (in window Y)`. Without explicit windowing, the numbers are meaningless.
2. **Standardize Early**: We relied on ad-hoc SQL in Looker for too long. As we approach $40M ARR, these "small" 2% discrepancies represent millions in projected revenue.
3. **Cross-functional Review**: Marketing and Product should have reviewed the MBR metrics together before the VP-level meeting.

## Related Documentation

- `notion__data-warehouse-conventions.md`
- `glossary__paid_customer.md`
- `slack__data-help__free-to-paid-conversion-window.md` (New)

---

**Thread from #data-help (2025-12-06)**:

> **@jasmine.park**: Hey @dan.lee, I'm seeing 11.8% for Nov conversion in my channel report, but the MBR says 14.2%. Are we excluding the 'referral' channel in the MBR?
>
> **@dan.lee**: No, should be everyone. I'm just doing `count(upgrades) / count(signups)` where signup_date is Nov.
>
> **@david.kim**: That's the issue. Dan, your `count(upgrades)` is looking at those specific Nov signups. Jasmine, your report is looking at *any* upgrade that happened in Nov. If an Oct signup upgraded on Nov 2nd, Dan misses it, but Jasmine counts it. 
>
> **@dan.lee**: 🤦‍♂️. We need a single model for this. 
>
> **@marcus.webb**: 🚩 This is a big delta. Let's make sure the board deck gets the corrected 11.8% if that's the volume reality. We can't overstate PLG efficiency by 20%.
