# googleAdsDummy – Engineering Plan

Purpose: deterministic mock of Google Ads–like data for study and tooling.

---

## 1. System Topology

```
Gad (public API)
 ├─ World (domain state)
 │    └─ owns campaigns, profiles, date boundaries, rules
 ├─ Executor (query engine)
 │    └─ AST → world lookups → generator calls → result shaping
 └─ Generator (stateless fabricator)
      └─ (world, campaign_id, date) → CampaignMetrics
```


- Compiler already exists and is isolated.
- Only `Gad` is visible to the user.

---

## 2. Domain Entities

### Campaign (static, created by World)

```py
id: str
name: str
budget_amount: float
```

### CampaignMetrics (temporal, produced by Generator)
```py
campaign_id: str
date: YYYY-MM-DD

impressions: int
clicks: int
cost: float
conversions: int

cpa: float # derived
```

### Validation Invariants
```py
impressions >= 0
clicks <= impressions
conversions <= clicks
cost >= 0
revenue >= 0
cpa = cost / conversions (0 if conversions = 0)
roas = revenue / cost (0 if cost = 0)
```

---

## 3. User Configuration Contract (gad.config)

All of this is user input.

```py
seed: int | None
num_campaigns: int
weekend_factor: float # 0.0 – 1.0

date_period: {
"start_date": YYYY-MM-DD,
"end_date": YYYY-MM-DD
}

anomaly_rules: {
"enabled": bool,
"probability": float, # 0.0 – 1.0
"effects": {
"spike_conversions": float, # e.g. +0.50 -- 0.0 - 1.0
"drop_conversions": float # e.g. -0.40 -- 0.0 - 1
}
}

profile_rules: {
"allowed_profiles": list[str], # ["A", "B", "C"]
"ensure_at_least_one": list[str], # ["A", "C"]
"distribution": dict[str, float] | None
# e.g. {"A": 0.2, "B": 0.5, "C": 0.3}
}
```

Guarantees:
```
same seed + same config → same world
same world + same query → same result
```

---

## 4. World – Domain State

World is instantiated once by `Gad.create(config)`.

World stores verbatim:
```
seed
num_campaigns
weekend_factor
date_period
anomaly_rules
profile_rules
```

World resolves at creation time:

```py
campaigns: dict[campaign_id, Campaign]
campaign_profiles: dict[campaign_id, ProfileType] # "A" | "B" | "C"
```

Profile resolution rules:
- Only values in `allowed_profiles` may be used.
- For each value in `ensure_at_least_one`, at least one campaign must receive it.
- Remaining campaigns are assigned using `distribution`
  (or uniform if None).

World exposes only structure and validity:
```py
list_campaigns() -> list[str]
campaign_exists(id) -> bool
get_campaign(id) -> Campaign
is_date_valid(date) -> bool
get_rules_snapshot() -> Rules
```

World never generates metrics.

---

## 5. Generator – Metric Fabricator

Generator is stateless.

Input:
```py
(world, campaign_id, date)
```

Output:
```py
CampaignMetrics
```

Rules:
```py
same (seed, campaign_id, date) → same output
```

Mechanics:
- reseed using hash(seed, campaign_id, date)
- apply:
  - weekday vs weekend factor
  - controlled random variation
  - anomaly_rules
  - campaign profile behavior

Generator knows nothing about AST or queries.

---

## 6. Executor – Query Engine

Executor bridges:
```
AST → World → Generator → Result
```

Executor responsibilities:
1. Receive `(world, ast)`
2. Validate:
   - entities exist in world
   - dates are valid
3. Resolve:
   - which campaigns
   - which dates
   - which metrics
4. Request metrics from Generator
5. Shape output according to query semantics
6. Return structured result

Executor owns query semantics, not business rules.

---

## 7. Gad – Public API

Lifecycle:
```Py
gad = Gad()
gad.config(...)
gad.create()
gad.query("SELECT ...")
```

Responsibilities:
- store configuration
- instantiate World on `create()`
- on `query()`:
  - parse → AST
  - call Executor(world, AST)
  - return result

Gad never calls Generator directly.

---

## 8. Order of Implementation

1. World
   - configuration ingestion
   - campaign creation
   - profile assignment
   - domain validation

2. Generator
   - deterministic numeric engine
   - profile behavior
   - anomaly handling

3. Executor
   - AST interpretation
   - world validation
   - metric orchestration

4. Gad
   - lifecycle
   - wiring
   - public API

Only after these are stable:
- tests
- packaging
- ergonomics

---
# 9. Query Handling

## Level 0 Queries

Level 0 queries operate exclusively over **static domain entities**.  
They do not involve time, metrics generation, aggregation, or any form of temporal interpretation.

They are evaluated directly over the data created by the `World` and are therefore:
- Deterministic
- Stateless
- Side-effect free

### What Level 0 Queries Can Access
- `campaign.id`
- `campaign.name`
- `campaign.budget_amount`

### Supported Query Types

- Full listing  
  `select * from campaign`

- Field projection  
  `select campaign.id from campaign`  
  `select campaign.id, campaign.name from campaign`

- Equality filters  
  `where campaign.id = ...`  
  `where campaign.name = ...`  
  `where campaign.budget_amount = ...`

- Numeric comparisons  
  `where campaign.budget_amount > ...`  
  `where campaign.budget_amount >= ...`  
  `where campaign.budget_amount < ...`

- Set membership  
  `where campaign.id in (...)`  
  `where campaign.name in (...)`

- Ordering  
  `order by campaign.name`  
  `order by campaign.budget_amount desc`

- Result limiting  
  `limit N`

- Combined clauses  
  Filters, ordering, and limits may be combined in a single query.

### Explicitly Out of Scope for Level 0

- Any reference to `metrics`
- Any reference to dates or time ranges
- Aggregations (`sum`, `avg`, `count`, etc.)
- Derived fields
- Cross-entity relations or joins

Level 0 defines the **minimal and stable query surface** of the gadAPI.  
More expressive queries are intentionally deferred to higher levels.




