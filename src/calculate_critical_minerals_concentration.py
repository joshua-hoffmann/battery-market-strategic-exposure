from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_PATH = BASE_DIR / "data" / "curated" / "critical_minerals_production_inputs.csv"

COUNTRY_SHARES_OUTPUT = (
    BASE_DIR / "data" / "processed" / "critical_minerals_country_shares.csv"
)
CONCENTRATION_METRICS_OUTPUT = (
    BASE_DIR / "data" / "processed" / "critical_minerals_concentration_metrics.csv"
)
LATEST_RANKING_OUTPUT = (
    BASE_DIR / "data" / "processed" / "critical_minerals_latest_ranking.csv"
)

EXPECTED_COLUMNS = [
    "year",
    "material",
    "country",
    "production_value",
    "unit",
    "source_name",
    "source_release",
    "source_year",
    "source_detail",
    "value_status",
    "is_world_total",
    "include_in_concentration_calc",
    "data_quality_flag",
    "notes",
]

EXPECTED_MATERIALS = [
    "lithium",
    "cobalt",
    "nickel",
    "natural_graphite",
    "manganese",
]

EXPECTED_YEARS = [2020, 2021, 2022, 2023, 2024]

EXCLUDED_VALUE_STATUSES = {"withheld", "not_available"}


def normalize_bool(value: object) -> bool:
    """Convert common CSV boolean strings to Python bool."""
    if isinstance(value, bool):
        return value

    if pd.isna(value):
        raise ValueError("Boolean field contains missing value.")

    normalized = str(value).strip().lower()

    if normalized == "true":
        return True
    if normalized == "false":
        return False

    raise ValueError(f"Invalid boolean value: {value!r}. Expected true/false.")


