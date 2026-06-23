# Data Sources

## Source Strategy

The initial scorecard uses a small manually curated CSV derived from public, reputationally credible sources.

Candidate source categories:

- International Energy Agency EV and battery-market publications
- U.S. Geological Survey lithium and mineral statistics
- Eurostat, if a clean EU-specific indicator is necessary
- EU policy sources, for context only

## Repository Rule

Do not include in the repository:

- large raw reports
- downloaded PDFs
- bulk Excel files
- proprietary datasets
- paid datasets
- unclear scraped datasets
- automated raw data dumps

The repository should contain a small curated input CSV with source metadata.

## Required Source Metadata

Every curated row must include:

- source_name
- source_detail
- source_year
- unit
- coverage_quality
- notes

## Source Documentation Table

| Source name | Source detail | Indicator used | Region coverage | Year coverage | Curation note | Limitation |
|---|---|---|---|---|---|---|

Rows will be added after public sources are selected.

## Source Boundary

A source may support an indicator, but it does not automatically support:

- a causal claim
- a forecast
- an investment conclusion
- a policy recommendation
- a geopolitical ranking
- a validated exposure model

## Value Type Documentation

Each curated row must document value_type using one of:

- direct_reported
- calculated_share
- residual
- mapped_proxy
- text_context

Use direct_reported when the source directly reports the value for the project region.

Use calculated_share when the project calculates a share from source values.

Use residual when the value is calculated as a remainder, for example Rest of World equals global total minus China minus EU minus United States.

Use mapped_proxy when the source does not directly match the project definition but is used as a transparent proxy.

Use text_context only for non-scoring policy_context rows.

## Region Mapping Documentation

Each curated row must document region_mapping using one of:

- direct_region
- eu_reported
- europe_used_as_proxy
- country_to_region_sum
- global_minus_selected_regions
- not_applicable

Do not silently map Europe to EU.

Do not treat Rest of World as a coherent strategic actor. It is a residual comparison group unless directly reported by the source.

## First Approved Source Families

The first source research phase should focus on:

- IEA Global EV Outlook or Global EV Data Explorer for EV battery demand and battery-market concentration indicators
- USGS Lithium and Mineral Commodity Summaries for lithium mine production or lithium supply proxy indicators
- EU or national policy sources only as excluded policy_context rows if needed

Deferred or excluded for the initial scorecard:

- UN Comtrade
- automated source fetchers
- PDF table extraction
- paid or proprietary battery databases
- large raw files in the repository

## Initial Source Research Decision

The first scorecard data version will use two primary public source families:

1. International Energy Agency
2. U.S. Geological Survey

Eurostat, UN Comtrade, automated fetchers, PDF extraction, and large raw data files are deferred or excluded from the initial scorecard.

## Approved Initial Scorecard Indicators

| indicator_name | indicator_category | source_family | unit | include_in_scorecard | first_version_scope | notes |
|---|---|---|---|---|---|---|
| ev_battery_demand_share | ev_battery_demand | IEA Global EV Outlook / Global EV Data Explorer | percent of global EV battery demand or deployment | true | latest-year first, then 2020-2025 if available | Main demand intensity proxy. |
| battery_manufacturing_capacity_share | market_concentration | IEA Global EV Outlook battery industry reporting | percent of global lithium-ion battery manufacturing capacity | true | latest-year first | Market concentration proxy. Manufacturing capacity is not the same as actual utilization. |
| lithium_mine_production_share | lithium_supply_dependency | USGS Lithium / Mineral Commodity Summaries | percent of global lithium mine production | true | latest-year first, then 2020-2025 if feasible | Lithium-related supply proxy. Does not measure battery-grade lithium access, refining, contracts, or resilience. |

## Optional Context Indicators

| indicator_name | indicator_category | source_family | include_in_scorecard | notes |
|---|---|---|---|---|
| battery_policy_support_context | policy_context | IEA policy commentary, EU or national policy sources | false | Context only. Must not enter the score calculation. |
| critical_minerals_policy_context | policy_context | EU or national policy sources | false | Context only. Must not enter the score calculation. |

## Source Selection Rules

Use IEA first for demand and manufacturing concentration indicators.

Use USGS first for lithium mine production indicators.

Use EU-specific values where available.

Do not silently treat Europe as EU.

Use Rest of World only as a residual aggregate unless directly reported by the source.

Rest of World should be documented as heterogeneous and not treated as a coherent strategic actor.

## Deferred Sources

UN Comtrade is excluded from the initial scorecard because it would require HS-code mapping, country aggregation, trade-flow interpretation, and additional data-quality logic.

Eurostat is deferred unless a specific EU-only gap appears that cannot be handled through IEA or USGS.

Automated API fetchers and PDF table extraction are excluded from the initial scorecard.

## Data Entry Gate

No values should be entered into data/curated/battery_exposure_inputs.csv until the specific source page, table, chart, or dataset location is identified for each indicator.

## Curated Value Extraction Protocol

The first scorecard CSV uses a latest-year-only comparison for 2025.

The first data-entry version should include exactly:

- 3 scoring indicators
- 4 project regions
- 12 curated rows

No 2020-2024 trend rows, 2030 rows, policy_context rows, UN Comtrade rows, Eurostat rows, forecast assumptions, or extra indicators should be added in the first scorecard version.

## Rounded IEA Value Convention

IEA values used in the first scorecard version may be reported in rounded textual form.

The project uses the following fixed convention:

| Source wording | CSV numeric convention |
|---|---|
| about X% | X |
| roughly X% | X |
| almost X% | X |
| X% | X |
| over X% | X as lower-bound rounded value |
| 6-7% | 6.5 as midpoint of reported range |

