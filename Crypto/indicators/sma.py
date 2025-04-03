# indicators/sma.py

def calculate_sma(data, period):
    if len(data) < period:
        return None
    return data['close'].rolling(window=period).mean()
