"""Run outbreak-focused time series analytics from GenAI diagnosis outputs.

This module consumes diagnosis parquet outputs and generates disease-level
surveillance charts and summary sheets for operational monitoring.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.pathing import find_project_root, safe_filename
from src.utils.statistics import calculate_moving_average, calculate_rolling_ci95_upper


@dataclass
class TimeSeriesConfig:
    """Store runtime paths and thresholds for time series analytics.

    Args:
        genai_output_parquet (Path): Input classified diagnosis parquet path.
        charts_dir (Path): Destination for per-disease outbreak charts.
        sheets_dir (Path): Destination for per-disease summary sheets.

    Returns:
        None: Dataclass instance with resolved directories.

    Example:
        >>> config = TimeSeriesConfig.default()
    """

    genai_output_parquet: Path
    charts_dir: Path
    sheets_dir: Path

    @classmethod
    def default(cls) -> "TimeSeriesConfig":
        """Create default configuration based on repository structure.

        Args:
            None

        Returns:
            TimeSeriesConfig: Default path configuration.

        Example:
            >>> TimeSeriesConfig.default()
        """
        root = find_project_root()
        base = root / "src" / "outputs" / "time_series"
        charts = base / "charts"
        sheets = base / "sheets"
        charts.mkdir(parents=True, exist_ok=True)
        sheets.mkdir(parents=True, exist_ok=True)
        return cls(
            genai_output_parquet=root / "src" / "outputs" / "genai" / "agent_outputs_dataset_sintomas_grupos_classificado.parquet",
            charts_dir=charts,
            sheets_dir=sheets,
        )


class TimeSeriesAnalyzer:
    """Compute outbreak indicators and export disease-level monitoring assets.

    Args:
        config (TimeSeriesConfig): Runtime configuration.

    Returns:
        None: Analyzer instance ready to execute pipeline.

    Example:
        >>> analyzer = TimeSeriesAnalyzer(TimeSeriesConfig.default())
    """

    def __init__(self, config: TimeSeriesConfig):
        self.config = config

    def select_outbreak_targets(self, daily: pd.DataFrame) -> dict[str, str]:
        """Select dengue and influenza labels from available diagnosis strings.

        Args:
            daily (pd.DataFrame): Daily disease counts dataframe.

        Returns:
            dict[str, str]: Mapping from group key to disease label found in data.

        Example:
            >>> analyzer.select_outbreak_targets(daily)
        """
        keyword_groups = {
            "dengue": ["dengue"],
            "influenza": ["influenza", "gripe", "flu"],
        }
        all_labels = sorted(daily["disease"].dropna().astype(str).unique().tolist())
        selected = {}
        for group, keywords in keyword_groups.items():
            matches = [label for label in all_labels if any(key in label.lower() for key in keywords)]
            if matches:
                selected[group] = matches[0]
        return selected

    def load_daily_cases(self) -> pd.DataFrame:
        """Load classified diagnosis output and aggregate daily disease counts.

        Args:
            None

        Returns:
            pd.DataFrame: Daily case counts by diagnosis.

        Example:
            >>> daily = analyzer.load_daily_cases()
        """
        df = pd.read_parquet(self.config.genai_output_parquet)
        df["report_created_at"] = pd.to_datetime(df["report_created_at"], errors="coerce")
        df = df.dropna(subset=["report_created_at", "primary_diagnosis"])
        df["date"] = df["report_created_at"].dt.normalize()
        if "user_id" in df.columns:
            daily = df.groupby(["date", "primary_diagnosis"])["user_id"].nunique().reset_index(name="cases")
        else:
            daily = df.groupby(["date", "primary_diagnosis"]).size().reset_index(name="cases")
        daily = daily.rename(columns={"primary_diagnosis": "disease"})
        return daily

    def build_disease_frame(self, daily: pd.DataFrame, disease: str) -> pd.DataFrame:
        """Create one disease weekly frame with outbreak statistics.

        Args:
            daily (pd.DataFrame): Full daily disease table.
            disease (str): Disease label to process.

        Returns:
            pd.DataFrame: Weekly disease frame with observed, estimated, and CI columns.

        Example:
            >>> frame = analyzer.build_disease_frame(daily, 'Dengue')
        """
        subset = daily[daily["disease"] == disease].copy()
        full_dates = pd.date_range(subset["date"].min(), subset["date"].max(), freq="D")
        frame_daily = subset.set_index("date").reindex(full_dates).rename_axis("date").reset_index()
        frame_daily["disease"] = disease
        frame_daily["observed_daily"] = frame_daily["cases"].fillna(0).astype(float)
        frame_daily["estimated_moving_average_7d_daily"] = calculate_moving_average(frame_daily["observed_daily"], 7)
        weekly = pd.DataFrame(
            {
                "date": frame_daily["date"].dt.to_period("W-SUN").dt.end_time.dt.normalize(),
                "disease": disease,
                "observed_weekly": frame_daily["observed_daily"].values,
                "estimated_moving_average_7d_weekly": frame_daily["estimated_moving_average_7d_daily"].values,
            }
        )
        weekly = weekly.groupby(["date", "disease"], as_index=False).mean(numeric_only=True)
        weekly["ci95_upper_30d"] = calculate_rolling_ci95_upper(weekly["estimated_moving_average_7d_weekly"], 30)
        weekly["outbreak_alert"] = weekly["observed_weekly"] > weekly["ci95_upper_30d"]
        weekly["period"] = "train"
        cutoff_idx = int(len(weekly) * 252 / 365) if len(weekly) > 0 else 0
        weekly.loc[weekly.index >= cutoff_idx, "period"] = "test"
        return weekly

    def export_disease_outputs(self, frame: pd.DataFrame, disease: str) -> None:
        """Save chart and summary sheet for one disease.

        Args:
            frame (pd.DataFrame): Disease-level time series frame.
            disease (str): Disease label.

        Returns:
            None: Files are persisted under configured output directories.

        Example:
            >>> analyzer.export_disease_outputs(frame, 'Dengue')
        """
        token = safe_filename(disease)
        chart_path = self.config.charts_dir / f"{token}.png"
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(frame["date"], frame["observed_weekly"], label="Observed weekly (raw)", color="C0")
        ax.plot(frame["date"], frame["estimated_moving_average_7d_weekly"], label="Estimated weekly (7-day MA)", color="C1")
        ax.plot(frame["date"], frame["ci95_upper_30d"], label="CI95 upper threshold", color="C3", linestyle="--")
        alert_points = frame[frame["outbreak_alert"]]
        if not alert_points.empty:
            ax.scatter(
                alert_points["date"],
                alert_points["observed_weekly"],
                color="red",
                s=22,
                label="Spikes (observed > CI95 upper)",
            )
        ax.set_title(disease)
        ax.set_ylabel("Weekly cases")
        ax.legend(loc="best")
        fig.tight_layout()
        fig.savefig(chart_path, dpi=140)
        plt.close(fig)

        last_30 = frame.tail(30).copy()
        summary = pd.DataFrame(
            {
                "disease": [disease],
                "last_30d_mean_observed": [float(last_30["observed_weekly"].mean())],
                "last_7d_mean_observed": [float(frame["observed_weekly"].tail(7).mean())],
                "ci95_upper_current": [float(frame["ci95_upper_30d"].iloc[-1])],
                "current_value_observed": [float(frame["observed_weekly"].iloc[-1])],
                "current_value_estimated_ma7": [float(frame["estimated_moving_average_7d_weekly"].iloc[-1])],
                "outbreak_alert_current": [bool(frame["outbreak_alert"].iloc[-1])],
                "spikes_train": [int(frame[(frame["period"] == "train") & (frame["outbreak_alert"])].shape[0])],
                "spikes_test": [int(frame[(frame["period"] == "test") & (frame["outbreak_alert"])].shape[0])],
            }
        )

        sheet_path = self.config.sheets_dir / f"{token}.xlsx"
        with pd.ExcelWriter(sheet_path, engine="openpyxl") as writer:
            last_30.to_excel(writer, index=False, sheet_name="last_30_days")
            summary.to_excel(writer, index=False, sheet_name="summary")

    def run(self) -> tuple[Path, Path]:
        """Execute full time series pipeline and persist all artifacts.

        Args:
            None

        Returns:
            tuple[Path, Path]: Charts directory and sheets directory.

        Example:
            >>> analyzer.run()
        """
        for existing in self.config.charts_dir.glob("*.png"):
            existing.unlink()
        for existing in self.config.sheets_dir.glob("*.xlsx"):
            existing.unlink()
        daily = self.load_daily_cases()
        selected = self.select_outbreak_targets(daily)
        for group, disease in selected.items():
            frame = self.build_disease_frame(daily, disease)
            self.export_disease_outputs(frame, f"{group}_{disease}")
        return self.config.charts_dir, self.config.sheets_dir


def main() -> None:
    """Run time series analyzer from command-line entry point.

    Args:
        None

    Returns:
        None: Writes charts and summary sheets to disk.

    Example:
        >>> main()
    """
    analyzer = TimeSeriesAnalyzer(TimeSeriesConfig.default())
    charts_dir, sheets_dir = analyzer.run()
    print(f"Generated charts in: {charts_dir}")
    print(f"Generated sheets in: {sheets_dir}")


if __name__ == "__main__":
    main()
