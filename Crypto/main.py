import websocket
import json
import threading
import time
import pandas as pd
from strategies.EARA import TrendSurferStrategy

# Initialize strategy
strategy = TrendSurferStrategy()

def on_message(ws, message):
    data = json.loads(message)

    if data.get('e') == "24hrTicker":
        price = float(data.get('c'))
        volume = float(data.get('v'))
        high = float(data.get('h'))
        low = float(data.get('l'))

        print(f"Received -> Price: {price},High: {high}, Low: {low}, Volume: {volume}")
        
        # Update strategy with new price and volume
        strategy.update(price,high, low, volume)

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
