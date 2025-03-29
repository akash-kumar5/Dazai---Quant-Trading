import pandas as pd

def generate_signals(data):
    signals = []

    for index, row in data.iterrows():
        buy_price = row['BID_CALL']
        sell_price = row['BID_PUT']
        oi_change = row['CHNG_IN_OI_CALL']  # Add this to your dataset
        iv_change = row['IV_CALL']  # Add this to your dataset
        
        # Entry Condition: Only Buy when IV is rising & OI is increasing
        if iv_change > 0 and oi_change > 0:
            signals.append((row['TIMESTAMP'], 'BUY', row['TYPE'], row['QTY'], buy_price, 'CONFIRMED'))
        
        # Exit Condition: Sell when IV starts dropping or price reaches target
        if iv_change < 0 or sell_price >= buy_price * 5:  # Example: 5x target
            signals.append((row['TIMESTAMP'], 'SELL', row['TYPE'], row['QTY'], sell_price, 'CONFIRMED'))
    
    return signals

