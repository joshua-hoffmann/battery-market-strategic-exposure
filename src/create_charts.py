from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "battery_exposure_indicators.csv"
CHART_DIR = PROJECT_ROOT / "outputs" / "charts"

REQUIRED_COLUMNS = [
    "year",
    "region",
    "demand_intensity_score",
    "lithium_dependency_score",
    "market_concentration_score",
    "scorecard_exposure_index",
    "observed_pressure_label",
    "data_completeness_flag",
    "evidence_quality_flag",
]


def load_processed() -> pd.DataFrame:
    if not PROCESSED_PATH.exists():
        raise FileNotFoundError(f"Missing processed indicators file: {PROCESSED_PATH}")

    df = pd.read_csv(PROCESSED_PATH)

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing:
        raise ValueError(f"Processed file is missing required columns: {missing}")

    if df.empty:
        raise ValueError("Processed indicators file contains no rows.")

    return df


def save_exposure_score_by_region(df: pd.DataFrame) -> Path:
    latest_year = int(df["year"].max())
    latest = df[df["year"] == latest_year].copy()
    latest = latest.sort_values("scorecard_exposure_index", ascending=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(latest["region"], latest["scorecard_exposure_index"])
    ax.set_title(f"Scorecard Exposure Index by Region, {latest_year}")
    ax.set_xlabel("Region")
    ax.set_ylabel("Scorecard exposure index, 0-100")
    ax.set_ylim(0, 100)
    ax.tick_params(axis="x", rotation=25)

    output_path = CHART_DIR / "exposure_score_by_region.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    return output_path


def save_exposure_components_latest_year(df: pd.DataFrame) -> Path:
    target_year = int(df["year"].max())
    latest = df[df["year"] == target_year].copy()

    x_positions = list(range(len(latest)))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        [x - width for x in x_positions],
        latest["demand_intensity_score"],
        width=width,
        label="Demand intensity",
    )

    ax.bar(
        x_positions,
        latest["lithium_dependency_score"],
        width=width,
        label="Lithium dependency",
    )

    ax.bar(
        [x + width for x in x_positions],
        latest["market_concentration_score"],
        width=width,
        label="Market concentration",
    )

    ax.set_title(f"Exposure Components by Region, {target_year}")
    ax.set_xlabel("Region")
    ax.set_ylabel("Normalized component score, 0-100")
    ax.set_ylim(0, 100)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(latest["region"], rotation=25)
    ax.legend()

    output_path = CHART_DIR / "exposure_components_2025.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    return output_path


def save_exposure_trend_if_available(df: pd.DataFrame) -> Path | None:
    unique_years = sorted(df["year"].unique())

    if len(unique_years) < 2:
        stale_path = CHART_DIR / "exposure_trend_2020_2025.png"

        if stale_path.exists():
            stale_path.unlink()

        print("Skipped trend chart: only one scorecard year is available.")
        return None

    fig, ax = plt.subplots(figsize=(10, 5))

    for region, group in df.sort_values("year").groupby("region"):
        ax.plot(
            group["year"],
            group["scorecard_exposure_index"],
            marker="o",
            label=region,
        )

    first_year = int(min(unique_years))
    last_year = int(max(unique_years))

    ax.set_title(f"Directional Exposure Scorecard Trend, {first_year}-{last_year}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Scorecard exposure index, 0-100")
    ax.set_ylim(0, 100)
    ax.legend()

    output_path = CHART_DIR / "exposure_trend_2020_2025.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    return output_path


def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = load_processed()

    output_paths = [
        save_exposure_score_by_region(df),
        save_exposure_components_latest_year(df),
    ]

    trend_path = save_exposure_trend_if_available(df)

    if trend_path is not None:
        output_paths.append(trend_path)

    for output_path in output_paths:
        print(f"Created chart: {output_path}")


if __name__ == "__main__":
    main()
