import pandas as pd
from collector import Collector
from logger import Logger

def main():

    logger = Logger()
    df = pd.DataFrame()
    logger.info('Main','main','Inicializar clase Logger')
    collector = Collector(logger=logger)
    
    df = collector.get_crude_oil_data()
    df.to_csv("src/crude_oil/static/data/crude_oil.csv", index=False)




if __name__ == "__main__":
    main()