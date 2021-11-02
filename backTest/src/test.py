import pandas as pd
import numpy as np
import os
from datetime import date

from backtesting import Backtest
from .strategies.crossover import SmaCross
from .strategies.BuyOnEven import BuyOnEven
from .strategies.aligartor_indicator import AligatorIndicator

html_dir = "html"

#Collect Data from CSV base on its Stock name
def datafromcsv(Stock, start_date=np.datetime64(date(2000, 1, 1)), end_date=np.datetime64(date(2020, 1, 1))):
    data = pd.read_csv("ressources/testData/"+ Stock + ".csv")
    columns = ['Date', 'Volume', 'Open', 'High', 'Low', 'Close', 'adjclose']
    data.columns = columns
    data = data.set_index("Date")
    data.index= pd.to_datetime(data.index)
    data = data.sort_index()
    data = data.iloc[ lambda x: x.index > start_date] 
    data = data.iloc[ lambda x: x.index < end_date]
    return data

def run(strategy=AligatorIndicator, strategy_str="AligatorIndicator"):
    bt = Backtest(datafromcsv("AAPL"), strategy, commission=0,
                exclusive_orders=True, cash=100000)
    stats = bt.run()

    if not os.path.exists(html_dir):
        os.mkdir(html_dir)

    bt.plot(filename='./' + html_dir + '/' + strategy_str)