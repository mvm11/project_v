"""Dashboard module.

This module generates a static dashboard using Matplotlib to visualize key
indicators related to crude-oil pricing. Charts and KPIs are saved to the
static folder.
"""

from __future__ import annotations

from typing import Final
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class Dashboard:
    CLASS_NAME: Final[str] = "Dashboard"
    DATA_PATH: Final[str] = "src/crude_oil/static/data/crude_oil_enriched.csv"
    OUTPUT_FOLDER: Final[str] = "src/crude_oil/static/dashboard"

    def __init__(self) -> None:
        self.data: pd.DataFrame = pd.DataFrame()
        os.makedirs(self.OUTPUT_FOLDER, exist_ok=True)

    def run(self) -> None:
        """Generate static visual dashboard and save charts and KPIs to disk."""
        self.data = self._load_data()
        if self.data.empty:
            print("[Dashboard] Dataset is empty. Dashboard not generated.")
            return

        kpis = self._compute_kpis(self.data)
        self._save_kpis_table(kpis)
        self._save_price_chart(self.data)
        self._save_log_return_chart(self.data)

    def _load_data(self) -> pd.DataFrame:
        try:
            df: pd.DataFrame = pd.read_csv(self.DATA_PATH)
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date")
            return df
        except Exception:
            return pd.DataFrame()

    def _compute_kpis(self, df: pd.DataFrame) -> dict[str, float]:
        return {
            "Tasa de Variación (%)": ((df["close"].iloc[-1] - df["close"].iloc[-2]) / df["close"].iloc[-2]) * 100,
            "Media Móvil 7 días": df["rolling_mean_7"].iloc[-1],
            "Volatilidad 7 días": df["rolling_std_7"].iloc[-1],
            "Retorno Acumulado (%)": ((df["close"].iloc[-1] / df["close"].iloc[0]) - 1) * 100,
            "Desviación Estándar Precio": df["close"].std(),
        }

    def _save_kpis_table(self, kpis: dict[str, float]) -> None:
        df_kpis = pd.DataFrame(kpis.items(), columns=["Indicador", "Valor"])
        output_path = os.path.join(self.OUTPUT_FOLDER, "kpis.csv")
        df_kpis.to_csv(output_path, index=False)
        print(f"[Dashboard] KPIs saved to: {output_path}")

    def _save_price_chart(self, df: pd.DataFrame) -> None:
        plt.figure(figsize=(10, 4))
        plt.plot(df["date"], df["close"], label="Precio de Cierre")
        plt.title("Evolución del Precio de Cierre")
        plt.xlabel("Fecha")
        plt.ylabel("Precio")
        plt.grid(True)
        plt.tight_layout()
        output_path = os.path.join(self.OUTPUT_FOLDER, "close_price_chart.png")
        plt.savefig(output_path)
        plt.close()
        print(f"[Dashboard] Precio de cierre chart saved to: {output_path}")

    def _save_log_return_chart(self, df: pd.DataFrame) -> None:
        plt.figure(figsize=(10, 4))
        plt.plot(df["date"], df["log_return"], label="Retorno Logarítmico Diario", color="orange")
        plt.title("Retorno Logarítmico Diario")
        plt.xlabel("Fecha")
        plt.ylabel("Log Return")
        plt.grid(True)
        plt.tight_layout()
        output_path = os.path.join(self.OUTPUT_FOLDER, "log_return_chart.png")
        plt.savefig(output_path)
        plt.close()
        print(f"[Dashboard] Log return chart saved to: {output_path}")


# Optional script entry point
if __name__ == "__main__":
    Dashboard().run()
