# import modules
import tickers
import stocks


def main():
    # Create tickers object
    stock_tickers = tickers.Tickers()

    # Create and generate the stocks_data object and main data
    stocks_data = stocks.Stocks(stock_tickers)
    stocks_data.generate_data()


if __name__ == "__main__":
    main()
