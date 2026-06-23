# PROJECT STATE — Battery Market Strategic Exposure

## Purpose

This file is the project-local source of truth for the current state of the Battery Market Strategic Exposure project.

Before creating new folders, files, scripts, data outputs, documentation artifacts, or V2 modules, check this file first.

## Project Root

C:\Users\joshu\battery-market-strategic-exposure

## Strategic Project Goal

Build a portfolio-grade battery minerals and supply-chain analytics project that demonstrates:

- public-source data analysis
- concentration measurement
- supply-chain bottleneck reasoning
- evidence-bounded strategic interpretation
- reproducible Python outputs
- clear claim boundaries

The project should support employer-facing proof of capability in:

Finance + Commodities + Python + Strategic Supply Chain Analytics.

## Existing Top-Level Structure

battery-market-strategic-exposure/
│
├── .git/
├── .venv/
├── data/
│   └── processed/
├── docs/
├── outputs/
│   ├── briefs/
│   └── charts/
├── private_learning/
├── src/
├── .gitignore
├── README.md
└── requirements.txt

## Existing Source Scripts

src/calculate_critical_minerals_concentration.py
- Calculates V2.1 critical minerals mine-production concentration metrics.

src/calculate_exposure_indicators.py
- Calculates earlier battery exposure indicators.

src/create_charts.py
- Creates earlier project charts.

src/create_critical_minerals_charts.py
- Creates V2.1 critical minerals concentration charts.

src/run_pipeline.py
- Runs the project pipeline.

## Existing Processed Data

data/processed/battery_exposure_indicators.csv
data/processed/critical_minerals_concentration_metrics.csv
data/processed/critical_minerals_country_shares.csv
data/processed/critical_minerals_latest_ranking.csv

## Existing Outputs

outputs/briefs/strategic_exposure_brief.md
outputs/charts/critical_minerals_2024_hhi.*
outputs/charts/critical_minerals_2024_top3_share.*
outputs/charts/critical_minerals_share_concentration.*
outputs/charts/critical_minerals_top3_share.*
outputs/charts/exposure_components_2025.png
outputs/charts/exposure_score_by_region.png

## Current Completed Work

V2.1 Critical Minerals Mine-Production Concentration Tracker is complete.

Current V2.1 scope:
- USGS-only mine-production concentration
- lithium
- cobalt
- nickel
- natural_graphite
- manganese
- 2020–2024
- concentration metrics only
- no risk score
- no investment signal
- no geopolitical ranking
- no forecast

## Current Proposed Next Module

V2.2 Battery Minerals Processing & Refining Concentration Snapshot

Supervisor decision:
Proceed only as a limited public-source snapshot, not a full 2020–2024 annual tracker.

Reason:
Public IEA evidence supports downstream concentration comparison, especially top-three concentration, but does not consistently provide full annual country-level shares required for exact HHI.

## V2.2 Claim Boundary

Allowed:
- concentration signal
- mining vs processing/refining comparison
- public-source snapshot comparison
- source-class and coverage diagnostics

Not allowed:
- risk score
- investment signal
- geopolitical ranking
- forecast
- policy recommendation
- full annual tracker claim unless full annual structured data is later verified

## V2.2 Governance Rule

Before implementing V2.2:
1. Preserve V2.1 outputs.
2. Do not overwrite existing processed files unless intentionally regenerating V2.1.
3. Prefer new V2.2-specific filenames over ambiguous generic files.
4. Use source diagnostics for IEA/public-source limitations.
5. Update PROJECT_FILE_REGISTRY.md when new important files are created.
6. Update PROJECT_CHANGELOG.md after the V2.2 milestone.
7. Update README.md only after V2.2 outputs are validated.

## Current Recommended Next Step

Route to Financial Data Pipeline Engineer for limited V2.2 snapshot implementation planning and execution.

Implementation must remain bounded to:
- top-three concentration comparison where public evidence supports it
- explicit source-class diagnostics
- no HHI unless full country shares are available
- no full 2020–2024 annual claim

## LinkedIn Publishing Workflow Status

As of 2026-06-23, a project-local LinkedIn publishing workflow has been added under:

outputs/linkedin/

Current sequence:

1. V2.1 Mine-Production Concentration Baseline — posted
2. V2.2 Processing & Refining Concentration Snapshot — prepared as follow-up

The V2.1 LinkedIn post establishes the upstream mine-production concentration baseline.

V2.1 post:
https://www.linkedin.com/feed/update/urn:li:ugcPost:7474976109584101377/

The V2.2 follow-up should be posted after a short delay, using the V2.1 post as context.

## V2.2 LinkedIn Follow-Up Preparation

As of 2026-06-23, V2.2 LinkedIn follow-up preparation has been completed under:

outputs/linkedin/v2_2_processing_refining_followup/

Prepared files include:

- final caption draft
- first-comment text
- final posting checklist
- engagement guide
- asset location check

V2.2 should be posted in the target window:

2026-06-25 to 2026-06-27

The V2.2 post should explicitly build on the published V2.1 upstream baseline post:

https://www.linkedin.com/feed/update/urn:li:ugcPost:7474976109584101377/

## V2.1 Standalone Case Study Documentation

As of 2026-06-23, V2.1 has a standalone GitHub case-study document:

docs/v2_1_mine_production_concentration_case_study.md

Purpose:

- make V2.1 easier to find from the GitHub viewer perspective
- mirror the V2.2 case-study documentation structure
- clarify that V2.1 is the upstream mine-production concentration baseline
- preserve the V2.1 claim boundary separately from the README

V2.1 remains the upstream baseline for the V2.2 processing/refining comparison.
