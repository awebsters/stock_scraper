# API to get stock data
from alpha_vantage.timeseries import TimeSeries

# Helper libraries
import pandas as pd
import time
import logging

# TODO: Implement your own key
API_KEY = "<key>"


class Stocks:

    def __init__(self, tickers, out_file='../data/data.csv', user='Stocks', logger_name='Stocks'):
        """
        initializes the class with logger info, API TimSeries object, stockdata and output file

        :param tickers: an instance of the tickers class what will be used to generate the stocks data
        :param out_file: the file that will output the data
        :param user: the user that is shows in logging messages
        :param logger_name: the name of the logger
        """

        self.user = user
        self.logger_name = logger_name

        self.d = {'user': user}
        self.sLogger = logging.getLogger(logger_name)

        self.tickers = tickers

        self.out_file_name = out_file
        self._ts = TimeSeries(key=API_KEY, output_format='pandas')

        # pandas df that will stock all the stock data
        self._stock_data = pd.DataFrame([], columns=['date', 'open', 'high',
                                                     'low', 'close', 'volume'])

        self.sLogger.info('Initialization Complete of {}'.format(self.__str__()), extra=self.d)

    def output_data(self, data=None):
        """
        Outputs data to the output file (declared in initialization).
        Will default to storing in 'data.csv' in this src folder when directory is not found.

        :param data: Data that will be outputted to the file.
                    Defaulted to the classes _stock_data
        :return: None
        """

        if data is None:
            data = self._stock_data

        # Store the data
        try:
            with open(self.out_file_name, 'w') as outfile:
                data.to_csv(outfile)
        except FileNotFoundError:
            logger_message = "Error when opening file {}, defaulting to data.csv in src folder"
            logging.error(logger_message.format(self.out_file_name), extra=self.d)
            with open('data.csv', 'w') as outfile:
                data.to_csv(outfile)

    def generate_data(self):
        """
        The main loop of the program. Will generate the _stock_data and
        constantly output to the csv file.

        :return: None
        """

        # Loop through the tickers and generate data
        # Note if you want to run on multiple machines change this for loop range()
        for stock_ticker_index in range(len(self.tickers.tickers)):

            stock_ticker = self.tickers.tickers[stock_ticker_index]
            logging.info("Adding data for {}".format(stock_ticker), extra=self.d)

            # Get the data and stop for a minute when the API gives us an error
            # This error is related to the number of data requests u can make every minute
            try:
                data, meta_data = self._ts.get_intraday(symbol=stock_ticker, interval='1min', outputsize='full')
            except KeyError:
                logging_message = "Stopping for a minute according to Alpha Vantage rules"
                logging.info(logging_message, extra=self.d)
                time.sleep(61)
                data, meta_data = self._ts.get_intraday(symbol=stock_ticker, interval='1min', outputsize='full')

            # Edit the data to prepare for appending
            data.rename(columns={'1. open': 'open', '2. high': 'high',
                                 '3. low': 'low', '4. close': 'close',
                                 '5. volume': 'volume'}, inplace=True)
            data['date'] = data.index
            data.index = [stock_ticker] * len(data['date'])

            # Note if you want to generate additional features to the data,
            # here is the stop to do it before the append.
            # This script was used with the goal of stock prediction,
            # I recommend creating special feature based on your goals

            # Addend to current data
            self._stock_data = self._stock_data.append(data)

            # Output the data
            self.output_data()
            logging.info("Data Added and Written to File {}".format(self.out_file_name), extra=self.d)

    def __str__(self):

        out_str = "Tickers Object of user - {user} and logger - {logger}."
        return out_str.format(user=self.user, logger=self.logger_name)