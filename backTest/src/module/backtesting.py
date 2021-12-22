import numpy as np
import pandas as pd

import logging
logging.basicConfig(filename='debug.log', format='', level=logging.FATAL, filemode='w')

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
    def __init__(self, broker, size, entry_price, _type, _opening_date=None):
        self._broker = broker
        self._size = size
        self._entry_price = entry_price
        self._type = _type
        self._curr_cash = None
        self._opening_date = _opening_date
        self._closing_date = None

    def close(self):
        self._broker.close_trade(self)
    
    def current_value(self, current_price):
        return self._size * current_price
    
    @property
    def ret(self):
        ##Absolute return of the trade
        if self._type == 'buy':
            ret_per_share = self._broker._last_price - self._entry_price
        else:
            ret_per_share = self._entry_price - self._broker._last_price
        return self._size * ret_per_share

    @property
    def entry_value(self):
        return self._size * self._entry_price
        

class Broker:
    def __init__(self, *, data, cash,exclusive_orders=False):
        self.orders = []
        self.trades = []
        self.closed_trades = []
        self._exclusive_orders = exclusive_orders
        self._data = data
        self._cash = cash
        self.position = Position(self)

    # def next(self):
    #     self.process_orders()    

    def new_order(self, cash_value, _type):
        order = Order(self, cash_value,  _type)

        if self._exclusive_orders:
            for order in self.orders:
                order.cancel()
            for trade in self.trades:
                trade.close() 
        
        self.orders.append(order)

    def process_orders(self):
        try:
            _open = self._data.Open[-1]
        except IndexError:
            self.orders = []
            return

        for order in self.orders:
            if self._cash <= 0:
                break
            
            # Get the number of shares to buy
            size = int(np.floor(order._cash_value / _open))

            if not size == 0:
                self.open_trade(size, _open, order._type)
            
            self.orders.remove(order)

    def open_trade(self, size, current_price, trade_type):

        trade = Trade(self, size, current_price, trade_type, _opening_date = self._data.iloc[-1].name)
        self.trades.append(trade)

        if(trade._type == "buy"):
            self._cash -= trade.entry_value
            logging.info(f'{self._data.iloc[-1].name}, {self.value}, {self._cash}, open buy, {trade._size}, {trade.entry_value}, {self._data.Open[-1]}')
        if(trade._type == "sell"):
            self._cash += trade.entry_value
            logging.info(f'{self._data.iloc[-1].name}, {self.value}, {self._cash}, open sell, {trade._size}, {trade.entry_value}, {self._data.Open[-1]}')
        return trade

    def close_trade(self, trade):
        self.trades.remove(trade)

        if(trade._type == "buy"):
            self._cash += trade.current_value(self._data.Open[-1])
            logging.info(f'{self._data.iloc[-1].name}, {self.value}, {self._cash}, close buy, {trade._size}, {trade.current_value(self._data.Open[-1])}, {self._data.Open[-1]}')
        if(trade._type == "sell"):
            self._cash -= trade.current_value(self._data.Open[-1])
            logging.info(f'{self._data.iloc[-1].name}, {self.value}, {self._cash}, close sell, {trade._size}, {trade.current_value(self._data.Open[-1])}, {self._data.Open[-1]}')

        trade._closing_date = self._data.iloc[-1].name
        trade._curr_cash = self._cash
        self.closed_trades.append(trade)
        
    @property
    def value(self):
        out = 0
        for trade in self.trades:
            if trade._type == 'sell':
                out -= trade.current_value(self._data.Open[-1])
            else:
                out += trade.entry_value + trade.ret
        return out + self._cash
    
    @property
    def _last_price(self):
        return self._data.Close[-1]
    @property
    def _max_size(self):
        return np.floor(self._cash / self._last_price)



    
class Backtest:
    def __init__(self, data, strategy, commission=0.022, exclusive_orders=True ,cash=100000):
        self.data = data
        self.broker = Broker(data=data, cash=cash, exclusive_orders=exclusive_orders)
        self.strategy = strategy(broker=self.broker, data=data, cash=cash)
        self.commission = commission
        self.exclusive_orders = exclusive_orders

    def data_extend_order_day(self, strat_order, i):
        self.data["TradeType"].iloc[i] = strat_order

    def trades_to_csv(self):
        trades = self.broker.closed_trades

        trade_frame = pd.DataFrame(columns=["Opening Date", "Closing Date", "Type", "Volume", "Cash"])

        for trade in trades:
            trade_array = pd.Series([trade._opening_date, trade._closing_date, trade._type, trade._size, trade._curr_cash], index = trade_frame.columns)
            trade_frame = trade_frame.append(trade_array, ignore_index=True)

        trade_frame.to_csv('trades.csv')

    @property
    def process_day(self):
        self.broker.process_orders()

        self.strategy.init()
        self.strategy.next()

    def run(self):
        print(" 'Output': 'Running Backtest.'")
        try:
            for i in range(1, len(self.data.index)):
                data = self.data.iloc[:i]
                self.strategy.data = data
                self.broker._data = data

                self.process_day
        
            print(" 'Output': 'Saving Data.'")
            self.trades_to_csv()
        
        except Exception as e:
            print(" 'Output': 'Error Detected.'")
            raise e

        finally:
            print(" 'Output': 'Backtest Complete.'")

    def plot(self):
        pass
