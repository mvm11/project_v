"""Modeller module.

This module contains the Modeller class, responsible for training and
serving a linear regression model to predict future crude‑oil prices.
The class mirrors the structure and logging style of the Collector class.
"""

from __future__ import annotations

import os
from typing import Tuple, Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

from logger import Logger


class Modeller:
    CLASS_NAME: str = "Modeller"

    # Paths
    DATA_FILE_PATH: str = "src/crude_oil/static/data/crude_oil_enriched.csv"
    MODEL_FOLDER_PATH: str = "src/crude_oil/static/models"
    MODEL_FILE_PATH: str = os.path.join(MODEL_FOLDER_PATH, "model.pkl")

    # Feature / target definition
    FEATURES: list[str] = [
        "close",
        "rolling_mean_7",
        "rolling_std_7",
        "log_return",
        "day_of_week",
    ]
    TARGET: str = "target"

    def __init__(self, logger: Logger) -> None:
        """Create a Modeller instance and verify required folders exist."""
        self.logger: Logger = logger
        self._verify_folder(self.MODEL_FOLDER_PATH)


    def train(self) -> None:
        """Train a LinearRegression model and store it."""
        df: pd.DataFrame = self._load_dataset()
        if df.empty:
            self.logger.error(self.CLASS_NAME, "train", "Empty dataset – aborting training.")
            return

        X, y = self._split_features_target(df)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        self.logger.info(self.CLASS_NAME, "train", "Dataset split into train/test subsets.")

        model: LinearRegression = LinearRegression()
        model.fit(X_train, y_train)
        self.logger.info(self.CLASS_NAME, "train", "Model successfully trained.")

        # Evaluation
        y_pred: np.ndarray = model.predict(X_test)
        rmse: float = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae: float = float(mean_absolute_error(y_test, y_pred))
        self.logger.info(
            self.CLASS_NAME,
            "train",
            f"Evaluation metrics → RMSE={rmse:.4f}, MAE={mae:.4f}",
        )

        # Persist model
        self._save_model(model)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Generate predictions for the provided feature DataFrame."""
        model: Optional[LinearRegression] = self._load_model()
        if model is None:
            return np.array([])

        try:
            predictions: np.ndarray = model.predict(X)
            self.logger.info(
                self.CLASS_NAME,
                "predict",
                f"Generated predictions for {len(predictions)} records.",
            )
            return predictions
        except Exception as error:  # noqa: BLE001
            self.logger.error(self.CLASS_NAME, "predict", f"Prediction error: {error}")
            return np.array([])


    def _verify_folder(self, path: str) -> None:
        """Ensure *path* exists; create it if missing."""
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            self.logger.info(
                self.CLASS_NAME,
                "_verify_folder",
                f"Created missing folder at {path}",
            )

    def _load_dataset(self) -> pd.DataFrame:
        """Load the enriched crude‑oil dataset from disk."""
        try:
            df: pd.DataFrame = pd.read_csv(self.DATA_FILE_PATH)
            self.logger.info(
                self.CLASS_NAME,
                "_load_dataset",
                f"Dataset loaded with shape {df.shape}",
            )
            return df
        except Exception as error:  # noqa: BLE001
            self.logger.error(
                self.CLASS_NAME,
                "_load_dataset",
                f"Failed to load dataset: {error}",
            )
            return pd.DataFrame()

    def _split_features_target(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Return X (features) and y (target) DataFrames ready for training."""
        X: pd.DataFrame = df[self.FEATURES]
        y: pd.Series = df[self.TARGET]
        self.logger.info(self.CLASS_NAME, "_split_features_target", "Features and target extracted.")
        return X, y

    def _save_model(self, model: LinearRegression) -> None:
        """Persist the trained model to disk."""
        try:
            joblib.dump(model, self.MODEL_FILE_PATH)
            self.logger.info(
                self.CLASS_NAME,
                "_save_model",
                f"Model saved at {self.MODEL_FILE_PATH}",
            )
        except Exception as error:
            self.logger.error(
                self.CLASS_NAME,
                "_save_model",
                f"Error saving model: {error}",
            )

    def _load_model(self) -> Optional[LinearRegression]:
        """Load the persisted model from disk; return *None* on failure."""
        try:
            model: LinearRegression = joblib.load(self.MODEL_FILE_PATH)
            self.logger.info(self.CLASS_NAME, "_load_model", "Model loaded successfully.")
            return model
        except Exception as error:
            self.logger.error(self.CLASS_NAME, "_load_model", f"Error loading model: {error}")
            return None
