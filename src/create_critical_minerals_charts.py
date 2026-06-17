from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

METRICS_INPUT = (
    BASE_DIR / "data" / "processed" / "critical_minerals_concentration_metrics.csv"
)
RANKING_INPUT = (
    BASE_DIR / "data" / "processed" / "critical_minerals_latest_ranking.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs" / "charts"

HHI_RANKING_OUTPUT = OUTPUT_DIR / "critical_minerals_2024_hhi_ranking.png"
TOP3_TREND_OUTPUT = OUTPUT_DIR / "critical_minerals_top3_share_trend.png"
TOP1_TOP3_OUTPUT = OUTPUT_DIR / "critical_minerals_2024_top1_top3_comparison.png"
SHARE_COVERAGE_OUTPUT = OUTPUT_DIR / "critical_minerals_share_coverage_diagnostic.png"

EXPECTED_MATERIALS = [
    "lithium",
    "cobalt",
    "nickel",
    "natural_graphite",
    "manganese",
]

EXPECTED_YEARS = [2020, 2021, 2022, 2023, 2024]

REQUIRED_METRICS_COLUMNS = [
    "year",
    "material",
    "top_1_producer",
    "top_1_producer_share_pct",
    "top_3_producers",
    "top_3_producer_share_pct",
    "hhi_concentration_index",
    "producer_count",
    "data_caveat_note",
]

REQUIRED_RANKING_COLUMNS = [
    "material",
    "year",
    "top_1_producer",
    "top_1_producer_share_pct",
    "top_3_producers",
    "top_3_producer_share_pct",
    "hhi_concentration_index",
    "producer_count",
    "concentration_rank",
    "data_caveat_note",
]


def display_material_name(material: str) -> str:
    """Return readable material label for chart display."""
    labels = {
        "lithium": "Lithium",
        "cobalt": "Cobalt",
        "nickel": "Nickel",
        "natural_graphite": "Natural graphite",
        "manganese": "Manganese",
    }
    return labels.get(material, material.replace("_", " ").title())


def load_csv(path: Path, required_columns: list[str]) -> pd.DataFrame:
    """Load a CSV and validate required columns."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    df = pd.read_csv(path)

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"{path.name} is missing required columns: {', '.join(missing_columns)}"
        )

    if df.empty:
        raise ValueError(f"{path.name} is empty.")

    return df


def validate_metrics(metrics: pd.DataFrame) -> pd.DataFrame:
    """Validate concentration metrics before charting."""
    validated = metrics.copy()

    validated["year"] = pd.to_numeric(validated["year"], errors="coerce")
    if validated["year"].isna().any():
        raise ValueError("Metrics file contains non-numeric year values.")
    validated["year"] = validated["year"].astype(int)

    numeric_columns = [
        "top_1_producer_share_pct",
        "top_3_producer_share_pct",
        "hhi_concentration_index",
        "producer_count",
    ]

    optional_numeric_columns = [
        "sum_producer_share_pct",
        "active_producer_count",
    ]

    for column in numeric_columns + [
        col for col in optional_numeric_columns if col in validated.columns
    ]:
        validated[column] = pd.to_numeric(validated[column], errors="coerce")
        if validated[column].isna().any():
            raise ValueError(f"Metrics file contains non-numeric values in {column}.")

    materials = sorted(validated["material"].unique())
    missing_materials = sorted(set(EXPECTED_MATERIALS) - set(materials))
    unknown_materials = sorted(set(materials) - set(EXPECTED_MATERIALS))

    if missing_materials:
        raise ValueError(f"Metrics file is missing materials: {missing_materials}")

    if unknown_materials:
        raise ValueError(f"Metrics file has unknown materials: {unknown_materials}")

    for material in EXPECTED_MATERIALS:
        material_df = validated[validated["material"] == material]
        years = sorted(material_df["year"].unique())

        missing_years = sorted(set(EXPECTED_YEARS) - set(years))
        extra_years = sorted(set(years) - set(EXPECTED_YEARS))

        if missing_years:
            raise ValueError(f"{material}: missing years in metrics: {missing_years}")

        if extra_years:
            raise ValueError(f"{material}: unexpected years in metrics: {extra_years}")

        if len(material_df) != len(EXPECTED_YEARS):
            raise ValueError(
                f"{material}: expected {len(EXPECTED_YEARS)} metric rows, "
                f"found {len(material_df)}."
            )

    if (validated["top_1_producer_share_pct"] < 0).any():
        raise ValueError("Negative top_1_producer_share_pct found.")

    if (validated["top_3_producer_share_pct"] < 0).any():
        raise ValueError("Negative top_3_producer_share_pct found.")

    if (validated["hhi_concentration_index"] < 0).any():
        raise ValueError("Negative hhi_concentration_index found.")

    if (validated["top_3_producer_share_pct"] < validated["top_1_producer_share_pct"]).any():
        raise ValueError("Top-3 share is smaller than Top-1 share for at least one row.")

    if "share_coverage_flag" in validated.columns:
        bad_flags = validated[validated["share_coverage_flag"] != "ok"]
        if not bad_flags.empty:
            examples = bad_flags[
                ["material", "year", "share_coverage_flag"]
            ].to_string(index=False)
            raise ValueError(
                "Non-ok share coverage flags found before charting:\n" + examples
            )

    return validated


def validate_ranking(ranking: pd.DataFrame) -> pd.DataFrame:
    """Validate latest ranking before charting."""
    validated = ranking.copy()

    validated["year"] = pd.to_numeric(validated["year"], errors="coerce")
    if validated["year"].isna().any():
        raise ValueError("Ranking file contains non-numeric year values.")
    validated["year"] = validated["year"].astype(int)

    numeric_columns = [
        "top_1_producer_share_pct",
        "top_3_producer_share_pct",
        "hhi_concentration_index",
        "producer_count",
        "concentration_rank",
    ]

    for column in numeric_columns:
        validated[column] = pd.to_numeric(validated[column], errors="coerce")
        if validated[column].isna().any():
            raise ValueError(f"Ranking file contains non-numeric values in {column}.")

    latest_years = sorted(validated["year"].unique())
    if latest_years != [2024]:
        raise ValueError(f"Ranking file should contain only 2024, found: {latest_years}")

    materials = sorted(validated["material"].unique())
    missing_materials = sorted(set(EXPECTED_MATERIALS) - set(materials))
    unknown_materials = sorted(set(materials) - set(EXPECTED_MATERIALS))

    if missing_materials:
        raise ValueError(f"Ranking file is missing materials: {missing_materials}")

    if unknown_materials:
        raise ValueError(f"Ranking file has unknown materials: {unknown_materials}")

    if len(validated) != len(EXPECTED_MATERIALS):
        raise ValueError(
            f"Ranking file should have {len(EXPECTED_MATERIALS)} rows, "
            f"found {len(validated)}."
        )

    expected_ranks = list(range(1, len(EXPECTED_MATERIALS) + 1))
    actual_ranks = sorted(validated["concentration_rank"].astype(int).tolist())

    if actual_ranks != expected_ranks:
        raise ValueError(
            f"Ranking file has invalid concentration ranks: {actual_ranks}"
        )

    return validated


def save_figure(path: Path) -> None:
    """Save current matplotlib figure with common settings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Created: {path.relative_to(BASE_DIR)}")


def create_hhi_ranking_chart(ranking: pd.DataFrame) -> None:
    """Create 2024 HHI ranking bar chart."""
    chart_df = ranking.sort_values(
        by=["hhi_concentration_index", "material"],
        ascending=[False, True],
        kind="mergesort",
    ).copy()

    labels = [display_material_name(material) for material in chart_df["material"]]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, chart_df["hhi_concentration_index"])

    plt.title("USGS mine-production concentration, 2024\nHHI by battery mineral")
    plt.ylabel("HHI concentration index")
    plt.xlabel("Material")
    plt.xticks(rotation=25, ha="right")

    for bar, value in zip(bars, chart_df["hhi_concentration_index"]):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    plt.figtext(
        0.01,
        0.01,
        "Source: USGS Mineral Commodity Summaries 2025. "
        "Concentration signal only; not a risk score.",
        ha="left",
        fontsize=8,
    )

    save_figure(HHI_RANKING_OUTPUT)


