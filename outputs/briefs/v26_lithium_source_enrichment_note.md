# V2.6 Lithium Source Enrichment Note

## Purpose

This note starts the lithium-specific enrichment path identified in V2.5.

V2.5 marked lithium as high priority because V2.4 shows a large processing/refining concentration gap and because clearer country-share or source-table evidence would improve traceability.

## Input

- data/curated/v25_source_gap_enrichment_plan.csv
- data/processed/v24_downstream_concentration_comparison.csv

## Output

- data/curated/v26_lithium_processing_refining_source_candidates.csv

## Candidate source logic

The first candidate source family is IEA because the current project evidence layer already uses IEA Global Critical Minerals Outlook 2025 for the lithium processing/refining snapshot.

The second candidate is the IEA Critical Minerals Data Explorer, which should be tested for structured or downloadable data before any manual value extraction is expanded.

The IEA Critical Minerals topic page is useful as context, but it should not be used as a lithium-specific numeric source unless it exposes a lithium-specific table or explicit statement.

USGS remains relevant for the mining baseline only. It should not be used as refining evidence unless a refining-specific table is identified.

## Acceptance criteria

A lithium processing/refining source should only be accepted for numeric enrichment if it identifies:

- year;
- geography;
- stage;
- product definition;
- denominator;
- country or producer share basis;
- table, chart, dataset, or explicit source statement.

If those fields are not available, the source may be retained as context but should not be converted into a comparable concentration value.

## Claim boundary

This is a source-candidate artifact. It does not add a new lithium concentration value.

Allowed claim type after this step:

- source candidate identified;
- extraction path clarified;
- lithium enrichment priority preserved;
- no change to the V2.4 result yet.

Still blocked:

- investment signal;
- policy recommendation;
- geopolitical ranking;
- bottleneck proof;
- disruption probability;
- company-level control;
- vulnerability ranking;
- complete supply-chain risk conclusion.

## Next extraction step

The next work block should inspect the IEA Global Critical Minerals Outlook 2025 and the IEA Critical Minerals Data Explorer for lithium-specific processing/refining evidence.

Only source-backed values with clear metadata should be added to the project.
