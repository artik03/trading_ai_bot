import datetime
import numpy as np
import pandas as pd
from getters_alpaca import get_closing_prices, get_open_values,get_high_values, get_low_values, get_close_values, get_volumes

# changeable variables (n represents number of time periods)
n_sma = 20
n_prediction = 8

# display to file
def display_data_to_file(data, file_name = 'output') -> None:
    np.savetxt(f'{file_name}.csv', data, delimiter=', ', fmt='%s')

# get range
def get_candles(data, cur: int, n: int):
    if n>=0:
       return data[cur:cur+n+1]
    if n<0:
       return data[cur+n:cur+1]

# calculations
def closing_price_change(data, cur:int, n: int) -> int:
    current_candle = data[cur]
    after_candle = data[cur+n]
    closing_price_change = get_closing_prices(current_candle) - get_closing_prices(after_candle)
    return closing_price_change   

def volume_sma(data, cur: int, n:int):
     data = get_candles(data, cur, -n)
     volumes = get_volumes(data)
     sma_value = np.mean(volumes)
     return sma_value

def sma(data, cur: int): # cur >= 20
    data = get_candles(data, cur, -n_sma)
    closing_prices = get_closing_prices(data)
    sma_value = np.mean(closing_prices)
    return sma_value

cashed_emas = {}
def ema(data, cur, soothing = 2): # cur >= 21
    if cur in cashed_emas: return cashed_emas[cur]
    if cur == n_sma:
        init_ema_value = sma(data, n_sma)
        cashed_emas[cur] = init_ema_value
        return init_ema_value
    
    current_candle = data[cur]
    cur_price = get_closing_prices(current_candle)
    ema_yesterday = ema(data, cur-1) 
    # python recursion limit 1000 - change to iterative approach/increse limit - should be ok always uses cashed values
    k = soothing / (1+n_sma)
    
    ema_value = (cur_price * k) + (ema_yesterday * (1-k))
    
    cashed_emas[cur] = ema_value
    
    return ema_value

def gon_from_seconds(time):
    seconds_in_day = 24*60*60
    radians = (time / seconds_in_day) * 2 * np.pi
    sine_time = np.sin(radians)
    cosine_time = np.cos(radians)
    return sine_time, cosine_time

def dfdate_to_gon(data):
    data_T = data.T 
    sine_values = []
    cosine_values = []
    for timestamp in data_T[0]:
        date, time = str(timestamp).split()
        hours, mins, seconds = time.split(":")
        in_seconds = int(hours)*3600 + int(mins)*60 + int(seconds)
        sine_time, cosine_time = gon_from_seconds(in_seconds)
        sine_values.append(sine_time)
        cosine_values.append(cosine_time)
    
    return np.array(sine_values), np.array(cosine_values)    

# filling data array
def fill_data(data): 
    sine_time_values, cosine_time_values = dfdate_to_gon(data)
    volumes = get_volumes(data)
    open_p = get_open_values(data)
    close_p = get_close_values(data)
    high_p = get_high_values(data)
    low_p = get_low_values(data)
    
    m, n = data.shape
    new_data = np.empty((m-n_sma-n_prediction, 13))
    
    # start from n_sma+1 since we need 21 candles before for it, -n_prediction-1 for same reason
    for i in range(n_sma,len(data)-n_prediction): # <20; 992) length: 1000-20-8
        new_data[i-n_sma][0] = closing_price_change(data, i, n_prediction)
        new_data[i-n_sma][1] = sma(data, i)
        new_data[i-n_sma][2] = ema(data, i)
        new_data[i-n_sma][3] = sine_time_values[i]
        new_data[i-n_sma][4] = cosine_time_values[i]
        new_data[i-n_sma][5] = volumes[i]
        new_data[i-n_sma][6] = volume_sma(data, i, 3)
        new_data[i-n_sma][7] = volume_sma(data, i, 8)
        new_data[i-n_sma][8] = volume_sma(data, i, 20)
        new_data[i-n_sma][9] = open_p[i]
        new_data[i-n_sma][10] = close_p[i]
        new_data[i-n_sma][11] = low_p[i]
        new_data[i-n_sma][12] = high_p[i]
             
    return new_data

def get_newest_data(data):
    sine_time_values, cosine_time_values = dfdate_to_gon(data)
    volumes = get_volumes(data)
    open_p = get_open_values(data)
    close_p = get_close_values(data)
    high_p = get_high_values(data)
    low_p = get_low_values(data)
    
    new_data = np.empty((15, 12))
    
    for i in range(len(data)-14,len(data)): # get data for 15 most recent candles
        new_data[i-n_sma][0] = sma(data, i)
        new_data[i-n_sma][1] = ema(data, i)
        new_data[i-n_sma][2] = sine_time_values[i]
        new_data[i-n_sma][3] = cosine_time_values[i]
        new_data[i-n_sma][4] = volumes[i]
        new_data[i-n_sma][5] = volume_sma(data, i, 3)
        new_data[i-n_sma][6] = volume_sma(data, i, 5)
        new_data[i-n_sma][7] = volume_sma(data, i, 8)
        new_data[i-n_sma][8] = open_p[i]
        new_data[i-n_sma][9] = close_p[i]
        new_data[i-n_sma][10] = low_p[i]
        new_data[i-n_sma][11] = high_p[i]
             
    return new_data