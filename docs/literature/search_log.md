# Literature Search Log (CLAUDE.md §5.1)

Every search used during Phase R is logged here, so the search can be reproduced. One row per query.

Conventions:

- **Track:** A–I (§5.1), `R0` (target-definition orientation, §11), `R1` (dataset feasibility, §12–§16), or `ENV` (environment capability test, not an evidence search).
- **Tool:** `WebSearch`, `Consensus`, or another named tool or database.
- **Filters:** exactly as passed (year, study type, open access, …). `none` if no filters were used.
- **Results:** number of results returned.
- **Registered:** IDs of the `SRC-###` entries created from this query. Results that were not registered are not evidence. Search snippets are never evidence (§5.2).
- Dates are ISO-8601. Each sub-table below covers one day or one session.

## Track status

| Track | Topic | Priority | Sources registered | Status |
| --- | --- | --- | --- | --- |
| A | PPG fundamentals, morphology, reflective PPG | P0 | 0 | NOT_STARTED |
| B | Pulse detection, pulse rate, PRV, PRV–HRV agreement | P0 | 0 | NOT_STARTED |
| C | PPG-derived respiration (AM / FM / BW) | P0 | 0 | NOT_STARTED |
| D | Signal quality, motion artifact, wearable artifacts | P0 | 0 | NOT_STARTED |
| E | Sleep physiology, PPG sleep/wake and staging | P0/P1 | 0 | NOT_STARTED |
| F | PPG and SDB | P1 | 0 | NOT_STARTED |
| G | Oximetry, desaturation, scoring rules, AHI/REI | P0/P1 | 0 | NOT_STARTED |
| H | Prior-art devices and validated systems | P1 | 0 | NOT_STARTED |
| I | Wearable / real-time / embedded physiological DSP | P1 | 0 | NOT_STARTED |

Status values: `NOT_STARTED`, `IN_PROGRESS`, `SUFFICIENT` (§5 sufficiency test met), `BUDGET_REACHED`, `BLOCKED_ACCESS` (see the gap registry).

## Log

### 2026-10-01 — Step 1 (environment capability tests)

| # | Date | Track | Tool | Query string | Filters | Results | Registered | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-10-01 | ENV | WebSearch (standard) | `photoplethysmography respiratory rate estimation review Charlton` | none | 10 | none | Capability test T1 (`research_environment.md`). Not an evidence search. |
| 2 | 2026-10-01 | ENV | Consensus | `photoplethysmography derived respiratory rate estimation during sleep` | none | 10 | none | Capability test T2. Abstracts were returned; nothing was registered, because Step 1 does not do evidence collection. |