def load_input(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    """Load curated critical minerals production input."""
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input file: {input_path}")

    df = pd.read_csv(input_path, dtype=str, keep_default_na=False)

    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(
            "Input CSV is missing required columns: "
            + ", ".join(missing_columns)
        )

    extra_columns = [col for col in df.columns if col not in EXPECTED_COLUMNS]
    if extra_columns:
        raise ValueError(
            "Input CSV contains unexpected columns: "
            + ", ".join(extra_columns)
        )

    return df


def validate_input(df: pd.DataFrame) -> pd.DataFrame:
    """Validate curated input before concentration calculations."""
    validated = df.copy()

    if validated.empty:
        raise ValueError("Input CSV is empty.")

    try:
        validated["year"] = validated["year"].astype(int)
    except ValueError as exc:
        raise ValueError("Column 'year' must contain integer years.") from exc

    try:
        validated["source_year"] = validated["source_year"].astype(int)
    except ValueError as exc:
        raise ValueError("Column 'source_year' must contain integer years.") from exc

    try:
        validated["is_world_total"] = validated["is_world_total"].apply(normalize_bool)
        validated["include_in_concentration_calc"] = validated[
            "include_in_concentration_calc"
        ].apply(normalize_bool)
    except ValueError as exc:
        raise ValueError(f"Boolean validation failed: {exc}") from exc

    materials = sorted(validated["material"].unique())
    unknown_materials = sorted(set(materials) - set(EXPECTED_MATERIALS))
    missing_materials = sorted(set(EXPECTED_MATERIALS) - set(materials))

    if unknown_materials:
        raise ValueError(
            "Unknown material names found: " + ", ".join(unknown_materials)
        )

    if missing_materials:
        raise ValueError(
            "Missing expected materials: " + ", ".join(missing_materials)
        )

    for material in EXPECTED_MATERIALS:
        material_df = validated[validated["material"] == material]
        material_years = sorted(material_df["year"].unique())

        missing_years = sorted(set(EXPECTED_YEARS) - set(material_years))
        extra_years = sorted(set(material_years) - set(EXPECTED_YEARS))

        if missing_years:
            raise ValueError(f"{material}: missing expected years: {missing_years}")

        if extra_years:
            raise ValueError(f"{material}: unexpected years found: {extra_years}")

        for year in EXPECTED_YEARS:
            group = material_df[material_df["year"] == year]

            world_rows = group[group["is_world_total"]]
            if len(world_rows) != 1:
                raise ValueError(
                    f"{material} {year}: expected exactly one World row, "
                    f"found {len(world_rows)}."
                )

            world_row = world_rows.iloc[0]

            if world_row["country"] != "World":
                raise ValueError(
                    f"{material} {year}: World row must have country='World'."
                )

            if bool(world_row["include_in_concentration_calc"]):
                raise ValueError(
                    f"{material} {year}: World row is incorrectly included "
                    "in concentration calculation."
                )

            world_value = pd.to_numeric(
                world_row["production_value"], errors="coerce"
            )

            if pd.isna(world_value):
                raise ValueError(
                    f"{material} {year}: World row has non-numeric production_value."
                )

            if world_value <= 0:
                raise ValueError(
                    f"{material} {year}: World total production must be > 0."
                )

            units = sorted(group["unit"].unique())
            if len(units) != 1:
                raise ValueError(
                    f"{material} {year}: inconsistent units found: {units}"
                )

    included = validated[validated["include_in_concentration_calc"]].copy()

    included_world_rows = included[included["is_world_total"]]
    if not included_world_rows.empty:
        raise ValueError("World rows found in concentration calculation input.")

    bad_status_rows = included[
        included["value_status"].str.lower().isin(EXCLUDED_VALUE_STATUSES)
    ]
    if not bad_status_rows.empty:
        raise ValueError(
            "withheld/not_available rows found in concentration calculation input."
        )

    blank_value_rows = included[included["production_value"].str.strip() == ""]
    if not blank_value_rows.empty:
        raise ValueError(
            "Included rows with blank production_value found. "
            "All included rows require numeric production_value."
        )

    included["production_value_numeric"] = pd.to_numeric(
        included["production_value"], errors="coerce"
    )

    non_numeric = included[included["production_value_numeric"].isna()]
    if not non_numeric.empty:
        examples = non_numeric[
            ["year", "material", "country", "production_value"]
        ].head(10)
        raise ValueError(
            "Included rows with non-numeric production_value found:\n"
            + examples.to_string(index=False)
        )

    negative_rows = included[included["production_value_numeric"] < 0]
    if not negative_rows.empty:
        examples = negative_rows[
            ["year", "material", "country", "production_value"]
        ].head(10)
        raise ValueError(
            "Negative production_value rows found:\n"
            + examples.to_string(index=False)
        )

    return validated


def calculate_country_shares(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate producer shares by material-year-country."""
    world_totals = (
        df[df["is_world_total"]]
        .loc[:, ["year", "material", "production_value", "unit"]]
        .rename(
            columns={
                "production_value": "world_total_production",
                "unit": "world_total_unit",
            }
        )
        .copy()
    )

    world_totals["world_total_production"] = pd.to_numeric(
        world_totals["world_total_production"], errors="coerce"
    )

    producers = df[
        (df["include_in_concentration_calc"])
        & (~df["is_world_total"])
        & (~df["value_status"].str.lower().isin(EXCLUDED_VALUE_STATUSES))
    ].copy()

    producers["production_value"] = pd.to_numeric(
        producers["production_value"], errors="coerce"
    )

    merged = producers.merge(
        world_totals,
        on=["year", "material"],
        how="left",
        validate="many_to_one",
    )

    missing_world_total = merged["world_total_production"].isna()
    if missing_world_total.any():
        examples = merged.loc[
            missing_world_total, ["year", "material", "country"]
        ].head(10)
        raise ValueError(
            "Missing world_total_production after merge:\n"
            + examples.to_string(index=False)
        )

    zero_world_total = merged["world_total_production"] <= 0
    if zero_world_total.any():
        examples = merged.loc[
            zero_world_total,
            ["year", "material", "country", "world_total_production"],
        ].head(10)
        raise ValueError(
            "Invalid world_total_production <= 0 after merge:\n"
            + examples.to_string(index=False)
        )

    unit_mismatch = merged["unit"] != merged["world_total_unit"]
    if unit_mismatch.any():
        examples = merged.loc[
            unit_mismatch,
            ["year", "material", "country", "unit", "world_total_unit"],
        ].head(10)
        raise ValueError(
            "Producer unit does not match World total unit:\n"
            + examples.to_string(index=False)
        )

    merged["producer_share"] = (
        merged["production_value"] / merged["world_total_production"]
    )
    merged["producer_share_pct"] = merged["producer_share"] * 100

    merged = merged.sort_values(
        by=["material", "year", "producer_share", "country"],
        ascending=[True, True, False, True],
        kind="mergesort",
    )

    merged["producer_rank"] = (
        merged.groupby(["material", "year"])["producer_share"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    output_columns = [
        "year",
        "material",
        "country",
        "production_value",
        "world_total_production",
        "unit",
        "producer_share",
        "producer_share_pct",
        "producer_rank",
        "source_name",
        "source_release",
        "source_year",
        "source_detail",
        "value_status",
        "data_quality_flag",
        "notes",
    ]

    return merged.loc[:, output_columns]


def build_data_caveat_note(group: pd.DataFrame) -> str:
    """Create a short caveat note for a material-year group."""
    caveats = []

    if (group["country"] == "Other countries").any():
        caveats.append("includes_other_countries_aggregate")

    if (group["production_value"] == 0).any():
        caveats.append("includes_source_reported_zero_rows")

    concentrate_mask = group["country"].str.contains(
        "concentrate", case=False, na=False
    ) | group["notes"].str.contains("concentrate", case=False, na=False)

    if concentrate_mask.any():
        caveats.append("includes_concentrate_labeled_rows")

    if group["value_status"].str.lower().eq("estimated").any():
        caveats.append("includes_estimated_values")

    if group["value_status"].str.lower().eq("rounded").any():
        caveats.append("includes_rounded_values")

    if not caveats:
        return "none"

    return ";".join(caveats)


def calculate_concentration_metrics(country_shares: pd.DataFrame) -> pd.DataFrame:
    """Calculate Top-1, Top-3, HHI, and caveat metrics by material-year."""
    records = []

    grouped = country_shares.groupby(["material", "year"], sort=True)

    for (material, year), group in grouped:
        sorted_group = group.sort_values(
            by=["producer_share", "country"],
            ascending=[False, True],
            kind="mergesort",
        ).copy()

        top_1 = sorted_group.iloc[0]
        top_3 = sorted_group.head(3)

        top_1_producer = str(top_1["country"])
        top_1_producer_share = float(top_1["producer_share"])
        top_3_producers = ";".join(top_3["country"].astype(str).tolist())
        top_3_producer_share = float(top_3["producer_share"].sum())
        hhi_concentration_index = float(
            ((sorted_group["producer_share"] * 100) ** 2).sum()
        )

        has_other_countries_aggregate = bool(
            (sorted_group["country"] == "Other countries").any()
        )
        has_source_reported_zero_rows = bool(
            (sorted_group["production_value"] == 0).any()
        )
        has_concentrate_labeled_rows = bool(
            sorted_group["country"]
            .str.contains("concentrate", case=False, na=False)
            .any()
            or sorted_group["notes"]
            .str.contains("concentrate", case=False, na=False)
            .any()
        )
        has_estimated_values = bool(
            sorted_group["value_status"].str.lower().eq("estimated").any()
        )
        has_rounded_values = bool(
            sorted_group["value_status"].str.lower().eq("rounded").any()
        )
        sum_producer_share = float(sorted_group["producer_share"].sum())
        sum_producer_share_pct = sum_producer_share * 100
        active_producer_count = int((sorted_group["production_value"] > 0).sum())

        if 0.95 <= sum_producer_share <= 1.05:
            share_coverage_flag = "ok"
        elif 0.90 <= sum_producer_share < 0.95 or 1.05 < sum_producer_share <= 1.10:
            share_coverage_flag = "review"
        else:
            share_coverage_flag = "warning"

        records.append(
            {
                "year": int(year),
                "material": material,
                "top_1_producer": top_1_producer,
                "top_1_producer_share": top_1_producer_share,
                "top_1_producer_share_pct": top_1_producer_share * 100,
                "top_3_producers": top_3_producers,
                "top_3_producer_share": top_3_producer_share,
                "top_3_producer_share_pct": top_3_producer_share * 100,
                "hhi_concentration_index": hhi_concentration_index,
                "producer_count": int(len(sorted_group)),
                "active_producer_count": active_producer_count,
                "world_total_production": float(top_1["world_total_production"]),
                "unit": str(top_1["unit"]),
                "sum_producer_share": sum_producer_share,
                "sum_producer_share_pct": sum_producer_share_pct,
                "share_coverage_flag": share_coverage_flag,
                "has_other_countries_aggregate": has_other_countries_aggregate,
                "has_source_reported_zero_rows": has_source_reported_zero_rows,
                "has_concentrate_labeled_rows": has_concentrate_labeled_rows,
                "has_estimated_values": has_estimated_values,
                "has_rounded_values": has_rounded_values,
                "data_caveat_note": build_data_caveat_note(sorted_group),
            }
        )

    metrics = pd.DataFrame.from_records(records)

    metrics = metrics.sort_values(
        by=["material", "year"],
        ascending=[True, True],
        kind="mergesort",
    ).reset_index(drop=True)

    metrics["yoy_change_top3_share"] = (
        metrics.groupby("material")["top_3_producer_share"].diff()
    )
    metrics["yoy_change_top3_share_pp"] = (
        metrics["yoy_change_top3_share"] * 100
    )

    output_columns = [
        "year",
        "material",
        "top_1_producer",
        "top_1_producer_share",
        "top_1_producer_share_pct",
        "top_3_producers",
        "top_3_producer_share",
        "top_3_producer_share_pct",
        "hhi_concentration_index",
        "producer_count",
        "active_producer_count",
        "world_total_production",
        "unit",
        "sum_producer_share",
        "sum_producer_share_pct",
        "share_coverage_flag",
        "yoy_change_top3_share",
        "yoy_change_top3_share_pp",
        "has_other_countries_aggregate",
        "has_source_reported_zero_rows",
        "has_concentrate_labeled_rows",
        "has_estimated_values",
        "has_rounded_values",
        "data_caveat_note",
    ]

    return metrics.loc[:, output_columns]


def create_latest_ranking(
    concentration_metrics: pd.DataFrame,
    latest_year: int = 2024,
) -> pd.DataFrame:
    """Create latest-year concentration ranking by HHI descending."""
    latest = concentration_metrics[
        concentration_metrics["year"] == latest_year
    ].copy()

    if latest.empty:
        raise ValueError(f"No concentration metrics found for latest_year={latest_year}.")

    missing_materials = sorted(set(EXPECTED_MATERIALS) - set(latest["material"]))
    if missing_materials:
        raise ValueError(
            f"Latest ranking missing materials for {latest_year}: {missing_materials}"
        )

    latest = latest.sort_values(
        by=["hhi_concentration_index", "top_3_producer_share", "material"],
        ascending=[False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)

    latest["concentration_rank"] = range(1, len(latest) + 1)

    output_columns = [
        "material",
        "year",
        "top_1_producer",
        "top_1_producer_share",
        "top_1_producer_share_pct",
        "top_3_producers",
        "top_3_producer_share",
        "top_3_producer_share_pct",
        "hhi_concentration_index",
        "producer_count",
        "active_producer_count",
        "sum_producer_share",
        "sum_producer_share_pct",
        "share_coverage_flag",
        "concentration_rank",
        "data_caveat_note",
    ]

    return latest.loc[:, output_columns]


def write_outputs(
    country_shares: pd.DataFrame,
    concentration_metrics: pd.DataFrame,
    latest_ranking: pd.DataFrame,
) -> None:
    """Write processed outputs."""
    output_dir = COUNTRY_SHARES_OUTPUT.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    country_shares.to_csv(COUNTRY_SHARES_OUTPUT, index=False)
    concentration_metrics.to_csv(CONCENTRATION_METRICS_OUTPUT, index=False)
    latest_ranking.to_csv(LATEST_RANKING_OUTPUT, index=False)

    print(f"Created: {COUNTRY_SHARES_OUTPUT.relative_to(BASE_DIR)}")
    print(f"Created: {CONCENTRATION_METRICS_OUTPUT.relative_to(BASE_DIR)}")
    print(f"Created: {LATEST_RANKING_OUTPUT.relative_to(BASE_DIR)}")


def main() -> None:
    """Run V2.1 critical minerals concentration calculation pipeline."""
    print("Loading curated critical minerals production input...")
    raw_input = load_input()

    print("Validating curated input...")
    validated_input = validate_input(raw_input)

    print("Calculating country producer shares...")
    country_shares = calculate_country_shares(validated_input)

    print("Calculating concentration metrics...")
    concentration_metrics = calculate_concentration_metrics(country_shares)

    print("Creating latest-year concentration ranking...")
    latest_ranking = create_latest_ranking(concentration_metrics, latest_year=2024)

    print("Writing processed outputs...")
    write_outputs(country_shares, concentration_metrics, latest_ranking)

    print("")
    print("V2.1 critical minerals concentration calculation completed successfully.")
    print("Ranking basis: hhi_concentration_index descending.")
    print("Interpretation boundary: concentration signal only, not a risk score.")


if __name__ == "__main__":
    main()


