from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "processed" / "critical_minerals_concentration_metrics.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "critical_minerals_processing_refining_snapshot.csv"
BRIEF_PATH = BASE_DIR / "outputs" / "briefs" / "processing_refining_concentration_snapshot_brief.md"

TARGET_YEAR = 2024

TARGET_MINERALS = [
    "lithium",
    "cobalt",
    "nickel",
    "natural_graphite",
    "manganese",
]

CLAIM_BOUNDARY_NOTE = (
    "Concentration signal only; not a risk score, investment signal, geopolitical ranking, "
    "forecast, policy recommendation, or full annual refining tracker."
)

PROCESSING_REFINING_SNAPSHOT = {
    "lithium": {
        "processing_refining_top_3_share": 96.0,
        "processing_product_definition": "Lithium refining / processing concentration, 2024 IEA top-three refining concentration snapshot.",
        "source_name": "IEA Global Critical Minerals Outlook 2025 / Lithium",
        "source_class": "structured web table / public IEA snapshot",
        "coverage_diagnostic": (
            "IEA public snapshot supports 2024 top-three refining concentration and 2021 comparison, "
            "but this is not a full 2020-2024 annual refining country-share table. Refining HHI is not feasible."
        ),
    },
    "cobalt": {
        "processing_refining_top_3_share": 89.0,
        "processing_product_definition": "Cobalt refining concentration, 2024 IEA top-three refining concentration snapshot.",
        "source_name": "IEA Global Critical Minerals Outlook 2025 / Cobalt",
        "source_class": "structured web table / public IEA snapshot",
        "coverage_diagnostic": (
            "IEA public snapshot supports 2024 top-three refining concentration and 2021 comparison, "
            "but this is not a full 2020-2024 annual refining country-share table. Refining HHI is not feasible."
        ),
    },
    "nickel": {
        "processing_refining_top_3_share": 78.0,
        "processing_product_definition": "Nickel refining concentration, 2024 IEA top-three refining concentration snapshot.",
        "source_name": "IEA Global Critical Minerals Outlook 2025 / Nickel",
        "source_class": "structured web table / public IEA snapshot",
        "coverage_diagnostic": (
            "IEA public snapshot supports 2024 top-three refining concentration and 2021 comparison, "
            "but this is not a full 2020-2024 annual refining country-share table. Refining HHI is not feasible."
        ),
    },
    "natural_graphite": {
        "processing_refining_top_3_share": 99.0,
        "processing_product_definition": "Graphite refining / processing concentration, 2024 IEA top-three refining concentration snapshot.",
        "source_name": "IEA Global Critical Minerals Outlook 2025 / Graphite",
        "source_class": "structured web table / public IEA snapshot",
        "coverage_diagnostic": (
            "IEA public snapshot supports 2024 top-three refining concentration and 2021 comparison, "
            "but graphite processing definitions may differ from USGS mine-production categories. "
            "Refining HHI is not feasible."
        ),
    },
    "manganese": {
        "processing_refining_top_3_share": 95.0,
        "processing_product_definition": "Battery-grade manganese sulphate production concentration proxy, not a clean comparable top-three refining metric.",
        "source_name": "IEA Global Critical Minerals Outlook 2025 / battery-grade manganese sulphate discussion",
        "source_class": "report narrative / weaker manually curated public snapshot",
        "coverage_diagnostic": (
            "Weaker snapshot evidence. IEA indicates battery-grade manganese sulphate production is about "
            "95% China-dominated, but this is not a clean top-three refining concentration table and is not directly "
            "comparable to USGS manganese mine-production concentration. Treat as a definition-limited proxy. "
            "Refining HHI is not feasible."
        ),
    },
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def normalize_mineral(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def find_column(df: pd.DataFrame, candidates: list[str], label: str) -> str:
    normalized = {col.strip().lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    fail(
        f"Could not find required {label} column. "
        f"Tried: {candidates}. Available columns: {list(df.columns)}"
    )


def normalize_share_to_percent(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    if values.isna().any():
        bad_rows = series[values.isna()].tolist()
        fail(f"Top-three mining share contains non-numeric values: {bad_rows}")

    max_value = values.max()
    if max_value <= 1.0:
        return values * 100.0
    return values


def higher_bottleneck_stage(mining_top_3: float, processing_top_3: float) -> str:
    diff = processing_top_3 - mining_top_3
    if abs(diff) < 0.000001:
        return "equal_top_3_concentration"
    if diff > 0:
        return "processing_refining"
    return "mine_production"


def build_snapshot() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        fail(f"Missing input file: {INPUT_PATH}")

    if not OUTPUT_PATH.parent.exists():
        fail(f"Missing output folder: {OUTPUT_PATH.parent}")

    if not BRIEF_PATH.parent.exists():
        fail(
            f"Missing brief output folder: {BRIEF_PATH.parent}. "
            "Do not create new folders without Supervisor approval."
        )

    df = pd.read_csv(INPUT_PATH)

    year_col = find_column(df, ["year"], "year")
    mineral_col = find_column(df, ["mineral", "material"], "mineral/material")
    top3_col = find_column(
        df,
        ["top_3_share", "top3_share", "top_3_country_share", "top_3_production_share", "top_3_producer_share_pct", "top_3_producer_share"],
        "top-three mining share",
    )

    working = df.copy()
    working["_year"] = pd.to_numeric(working[year_col], errors="coerce")
    if working["_year"].isna().any():
        fail("Year column contains non-numeric values.")

    working["_mineral"] = working[mineral_col].map(normalize_mineral)
    working["_mining_top_3_share"] = normalize_share_to_percent(working[top3_col])

    subset = working[
        (working["_year"] == TARGET_YEAR)
        & (working["_mineral"].isin(TARGET_MINERALS))
    ].copy()

    missing = sorted(set(TARGET_MINERALS) - set(subset["_mineral"]))
    if missing:
        fail(f"Missing 2024 mining top-three share rows for minerals: {missing}")

    duplicate_check = subset["_mineral"].value_counts()
    duplicates = duplicate_check[duplicate_check > 1]
    if not duplicates.empty:
        fail(f"Duplicate 2024 mineral rows detected: {duplicates.to_dict()}")

    records = []
    for mineral in TARGET_MINERALS:
        mining_value = float(subset.loc[subset["_mineral"] == mineral, "_mining_top_3_share"].iloc[0])
        source = PROCESSING_REFINING_SNAPSHOT[mineral]
        processing_value = float(source["processing_refining_top_3_share"])
        diff = processing_value - mining_value

        records.append(
            {
                "year": TARGET_YEAR,
                "mineral": mineral,
                "mining_top_3_share": round(mining_value, 2),
                "processing_refining_top_3_share": round(processing_value, 2),
                "processing_minus_mining_top_3_share": round(diff, 2),
                "higher_bottleneck_stage": higher_bottleneck_stage(mining_value, processing_value),
                "processing_product_definition": source["processing_product_definition"],
                "source_name": source["source_name"],
                "source_class": source["source_class"],
                "coverage_diagnostic": source["coverage_diagnostic"],
                "hhi_feasible": "not_applicable_public_snapshot_only",
                "claim_boundary_note": CLAIM_BOUNDARY_NOTE,
            }
        )

    output = pd.DataFrame(records)
    output.to_csv(OUTPUT_PATH, index=False)

    write_brief(output, list(df.columns), year_col, mineral_col, top3_col)

    print(f"Created: {OUTPUT_PATH}")
    print(f"Created: {BRIEF_PATH}")
    print()
    print(output[[
        "year",
        "mineral",
        "mining_top_3_share",
        "processing_refining_top_3_share",
        "processing_minus_mining_top_3_share",
        "higher_bottleneck_stage",
        "hhi_feasible",
    ]].to_string(index=False))

    return output


def dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    """Return a simple GitHub-style markdown table without optional dependencies."""
    columns = list(df.columns)
    rows = df.astype(str).values.tolist()

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]

    return "\n".join([header, separator] + body)

def write_brief(output: pd.DataFrame, input_columns: list[str], year_col: str, mineral_col: str, top3_col: str) -> None:
    display = output[[
        "year",
        "mineral",
        "mining_top_3_share",
        "processing_refining_top_3_share",
        "processing_minus_mining_top_3_share",
        "higher_bottleneck_stage",
    ]].copy()

    markdown_table = dataframe_to_markdown_table(display)

    stronger_processing_count = int((output["higher_bottleneck_stage"] == "processing_refining").sum())

    brief = f"""# Battery Minerals Processing & Refining Concentration Snapshot V2.2

## Business question

Which battery minerals remain most concentrated after mine production, and does refining/processing concentration create a stronger bottleneck than mining concentration?

## Claim boundary

This output is a concentration signal only. It is not a risk score, investment signal, geopolitical ranking, forecast, policy recommendation, or full annual refining tracker.

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

{", ".join(input_columns)}

Resolved columns:

- year: `{year_col}`
- mineral: `{mineral_col}`
- mining top-three share: `{top3_col}`

## V2.2 snapshot table

{markdown_table}

## Summary signal

In this limited public-source snapshot, processing/refining concentration is higher than mine-production top-three concentration for {stronger_processing_count} of {len(output)} minerals.

This comparison supports only a narrow bottleneck-stage signal based on top-three concentration. It does not establish risk, investability, policy priority, or future supply vulnerability.

## Coverage limitations

- Refining HHI is not calculated because public source evidence does not provide complete comparable country-share tables.
- This is not a full 2020-2024 annual refining tracker.
- Lithium, cobalt, nickel, and natural graphite use public IEA top-three refining concentration snapshot evidence.
- Manganese uses weaker battery-grade manganese sulphate evidence and should be treated as a definition-limited proxy.
- Processing/refining product definitions may not match USGS mine-production categories exactly.
- Country-level concentration should not be interpreted as company-level control.
- Manual source curation creates reproducibility limits relative to the V2.1 USGS-only mine-production pipeline.

## Generated outputs

- `data/processed/critical_minerals_processing_refining_snapshot.csv`
- `outputs/briefs/processing_refining_concentration_snapshot_brief.md`
"""

    BRIEF_PATH.write_text(brief, encoding="utf-8")


if __name__ == "__main__":
    build_snapshot()

