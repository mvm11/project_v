from __future__ import annotations
from pathlib import Path
from typing import Final

import pandas as pd

from logger import Logger
from collector import Collector
from enricher import Enricher
from modeller import Modeller
from dashboard import Dashboard


class CrudeOilDataPipeline:
    CLASS_NAME: Final[str] = "CrudeOilDataPipeline"
    PACKAGE_DIR: Path = Path(__file__).resolve().parent
    DATA_DIR: Path = PACKAGE_DIR / "static" / "data"
    RAW_OUTPUT_PATH: Path = DATA_DIR / "crude_oil.csv"

    def __init__(self) -> None:
        self.logger: Logger = Logger()
        self.collector: Collector = Collector(logger=self.logger)
        self.enricher: Enricher = Enricher(logger=self.logger)
        self.modeller: Modeller = Modeller(logger=self.logger)
        self.dashboard: Dashboard = Dashboard()

        self.DATA_DIR.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        self.logger.info(self.CLASS_NAME, "run", "Pipeline execution started.")

        self._collect_raw_data()
        enriched_df: pd.DataFrame = self._enrich_data()
        if not enriched_df.empty:
            self._train_model()
            self._launch_dashboard()

        self.logger.info(self.CLASS_NAME, "run", "Pipeline execution finished.")

    # ------------------------------------------------------------------
    # Phase 1 – Collection
    # ------------------------------------------------------------------
    def _collect_raw_data(self) -> None:
        self.logger.info(self.CLASS_NAME, "_collect_raw_data", "Collecting raw data.")
        df: pd.DataFrame = self.collector.get_crude_oil_data()
        if df.empty:
            self.logger.warning(self.CLASS_NAME, "_collect_raw_data", "No data collected.")
            return
        self._save_raw_csv(df)

    def _save_raw_csv(self, df: pd.DataFrame) -> None:
        try:
            if self.RAW_OUTPUT_PATH.exists():
                existing_df: pd.DataFrame = pd.read_csv(self.RAW_OUTPUT_PATH)
                combined_df: pd.DataFrame = pd.concat([existing_df, df], ignore_index=True)
                combined_df.drop_duplicates(subset=["date"], inplace=True)
            else:
                combined_df = df

            combined_df.sort_values(by="date", ascending=False, inplace=True)
            combined_df.to_csv(self.RAW_OUTPUT_PATH, index=False)
            self.logger.info(
                self.CLASS_NAME,
                "_save_raw_csv",
                f"Raw data merged and saved to {self.RAW_OUTPUT_PATH}",
            )
        except Exception as error:
            self.logger.error(self.CLASS_NAME, "_save_raw_csv", f"Failed to save raw CSV: {error}")

    # ------------------------------------------------------------------
    # Phase 2 – Enrichment
    # ------------------------------------------------------------------
    def _enrich_data(self) -> pd.DataFrame:
        self.logger.info(self.CLASS_NAME, "_enrich_data", "Starting enrichment phase.")
        df_enriched: pd.DataFrame = self.enricher.enrich()
        if df_enriched.empty:
            self.logger.warning(self.CLASS_NAME, "_enrich_data", "Enrichment produced an empty DataFrame.")
        return df_enriched

    # ------------------------------------------------------------------
    # Phase 3 – Modelling
    # ------------------------------------------------------------------
    def _train_model(self) -> None:
        self.logger.info(self.CLASS_NAME, "_train_model", "Starting model training phase.")
        self.modeller.train()

    # ------------------------------------------------------------------
    # Phase 4 – Dashboard
    # ------------------------------------------------------------------
    def _launch_dashboard(self) -> None:
        self.logger.info(self.CLASS_NAME, "_launch_dashboard", "Launching dashboard.")
        self.dashboard.run()


# ----------------------------------------------------------------------
# Script entry‑point convenience wrapper
# ----------------------------------------------------------------------

def main() -> None:
    pipeline = CrudeOilDataPipeline()
    pipeline.run()


if __name__ == "__main__":
    main()
