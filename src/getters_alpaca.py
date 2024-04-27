from typing import List
import numpy as np

def get_closing_prices(data) -> List[float]:
    data_T = data.T
    closing_prices = data_T[4]
    closing_prices_float = np.array(closing_prices, dtype=float)
    
    return closing_prices_float

def get_volumes(data) -> List[float]:
    data_T = data.T 
    volumes = data_T[5]
    volumes_float = np.array(volumes, dtype=float)
    return volumes_float

def get_open_values(data):
    data_T = data.T 
    open_prices = data_T[1]
    op_float = np.array(open_prices, dtype=float)
    return op_float

def get_high_values(data):
    data_T = data.T 
    high_prices = data_T[2]
    hp_float = np.array(high_prices, dtype=float)
    return hp_float

def get_low_values(data):
    data_T = data.T 
    low_prices = data_T[3]
    low_float = np.array(low_prices, dtype=float)
    return low_float

def get_close_values(data):
    data_T = data.T 
    close_prices = data_T[4]
    close_float = np.array(close_prices, dtype=float)
    return close_float