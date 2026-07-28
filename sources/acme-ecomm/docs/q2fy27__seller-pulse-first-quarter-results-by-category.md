---
title: "Seller Pulse survey results export: first quarter of data, theme shares by category"
source_url: "internal://acme-ecomm/docs/q2fy27__seller-pulse-first-quarter-results-by-category"
license: "synthetic-demo"
attribution: "Synthetic content, Acme internal demo. Acme is a fictitious company."
fetched_at: '2026-07-20T12:00:00+00:00'
adapter: seller_pulse_survey
---

# Seller Pulse survey results export: first quarter of data, theme shares by category

**Author:** camille.duarte (Sr PM Marketplace Seller Experience)  
**Data Support:** wei.hartono (Analytics Engineer)  
**Date:** 2026-07-20  
**System of Record:** `nexus-analyst-demo.acme_ecomm` (`docs`)  

---

### 1. Administrative & Methodological Context

With the Seller Pulse survey instrument having completed its initial three months in market since launching back on 2026-04-20—following my onboarding as Sr PM for Marketplace Seller Experience (covering the Seller Listing and Seller Optimization surfaces across all three Marketplace sub-verticals)—wei.hartono and I have pulled the first full quarterly data export to review theme shares across categories.

**CRITICAL METHODOLOGICAL DISTINCTION (DO NOT BLEND STREAMS):**
As a preliminary point of record for any cross-functional data analysts or BI developers working on feedback loops, it must be stated explicitly that **this document and the underlying `fact_seller_voc_responses` table (`svoc_` prefix) represent a FULLY SEPARATE survey instrument from the buyer-side Medallia voice-of-customer stream (`fact_voc_responses`, `voc_` prefix)**. 
* Buyer VOC (Medallia) is triggered on a per-order or per-care-contact cadence, capturing consumer sentiments like `refund delay` or `listing-accuracy-gap`.
* **Seller Pulse** is an internal seller onboarding-milestone and quarterly survey instrument. It is triggered automatically at specific seller listing-count milestones (listing 1, listing 5, listing 10) alongside a standing quarterly NPS cadence.
* The two streams utilize entirely different theme vocabularies and underlying database tables. They must **never** be joined or blended into a generic "VOC" metric query. A seller-side theme (such as `authentication-friction`) must never appear on a buyer VOC row, and conversely, buyer themes are absent here.

The dataset analyzed here represents a representative panel of ~4,000 response rows spanning our ~2,560-seller active panel (which itself models a true active marketplace seller base of ~38,000).

---

### 2. Onboarding-Pulse Theme Shares by Category (L1 / L5)

Looking at the onboarding-pulse responses (`onboarding_pulse_l1` and `onboarding_pulse_l5` survey types), the theme distribution across our three Marketplace sub-verticals (**Collectibles**, **Style**, and **Resold**) reveals a stark divergence in seller friction points. 

As established since victor.okonkwo’s organization ramped up our trust and safety measures following the August 2025 counterfeit spike, our authentication protocols sit downstream of the buyer-trust wins. However, the seller-side survey results quantify precisely where that friction concentrates:

* **`authentication-friction` is overwhelmingly dominant within Collectibles onboarding-pulse respondents, registering at ~38%** of all verbatims. 
* By contrast, `authentication-friction` registers at only **~5% for Style** and **~6% for Resold**. This variance is structurally expected, as Style and Resold categories do not require the mandatory GradeSure authentication checks that govern Collectibles listings under the "Acme Verified" program launched back on 2025-09-08.

#### Category-Agnostic Themes (Surfaces Mapped)
In addition to the Collectibles authentication outlier, two major category-agnostic themes appear at remarkably consistent levels across all three sub-verticals (roughly 15–20% and 12–18% respectively). Crucially, these two map directly onto the specific product surfaces under my ownership:

1. **`listing-setup-complexity` (~15–20% share across all categories):** This theme hits hardest between listing 1 and listing 5. Verbatims consistently point to the lack of robust bulk-upload tools and duplicate-listing workflows for emerging third-party sellers. This maps directly to the **Seller Listing** surface.
2. **`no-performance-visibility` (~12–18% share across all categories):** This theme is heavily concentrated in the listing 5 to 10 range. These are sellers who successfully cleared initial setup hurdles but find themselves stalled, unable to discern why an existing listing isn't converting or what metrics to optimize next. This maps directly to the **Seller Optimization** surface.

---

### 3. Representative Seller Verbatim Quotes by Theme

To provide qualitative color to the quantitative shares cited above, below is an anonymized batch of representative seller verbatims pulled directly from `fact_seller_voc_responses`:

#### Theme: `authentication-friction` (Collectibles-heavy, ~38%)
* *"I had 40 vintage baseball cards ready to go live on day one. Waiting four to six days per card for GradeSure to clear the authentication queue before my badge shows up means my capital is tied up and my shop launch completely stalled out. If you're a small seller, the latency kills your momentum."* — Collectibles seller (onboarding milestone L1)
* *"The verification fee structure isn't transparent until you've already submitted the listing. When you're testing the platform with your first 5 items, the friction feels punitive rather than protective."* — Collectibles seller (onboarding milestone L5)

#### Theme: `listing-setup-complexity` (Category-agnostic, ~15–20%)
* *"There is zero CSV or bulk upload support for new catalog creators in the Resold tier. I have to input SKU attributes, dimensions, and condition grades one by one. It took me an entire weekend just to post 12 items."* — Resold seller (sel_500203, onboarding milestone L1)
* *"The attribute dropdowns for apparel sizing and material composition reset every time you hit back. For a multi-variant style listing, you're re-typing the same data over and over."* — Style seller (sel_500210, onboarding milestone L5)

#### Theme: `no-performance-visibility` (Category-agnostic, ~12–18%)
* *"My first 8 listings are live, but I have no idea how many people are actually viewing them versus clicking away. The dashboard just shows a static 'active' pill with zero impression or click metrics. How am I supposed to know if my pricing is wrong?"* — Style seller (onboarding milestone L5)
* *"I crossed 10 listings last month, but sales flatlined. I can't tell if my search ranking is buried or if my photos are the issue because the seller portal doesn't expose any category-benchmark data."* — Collectibles seller (onboarding milestone L10)

---

### 4. Survey Response-Rate Statistics & Operational Noise

* **Total Sent:** 5,420 milestone and quarterly survey invitations distributed across the active panel between 2026-04-20 and 2026-07-15.
* **Completed Responses:** 1,385 valid submissions (`fact_seller_voc_responses`), yielding an aggregate completion rate of **25.5%**, which sits comfortably above our historical internal benchmark for B2B/seller-facing instrumentation (typically targeted at 20%).
* **Sentiment Breakdown:** Across all categories, sentiment in onboarding pulses skews 42% neutral, 31% negative, and 27% positive—reflecting the natural friction inherent in setting up a new retail channel. Collectibles negative sentiment is heavily front-loaded around the authentication milestone (L1), whereas Style and Resold negative verbatims cluster primarily around listing setup tooling.

*Note on background office noise:* While wei.hartono and I were wrapping up this aggregation in BigQuery, the data engineering team has been dealing with ongoing noise regarding the migration of legacy Looker dashboards to our Compass-analog reporting environment. Also, half the Marketplace product team was out of office last Thursday for the regional Q2 offsite at the warehouse dock in Joliet, which fortunately didn't disrupt pipeline syncs. 

---
