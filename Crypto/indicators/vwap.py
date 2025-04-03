import pandas as pd

def calculate_vwap(data):
    cumulative_vol_price = (data['close'] * data['volume']).cumsum()
    cumulative_vol = data['volume'].cumsum()
    vwap = cumulative_vol_price / cumulative_vol
    return vwap