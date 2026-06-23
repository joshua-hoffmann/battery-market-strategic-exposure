from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

CURATED_INPUT_PATH = BASE_DIR / "data" / "curated" / "v23_battery_grade_downstream_sources.csv"
PROCESSED_OUTPUT_PATH = BASE_DIR / "data" / "processed" / "v23_downstream_concentration_evidence_tracker.csv"

VERSION = "V2.3"

MINERALS = {
    "lithium",
    "cobalt",
    "nickel",
    "natural_graphite",
    "manganese",
}

STAGES = {
    "mining",
    "processing_refining",
    "battery_grade_conversion",
}

RAW_COLUMNS = [
    "version",
    "mineral",
    "stage",
    "year",
    "country",
    "country_rank",
    "share_percent",
    "volume",
    "unit",
    "denominator_type",
    "metric_basis",
    "aggregation_level",
    "material_form",
    "battery_grade_flag",
    "battery_grade_definition",
    "geography_basis",
    "comparison_year_basis",
    "source_name",
    "source_year",
    "source_reference",
    "source_table_or_chart",
    "source_confidence",
    "evidence_tier",
    "missingness_status",
    "extraction_method",
    "calculation_allowed",
    "calculation_block_reason",
    "notes",
]

PROCESSED_COLUMNS = [
    "version",
    "mineral",
    "year",
    "mining_denominator_type",
    "mining_metric_basis",
    "mining_top1_share_percent",
    "mining_top3_share_percent",
    "mining_hhi",
    "mining_hhi_valid",
    "mining_evidence_tier",
    "mining_source_confidence",
    "processing_denominator_type",
    "processing_metric_basis",
    "processing_top1_share_percent",
    "processing_top3_share_percent",
    "processing_hhi",
    "processing_hhi_valid",
    "processing_evidence_tier",
    "processing_source_confidence",
    "downstream_material_form",
    "downstream_denominator_type",
    "downstream_metric_basis",
    "downstream_battery_grade_flag",
    "downstream_top1_share_percent",
    "downstream_top3_share_percent",
    "downstream_hhi",
    "downstream_hhi_valid",
    "downstream_evidence_tier",
    "downstream_source_confidence",
    "mining_to_processing_gap_pp",
    "processing_to_downstream_gap_pp",
    "mining_to_downstream_gap_pp",
    "mining_processing_comparability_status",
    "processing_downstream_comparability_status",
    "mining_downstream_comparability_status",
    "overall_comparability_status",
    "strongest_observable_concentration_stage",
    "strongest_stage_basis",
    "missingness_status",
    "calculation_status",
    "calculation_notes",
    "primary_source_summary",
    "public_summary",
]

ALLOWED_VALUES = {
    "mineral": MINERALS,
    "stage": STAGES,
    "denominator_type": {
        "mine_production",
        "refined_production",
        "processed_production",
        "battery_grade_chemical_production",
        "battery_grade_material_production",
        "battery_grade_conversion_capacity",
        "battery_material_capacity",
        "source_reported_top1_share",
        "source_reported_top3_share",
        "qualitative_directional",
        "not_observed",
        "not_applicable",
        "mixed_or_unclear",
    },
    "metric_basis": {
        "production",
        "capacity",
        "source_reported_share",
        "qualitative",
        "mixed",
        "not_applicable",
    },
    "aggregation_level": {
        "country",
        "top1",
        "top3",
        "regional",
        "global_aggregate",
        "qualitative",
    },
    "material_form": {
        "lithium_mine_output",
        "lithium_refined_chemical",
        "battery_grade_lithium_carbonate",
        "battery_grade_lithium_hydroxide",
        "cobalt_mine_output",
        "refined_cobalt",
        "cobalt_sulphate",
        "battery_grade_cobalt_chemical",
        "nickel_mine_output",
        "refined_nickel",
        "nickel_sulphate",
        "battery_grade_nickel_chemical",
        "natural_graphite_mine_output",
        "processed_graphite",
        "spherical_purified_graphite",
        "coated_spherical_graphite",
        "anode_grade_graphite",
        "manganese_mine_output",
        "refined_manganese",
        "high_purity_manganese_sulphate",
        "battery_grade_manganese_sulphate",
        "unknown",
        "not_applicable",
    },
    "battery_grade_flag": {
        "yes",
        "no",
        "partial",
        "unclear",
    },
    "geography_basis": {
        "production_location",
        "facility_location",
        "company_headquarters",
        "ownership_control",
        "unclear",
        "not_applicable",
    },
    "comparison_year_basis": {
        "same_year",
        "nearest_available_year",
        "source_snapshot_year",
        "multi_year_estimate",
        "unclear",
    },
    "source_confidence": {
        "high",
        "medium",
        "low",
    },
    "evidence_tier": {
        "tier_1",
        "tier_2",
        "tier_3",
        "tier_4",
    },
    "missingness_status": {
        "available",
        "source_reported_only",
        "directional_only",
        "not_publicly_observed",
        "not_comparable",
        "not_applicable",
    },
    "extraction_method": {
        "downloaded_table",
        "manual_table_entry",
        "source_reported_top1",
        "source_reported_top3",
        "chart_read",
        "text_statement",
        "derived_from_volume",
    },
    "calculation_allowed": {
        "true",
        "false",
    },
}

