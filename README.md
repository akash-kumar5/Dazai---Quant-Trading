# Dazai – Streamlit-Powered Crypto Strategy Backtester

**Dazai** is a modular Python trading system paired with a Streamlit dashboard that simulates simple crypto trading strategies. It helps visualize how a retail trader might behave across different market conditions using historical BTC/USD data.

You can backtest and visualize two core strategies — including one built on a combination of industry-standard technical indicators.

---

## 📊 Key Features

- 📈 Backtest BTC/USD data with just a CSV
- 🧠 Two strategies:
  - **Moving Average Crossover**
  - **EARA Strategy** (EMA, ADX, RSI, ATR combined)
- 🧮 Performance metrics: Win Rate, Sharpe Ratio, Drawdown
- 📉 Candlestick charts with buy/sell signal overlays
- ⚙️ Streamlit dashboard for quick testing and visualization

---

## 🧠 Strategies Explained

- **EMA Cross**  
  A simple moving average crossover strategy using short and long EMAs to generate trade signals.

- **EARA** (EMA-ADX-RSI-ATR Strategy)  
  A custom strategy combining:
  - **EMA** for trend detection  
  - **ADX** to filter trend strength  
  - **RSI** to spot momentum exhaustion  
  - **ATR** for volatility-aware conditions

---

## 🧱 Project Structure
.
├── backtest/
│ ├── backtester.py
│ └── result_analyzer.py
├── core/
│ ├── execution.py
│ ├── indicator.py
│ ├── regime_classifier.py
│ └── risk_manager.py
├── data/
│ └── btcusd_1h.csv
├── interface/
│ ├── pages/
│ │ ├── Loader.py
│ │ ├── Backtester.py
│ │ └── Visualizer.py
│ └── app.py
├── log/
│ ├── 2025-05-15_EARA_Strategy.csv
│ ├── 2025-07-06_EARA_Strategy.csv
│ └── 2025-07-06_Moving_Average_Strategy.csv
├── strategies/
│ ├── MA.py
│ └── EARA.py
├── utils/
│ ├── loader.py
│ ├── logger.py
│ ├── metrics.py
│ └── trade_visualizer.py
├── assets/
│ ├── dashboard.png
│ ├── ema_signals.png
│ ├── eara_strategy.png
│ └── backtester.png
├── README.md


## 🖥️ Dashboard Preview

![Dashboard Preview](assest/dashboard.png)

## 🚀 How to Run

Install requirements and launch the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Future Scope
- Add more technical strategies (MACD, Bollinger, VWAP, etc.)
- Live data feeds from Binance
- Reinforcement learning agent for adaptive trading
- Portfolio performance dashboard
