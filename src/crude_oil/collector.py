import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from logger import Logger


class Collector:
    CLASS_NAME = "Collector"
    DATA_FOLDER_PATH = 'src/crude_oil/static/data'
    STATIC_FOLDER_PATH = 'src/crude_oil/static'
    BASE_URL = 'https://finance.yahoo.com/quote/CL%3DF/history/?period1=967003200&period2=1746999065'

    def __init__(self, logger: Logger):
        self.logger = logger
        self.url = self.BASE_URL
        self._verify_folder(self.STATIC_FOLDER_PATH)
        self._verify_folder(self.DATA_FOLDER_PATH)

    def _verify_folder(self, path: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)
            self.logger.info(self.CLASS_NAME, "_verify_folder", f"Created missing folder at {path}")

    def get_crude_oil_data(self) -> pd.DataFrame:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(self.url, headers=headers)

            if not self._is_successful_response(response):
                self.logger.error(self.CLASS_NAME, "get_crude_oil_data", f"Error fetching data: HTTP {response.status_code}")
                return pd.DataFrame()

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('div[data-testid="history-table"] table')

            if table is None:
                self.logger.error(self.CLASS_NAME, "get_crude_oil_data", "Table with data-testid=history-table not found")
                return pd.DataFrame()

            headers = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            rows = [
                [td.get_text(strip=True) for td in tr.find_all('td')]
                for tr in table.tbody.find_all('tr')
                if len(tr.find_all('td')) == len(headers)
            ]

            df = self._build_dataframe(headers, rows)
            self.logger.info(self.CLASS_NAME, "get_crude_oil_data", f"Data successfully retrieved with shape {df.shape}")
            return df

        except Exception as error:
            self.logger.error(self.CLASS_NAME, "get_crude_oil_data", f"Error retrieving data from the URL: {error}")
            return pd.DataFrame()

    @staticmethod
    def _is_successful_response(response: requests.Response) -> bool:
        return response.status_code == 200

    @staticmethod
    def _build_dataframe(headers: list[str], rows: list[list[str]]) -> pd.DataFrame:
        column_mapping = {
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low.': 'low',
            'CloseClose price adjusted for splits.': 'close',
            'Adj CloseAdjusted close price adjusted for splits and dividend and/or capital gain distributions.': 'adj_close',
            'Volume': 'volume'
        }
        return pd.DataFrame(rows, columns=headers).rename(columns=column_mapping)