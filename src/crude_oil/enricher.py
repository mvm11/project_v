"""Enricher module.

This module provides the Enricher class, responsible for taking raw crude‐oil
price data and generating an enriched dataset with additional engineered
features.
"""

from __future__ import annotations

import os
from typing import Final

import numpy as np
import pandas as pd

from logger import Logger


class Enricher:
    CLASS_NAME: Final[str] = "Enricher"

    # ------------------------------------------------------------------
    # File system constants
    # ------------------------------------------------------------------
    RAW_DATA_PATH: Final[str] = "src/crude_oil/static/data/crude_oil.csv"
    ENRICHED_DATA_PATH: Final[str] = "src/crude_oil/static/data/crude_oil_enriched.csv"

    def __init__(self, logger: Logger) -> None:
        """Instantiate an Enricher and ensure output folder exists."""
        self.logger: Logger = logger
        self._verify_folder(os.path.dirname(self.ENRICHED_DATA_PATH))


    def enrich(self) -> pd.DataFrame:
        """Load raw data, engineer features, persist, and return DataFrame."""
        df: pd.DataFrame = self._load_raw_data()
        if df.empty:
            self.logger.error(self.CLASS_NAME, "enrich", "Raw dataset is empty – aborting.")
            return df

        df = self._add_features(df)
        df = df.dropna()
        self.logger.info(
            self.CLASS_NAME,
            "enrich",
            f"Data enriched. Final shape after dropna: {df.shape}",
        )

        self._save_enriched(df)
        return df


    def _verify_folder(self, path: str) -> None:
        """Ensure *path* exists; create it if missing."""
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            self.logger.info(
                self.CLASS_NAME,
                "_verify_folder",
                f"Created missing folder at {path}",
            )

    def _load_raw_data(self) -> pd.DataFrame:
        """Read the raw CSV into a DataFrame."""
        try:
            df: pd.DataFrame = pd.read_csv(self.RAW_DATA_PATH)
            self.logger.info(
                self.CLASS_NAME,
                "_load_raw_data",
                f"Raw dataset loaded with shape {df.shape}",
            )
            # Ensure date column has correct dtype and sorted order
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.sort_values("date")
            return df
        except Exception as error:
            self.logger.error(
                self.CLASS_NAME,
                "_load_raw_data",
                f"Failed to load raw dataset: {error}",
            )
            return pd.DataFrame()

    def _add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer additional columns on *df* and return it."""
        try:
            df["day_of_week"] = df["date"].dt.dayofweek
            df["rolling_mean_7"] = df["close"].rolling(window=7).mean()
            df["rolling_std_7"] = df["close"].rolling(window=7).std()
            df["log_return"] = np.log(df["close"] / df["close"].shift(1))
            df["target"] = df["close"].shift(-1)
            self.logger.info(self.CLASS_NAME, "_add_features", "Feature engineering complete.")
            return df
        except Exception as error:
            self.logger.error(
                self.CLASS_NAME,
                "_add_features",
                f"Error during feature engineering: {error}",
            )
            return pd.DataFrame()

    def _save_enriched(self, df: pd.DataFrame) -> None:
        """Persist the enriched DataFrame."""
        try:
            df.to_csv(self.ENRICHED_DATA_PATH, index=False)
            self.logger.info(
                self.CLASS_NAME,
                "_save_enriched",
                f"Enriched data saved to {self.ENRICHED_DATA_PATH}",
            )
        except Exception as error:
            self.logger.error(
                self.CLASS_NAME,
                "_save_enriched",
                f"Failed to save enriched data: {error}",
            )
