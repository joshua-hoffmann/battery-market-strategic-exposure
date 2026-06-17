# Battery Market Strategic Exposure Case Study

## Overview

This project is a Python-supported business analytics case study that evaluates regional strategic exposure in the global battery value chain using selected public-data indicators.

It compares China, the European Union, the United States, and Rest of World using a compact scorecard based on:

- EV battery demand / deployment
- lithium mine production dependency proxy
- battery manufacturing capacity concentration

The project builds on the author's academic interest in battery-market structure and translates that topic into a compact public-data analytics case study.

## Business Question

How did regional exposure to battery value-chain pressure differ across China, the EU, the United States, and the Rest of World, based on selected public indicators for demand intensity, lithium dependency, and market concentration?

## Decision Form

This project provides a scorecard-assisted descriptive judgment based on selected public indicators.

It is not:

- a forecast model
- an investment recommendation
- a policy prescription
- a geopolitical ranking
- an automatic risk score
- a validated strategic exposure model

## Current Status

The current version is a latest-year MVP using 2025 data only.

Validated outputs currently include:

- processed scorecard output
- two generated charts
- validation note
- strategic exposure brief

The project does not yet include a 2020-2025 trend analysis. The trend chart is intentionally postponed until consistent multi-year data exists.

## Repository Structure

battery-market-strategic-exposure/

- data/
  - curated/
    - battery_exposure_inputs.csv
  - processed/
    - battery_exposure_indicators.csv
- docs/
  - data_sources.md
  - limitations.md
  - methodology.md
  - validation_note.md
- outputs/
  - briefs/
    - strategic_exposure_brief.md
  - charts/
    - exposure_components_2025.png
    - exposure_score_by_region.png
- src/
  - calculate_exposure_indicators.py
  - create_charts.py
  - run_pipeline.py
- .gitignore
- README.md
- requirements.txt

## Data Contract

The curated input file is:

    data/curated/battery_exposure_inputs.csv

Current schema:

    year,region,indicator_name,indicator_category,value,unit,value_type,source_name,source_detail,source_year,is_outlook_context,include_in_scorecard,coverage_quality,region_mapping,notes

The first validated MVP input contains:

- 3 scoring indicators
- 4 project regions
- 12 curated rows
- 2025 only
- no policy_context rows
- no 2030 rows
- no trend rows

## Source Basis

The MVP uses public sources from:

- International Energy Agency, Global EV Outlook 2026
- U.S. Geological Survey, Mineral Commodity Summaries 2026, Lithium

The source rules and caveats are documented in:

- docs/data_sources.md
- docs/validation_note.md

## Methodology Summary

The pipeline validates the curated CSV, normalizes indicator values by year and category, and calculates three component scores:

- demand_intensity_score
- lithium_dependency_score
- market_concentration_score

The final scorecard_exposure_index is an equal-weight descriptive average of the available component scores.

The lithium dependency component is inverted from lithium mine production share. Lower disclosed lithium mine production share therefore creates higher observed lithium dependency pressure in the scorecard.

## Current MVP Results

| Region | Demand | Lithium dependency | Market concentration | Exposure index | Label | Evidence |
|---|---:|---:|---:|---:|---|---|
| China | 100.0 | 72.7 | 100.0 | 90.9 | higher_observed_pressure | medium |
| EU | 10.0 | 99.9 | 0.0 | 36.6 | moderate_observed_pressure | medium |
| United States | 0.0 | 100.0 | 0.0 | 33.3 | moderate_observed_pressure | low |
| Rest of World | 10.0 | 0.0 | 0.7 | 3.6 | lower_observed_pressure | low |

These values are directional scorecard outputs, not precise measurements of strategic exposure.

## Charts

Current generated charts:

- outputs/charts/exposure_score_by_region.png
- outputs/charts/exposure_components_2025.png

The trend chart is intentionally postponed because the current MVP contains only one scorecard year.

## How to Run

Create or use the project virtual environment, install requirements, then run:

    .\.venv\Scripts\python.exe src\run_pipeline.py

This generates:

- data/processed/battery_exposure_indicators.csv
- outputs/charts/exposure_score_by_region.png
- outputs/charts/exposure_components_2025.png

## Key Limitations

The scorecard uses selected observable proxies. It does not measure strategic exposure directly.

High exposure does not automatically mean weakness. A high score may reflect market size, industrial scale, or concentration as well as pressure.

IEA values used in the MVP are rounded textual values entered using a fixed rounding convention.

USGS lithium mine production is country-based. U.S. production is withheld by USGS, so the U.S. lithium row is a disclosed-data proxy and not proof of zero production.

Rest of World is a residual aggregate and should not be interpreted as a coherent strategic actor.

The current MVP is latest-year only and should not be described as a 2020-2025 trend analysis.

## Strategic Brief

The management-oriented brief is available at:

    outputs/briefs/strategic_exposure_brief.md

## AI-Assisted Workflow

AI tools were used to support documentation structure, wording review, implementation drafting, debugging, and claim-discipline checks.

Data selection, source review, indicator design, interpretation, validation, and final responsibility remain with the author.

The project does not use proprietary data, proprietary forecasting, automated investment recommendations, or AI-generated evidence.

## Portfolio Relevance

This project demonstrates:

- public-data curation
- Python-based validation and processing
- scorecard-assisted business analytics
- transparent limitations
- management-oriented communication
- strategic finance and business analytics reasoning

It complements company-level finance analytics projects by adding an industry and value-chain exposure perspective.
