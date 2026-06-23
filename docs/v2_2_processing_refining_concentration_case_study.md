# Battery Minerals Bottleneck Analysis: Mining vs. Processing Concentration

## Project Summary

This case study extends a battery market strategic exposure project from upstream mine-production concentration into downstream processing and refining concentration.

The analysis asks whether the stronger concentration bottleneck appears at the mine-production stage or later in the supply chain, where raw minerals are processed or refined into battery-relevant materials.

V2.1 established a mine-production concentration baseline using USGS-only data for lithium, cobalt, nickel, natural graphite, and manganese. V2.2 adds a focused 2024 processing/refining concentration snapshot and compares downstream top-three country concentration against the V2.1 mining baseline.

The result is not a risk score or investment recommendation. It is a bounded concentration signal: a structured way to identify where supply-chain dependence appears stronger based on public-source evidence.

## Problem / Question

Battery supply-chain discussions often focus on where minerals are mined. But for strategic exposure, mining is only one stage of the value chain.

The core question for V2.2 was:

**Which battery minerals remain most concentrated after mine production, and does processing/refining concentration create a stronger bottleneck than mining concentration?**

This matters because a mineral can appear diversified at the mine-production stage while still depending heavily on a small number of countries for processing, refining, or battery-grade conversion.

## Method

### 1. V2.1 mine-production concentration baseline

V2.1 created the upstream baseline for the project.

It tracked 2020–2024 mine-production concentration for:

- lithium
- cobalt
- nickel
- natural graphite
- manganese

The V2.1 scope was intentionally narrow. It measured mine-production concentration only, including top concentration metrics and HHI where supported by the source structure. It did not create a risk score, investment signal, geopolitical ranking, forecast, or policy recommendation.

This baseline gave V2.2 a clean upstream comparison point.

### 2. V2.2 downstream processing/refining snapshot

V2.2 extended the analysis downstream by adding a 2024 processing/refining concentration snapshot.

The purpose was not to build a full historical tracker. The purpose was to test whether the strongest 2024 concentration signal appears at the mining stage or at the processing/refining stage.

The output file supporting the analysis is:

`data/processed/critical_minerals_processing_refining_snapshot.csv`

The public project brief is:

`outputs/briefs/processing_refining_concentration_snapshot_brief.md`

### 3. Top-three-share comparison

The main comparison metric is:

**processing/refining top-three country share minus mine-production top-three country share**

This produces a simple stage-comparison signal:

- positive gap: processing/refining is more concentrated than mining
- negative gap: mining is more concentrated than processing/refining
- near-zero gap: concentration is similar across stages

The analysis uses this comparison because it is transparent, interpretable, and appropriate for a bounded public-source snapshot.

### 4. Source and coverage diagnostics

The method includes source and coverage diagnostics to avoid treating the output as more precise than the evidence supports.

The analysis preserves several boundaries:

- processing/refining evidence is limited to 2024
- refining HHI is not calculated
- refining top-one share is not calculated
- manganese uses weaker battery-grade manganese sulphate proxy evidence
- processing/refining definitions may not map perfectly onto USGS mine-production categories
- country-level concentration is not the same as company-level control

This keeps the analysis bounded by separating what the data shows from what it does not show.

## Key Finding

Under the allowed 2024 top-three-share comparison, all five minerals show higher processing/refining concentration than mine-production concentration.

| Year | Mineral | Mining top-three share | Processing/refining top-three share | Processing minus mining | Higher bottleneck stage |
|---:|---|---:|---:|---:|---|
| 2024 | Lithium | 74.17% | 96.00% | 21.83 pp | Processing/refining |
| 2024 | Cobalt | 88.52% | 89.00% | 0.48 pp | Processing/refining |
| 2024 | Nickel | 76.49% | 78.00% | 1.51 pp | Processing/refining |
| 2024 | Natural graphite | 89.62% | 99.00% | 9.38 pp | Processing/refining |
| 2024 | Manganese | 74.00% | 95.00% | 21.00 pp | Processing/refining |

The strongest processing-over-mining gaps appear in:

- **lithium:** +21.83 percentage points
- **manganese:** +21.00 percentage points
- **natural graphite:** +9.38 percentage points

Cobalt and nickel also show higher downstream concentration, but the gap is much smaller:

- **cobalt:** +0.48 percentage points
- **nickel:** +1.51 percentage points

The main interpretation is that mine-production concentration alone may understate stage-level concentration for some battery minerals. For this 2024 snapshot, the downstream processing/refining stage is the higher concentration bottleneck for all five minerals in scope.

## Limitations

V2.2 is a limited 2024 snapshot, not a full annual tracker.

Refining HHI is not calculated.

Refining top-one share is not calculated.

Manganese is weaker evidence because it uses battery-grade manganese sulphate proxy evidence.

Processing/refining definitions may not exactly match USGS mine-production categories.

Country-level concentration is not company-level control.

The output is a concentration signal only. It is not a risk score, investment signal, geopolitical ranking, forecast, or policy recommendation.

