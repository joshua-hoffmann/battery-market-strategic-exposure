# PROJECT CHANGELOG — Battery Market Strategic Exposure

## 2026-06-17

- Created Battery Market Strategic Exposure project structure.
- Added source scripts for exposure indicators and critical minerals concentration analysis.
- Generated processed datasets in data/processed.
- Generated chart outputs in outputs/charts.
- Generated strategic exposure brief in outputs/briefs.

## 2026-06-18

- Completed V2.1 Critical Minerals Mine-Production Concentration Tracker.
- V2.1 scope:
  - USGS-only mine-production concentration
  - lithium
  - cobalt
  - nickel
  - natural_graphite
  - manganese
  - 2020–2024
  - top concentration metrics
  - concentration signal only
  - no risk score
  - no investment signal
  - no geopolitical ranking
  - no forecast
- Generated V2.1 processed outputs:
  - data/processed/critical_minerals_concentration_metrics.csv
  - data/processed/critical_minerals_country_shares.csv
  - data/processed/critical_minerals_latest_ranking.csv
- Generated V2.1 chart outputs in outputs/charts.
- Updated README.md for public project presentation.

## 2026-06-22

- Completed source-feasibility review for proposed V2.2 Battery Minerals Processing & Refining Concentration module.
- Supervisor decision:
  - proceed with limited V2.2 snapshot only
  - do not proceed with full 2020–2024 annual tracker yet
- Reason:
  - public IEA evidence supports downstream concentration comparison
  - public sources do not consistently provide full annual country-level refining/processing shares required for exact HHI
- Added project governance baseline:
  - PROJECT_STATE.md
  - PROJECT_FILE_REGISTRY.md
  - PROJECT_CHANGELOG.md
  - src/project_status_audit.ps1
- Governance purpose:
  - prevent file duplication
  - preserve V2.1 outputs
  - support safe V2.2 implementation
  - enable repeatable project status audits

## V2.2 Battery Minerals Processing & Refining Concentration Snapshot

Implemented limited V2.2 snapshot comparing 2024 V2.1 mine-production top-three concentration with public IEA processing/refining snapshot evidence for lithium, cobalt, nickel, natural_graphite, and manganese.

Created:
- src/calculate_processing_refining_snapshot.py
- data/processed/critical_minerals_processing_refining_snapshot.csv
- outputs/briefs/processing_refining_concentration_snapshot_brief.md

Validated output:
- lithium: processing/refining top-three concentration exceeds mining top-three concentration by 21.83 percentage points.
- cobalt: processing/refining top-three concentration exceeds mining top-three concentration by 0.48 percentage points.
- nickel: processing/refining top-three concentration exceeds mining top-three concentration by 1.51 percentage points.
- natural_graphite: processing/refining top-three concentration exceeds mining top-three concentration by 9.38 percentage points.
- manganese: processing/refining top-three proxy exceeds mining top-three concentration by 21.00 percentage points.

Boundary:
- concentration signal only
- not a risk score
- not an investment signal
- not a geopolitical ranking
- not a forecast
- not a policy recommendation
- not a full annual refining tracker

Known limitation:
Manganese uses weaker battery-grade manganese sulphate snapshot evidence and is not a clean comparable top-three refining concentration metric. Refining HHI is not calculated for any mineral.

## 2026-06-22 — V2.2 README and Milestone Commit Preparation

- Validated V2.2 Processing & Refining Concentration Snapshot locally.
- Confirmed V2.2 output files:
  - src/calculate_processing_refining_snapshot.py
  - data/processed/critical_minerals_processing_refining_snapshot.csv
  - outputs/briefs/processing_refining_concentration_snapshot_brief.md
- Updated README.md with bounded V2.2 portfolio description.
- Preserved claim boundary:
  - concentration signal only
  - no risk score
  - no investment signal
  - no geopolitical ranking
  - no forecast
  - no full annual refining tracker
- Prepared repository for a single governance-safe V2.2 milestone commit.
