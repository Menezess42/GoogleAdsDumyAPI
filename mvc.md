# MVC - Minimum Viable Capability

## Entities and Fileds

- Campaign (base model)
    - `id` (String) - unique identifier
    - `name` (String) - campaign name
    - `status` (String) - ENABLED, PAUSED, REMOVED
    - `budget_amount` (float) - daily Budget in dollars

- CampaignMetrics (Daily Metrics)
    - `campaign_id` (String) - campaign reference
    - `date` (String) - YYYY-MM-DD format

- Raw metrics (base):
    - `impressions` (int) - ad views
    - `clicks` (int) - ad clicks
    - `cost` (float) - cost in dollars (not micros, simplified)
    - `conversions` (int) - number of conversions
    - `revenue` (float) - conversion value (conversions_value in real API)

- Calculated metrics (convenience):
    - `cpa` (float) - cost/conversions
    - `roas` (float) - revenu/cost

> Note: Real Google Ads API does NOT return calculated CPA/ROAS. We include boh for development convenience, but consumers should be aware they'd need to calculate these in the real API.
---

## Public Interface (Client)
    - The way to go is to make like googleAdsAPI where you send a search querry and
    the API sends you the information requested.
---

## Data Generation - Temporal Behavior

- Weekly Variation:
    - Monday through Friday: normal traffic (baseline)
    - Satruday/Sunday: -30% impressions (weekend)

- Controlled random variation:
    - Normal days: +-15% variation
    - Exceptional days (5% chance): +50% conversions or -40% conversions(problems)

- Campaign profiles:
    - Campaign A: high volume, low CPA (~$15-20, efficient)
    - Campaign B: medium volume, normal CPA (~$30-40)
    - Campaign C: low volume, high CPA (~$60-80, problematic for alerts)
---
# Configuration and Reproducibility

- Client should accept configuration parameters:
    ```py
    client(
            seed: int = None,
            num_campaigns: int = 3,
            enable_anomalies: bool = True,
            weekend_factor: float = 0.7
          )
    ```
- Consistency guarantees:
    - Same `seed` + same `data` + same `campaign_id` = same metrics
    - Metrics always coherent: `clicks <= impressions`, `conversions <= clicks`

- Automatic validation (Pydantic):
    - Impressions >= 0
    - Clicks >= 0 and <= impressions
    - Conversions >= 0 and <= clicks
    - Cost >= 0
    - revenue >= 0
    - CPA = Cost/ conversions (0 if converions = 0)
    - ROAS = revenue/cost (0 if cost = 0)