These values are used only for a descriptive scorecard. They are not precise measurements.

## IEA Rest of World Residual Rule

For IEA share indicators:

Rest of World = 100 - China - EU - United States

Rest of World is a residual aggregate. It is not directly reported as a homogeneous strategic region.

Rest of World rows using rounded IEA values should use:

- value_type = residual
- region_mapping = global_minus_selected_regions
- coverage_quality = low

## IEA 2025 Demand Indicator Rule

Indicator:

ev_battery_demand_share

Source family:

IEA Global EV Outlook 2026, Electric vehicle batteries section.

Source basis:

The source reports that EV battery deployment in 2025 was 60% in China, almost 15% in the European Union, and 10% in the United States.

CSV convention:

- China = 60
- EU = 15
- United States = 10
- Rest of World = 15

Rest of World is calculated as 100 - 60 - 15 - 10.

## IEA 2025 Manufacturing Capacity Indicator Rule

Indicator:

battery_manufacturing_capacity_share

Source family:

IEA Global EV Outlook 2026, Electric vehicle batteries section.

Source basis:

The source reports that China accounts for over 80% of global battery manufacturing capacity, while the European Union and United States account for 6-7% each.

CSV convention:

- China = 80
- EU = 6.5
- United States = 6.5
- Rest of World = 7

Rest of World is calculated as 100 - 80 - 6.5 - 6.5.

China is entered as a lower-bound rounded value because the source says over 80%.

EU and United States are entered as midpoint values because the source says 6-7% each.

## USGS Lithium Mine Production Mapping Rule

Indicator:

lithium_mine_production_share

Source family:

USGS Mineral Commodity Summaries 2026, Lithium.

Source basis:

The source provides 2025 mine production by country and a rounded world total.

The first scorecard version maps disclosed 2025 country production into the project regions.

Mapping rule:

- China = China
- EU = disclosed EU member countries in the USGS table
- United States = disclosed U.S. production if available
- Rest of World = world total minus China minus EU minus United States

For the 2025 USGS lithium table:

- China has disclosed 2025 mine production.
- Portugal has disclosed 2025 mine production and is treated as the EU row.
- U.S. production is withheld by USGS.
- World total excludes U.S. production.

## U.S. Lithium Withheld Data Rule

USGS withholds U.S. lithium mine production to avoid disclosing company proprietary data.

For the first scorecard version, the United States lithium_mine_production_share may be entered as 0 only as a disclosed-data proxy for scorecard calculation.

This does not mean U.S. lithium production is proven to be zero.

The United States lithium row must use:

- value_type = mapped_proxy
- region_mapping = country_to_region_sum
- coverage_quality = low

Required note:

U.S. mine production is withheld by USGS; entered as 0 for disclosed-data scorecard proxy, not as proof of zero production.

## USGS Lithium Share Calculation Rule

Use the following formula:

regional lithium mine production share = regional disclosed production / world total production * 100

Use the USGS rounded world total for 2025.

If the world total excludes U.S. production, this must be documented in notes.

## First Scorecard Data Entry Gate

Before running the pipeline, the curated CSV must contain only the approved 12 scoring rows.

No policy_context rows should be added yet.

No analytical conclusions should be written before validation, processed output, and charts exist.

<!-- V2.1_CRITICAL_MINERALS_DATA_SOURCES_START -->

## V2.1 Data Sources - Critical Minerals Concentration Tracker

### Purpose

V2.1 extends the original battery exposure scorecard with a separate concentration tracker for critical battery minerals.

V2.1 question:

Which battery minerals show the highest and most persistent supply concentration, and has concentration improved or worsened over time?

### Primary source

V2.1 uses USGS Mineral Commodity Summaries 2025 Data Releases as the primary source for mine-production concentration analysis.

Target materials:

- lithium
- cobalt
- nickel
- natural_graphite
- manganese

Target period:

- 2020
- 2021
- 2022
- 2023
- 2024

The project treats USGS world production data as the source basis for country-level production shares.

### Source boundary

V2.1 is USGS-only for the core concentration calculation.

IEA Critical Minerals data may be reviewed for bounded processing/refining concentration context where source coverage supports the stated comparison, but it is not part of the V2.1 USGS-only mine-production calculation layer.

### Canonical material naming

The project uses the following canonical material names:

- lithium
- cobalt
- nickel
- natural_graphite
- manganese

USGS source-release naming should be preserved separately in the source_release column.

Example:

- material = natural_graphite
- source_release = Mineral Commodity Summaries 2025 - GRAPHITE (NATURAL) Data Release

### Curated input file

The V2.1 curated input contract is:

data/curated/critical_minerals_production_inputs.csv

Required columns:

- year
- material
- country
- production_value
- unit
- source_name
- source_release
- source_year
- source_detail
- value_status
- is_world_total
- include_in_concentration_calc
- data_quality_flag
- notes

### Data-entry rule

Do not treat missing, withheld, or unavailable values as zero.

Allowed value_status examples:

- reported
- estimated
- withheld
- not_available
- rounded

Rows with withheld or not_available values should not be included in concentration calculations unless a later documented methodology change explicitly allows it.

<!-- V2.1_CRITICAL_MINERALS_DATA_SOURCES_END -->


## V2.3 Source Coverage Boundary

V2.3 source coverage is incomplete across downstream stages. Source references are included only where they support the stated downstream evidence, and missing numeric coverage is preserved as a limitation rather than estimated or inferred. V2.3 remains evidence-limited and is not treated as a completed public case study.
