<!--
INTERNAL PROJECT GOVERNANCE RECORD
This file is retained for project-state continuity and internal workflow traceability.
It is not a public-facing README, portfolio artifact, analytical claim, or publication-ready document.
Do not use this file as external project documentation without a separate Public Surface Review.
-->

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

## 2026-06-22 — V2.2 Portfolio Case Study Added

- Added standalone V2.2 case study documentation:
  - docs/v2_2_processing_refining_concentration_case_study.md
- Purpose:
  - explain the V2.2 mining vs processing/refining concentration comparison
  - preserve the 2024 snapshot boundary
  - document the project as a portfolio-ready supply-chain analytics case
- Claim boundary preserved:
  - concentration signal only
  - no risk score
  - no investment signal
  - no geopolitical ranking
  - no forecast
  - no policy recommendation
  - no full annual refining tracker

## 2026-06-23 — V2.1 Standalone Case Study Added

- Added standalone V2.1 case-study documentation:
  - docs/v2_1_mine_production_concentration_case_study.md

- Updated README with a direct link to the V2.1 case study.

- Updated governance records:
  - PROJECT_FILE_REGISTRY.md
  - PROJECT_STATE.md

- Purpose:
  Improve GitHub viewer experience by making V2.1 easier to find as a standalone case study, matching the V2.2 documentation pattern.

## 2026-06-23 — Removed Public Portfolio-Framing Language

- Removed public-facing non-project framing language from documentation where present.
- Purpose:
  Keep GitHub documentation focused on project logic, methodology, outputs, and claim boundaries rather than non-project commentary.

## 2026-06-23 — Public Documentation Language Cleanup

- Removed non-project framing language from README and case-study documentation.
- Replaced non-project framing language with neutral project documentation language.
- Added local-only notes folder to .gitignore so non-public notes remain excluded from repository tracking.
- Cleaned public registry and snapshot references to local-only notes.


## 2026-06-23 — Removed Local Publication Planning Files From Public Tracking

- Removed local publication planning files from public repository tracking while keeping them available locally.
- Cleaned public governance references so repository documentation remains focused on project methodology, data, code, outputs, and claim boundaries.
- Updated the project audit workflow so local-only publication planning folders are not listed in public status snapshots.

## 2026-06-23 — V2.3 Phase 1–2 Downstream Concentration Evidence Tracker

- Added schema-only curated evidence input:
  - data/curated/v23_battery_grade_downstream_sources.csv

- Added V2.3 validation and processing script:
  - src/v23_downstream_concentration_evidence_tracker.py

- Added processed output schema:
  - data/processed/v23_downstream_concentration_evidence_tracker.csv

- Confirmed V2.3 processor executes successfully with zero source-backed evidence rows.
- Confirmed no unsupported numeric concentration claims were added.
- Confirmed HHI, stage-gap, and strongest-stage calculations remain blocked until source-backed comparable evidence rows are added.
- Preserved V2.1 and V2.2 behavior.
- No public documentation, charts, briefs, or README updates were created during this phase.


## 2026-06-23 — V2.3 Phase 3 First Controlled Evidence Batch

- Added first controlled source-backed curated evidence rows for:
  - lithium
  - natural_graphite
  - manganese

- Re-ran:
  - src/v23_downstream_concentration_evidence_tracker.py

- Generated processed V2.3 output with 3 rows:
  - lithium: directional-only downstream battery-grade conversion evidence
  - natural_graphite: directional-only downstream battery-grade conversion evidence
  - manganese: source-reported downstream top-1 evidence for battery-grade manganese sulphate

- Manganese downstream top-1 was populated from source-reported evidence.
- HHI, top-three, stage-gap, and strongest-stage calculations remain blocked due to insufficient comparable evidence.
- No public-facing V2.3 documentation, charts, briefs, or README updates were created.
- V2.1 and V2.2 files remain unchanged.


## 2026-06-23 — V2.3 Phase 4 Controlled Evidence Expansion

- Added source-backed directional evidence rows for cobalt and nickel.
- Cobalt row preserves IEA stage-definition evidence for final refined cobalt products including cobalt sulphate.
- Nickel row preserves IEA stage-definition evidence for nickel final products including nickel sulphate.
- Both rows remain calculation-blocked because the source does not provide safe public numeric country shares for battery-grade downstream conversion.
- Existing lithium, natural graphite, and manganese rows remain unchanged.
- HHI, top-three, stage-gap, and strongest-stage calculations remain blocked.
- No README, docs, charts, briefs, or public-facing claims were created.


## 2026-06-23 — V2.3 Public Documentation Boundary Added

- Added bounded public documentation language for V2.3.
- Clarified that V2.3 is an evidence-limited downstream concentration evidence module.
- Preserved public emphasis on completed V2.1 and V2.2 outputs.
- Did not create a V2.3 brief, chart, case study, risk score, forecast, policy claim, investment signal, or completed downstream bottleneck result.


## V2.12 to V2.16 Internal Alignment

- V2.12 recorded the stage architecture decision: upstream is V2.1, midstream is V2.4 to V2.11 and later V2.14, true downstream remains unbuilt and unclaimed.
- V2.13 recorded natural graphite product-definition traceability and retained the existing V2.4 value 99 as public-snapshot only.
- V2.14 consolidated the midstream line: lithium source-traceable, manganese proxy-limited, natural graphite product-definition-limited, cobalt/nickel low-priority precision gaps.
- V2.15 recorded project-state/file-registry alignment as the next internal governance check.
- V2.16 recorded registry/changelog alignment check before visual polish, public-surface work, or downstream expansion.

Boundary: no README polish, docs polish, public packaging, portfolio framing, investment signal, policy recommendation, geopolitical ranking, forecast, bottleneck proof, vulnerability ranking, or validated risk model was created in this alignment block.

## V2.17 to V2.41 Public Surface and Visual Upgrade Governance
- V2.17 to V2.23: public-surface preflight, scan, inspection, closeout, and post-review state recorded without modifying README, docs, or public briefs.
- V2.24 to V2.32: midstream visual upgrade planned, specified, drafted, QA-checked, refined, QA-checked again, and gated for possible future public insertion.
- V2.33 to V2.40: upstream visual review, classification, source-candidate selection, specification, draft, QA, refined visual, and public-insertion gate completed.
- V2.41: visual-upgrade block closed with both refined SVGs kept internal pending separate public-surface patch decision.
- Boundary retained: no investment signal, policy recommendation, geopolitical ranking, forecast, bottleneck proof, disruption probability, vulnerability ranking, full battery value-chain model, complete downstream layer, complete supply-chain risk model, or validated risk model.
