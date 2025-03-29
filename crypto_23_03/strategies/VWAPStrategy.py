from util.logger import log_signal

class VWAPStrategy:
    def __init__(self, period):
        self.period = period
        self.prices = []
        self.volumes = []

    def update(self, price, volume):
        price = float(price)
        volume = float(volume)

        self.prices.append(price)
        self.volumes.append(volume)

        if len(self.prices) > self.period:
            self.prices.pop(0)
            self.volumes.pop(0)

    def calculate_vwap(self):
        total_volume = sum(self.volumes)
    
    # Check if volume is zero to avoid division by zero
        if total_volume == 0 or len(self.prices) < self.period:
            return 0.0  # Explicitly return None

        vwap = sum(p * v for p, v in zip(self.prices, self.volumes)) / total_volume
        log_signal("VWAPStrategy", "VWAP Calculated", vwap)
        return float(vwap)


    def generate_signal(self, price):
        price = float(price)
        vwap = self.calculate_vwap()

        # Check if VWAP is a valid number
        if vwap == 0.0:
            # log_signal("VWAPStrategy", "HOLD", price, "VWAP not ready yet")
            return "HOLD"

        if price > vwap:
            log_signal("VWAPStrategy", "BUY", price, f"Price: {price} > VWAP: {vwap}")
            return "BUY"
        elif price < vwap:
            log_signal("VWAPStrategy", "SELL", price, f"Price: {price} < VWAP: {vwap}")
            return "SELL"
        else:
            log_signal("VWAPStrategy", "HOLD", price, f"Price: {price} = VWAP: {vwap}")
            return "HOLD"

