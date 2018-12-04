# stock_scraper
This program uses the alpha_vantage API in order to gather stock data 
and store in pandas dataFrames. It gets the high, low, open, close, volume and date of the top
500 stocks in the s&p 500 over 1 min intervals. This program stores the data each time it collects
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

## How to work
Need to fill in your own API key, can get a key [here](https://www.alphavantage.co/support/#api-key).
It needs to be placed in the global variable API_KEY in the stocks.py file.

Please Note: This can take about 3 hours to run, most of the time less than that. This is 
because alpha_vantage only allows so many requests in a given time period, so pauses are included.
I recommend splitting the task between multiple computers. To do this change range() in the 
generate_data method of Stocks class in stocks.py. You can manually split the data in half using
range(255) for the first half and range(255, 500) for the second (as an example). Then merge
the data when complete.
