import numpy as np
import pandas as pd

from datetime import date
from abc import abstractmethod, ABCMeta

from ..indicators import moving_average


class Strategy(metaclass=ABCMeta):
    def __init__(self,broker, data=None, cash=None):
        self.data = data
        self.indicators = []
        self._broker = broker
        self.order = None

        # self.init()

    def I(self, indicator_function, data, *args, **kwargs):
        indicator = indicator_function(data, *args, **kwargs)
        self.indicators.append(indicator)
        return indicator
    

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def next(self):
        pass

    def get_order(self):
        self.order = None
        self.init()
        self.next()
        self._broker.process_orders()
        return self._broker.trades

    def buy(self):
        return self._broker.new_order(self._broker._cash, "buy")

    def sell(self):
        return self._broker.new_order(self._broker._cash, "sell")

    @property
    def position(self):
        return self._broker.position

    @property
    def orders(self):
        return self._broker.orders

    @property
    def trades(self):
        return self._broker.trades

class Position:

    def __init__(self, broker):
        self._broker = broker

    def close(self):
        for trade in self._broker.trades:
            trade.close()


class Order:
    def __init__(self , broker, cash_value, _type):
        self._broker = broker
        self._cash_value = cash_value
        self._type = _type
    def cancel(self):
        self._broker.orders.remove(self)

class Trade:
    def __init__(self, broker, size_abs, entry_price, trade_type, _opening_date=None):
        self._broker = broker
        self._size_abs = size_abs
        self._entry_price = entry_price
        self._trade_type = trade_type
        self._curr_cash = None
        self._opening_date = _opening_date
        self._closing_date = None
    
    def close(self):
        self._broker.close_trade(self)
        if self._trade_type == 'buy':
            order = self._broker.new_order(self._size_abs * self._broker._data.iloc[-1]['Open'],"sell")
        if self._trade_type == 'sell':
            order = self._broker.new_order(self._size_abs * self._broker._data.iloc[-1]['Open'],"buy")
        #Warning!!!! order can be None
        self._broker.orders.insert(0, order)
    
    def current_value(self, current_price):
        return abs(self._size_abs) * current_price
    
    @property
    def ret(self):
        ##Absolute return of the trade
        return abs(self._size_abs) * (self._broker._last_price - self._entry_price)

    @property
    def entry_value(self):
        return abs(self._size_abs) * self._entry_price
    
    
        

class Broker:
    def __init__(self, *, data, cash,exclusive_orders=True):
        self.orders = []
        self.trades = []
        self.closed_trades = []
        self._exclusive_orders = exclusive_orders
        self._data = data
        self._cash = cash
        self.position = Position(self)


    def next(self):
        ##current time index
        # i = len(self._data) - 1
        self.process_orders()    

    def new_order(self, cash_value, _type):
        ## Args should be changend in the future for more functionality
        order = Order(self, cash_value,  _type)
        if self._exclusive_orders:
            for order in self.orders:
                order.cancel()
            for trade in self.trades:
                trade.close() 
        
        self.orders.append(order)
        return order

    def process_orders(self):
        data = self._data
        try:
            _open, high, low = data.Open[-1], data.High[-1], data.Low[-1]
            old_close = data.Close[-2]
        except IndexError:
            return

        for order in self.orders:
            ##needs to be a integer dont know how ?!
            size = np.floor(order._cash_value / _open)
            if (order._type == "buy" or (order._type == "sell")) and self._cash > 0 and not size == 0:
                self.open_trade(size, _open, order._type)
            
            self.orders.remove(order)


    def open_trade(self, cash_value, current_price, trade_type):
        trade = Trade(self, cash_value, current_price, trade_type, _opening_date = self._data.iloc[-1].name)

        if(trade._trade_type == "buy"):
            self._cash -= trade.entry_value
        if(trade._trade_type == "sell"):
            self._cash += trade.entry_value

        self.trades.append(trade)
        return trade

    def close_trade(self, trade):
        if(trade._trade_type == "buy"):
            self._cash += trade.current_value(self._data.Open[-1])
        if(trade._trade_type == "sell"):
            self._cash -= trade.current_value(self._data.Open[-1])

        self.trades.remove(trade)

        trade._closing_date = self._data.iloc[-1].name
        trade._curr_cash = self._cash
        self.closed_trades.append(trade)
        
    
    
    @property
    def _last_price(self):
        return self._data.Close[-1]
    @property
    def _max_size(self):
        return np.floor(self._cash / self._last_price)



    
