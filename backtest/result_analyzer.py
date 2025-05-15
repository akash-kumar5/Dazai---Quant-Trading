import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import csv
from datetime import datetime
import util.metrics as metric

class ResultAnalyzer:
    def analyze_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"[ERROR] Log file '{file_path}' not found.")
            return

        trades = self.read_logs(file_path)
        print(trades)
        if not trades:
            return None
        else:
           return self.get_metrics_dict(trades)

    def read_logs(self, file_path):
        """Read the log CSV file and return parsed trades."""
        trades = []
        previous_price = None
        previous_signal = None

        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)

                # Validate header
                required_fields = {"Timestamp", "Price", "Signal Type"}
                if not reader.fieldnames or not required_fields.issubset(reader.fieldnames):
                    print(f"[ERROR] Missing required headers. Found: {reader.fieldnames}")
                    return trades

                for row in reader:
                    raw_signal = row["Signal Type"].strip()
                    price_str = row["Price"].strip()

                    if "Signal:" in raw_signal:
                        signal = raw_signal.split("Signal:")[1].strip()
                    else:
                        signal = raw_signal

                    if signal not in ["BUY", "SELL"] or not price_str:
                        continue

                    price = float(price_str)

                    if signal == "BUY":
                        previous_price = price
                        previous_signal = "BUY"
                    elif signal == "SELL" and previous_price is not None and previous_signal == "BUY":
                        pnl = price - previous_price
                        trades.append({
                            "timestamp": row["Timestamp"],
                            "entry_price": previous_price,
                            "exit_price": price,
                            "signal": "SELL",
                            "pnl": pnl
                        })
                        previous_price = None
                        previous_signal = None

        except Exception as e:
            print(f"[ERROR] Failed to read the log file. {e}")

        return trades


    def get_metrics_dict(self, trades):
        return {
            # "Total Trades": len(trades),
            "Total Return": round(metric.total_return(trades), 2),
            "Average Return": round(metric.average_return(trades), 2),
            "Win Rate (%)": round(metric.win_rate(trades) * 100, 2),
            "Loss Rate (%)": round(metric.loss_rate(trades) * 100, 2),
            "Max Drawdown": round(metric.max_drawdown(trades), 2),
            "Profit Factor": round(metric.profit_factor(trades), 2),
            "Sortino Ratio": round(metric.sortino_ratio(trades), 2),
            "Expectancy": round(metric.expectancy(trades), 2),
            "Average Win": round(metric.avg_win(trades), 2),
            "Average Loss": round(metric.avg_loss(trades), 2),
            "Sharpe Ratio": round(metric.sharpe_ratio(trades), 2),
            "Payoff Ratio": round(metric.payoff_ratio(trades), 2),
        }

# Optional: Run directly if this file is executed standalone
if __name__ == "__main__":
    ResultAnalyzer()
