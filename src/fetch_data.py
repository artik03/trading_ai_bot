import numpy as np
import requests
import pandas as pd   

def get_data(coin: str, interval: str, n_of_intervals: int):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": coin, 
        "interval": interval,     
        "limit": n_of_intervals   
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    df: pd.DataFrame = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
    print(df)
    df.drop(columns=["ignore"], inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    return df

def remove_cols(data:pd.DataFrame, *args: str): 
    data.drop(columns=[*args], inplace=True)
    return data
