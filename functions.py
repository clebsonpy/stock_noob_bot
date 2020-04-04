from yahooquery import Ticker


def get_stock(symbol):
    try:
        symbol = symbol+'.SA'
        ticker = Ticker(symbol)
        data = ticker.financial_data.get(symbol)
        value = data.get('currentPrice')
        return value
    except AttributeError:
        raise AttributeError(ticker.financial_data)


def main():
    print(get_stock('PETR'))


if __name__ == '__main__':
    main()
