import numpy as np
import pandas as pd

from datetime import date
from abc import abstractmethod, ABCMeta

from ..indicators import moving_average


class Strategy(metaclass=ABCMeta):
    def __init__(self,broker, data=None, cash=None):
        self.data = data
        self.cash = cash
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

    def buy(self,
            size: float = 1):

        return self._broker.new_order(size, "buy")

    def sell(self,
             size: float = 1):

        return self._broker.new_order(size, "sell")

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
    def __init__(self , broker, size, order_type):
        self.__broker = broker
        self._size = size
        self._order_type = order_type
    def cancel(self):
        self.__broker.orders.remove(self)

class Trade:
    def __init__(self, broker, size, entry_price, trade_type):
        self.__broker = broker
        self._size = size
        self._entry_price = entry_price
        self._trade_type = trade_type
    
    def close(self):
        self.__broker.close_trade(self)
        if self._trade_type == 'buy':
            order = self.__broker.new_order(self._size,"sell")
        if self._trade_type == 'sell':
            order = self.__broker.new_order(self._size,"buy")
        #Warning!!!! order can be None
        self.__broker.orders.insert(0, order)
    
    @property
    def value(self):
        return abs(self._size)*self._entry_price
    
    @property
    def ret(self):
        ##Return of the trade
        return abs(self._size)*(self.__broker._last_price-self._entry_price)
    
    
        

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
        i = len(self._data) - 1
        self.process_orders()    

    def new_order(self, size, order_type):
        ## Args should be changend in the fuure for more functionality
        order = Order(self, size,  order_type)
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
            size = order._size
            ##print("request new trade")
            self.open_trade(size, _open, order._order_type)
            self.orders.remove(order)


    def open_trade(self, size, price, trade_type):
        trade = Trade(self, size, price, trade_type)
        self.trades.append(trade)
        return trade
    def close_trade(self, trade):
        self.trades.remove(trade)
        self.closed_trades.append(trade)
        self._cash += trade.ret
    
    
    @property
    def _last_price(self):
        return self._data.Close[-1]



    
class Backtest:
    def __init__(self, data, strategy, commission=0.022, exclusive_orders=True ,cash=100000):
        #print("Input strategy",strategy)
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

    def data_extend_order(self, strat_order, i):
        self.data["TradeType"].iloc[i] = strat_order

    def run(self):
        #Initialize the strategy first
        # I don't know if this is the right position for this. Might change in the future

        self.strategy.init()

        # Dirty Solutins maybe there is a better way to do this
        indicator_attrs = {attr: indicator for attr, indicator in self.strategy.__dict__.items() if attr != 'data' and attr != "cash" and attr != "_broker" and attr != "indicators" and attr != "order"}

        ##print(indicator_attrs)

        #data = self.data.copy(deep=False)

        for i in range(1, len(self.data.index)):
            #data = self.data.iloc[:i]
            self.strategy.data = self.data.iloc[:i]
            self.broker.data = self.data.iloc[:i]
            # Slice Indicators
            for attr in indicator_attrs:
                indicator=indicator_attrs[attr] 

                ##print(indicator.iloc[:i+1])
                setattr(self.strategy, attr, indicator.iloc[:i+1])
            
            self.broker.next()
            self.strategy.next()
            
            """ trades = self.strategy.get_order()
            if len(trades) == 0:
                out = ""
            else:
                out = trades[0]._trade_type
            self.data_extend_order(out, i)
            # print(self.strategy.data)
             """
        print (len(self.broker.closed_trades),len(self.broker.orders),len(self.broker.trades))
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
                ##print("requesting a buy order")
                self.position.close()
                self.buy()
            else:
                ##print("requesting a sell order")
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
