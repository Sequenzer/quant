import unittest
import numpy as np
from datetime import date

from ..strategies.test_trategy import AligatorIndicator
from ..module import Backtest
from ..run_module import datafromcsv


class Tests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Tests, self).__init__(*args, **kwargs)
        bt = Backtest(datafromcsv("AAPL", start_date=np.datetime64(date(2000, 1, 1)), end_date=np.datetime64(date(2020, 1, 1))), AligatorIndicator, commission=.002)
        self.stats = bt.run()

    def test_aapl_aligator_size(self):
        self.assertEqual(self.stats['trades'][-1].size, 360, "Apple Aligator test schould be 360")
