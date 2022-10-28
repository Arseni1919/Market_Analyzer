import pandas as pd

from globals import *


def get_data():
    client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

    request_params = StockBarsRequest(
        symbol_or_symbols=['SPY'],
        timeframe=TimeFrame.Hour,
        start="2022-01-01 00:00:00"
    )
    bars = client.get_stock_bars(request_params)
    bars_dict = {
        'index': [],
        'open': [],
        'close': [],
        'high': [],
        'low': [],
    }
    for b in bars.data['SPY']:

        bars_dict['index'].append(b.timestamp)
        bars_dict['open'].append(b.open)
        bars_dict['close'].append(b.close)
        bars_dict['high'].append(b.high)
        bars_dict['low'].append(b.low)
    bars_df = pd.DataFrame(bars_dict)
    print(bars_df)
    bars_df.plot()
    plt.show()


def main():
    get_data()


if __name__ == '__main__':
    dotenv.load_dotenv()
    API_KEY = os.environ['API_KEY']
    SECRET_KEY = os.environ['SECRET_KEY']

    main()