def create_top3_share_trend_chart(metrics: pd.DataFrame, ranking: pd.DataFrame) -> None:
    """Create Top-3 producer share trend chart for 2020-2024."""
    ranking_order = (
        ranking.sort_values(
            by=["hhi_concentration_index", "material"],
            ascending=[False, True],
            kind="mergesort",
        )["material"]
        .tolist()
    )

    plt.figure(figsize=(10, 6))

    for material in ranking_order:
        material_df = metrics[metrics["material"] == material].sort_values(
            by="year", kind="mergesort"
        )
        plt.plot(
            material_df["year"],
            material_df["top_3_producer_share_pct"],
            marker="o",
            label=display_material_name(material),
        )

    plt.title(
        "Top-3 producer share trend, 2020–2024\n"
        "USGS mine-production concentration signal"
    )
    plt.ylabel("Top-3 producer share (%)")
    plt.xlabel("Year")
    plt.xticks(EXPECTED_YEARS)
    plt.ylim(0, 100)
    plt.legend(title="Material", loc="best")
    plt.grid(axis="y", alpha=0.3)

    plt.figtext(
        0.01,
        0.01,
        "Source: USGS Mineral Commodity Summaries 2025. "
        "Shows concentration trend, not supply-chain risk.",
        ha="left",
        fontsize=8,
    )

    save_figure(TOP3_TREND_OUTPUT)


