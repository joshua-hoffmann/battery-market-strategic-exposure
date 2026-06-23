# Battery Minerals Processing & Refining Concentration Snapshot V2.2

## Business question

Which battery minerals remain most concentrated after mine production, and where is processing/refining top-three concentration higher than mining top-three concentration?

## Claim boundary

This output is a bounded concentration comparison only. It is not a risk score, investment signal, geopolitical ranking, forecast, policy recommendation, bottleneck proof, or full annual refining tracker.

## Source and method

Mining concentration uses the 2024 `top_3_share` from the existing V2.1 processed file:

`data/processed/critical_minerals_concentration_metrics.csv`

Processing/refining concentration uses manually curated public IEA snapshot evidence from the feasibility review:

- lithium: IEA reports top-three refining concentration of 96% in 2024 and 99% in 2021.
- cobalt: IEA reports top-three refining concentration of 89% in 2024 and 82% in 2021.
- nickel: IEA reports top-three refining concentration of 78% in 2024 and 66% in 2021.
- natural_graphite: IEA reports top-three refining concentration of 99% in 2024 and 100% in 2021.
- manganese: IEA reports battery-grade manganese sulphate production is about 95% China-dominated, but this is weaker snapshot evidence and not a clean comparable top-three annual refining metric.

## Input schema inspected

Available input columns:

year, material, top_1_producer, top_1_producer_share, top_1_producer_share_pct, top_3_producers, top_3_producer_share, top_3_producer_share_pct, hhi_concentration_index, producer_count, active_producer_count, world_total_production, unit, sum_producer_share, sum_producer_share_pct, share_coverage_flag, yoy_change_top3_share, yoy_change_top3_share_pp, has_other_countries_aggregate, has_source_reported_zero_rows, has_concentrate_labeled_rows, has_estimated_values, has_rounded_values, data_caveat_note

Resolved columns:

- year: `year`
- mineral: `material`
- mining top-three share: `top_3_producer_share_pct`

## V2.2 snapshot table

| year | mineral | mining_top_3_share | processing_refining_top_3_share | processing_minus_mining_top_3_share | higher_top_three_concentration_stage |
| --- | --- | --- | --- | --- | --- |
| 2024 | lithium | 74.17 | 96.0 | 21.83 | processing_refining |
| 2024 | cobalt | 88.52 | 89.0 | 0.48 | processing_refining |
| 2024 | nickel | 76.49 | 78.0 | 1.51 | processing_refining |
| 2024 | natural_graphite | 89.62 | 99.0 | 9.38 | processing_refining |
| 2024 | manganese | 74.0 | 95.0 | 21.0 | processing_refining |

## Summary

In this limited public-source snapshot, processing/refining concentration is higher than mine-production top-three concentration for 5 of 5 minerals.

This comparison supports only a stage-level concentration comparison based on top-three concentration. The percentage-point gap is an arithmetic difference between concentration shares. It does not establish risk, investment relevance, policy priority, bottleneck proof, market power, disruption probability, or future supply outcomes.

## Coverage limitations

- Refining HHI is not calculated because public source evidence does not provide complete comparable country-share tables.
- This is not a full 2020-2024 annual refining tracker.
- Lithium, cobalt, nickel, and natural graphite use public IEA top-three refining concentration snapshot evidence.
- Manganese uses weaker battery-grade manganese sulphate evidence and should be treated as a definition-limited proxy.
- Processing/refining product definitions may not match USGS mine-production categories exactly.
- Country-level concentration should not be interpreted as company-level control.
- Manual source curation creates reproducibility limits compared with the V2.1 USGS-only mine-production pipeline.

## Generated outputs

- `data/processed/critical_minerals_processing_refining_snapshot.csv`
- `outputs/briefs/processing_refining_concentration_snapshot_brief.md`
