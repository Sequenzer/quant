from abc import abstractmethod, ABCMeta

class Strategy(metaclass=ABCMeta):
    def __init__(self, broker, data=None, cash=None):
        self.data = data
        self.indicators = []
        self._broker = broker
        self.order = None

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