import numpy as np
from fetch_data import get_data, remove_cols
from helper import *
from getters_alpaca import *

coin_name = "LTCUSDT"
one_candle_intervals = "15m"
n_periods: int = 1000 # alpaca api limit

# get alpaca data
alpaca_data = get_data(coin_name, one_candle_intervals, n_periods)
alpaca_data = remove_cols(alpaca_data, "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume")

# turn it to np
alpaca_data = np.array(alpaca_data)

# make series with usefull data
data = fill_data(alpaca_data)
m, n = data.shape
np.random.shuffle(data)

data_dev = data[:900].T
label_dev = data_dev[0]
p_dev = data_dev[1:n]

data_train = data[900:m].T
label_train = data_train[0]
p_train = data_train[1:n]