class Backtest:
    def __init__(self, data, strategy, commission=0.022, exclusive_orders=True ,cash=100000):
        self.data = data
        self.broker = Broker(data=data, cash=cash ,exclusive_orders=exclusive_orders)
        self.strategy = strategy( broker = self.broker,data=data,cash=cash)
        self.commission = commission
        self.exclusive_orders = exclusive_orders

        

        self.creat_output_data_layout()

    def creat_output_data_layout(self):
        self.data["Cash"] = None
        self.data["TradeType"] = None
        self.data["TradeVolume"] = None
        self.data["TradeValue"] = None
        self.data["TradeStock"] = None
        self.data["TradeID"] = None
        self.data["TradePositionList"] = None

    def data_extend_order_day(self, strat_order, i):
        self.data["TradeType"].iloc[i] = strat_order

    def trades_to_csv(self):
        trades = self.broker.closed_trades

        trade_frame = pd.DataFrame(columns=["Opening Date", "Closing Date", "Type", "Volume", "Cash"])

        for trade in trades:
            trade_array = pd.Series([trade._opening_date, trade._closing_date, trade._trade_type, trade._size_abs, trade._curr_cash], index = trade_frame.columns)
            trade_frame = trade_frame.append(trade_array, ignore_index=True)

        trade_frame.to_csv('trades.csv')

    def run(self):
        #Initialize the strategy first
        # I don't know if this is the right position for this. Might change in the future

        self.strategy.init()

        # Dirty Solutins maybe there is a better way to do this
        indicator_attrs = {attr: indicator for attr, indicator in self.strategy.__dict__.items() if attr != 'data' and attr != "cash" and attr != "_broker" and attr != "indicators" and attr != "order"}

        #data = self.data.copy(deep=False)

        for i in range(1, len(self.data.index)):
            #data = self.data.iloc[:i]
            self.strategy.data = self.data.iloc[:i]
            self.broker._data = self.data.iloc[:i]
            # Slice Indicators
            for attr in indicator_attrs:
                indicator=indicator_attrs[attr] 

                setattr(self.strategy, attr, indicator.iloc[:i+1])
            
            self.broker.next()
            self.strategy.next()

        self.trades_to_csv()

        print (len(self.broker.closed_trades),len(self.broker.orders),len(self.broker.trades))
        print(self.broker._cash)
        self.data.to_csv('test.csv')

    def plot(self):
        pass

def aligator_indicator(green, red, blue):
    try:
        is_red_blue_crossover = red[-2] < blue[-2] and red[-1] > blue[-1]
        is_blue_red_crossover =  red[-2] > blue[-2] and red[-1] < blue[-1]
  

        green_over_blue = green[-1] > blue[-1]
        blue_over_green = green[-1] < blue[-1]

        green_over_red = green[-1] > red[-1]
        red_over_green = green[-1] < red[-1]

        if is_red_blue_crossover and green_over_blue and green_over_red:
            return True
        if is_blue_red_crossover and blue_over_green and red_over_green:
            return False
        return None
    except IndexError:
        return None

class AligatorIndicator(Strategy):
    def init(self):
        price = self.data.Close
        self.green = self.I(moving_average, price, 5, 3)
        self.red = self.I(moving_average, price, 8, 5)
        self.blue = self.I(moving_average, price, 13, 8)

    def next(self):
        indicator = aligator_indicator(self.green, self.red, self.blue)
        if indicator != None:
            if indicator:
                self.position.close()
                self.buy()
            else:
                self.position.close()
                self.sell()

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
    print("running")
    bt = Backtest(datafromcsv("AAPL"), strategy, commission=.002,
                exclusive_orders=True)
    stats = bt.run()

    # if not os.path.exists(html_dir):
    #     os.mkdir(html_dir)

    # bt.plot(filename='./' + html_dir + '/' + strategy_str)

# def run():
