import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from binance.client import Client
import pandas as pd
import time


class BinanceDataFetcher:
    API_KEY = "ItFMygh3PlB7ftuFKdX9qx2ewTu2O8azEjZAvhzDZdbX2L2ih8OVws2uS27YScQs"
    API_SECRET = "plDC99R0tFZ3wYN0pbC5SkuexnoYSBg0eCIJoBLpiq2tFPswFFlVrf0xZz8BOyKb"
    SYMBOL = "BTCUSDT"
    INTERVAL = Client.KLINE_INTERVAL_1MINUTE

    @classmethod
    def fetch_ohlcv_to_csv(cls, start_date, end_date, file_name):
        """Fetch fixed-symbol OHLCV data and save to CSV."""
        client = Client(cls.API_KEY, cls.API_SECRET)
        print(f"Fetching data for {cls.SYMBOL} from {start_date} to {end_date}...")
        
        klines = []
        start_ts = int(pd.Timestamp(start_date).timestamp() * 1000)
        end_ts = int(pd.Timestamp(end_date).timestamp() * 1000)

        while start_ts < end_ts:
            new_candles = client.get_klines(
                symbol=cls.SYMBOL, interval=cls.INTERVAL, startTime=start_ts, limit=1000
            )
            if not new_candles:
                break

            klines.extend(new_candles)
            start_ts = new_candles[-1][0] + 1
            time.sleep(0.5)

        if not klines:
            print("No data fetched.")
            return

        df = pd.DataFrame(klines, columns=[
            "Time", "Open", "High", "Low", "Close", "Volume", "CloseTime",
            "QuoteAssetVolume", "Trades", "TakerBaseVolume", "TakerQuoteVolume", "Ignore"
        ])
        df["Time"] = pd.to_datetime(df["Time"], unit="ms")
        df[["Open", "High", "Low", "Close", "Volume"]] = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

        folder = "data"
        os.makedirs("data", exist_ok=True)
        file_path = os.path.join(folder,file_name)
        df.to_csv(file_path, index=False)

        print(f"Data saved to {file_name} successfully!")
        print(df.head())

# ---------------- Usage ----------------
if __name__ == "__main__":
    BinanceDataFetcher.fetch_ohlcv_to_csv(
        start_date="2025-05-08",
        end_date="2025-05-09",
        file_name="BTCUSDT_May_1d.csv"
    )
