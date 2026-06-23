# V2.1 Case Study — Critical Minerals Mine-Production Concentration Tracker

## Project Context

Battery Market Strategic Exposure analyzes supply concentration patterns in selected battery-related critical minerals.

V2.1 establishes the upstream baseline: observed mine-production concentration.

This baseline matters because a downstream bottleneck comparison only makes sense after the mining-stage concentration picture is clear.

## Business Question

Which battery minerals show the highest and most persistent mine-production concentration, and has concentration improved or worsened over time?

## Scope

V2.1 covers five battery-related critical minerals:

- Lithium
- Cobalt
- Nickel
- Natural graphite
- Manganese

The analysis uses a USGS-only mine-production dataset covering 2020 to 2024.

## What V2.1 Measures

V2.1 measures country-level mine-production concentration.

The core signals are:

- producer share by country
- largest producer share
- top-three producer share
- Herfindahl-Hirschman Index, or HHI
- share coverage validation

The purpose is to convert raw mine-production data into decision-ready concentration signals.

## Key 2024 Output

| Rank | Material | Top Producer | Top 3 Share (%) | HHI |
|---:|---|---|---:|---:|
| 1 | Natural graphite | China | 89.625 | 6380.866 |
| 2 | Cobalt | Congo (Kinshasa) | 88.517 | 5871.850 |
| 3 | Nickel | Indonesia | 76.486 | 3771.872 |
| 4 | Lithium | Australia | 74.167 | 2215.265 |
| 5 | Manganese | South Africa | 74.000 | 2200.027 |

## Interpretation

The 2024 ranking shows natural graphite and cobalt with the highest observed mine-production concentration among the selected minerals.

Nickel also shows elevated concentration, while lithium and manganese are lower in the selected group but still have top-three producer shares above 70%.

The key point is not that these values are risk scores.

The key point is that mine production is already concentrated enough to justify a structured upstream baseline before moving into downstream processing and refining comparisons.

## Methodology

The V2.1 pipeline starts from curated USGS-only mine-production inputs.

For each material, year, and producing country, the pipeline calculates producer share:

    Producer share = Country mine production / Reported world mine production

The largest producer share identifies the largest producer in each material-year.

The top-three producer share sums the shares of the three largest producers:

    Top-three share = Share of producer 1 + share of producer 2 + share of producer 3

HHI squares and sums producer shares across the producer base:

    HHI = sum of squared producer shares

A higher HHI indicates more concentrated observed mine production.

The pipeline also includes share coverage validation to check whether calculated country shares align with reported world totals before the outputs are interpreted.

## Pipeline Files

### Source Scripts

    src/calculate_critical_minerals_concentration.py
    src/create_critical_minerals_charts.py

### Curated Input

    data/curated/critical_minerals_production_inputs.csv

### Processed Outputs

    data/processed/critical_minerals_country_shares.csv
    data/processed/critical_minerals_concentration_metrics.csv
    data/processed/critical_minerals_latest_ranking.csv

### Chart Outputs

    outputs/charts/critical_minerals_2024_hhi_ranking.png
    outputs/charts/critical_minerals_top3_share_trend.png
    outputs/charts/critical_minerals_2024_top1_top3_comparison.png
    outputs/charts/critical_minerals_share_coverage_diagnostic.png

## Visual Outputs

The main README visual outputs are:

1. 2024 HHI ranking by material
2. Top-three producer share trend over time
3. 2024 comparison of largest-producer share and top-three share

The share coverage diagnostic chart is retained as a method and audit output rather than as a main portfolio visual.

## Claim Boundary

This project measures observed USGS mine-production concentration only.

It is not:

- a risk score
- an investment signal
- a geopolitical ranking
- a forecast
- a full supply-chain risk model

The results show where mine production is concentrated by country, but they do not independently measure:

- trade flows
- refining capacity
- reserves
- substitution potential
- inventory buffers
- company exposure
- political stability
- pricing power
- downstream battery supply-chain resilience

Concentration is therefore treated as a decision-relevant supply-structure signal, not as a complete measure of mineral supply risk.

## Link to V2.2

V2.1 establishes the upstream mine-production baseline.

V2.2 extends this baseline by comparing mine-production concentration with processing/refining concentration.

The follow-up question is:

    Which battery minerals remain most concentrated after mine production, and does processing/refining concentration create a stronger bottleneck than mining concentration?

V2.2 is documented separately in:

    docs/v2_2_processing_refining_concentration_case_study.md

## Portfolio Relevance

V2.1 demonstrates how a focused public-data pipeline can turn raw production data into a clear business analytics signal.

The project shows:

- curated data preparation
- country-level production share calculation
- concentration metric design
- diagnostic validation before interpretation
- visual communication of supply concentration
- explicit claim boundaries

This makes the case study relevant for roles involving finance, business analytics, supply-chain analysis, market research, and Python-based decision support.
