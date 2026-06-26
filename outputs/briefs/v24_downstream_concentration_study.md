# V2.4 Battery Minerals Downstream Concentration Study

## Analytical boundary

This study is a bounded descriptive concentration comparison. It compares mine-production top-three concentration with processing/refining top-three concentration evidence for selected battery minerals.

It is not a forecast model, investment recommendation, policy recommendation, geopolitical ranking, bottleneck proof, vulnerability ranking, or complete supply-chain risk model.

## Study question

Where does selected public evidence indicate higher concentration: mining or processing/refining?

## Source layer

This V2.4 study uses the existing project file:

- data/processed/critical_minerals_processing_refining_snapshot.csv

The generated V2.4 comparison table is:

- data/processed/v24_downstream_concentration_comparison.csv

No new external values are introduced in this step.

## Comparison table

| Mineral | Mining top-three share | Processing/refining top-three share | Gap | Gap class | Evidence class |
|---|---:|---:|---:|---|---|
| lithium | 74.17% | 96.0% | +21.83 pp | large_processing_refining_gap | public_snapshot_top_three_comparison |
| manganese | 74.0% | 95.0% | +21.0 pp | large_processing_refining_gap | definition_limited_proxy |
| natural_graphite | 89.62% | 99.0% | +9.38 pp | moderate_processing_refining_gap | public_snapshot_top_three_comparison |
| nickel | 76.49% | 78.0% | +1.51 pp | small_processing_refining_gap | public_snapshot_top_three_comparison |
| cobalt | 88.52% | 89.0% | +0.48 pp | small_processing_refining_gap | public_snapshot_top_three_comparison |

## Reading the output

The current comparison table contains 5 minerals. In this snapshot, processing/refining concentration is higher than mine-production concentration for all minerals in scope.

Large processing/refining gaps appear in:

- lithium: +21.83 percentage points.
- manganese: +21.0 percentage points.

A moderate processing/refining gap appears in:

- natural_graphite: +9.38 percentage points.

Small processing/refining gaps appear in:

- nickel: +1.51 percentage points.
- cobalt: +0.48 percentage points.

The largest observed gaps are descriptive concentration gaps only. They should not be read as direct evidence of supply disruption, policy priority, market power, investment relevance, or strategic vulnerability.

## Evidence and comparability notes

### lithium

- Processing product definition: Lithium refining / processing concentration, 2024 IEA top-three refining concentration snapshot.
- Source layer: IEA Global Critical Minerals Outlook 2025 / Lithium
- Coverage diagnostic: IEA public snapshot supports 2024 top-three refining concentration and 2021 comparison, but this is not a full 2020-2024 annual refining country-share table. Refining HHI is not feasible.
- Comparability note: Mining top-three and processing/refining top-three values are compared as bounded public-source concentration snapshot evidence.

### manganese

- Processing product definition: Battery-grade manganese sulphate production concentration proxy, not a clean comparable top-three refining metric.
- Source layer: IEA Global Critical Minerals Outlook 2025 / battery-grade manganese sulphate discussion
- Coverage diagnostic: Weaker snapshot evidence. IEA indicates battery-grade manganese sulphate production is about 95% China-dominated, but this is not a clean top-three refining concentration table and is not directly comparable to USGS manganese mine-production concentration. Treat as a definition-limited proxy. Refining HHI is not feasible.
- Comparability note: Manganese uses battery-grade manganese sulphate production evidence and should be treated as a definition-limited proxy, not as a clean comparable top-three refining metric.

### natural_graphite

- Processing product definition: Graphite refining / processing concentration, 2024 IEA top-three refining concentration snapshot.
- Source layer: IEA Global Critical Minerals Outlook 2025 / Graphite
- Coverage diagnostic: IEA public snapshot supports 2024 top-three refining concentration and 2021 comparison, but graphite processing definitions may differ from USGS mine-production categories. Refining HHI is not feasible.
- Comparability note: Graphite processing definitions may differ from USGS mine-production categories; compare as bounded public-source concentration evidence.

### nickel

- Processing product definition: Nickel refining concentration, 2024 IEA top-three refining concentration snapshot.
- Source layer: IEA Global Critical Minerals Outlook 2025 / Nickel
- Coverage diagnostic: IEA public snapshot supports 2024 top-three refining concentration and 2021 comparison, but this is not a full 2020-2024 annual refining country-share table. Refining HHI is not feasible.
- Comparability note: Mining top-three and processing/refining top-three values are compared as bounded public-source concentration snapshot evidence.

### cobalt

- Processing product definition: Cobalt refining concentration, 2024 IEA top-three refining concentration snapshot.
- Source layer: IEA Global Critical Minerals Outlook 2025 / Cobalt
- Coverage diagnostic: IEA public snapshot supports 2024 top-three refining concentration and 2021 comparison, but this is not a full 2020-2024 annual refining country-share table. Refining HHI is not feasible.
- Comparability note: Mining top-three and processing/refining top-three values are compared as bounded public-source concentration snapshot evidence.

## Limitations

- The comparison uses top-three concentration shares only.
- Processing/refining HHI is not calculated from complete country-share tables.
- Manganese is definition-limited because the available evidence refers to battery-grade manganese sulphate production rather than a clean comparable top-three refining table.
- Natural graphite processing definitions may not perfectly match USGS mine-production categories.
- The study does not infer company-level control, contract access, stockpile availability, substitution capacity, recycling capacity, or disruption probability.
- The study does not rank countries, regions, companies, or minerals by strategic vulnerability.

## Source gaps for future enrichment

Future work can strengthen this study by adding source-backed country-share tables for processing/refining where public evidence supports comparable values.

Priority gaps:

- complete processing/refining country-share tables where available;
- consistent product definitions across mine production and refining stages;
- clearer battery-grade downstream conversion evidence;
- year-consistent comparison across 2020-2024 only if comparable annual data is available.

## Interpretation

The V2.4 result supports a bounded observation: in the current public-source snapshot, processing/refining concentration is higher than mine-production concentration for the selected battery minerals. This is a concentration-pattern finding, not a complete supply-chain risk conclusion.
