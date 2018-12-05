# Libraries for web-scrapping
import requests
from bs4 import BeautifulSoup
import logging


class Tickers:

    FORMAT = '%(asctime)-15s %(user)-8s %(message)s'

    # Url with the company tickers
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    def __init__(self, user='tickers', logger_name='tickers'):
        """
        initializes the Tickers object

        :param user: the user to be shows in logging
        :param logger_name: the name of the logger
        """

        self.user = user
        self.logger_name = logger_name

        # Set up logger
        logging.basicConfig(format=self.FORMAT, level=logging.INFO)
        self.d = {'user': user}
        self.tLogger = logging.getLogger(logger_name)

        # setup request
        self.r = requests.get(self.url)

        # log the status code
        self.tLogger.info("Request Status: {}".format(self.r.status_code), extra=self.d)

        # log when the request fails and raise the error
        if not self.r.ok:
            self.tLogger.error("Request Failed", extra=self.d)
            self.r.raise_for_status()

        # set up BeautifulSoup
        self._soup = BeautifulSoup(self.r.content, features='html.parser')

        # find the correct tags
        self._table = self._soup.find('tbody')
        self._tr_tags = self._table.findChildren('tr')

        # get the tickers
        self.tickers = self.scrape_tickers()

        # log the completed initialization
        self.tLogger.info("Initialization Complete of {}".format(self.__str__()), extra=self.d)

    def scrape_tickers(self):
        """
        Get the tickers from the url

        :return: None
        """

        # Scrape the first 500 tickers
        tickers = []
        for tr_index in range(1, 501):
            tickers.append(self._tr_tags[tr_index].find('a').text)
        return tickers

    def __str__(self):
        out_str = "Tickers Object of user - {user} and logger - {logger}."
        return out_str.format(user=self.user, logger=self.logger_name)