from util.logger import log_signal

class MovingAverageStrategy:
    def __init__(self):
        self.data = []  # Store received prices

    def on_price_update(self, symbol, price, timestamp):
        # Ensure price is a float
        try:
            price = float(price)  # Convert price to float
        except ValueError:
            print(f"Invalid price format: {price}")
            return
        
        print(f"Strategy received data - Symbol: {symbol}, Price: {price}, Time: {timestamp}")
        
        # Add your logic here, e.g., strategy execution
        self.data.append(price)
        # Example: Simple strategy logic
        if len(self.data) > 5:
            avg_price = sum(self.data[-5:]) / 5
            signal = "BUY" if price > avg_price else "SELL"
            log_signal("MovingAverageStrategy", signal, price, timestamp)
