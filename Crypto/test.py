# test_import.py

from indicators.sma import calculate_sma
import pandas as pd

print("SMA import successful")

data = pd.DataFrame({'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
result = calculate_sma(data, 3)
print(result)
