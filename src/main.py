import numpy as np
from fetch_data import get_data, remove_cols
from helper import *
from getters_alpaca import *
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import time
import requests 


coin_name = "LTCUSDT"
interval = "15m"
limit: int = 100000

from fetch_data import get_data, remove_cols
# get alpaca data
alpaca_data = get_data(coin_name, interval, limit)
alpaca_data = remove_cols(alpaca_data, "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume")
# turn it to np
alpaca_data = np.array(alpaca_data)

