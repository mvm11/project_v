import requests
import pandas as pd
from bs4 import BeautifulSoup
from logger import Logger
import os

DATA_FOLDER_PATH = 'src/crude_oil/static/data'
STATIC_FOLDER_PATH = 'src/crude_oil/static'
BASE_URL = 'https://finance.yahoo.com/quote/CL%3DF/history/?period1=967003200&period2=1746999065'


def verify_static_folder():
    if not os.path.exists(STATIC_FOLDER_PATH):
        os.makedirs(STATIC_FOLDER_PATH)


def verify_data_folder():
    if not os.path.exists(DATA_FOLDER_PATH):
        os.makedirs(DATA_FOLDER_PATH)


class Collector:
    def __init__(self, logger):
        self.class_name = "Collector"
        self.url = BASE_URL
        self.logger = logger

        verify_static_folder()
        verify_data_folder()

    def get_crude_oil_data(self):
        try:
            df = pd.DataFrame()
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            response = requests.get(self.url, headers=headers)
            if response.status_code != 200:
                self.logger.error("Error fetching the crude oil data: {}".format(response.status_code))
                return df
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('div[data-testid="history-table"] table')
            if table is None:
                self.logger.error("Error al buscar la tabla data-testid=history-table")
                return df
            headerss = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            rows = []
            for tr in table.tbody.find_all('tr'):
                colums = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(colums) == len(headerss):
                    rows.append(colums)
            df = pd.DataFrame(rows, columns=headerss).rename(columns={
                'Date': 'date',
                'Open': 'open',
                'High': 'high',
                'Low.': 'low',
                'CloseClose price adjusted for splits.': 'close',
                'Adj CloseAdjusted close price adjusted for splits and dividend and/or capital gain distributions.': 'adj_close',
                'Volume': 'volume'
                
            })
            
            self.logger.info(self.class_name, "get_crude_oil_data", "Data successfully retrieved with shape {}".format(df.shape))

            return df
        except Exception as error:
            self.logger.error(self.class_name, "get_crude_oil_data", f"Error retrieving data from the URL: {error}")



