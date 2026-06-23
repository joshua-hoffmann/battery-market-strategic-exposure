# Methodology

## Purpose

This document defines the methodology for the Battery Market Strategic Exposure project.

The project uses selected public-data indicators to compare regional exposure to battery value-chain pressure from 2020 to 2025.

## Analytical Form

The permitted analytical form is:

descriptive scorecard interpretation

The project does not support:

- rule-based strategy
- investment model
- forecast model
- policy recommendation model
- geopolitical ranking
- validated exposure model
- automatic risk score

## Working Definition

Strategic exposure means a region's observable exposure to battery value-chain pressure based on selected public-data proxies for:

- demand intensity
- lithium-related dependency
- market concentration

Exposure does not automatically mean weakness. High demand can reflect market strength as well as pressure. Concentration can indicate strategic importance, dependency, or pressure, but it does not prove vulnerability.

## Regions

The initial scorecard uses four regional groups:

- China
- EU
- United States
- Rest of World

Rest of World is a residual comparison group, not a coherent strategic actor.

## Time Period

The scorecard covers:

- 2020
- 2021
- 2022
- 2023
- 2024
- 2025

2030 may be used only as external outlook context and must be excluded from score calculation.

## Indicator Categories

Allowed curated indicator categories:

- ev_battery_demand
- lithium_supply_dependency
- market_concentration
- policy_context

For the initial scorecard, policy_context rows are documented but excluded from score calculation.

## Curated Input Schema

The curated input file is:

data/curated/battery_exposure_inputs.csv

Required columns:

- year
- region
- indicator_name
- indicator_category
- value
- unit
- source_name
- source_detail
- source_year
- is_outlook_context
- include_in_scorecard
- coverage_quality
- notes

## Scorecard Inclusion Logic

The scorecard calculation may use only rows where:

- 2020 <= year <= 2025
- include_in_scorecard = true
- is_outlook_context = false
- indicator_category is not policy_context

Rows from 2030 or later must not enter the scorecard.

## Processed Output Schema

The processed output will be:

data/processed/battery_exposure_indicators.csv

Planned columns:

- year
- region
- demand_intensity_score
- lithium_dependency_score
- market_concentration_score
- scorecard_exposure_index
- observed_pressure_label
- data_completeness_flag
- evidence_quality_flag
- included_indicator_count
- excluded_policy_context_count
- method_notes

## Scorecard Exposure Index

The scorecard_exposure_index is a descriptive summary index, not a validated exposure model.

It should be interpreted together with:

- component scores
- observed pressure labels
- evidence quality flags
- data completeness flags
- limitations

## Observed Pressure Labels

The initial scorecard uses descriptive labels:

- 0-33: lower_observed_pressure
- 34-66: moderate_observed_pressure
- 67-100: higher_observed_pressure
- missing: insufficient_evidence

These are not risk ratings.

## Missing Data

Missing data must not be silently imputed. If a region-year lacks an indicator category, this must be reflected in the completeness flag and method notes.

## Additional Data Contract Fields

The curated input schema includes two provenance fields to prevent silent mapping or transformation drift.

### value_type

Allowed values:

- direct_reported
- calculated_share
- residual
- mapped_proxy
- text_context

Purpose:

This field explains whether the value is directly reported by the source, calculated from source values, derived as a residual, mapped as a proxy, or included only as text context.

### region_mapping

Allowed values:

- direct_region
- eu_reported
- europe_used_as_proxy
- country_to_region_sum
- global_minus_selected_regions
- not_applicable

Purpose:

This field explains how the source geography was mapped into the project regions.

Europe must not be silently treated as EU. If Europe is used as an EU proxy, this must be marked as europe_used_as_proxy and explained in notes.

Rest of World should usually be treated as a residual aggregate and marked as global_minus_selected_regions unless the source directly reports it.

## Final Curated Input Header

The final curated input header is:

year,region,indicator_name,indicator_category,value,unit,value_type,source_name,source_detail,source_year,is_outlook_context,include_in_scorecard,coverage_quality,region_mapping,notes

<!-- V2.1_CRITICAL_MINERALS_METHODOLOGY_START -->

## V2.1 Methodology - Critical Minerals Concentration Tracker

### Analytical form

V2.1 is a descriptive concentration tracker.

It does not create an investment recommendation, a forecast model, a geopolitical ranking, or a validated supply-chain risk model.

Analytical form:

- descriptive scorecard interpretation

Core signal:

- observed supply concentration metric

Not:

- risk score

### Unit discipline

Production quantities may use different units across different materials.

The project may compare concentration metrics across materials because Top-1 share, Top-3 share, and HHI are dimensionless.

The project must not compare raw production quantities across materials unless units and measurement bases are explicitly comparable.

### Producer share

For each material-year-country row:

producer_share = production_value / world_total_production

world_total_production comes from the USGS world total row for the same material and year.

### Top-1 producer share

top_1_producer_share = max(producer_share)

Also record:

top_1_producer = country with highest producer_share

### Top-3 producer share

top_3_producer_share = sum(producer_share for the three largest producer countries)

If fewer than three valid producer rows exist for a material-year, the data quality flag should be lowered and the limitation should be documented.

### HHI concentration index

V2.1 uses the 0-10000 HHI convention:

hhi_concentration_index = sum((producer_share * 100)^2)

Examples:

- If one country has 100 percent share, HHI = 10000.
- If four countries each have 25 percent share, HHI = 2500.

### YoY change in Top-3 share

yoy_change_top3_share_pp = top_3_producer_share_current_year - top_3_producer_share_previous_year

Example:

0.72 - 0.69 = 0.03 = plus 3 percentage points

The first year, 2020, has no prior-year comparison and should remain blank for YoY change.

### Latest-year material ranking

For V2.1, the latest year is expected to be 2024.

Ranking rule:

- Primary rank: hhi_concentration_index descending
- Secondary reference: top_3_producer_share descending

This is a concentration ranking, not a geopolitical or investment ranking.

### Validation checks required before processed outputs

Input schema must include all required columns.

Allowed materials:

- lithium
- cobalt
- nickel
- natural_graphite
- manganese

Allowed V2.1 years:

- 2020
- 2021
- 2022
- 2023
- 2024

For each material-year, exactly one world total row should exist:

- is_world_total = true
- include_in_concentration_calc = false

Producer rows should use:

- is_world_total = false
- include_in_concentration_calc = true

Rows with withheld or unavailable values should use:

- include_in_concentration_calc = false

Share-sum checks should flag material-years where included producer shares differ materially from the USGS world total.

<!-- V2.1_CRITICAL_MINERALS_METHODOLOGY_END -->

