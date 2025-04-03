import websocket
import json
import threading
import time
import pandas as pd
from strategies.multiInd import MultiIndicatorStrategy

# Initialize strategy
strategy = MultiIndicatorStrategy(rsi_period=3, macd_fast=3, macd_slow=6, macd_signal=3, vwap_period=3)

def on_message(ws, message):
    data = json.loads(message)

    if data.get('e') == "24hrTicker":
        price = float(data.get('c'))
        volume = float(data.get('v'))

        print(f"Received -> Price: {price}, Volume: {volume}")
        
        # Update strategy with new price and volume
        strategy.update(price, volume)

        # Generate and print signal if data is sufficient
        signal_df = strategy.generate_signals()
        if not signal_df.empty:
            print(f"Signal: {signal_df.iloc[-1]['Signal']}")
        else:
            # print("Not enough data to generate signals")
            pass

    else:
        print(f"Unexpected message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket closed: {close_status_code} - {close_msg}")

def on_open(ws):
    print("WebSocket opened")
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params": ["btcusdt@ticker"],
        "id": 1
    }))

def on_ping(ws, message):
    # print(f"Ping received: {message}")
    ws.send(message, websocket.ABNF.OPCODE_PONG)
    # print(f"Pong sent: {message}")

def run_socket():
    websocket.enableTrace(False)
    socket_url = 'wss://stream.binance.com:9443/ws'
    ws = websocket.WebSocketApp(
        socket_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open,
        on_ping=on_ping
    )
    ws.run_forever(ping_interval=30, ping_timeout=10)

if __name__ == "__main__":
    socket_thread = threading.Thread(target=run_socket)
    socket_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminated by user")
