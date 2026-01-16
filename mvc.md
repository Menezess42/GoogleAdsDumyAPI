# googleAdsDummy – Engineering Plan

Purpose: deterministic mock of Google Ads–like data for study and tooling.

---

## 1. Core Concepts
The system has four active layers:
```
Gad (API facade)
 ├─ World (state + business rules + entities)
 │    └─ owns Campaigns and temporal boundaries
 ├─ Executor (query interpreter)
 │    └─ translates AST → world interactions
 └─ Generator (metric fabricator)
      └─ produces reproducible metrics from (world + date + entity)
```
The compiler already exists and is isolated.

Only `Gad` is visible to the user.

---
## 2. Entities
- Campaign (static)
- id: str
- name: str
- status: str (ENABLED | PAUSED | REMOVED)
- budget_amount: float

CampaignMetrics (temporal)
- campaign_id: str
- date: YYYY-MM-DD

Raw:
- impressions: int
- clicks: int
- cost: float
- conversions: int
- revenue: float

Derived:
- cpa: float
- roas: float

Validation invariants:
- impressions >= 0
- clicks <= impressions
- conversions <= clicks
- cost >= 0
- revenue >= 0
- cpa = cost / conversions (0 if conversions = 0)
- roas = revenue / cost (0 if cost = 0)

---

## 3. World – Responsibilities

`World` is instantiated once by `Gad.create()`.

It owns:

- Configuration snapshot:
    - num_campaigns
    - date range
    - anomaly rules
    - weekend factor
    - seed

- Static structure:
  - campaigns
  - campaign profiles (A/B/C behavior class)

It exposes only structural and semantic queries, never metrics:
  - list_campaigns() → [campaign_id]
  - campaign_exists(id) → bool
  - get_campaign(id) → Campaign
  - is_date_valid(date) → bool
  - get_rules_snapshot() → Rules

World does not generate metrics.
World defines what exists and what is allowed.

World is pure domain state.

---

## 4. Generator – Responsibilities
Generator is stateless.

- Inputs:
    -  world snapshot
    -  campaign_id
    -  date

- Output:
    - CampaignMetrics

- Rules:
    - Same (seed, campaign_id, date) → same output
    - Uses hash-based reseeding per (campaign_id, date, seed)

    - Applies:
      - weekday vs weekend factor
      - controlled random variation
      - anomaly probability
      - campaign profile behavior

Generator knows nothing about queries or AST.

---

## 5. Executor – Responsibilities
Executor bridges:
```
AST (from compiler) → World → Generator → Result
```
Executor:
1. Receives:
    - world instance
    - parsed AST

2. Validates:
    - entities exist in world
    - dates are valid

3. Determines:
    - which campaigns
    - which date ranges
    - which metrics are requested

4. Requests metrics from Generator

5. Shapes result to match query semantics

6. Returns structured data to Gad

Executor owns query semantics, not business rules.

---

## 6. Gad – Responsibilities
Public API.

Lifecycle:
```py
gad = Gad()
gad.config(...)
gad.create()
gad.query("SELECT ...")
```
- Gad:
    - Stores configuration
    - Instantiates World on create()
    - On query():
      - calls compiler → AST
      - passes (world, AST) to Executor
      - returns result

Gad never touches Generator directly.

---

## 7. Configuration Contract

```py
seed: int | None
num_campaigns: int = 3
enable_anomalies: bool = True
weekend_factor: float = 0.7
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
```
- Guarantees:
  - Same seed + same config → same world
  - Same seed + same world + same query → same result
  - Metrics always coherent

---

## 8. Order of Implementation
1. World
  - Define structure
  - Create campaigns deterministically
  - Enforce domain rules
  - No metrics

2. Generator
  - Deterministic numeric fabricator
  - Campaign profile behavior
  - Date-based seeding

3. Executor
  - Consume AST
  - Validate against World
  - Orchestrate metric generation

4. Gad
  - Config lifecycle
  - World instantiation
  - Compiler + Executor wiring

- Only after these four are stable:
  - Tests
  - Packaging
  - Ergonomics


