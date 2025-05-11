import pandas as pd
from collector import Collector
from logger import Logger


class CrudeOilDataPipeline:
    OUTPUT_PATH = "src/crude_oil/static/data/crude_oil.csv"

    def __init__(self):
        self.logger = Logger()
        self.collector = Collector(logger=self.logger)

    def run(self) -> None:
        self.logger.info("CrudeOilDataPipeline", "run", "Starting data collection process")

        data_frame = self.collector.get_crude_oil_data()
        if not data_frame.empty:
            self._save_to_csv(data_frame)
        else:
            self.logger.warning("CrudeOilDataPipeline", "run", "No data collected to save")

    def _save_to_csv(self, df: pd.DataFrame) -> None:
        df.to_csv(self.OUTPUT_PATH, index=False)
        self.logger.info("CrudeOilDataPipeline", "_save_to_csv", f"Data saved to {self.OUTPUT_PATH}")


def main():
    pipeline = CrudeOilDataPipeline()
    pipeline.run()


if __name__ == "__main__":
    main()