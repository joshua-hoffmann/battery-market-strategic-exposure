# Limitations

This project is a public-data case study. It uses selected observable proxies and does not measure strategic exposure directly.

## Main Limitations

- Public sources may define regions inconsistently.
- China, EU, United States, and Rest of World are not perfectly symmetric units.
- Rest of World is a residual category and may hide conflicting country-level patterns.
- Lithium dependency is only one part of battery value-chain exposure.
- The project does not directly observe contract-level supply security.
- The project does not directly observe battery-grade lithium availability unless explicitly measured.
- The project does not directly observe corporate sourcing resilience.
- The project does not directly observe substitution capacity or recycling capacity.
- Policy context is documented but excluded from MVP score calculation.
- 2030 outlook data is external context only and is excluded from the 2020-2025 scorecard.
- The scorecard index is directional and descriptive.
- The analysis is not an investment recommendation, policy recommendation, forecast, geopolitical ranking, or validated risk model.

## Invalid Claim Types

Do not claim that this project:

- proves which region is most vulnerable
- predicts regional battery-market outcomes
- measures strategic exposure directly
- identifies geopolitical winners or losers
- creates an investment signal
- validates a policy recommendation
- produces a rule-based strategy
- determines the objective ranking of regions
- forecasts battery-market dominance

## Required Boundary Sentence

This project provides a scorecard-assisted descriptive judgment based on selected public indicators. It is not a forecast model, investment recommendation, policy prescription, geopolitical ranking, automatic risk score, or validated strategic exposure model.

<!-- V2.1_CRITICAL_MINERALS_LIMITATIONS_START -->

## V2.1 Limitations - Critical Minerals Concentration Tracker

### What V2.1 measures

V2.1 measures:

- mine-production concentration

It does not measure:

- refining concentration
- processing concentration
- battery-grade chemical availability
- trade dependency
- import dependency
- contracted supply
- inventory buffers
- policy risk
- company-level procurement risk

### What V2.1 does not claim

V2.1 does not claim that concentration automatically means supply-chain risk.

V2.1 does not produce:

- investment recommendation
- forecast model
- geopolitical ranking
- validated supply-chain risk model
- country risk score

The output should be interpreted as a structural concentration signal that may motivate further analysis.

### Data limitations

USGS values may be estimated, rounded, withheld, or unavailable.

Rules:

- withheld is not zero
- not_available is not zero

World total values may not exactly equal the sum of listed country values because of rounding, withheld rows, or unlisted producers.

The calculation should use the USGS world total as denominator and document material discrepancies.

### Material comparability limitation

Raw production quantities are not directly comparable across materials because units and measurement bases can differ.

Concentration metrics are comparable because they are based on within-material production shares.

### 2025 exclusion

V2.1 is scoped to 2020-2024.

If 2025 is added later, it should be treated as a separate V2.2 latest-estimate layer and clearly labeled, not silently mixed into the V2.1 historical period.

<!-- V2.1_CRITICAL_MINERALS_LIMITATIONS_END -->
