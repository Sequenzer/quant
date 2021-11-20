from abc import abstractmethod, ABCMeta

class Strategy(metaclass=ABCMeta):
    def __init__(self, broker, data=None, cash=None):
        self.data = data
        self.indicators = {}
        self._broker = broker
        self.order = None

    def add_indicator_fkt(self, name, indicator_function, data, *args, **kwargs):
        self.indicators[name] = indicator_function(data, *args, **kwargs)

    def get_indicator_dataset(self, name):
        return self.indicators[name]

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

    def buy(self, id=None, cash=None, size=None):
        return self._broker.new_order("buy", 'AAPL', cash, size, True)

    def sell(self, id=None, cash=None, size=None):
        return self._broker.new_order("short", 'AAPL', cash, size, True)

    # def short(self, id=None, cash=None, size=None):
    #     return self._broker.new_order(self._broker.cash, "short")

    # def remove_short(self, id=None, cash=None, size=None):
    #     return self._broker.new_order(self._broker.cash, "removeShort")

    def close_position(self):
        self.position.close()

    @property
    def position(self):
        return self._broker.position

    @property
    def orders(self):
        return self._broker.orders

    @property
    def trades(self):
        return self._broker.trades