from __future__ import annotations

from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "curated" / "battery_exposure_inputs.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "battery_exposure_indicators.csv"

REQUIRED_COLUMNS = [
    "year",
    "region",
    "indicator_name",
    "indicator_category",
    "value",
    "unit",
    "value_type",
    "source_name",
    "source_detail",
    "source_year",
    "is_outlook_context",
    "include_in_scorecard",
    "coverage_quality",
    "region_mapping",
    "notes",
]

ALLOWED_REGIONS = {"China", "EU", "United States", "Rest of World"}

ALLOWED_CATEGORIES = {
    "ev_battery_demand",
    "lithium_supply_dependency",
    "market_concentration",
    "policy_context",
}

ALLOWED_VALUE_TYPES = {
    "direct_reported",
    "calculated_share",
    "residual",
    "mapped_proxy",
    "text_context",
}

ALLOWED_REGION_MAPPINGS = {
    "direct_region",
    "eu_reported",
    "europe_used_as_proxy",
    "country_to_region_sum",
    "global_minus_selected_regions",
    "not_applicable",
}

ALLOWED_COVERAGE_QUALITY = {"high", "medium", "low"}

SCORECARD_CATEGORIES = [
    "ev_battery_demand",
    "lithium_supply_dependency",
    "market_concentration",
]

COMPONENT_COLUMN_MAP = {
    "ev_battery_demand": "demand_intensity_score",
    "lithium_supply_dependency": "lithium_dependency_score",
    "market_concentration": "market_concentration_score",
}

QUALITY_RANK = {"high": 1, "medium": 2, "low": 3}


def parse_bool(value: object) -> bool:
    text = str(value).strip().lower()

    if text in {"true", "1", "yes", "y"}:
        return True

    if text in {"false", "0", "no", "n"}:
        return False

    raise ValueError(f"Invalid boolean value: {value!r}")


