import pandas as pd

# EMA Calculation Function
def calculate_ema(data, period):
    # Handle list input by converting to DataFrame
    if isinstance(data, list):
        data = pd.DataFrame({'close': data})

    # Validation
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data must be a Pandas DataFrame or a list")
    if 'close' not in data.columns:
        raise ValueError("'close' column not found in data")
    if len(data) < period:
        raise ValueError("Insufficient data for EMA calculation")

    # Calculate EMA
    return data['close'].ewm(span=period, adjust=False).mean()