def create_top1_top3_comparison_chart(ranking: pd.DataFrame) -> None:
    """Create 2024 Top-1 vs Top-3 comparison chart."""
    chart_df = ranking.sort_values(
        by=["hhi_concentration_index", "material"],
        ascending=[False, True],
        kind="mergesort",
    ).copy()

    labels = [display_material_name(material) for material in chart_df["material"]]
    x_positions = range(len(chart_df))
    bar_width = 0.38

    top1_positions = [position - bar_width / 2 for position in x_positions]
    top3_positions = [position + bar_width / 2 for position in x_positions]

    plt.figure(figsize=(11, 6))

    top1_bars = plt.bar(
        top1_positions,
        chart_df["top_1_producer_share_pct"],
        width=bar_width,
        label="Top-1 producer share",
    )

    top3_bars = plt.bar(
        top3_positions,
        chart_df["top_3_producer_share_pct"],
        width=bar_width,
        label="Top-3 producer share",
    )

    plt.title(
        "Top-1 vs Top-3 producer concentration, 2024\n"
        "USGS mine-production concentration"
    )
    plt.ylabel("Producer share (%)")
    plt.xlabel("Material")
    plt.xticks(list(x_positions), labels, rotation=25, ha="right")
    plt.ylim(0, 100)
    plt.legend(loc="best")
    plt.grid(axis="y", alpha=0.3)

    for bars in [top1_bars, top3_bars]:
        for bar in bars:
            value = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                value,
                f"{value:.1f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    plt.figtext(
        0.01,
        0.01,
        "Source: USGS Mineral Commodity Summaries 2025. "
        "Compares producer concentration structure; not a risk ranking.",
        ha="left",
        fontsize=8,
    )

    save_figure(TOP1_TOP3_OUTPUT)


def create_share_coverage_diagnostic_chart(metrics: pd.DataFrame) -> None:
    """Create optional share coverage diagnostic chart if coverage columns exist."""
    required_columns = {"sum_producer_share_pct", "share_coverage_flag"}

    if not required_columns.issubset(set(metrics.columns)):
        print(
            "Skipped optional share coverage diagnostic chart: "
            "sum_producer_share_pct/share_coverage_flag not found."
        )
        return

    chart_df = metrics.copy()
    chart_df["material_label"] = chart_df["material"].apply(display_material_name)

    material_order = [
        display_material_name(material)
        for material in sorted(chart_df["material"].unique())
    ]

    plt.figure(figsize=(10, 6))

    for material_label in material_order:
        material_df = chart_df[chart_df["material_label"] == material_label].sort_values(
            by="year", kind="mergesort"
        )
        plt.plot(
            material_df["year"],
            material_df["sum_producer_share_pct"],
            marker="o",
            label=material_label,
        )

    plt.axhline(100, linestyle="--", linewidth=1)
    plt.title(
        "Share coverage diagnostic, 2020–2024\n"
        "Producer shares versus USGS World totals"
    )
    plt.ylabel("Sum of producer shares (%)")
    plt.xlabel("Year")
    plt.xticks(EXPECTED_YEARS)
    plt.legend(title="Material", loc="best")
    plt.grid(axis="y", alpha=0.3)

    plt.figtext(
        0.01,
        0.01,
        "Diagnostic only. Values near 100% indicate producer rows align with USGS World totals.",
        ha="left",
        fontsize=8,
    )

    save_figure(SHARE_COVERAGE_OUTPUT)


def create_charts(metrics: pd.DataFrame, ranking: pd.DataFrame) -> None:
    """Create all V2.1 critical minerals charts."""
    create_hhi_ranking_chart(ranking)
    create_top3_share_trend_chart(metrics, ranking)
    create_top1_top3_comparison_chart(ranking)
    create_share_coverage_diagnostic_chart(metrics)


def main() -> None:
    """Run V2.1 chart pipeline."""
    print("Loading processed V2.1 concentration outputs...")
    metrics = load_csv(METRICS_INPUT, REQUIRED_METRICS_COLUMNS)
    ranking = load_csv(RANKING_INPUT, REQUIRED_RANKING_COLUMNS)

    print("Validating chart inputs...")
    metrics = validate_metrics(metrics)
    ranking = validate_ranking(ranking)

    print("Creating V2.1 critical minerals charts...")
    create_charts(metrics, ranking)

    print("")
    print("V2.1 critical minerals chart pipeline completed successfully.")
    print("Interpretation boundary: charts show concentration signals, not risk scores.")


if __name__ == "__main__":
    main()

