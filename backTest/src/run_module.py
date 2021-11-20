import pandas as pd
import numpy as np
from datetime import date



from .strategies.aligartor_indicator import AligatorIndicator
from .module import Backtest

#Collect Data from CSV base on its Stock name
def datafromcsv(Stock, start_date=np.datetime64(date(2000, 1, 1)), end_date=np.datetime64(date(2020, 1, 1))):
    data = pd.read_csv("utils/"+ Stock + ".csv")
    columns = ['Date', 'Volume', 'Open', 'High', 'Low', 'Close', 'adjclose']
    data.columns = columns
    data = data.set_index("Date")
    data.index= pd.to_datetime(data.index)
    data = data.sort_index()
    data = data.iloc[ lambda x: x.index > start_date] 
    data = data.iloc[ lambda x: x.index < end_date]
    return data

def run(strategy=AligatorIndicator, strategy_str="AligatorIndicator",data=datafromcsv("AAPL")):
    bt = Backtest(data, strategy, commission=.002,
                exclusive_orders=True)
    stats = bt.run()
    