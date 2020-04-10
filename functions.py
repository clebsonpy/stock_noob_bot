from yahooquery import Ticker
import datetime


def get_stock(symbol):
    try:
        symbol = symbol+'.SA'
        ticker = Ticker(symbol)
        df = ticker.history(period='1mo', interval='1d')
        value = df.close[-1]
        value_ = df.close[-2]
        percent_day = ((value - value_)/value_)*100
        return value, percent_day
    except:
        raise AttributeError(ticker.financial_data)

def main():
    print(get_stock('sula11'))


if __name__ == '__main__':
    main()