BATTERY_GRADE_FORMS = {
    "battery_grade_lithium_carbonate",
    "battery_grade_lithium_hydroxide",
    "cobalt_sulphate",
    "battery_grade_cobalt_chemical",
    "nickel_sulphate",
    "battery_grade_nickel_chemical",
    "spherical_purified_graphite",
    "coated_spherical_graphite",
    "anode_grade_graphite",
    "high_purity_manganese_sulphate",
    "battery_grade_manganese_sulphate",
}

GENERIC_REFINING_FORMS = {
    "lithium_refined_chemical",
    "refined_cobalt",
    "refined_nickel",
    "processed_graphite",
    "refined_manganese",
}

COMPARABLE_DENOMINATORS = {
    ("mine_production", "refined_production"),
    ("mine_production", "processed_production"),
    ("refined_production", "battery_grade_chemical_production"),
    ("processed_production", "battery_grade_material_production"),
    ("mine_production", "battery_grade_chemical_production"),
    ("mine_production", "battery_grade_material_production"),
}


def fail(message: str) -> None:
    raise ValueError(f"V2.3 validation failed: {message}")


def normalize_text(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize_bool(value: Any) -> str:
    text = normalize_text(value).lower()
    if text in {"true", "1", "yes"}:
        return "true"
    if text in {"false", "0", "no", ""}:
        return "false"
    return text


def load_curated_input() -> pd.DataFrame:
    if not CURATED_INPUT_PATH.exists():
        fail(f"Required curated input file not found: {CURATED_INPUT_PATH}")

    df = pd.read_csv(CURATED_INPUT_PATH, dtype=str, keep_default_na=False)

    missing_columns = [column for column in RAW_COLUMNS if column not in df.columns]
    if missing_columns:
        fail(f"Missing required curated input columns: {missing_columns}")

    extra_columns = [column for column in df.columns if column not in RAW_COLUMNS]
    if extra_columns:
        fail(f"Unexpected curated input columns found: {extra_columns}")

    df = df[RAW_COLUMNS].copy()

    for column in RAW_COLUMNS:
        df[column] = df[column].map(normalize_text)

    df["calculation_allowed"] = df["calculation_allowed"].map(normalize_bool)

    return df


def validate_controlled_fields(df: pd.DataFrame) -> None:
    if df.empty:
        return

    for column, allowed in ALLOWED_VALUES.items():
        unknown_values = sorted(
            {
                value
                for value in df[column].dropna().astype(str).str.strip()
                if value != "" and value not in allowed
            }
        )
        if unknown_values:
            fail(f"Column '{column}' contains unsupported values: {unknown_values}")


def validate_numeric_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for column in ["year", "country_rank", "share_percent", "volume", "source_year"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df.empty:
        return df

    invalid_share_rows = df[
        df["share_percent"].notna()
        & ((df["share_percent"] < 0) | (df["share_percent"] > 100))
    ]
    if not invalid_share_rows.empty:
        fail("share_percent must be between 0 and 100 where provided.")

    invalid_year_rows = df[df["year"].notna() & (df["year"] < 1900)]
    if not invalid_year_rows.empty:
        fail("year must be 1900 or later where provided.")

    invalid_source_year_rows = df[df["source_year"].notna() & (df["source_year"] < 1900)]
    if not invalid_source_year_rows.empty:
        fail("source_year must be 1900 or later where provided.")

    return df


def validate_required_row_content(df: pd.DataFrame) -> None:
    if df.empty:
        return

    required_non_blank = [
        "version",
        "mineral",
        "stage",
        "denominator_type",
        "metric_basis",
        "aggregation_level",
        "material_form",
        "battery_grade_flag",
        "geography_basis",
        "comparison_year_basis",
        "source_name",
        "source_reference",
        "source_confidence",
        "evidence_tier",
        "missingness_status",
        "extraction_method",
        "calculation_allowed",
    ]

    for column in required_non_blank:
        blank_count = (df[column].astype(str).str.strip() == "").sum()
        if blank_count:
            fail(f"Column '{column}' has {blank_count} blank value(s).")

    invalid_version_count = (df["version"] != VERSION).sum()
    if invalid_version_count:
        fail(f"All rows must use version '{VERSION}'.")


def validate_battery_grade_rules(df: pd.DataFrame) -> None:
    if df.empty:
        return

    downstream = df[df["stage"] == "battery_grade_conversion"].copy()
    if downstream.empty:
        return

    numeric_downstream = downstream[
        (downstream["share_percent"].notna())
        | (downstream["volume"].notna())
        | (downstream["calculation_allowed"] == "true")
    ]

    invalid_flag = numeric_downstream[
        numeric_downstream["battery_grade_flag"].isin({"no", "unclear"})
    ]
    if not invalid_flag.empty:
        fail(
            "Battery-grade downstream numeric/calculable rows cannot use "
            "battery_grade_flag 'no' or 'unclear'."
        )

    generic_calculable = downstream[
        downstream["material_form"].isin(GENERIC_REFINING_FORMS)
        & (downstream["calculation_allowed"] == "true")
    ]
    if not generic_calculable.empty:
        fail(
            "Generic refining material forms cannot be calculated as "
            "battery_grade_conversion unless explicitly reclassified with an approved "
            "battery-grade material_form."
        )

    unsupported_forms = downstream[
        (downstream["calculation_allowed"] == "true")
        & (~downstream["material_form"].isin(BATTERY_GRADE_FORMS))
    ]
    if not unsupported_forms.empty:
        fail("Calculable battery_grade_conversion rows must use approved battery-grade material forms.")


def validate_calculation_flags(df: pd.DataFrame) -> None:
    if df.empty:
        return

    calculable = df[df["calculation_allowed"] == "true"].copy()
    if calculable.empty:
        return

    missing_source = calculable[
        (calculable["source_name"].astype(str).str.strip() == "")
        | (calculable["source_reference"].astype(str).str.strip() == "")
    ]
    if not missing_source.empty:
        fail("Rows with calculation_allowed=true must include source_name and source_reference.")

    missing_metric = calculable[
        calculable["metric_basis"].isin({"qualitative", "mixed", "not_applicable"})
    ]
    if not missing_metric.empty:
        fail("Rows with calculation_allowed=true cannot use qualitative, mixed, or not_applicable metric_basis.")

    missing_denominator = calculable[
        calculable["denominator_type"].isin(
            {"qualitative_directional", "not_observed", "not_applicable", "mixed_or_unclear"}
        )
    ]
    if not missing_denominator.empty:
        fail("Rows with calculation_allowed=true must use a calculable denominator_type.")

    no_numeric_value = calculable[
        calculable["share_percent"].isna()
        & calculable["volume"].isna()
        & ~calculable["aggregation_level"].isin({"top1", "top3"})
    ]
    if not no_numeric_value.empty:
        fail("Rows with calculation_allowed=true must provide share_percent, volume, or source-reported top1/top3 evidence.")


def validate_top3_vs_top1(df: pd.DataFrame) -> None:
    if df.empty:
        return

    for (mineral, stage, year), group in df.groupby(["mineral", "stage", "year"], dropna=False):
        top1_values = group.loc[group["aggregation_level"] == "top1", "share_percent"].dropna()
        top3_values = group.loc[group["aggregation_level"] == "top3", "share_percent"].dropna()

        if not top1_values.empty and not top3_values.empty:
            if top3_values.max() < top1_values.max():
                fail(
                    f"top3 share is lower than top1 share for "
                    f"mineral={mineral}, stage={stage}, year={year}."
                )


def validate_curated_input(df: pd.DataFrame) -> pd.DataFrame:
    validate_controlled_fields(df)
    df = validate_numeric_fields(df)
    validate_required_row_content(df)
    validate_battery_grade_rules(df)
    validate_calculation_flags(df)
    validate_top3_vs_top1(df)
    return df


def rank_confidence(values: pd.Series) -> str:
    ordered = ["high", "medium", "low"]
    present = [value for value in ordered if value in set(values.dropna().astype(str))]
    return present[0] if present else ""


def rank_evidence_tier(values: pd.Series) -> str:
    ordered = ["tier_1", "tier_2", "tier_3", "tier_4"]
    present = [value for value in ordered if value in set(values.dropna().astype(str))]
    return present[0] if present else ""


def joined_unique(values: pd.Series) -> str:
    clean = sorted({normalize_text(value) for value in values if normalize_text(value)})
    return "; ".join(clean)


def hhi_from_country_rows(group: pd.DataFrame) -> tuple[float | None, bool]:
    country_rows = group[
        (group["aggregation_level"] == "country")
        & (group["share_percent"].notna())
        & (group["calculation_allowed"] == "true")
    ].copy()

    if country_rows.empty:
        return None, False

    denominator_count = country_rows["denominator_type"].nunique(dropna=True)
    metric_count = country_rows["metric_basis"].nunique(dropna=True)

    if denominator_count != 1 or metric_count != 1:
        return None, False

    share_sum = country_rows["share_percent"].sum()

    if share_sum < 98 or share_sum > 102:
        return None, False

    hhi = float((country_rows["share_percent"] ** 2).sum())
    return round(hhi, 2), True


def top1_from_group(group: pd.DataFrame) -> float | None:
    country_rows = group[
        (group["aggregation_level"] == "country")
        & (group["share_percent"].notna())
        & (group["calculation_allowed"] == "true")
    ]

    if not country_rows.empty:
        return round(float(country_rows["share_percent"].max()), 2)

    source_top1 = group[
        (group["aggregation_level"] == "top1")
        & (group["share_percent"].notna())
        & (group["calculation_allowed"] == "true")
    ]

    if not source_top1.empty:
        return round(float(source_top1["share_percent"].max()), 2)

    return None


def top3_from_group(group: pd.DataFrame) -> float | None:
    country_rows = group[
        (group["aggregation_level"] == "country")
        & (group["share_percent"].notna())
        & (group["calculation_allowed"] == "true")
    ].copy()

    if len(country_rows) >= 3:
        top3 = country_rows.sort_values("share_percent", ascending=False).head(3)
        return round(float(top3["share_percent"].sum()), 2)

    source_top3 = group[
        (group["aggregation_level"] == "top3")
        & (group["share_percent"].notna())
        & (group["calculation_allowed"] == "true")
    ]

    if not source_top3.empty:
        return round(float(source_top3["share_percent"].max()), 2)

    return None


def representative_value(group: pd.DataFrame, column: str) -> str:
    if group.empty:
        return ""

    non_blank = [normalize_text(value) for value in group[column] if normalize_text(value)]
    if not non_blank:
        return ""

    counts = pd.Series(non_blank).value_counts()
    return str(counts.index[0])


def stage_stats(stage_group: pd.DataFrame) -> dict[str, Any]:
    if stage_group.empty:
        return {
            "denominator_type": "",
            "metric_basis": "",
            "material_form": "",
            "battery_grade_flag": "",
            "top1": None,
            "top3": None,
            "hhi": None,
            "hhi_valid": False,
            "evidence_tier": "",
            "source_confidence": "",
            "missingness_status": "not_publicly_observed",
            "source_summary": "",
            "geography_basis": "",
            "comparison_year_basis": "",
        }

    hhi, hhi_valid = hhi_from_country_rows(stage_group)

    return {
        "denominator_type": representative_value(stage_group, "denominator_type"),
        "metric_basis": representative_value(stage_group, "metric_basis"),
        "material_form": representative_value(stage_group, "material_form"),
        "battery_grade_flag": representative_value(stage_group, "battery_grade_flag"),
        "top1": top1_from_group(stage_group),
        "top3": top3_from_group(stage_group),
        "hhi": hhi,
        "hhi_valid": hhi_valid,
        "evidence_tier": rank_evidence_tier(stage_group["evidence_tier"]),
        "source_confidence": rank_confidence(stage_group["source_confidence"]),
        "missingness_status": representative_value(stage_group, "missingness_status"),
        "source_summary": joined_unique(stage_group["source_name"]),
        "geography_basis": representative_value(stage_group, "geography_basis"),
        "comparison_year_basis": representative_value(stage_group, "comparison_year_basis"),
    }


def compare_stages(left: dict[str, Any], right: dict[str, Any], includes_downstream: bool = False) -> str:
    if left["top3"] is None or right["top3"] is None:
        return "insufficient_evidence"

    if includes_downstream and right["battery_grade_flag"] in {"no", "unclear", ""}:
        return "not_comparable"

    if includes_downstream and right["material_form"] in GENERIC_REFINING_FORMS:
        return "not_comparable"

    if left["metric_basis"] == "capacity" and right["metric_basis"] == "production":
        return "partially_comparable"

    if left["metric_basis"] == "production" and right["metric_basis"] == "capacity":
        return "partially_comparable"

    if left["metric_basis"] != right["metric_basis"]:
        return "not_comparable"

    if left["denominator_type"] in {"mixed_or_unclear", "not_observed", "not_applicable", ""}:
        return "not_comparable"

    if right["denominator_type"] in {"mixed_or_unclear", "not_observed", "not_applicable", ""}:
        return "not_comparable"

    denominator_pair = (left["denominator_type"], right["denominator_type"])
    if denominator_pair not in COMPARABLE_DENOMINATORS:
        return "partially_comparable"

    if left["geography_basis"] != right["geography_basis"]:
        if {left["geography_basis"], right["geography_basis"]} <= {"production_location", "facility_location"}:
            return "partially_comparable"
        return "not_comparable"

    if left["comparison_year_basis"] != right["comparison_year_basis"]:
        return "partially_comparable"

    if "low" in {left["source_confidence"], right["source_confidence"]}:
        return "partially_comparable"

    return "comparable"


def gap_if_comparable(left_top3: float | None, right_top3: float | None, status: str) -> float | None:
    if status != "comparable":
        return None

    if left_top3 is None or right_top3 is None:
        return None

    return round(float(right_top3 - left_top3), 2)


def overall_status(statuses: list[str]) -> str:
    if all(status == "comparable" for status in statuses):
        return "comparable"
    if any(status == "not_comparable" for status in statuses):
        return "not_comparable"
    if any(status == "partially_comparable" for status in statuses):
        return "partially_comparable"
    return "insufficient_evidence"


def row_missingness(stats: list[dict[str, Any]]) -> str:
    statuses = {item["missingness_status"] for item in stats if item["missingness_status"]}

    if not statuses:
        return "not_publicly_observed"

    if "available" in statuses:
        if len(statuses) == 1:
            return "available"
        return "not_comparable"

    if "source_reported_only" in statuses:
        return "source_reported_only"

    if "directional_only" in statuses:
        return "directional_only"

    if "not_comparable" in statuses:
        return "not_comparable"

    if "not_applicable" in statuses:
        return "not_applicable"

    return "not_publicly_observed"


def strongest_stage(
    mining: dict[str, Any],
    processing: dict[str, Any],
    downstream: dict[str, Any],
    status_mp: str,
    status_pd: str,
    status_md: str,
) -> tuple[str, str]:
    if status_mp == status_pd == status_md == "comparable":
        stage_values = {
            "mining": mining["top3"],
            "processing_refining": processing["top3"],
            "battery_grade_conversion": downstream["top3"],
        }

        if all(value is not None for value in stage_values.values()):
            max_value = max(stage_values.values())
            winners = [stage for stage, value in stage_values.items() if value == max_value]
            if len(winners) == 1:
                return winners[0], "top3_comparable"
            return "tie", "top3_comparable"

    comparable_hhi = {
        "mining": mining["hhi"] if mining["hhi_valid"] else None,
        "processing_refining": processing["hhi"] if processing["hhi_valid"] else None,
        "battery_grade_conversion": downstream["hhi"] if downstream["hhi_valid"] else None,
    }
    hhi_values = {stage: value for stage, value in comparable_hhi.items() if value is not None}

    if len(hhi_values) >= 2 and status_mp == status_pd == status_md == "comparable":
        max_value = max(hhi_values.values())
        winners = [stage for stage, value in hhi_values.items() if value == max_value]
        if len(winners) == 1:
            return winners[0], "hhi_comparable"
        return "tie", "hhi_comparable"

    if "not_comparable" in {status_mp, status_pd, status_md}:
        return "not_comparable", "not_comparable"

    if "partially_comparable" in {status_mp, status_pd, status_md}:
        return "unclear", "directional_evidence"

    return "unclear", "insufficient_evidence"


def calculation_status(row: dict[str, Any]) -> str:
    numeric_fields = [
        "mining_top1_share_percent",
        "mining_top3_share_percent",
        "processing_top1_share_percent",
        "processing_top3_share_percent",
        "downstream_top1_share_percent",
        "downstream_top3_share_percent",
    ]
    numeric_count = sum(pd.notna(row.get(field)) and row.get(field) != "" for field in numeric_fields)

    if numeric_count == 0:
        return "blocked"

    if row["overall_comparability_status"] == "comparable":
        return "calculated"

    if row["overall_comparability_status"] == "partially_comparable":
        return "partially_calculated"

    return "directional_only"


def public_summary_for_row(row: dict[str, Any]) -> str:
    mineral = row["mineral"]
    status = row["overall_comparability_status"]
    stage = row["strongest_observable_concentration_stage"]

    if row["calculation_status"] == "blocked":
        return (
            f"For {mineral}, V2.3 does not yet have enough source-backed public evidence "
            "to calculate comparable concentration metrics across mining, processing/refining, "
            "and battery-grade conversion."
        )

    if status == "comparable" and stage not in {"unclear", "not_comparable"}:
        return (
            f"For {mineral}, the strongest observable concentration evidence in V2.3 appears "
            f"at the {stage} stage, based on comparable public concentration metrics."
        )

    return (
        f"For {mineral}, V2.3 preserves public concentration evidence but does not treat the "
        "available stage data as fully comparable."
    )


def process(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=PROCESSED_COLUMNS)

    rows: list[dict[str, Any]] = []

    calculable_or_observed = df[
        (df["year"].notna())
        & (df["mineral"].isin(MINERALS))
        & (df["stage"].isin(STAGES))
    ].copy()

    if calculable_or_observed.empty:
        return pd.DataFrame(columns=PROCESSED_COLUMNS)

    for (mineral, year), group in calculable_or_observed.groupby(["mineral", "year"], dropna=False):
        mining = stage_stats(group[group["stage"] == "mining"])
        processing = stage_stats(group[group["stage"] == "processing_refining"])
        downstream = stage_stats(group[group["stage"] == "battery_grade_conversion"])

        status_mp = compare_stages(mining, processing, includes_downstream=False)
        status_pd = compare_stages(processing, downstream, includes_downstream=True)
        status_md = compare_stages(mining, downstream, includes_downstream=True)

        overall = overall_status([status_mp, status_pd, status_md])

        strongest, strongest_basis = strongest_stage(
            mining,
            processing,
            downstream,
            status_mp,
            status_pd,
            status_md,
        )

        row = {
            "version": VERSION,
            "mineral": mineral,
            "year": int(year) if pd.notna(year) else "",
            "mining_denominator_type": mining["denominator_type"],
            "mining_metric_basis": mining["metric_basis"],
            "mining_top1_share_percent": mining["top1"],
            "mining_top3_share_percent": mining["top3"],
            "mining_hhi": mining["hhi"],
            "mining_hhi_valid": mining["hhi_valid"],
            "mining_evidence_tier": mining["evidence_tier"],
            "mining_source_confidence": mining["source_confidence"],
            "processing_denominator_type": processing["denominator_type"],
            "processing_metric_basis": processing["metric_basis"],
            "processing_top1_share_percent": processing["top1"],
            "processing_top3_share_percent": processing["top3"],
            "processing_hhi": processing["hhi"],
            "processing_hhi_valid": processing["hhi_valid"],
            "processing_evidence_tier": processing["evidence_tier"],
            "processing_source_confidence": processing["source_confidence"],
            "downstream_material_form": downstream["material_form"],
            "downstream_denominator_type": downstream["denominator_type"],
            "downstream_metric_basis": downstream["metric_basis"],
            "downstream_battery_grade_flag": downstream["battery_grade_flag"],
            "downstream_top1_share_percent": downstream["top1"],
            "downstream_top3_share_percent": downstream["top3"],
            "downstream_hhi": downstream["hhi"],
            "downstream_hhi_valid": downstream["hhi_valid"],
            "downstream_evidence_tier": downstream["evidence_tier"],
            "downstream_source_confidence": downstream["source_confidence"],
            "mining_to_processing_gap_pp": gap_if_comparable(mining["top3"], processing["top3"], status_mp),
            "processing_to_downstream_gap_pp": gap_if_comparable(processing["top3"], downstream["top3"], status_pd),
            "mining_to_downstream_gap_pp": gap_if_comparable(mining["top3"], downstream["top3"], status_md),
            "mining_processing_comparability_status": status_mp,
            "processing_downstream_comparability_status": status_pd,
            "mining_downstream_comparability_status": status_md,
            "overall_comparability_status": overall,
            "strongest_observable_concentration_stage": strongest,
            "strongest_stage_basis": strongest_basis,
            "missingness_status": row_missingness([mining, processing, downstream]),
            "calculation_status": "",
            "calculation_notes": "",
            "primary_source_summary": joined_unique(group["source_name"]),
            "public_summary": "",
        }

        row["calculation_status"] = calculation_status(row)

        if row["calculation_status"] == "blocked":
            row["calculation_notes"] = (
                "No supported numeric concentration calculations were produced. "
                "Add source-backed evidence rows before calculating stage concentration metrics."
            )
        elif overall != "comparable":
            row["calculation_notes"] = (
                "Numeric evidence exists, but one or more stage comparisons are not fully comparable. "
                "Capacity, production, denominator, geography, year, source-confidence, and battery-grade flags "
                "must align before calculating numeric stage gaps."
            )
        else:
            row["calculation_notes"] = (
                "Comparable public concentration evidence was available for the calculated fields."
            )

        row["public_summary"] = public_summary_for_row(row)
        rows.append(row)

    output = pd.DataFrame(rows, columns=PROCESSED_COLUMNS)
    return output


def write_processed_output(df: pd.DataFrame) -> None:
    PROCESSED_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    output = df.copy()

    for column in PROCESSED_COLUMNS:
        if column not in output.columns:
            output[column] = ""

    output = output[PROCESSED_COLUMNS]
    output.to_csv(PROCESSED_OUTPUT_PATH, index=False)


def main() -> None:
    curated = load_curated_input()
    curated = validate_curated_input(curated)
    processed = process(curated)
    write_processed_output(processed)

    print("V2.3 downstream concentration evidence tracker completed.")
    print(f"Input rows validated: {len(curated)}")
    print(f"Processed rows written: {len(processed)}")
    print(f"Created output: {PROCESSED_OUTPUT_PATH}")

    if processed.empty:
        print(
            "No calculations were produced because the curated evidence file is schema-only "
            "or contains no source-backed calculable evidence rows."
        )


if __name__ == "__main__":
    main()
