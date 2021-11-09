import numpy as np
import pandas as pd

import logging
logging.basicConfig(filename='debug.log', format='', level=logging.INFO, filemode='w')

class Stock:
    def __init__(self, id, stock_id, name, broker, _type, saved_cash=None):
        self.id = id
        self.stock_id = stock_id
        self.name = name
        self._broker = broker
        self.saved_cash = saved_cash

        assert _type in ['own', 'short'], 'Stock type must be own or short.'
        self._type = _type

    def __repr__(self):
        return f'Sock({self.id}, {self.stock_id}, {self._type})'


class Position:
    def __init__(self, broker):
        self._broker = broker
        self.stocks = dict()

    def add(self, stock):
        if not stock.stock_id in self.stocks:
            self.stocks[stock.stock_id] = {'own' : [], 'short' : []}

        assert stock._type in ['own', 'short'] , 'Stock type must be own or short.'
        
        self.stocks[stock.stock_id][stock._type].append(stock)

    def remove_first_i_stocks(self, stock_id, stock_type, size):
        if not stock_id in self.stocks:
            return

        assert stock_type in ['own', 'short'] , 'Stock type must be own or short.'

        del self.stocks[stock_id][stock_type][:size]
        
        if not self._broker.position.stocks[stock_id]['own'] and not self._broker.position.stocks[stock_id]['short']:
            del self._broker.position.stocks[stock_id]
            
    def close(self):
        for stock_id in self.stocks:
            if self.stocks[stock_id]['own']:
                self._broker.new_order('sell', stock_id, None, len(self.stocks[stock_id]['own']))
            if self.stocks[stock_id]['short']:
                self._broker.new_order('removeShort', stock_id, None, len(self.stocks[stock_id]['short']))


class Order:
    def __init__(self, _type, stock_id, cash_value, size, _max, broker):
        self._broker = broker
        self.stock_id = stock_id
        self.cash_value = cash_value
        self.size = size
        self._max = _max

        self._types = ['sell', 'buy', 'short', 'removeShort']
        assert _type in self._types, 'Order must be string of type' + str(self._types)
        self._type = _type

    @property
    def get_size(self):
        if self.size:
            return self.size

        if self._max:
            cash_value = self._broker.cash
        else:
            cash_value = self.cash_value
        
        price = self._broker.stock_price(self.stock_id)
        if price:
            if not self.size:
                # Get the number of shares to buy
                return int(np.floor(cash_value / price))
        else:
            return 0

    @property
    def cancel(self):
        self._broker.orders.remove(self)

    @property
    def legal(self):
        return self._broker.order_legal(self._type, self.stock_id, self.cash_value, self.size, self._max)

class Trade:
    stock_id_helper = 0

    def __init__(self, broker, size, entry_price, _type, stock_id='AAPL', opening_date=None):
        self._broker = broker
        self.size = size
        self.entry_price = entry_price
        self._type = _type
        self.curr_cash = None
        self.opening_date = opening_date
        self.stock_id = stock_id
        self.closing_date = None
    
    def current_value(self, current_price):
        return self.size * current_price

    @property
    def get_unique_id(self):
        Trade.stock_id_helper += 1
        return Trade.stock_id_helper

    @property
    def process(self):
        if (self._type == 'buy'):
            for _ in range(self.size):
                stock = Stock(self.get_unique_id, self.stock_id, 'AAPL', self._broker, 'own')
                self._broker.position.add(stock)
            self._broker.cash -= self.entry_value
            logging.info(f'{self._broker._data.iloc[-1].name}, {self._broker.value}, {self._broker.cash}, open buy, {self.size}, {self.entry_value}, {self._broker._data.Open[-1]}')

        if (self._type == 'sell'):
            self._broker.position.remove_first_i_stocks(self.stock_id, 'own', self.size)

            self._broker.cash += self.entry_value
            logging.info(f'{self._broker._data.iloc[-1].name}, {self._broker.value}, {self._broker.cash}, open sell, {self.size}, {self.entry_value}, {self._broker._data.Open[-1]}')
        
        if (self._type == 'short'):
            for _ in range(self.size):
                stock = Stock(self.get_unique_id, self.stock_id, 'AAPL', self._broker, 'short', self.entry_price)
                self._broker.position.add(stock)
            self._broker.cash -= self.entry_value
            logging.info(f'{self._broker._data.iloc[-1].name}, {self._broker.value}, {self._broker.cash}, open short, {self.size}, {self.entry_value}, {self._broker._data.Open[-1]}')
        
        if (self._type == 'removeShort'):
            for idx, stock in enumerate(self._broker.position.stocks[self.stock_id]['short']):
                if idx >= self.size:
                    break
                self._broker.cash += (stock.saved_cash * 2) - self._broker.stock_price(stock.stock_id)
            self._broker.position.remove_first_i_stocks(self.stock_id, 'short', self.size)
            logging.info(f'{self._broker._data.iloc[-1].name}, {self._broker.value}, {self._broker.cash}, open short, {self.size}, {self.entry_value}, {self._broker._data.Open[-1]}')

        self.close

    @property
    def close(self):
        self.closing_date = self._broker._data.iloc[-1].name
        self.curr_cash = self._broker.cash
        self.remove_from_trades_list()

    def remove_from_trades_list(self):
        self._broker.trades.remove(self)
        self._broker.closed_trades.append(self)

    @property
    def ret(self):
        ##Absolute return of the trade
        if self._type == 'buy':
            ret_per_share = self._broker._last_price - self.entry_price
        else:
            ret_per_share = self.entry_price - self._broker._last_price
        return self.size * ret_per_share

    @property
    def entry_value(self):
        return self.size * self.entry_price
        

