# Stock Scraper
This program uses the [Alpha Vantage]((https://www.alphavantage.co/) API to collect stock data 
and store it in pandas data frames. It gets the high, low, open, close, volume and date of the top
500 stocks in the S&P500 in 1 minute intervals. This program stores the data each time it collects
new data into the designated file (defaulted to ../data/data.csv or data.csv when necessary).
This allows you to stop execution and still have the most recent data available.

There is a full data.csv file under data/data.csv of the default data generated. It is completely
free to download and use.

## Libraries
This program was built on the following libraries and version numbers in **Python 3.7**
* alpha_vantage - v2.1.0
* pandas - v0.23.4
* time - included in python
* logging - included in python
* requests - v2.20.1
* bs4 - v4.6.3

## How to use
You need to fill in your own API key. You can get a key [here](https://www.alphavantage.co/support/#api-key).
It needs to be placed in the global variable API_KEY in the stocks.py file.

Please Note: This can take about 3 hours to run, most of the time less than that. This is 
because Alpha Vantage only allows 5 requests per minute, so pauses are necessary.
I recommend splitting the task between multiple computers. To do this change range() in the 
generate_data method of Stocks class in stocks.py. You can manually split the stocks to fetch in half using
range(255) for the first half and range(255, 500) for the second (as an example). After the computers collect
the data you assign them, you can merge it yourself manually. The pandas function `concat` may be useful for this purpose.
