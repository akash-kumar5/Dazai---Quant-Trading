import pandas as pd

def generate_signals(df):
    """Generates basic buy/sell signals based on OI & IV."""
    signals = []

    for _, row in df.iterrows():
        strike = row["STRIKE"]
        call_oi = row["Call OI"]
        call_iv = row["Call IV"]
        put_oi = row["Put OI"]
        put_iv = row["Put IV"]

        signal = None

        # BUY CALL: High Call OI increase + High IV
        if call_oi > 100000 and call_iv > 20:  
            signal = f"BUY CALL {strike}"

        # BUY PUT: High Put OI increase + High IV
        elif put_oi > 100000 and put_iv > 20:
            signal = f"BUY PUT {strike}"

        # SELL CALL: Call OI Drop
        elif call_oi < 50000:
            signal = f"SELL CALL {strike}"

        # SELL PUT: Put OI Drop
        elif put_oi < 50000:
            signal = f"SELL PUT {strike}"

        if signal:
            signals.append(signal)

    return signals
