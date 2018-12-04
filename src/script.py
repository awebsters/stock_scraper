import tickers
import stocks


def main():
    stock_tickers = tickers.Tickers()
    stocks_data = stocks.Stocks(stock_tickers)
    stocks_data.generate_data()


if __name__ == "__main__":
    main()
