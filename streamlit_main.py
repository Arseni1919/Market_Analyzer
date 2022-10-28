from datetime import datetime, timedelta
from globals import *
import streamlit as st

y_to_show_dict = {
    'All Ticks': ['open', 'close', 'high', 'low'],
    'Close': ['close'],
    'Volume': ['volume']
}


def get_from_time_final(time_period_option, last_time_frame, from_time_sidebar):
    if time_period_option == 'last_time_frame':
        # ('Hour', 'Day', 'Month', '3 Months', '6 Months', 'Year')
        return_dict = {
            'Hour': datetime.now() - timedelta(hours=1),
            'Day': datetime.now() - timedelta(days=1),
            'Month': datetime.now() - timedelta(days=30),
            '3 Months': datetime.now() - timedelta(days=60),
            '6 Months': datetime.now() - timedelta(days=180),
            'Year': datetime.now() - timedelta(days=365)
        }
        return return_dict[last_time_frame]
    if time_period_option == 'from_time_sidebar':
        return from_time_sidebar


@st.cache
def get_data(from_time, stock_option='SPY'):
    from_time_str = from_time.strftime("%Y-%m-%d %H:%M:%S")
    client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
    request_params = StockBarsRequest(
        symbol_or_symbols=[stock_option],
        timeframe=TimeFrame.Hour,
        start=from_time_str
    )
    bars = client.get_stock_bars(request_params)
    bars_dict = {
        'datetime': [],
        'open': [],
        'close': [],
        'high': [],
        'low': [],
        'volume': []
    }
    for b in bars.data[stock_option]:
        bars_dict['datetime'].append(b.timestamp)
        bars_dict['open'].append(b.open)
        bars_dict['close'].append(b.close)
        bars_dict['high'].append(b.high)
        bars_dict['low'].append(b.low)
        bars_dict['volume'].append(b.volume)
    bars_df = pd.DataFrame(bars_dict)
    return bars_df


def main():
    st.title("Analyzing The Markets")
    stock_option = st.sidebar.selectbox(
        'Pick a stock',
        ('SPY', 'TSLA', 'AAPL'))
    graphs_type = st.sidebar.radio('Graph Type: ', ('All Ticks', 'Close', 'Volume'))

    from_time = datetime.strptime("2022-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    time_period_option = st.sidebar.radio(
        "How to limit time:",
        ('last_time_frame', 'from_time_sidebar'))
    last_time_frame = st.sidebar.selectbox(
        'Last...',
        ('Hour', 'Day', 'Month', '3 Months', '6 Months', 'Year'),
        disabled=time_period_option!='last_time_frame'
    )
    from_time_sidebar = st.sidebar.date_input(
        label='From DateTime',
        value=from_time,
        disabled=time_period_option!='from_time_sidebar'
    )
    x_as_time = st.sidebar.checkbox('X as Time')

    from_time_final = get_from_time_final(time_period_option, last_time_frame, from_time_sidebar)
    stock_data_df = get_data(from_time_final, stock_option)
    # st.dataframe(stock_data_df)
    y_to_show = y_to_show_dict[graphs_type]
    if x_as_time:
        st.line_chart(stock_data_df, x='datetime', y=y_to_show)
    else:
        st.line_chart(stock_data_df, y=y_to_show)



if __name__ == '__main__':
    dotenv.load_dotenv()
    API_KEY = os.environ['API_KEY']
    SECRET_KEY = os.environ['SECRET_KEY']
    # st
    st.set_page_config(
        page_title="Markets",
        page_icon="✅",
        layout="wide",
    )
    main()
