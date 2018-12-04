# API to get stock data
from alpha_vantage.timeseries import TimeSeries

# Helper libraries
import pandas as pd
import time
import logging
from math import floor

API_KEY = "ANN6AN4B37D0W8EV"


class Stocks:
    def __init__(self, tickers, out_file='../data/data.csv', user='Stocks', logger_name='Stocks'):
        self.user = user
        self.logger_name = logger_name

        self.d = {'user': user}
        self.sLogger = logging.getLogger(logger_name)

        self.tickers = tickers

        self.out_file_name = out_file
        self._ts = TimeSeries(key=API_KEY, output_format='pandas')
        self._stock_data = pd.DataFrame([], columns=['date', 'open', 'high',
                                                     'low', 'close', 'volume'])

        self.sLogger.info('Initialization Complete of {}'.format(self.__str__()), extra=self.d)

    def output_data(self, data=None):
        if data is None:
            data = self._stock_data
        try:
            with open(self.out_file_name, 'w') as outfile:
                data.to_csv(outfile)
        except FileNotFoundError:
            logger_message = "Error when opening file {}, defaulting to data.csv in src folder"
            logging.error(logger_message.format(self.out_file_name), extra=self.d)
            with open('data.csv', 'w') as outfile:
                data.to_csv(outfile)

    def generate_data(self):
        for stock_ticker_index in range(len(self.tickers.tickers)):

            stock_ticker = self.tickers.tickers[stock_ticker_index]
            logging.info("Adding data for {}".format(stock_ticker), extra=self.d)

            try:
                data, meta_data = self._ts.get_intraday(symbol=stock_ticker, interval='1min', outputsize='full')
            except KeyError:
                logging_message = "Stopping for a minute according to Alpha Vantage rules"
                logging.info(logging_message, extra=self.d)
                time.sleep(61)
                data, meta_data = self._ts.get_intraday(symbol=stock_ticker, interval='1min', outputsize='full')

            data.rename(columns={'1. open': 'open', '2. high': 'high',
                                 '3. low': 'low', '4. close': 'close',
                                 '5. volume': 'volume'}, inplace=True)
            data['date'] = data.index
            data.index = [stock_ticker] * len(data['date'])

            self._stock_data = self._stock_data.append(data)

            self.output_data()
            logging.info("Data Added and Written to File {}".format(self.out_file_name), extra=self.d)


    def __str__(self):
        out_str = "Tickers Object of user - {user} and logger - {logger}."
        return out_str.format(user=self.user, logger=self.logger_name)