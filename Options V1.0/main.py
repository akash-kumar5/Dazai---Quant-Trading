from strategies.option_strategy import generate_signals
import requests
import pandas as pd

def fetch_nifty_option_chain():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Error fetching data from NSE")
        return None
    
    data = response.json()
    return data["records"]["data"]

def extract_option_data(option_chain):
    option_data = []

    for record in option_chain:
        strike_price = record["strikePrice"]
        
        call_oi = record.get("CE", {}).get("openInterest", 0)
        call_iv = record.get("CE", {}).get("impliedVolatility", 0)

        put_oi = record.get("PE", {}).get("openInterest", 0)
        put_iv = record.get("PE", {}).get("impliedVolatility", 0)

        option_data.append([strike_price, call_oi, call_iv, put_oi, put_iv])

    df = pd.DataFrame(option_data, columns=["Strike Price", "Call OI", "Call IV", "Put OI", "Put IV"])
    return df

if __name__ == "__main__":
    print("🔄 Fetching Nifty Option Chain...")
    option_chain = fetch_nifty_option_chain()
    
    if option_chain:
        df = extract_option_data(option_chain)
        signals = generate_signals(df)

        print("\n📢 Trading Signals:")
        for signal in signals:
            print(signal)
    else:
        print("❌ Could not fetch option chain data")