class Broker:
    def __init__(self, *, data, cash, time='Open'):
        self.orders = []
        self.trades = []
        self.closed_trades = []
        self._data = data
        self.cash = cash
        self.time = time
        self.position = Position(self)

    def new_order(self, _type, stock_id, cash_value, size=None, _max=None):
        order = Order(_type, stock_id, cash_value, size, _max, self)
        self.orders.append(order)
        return True

    def order_legal(self, _type, stock_id, cash_value, size, _max):
        price = self.stock_price(stock_id)
        if not price:
            return False

        if _max:
            cash_value = self.cash

        if not size:
            # Get the number of shares to buy
            size = int(np.floor(cash_value / price))

        if size <= 0:
            return False

        if _type in ['buy', 'short']:

            if self.cash <= price * size:
                return False
            return True

        if _type in ['sell']:
            try:
                if len(self.position.stocks[stock_id]['own']) >= size:
                    return True
            except KeyError:
                pass
            return False

        if _type in ['removeShort']:
            try:
                if len(self.position.stocks[stock_id]['short']) >= size:
                    return True
            except KeyError:
                pass
            return False

        return False

    def process_orders(self):
        for order in self.orders:
            if order.legal:
                self.open_trade(order.get_size, self.stock_price(order.stock_id), order._type)
        self.orders = []

    def open_trade(self, size, current_price, trade_type):
        trade = Trade(self, size, current_price, trade_type, opening_date = self._data.iloc[-1].name)
        self.trades.append(trade)
        trade.process

    def stock_price(self, id=None):
        try:
            return self._data[self.time][-1]
        except IndexError:
            return False

    def set_time(self, time):
        self.time = time
        
    @property
    def value(self):
        out = 0
        for trade in self.trades:
            if trade._type == 'sell':
                out -= trade.current_value(self._data.Open[-1])
            else:
                out += trade.entry_value + trade.ret
        return out + self.cash
    
    @property
    def _last_price(self):
        return self._data.Close[-1]
    @property
    def _max_size(self):
        return np.floor(self.cash / self._last_price)

    
class Backtest:
    def __init__(self, data, strategy, commission=0.022, cash=100000):
        self.data = data
        self.broker = Broker(data=data, cash=cash, time='Open')
        self.strategy = strategy(broker=self.broker, data=data, cash=cash)
        self.commission = commission

    def data_extend_order_day(self, strat_order, i):
        self.data["TradeType"].iloc[i] = strat_order

    def trades_to_csv(self):
        trades = self.broker.closed_trades

        trade_frame = pd.DataFrame(columns=["Opening Date", "Closing Date", "Type", "Volume", "Cash"])

        for trade in trades:
            trade_array = pd.Series([trade.opening_date, trade.closing_date, trade._type, trade.size, trade.curr_cash], index = trade_frame.columns)
            trade_frame = trade_frame.append(trade_array, ignore_index=True)

        trade_frame.to_csv('trades.csv')

    @property
    def process_day(self):
        self.broker.set_time('Open')
        self.broker.process_orders()

        self.broker.set_time('Close')
        self.strategy.init()
        self.strategy.next()

    def run(self):
        print('Running Backtest.')
        try:
            for i in range(1, len(self.data.index)):
                data = self.data.iloc[:i]
                self.strategy.data = data
                self.broker._data = data

                self.process_day
        
            print('Saving Data.')
            self.trades_to_csv()
        
        except Exception as e:
            print('Error Detected.')
            raise e

        finally:
            print('Backtest Complete.')

    def plot(self):
        pass
