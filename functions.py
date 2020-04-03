from yahooquery import Ticker


def get_stock(symbol):
    symbol = symbol+'.SA'
    ticker = Ticker(symbol)
    value = ticker.financial_data.get(symbol).get('currentPrice')
    return value


def main():
    print(get_stock('PETR4'))


if __name__ == '__main__':
    main()
