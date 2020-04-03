from yahooquery import Ticker


def get_stock(symbol):
    symbol = symbol+'.SA'
    ticker = Ticker(symbol)
    data = ticker.financial_data.get(symbol)
    value = data.get('currentPrice')
    return value


def main():
    print(get_stock('PETR4'))


if __name__ == '__main__':
    main()
