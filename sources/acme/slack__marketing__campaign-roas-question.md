---
title: "Slack #marketing — campaign ROAS attribution disagreement"
source_url: "internal://acme/slack/marketing/campaign-roas-question"
license: "synthetic-demo"
attribution: "Acme Inc internal Slack thread (synthetic demo)."
fetched_at: '2026-05-04T07:00:00+00:00'
adapter: slack_thread
---

### #marketing
**Thread: Q1 Paid Search ROAS reporting**

**2026-03-04 09:12 AM**
**@jasmine.park**: Hey team, just pulling the final numbers for the Feb performance review. Paid search is looking incredibly strong for Q1 so far. Based on the `marts/sales/bookings_attribution` model, we’re seeing a ROAS of 4.2x on the "Workflow Automation" and "Zapier Alternative" keyword groups. 🚀

**2026-03-04 09:28 AM**
**@aliyah.brooks**: 4.2x is a great headline, but I’m looking at the `fact_marketing_touches` raw data and I’m worried we’re over-indexing on the final click. A lot of these "Paid Search" conversions actually had 2-3 content touches (whitepapers, webinars) in the 6 weeks prior. If we only credit the first touch, we’re basically saying our content strategy doesn't matter for MM/Ent deals.

**2026-03-04 09:35 AM**
**@jasmine.park**: @aliyah.brooks I hear you, but the model in `dbt__model__bookings_attribution.md` is explicitly first-touch. It’s what we’ve used for the last three board decks. If we change the logic now, we’re going to have to restate the last 4 quarters of channel performance.

**2026-03-04 09:42 AM**
**@aliyah.brooks**: I’m not saying restate, I’m saying we need to acknowledge the consideration cycle. For `cust_000512` (Vandelay Industries), they hit a blog post in December, attended a webinar in January, and *then* clicked a paid search ad in February. First-touch gives all $45k ACV to the search ad. That feels wrong.

**2026-03-04 10:05 AM**
**@jorge.martinez**: Jumping in from Sales Ops. Aliyah is right that the lag is real—our average sales cycle for Business tier is ~65 days. However, the current warehouse schema only supports first-touch attribution reliably. 

**2026-03-04 10:06 AM**
**@jorge.martinez**: Per the notes in `dbt__model__bookings_attribution.md`, multi-touch (linear or U-shaped) is on the H2 roadmap. We don't have the logic built yet to weight those intermediate touches without double-counting the ACV.

**2026-03-04 10:15 AM**
**@lina.cho**: @jorge.martinez @jasmine.park If we report 4.2x to @rachel.stein for the board deck, she’s going to ask why we aren't doubling the search budget. If the "real" ROAS (accounting for content) is actually 2.5x, we’re going to overspend in the wrong places.

**2026-03-04 10:22 AM**
**@lina.cho**: Can we report both? Or at least add a "Marketing Contribution" slide that shows the touch-count distribution per won opp?

**2026-03-04 10:45 AM**
**@jorge.martinez**: I can pull a quick view of `fact_marketing_touches` joined to `fact_opportunities` to show "Average touches per Closed_Won account" by tier. It won't be a formal ROAS model, but it’ll provide the context @aliyah.brooks is looking for.

**2026-03-04 11:02 AM**
**@jasmine.park**: That works for me. I’ll keep the 4.2x as the "First-Touch ROAS" (labeled clearly) and we can add a footnote about the 6-week multi-touch consideration cycle. 

**2026-03-04 11:15 AM**
**@aliyah.brooks**: Thanks @jorge.martinez. Let's make sure we specifically highlight the MM/Ent segment. The self-serve Pro conversions are usually 1-2 touches, but the Business deals are where the content lag really shows up.

**2026-03-04 11:30 AM**
**@lina.cho**: Agreed. I'll help @jorge.martinez sense-check the numbers before we send the draft to Rachel. We need to be careful—if we show search is "less" effective than previously thought, we need to show exactly where that value is actually being created (Content/Webinars).

**2026-03-04 11:45 AM**
**@jasmine.park**: 👍 I'll update the slide deck template to include the "Attribution Methodology" disclaimer pointing to the dbt docs.

---
**Labels**: `attribution-logic` `roas` `q1-reporting`
**Reactions**: ✅ (3), 📊 (2)
