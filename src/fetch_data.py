from math import floor
import time
import numpy as np
import requests
import pandas as pd   

# fetchin data using binance api

# 
def get_data(coin: str, interval: str, limit: int):
    """
    Fetches historical data for a given coin and interval from Binance API.

    Args:
        coin (str): The symbol of the coin to fetch data for.
        interval (str): The interval at which to fetch the data.
        limit (int): The maximum number of data points to fetch.

    Returns:
        pandas.DataFrame: The fetched historical data.
    """

    # Convert the interval string to the corresponding interval in seconds
    interval_to_seconds = {
        "1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
        "1h": 3600, "2h": 7200, "4h": 14400, "6h": 21600, "8h": 28800,
        "12h": 43200, "1d": 86400, "3d": 259200, "1w": 604800, "1M": 2592000
    }
    interval_int = interval_to_seconds[interval]

    # Calculate the start time for fetching the data
    start_time = int(time.time() * 1000) - (interval_int * 1000 * limit)

    # Print the start time
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time / 1000))}")

    # Initialize an empty DataFrame to store the fetched data
    data = pd.DataFrame()

    # Fetch the data in small chunks until the limit is reached
    while True:
        temp_data = get_data_from_timestamp(coin, interval, start_time, min(1000, limit))
        data = pd.concat([data, temp_data], ignore_index=True)

        if temp_data.empty:
            break

        start_time = temp_data.iloc[-1]['close_time'] + 1
        limit -= 1000

    return data


def get_data_from_timestamp(coin: str, interval: str, start_time: int, limit: int = 1000):
    """
    Fetches historical data for a given coin and interval from Binance API 
    within a specified time range.

    Args:
        coin (str): The symbol of the coin to fetch data for.
        interval (str): The interval at which to fetch the data.
        start_time (int): The start time of the data in milliseconds since epoch.
        limit (int): The maximum number of data points to fetch.

    Returns:
        pandas.DataFrame: The fetched historical data.
    """

    # Construct the API endpoint URL
    url = "https://api.binance.com/api/v3/klines"

    # Set the parameters for the API request
    params = {
        "symbol": coin, 
        "interval": interval, 
        "limit": limit, 
        "startTime": start_time 
    }

    # Send the GET request to the API
    response = requests.get(url, params=params)

    # Parse the response JSON into a DataFrame
    data = response.json()
    df: pd.DataFrame = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])

    # Drop the unnecessary 'ignore' column
    df.drop(columns=["ignore"], inplace=True)

    # Convert the 'timestamp' column to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    return df


def remove_cols(data:pd.DataFrame, *args: str): 
    data.drop(columns=[*args], inplace=True)
    return data