def validate_input(df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df[REQUIRED_COLUMNS].copy()

    if df.empty:
        raise ValueError("Curated input CSV contains no data rows.")

    df["year"] = pd.to_numeric(df["year"], errors="raise").astype(int)
    df["source_year"] = pd.to_numeric(df["source_year"], errors="raise").astype(int)
    df["value"] = pd.to_numeric(
        df["value"].astype(str).str.replace(",", ".", regex=False),
        errors="raise",
    )
    df["is_outlook_context"] = df["is_outlook_context"].map(parse_bool)
    df["include_in_scorecard"] = df["include_in_scorecard"].map(parse_bool)

    invalid_regions = sorted(set(df["region"]) - ALLOWED_REGIONS)
    if invalid_regions:
        raise ValueError(f"Invalid regions found: {invalid_regions}")

    invalid_categories = sorted(set(df["indicator_category"]) - ALLOWED_CATEGORIES)
    if invalid_categories:
        raise ValueError(f"Invalid indicator categories found: {invalid_categories}")

    invalid_value_types = sorted(set(df["value_type"]) - ALLOWED_VALUE_TYPES)
    if invalid_value_types:
        raise ValueError(f"Invalid value_type values found: {invalid_value_types}")

    invalid_region_mappings = sorted(set(df["region_mapping"]) - ALLOWED_REGION_MAPPINGS)
    if invalid_region_mappings:
        raise ValueError(f"Invalid region_mapping values found: {invalid_region_mappings}")

    invalid_coverage = sorted(set(df["coverage_quality"]) - ALLOWED_COVERAGE_QUALITY)
    if invalid_coverage:
        raise ValueError(f"Invalid coverage_quality values found: {invalid_coverage}")

    required_text_columns = [
        "indicator_name",
        "unit",
        "source_name",
        "source_detail",
        "coverage_quality",
        "region_mapping",
        "notes",
    ]

    for column in required_text_columns:
        blank_mask = df[column].astype(str).str.strip().eq("")
        if blank_mask.any():
            raise ValueError(f"Blank values detected in required text column: {column}")

    if df.duplicated().any():
        raise ValueError("Duplicate exact rows detected in curated input CSV.")

    scorecard_rows = df[df["include_in_scorecard"]].copy()

    if scorecard_rows.empty:
        raise ValueError("No scorecard rows found.")

    bad_scorecard_years = scorecard_rows[~scorecard_rows["year"].between(2020, 2025)]
    if not bad_scorecard_years.empty:
        raise ValueError("Scorecard rows must be between 2020 and 2025.")

    bad_scorecard_categories = scorecard_rows[
        ~scorecard_rows["indicator_category"].isin(SCORECARD_CATEGORIES)
    ]

    if not bad_scorecard_categories.empty:
        raise ValueError("Scorecard rows may only use the three scoring indicator categories.")

    bad_policy_rows = df[
        (df["indicator_category"] == "policy_context")
        & (df["include_in_scorecard"])
    ]

    if not bad_policy_rows.empty:
        raise ValueError("policy_context rows must not be included in MVP score calculation.")

    bad_future_score_rows = df[
        (df["year"] > 2025)
        & (df["include_in_scorecard"])
    ]

    if not bad_future_score_rows.empty:
        raise ValueError("Rows after 2025 must not be included in scorecard calculation.")

    bad_outlook_rows = df[
        (df["year"] >= 2030)
        & (
            (df["include_in_scorecard"])
            | (~df["is_outlook_context"])
        )
    ]

    if not bad_outlook_rows.empty:
        raise ValueError("2030 or later rows must be outlook context only and excluded from scorecard.")

    return df


def add_component_scores(scorecard: pd.DataFrame) -> pd.DataFrame:
    scored_parts = []

    for (year, category), group in scorecard.groupby(["year", "indicator_category"]):
        group = group.copy()
        minimum = group["value"].min()
        maximum = group["value"].max()

        if maximum == minimum:
            group["normalized_value_score"] = 50.0
        else:
            group["normalized_value_score"] = ((group["value"] - minimum) / (maximum - minimum)) * 100

        if category == "lithium_supply_dependency":
            group["component_score"] = 100 - group["normalized_value_score"]
        else:
            group["component_score"] = group["normalized_value_score"]

        scored_parts.append(group)

    if not scored_parts:
        raise ValueError("No scorecard groups available for scoring.")

    return pd.concat(scored_parts, ignore_index=True)


def pressure_label(score: object) -> str:
    if pd.isna(score):
        return "insufficient_evidence"

    score_float = float(score)

    if score_float <= 33:
        return "lower_observed_pressure"

    if score_float <= 66:
        return "moderate_observed_pressure"

    return "higher_observed_pressure"


def conservative_quality(values: pd.Series) -> str:
    if values.empty:
        return "low"

    worst_rank = max(QUALITY_RANK[str(value)] for value in values)

    for label, rank in QUALITY_RANK.items():
        if rank == worst_rank:
            return label

    return "low"


def build_method_note(row: pd.Series) -> str:
    missing_components = []

    if pd.isna(row["demand_intensity_score"]):
        missing_components.append("demand_intensity_score")

    if pd.isna(row["lithium_dependency_score"]):
        missing_components.append("lithium_dependency_score")

    if pd.isna(row["market_concentration_score"]):
        missing_components.append("market_concentration_score")

    base_note = (
        "Scorecard index is an equal-weight descriptive average of available component scores. "
        "Lithium dependency score is inverted from lithium mine production share, so lower disclosed production share creates higher dependency pressure."
    )

    if missing_components:
        return base_note + " Missing components: " + ", ".join(missing_components) + "."

    return base_note + " All three MVP components are available."


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    scorecard = df[
        (df["include_in_scorecard"])
        & (~df["is_outlook_context"])
        & (df["year"].between(2020, 2025))
        & (df["indicator_category"].isin(SCORECARD_CATEGORIES))
    ].copy()

    if scorecard.empty:
        raise ValueError("No eligible scorecard rows after filtering.")

    grouped = add_component_scores(scorecard)

    pivot = (
        grouped
        .pivot_table(
            index=["year", "region"],
            columns="indicator_category",
            values="component_score",
            aggfunc="mean",
        )
        .reset_index()
        .rename(columns=COMPONENT_COLUMN_MAP)
    )

    for column in [
        "demand_intensity_score",
        "lithium_dependency_score",
        "market_concentration_score",
    ]:
        if column not in pivot.columns:
            pivot[column] = pd.NA

    component_columns = [
        "demand_intensity_score",
        "lithium_dependency_score",
        "market_concentration_score",
    ]

    pivot["included_indicator_count"] = pivot[component_columns].notna().sum(axis=1)
    pivot["scorecard_exposure_index"] = pivot[component_columns].mean(axis=1)
    pivot["observed_pressure_label"] = pivot["scorecard_exposure_index"].map(pressure_label)

    pivot["data_completeness_flag"] = pivot["included_indicator_count"].map(
        lambda count: "complete" if count == 3 else ("partial" if count > 0 else "insufficient")
    )

    quality = (
        grouped
        .groupby(["year", "region"])["coverage_quality"]
        .apply(conservative_quality)
        .reset_index(name="evidence_quality_flag")
    )

    policy_counts = (
        df[df["indicator_category"] == "policy_context"]
        .groupby(["year", "region"])
        .size()
        .reset_index(name="excluded_policy_context_count")
    )

    result = pivot.merge(quality, on=["year", "region"], how="left")
    result = result.merge(policy_counts, on=["year", "region"], how="left")

    result["excluded_policy_context_count"] = (
        result["excluded_policy_context_count"]
        .fillna(0)
        .astype(int)
    )

    result["method_notes"] = result.apply(build_method_note, axis=1)

    ordered_columns = [
        "year",
        "region",
        "demand_intensity_score",
        "lithium_dependency_score",
        "market_concentration_score",
        "scorecard_exposure_index",
        "observed_pressure_label",
        "data_completeness_flag",
        "evidence_quality_flag",
        "included_indicator_count",
        "excluded_policy_context_count",
        "method_notes",
    ]

    result = result[ordered_columns].sort_values(["year", "region"]).reset_index(drop=True)

    numeric_columns = [
        "demand_intensity_score",
        "lithium_dependency_score",
        "market_concentration_score",
        "scorecard_exposure_index",
    ]

    result[numeric_columns] = result[numeric_columns].round(1)

    return result


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing curated input file: {INPUT_PATH}")

    raw = pd.read_csv(INPUT_PATH)
    validated = validate_input(raw)
    processed = calculate_indicators(validated)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    processed.to_csv(OUTPUT_PATH, index=False)

    print(f"Created processed indicators: {OUTPUT_PATH}")
    print(f"Rows written: {len(processed)}")
    print("")
    print(processed[[
        "year",
        "region",
        "demand_intensity_score",
        "lithium_dependency_score",
        "market_concentration_score",
        "scorecard_exposure_index",
        "observed_pressure_label",
        "data_completeness_flag",
        "evidence_quality_flag",
    ]].to_string(index=False))


if __name__ == "__main__":
    main()
