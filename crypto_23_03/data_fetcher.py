import websocket
import json
import threading
import time
# from strategies.MovingAverageStrategy import MovingAverageStrategy
from strategies.VWAPStrategy import VWAPStrategy

strategy = VWAPStrategy(period=10)


def on_message(ws, message):
    data = json.loads(message)
    
    # Check for the expected event type
    if data.get('e') == "24hrTicker":
        # print(data)
        price = data.get('c')  # 'c' is the current close price
        symbol = data.get('s')  # 's' is the symbol
        timestamp = data.get('E')  # 'E' is the event time
        volume = data.get('v') # 'v' is the volume
        
        print(f"Received in main.py -> Price: {price}, Volume: {volume}")
        strategy.update(price, volume)
        strategy.generate_signal(price)


        # Display real-time data
        # print(f"Symbol: {symbol}, Price: {price}, Time: {timestamp}")
    else:
        print(f"Received unexpected message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

def on_open(ws):
    print("WebSocket connection opened")
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@ticker"],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))

def on_ping(ws, message):
    print(f"Received ping: {message}")
    ws.send(message, websocket.ABNF.OPCODE_PONG)
    print(f"Sent pong: {message}")

def run_socket():
    websocket.enableTrace(False)
    socket = 'wss://stream.binance.com:9443/ws'
    ws = websocket.WebSocketApp(
        socket,
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

    # Continuously keep the program running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated by user")
        