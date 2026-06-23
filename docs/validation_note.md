# Validation Note

## Status

The first latest-year scorecard pipeline run has passed validation.

The project currently contains a manually curated 2025 scorecard input, a processed scorecard output, and two generated charts.

## Validated Inputs

Curated input file:

data/curated/battery_exposure_inputs.csv

The curated input contains:

- 3 scoring indicators
- 4 project regions
- 12 curated rows
- 2025 only
- no 2030 rows
- no policy_context rows
- no trend rows

## Validated Processed Output

Processed output file:

data/processed/battery_exposure_indicators.csv

The processed output contains:

- 4 rows
- one row per project region
- year 2025 only
- complete data_completeness_flag for all regions
- observed_pressure_label for all regions
- evidence_quality_flag for all regions

## Generated Charts

Generated chart files:

- outputs/charts/exposure_score_by_region.png
- outputs/charts/exposure_components_2025.png

The trend chart is intentionally postponed because the current input contains only one scorecard year.

The following file should not exist yet:

outputs/charts/exposure_trend_2020_2025.png

## Method Validation

The scorecard uses three component scores:

- demand_intensity_score
- lithium_dependency_score
- market_concentration_score

The scorecard_exposure_index is calculated as an equal-weight descriptive average of the available component scores.

The lithium_dependency_score is inverted from lithium mine production share. This means lower disclosed lithium mine production share creates higher observed lithium dependency pressure in the scorecard.

## Interpretation Boundaries

This output supports only a descriptive scorecard interpretation.

It is not:

- a forecast model
- an investment recommendation
- a policy prescription
- a geopolitical ranking
- an automatic risk score
- a validated exposure model

The current scorecard is latest-year only. It should not be described as a 2020-2025 trend analysis until multi-year data rows are added.

## Data Caveats

IEA values used in the scorecard are rounded textual values and are entered using a fixed rounding convention.

Rest of World is a residual aggregate and not a coherent strategic actor.

USGS lithium mine production is country-based. U.S. production is withheld by USGS, so the United States lithium row is a disclosed-data proxy and not proof of zero production.

## Validation Result

PASS.

The project is ready for a short public brief based on the latest-year scorecard outputs, with strict caveats.

