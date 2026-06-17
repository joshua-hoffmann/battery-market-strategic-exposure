# Methodology

## Purpose

This document defines the methodology for the Battery Market Strategic Exposure Case Study.

The project uses selected public-data indicators to compare regional exposure to battery value-chain pressure from 2020 to 2025.

## Decision Form

The permitted decision form is:

scorecard-assisted descriptive judgment

The project does not support:

- rule-based strategy
- investment model
- forecast model
- policy recommendation model
- geopolitical ranking
- validated strategic exposure model
- automatic risk score

## Working Definition

Strategic exposure means a region's observable exposure to battery value-chain pressure based on selected public-data proxies for:

- demand intensity
- lithium-related dependency
- market concentration

Exposure does not automatically mean weakness. High demand can reflect market strength as well as pressure. Concentration can indicate strategic importance, dependency, or pressure, but it does not prove vulnerability.

## Regions

The MVP uses four regional groups:

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

For the MVP, policy_context rows are documented but excluded from score calculation.

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

The MVP uses descriptive labels:

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
