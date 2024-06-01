from math import floor
import time
import numpy as np
import requests
import pandas as pd   


def get_data(coin: str, interval: str, limit: int):
    interval_int = {
        "1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
        "1h": 3600, "2h": 7200, "4h": 14400, "6h": 21600, "8h": 28800,
        "12h": 43200, "1d": 86400, "3d": 259200, "1w": 604800, "1M": 2592000
    }[interval]
    
    start_time = int(time.time() * 1000) - (interval_int*1000 * limit )
    print(f"start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time/1000))}")
    data = pd.DataFrame()
    
    while True: 
        temp_data = get_data_from_timestamp(coin, interval, start_time, min(1000, limit))
        data = pd.concat([data, temp_data], ignore_index=True)
        
        if temp_data.empty:
            print("break")
            break
        
        start_time = temp_data.iloc[-1]['close_time'] + 1
        limit -= 1000
        
    return data


def get_data_from_timestamp(coin: str, interval: str, start_time: int, limit: int = 1000):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": coin, 
        "interval": interval,     
        "limit": limit, 
        "startTime": start_time
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    df: pd.DataFrame = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
    df.drop(columns=["ignore"], inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    return df

def remove_cols(data:pd.DataFrame, *args: str): 
    data.drop(columns=[*args], inplace=True)
    return data

